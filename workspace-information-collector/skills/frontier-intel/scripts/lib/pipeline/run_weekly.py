from __future__ import annotations

from pathlib import Path

from scripts.lib.pipeline.digest_weekly import build_weekly_digest_markdown
from scripts.lib.storage.items_store import ItemsStore
from scripts.utils.dates import current_week_key


def run_weekly(skill_root: Path, digest_date: str) -> tuple[str, str]:
    project_root = skill_root.parent.parent / "projects" / "frontier-intel"
    store = ItemsStore(project_root)
    items = store.load_items(digest_date)
    week_key = current_week_key()
    markdown = build_weekly_digest_markdown(week_key, items)
    target = project_root / "digests" / "weekly" / f"{week_key}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(markdown)
    return week_key, markdown
