import io
import shlex
import shutil
import subprocess
import textwrap
import warnings
from collections.abc import Mapping

import pytest

import click.shell_completion
from click.core import Argument
from click.core import Command
from click.core import Group
from click.core import Option
from click.shell_completion import add_completion_class
from click.shell_completion import CompletionItem
from click.shell_completion import FishComplete
from click.shell_completion import PowerShellComplete
from click.shell_completion import shell_complete
from click.shell_completion import ShellComplete
from click.types import Choice
from click.types import File
from click.types import Path


def _get_completions(cli, args, incomplete):
    comp = ShellComplete(cli, {}, cli.name, "_CLICK_COMPLETE")
    return comp.get_completions(args, incomplete)


def _get_words(cli, args, incomplete):
    return [c.value for c in _get_completions(cli, args, incomplete)]


def test_command():
    cli = Command("cli", params=[Option(["-t", "--test"])])
    assert _get_words(cli, [], "") == []
    assert _get_words(cli, [], "-") == ["-t", "--test", "--help"]
    assert _get_words(cli, [], "--") == ["--test", "--help"]
    assert _get_words(cli, [], "--t") == ["--test"]
    # -t has been seen, so --test isn't suggested
    assert _get_words(cli, ["-t", "a"], "-") == ["--help"]


def test_group():
    cli = Group("cli", params=[Option(["-a"])], commands=[Command("x"), Command("y")])
    assert _get_words(cli, [], "") == ["x", "y"]
    assert _get_words(cli, [], "-") == ["-a", "--help"]


@pytest.mark.parametrize(
    ("args", "word", "expect"),
    [
        ([], "", ["get"]),
        (["get"], "", ["full"]),
        (["get", "full"], "", ["data"]),
        (["get", "full"], "-", ["--verbose", "--help"]),
        (["get", "full", "data"], "", []),
        (["get", "full", "data"], "-", ["-a", "--help"]),
    ],
)
def test_nested_group(args: list[str], word: str, expect: list[str]) -> None:
    cli = Group(
        "cli",
        commands=[
            Group(
                "get",
                commands=[
                    Group(
                        "full",
                        params=[Option(["--verbose"])],
                        commands=[Command("data", params=[Option(["-a"])])],
                    )
                ],
            )
        ],
    )
    assert _get_words(cli, args, word) == expect


def test_group_command_same_option():
    cli = Group(
        "cli", params=[Option(["-a"])], commands=[Command("x", params=[Option(["-a"])])]
    )
    assert _get_words(cli, [], "-") == ["-a", "--help"]
    assert _get_words(cli, ["-a", "a"], "-") == ["--help"]
    assert _get_words(cli, ["-a", "a", "x"], "-") == ["-a", "--help"]
    assert _get_words(cli, ["-a", "a", "x", "-a", "a"], "-") == ["--help"]


def test_chained():
    cli = Group(
        "cli",
        chain=True,
        commands=[
            Command("set", params=[Option(["-y"])]),
            Command("start"),
            Group("get", commands=[Command("full")]),
        ],
    )
    assert _get_words(cli, [], "") == ["get", "set", "start"]
    assert _get_words(cli, [], "s") == ["set", "start"]
    assert _get_words(cli, ["set", "start"], "") == ["get"]
    # subcommands and parent subcommands
    assert _get_words(cli, ["get"], "") == ["full", "set", "start"]
    assert _get_words(cli, ["get", "full"], "") == ["set", "start"]
    assert _get_words(cli, ["get"], "s") == ["set", "start"]


def test_help_option():
    cli = Group("cli", commands=[Command("with"), Command("no", add_help_option=False)])
    assert _get_words(cli, ["with"], "--") == ["--help"]
    assert _get_words(cli, ["no"], "--") == []


