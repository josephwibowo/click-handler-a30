"""Both real completion defects composed through native shell interaction."""

import pytest

from acceptance.shell_probe import complete_and_invoke


@pytest.mark.parametrize("shell", ["bash", "zsh"])
@pytest.mark.parametrize("command", ["gobble --color=al", "gobble --color al"])
def test_real_completion_preserves_the_option_without_evaluating_defaults(
    tmp_path,
    shell,
    command,
):
    """Catch fixes that still lose the option or execute unrelated work."""
    observed = complete_and_invoke(tmp_path, shell, command)
    assert observed["completion_called_default"] is False, observed["transcript"]
    assert observed["result"] == {"color": "always", "name": "calculated"}
    assert observed["invocation_calls"] == ["called"]
