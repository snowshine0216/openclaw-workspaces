from __future__ import annotations

from collections import defaultdict
from urllib.parse import urlsplit

from scripts.lib.models.item import FrontierItem

MAX_SECTION_ITEMS = {
    "news": 6,
    "github": 5,
    "arxiv": 5,
    "tweet": 8,
    "reddit": 4,
}

OPENAI_HEAVY_HINTS = ("openai", "gpt", "chatgpt", "frontier")


def select_digest_items(items: list[FrontierItem]) -> dict[str, list[FrontierItem]]:
    grouped: dict[str, list[FrontierItem]] = defaultdict(list)
    for item in sorted(items, key=lambda current: current.score, reverse=True):
        grouped[item.type].append(item)

    selected: dict[str, list[FrontierItem]] = {}
    for item_type, candidates in grouped.items():
        limit = MAX_SECTION_ITEMS.get(item_type, 5)
        if item_type == "news":
            selected[item_type] = _select_diverse_news(candidates, limit)
        else:
            selected[item_type] = candidates[:limit]
    return selected


def build_highlight_items(items: list[FrontierItem]) -> list[FrontierItem]:
    selected = select_digest_items(items)
    highlights: list[FrontierItem] = []
    for item_type in ("news", "github", "arxiv", "tweet", "reddit"):
        bucket = selected.get(item_type, [])
        if bucket:
            highlights.append(bucket[0])
    return highlights[:5]


def _select_diverse_news(items: list[FrontierItem], limit: int) -> list[FrontierItem]:
    selected: list[FrontierItem] = []
    seen_domains: set[str] = set()
    openai_like_count = 0

    for item in items:
        domain = urlsplit(item.url).netloc.lower()
        title_lower = item.title.lower()
        openai_like = any(hint in title_lower for hint in OPENAI_HEAVY_HINTS)
        if domain in seen_domains:
            continue
        if openai_like and openai_like_count >= 1:
            continue
        selected.append(item)
        seen_domains.add(domain)
        if openai_like:
            openai_like_count += 1
        if len(selected) >= limit:
            break

    if len(selected) < limit:
        for item in items:
            if item in selected:
                continue
            selected.append(item)
            if len(selected) >= limit:
                break
    return selected