def test_argument_order():
    cli = Command(
        "cli",
        params=[
            Argument(["plain"]),
            Argument(["c1"], type=Choice(["a1", "a2", "b"])),
            Argument(["c2"], type=Choice(["c1", "c2", "d"])),
        ],
    )
    # first argument has no completions
    assert _get_words(cli, [], "") == []
    assert _get_words(cli, [], "a") == []
    # first argument filled, now completion can happen
    assert _get_words(cli, ["x"], "a") == ["a1", "a2"]
    assert _get_words(cli, ["x", "b"], "d") == ["d"]


def test_argument_default():
    cli = Command(
        "cli",
        add_help_option=False,
        params=[
            Argument(["a"], type=Choice(["a"]), default="a"),
            Argument(["b"], type=Choice(["b"]), default="b"),
        ],
    )
    assert _get_words(cli, [], "") == ["a"]
    assert _get_words(cli, ["a"], "b") == ["b"]
    # ignore type validation
    assert _get_words(cli, ["x"], "b") == ["b"]


def test_type_choice():
    cli = Command("cli", params=[Option(["-c"], type=Choice(["a1", "a2", "b"]))])
    assert _get_words(cli, ["-c"], "") == ["a1", "a2", "b"]
    assert _get_words(cli, ["-c"], "a") == ["a1", "a2"]
    assert _get_words(cli, ["-c"], "a2") == ["a2"]


def test_choice_special_characters():
    cli = Command("cli", params=[Option(["-c"], type=Choice(["!1", "!2", "+3"]))])
    assert _get_words(cli, ["-c"], "") == ["!1", "!2", "+3"]
    assert _get_words(cli, ["-c"], "!") == ["!1", "!2"]
    assert _get_words(cli, ["-c"], "!2") == ["!2"]


def test_choice_conflicting_prefix():
    cli = Command(
        "cli",
        params=[
            Option(["-c"], type=Choice(["!1", "!2", "+3"])),
            Option(["+p"], is_flag=True),
        ],
    )
    assert _get_words(cli, ["-c"], "") == ["!1", "!2", "+3"]
    assert _get_words(cli, ["-c"], "+") == ["+p"]


def test_option_count():
    cli = Command("cli", params=[Option(["-c"], count=True)])
    assert _get_words(cli, ["-c"], "") == []
    assert _get_words(cli, ["-c"], "-") == ["--help"]


def test_option_optional():
    cli = Command(
        "cli",
        add_help_option=False,
        params=[
            Option(["--name"], is_flag=False, flag_value="value"),
            Option(["--flag"], is_flag=True),
        ],
    )
    assert _get_words(cli, ["--name"], "") == []
    assert _get_words(cli, ["--name"], "-") == ["--flag"]
    assert _get_words(cli, ["--name", "--flag"], "-") == []


@pytest.mark.parametrize(
    ("type", "expect"),
    [(File(), "file"), (Path(), "file"), (Path(file_okay=False), "dir")],
)
def test_path_types(type, expect):
    cli = Command("cli", params=[Option(["-f"], type=type)])
    out = _get_completions(cli, ["-f"], "ab")
    assert len(out) == 1
    c = out[0]
    assert c.value == "ab"
    assert c.type == expect


def test_absolute_path():
    cli = Command("cli", params=[Option(["-f"], type=Path())])
    out = _get_completions(cli, ["-f"], "/ab")
    assert len(out) == 1
    c = out[0]
    assert c.value == "/ab"


def test_option_flag():
    cli = Command(
        "cli",
        add_help_option=False,
        params=[
            Option(["--on/--off"]),
            Argument(["a"], type=Choice(["a1", "a2", "b"])),
        ],
    )
    assert _get_words(cli, [], "--") == ["--on", "--off"]
    # flag option doesn't take value, use choice argument
    assert _get_words(cli, ["--on"], "a") == ["a1", "a2"]


