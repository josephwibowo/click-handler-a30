"""Run one frozen objective check against this checkout's actual Click source."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ElementTree
from collections.abc import Sequence
from pathlib import Path


def lint_steps(output: str) -> dict[str, list[str]]:
    """The ruff and mypy steps of the required handler-check workflow's static job.

    Each step runs the uv.lock-pinned tool with this repository's own pyproject
    configuration, exactly as the workflow does. Only cache placement differs, which
    changes no verdict: an independent check keeps the candidate read-only, so ruff
    keeps no cache and mypy's lives under the report directory. The workflow's
    `pyright --verifytypes click` is not run: it asks the interpreter for its search
    path through a Node child process, which Handler's native sandbox refuses (EPERM).
    """
    return {
        "ruff-check": ["ruff", "check", "--no-fix", "--no-cache", "."],
        "ruff-format": ["ruff", "format", "--check", "--no-cache", "."],
        "mypy": ["mypy", "--cache-dir", f"{output}/mypy-cache"],
    }


def run_lint(root: Path, output: str) -> int:
    """Run every lint step, print its output, and report each step as a JUnit case."""
    suite = ElementTree.Element("testsuite", name="lint")
    failures = 0
    steps = lint_steps(output)
    for name, args in steps.items():
        started = time.monotonic()
        completed = subprocess.run(
            [sys.executable, "-m", *args],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        elapsed = time.monotonic() - started
        print(f"== {name}: exit {completed.returncode} in {elapsed:.1f}s", flush=True)
        print(completed.stdout + completed.stderr, end="", flush=True)
        case = ElementTree.SubElement(
            suite,
            "testcase",
            name=f"ci/check_objective.py::lint::{name}",
            time=f"{elapsed:.3f}",
        )
        if completed.returncode != 0:
            failures += 1
            ElementTree.SubElement(
                case, "failure", message=f"{name} exited {completed.returncode}"
            )
    suite.set("tests", str(len(steps)))
    suite.set("failures", str(failures))
    ElementTree.ElementTree(suite).write(
        root / f"{output}.xml", encoding="utf-8", xml_declaration=True
    )
    return 1 if failures else 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        choices=["upstream", "defaults", "equals", "integrated", "negative", "lint"],
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
    # The JUnit report is reports/<mode>.xml, so the one report capability Handler's
    # assurance derives is reports/ itself; pytest's, mypy's and tempfile's scratch
    # trees live under reports/<mode>/.
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
    if args.mode == "lint":
        # Every run is cold, as the workflow's is.
        cache = root / output / "mypy-cache"
        shutil.rmtree(cache, ignore_errors=True)
        try:
            return run_lint(root, output)
        finally:
            shutil.rmtree(cache, ignore_errors=True)
            shutil.rmtree(temporary)
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
