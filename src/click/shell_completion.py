from __future__ import annotations

import collections.abc as cabc
import os
import re
import typing as t
from gettext import gettext as _

from .core import Argument
from .core import Command
from .core import Context
from .core import Group
from .core import Option
from .core import Parameter
from .core import ParameterSource
from .parser import _split_opt
from .utils import echo


def shell_complete(
    cli: Command,
    ctx_args: cabc.MutableMapping[str, t.Any],
    prog_name: str,
    complete_var: str,
    instruction: str,
) -> t.Literal[0, 1]:
    """Perform shell completion for the given CLI program.

    :param cli: Command being called.
    :param ctx_args: Extra arguments to pass to
        ``cli.make_context``.
    :param prog_name: Name of the executable in the shell.
    :param complete_var: Name of the environment variable that holds
        the completion instruction.
    :param instruction: Value of ``complete_var`` with the completion
        instruction and shell, in the form ``instruction_shell``.
    :return: Status code to exit with.
    """
    shell, _, instruction = instruction.partition("_")
    comp_cls = get_completion_class(shell)

    if comp_cls is None:
        return 1

    comp = comp_cls(cli, ctx_args, prog_name, complete_var)

    # Write bytes, otherwise Windows text stdout translates LF to CRLF and breaks.
    if instruction == "source":
        echo(comp.source().encode(), nl=False)
        return 0

    if instruction == "complete":
        echo(comp.complete().encode())
        return 0

    return 1


if t.TYPE_CHECKING:
    from typing_extensions import TypeVar

    # `Any` is used as default for backwards compatibility (instead of e.g. `str`)
    _ValueT_co = TypeVar("_ValueT_co", covariant=True, default=t.Any)
else:
    _ValueT_co = t.TypeVar("_ValueT_co", covariant=True)


class CompletionItem(t.Generic[_ValueT_co]):
    """Represents a completion value and metadata about the value. The
    default metadata is ``type`` to indicate special shell handling,
    and ``help`` if a shell supports showing a help string next to the
    value.

    Arbitrary parameters can be passed when creating the object, and
    accessed using ``item.attr``. If an attribute wasn't passed,
    accessing it returns ``None``.

    :param value: The completion suggestion.
    :param type: Tells the shell script to provide special completion
        support for the type. Click uses ``"dir"`` and ``"file"``.
    :param help: String shown next to the value if supported.
    :param kwargs: Arbitrary metadata. The built-in implementations
        don't use this, but custom type completions paired with custom
        shell support could use it.
    """

    __slots__ = ("value", "type", "help", "_info")

    def __init__(
        self,
        value: _ValueT_co,
        type: str = "plain",
        help: str | None = None,
        **kwargs: t.Any,
    ) -> None:
        self.value: _ValueT_co = value
        self.type: str = type
        self.help: str | None = help
        self._info = kwargs

    def __getattr__(self, name: str) -> t.Any:
        return self._info.get(name)


# Only Bash >= 4.4 has the nosort option.
_SOURCE_BASH = """\
%(complete_func)s() {
    local IFS=$'\\n'
    local response
    local quoted=${COMP_WORDS[COMP_CWORD]:0:1}
    local escaped char i

    response=$(env COMP_WORDS="${COMP_WORDS[*]}" COMP_CWORD=$COMP_CWORD \
COMP_LINE="$COMP_LINE" COMP_POINT="$COMP_POINT" \
%(complete_var)s=bash_complete $1)

    for completion in $response; do
        IFS=',' read -r type value <<< "$completion"

        if [[ $type == 'dir' ]]; then
            COMPREPLY=()
            compopt -o dirnames
        elif [[ $type == 'file' ]]; then
            COMPREPLY=()
            compopt -o default
        elif [[ $type == 'plain' ]]; then
            # Bash inserts a reply literally. Escape it for the quotes the
            # word was opened with, or escape spaces and other special
            # characters if it isn't quoted, so the value stays one argument.
            if [[ $quoted == [\\'\\"] ]]; then
                escaped=''

                for (( i = 0; i < ${#value}; i++ )); do
                    char=${value:i:1}

                    case $quoted$char in
                        "''") escaped+="'\\''" ;;
                        '"\\'|'"$'|'"`'|'""') escaped+="\\\\$char" ;;
                        *) escaped+=$char ;;
                    esac
                done

                value=$escaped
            else
                printf -v value '%%q' "$value"
            fi

            COMPREPLY+=("$value")
        fi
    done

    return 0
}

%(complete_func)s_setup() {
    complete -o nosort -F %(complete_func)s %(prog_name)s
}

%(complete_func)s_setup;
"""