def test_flag_option_with_nargs_option():
    cli = Command(
        "cli",
        add_help_option=False,
        params=[
            Argument(["a"], type=Choice(["a1", "a2", "b"])),
            Option(["--flag"], is_flag=True),
            Option(["-c"], type=Choice(["p", "q"]), nargs=2),
        ],
    )
    assert _get_words(cli, ["a1", "--flag", "-c"], "") == ["p", "q"]


def test_option_custom():
    def custom(ctx, param, incomplete):
        return [incomplete.upper()]

    cli = Command(
        "cli",
        params=[
            Argument(["x"]),
            Argument(["y"]),
            Argument(["z"], shell_complete=custom),
        ],
    )
    assert _get_words(cli, ["a", "b"], "") == [""]
    assert _get_words(cli, ["a", "b"], "c") == ["C"]


def test_option_multiple():
    cli = Command(
        "type",
        params=[Option(["-m"], type=Choice(["a", "b"]), multiple=True), Option(["-f"])],
    )
    assert _get_words(cli, ["-m"], "") == ["a", "b"]
    assert "-m" in _get_words(cli, ["-m", "a"], "-")
    assert _get_words(cli, ["-m", "a", "-m"], "") == ["a", "b"]
    # used single options aren't suggested again
    assert "-c" not in _get_words(cli, ["-c", "f"], "-")


def test_option_nargs():
    cli = Command("cli", params=[Option(["-c"], type=Choice(["a", "b"]), nargs=2)])
    assert _get_words(cli, ["-c"], "") == ["a", "b"]
    assert _get_words(cli, ["-c", "a"], "") == ["a", "b"]
    assert _get_words(cli, ["-c", "a", "b"], "") == []


def test_argument_nargs():
    cli = Command(
        "cli",
        params=[
            Argument(["x"], type=Choice(["a", "b"]), nargs=2),
            Argument(["y"], type=Choice(["c", "d"]), nargs=-1),
            Option(["-z"]),
        ],
    )
    assert _get_words(cli, [], "") == ["a", "b"]
    assert _get_words(cli, ["a"], "") == ["a", "b"]
    assert _get_words(cli, ["a", "b"], "") == ["c", "d"]
    assert _get_words(cli, ["a", "b", "c"], "") == ["c", "d"]
    assert _get_words(cli, ["a", "b", "c", "d"], "") == ["c", "d"]
    assert _get_words(cli, ["a", "-z", "1"], "") == ["a", "b"]
    assert _get_words(cli, ["a", "-z", "1", "b"], "") == ["c", "d"]


def test_double_dash():
    cli = Command(
        "cli",
        add_help_option=False,
        params=[
            Option(["--opt"]),
            Argument(["name"], type=Choice(["name", "--", "-o", "--opt"])),
        ],
    )
    assert _get_words(cli, [], "-") == ["--opt"]
    assert _get_words(cli, ["value"], "-") == ["--opt"]
    assert _get_words(cli, [], "") == ["name", "--", "-o", "--opt"]
    assert _get_words(cli, ["--"], "") == ["name", "--", "-o", "--opt"]


def test_hidden():
    cli = Group(
        "cli",
        commands=[
            Command(
                "hidden",
                add_help_option=False,
                hidden=True,
                params=[
                    Option(["-a"]),
                    Option(["-b"], type=Choice(["a", "b"]), hidden=True),
                ],
            )
        ],
    )
    assert "hidden" not in _get_words(cli, [], "")
    assert "hidden" not in _get_words(cli, [], "hidden")
    assert _get_words(cli, ["hidden"], "-") == ["-a"]
    assert _get_words(cli, ["hidden", "-b"], "") == ["a", "b"]


def test_add_different_name():
    cli = Group("cli", commands={"renamed": Command("original")})
    words = _get_words(cli, [], "")
    assert "renamed" in words
    assert "original" not in words


def test_completion_item_data():
    c = CompletionItem("test", a=1)
    assert c.a == 1
    assert c.b is None


@pytest.fixture()
def _patch_for_completion(monkeypatch):
    monkeypatch.setattr(
        "click.shell_completion.BashComplete._check_version", lambda self: True
    )


