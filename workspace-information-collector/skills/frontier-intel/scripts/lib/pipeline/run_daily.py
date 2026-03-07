from __future__ import annotations

from pathlib import Path

from scripts.lib.collectors.arxiv import ArxivCollector
from scripts.lib.collectors.github import GitHubCollector
from scripts.lib.collectors.reddit import RedditCollector
from scripts.lib.collectors.twitter import TwitterCollector
from scripts.lib.collectors.web_news import WebNewsCollector
from scripts.lib.models.item import FrontierItem
from scripts.lib.pipeline.dedupe import dedupe_items
from scripts.lib.pipeline.digest_daily import build_daily_digest_markdown
from scripts.lib.pipeline.scoring import apply_scores
from scripts.lib.storage.items_store import ItemsStore
from scripts.utils.dates import current_digest_date


COLLECTOR_TYPES = (
    WebNewsCollector,
    GitHubCollector,
    ArxivCollector,
    TwitterCollector,
    RedditCollector,
)


def collect_all_items() -> list[FrontierItem]:
    items: list[FrontierItem] = []
    for collector_type in COLLECTOR_TYPES:
        items.extend(collector_type().collect())
    return apply_scores(dedupe_items(items))


def run_daily(skill_root: Path) -> tuple[str, list[FrontierItem], Path]:
    digest_date = current_digest_date()
    items = collect_all_items()
    project_root = skill_root.parent.parent / "projects" / "frontier-intel"
    store = ItemsStore(project_root)
    store.save_items(digest_date, items)
    markdown = build_daily_digest_markdown(digest_date, items)
    target = project_root / "digests" / "daily" / f"{digest_date}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(markdown)
    return digest_date, items, target
