from __future__ import annotations

import re
from html import unescape

MULTISPACE_PATTERN = re.compile(r"\s+")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\([^\)]+\)")
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])\s+")
DATE_LEAD_PATTERN = re.compile(r"^[A-Z][a-z]+\s+\d{1,2},\s+\d{4}[)\-,:\s]+")

NOISE_PATTERNS = [
    re.compile(r"skip to main content.*", re.IGNORECASE),
    re.compile(r"toggle main menu.*", re.IGNORECASE),
    re.compile(r"search for: submit.*", re.IGNORECASE),
    re.compile(r"home canada business investing life opinion world politics.*", re.IGNORECASE),
    re.compile(r"find clarity in the chaos.*", re.IGNORECASE),
    re.compile(r"published time:.*", re.IGNORECASE),
    re.compile(r"markdown content:.*", re.IGNORECASE),
    re.compile(r"url source:.*", re.IGNORECASE),
    re.compile(r"title:.*", re.IGNORECASE),
]


def clean_summary_text(text: str, limit: int = 280) -> str:
    if not text:
        return ""
    cleaned = unescape(text)
    cleaned = MARKDOWN_LINK_PATTERN.sub(r"\1", cleaned)
    cleaned = cleaned.replace("#", " ").replace("*", " ")
    cleaned = MULTISPACE_PATTERN.sub(" ", cleaned).strip()
    cleaned = DATE_LEAD_PATTERN.sub("", cleaned).strip()
    lower_cleaned = cleaned.lower()
    for marker in [
        "skip to main content",
        "toggle main menu",
        "search for: submit",
        "url source:",
        "markdown content:",
        "published time:",
    ]:
        idx = lower_cleaned.find(marker)
        if idx != -1:
            cleaned = cleaned[:idx].strip()
            lower_cleaned = cleaned.lower()
    for pattern in NOISE_PATTERNS:
        cleaned = pattern.sub("", cleaned).strip()
    sentences = _unique_sentences(cleaned)
    compact = " ".join(sentences[:3]).strip()
    compact = _trim_to_sentence(compact, limit)
    return compact


def first_sentence(text: str, limit: int = 220) -> str:
    cleaned = clean_summary_text(text, limit=limit * 2)
    if not cleaned:
        return ""
    sentences = _unique_sentences(cleaned)
    if not sentences:
        return _trim_to_sentence(cleaned, limit)
    return _trim_to_sentence(sentences[0], limit)


def concise_summary(*, title: str, text: str, max_sentences: int = 2, limit: int = 420) -> str:
    cleaned = clean_summary_text(text, limit=limit * 2)
    if not cleaned:
        return unescape(title.strip())
    title_norm = _normalize(title)
    filtered: list[str] = []
    seen_filtered: set[str] = set()
    for sentence in _unique_sentences(cleaned):
        sentence_norm = _normalize(sentence)
        if not sentence_norm:
            continue
        if sentence_norm == title_norm:
            continue
        if sentence_norm.startswith(title_norm):
            sentence = sentence[len(title):].lstrip(" :-—–")
            sentence_norm = _normalize(sentence)
        if sentence_norm and sentence_norm not in seen_filtered:
            filtered.append(sentence)
            seen_filtered.add(sentence_norm)
        if len(filtered) >= max_sentences:
            break
    if not filtered:
        return unescape(title.strip())
    joined = " ".join(filtered).strip()
    return _trim_to_sentence(joined, limit)


def _unique_sentences(text: str) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for sentence in SENTENCE_SPLIT_PATTERN.split(text):
        sentence = sentence.strip()
        normalized = _normalize(sentence)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        unique.append(sentence)
    return unique


def _trim_to_sentence(text: str, limit: int) -> str:
    text = text[:limit].rstrip()
    last_punct = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
    if last_punct >= 40:
        return text[: last_punct + 1].rstrip()
    return text.rstrip(' ,;:-')


def _normalize(text: str) -> str:
    return MULTISPACE_PATTERN.sub(" ", unescape(text)).strip().lower()