@pytest.mark.parametrize("shell", ["bash", "zsh", "fish"])
@pytest.mark.usefixtures("_patch_for_completion")
def test_full_source(runner, shell):
    cli = Group("cli", commands=[Command("a"), Command("b")])
    result = runner.invoke(cli, env={"_CLI_COMPLETE": f"{shell}_source"})
    assert f"_CLI_COMPLETE={shell}_complete" in result.output


def test_full_source_powershell(runner):
    # The PowerShell source script sets the completion env var via
    # `$env:_CLI_COMPLETE = 'powershell_complete'`, so the substring
    # `_CLI_COMPLETE=powershell_complete` used by test_full_source above
    # is not present. Assert on the PowerShell-specific markers instead.
    cli = Group("cli", commands=[Command("a"), Command("b")])
    result = runner.invoke(cli, env={"_CLI_COMPLETE": "powershell_source"})
    assert "Register-ArgumentCompleter" in result.output
    assert "powershell_complete" in result.output


@pytest.mark.parametrize(
    ("shell", "env", "expect"),
    [
        ("bash", {"COMP_WORDS": "", "COMP_CWORD": "0"}, "plain,a\nplain,b\n"),
        ("bash", {"COMP_WORDS": "a b", "COMP_CWORD": "1"}, "plain,b\n"),
        ("zsh", {"COMP_WORDS": "", "COMP_CWORD": "0"}, "plain\na\n_\nplain\nb\nbee\n"),
        ("zsh", {"COMP_WORDS": "a b", "COMP_CWORD": "1"}, "plain\nb\nbee\n"),
        ("fish", {"COMP_WORDS": "", "COMP_CWORD": ""}, "plain,a\nplain,b\tbee\n"),
        ("fish", {"COMP_WORDS": "a b", "COMP_CWORD": "b"}, "plain,b\tbee\n"),
        ("fish", {"COMP_WORDS": 'a "b', "COMP_CWORD": '"b'}, "plain,b\tbee\n"),
        (
            "powershell",
            {"COMP_WORDS": "", "COMP_CWORD": "0"},
            "plain\na\n_\nplain\nb\nbee\n",
        ),
        ("powershell", {"COMP_WORDS": "a b", "COMP_CWORD": "1"}, "plain\nb\nbee\n"),
    ],
)
@pytest.mark.usefixtures("_patch_for_completion")
def test_full_complete(runner, shell, env, expect):
    cli = Group("cli", commands=[Command("a"), Command("b", help="bee")])
    env["_CLI_COMPLETE"] = f"{shell}_complete"
    result = runner.invoke(cli, env=env)
    assert result.output == expect


def test_source_uses_lf_line_endings(monkeypatch):
    stdout = io.BytesIO()
    stream = io.TextIOWrapper(stdout, encoding="utf-8", newline="\r\n")
    monkeypatch.setattr("click.utils._default_text_stdout", lambda: stream)

    cli = Group("cli", commands=[Command("a"), Command("b")])
    assert shell_complete(cli, {}, "cli", "_CLI_COMPLETE", "zsh_source") == 0

    stream.flush()
    output = stdout.getvalue()
    assert b"\r\n" not in output
    assert b"\n" in output


