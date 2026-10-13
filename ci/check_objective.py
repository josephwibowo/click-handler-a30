"""Run one frozen objective check against this checkout's actual Click source."""

from __future__ import annotations

import argparse
import os
import sys
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

    import pytest

    import click

    if Path(click.__file__).resolve() != root / "src/click/__init__.py":
        raise RuntimeError(
            "the check imported Click from outside its approved candidate"
        )
    target = {
        "upstream": ["tests"],
        "defaults": ["acceptance/test_completion_defaults.py"],
        "equals": [
            "acceptance/test_completion_equals.py",
            "acceptance/test_completion_integrated.py",
        ],
        "integrated": ["acceptance"],
        "negative": ["acceptance/test_negative_inputs.py"],
    }[args.mode]
    output = f"reports/{args.mode}"
    (root / output).mkdir(parents=True, exist_ok=True)
    return int(
        pytest.main(
            [
                "-q",
                "-p",
                "no:cacheprovider",
                "--tb=short",
                *target,
                f"--basetemp={output}/tmp",
                f"--junitxml={output}/junit.xml",
            ]
        )
    )


if __name__ == "__main__":
    raise SystemExit(main())
