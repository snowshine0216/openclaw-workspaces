from __future__ import annotations

import re
from urllib.request import Request, urlopen

JINA_PREFIX = "https://r.jina.ai/http://"
JINA_WRAPPER_START = "Title: "
JINA_MARKDOWN_MARKER = "Markdown Content:"
WRAPPER_SIGNALS = (
    "title:",
    "url source:",
    "published time:",
    "markdown content:",
)
NOISE_PATTERNS = [
    re.compile(r"^Title:\s*.*$", re.MULTILINE),
    re.compile(r"^URL Source:\s*.*$", re.MULTILINE),
    re.compile(r"^Published Time:\s*.*$", re.MULTILINE),
    re.compile(r"^Markdown Content:\s*", re.MULTILINE),
]


def fetch_url_text(url: str, timeout: int = 30) -> str:
    if not url:
        return ""
    candidates: list[tuple[str, str]] = []
    if url.startswith("https://"):
        candidates.append(("jina", JINA_PREFIX + url.removeprefix("https://")))
        candidates.append(("direct", url))
    elif url.startswith("http://"):
        candidates.append(("jina", "https://r.jina.ai/http://" + url.removeprefix("http://")))
        candidates.append(("direct", url))
    else:
        candidates.append(("direct", url))
    best_text = ""
    for source_type, candidate in candidates:
        try:
            request = Request(candidate, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(request, timeout=timeout) as response:
                raw_text = response.read().decode(errors="ignore")
            cleaned = _clean_fetched_text(raw_text, source_type=source_type)
            if _looks_usable(cleaned):
                return cleaned
            if len(cleaned) > len(best_text):
                best_text = cleaned
        except Exception:
            continue
    return ""


def _clean_fetched_text(text: str, *, source_type: str) -> str:
    cleaned = text.strip()
    if source_type == "jina":
        cleaned = _strip_jina_wrapper(cleaned)
    for pattern in NOISE_PATTERNS:
        cleaned = pattern.sub("", cleaned)
    return cleaned.strip()


def _strip_jina_wrapper(text: str) -> str:
    if JINA_MARKDOWN_MARKER in text:
        text = text.split(JINA_MARKDOWN_MARKER, 1)[1].strip()
    elif text.startswith(JINA_WRAPPER_START):
        parts = text.split("\n\n", 1)
        if len(parts) == 2:
            text = parts[1].strip()
    return text


def _looks_usable(text: str) -> bool:
    if not text or len(text) < 200:
        return False
    lowered = text.lower()
    bad_signals = [
        "toggle main menu",
        "search for:",
        "home canada business investing life opinion world politics",
        "buy/sell trade spot",
        "copy trading",
        "title:",
        "url source:",
        "markdown content:",
        "published time:",
    ]
    if any(signal in lowered for signal in bad_signals):
        return False
    wrapper_hits = sum(signal in lowered for signal in WRAPPER_SIGNALS)
    if wrapper_hits >= 2:
        return False
    return True
