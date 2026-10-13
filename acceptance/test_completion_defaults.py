"""The observed callable-default regression and its compatibility boundaries."""

from pathlib import Path

import pytest

import click
from click.testing import CliRunner


@pytest.mark.parametrize("from_map", [False, True])
@pytest.mark.parametrize("shell", ["bash", "zsh"])
def test_completion_leaves_callable_defaults_unevaluated(tmp_path, from_map, shell):
    """Catch #2614: resolving another option executes a callable default."""
    marker: Path = tmp_path / "default-calls"

    def default():
        with marker.open("a", encoding="utf-8") as stream:
            stream.write("called\n")
        return "calculated"

    @click.command()
    @click.option("--color", type=click.Choice(["auto", "always", "never"]))
    @click.option("--name", default=None if from_map else default)
    def cli(color, name):
        click.echo(name)

    kwargs = {"default_map": {"name": default}} if from_map else {}
    result = CliRunner().invoke(
        cli,
        [],
        prog_name="gobble",
        env={
            "_GOBBLE_COMPLETE": f"{shell}_complete",
            "COMP_WORDS": "gobble --color a",
            "COMP_CWORD": "2",
        },
        **kwargs,
    )
    assert result.exit_code == 0, result.output
    assert "auto" in result.output and "always" in result.output
    assert not marker.exists()

    invoked = CliRunner().invoke(cli, ["--color", "always"], **kwargs)
    assert invoked.exit_code == 0, invoked.output
    assert invoked.output == "calculated\n"
    assert marker.read_text(encoding="utf-8") == "called\n"


@pytest.mark.parametrize("explicit", [False, True])
def test_completion_keeps_literal_and_explicit_context_values(explicit):
    """Catch suppressing literals or losing parsed values while avoiding a call."""

    def complete(ctx, param, incomplete):
        return [ctx.params["name"]]

    @click.command()
    @click.option("--name", default="literal")
    @click.option("--color", shell_complete=complete)
    def cli(name, color):
        click.echo(color)

    words = "gobble --name explicit --color a" if explicit else "gobble --color a"
    result = CliRunner().invoke(
        cli,
        [],
        prog_name="gobble",
        env={
            "_GOBBLE_COMPLETE": "bash_complete",
            "COMP_WORDS": words,
            "COMP_CWORD": "4" if explicit else "2",
        },
    )
    assert result.exit_code == 0, result.output
    assert result.output == f"plain,{'explicit' if explicit else 'literal'}\n"


def test_completion_keeps_a_literal_default_map_and_its_parameter_source():
    """Catch suppression of literal default-map values or their parameter source."""

    def complete(ctx, param, incomplete):
        source = ctx.get_parameter_source("name")
        return [f"{ctx.params['name']}:{source.name}"]

    @click.command()
    @click.option("--name", default="fallback")
    @click.option("--color", shell_complete=complete)
    def cli(name, color):
        click.echo(name)

    result = CliRunner().invoke(
        cli,
        [],
        default_map={"name": "mapped"},
        prog_name="gobble",
        env={
            "_GOBBLE_COMPLETE": "bash_complete",
            "COMP_WORDS": "gobble --color a",
            "COMP_CWORD": "2",
        },
    )
    assert result.exit_code == 0, result.output
    assert result.output == "plain,mapped:DEFAULT_MAP\n"


@pytest.mark.parametrize("explicit", [False, True])
def test_subcommand_completion_keeps_parent_context(explicit):
    """Catch completion losing values/source from the already parsed parent."""

    @click.group()
    @click.option("--name", default="literal")
    def group(name):
        pass

    def complete(ctx, param, incomplete):
        parent = ctx.parent
        source = parent.get_parameter_source("name")
        return [f"{parent.params['name']}:{source.name}"]

    @group.command()
    @click.option("--color", shell_complete=complete)
    def sub(color):
        click.echo(color)

    words = (
        "gobble --name explicit sub --color a" if explicit else "gobble sub --color a"
    )
    result = CliRunner().invoke(
        group,
        [],
        prog_name="gobble",
        env={
            "_GOBBLE_COMPLETE": "bash_complete",
            "COMP_WORDS": words,
            "COMP_CWORD": "5" if explicit else "3",
        },
    )
    assert result.exit_code == 0, result.output
    expected = "explicit:COMMANDLINE" if explicit else "literal:DEFAULT"
    assert result.output == f"plain,{expected}\n"