@pytest.mark.parametrize(
    ("env", "expect"),
    [
        (
            {"COMP_WORDS": "", "COMP_CWORD": "0"},
            textwrap.dedent(
                """\
                    plain
                    a
                    _
                    plain
                    b
                    bee
                    plain
                    c\\:d
                    cee:dee
                    plain
                    c:e
                    _
                """
            ),
        ),
        (
            {"COMP_WORDS": "a c", "COMP_CWORD": "1"},
            textwrap.dedent(
                """\
                    plain
                    c\\:d
                    cee:dee
                    plain
                    c:e
                    _
                """
            ),
        ),
        (
            {"COMP_WORDS": "a c:", "COMP_CWORD": "1"},
            textwrap.dedent(
                """\
                    plain
                    c\\:d
                    cee:dee
                    plain
                    c:e
                    _
                """
            ),
        ),
    ],
)
@pytest.mark.usefixtures("_patch_for_completion")
def test_zsh_full_complete_with_colons(
    runner, env: Mapping[str, str], expect: str
) -> None:
    cli = Group(
        "cli",
        commands=[
            Command("a"),
            Command("b", help="bee"),
            Command("c:d", help="cee:dee"),
            Command("c:e"),
        ],
    )
    result = runner.invoke(
        cli,
        env={
            **env,
            "_CLI_COMPLETE": "zsh_complete",
        },
    )
    assert result.output == expect


@pytest.mark.usefixtures("_patch_for_completion")
def test_context_settings(runner):
    def complete(ctx, param, incomplete):
        return ctx.obj["choices"]

    cli = Command("cli", params=[Argument("x", shell_complete=complete)])
    result = runner.invoke(
        cli,
        obj={"choices": ["a", "b"]},
        env={"COMP_WORDS": "", "COMP_CWORD": "0", "_CLI_COMPLETE": "bash_complete"},
    )
    assert result.output == "plain,a\nplain,b\n"


# case_sensitive=False normalizes values to lowercase, matching remains case insensitive
@pytest.mark.parametrize(("value", "expect"), [(False, ["au", "al"]), (True, ["al"])])
def test_choice_case_sensitive(value, expect):
    cli = Command(
        "cli",
        params=[Option(["-a"], type=Choice(["Au", "al", "Bc"], case_sensitive=value))],
    )
    completions = _get_words(cli, ["-a"], "a")
    assert completions == expect


@pytest.fixture()
def _restore_available_shells(tmpdir):
    prev_available_shells = click.shell_completion._available_shells.copy()
    click.shell_completion._available_shells.clear()
    yield
    click.shell_completion._available_shells.clear()
    click.shell_completion._available_shells.update(prev_available_shells)


@pytest.mark.usefixtures("_restore_available_shells")
def test_add_completion_class():
    # At first, "mysh" is not in available shells
    assert "mysh" not in click.shell_completion._available_shells

    class MyshComplete(ShellComplete):
        name = "mysh"
        source_template = "dummy source"

    # "mysh" still not in available shells because it is not registered
    assert "mysh" not in click.shell_completion._available_shells

    # Adding a completion class should return that class
    assert add_completion_class(MyshComplete) is MyshComplete

    # Now, "mysh" is finally in available shells
    assert "mysh" in click.shell_completion._available_shells
    assert click.shell_completion._available_shells["mysh"] is MyshComplete


@pytest.mark.usefixtures("_restore_available_shells")
def test_add_completion_class_with_name():
    # At first, "mysh" is not in available shells
    assert "mysh" not in click.shell_completion._available_shells
    assert "not_mysh" not in click.shell_completion._available_shells

    class MyshComplete(ShellComplete):
        name = "not_mysh"
        source_template = "dummy source"

    # "mysh" and "not_mysh" are still not in available shells because
    # it is not registered yet
    assert "mysh" not in click.shell_completion._available_shells
    assert "not_mysh" not in click.shell_completion._available_shells

    # Adding a completion class should return that class.
    # Because we are using the "name" parameter, the name isn't taken
    # from the class.
    assert add_completion_class(MyshComplete, name="mysh") is MyshComplete

    # Now, "mysh" is finally in available shells
    assert "mysh" in click.shell_completion._available_shells
    assert "not_mysh" not in click.shell_completion._available_shells
    assert click.shell_completion._available_shells["mysh"] is MyshComplete


