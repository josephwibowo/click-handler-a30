"""Independent rejection and quoted-value controls for completion fixes."""

import pytest

import click
from click.testing import CliRunner


@pytest.mark.parametrize("args", [["--color", "unknown"], ["--unknown"], ["extra"]])
def test_ordinary_invocation_rejects_invalid_inputs(args):
    """Catch a completion fix weakening ordinary choice/option/argument validation."""

    @click.command()
    @click.option("--color", type=click.Choice(["two words", "a=b"]))
    def cli(color):
        click.echo(color)

    result = CliRunner().invoke(cli, args)
    assert result.exit_code == 2, result.output
    assert "Error:" in result.output


@pytest.mark.parametrize("value", ["two words", "a=b"])
def test_ordinary_invocation_preserves_spaces_and_equals_in_values(value):
    """Catch lossy option/value normalization changing an actual argument value."""

    @click.command()
    @click.option("--color", type=click.Choice(["two words", "a=b"]))
    def cli(color):
        click.echo(color)

    result = CliRunner().invoke(cli, [f"--color={value}"])
    assert result.exit_code == 0, result.output
    assert result.output == f"{value}\n"