# See ZshComplete.format_completion below, and issue #2703, before
# changing this script.
#
# (TL;DR: _describe is picky about the format, but this Zsh script snippet
# is already widely deployed.  So freeze this script, and use clever-ish
# handling of colons in ZshComplet.format_completion.)
_SOURCE_ZSH = """\
#compdef %(prog_name)s

%(complete_func)s() {
    local -a completions
    local -a completions_with_descriptions
    local -a response
    (( ! $+commands[%(prog_name)s] )) && return 1

    response=("${(@f)$(env COMP_WORDS="${words[*]}" COMP_CWORD=$((CURRENT-1)) \
%(complete_var)s=zsh_complete %(prog_name)s)}")

    for type key descr in "${response[@]}"; do
        if [[ "$type" == "plain" ]]; then
            if [[ "$descr" == "_" ]]; then
                completions+=("$key")
            else
                completions_with_descriptions+=("$key":"$descr")
            fi
        elif [[ "$type" == "dir" || "$type" == "file" ]]; then
            # A path given as --name=path is completed after the "=".
            if [[ "$PREFIX" == ?*"=$key" ]]; then
                compset -P 1 '*='
            fi

            if [[ "$type" == "dir" ]]; then
                _path_files -/
            else
                _path_files -f
            fi
        fi
    done

    if [ -n "$completions_with_descriptions" ]; then
        _describe -V unsorted completions_with_descriptions -U
    fi

    if [ -n "$completions" ]; then
        compadd -U -V unsorted -a completions
    fi
}

if [[ $zsh_eval_context[-1] == loadautofunc ]]; then
    # autoload from fpath, call function directly
    %(complete_func)s "$@"
else
    # eval/source/. command, register function for later
    compdef %(complete_func)s %(prog_name)s
fi
"""

_SOURCE_FISH = """\
function %(complete_func)s;
    set -l response (env %(complete_var)s=fish_complete COMP_WORDS=(commandline -cp) \
COMP_CWORD=(commandline -t) %(prog_name)s);

    for completion in $response;
        set -l metadata (string split "," $completion);

        if test $metadata[1] = "dir";
            __fish_complete_directories $metadata[2];
        else if test $metadata[1] = "file";
            __fish_complete_path $metadata[2];
        else if test $metadata[1] = "plain";
            echo $metadata[2];
        end;
    end;
end;

complete --no-files --command %(prog_name)s --arguments \
"(%(complete_func)s)";
"""