@pytest.mark.usefixtures("_restore_available_shells")
def test_add_completion_class_decorator():
    # At first, "mysh" is not in available shells
    assert "mysh" not in click.shell_completion._available_shells

    @add_completion_class
    class MyshComplete(ShellComplete):
        name = "mysh"
        source_template = "dummy source"

    # Using `add_completion_class` as a decorator adds the new shell immediately
    assert "mysh" in click.shell_completion._available_shells
    assert click.shell_completion._available_shells["mysh"] is MyshComplete


# Don't make the ResourceWarning give an error
@pytest.mark.filterwarnings("default::ResourceWarning")
def test_files_closed(tmp_path) -> None:
    config_file = str(tmp_path / "foo.txt")
    with open(config_file, "w") as f:
        f.write("bar")

    @click.group()
    @click.option(
        "--config-file",
        default=config_file,
        type=click.File(mode="r"),
    )
    @click.pass_context
    def cli(ctx, config_file):
        pass

    with warnings.catch_warnings(record=True) as current_warnings:
        assert not current_warnings, "There should be no warnings to start"
        _get_completions(cli, args=[], incomplete="")
        assert not current_warnings, "There should be no warnings after either"


@pytest.mark.parametrize("from_map", [False, True])
def test_completion_does_not_call_callable_default(runner, from_map):
    """Resolving the context for completion doesn't call a callable default,
    from either the parameter or the default map. Ordinary invocation still
    calls it once. https://github.com/pallets/click/issues/2614
    """
    calls = []

    def default():
        calls.append("called")
        return "calculated"

    def complete(ctx, param, incomplete):
        source = ctx.get_parameter_source("name")
        return [f"{ctx.params['name']}:{source.name}"]

    @click.command(
        context_settings={"default_map": {"name": default}} if from_map else {}
    )
    @click.option("--name", default=None if from_map else default)
    @click.option("--color", shell_complete=complete)
    def cli(name, color):
        click.echo(name)

    expect_source = "DEFAULT_MAP" if from_map else "DEFAULT"
    assert _get_words(cli, ["--color"], "") == [f"None:{expect_source}"]
    assert _get_words(cli, [], "--") == ["--name", "--color", "--help"]
    assert calls == []

    result = runner.invoke(cli, ["--color", "red"])
    assert result.exit_code == 0, result.output
    assert result.output == "calculated\n"
    assert calls == ["called"]


@pytest.mark.parametrize(
    ("args", "default_map", "expect"),
    [
        ([], None, "literal:DEFAULT"),
        ([], {"name": "mapped"}, "mapped:DEFAULT_MAP"),
        (["--name", "explicit"], None, "explicit:COMMANDLINE"),
        (["--name", "explicit"], {"name": lambda: "x"}, "explicit:COMMANDLINE"),
    ],
)
def test_completion_keeps_literal_and_explicit_values(args, default_map, expect):
    """Literal defaults, literal default map values and parsed values still
    populate the completion context.
    """

    def complete(ctx, param, incomplete):
        source = ctx.get_parameter_source("name")
        return [f"{ctx.params['name']}:{source.name}"]

    @click.command(context_settings={"default_map": default_map})
    @click.option("--name", default="literal")
    @click.option("--color", shell_complete=complete)
    def cli(name, color):
        pass

    assert _get_words(cli, [*args, "--color"], "") == [expect]


def test_completion_keeps_callable_flag_value():
    """A callable flag value used as a flag's default is a literal value, not a
    callable default, so completion still exposes it uncalled.
    """

    def complete(ctx, param, incomplete):
        return [ctx.params["upper"].__name__]

    @click.command()
    @click.option("--upper", "upper", flag_value=str.upper, default=True)
    @click.option("--color", shell_complete=complete)
    def cli(upper, color):
        pass

    assert _get_words(cli, ["--color"], "") == ["upper"]


def _equals_cli(choices=("auto", "always", "never")):
    def complete_size(ctx, param, incomplete):
        return [f"color={ctx.params['color']}"]

    @click.command()
    @click.option("--color", type=Choice(choices))
    @click.option("--size", shell_complete=complete_size)
    def cli(color, size):
        click.echo(color)

    return cli


