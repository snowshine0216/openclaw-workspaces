from __future__ import annotations

import json
from pathlib import Path

from scripts.lib.models.item import FrontierItem


class ItemsStore:
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def path_for_date(self, digest_date: str) -> Path:
        return self.base_dir / "items" / f"{digest_date}.json"

    def save_items(self, digest_date: str, items: list[FrontierItem]) -> Path:
        target = self.path_for_date(digest_date)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = [item.to_dict() for item in items]
        target.write_text(json.dumps(payload, indent=2, sort_keys=True))
        return target

    def load_items(self, digest_date: str) -> list[FrontierItem]:
        target = self.path_for_date(digest_date)
        if not target.exists():
            return []
        raw_items = json.loads(target.read_text())
        return [FrontierItem.from_dict(item) for item in raw_items]
