from __future__ import annotations

import math

from scripts.lib.models.item import FrontierItem


def score_item(item: FrontierItem) -> float:
    if item.type == "arxiv":
        return 60.0
    if item.type == "github":
        return min(item.score or 0.0, 80.0)
    if item.type == "news":
        return 55.0
    if item.type == "tweet":
        return 45.0
    if item.type == "reddit":
        return min(25.0 + math.log10(max(item.score, 1.0)) * 10.0, 50.0)
    return item.score


def apply_scores(items: list[FrontierItem]) -> list[FrontierItem]:
    for item in items:
        item.score = score_item(item)
    return items
