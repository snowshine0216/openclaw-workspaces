from __future__ import annotations

import hashlib

from scripts.lib.models.item import FrontierItem
from scripts.utils.urls import canonicalize_url


SOURCE_TYPES_WITH_URL_KEYS = {"news", "tweet", "reddit"}


def build_dedup_key(item: FrontierItem) -> str:
    if item.type == "arxiv" and item.pdf_url:
        return item.id or item.pdf_url.rsplit("/", 1)[-1]
    if item.type == "github" and item.url:
        trimmed = canonicalize_url(item.url).replace("https://github.com/", "")
        return trimmed
    if item.url and item.type in SOURCE_TYPES_WITH_URL_KEYS:
        return hashlib.sha256(canonicalize_url(item.url).encode()).hexdigest()
    if item.url:
        return hashlib.sha256(item.url.encode()).hexdigest()
    return item.id


def dedupe_items(items: list[FrontierItem]) -> list[FrontierItem]:
    unique_items: dict[str, FrontierItem] = {}
    for item in items:
        dedup_key = build_dedup_key(item)
        item.id = dedup_key
        unique_items.setdefault(dedup_key, item)
    return list(unique_items.values())