def _shell_complete_output(runner, cli, shell, words, cword):
    result = runner.invoke(
        cli,
        prog_name="gobble",
        env={
            "_GOBBLE_COMPLETE": f"{shell}_complete",
            "COMP_WORDS": words,
            "COMP_CWORD": str(cword),
        },
    )
    assert result.exit_code == 0, result.output
    return result.output


@pytest.mark.parametrize(
    ("words", "cword", "expect"),
    [
        # Bash splits at "=" in COMP_WORDBREAKS, and replaces only the value.
        ("gobble --color = al", 3, ["always"]),
        ("gobble --color = a", 3, ["auto", "always"]),
        ("gobble --color = ", 3, ["auto", "always", "never"]),
        # The cursor directly after "=" is on the "=" word, but Bash inserts
        # after it.
        ("gobble --color =", 2, ["auto", "always", "never"]),
        # Without "=" in COMP_WORDBREAKS, Bash replaces the whole word.
        ("gobble --color=al", 1, ["--color=always"]),
        ("gobble --color=", 1, ["--color=auto", "--color=always", "--color=never"]),
        # The space-separated form is unchanged.
        ("gobble --color al", 2, ["always"]),
    ],
)
def test_bash_completes_option_value_after_equals(runner, words, cword, expect):
    """Bash completes a value given with ``=`` and keeps the option name.
    https://github.com/pallets/click/issues/2847
    """
    output = _shell_complete_output(runner, _equals_cli(), "bash", words, cword)
    assert output.splitlines() == [f"plain,{value}" for value in expect]


@pytest.mark.parametrize(
    ("words", "cword", "expect"),
    [
        ("gobble --color = a", 3, ["a=b", "a=c"]),
        ("gobble --color = a =", 4, ["b", "c"]),
        ("gobble --color = a = c", 5, ["c"]),
        ("gobble --color=a=", 1, ["--color=a=b", "--color=a=c"]),
    ],
)
def test_bash_completes_option_value_containing_equals(runner, words, cword, expect):
    """Bash also splits an ``=`` in the value. Only the part Bash replaces is
    returned. https://github.com/pallets/click/issues/2847
    """
    cli = _equals_cli(("a=b", "a=c"))
    output = _shell_complete_output(runner, cli, "bash", words, cword)
    assert output.splitlines() == [f"plain,{value}" for value in expect]


@pytest.mark.parametrize(
    ("words", "cword"),
    [
        ("gobble --color = always --size ", 5),
        ("gobble --color=always --size ", 3),
        ("gobble --color always --size ", 4),
    ],
)
def test_bash_parses_complete_option_value_after_equals(runner, words, cword):
    """An ``--name=value`` split by Bash in the complete args is parsed as
    the option's value. https://github.com/pallets/click/issues/2847
    """
    output = _shell_complete_output(runner, _equals_cli(), "bash", words, cword)
    assert output.splitlines() == ["plain,color=always"]


def test_bash_equals_after_argument_is_unchanged(runner):
    """An ``=`` word after a word that is not an option is not joined, it is
    still the value of the next argument.
    """

    @click.command()
    @click.argument("key")
    @click.argument("value", type=Choice(["=", "x"]))
    @click.argument("rest", type=Choice(["r"]))
    def cli(key, value, rest):
        pass

    output = _shell_complete_output(runner, cli, "bash", "gobble key = ", 3)
    assert output.splitlines() == ["plain,r"]


@pytest.mark.parametrize(
    ("words", "cword", "expect"),
    [
        ("gobble --color=al", 1, ["--color=always"]),
        ("gobble --color=a", 1, ["--color=auto", "--color=always"]),
        ("gobble --color=", 1, ["--color=auto", "--color=always", "--color=never"]),
        ("gobble --color al", 2, ["always"]),
        ("gobble --col", 1, ["--color"]),
    ],
)
def test_zsh_completes_option_value_after_equals(runner, words, cword, expect):
    """Zsh replaces the whole ``--name=value`` word, so the values keep the
    option name. https://github.com/pallets/click/issues/2847
    """
    output = _shell_complete_output(runner, _equals_cli(), "zsh", words, cword)
    assert output.splitlines() == [
        line for value in expect for line in ("plain", value, "_")
    ]