# Compatible with Windows PowerShell 5.1+ and PowerShell (pwsh) 7+.
# Uses Register-ArgumentCompleter -Native, which receives the command AST
# as parsed by PowerShell. The command text is forwarded verbatim through
# COMP_WORDS so the Python side can reuse the same shlex-based splitting
# used by the bash/zsh completers.
_SOURCE_POWERSHELL = """\
Register-ArgumentCompleter -Native -CommandName %(prog_name)s -ScriptBlock {
    param($wordToComplete, $commandAst, $cursorPosition)

    $prev_complete = $env:%(complete_var)s
    $prev_words = $env:COMP_WORDS
    $prev_cword = $env:COMP_CWORD

    $env:%(complete_var)s = 'powershell_complete'
    $env:COMP_WORDS = $commandAst.ToString()
    if ($wordToComplete) {
        $env:COMP_CWORD = $commandAst.CommandElements.Count - 1
    } else {
        $env:COMP_CWORD = $commandAst.CommandElements.Count
    }

    try {
        $response = & %(prog_name)s 2>$null
    } finally {
        $env:%(complete_var)s = $prev_complete
        $env:COMP_WORDS = $prev_words
        $env:COMP_CWORD = $prev_cword
    }

    if (-not $response) { return }

    $prefix = "$wordToComplete*"
    $lines = $response -split "`n"
    for ($i = 0; $i + 2 -lt $lines.Count; $i += 3) {
        $type = $lines[$i]
        $value = $lines[$i + 1]
        $descr = $lines[$i + 2]
        if (-not $type) { continue }

        if ($type -eq 'plain') {
            $tip = if ($descr -and $descr -ne '_') { $descr } else { $value }
            [System.Management.Automation.CompletionResult]::new(
                $value, $value, 'ParameterValue', $tip)
        } elseif ($type -eq 'dir') {
            Get-ChildItem -Directory -Path $prefix -ErrorAction SilentlyContinue |
                ForEach-Object {
                    [System.Management.Automation.CompletionResult]::new(
                        $_.FullName, $_.Name, 'ProviderContainer', $_.FullName)
                }
        } elseif ($type -eq 'file') {
            Get-ChildItem -Path $prefix -ErrorAction SilentlyContinue |
                ForEach-Object {
                    $kind = 'ProviderItem'
                    if ($_.PSIsContainer) { $kind = 'ProviderContainer' }
                    [System.Management.Automation.CompletionResult]::new(
                        $_.FullName, $_.Name, $kind, $_.FullName)
                }
        }
    }
}
"""


class _SourceVarsDict(t.TypedDict):
    complete_func: str
    complete_var: str
    prog_name: str


class ShellComplete:
    """Base class for providing shell completion support. A subclass for
    a given shell will override attributes and methods to implement the
    completion instructions (``source`` and ``complete``).

    :param cli: Command being called.
    :param prog_name: Name of the executable in the shell.
    :param complete_var: Name of the environment variable that holds
        the completion instruction.

    .. versionadded:: 8.0
    """

    name: t.ClassVar[str]
    """Name to register the shell as with :func:`add_completion_class`.
    This is used in completion instructions (``{name}_source`` and
    ``{name}_complete``).
    """

    source_template: t.ClassVar[str]
    """Completion script template formatted by :meth:`source`. This must
    be provided by subclasses.
    """

    cli: Command
    ctx_args: cabc.MutableMapping[str, t.Any]
    prog_name: str
    complete_var: str

    def __init__(
        self,
        cli: Command,
        ctx_args: cabc.MutableMapping[str, t.Any],
        prog_name: str,
        complete_var: str,
    ) -> None:
        self.cli = cli
        self.ctx_args = ctx_args
        self.prog_name = prog_name
        self.complete_var = complete_var

    @property
    def func_name(self) -> str:
        """The name of the shell function defined by the completion
        script.
        """
        safe_name = re.sub(r"\W*", "", self.prog_name.replace("-", "_"), flags=re.ASCII)
        return f"_{safe_name}_completion"

    def source_vars(self) -> _SourceVarsDict:
        """Vars for formatting :attr:`source_template`.

        By default this provides ``complete_func``, ``complete_var``,
        and ``prog_name``.
        """
        return {
            "complete_func": self.func_name,
            "complete_var": self.complete_var,
            "prog_name": self.prog_name,
        }

    def source(self) -> str:
        """Produce the shell script that defines the completion
        function. By default this ``%``-style formats
        :attr:`source_template` with the dict returned by
        :meth:`source_vars`.
        """
        return self.source_template % self.source_vars()

    def get_completion_args(self) -> tuple[list[str], str]:
        """Use the env vars defined by the shell script to return a
        tuple of ``args, incomplete``. This must be implemented by
        subclasses.
        """
        raise NotImplementedError

    def get_completions(
        self, args: list[str], incomplete: str
    ) -> list[CompletionItem[str]]:
        """Determine the context and last complete command or parameter
        from the complete args. Call that object's ``shell_complete``
        method to get the completions for the incomplete value.

        :param args: List of complete args before the incomplete value.
        :param incomplete: Value being completed. May be empty.
        """
        ctx = _resolve_context(self.cli, self.ctx_args, self.prog_name, args)
        obj, incomplete = _resolve_incomplete(ctx, args, incomplete)
        return obj.shell_complete(ctx, incomplete)

    def format_completion(self, item: CompletionItem[str]) -> str:
        """Format a completion item into the form recognized by the
        shell script. This must be implemented by subclasses.

        :param item: Completion item to format.
        """
        raise NotImplementedError

    def complete(self) -> str:
        """Produce the completion data to send back to the shell.

        By default this calls :meth:`get_completion_args`, gets the
        completions, then calls :meth:`format_completion` for each
        completion.
        """
        args, incomplete = self.get_completion_args()
        completions = self.get_completions(args, incomplete)
        out = [self.format_completion(item) for item in completions]
        return "\n".join(out)


