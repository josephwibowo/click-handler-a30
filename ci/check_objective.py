"""Run one frozen objective check against this checkout's actual Click source."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode", choices=["upstream", "defaults", "equals", "integrated", "negative"]
    )
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    if Path.cwd().resolve() != root:
        parser.error("run the check from its approved repository root")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root / "src"))
    os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    # Subprocesses a test starts (sys.executable -c "import click") must import this
    # candidate too, never whatever the interpreter's environment has installed.
    os.environ["PYTHONPATH"] = str(root / "src")

    import pytest

    import click

    if Path(click.__file__).resolve() != root / "src/click/__init__.py":
        raise RuntimeError(
            "the check imported Click from outside its approved candidate"
        )
    target = {
        # Handler's native sandbox presents /tmp as an unreadable directory, and this
        # one case asserts a click.Path() default of the literal host path "/tmp"
        # passes the readable check. It cannot pass in any sandbox that hides /tmp;
        # every other default-propagation case of the same test still runs.
        "upstream": [
            "tests",
            "--deselect",
            "tests/test_commands.py::test_other_command_invoke_with_defaults"
            "[opt_params12-/tmp]",
        ],
        "defaults": ["acceptance/test_completion_defaults.py"],
        "equals": [
            "acceptance/test_completion_equals.py",
            "acceptance/test_completion_integrated.py",
        ],
        "integrated": ["acceptance"],
        "negative": ["acceptance/test_negative_inputs.py"],
    }[args.mode]
    # The JUnit report is reports/<mode>.xml, so the one report capability Handler's
    # assurance derives is reports/ itself; pytest's and tempfile's scratch trees
    # live under reports/<mode>/.
    output = f"reports/{args.mode}"
    (root / output).mkdir(parents=True, exist_ok=True)
    # The sandbox denies /tmp and the caller sets no TMPDIR, so tempfile would fall
    # back to the candidate root. Keep temporary files inside the report directory,
    # the only path an independent check may write, and remove them afterwards.
    temporary = root / output / "tmpdir"
    shutil.rmtree(temporary, ignore_errors=True)
    temporary.mkdir()
    os.environ["TMPDIR"] = str(temporary)
    tempfile.tempdir = None
    try:
        return int(
            pytest.main(
                [
                    "-q",
                    "-p",
                    "no:cacheprovider",
                    "--tb=short",
                    *target,
                    f"--basetemp={output}/tmp",
                    f"--junitxml={output}.xml",
                ]
            )
        )
    finally:
        shutil.rmtree(temporary)


if __name__ == "__main__":
    raise SystemExit(main())
