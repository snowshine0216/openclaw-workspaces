from __future__ import annotations

import re

WRAPPER_PATTERNS = (
    "title:",
    "url source:",
    "published time:",
    "markdown content:",
    "skip to main content",
    "toggle main menu",
)
TRUNCATION_PATTERNS = (
    "...",
    "…",
)


def is_bad_summary(title: str, summary: str) -> bool:
    if not summary or len(summary.strip()) < 20:
        return True
    lowered = summary.lower()
    if any(token in lowered for token in WRAPPER_PATTERNS):
        return True
    normalized_title = _normalize(title)
    normalized_summary = _normalize(summary)
    if normalized_summary == normalized_title:
        return True
    if normalized_summary.startswith(normalized_title):
        return True
    if any(summary.rstrip().endswith(token) for token in TRUNCATION_PATTERNS):
        return True
    return False


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip().lower()