class BashComplete(ShellComplete):
    """Shell completion for Bash."""

    name: t.ClassVar[str] = "bash"
    source_template: t.ClassVar[str] = _SOURCE_BASH

    @staticmethod
    def _check_version() -> None:
        import shutil
        import subprocess

        bash_exe = shutil.which("bash")

        if bash_exe is None:
            match = None
        else:
            output = subprocess.run(
                [bash_exe, "--norc", "-c", 'echo "${BASH_VERSION}"'],
                stdout=subprocess.PIPE,
            )
            match = re.search(r"^(\d+)\.(\d+)\.\d+", output.stdout.decode())

        if match is not None:
            major, minor = match.groups()

            if major < "4" or major == "4" and minor < "4":
                echo(
                    _(
                        "Shell completion is not supported for Bash"
                        " versions older than 4.4."
                    ),
                    err=True,
                )
        else:
            echo(
                _("Couldn't detect Bash version, shell completion is not supported."),
                err=True,
            )

    def source(self) -> str:
        self._check_version()
        return super().source()

    _typed_word: tuple[str, str] | None = None
    """The incomplete word from :meth:`get_completion_args`, and its start
    that Bash keeps when it inserts a completion.
    """

    def get_completion_args(self) -> tuple[list[str], str]:
        """
        .. versionchanged:: 8.6.0
            The words are split from ``COMP_LINE`` before ``COMP_POINT`` like
            the shell splits them, if the script passes them. Otherwise, an
            option name split from its value at an ``=`` word break is joined
            back together.
        """
        cwords = split_arg_string(os.environ["COMP_WORDS"])
        cword = int(os.environ["COMP_CWORD"])
        args = cwords[1:cword]

        try:
            incomplete = cwords[cword]
        except IndexError:
            incomplete = ""

        # Bash replaces only the current word, and not "=" or ":" word
        # breaks that the cursor directly follows.
        replaced = "" if incomplete and not incomplete.strip("=:") else incomplete
        line_words = self._get_line_words(cwords, cword)

        if line_words is not None and line_words[-1].endswith(replaced):
            *args, incomplete = line_words
        else:
            *args, incomplete = _join_option_values([*args, incomplete])

        self._typed_word = (incomplete, incomplete[: len(incomplete) - len(replaced)])
        return args, incomplete

    @staticmethod
    def _get_line_words(cwords: list[str], cword: int) -> list[str] | None:
        """Split ``COMP_LINE`` before ``COMP_POINT`` into the shell words after
        the program name, the last being the incomplete word. Bash also splits
        ``COMP_WORDS`` at the characters in ``COMP_WORDBREAKS``, such as ``=``
        in a value, but the program receives the shell words.

        Return ``None`` if the line wasn't passed, or doesn't have the same
        text as ``COMP_WORDS``.

        :param cwords: The split ``COMP_WORDS``.
        :param cword: The index of the current word in ``COMP_WORDS``.
        """
        line = os.environ.get("COMP_LINE")
        point = os.environ.get("COMP_POINT")

        if line is None or point is None or not point.isdigit():
            return None

        index = int(point)

        if index > len(line):
            return None

        words = _split_shell_words(line[:index])[1:]

        if not words or "".join(words) != "".join(cwords[1 : cword + 1]):
            return None

        return words

    def get_completions(
        self, args: list[str], incomplete: str
    ) -> list[CompletionItem[str]]:
        """
        .. versionchanged:: 8.6.0
            The values for an option given as ``--name=value`` include the
            part of the word that Bash doesn't replace, such as ``--name=``
            if ``COMP_WORDBREAKS`` doesn't contain ``=``.
        """
        items = _get_completions_keeping_option(self, args, incomplete)

        if self._typed_word is None or self._typed_word[0] != incomplete:
            return items

        kept = self._typed_word[1]

        if not kept:
            return items

        return [
            _with_value(item, item.value[len(kept) :])
            if item.type == "plain"
            and isinstance(item.value, str)
            and item.value.startswith(kept)
            else item
            for item in items
        ]

    def format_completion(self, item: CompletionItem[t.Any]) -> str:
        return f"{item.type},{item.value}"


