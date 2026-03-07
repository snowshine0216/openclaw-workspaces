from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass


@dataclass(slots=True)
class CommandResult:
    stdout: str
    stderr: str
    returncode: int

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def run_command(args: list[str], timeout: int = 60) -> CommandResult:
    completed = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    return CommandResult(
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
    )


def load_json_output(args: list[str], timeout: int = 60) -> object:
    result = run_command(args, timeout=timeout)
    if not result.ok:
        raise RuntimeError(result.stderr.strip() or f"Command failed: {' '.join(args)}")
    return json.loads(result.stdout)