def test_zsh_option_value_after_equals_keeps_help(runner):
    """A value with help is prefixed before colons in it are escaped."""

    def complete(ctx, param, incomplete):
        return [CompletionItem("a:b", help="first")]

    @click.command()
    @click.option("--color", shell_complete=complete)
    def cli(color):
        pass

    output = _shell_complete_output(runner, cli, "zsh", "gobble --color=a", 1)
    assert output.splitlines() == ["plain", r"--color=a\:b", "first"]


def test_option_value_after_equals_keeps_dir_and_file_types(runner):
    """Only plain values get the option prefix, the shell completes paths."""

    @click.command()
    @click.option("--out", type=Path())
    def cli(out):
        pass

    output = _shell_complete_output(runner, cli, "zsh", "gobble --out=sr", 1)
    assert output.splitlines() == ["file", "sr", "_"]
    output = _shell_complete_output(runner, cli, "bash", "gobble --out = sr", 3)
    assert output.splitlines() == ["file,sr"]


def test_get_completions_without_option_prefix():
    """The base class still returns the values without the option name."""
    assert _get_words(_equals_cli(), [], "--color=al") == ["always"]


@pytest.mark.skipif(shutil.which("bash") is None, reason="requires Bash")
@pytest.mark.parametrize(
    ("current", "expect"),
    [
        ("two", ["two\\ words", "a=b", "x\\$y"]),
        ("'two", ["two words", "a=b", "x$y"]),
    ],
)
@pytest.mark.usefixtures("_patch_for_completion")
def test_bash_script_quotes_inserted_values(runner, current, expect):
    """Bash inserts a reply literally, so the script escapes spaces and other
    special characters, unless the word is in quotes.
    https://github.com/pallets/click/issues/2847
    """
    result = runner.invoke(
        _equals_cli(), prog_name="gobble", env={"_GOBBLE_COMPLETE": "bash_source"}
    )
    script = (
        f"{result.output}\n"
        # Answer as the program would, without running it.
        "env() { printf 'plain,two words\\nplain,a=b\\nplain,x$y\\n'; }\n"
        f"COMP_WORDS=(gobble --color = {shlex.quote(current)}); COMP_CWORD=3\n"
        "_gobble_completion gobble\n"
        'printf "%s\\n" "${COMPREPLY[@]}"\n'
    )
    completed = subprocess.run(
        [shutil.which("bash"), "--norc", "--noprofile", "-c", script],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    assert completed.stdout.splitlines() == expect


def test_fish_format_completion_escapes_help():
    fc = FishComplete(Command("x"), {}, "x", "_X_COMPLETE")
    item = CompletionItem("--at", help="first\nsecond\tthird")
    # The newline is escaped to the literal characters backslash-n and the tab
    # becomes a space, so each completion stays on one line for fish.
    assert fc.format_completion(item) == "plain,--at\tfirst\\nsecond third"


def test_powershell_format_completion_escapes_help():
    pc = PowerShellComplete(Command("x"), {}, "x", "_X_COMPLETE")
    # Newlines (LF and CRLF) collapse to spaces so the help text stays
    # on a single line and doesn't break the 3-lines-per-item framing
    # consumed by the PowerShell completion script.
    item = CompletionItem("--at", help="first\nsecond\r\nthird")
    assert pc.format_completion(item) == "plain\n--at\nfirst second  third"
    # Items without help text use the "_" sentinel, matching the format
    # produced by ZshComplete.
    item = CompletionItem("--at")
    assert pc.format_completion(item) == "plain\n--at\n_"
