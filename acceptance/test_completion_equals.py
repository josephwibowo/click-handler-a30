"""The equals-word protocol cases, before actual shell interaction is composed."""

import pytest

import click
from click.testing import CliRunner


@pytest.mark.parametrize(
    "prefix, expected",
    [
        ("", ["auto", "always", "never"]),
        ("a", ["auto", "always"]),
        ("al", ["always"]),
    ],
)
@pytest.mark.parametrize("form", ["attached", "split", "space"])
def test_bash_completes_choice_values_in_all_word_forms(prefix, expected, form):
    """Catch #2847: Bash word breaks around '=' suppress choice completion."""

    @click.command()
    @click.option("--color", type=click.Choice(["auto", "always", "never"]))
    def cli(color):
        click.echo(color)

    if form == "attached":
        words, index = f"gobble --color={prefix}", "1"
    elif form == "split":
        words, index = f"gobble --color = {prefix}", "3"
    else:
        words, index = f"gobble --color {prefix}", "2"
    result = CliRunner().invoke(
        cli,
        [],
        prog_name="gobble",
        env={
            "_GOBBLE_COMPLETE": "bash_complete",
            "COMP_WORDS": words,
            "COMP_CWORD": index,
        },
    )
    assert result.exit_code == 0, result.output
    # Some shells need candidates prefixed; both wire forms denote these values.
    values = [
        line.removeprefix("plain,").removeprefix("--color=")
        for line in result.output.splitlines()
    ]
    assert values == expected