class ZshComplete(ShellComplete):
    """Shell completion for Zsh."""

    name: t.ClassVar[str] = "zsh"
    source_template: t.ClassVar[str] = _SOURCE_ZSH

    def get_completion_args(self) -> tuple[list[str], str]:
        cwords = split_arg_string(os.environ["COMP_WORDS"])
        cword = int(os.environ["COMP_CWORD"])
        args = cwords[1:cword]

        try:
            incomplete = cwords[cword]
        except IndexError:
            incomplete = ""

        return args, incomplete

    def get_completions(
        self, args: list[str], incomplete: str
    ) -> list[CompletionItem[str]]:
        """
        .. versionchanged:: 8.6.0
            The values for an option given as ``--name=value`` include the
            ``--name=`` prefix, as Zsh replaces the whole word.
        """
        return _get_completions_keeping_option(self, args, incomplete)

    def format_completion(self, item: CompletionItem[str]) -> str:
        help_ = item.help or "_"
        # The zsh completion script uses `_describe` on items with help
        # texts (which splits the item help from the item value at the
        # first unescaped colon) and `compadd` on items without help
        # text (which uses the item value as-is and does not support
        # colon escaping).  So escape colons in the item value if and
        # only if the item help is not the sentinel "_" value, as used
        # by the completion script.
        #
        # (The zsh completion script is potentially widely deployed, and
        # thus harder to fix than this method.)
        #
        # See issue #1812 and issue #2703 for further context.
        value = item.value.replace(":", r"\:") if help_ != "_" else item.value
        return f"{item.type}\n{value}\n{help_}"


class FishComplete(ShellComplete):
    """Shell completion for Fish."""

    name: t.ClassVar[str] = "fish"
    source_template: t.ClassVar[str] = _SOURCE_FISH

    def get_completion_args(self) -> tuple[list[str], str]:
        cwords = split_arg_string(os.environ["COMP_WORDS"])
        incomplete = os.environ["COMP_CWORD"]
        if incomplete:
            incomplete = split_arg_string(incomplete)[0]
        args = cwords[1:]

        # Fish stores the partial word in both COMP_WORDS and
        # COMP_CWORD, remove it from complete args.
        if incomplete and args and args[-1] == incomplete:
            args.pop()

        return args, incomplete

    def format_completion(self, item: CompletionItem[str]) -> str:
        """
        .. versionchanged:: 8.4.2
            Escape newlines and replace tabs with spaces in the help text to
            fix completion errors with multi-line help strings.
        """
        # According to https://fishshell.com/docs/current/cmds/complete.html
        # Command substitutions found in ARGUMENTS should return a newline-
        # separated list of arguments, and each argument may optionally have a tab
        # character followed by the argument description.
        if item.help:
            help_ = item.help.replace("\n", "\\n").replace("\t", " ")
            return f"{item.type},{item.value}\t{help_}"

        return f"{item.type},{item.value}"


