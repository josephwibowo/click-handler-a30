"""Run one frozen objective check against this checkout's actual Click source."""

from __future__ import annotations

import argparse
import base64
import faulthandler
import hashlib
import json
import os
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ElementTree
from collections.abc import Sequence
from pathlib import Path
from typing import cast


def lint_steps(output: str) -> dict[str, list[str]]:
    """The protected native ruff and mypy steps from the historical static job.

    Each step runs the uv.lock-pinned tool with this repository's own pyproject
    configuration, as the historical workflow did. Only cache placement differs, which
    changes no verdict: an independent check keeps the candidate read-only, so ruff
    keeps no cache and mypy's lives under the report directory. The historical
    workflow's `pyright --verifytypes click` is not run: it asks the interpreter
    for its search path through a Node child process, which Handler's native sandbox
    refuses (EPERM).
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


def upstream_evidence(raw: bytes) -> dict[str, object]:
    """Validate complete pytest JUnit and preserve every actual inner outcome."""
    if not raw or len(raw) > 4 * 1024 * 1024:
        raise ValueError("upstream JUnit is missing or exceeds its bound")
    root = ElementTree.fromstring(raw)
    if root.tag not in {"testsuite", "testsuites"}:
        raise ValueError("upstream JUnit has no suite root")
    identities: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    def inspect_suite(node: ElementTree.Element) -> dict[str, int]:
        counts = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
        for child in node:
            if child.tag in {"testsuite", "testsuites"}:
                nested = inspect_suite(child)
                for key in counts:
                    counts[key] += nested[key]
            elif child.tag == "testcase":
                name, classname = child.get("name"), child.get("classname")
                if not name or not classname:
                    raise ValueError("upstream case has no exact identity")
                identity = (child.get("file", ""), classname, name)
                if identity in seen:
                    raise ValueError("duplicate upstream case identity")
                seen.add(identity)
                if any(
                    item.tag
                    not in {
                        "properties",
                        "system-out",
                        "system-err",
                        "failure",
                        "error",
                        "skipped",
                    }
                    for item in child
                ):
                    raise ValueError("unsupported upstream testcase element")
                outcomes = [
                    item.tag
                    for item in child
                    if item.tag in {"failure", "error", "skipped"}
                ]
                if len(outcomes) > 1:
                    raise ValueError("contradictory upstream case outcomes")
                outcome = outcomes[0] if outcomes else "pass"
                counts["tests"] += 1
                if outcomes:
                    counts[
                        {
                            "failure": "failures",
                            "error": "errors",
                            "skipped": "skipped",
                        }[outcome]
                    ] += 1
                identities.append(
                    {
                        "file": identity[0],
                        "classname": classname,
                        "name": name,
                        "outcome": outcome,
                    }
                )
            elif child.tag not in {"properties", "system-out", "system-err"}:
                raise ValueError("unsupported upstream JUnit element")
        for key, count in counts.items():
            declared = node.get(key)
            if node.tag == "testsuite" and declared is None:
                raise ValueError("incomplete upstream suite counts")
            if declared is not None and (
                not declared.isdecimal() or int(declared) != count
            ):
                raise ValueError("contradictory upstream suite counts")
        return counts

    counts = inspect_suite(root)
    passed = counts["tests"] - counts["failures"] - counts["errors"] - counts["skipped"]
    if counts["tests"] == 0:
        raise ValueError("upstream suite contains no cases")
    return {
        "sha256": hashlib.sha256(raw).hexdigest(),
        "raw_junit_b64": base64.b64encode(raw).decode(),
        "counts": {**counts, "passed": passed},
        "cases": identities,
    }


def run_upstream(root: Path, output: Path, command: list[str]) -> int:
    """Certify the protected process and retain its exact original raw report."""
    original = output / "original-upstream.xml"
    # A repeated host invocation must not certify an earlier invocation's report.
    original.unlink(missing_ok=True)
    diagnostic_bootstrap = (
        "import faulthandler,os,runpy,signal,sys;"
        "diagnostic=os.fdopen(os.dup(2),'w');"
        "faulthandler.register(signal.SIGSYS,file=diagnostic,all_threads=True,chain=True);"
        "sys.argv=['pytest',*sys.argv[1:]];runpy.run_module('pytest',run_name='__main__')"
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            diagnostic_bootstrap,
            *command,
            f"--junitxml={original}",
        ],
        cwd=root,
        check=False,
    )
    suite = ElementTree.Element(
        "testsuite",
        name="upstream-workflow",
        tests="1",
        failures="0",
        errors="0",
        skipped="0",
    )
    case = ElementTree.SubElement(
        suite,
        "testcase",
        classname="protected_workflow",
        name="upstream_default_pytest_process_succeeds",
    )
    evidence: dict[str, object] = {
        "process_exit_code": completed.returncode,
        "evidence_kind": "workflow-step",
    }
    error = None
    outcome = "pass"
    report_outcome = None
    try:
        descriptor = os.open(original, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(descriptor, "rb") as stream:
            metadata = os.fstat(stream.fileno())
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise ValueError("upstream JUnit must be a plain unlinked report")
            raw = stream.read(4 * 1024 * 1024 + 1)
        # Retain exact original bytes even when semantic validation rejects them.
        if len(raw) > 4 * 1024 * 1024:
            raise ValueError("upstream JUnit exceeds its bound")
        evidence.update(
            {
                "sha256": hashlib.sha256(raw).hexdigest(),
                "raw_junit_b64": base64.b64encode(raw).decode(),
            }
        )
        original_evidence = upstream_evidence(raw)
        evidence.update(original_evidence)
        counts = cast(dict[str, int], original_evidence["counts"])
        if counts["errors"]:
            outcome, report_outcome = "collection_error", "error"
            error = "upstream JUnit contains collection/execution errors"
        elif counts["failures"]:
            outcome, report_outcome = "behavior_failure", "failure"
            error = "upstream JUnit contains behavioral failures"
        elif counts["passed"] < 1:
            outcome, report_outcome = "collection_error", "error"
            error = "upstream JUnit contains no genuine passes"
        elif completed.returncode != 0:
            # A clean JUnit plus nonzero wrapper exit has the existing host
            # operational_error meaning, rather than inventing a failed assertion.
            outcome = "operational_error"
            error = (
                f"upstream pytest exited {completed.returncode} "
                "without behavioral failures"
            )
    except (OSError, ValueError, ElementTree.ParseError) as exc:
        outcome, report_outcome = "collection_error", "error"
        error = str(exc)
    evidence["workflow_outcome"] = outcome
    if error is not None:
        evidence["workflow_error"] = error
    ElementTree.SubElement(case, "system-out").text = json.dumps(
        evidence, sort_keys=True
    )
    if report_outcome is not None:
        suite.set("errors" if report_outcome == "error" else "failures", "1")
        ElementTree.SubElement(case, report_outcome, message=error).text = error
    ElementTree.ElementTree(suite).write(
        output.parent / "upstream-workflow.xml", encoding="utf-8", xml_declaration=True
    )
    return 1 if error is not None else 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        choices=[
            "upstream-workflow",
            "defaults",
            "equals",
            "integrated",
            "negative",
            "lint",
        ],
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
    # Preserve the declared reports/ artifact path under the provided capability.
    # Ordinary host invocations retain their repository-relative reports/ contract.
    provided_output = os.environ.get("HANDLER_CHECK_OUTPUT")
    output_base = root if provided_output is None else Path(provided_output)
    if not output_base.is_absolute() or not output_base.is_dir():
        raise RuntimeError("HANDLER_CHECK_OUTPUT must name an existing absolute root")
    reports = output_base / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    output = str(reports / args.mode)
    Path(output).mkdir(exist_ok=True)
    temporary = Path(output) / "tmpdir"
    if temporary.exists():
        shutil.rmtree(temporary)
    temporary.mkdir()
    os.environ["TMPDIR"] = str(temporary)
    tempfile.tempdir = None
    # Preserve the original report descriptor across pytest fd2 redirection.
    diagnostic = os.fdopen(os.dup(2), "w")
    faulthandler.register(signal.SIGSYS, file=diagnostic, all_threads=True, chain=True)
    if args.mode == "lint":
        # Every run is cold, as the historical workflow was.
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
        "upstream-workflow": [
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
    command = [
        "-q",
        "-p",
        "no:cacheprovider",
        "--tb=short",
        *target,
        f"--basetemp={output}/tmp",
    ]
    try:
        if args.mode == "upstream-workflow":
            return run_upstream(root, Path(output), command)
        return int(pytest.main([*command, f"--junitxml={output}.xml"]))
    finally:
        shutil.rmtree(temporary)
        faulthandler.unregister(signal.SIGSYS)
        diagnostic.close()


if __name__ == "__main__":
    raise SystemExit(main())
