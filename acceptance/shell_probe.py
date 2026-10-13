"""Bounded interaction with generated completion in a real, clean shell."""

from __future__ import annotations

import json
import os
import pty
import re
import select
import shutil
import subprocess
import sys
import time
from pathlib import Path

_TIMEOUT = 10.0


def _read_until(fd: int, expected: bytes, timeout: float = _TIMEOUT) -> bytes:
    deadline = time.monotonic() + timeout
    output = bytearray()
    while time.monotonic() < deadline:
        ready, _, _ = select.select(
            [fd], [], [], max(0.0, min(0.1, deadline - time.monotonic()))
        )
        if ready:
            try:
                output.extend(os.read(fd, 65536))
            except OSError as exc:
                raise RuntimeError("completion shell closed before its result") from exc
            if expected in output:
                return bytes(output)
    raise RuntimeError(f"completion shell exceeded its bound: {output[-4096:]!r}")


def complete_and_invoke(
    root: Path,
    shell: str,
    command: str,
    *,
    expected: str = "always",
    choices: tuple[str, ...] = ("auto", "always", "never"),
) -> dict[str, object]:
    executable = shutil.which(shell)
    if executable is None:
        raise RuntimeError(f"required completion shell is absent: {shell}")
    version = subprocess.run(
        [executable, "--version"],
        check=True,
        capture_output=True,
        timeout=5,
    ).stdout.decode()
    if shell == "bash":
        match = re.search(r"version (\d+)\.(\d+)", version)
        if match is None or tuple(map(int, match.groups())) < (4, 4):
            raise RuntimeError("the objective requires Bash >=4.4")

    binroot = root / "bin"
    binroot.mkdir()
    cli = binroot / "gobble"
    marker = root / "callable-default"
    program = f"""#!{sys.executable}
import json
from pathlib import Path
import click
def default():
    with Path({str(marker)!r}).open("a", encoding="utf-8") as stream:
        stream.write("called\\n")
    return "calculated"
@click.command()
@click.option("--color", type=click.Choice({choices!r}))
@click.option("--name", default=default)
def main(color, name):
    click.echo("A30_RESULT=" + json.dumps({{"color": color, "name": name}}))
if __name__ == "__main__":
    main()
"""
    cli.write_text(program, encoding="utf-8")
    cli.chmod(0o700)
    source_root = Path(__file__).resolve().parents[1] / "src"
    environment = {
        "PATH": os.pathsep.join(
            [str(binroot), str(Path(sys.executable).parent), "/usr/bin", "/bin"]
        ),
        "PYTHONPATH": str(source_root),
        "PYTHONDONTWRITEBYTECODE": "1",
        "TERM": "xterm",
        "LC_ALL": "C",
    }
    master, slave = pty.openpty()
    argv = (
        [executable, "--noprofile", "--norc", "-i"]
        if shell == "bash"
        else [executable, "-f"]
    )
    process = subprocess.Popen(
        argv,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        env=environment,
        start_new_session=True,
    )
    os.close(slave)
    transcript = bytearray()
    try:
        setup = (
            "autoload -Uz compinit; compinit -D; PROMPT='A30> '; "
            if shell == "zsh"
            else "PS1='A30> '; "
        )
        setup += f'eval "$(_GOBBLE_COMPLETE={shell}_source gobble)"; echo A30_READY\n'
        os.write(master, setup.encode())
        transcript.extend(_read_until(master, b"\r\nA30_READY\r\n"))
        os.write(master, (command + "\t").encode())
        transcript.extend(_read_until(master, expected.split()[-1].encode()))
        completion_called_default = marker.exists()
        os.write(master, b"\n")
        output = _read_until(master, b"A30> ")
        transcript.extend(output)
        text = output.decode(errors="replace")
        match = re.search(r"A30_RESULT=(\{[^\r\n]*\})", text)
        if match is None:
            raise RuntimeError(f"completed command did not invoke correctly: {text!r}")
        observation = json.loads(match.group(1))
        return {
            "shell": shell,
            "version": version.splitlines()[0],
            "completion_called_default": completion_called_default,
            "result": observation,
            "invocation_calls": marker.read_text(encoding="utf-8").splitlines(),
            "transcript": transcript.decode(errors="replace"),
        }
    finally:
        if process.poll() is None:
            os.write(master, b"exit\n")
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=2)
        os.close(master)