class PowerShellComplete(ShellComplete):
    """Shell completion for PowerShell (Windows PowerShell 5.1+ and pwsh 7+).

    .. versionadded:: 8.5.0
    """

    name: t.ClassVar[str] = "powershell"
    source_template: t.ClassVar[str] = _SOURCE_POWERSHELL

    def get_completion_args(self) -> tuple[list[str], str]:
        cwords = split_arg_string(os.environ["COMP_WORDS"])
        cword = int(os.environ["COMP_CWORD"])
        args = cwords[1:cword]

        try:
            incomplete = cwords[cword]
        except IndexError:
            incomplete = ""

        return args, incomplete

    def format_completion(self, item: CompletionItem[str]) -> str:
        # PowerShell parses the response by splitting on newlines and
        # consuming three lines per completion (type, value, help).
        # Multi-line help text would break that framing, so collapse
        # newlines and carriage returns to spaces. The literal "_"
        # sentinel matches what ZshComplete uses for "no help text".
        if item.help:
            help_ = item.help.replace("\r", " ").replace("\n", " ")
        else:
            help_ = "_"
        return f"{item.type}\n{item.value}\n{help_}"


_available_shells: t.Final[dict[str, type[ShellComplete]]] = {
    "bash": BashComplete,
    "fish": FishComplete,
    "powershell": PowerShellComplete,
    "zsh": ZshComplete,
}

_ShellCompleteT = t.TypeVar("_ShellCompleteT", bound="ShellComplete")


def add_completion_class(
    cls: type[_ShellCompleteT], name: str | None = None
) -> type[_ShellCompleteT]:
    """Register a :class:`ShellComplete` subclass under the given name.
    The name will be provided by the completion instruction environment
    variable during completion.

    :param cls: The completion class that will handle completion for the
        shell.
    :param name: Name to register the class under. Defaults to the
        class's ``name`` attribute.
    """
    if name is None:
        name = cls.name

    _available_shells[name] = cls

    return cls


@t.overload
def get_completion_class(shell: t.Literal["bash"]) -> type[BashComplete]: ...
@t.overload
def get_completion_class(shell: t.Literal["fish"]) -> type[FishComplete]: ...
@t.overload
def get_completion_class(shell: t.Literal["zsh"]) -> type[ZshComplete]: ...
@t.overload
def get_completion_class(shell: str) -> type[ShellComplete] | None: ...
def get_completion_class(shell: str) -> type[ShellComplete] | None:
    """Look up a registered :class:`ShellComplete` subclass by the name
    provided by the completion instruction environment variable. If the
    name isn't registered, returns ``None``.

    :param shell: Name the class is registered under.
    """
    return _available_shells.get(shell)


def split_arg_string(string: str) -> list[str]:
    """Split an argument string as with :func:`shlex.split`, but don't
    fail if the string is incomplete. Ignores a missing closing quote or
    incomplete escape sequence and uses the partial token as-is.

    .. code-block:: python

        split_arg_string("example 'my file")
        ["example", "my file"]

        split_arg_string("example my\\")
        ["example", "my"]

    :param string: String to split.

    .. versionchanged:: 8.2
        Moved to ``shell_completion`` from ``parser``.
    """
    import shlex

    lex = shlex.shlex(string, posix=True)
    lex.whitespace_split = True
    lex.commenters = ""
    out: list[str] = []

    try:
        out.extend(lex)
    except ValueError:
        # Raised when end-of-string is reached in an invalid state. Use
        # the partial token as-is. The quote or escape character is in
        # lex.state, not lex.token.
        out.append(lex.token)

    return out


def _is_incomplete_argument(ctx: Context, param: Parameter) -> bool:
    """Determine if the given parameter is an argument that can still
    accept values.

    :param ctx: Invocation context for the command represented by the
        parsed complete args.
    :param param: Argument object being checked.
    """
    if not isinstance(param, Argument):
        return False

    value = ctx.params.get(param.name)
    return (
        param.nargs == -1
        or ctx.get_parameter_source(param.name) is not ParameterSource.COMMANDLINE
        or (
            param.nargs > 1
            and isinstance(value, (tuple, list))
            and len(value) < param.nargs
        )
    )


