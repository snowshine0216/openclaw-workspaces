from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonStateStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self, default: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.path.exists():
            return default or {}
        return json.loads(self.path.read_text())

    def write(self, payload: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True))
