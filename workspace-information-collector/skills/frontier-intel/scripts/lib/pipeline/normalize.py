from __future__ import annotations

from scripts.lib.models.item import FrontierItem
from scripts.utils.dates import current_digest_date, current_week_key, utc_now_iso


SUPPORTED_TYPES = {"news", "github", "arxiv", "tweet", "reddit"}


def normalize_item(raw_item: dict) -> FrontierItem:
    item_type = raw_item.get("type", "news")
    if item_type not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported frontier item type: {item_type}")
    source_urls = list(raw_item.get("source_urls") or [])
    url = raw_item.get("url", "")
    if url and url not in source_urls:
        source_urls.insert(0, url)
    return FrontierItem(
        id=raw_item.get("id", ""),
        type=item_type,
        title=raw_item.get("title", "").strip(),
        source=raw_item.get("source", "").strip(),
        url=url,
        source_urls=source_urls,
        pdf_url=raw_item.get("pdf_url"),
        published_at=raw_item.get("published_at"),
        collected_at=raw_item.get("collected_at") or utc_now_iso(),
        summary=raw_item.get("summary", "").strip(),
        executive_summary=raw_item.get("executive_summary", "").strip(),
        highlights=list(raw_item.get("highlights") or []),
        suggested_actions=list(raw_item.get("suggested_actions") or []),
        learning=list(raw_item.get("learning") or []),
        tags=list(raw_item.get("tags") or []),
        week_key=raw_item.get("week_key") or current_week_key(),
        digest_date=raw_item.get("digest_date") or current_digest_date(),
        raw_source_type=raw_item.get("raw_source_type", item_type),
        score=float(raw_item.get("score", 0.0)),
    )


def normalize_items(raw_items: list[dict]) -> list[FrontierItem]:
    return [normalize_item(raw_item) for raw_item in raw_items]