def _start_of_option(ctx: Context, value: str) -> bool:
    """Check if the value looks like the start of an option."""
    if not value:
        return False

    c = value[0]
    return c in ctx._opt_prefixes


def _is_incomplete_option(ctx: Context, args: list[str], param: Parameter) -> bool:
    """Determine if the given parameter is an option that needs a value.

    :param args: List of complete args before the incomplete value.
    :param param: Option object being checked.
    """
    if not isinstance(param, Option):
        return False

    if param.is_flag or param.count:
        return False

    last_option = None

    for index, arg in enumerate(reversed(args)):
        if index + 1 > param.nargs:
            break

        if _start_of_option(ctx, arg):
            last_option = arg
            break

    return last_option is not None and last_option in param.opts


def _resolve_context(
    cli: Command,
    ctx_args: cabc.MutableMapping[str, t.Any],
    prog_name: str,
    args: list[str],
) -> Context:
    """Produce the context hierarchy starting with the command and
    traversing the complete arguments. This only follows the commands,
    it doesn't trigger input prompts or callbacks.

    :param cli: Command being called.
    :param prog_name: Name of the executable in the shell.
    :param args: List of complete args before the incomplete value.
    """
    ctx_args["resilient_parsing"] = True
    with cli.make_context(prog_name, args.copy(), **ctx_args) as ctx:
        args = ctx._protected_args + ctx.args

        while args:
            command = ctx.command

            if isinstance(command, Group):
                if not command.chain:
                    name, cmd, args = command.resolve_command(ctx, args)

                    if cmd is None:
                        return ctx

                    with cmd.make_context(
                        name, args, parent=ctx, resilient_parsing=True
                    ) as sub_ctx:
                        ctx = sub_ctx
                        args = ctx._protected_args + ctx.args
                else:
                    sub_ctx = ctx

                    while args:
                        name, cmd, args = command.resolve_command(ctx, args)

                        if cmd is None:
                            return ctx

                        with cmd.make_context(
                            name,
                            args,
                            parent=ctx,
                            allow_extra_args=True,
                            allow_interspersed_args=False,
                            resilient_parsing=True,
                        ) as sub_sub_ctx:
                            sub_ctx = sub_sub_ctx
                            args = sub_ctx.args

                    ctx = sub_ctx
                    args = [*sub_ctx._protected_args, *sub_ctx.args]
            else:
                break

    return ctx


def _resolve_incomplete(
    ctx: Context, args: list[str], incomplete: str
) -> tuple[Command | Parameter, str]:
    """Find the Click object that will handle the completion of the
    incomplete value. Return the object and the incomplete value.

    :param ctx: Invocation context for the command represented by
        the parsed complete args.
    :param args: List of complete args before the incomplete value.
    :param incomplete: Value being completed. May be empty.
    """
    # Different shells treat an "=" between a long option name and
    # value differently. Might keep the value joined, return the "="
    # as a separate item, or return the split name and value. Always
    # split and discard the "=" to make completion easier. Like the
    # parser, don't split a short option name, the value of "-c=al" is
    # "=al".
    if incomplete == "=":
        incomplete = ""
    elif "=" in incomplete and _start_of_option(ctx, incomplete):
        name, _, value = incomplete.partition("=")

        if not _is_short_option_name(name):
            args.append(name)
            incomplete = value

    # The "--" marker tells Click to stop treating values as options
    # even if they start with the option character. If it hasn't been
    # given and the incomplete arg looks like an option, the current
    # command will provide option name completions.
    if "--" not in args and _start_of_option(ctx, incomplete):
        return ctx.command, incomplete

    params = ctx.command.get_params(ctx)

    # If the last complete arg is an option name with an incomplete
    # value, the option will provide value completions.
    for param in params:
        if _is_incomplete_option(ctx, args, param):
            return param, incomplete

    # It's not an option name or value. The first argument without a
    # parsed value will provide value completions.
    for param in params:
        if _is_incomplete_argument(ctx, param):
            return param, incomplete

    # There were no unparsed arguments, the command may be a group that
    # will provide command name completions.
    return ctx.command, incomplete


def _is_short_option_name(name: str) -> bool:
    """Check if an option name is a short name like ``-c``, which the parser
    never splits from an attached value at ``=``.
    """
    prefix, rest = _split_opt(name)
    return len(prefix) == 1 and len(rest) == 1


def _split_shell_words(line: str) -> list[str]:
    """Split a command line into words with quotes and escapes removed, like
    the shell does. The last word is the incomplete word, which is empty if
    the line ends with whitespace. An unclosed quote or a trailing backslash
    is ignored.

    :param line: The command line up to the cursor.
    """
    words: list[str] = []
    word: list[str] = []
    in_word = False
    quote = ""
    chars = iter(line)

    for char in chars:
        if quote == "'":
            if char == "'":
                quote = ""
            else:
                word.append(char)
        elif quote == '"':
            if char == '"':
                quote = ""
            elif char == "\\":
                escaped = next(chars, "")

                if escaped not in '\\"$`\n':
                    word.append(char)

                if escaped != "\n":
                    word.append(escaped)
            else:
                word.append(char)
        elif char == "\\":
            in_word = True
            escaped = next(chars, "")

            if escaped != "\n":
                word.append(escaped)
        elif char in " \t\n":
            if in_word:
                words.append("".join(word))
                word = []
                in_word = False
        else:
            in_word = True

            if char in "'\"":
                quote = char
            else:
                word.append(char)

    words.append("".join(word))
    return words


def _join_option_values(words: list[str]) -> list[str]:
    """Join an option name and its value that Bash split into separate words.

    Bash splits the words it passes to completion at the characters in
    ``COMP_WORDBREAKS``, which contains ``=`` by default, so ``--name=value``
    arrives as the three words ``--name``, ``=``, and ``value``. Join an ``=``
    word that follows an option name back onto it, along with the value after
    it. Values containing ``=`` are split again, so they are joined as well.

    :param words: Words after the program name, including the incomplete
        word last.
    """
    out: list[str] = []
    joining = False

    for word in words:
        if joining:
            out[-1] += word
            joining = word == "="
        elif word == "=" and out and _looks_like_option(out[-1]):
            out[-1] += word
            joining = True
        else:
            out.append(word)

    return out


def _looks_like_option(word: str) -> bool:
    """Check if a word looks like an option name, before the context that
    knows the actual option prefixes is resolved.
    """
    return len(word) > 1 and not word[0].isalnum() and word[0] != "="


def _with_value(item: CompletionItem[t.Any], value: str) -> CompletionItem[str]:
    """Copy a completion item with a different value."""
    return CompletionItem(value, type=item.type, help=item.help, **item._info)


def _get_completions_keeping_option(
    comp: ShellComplete, args: list[str], incomplete: str
) -> list[CompletionItem[str]]:
    """Get completions like :meth:`ShellComplete.get_completions`, but if the
    incomplete word is an option name with an attached value, such as
    ``--name=val``, prefix each value completion with ``--name=``. A shell that
    replaces the whole incomplete word with the completion then keeps the
    option name.

    :param comp: The shell completion instance.
    :param args: List of complete args before the incomplete value.
    :param incomplete: Value being completed. May be empty.
    """
    ctx = _resolve_context(comp.cli, comp.ctx_args, comp.prog_name, args)
    obj, value = _resolve_incomplete(ctx, args, incomplete)
    items = obj.shell_complete(ctx, value)
    name, sep, _ = incomplete.partition("=")

    if not sep or not isinstance(obj, Option) or name not in obj.opts:
        return items

    return [
        _with_value(item, f"{name}={item.value}") if item.type == "plain" else item
        for item in items
    ]
