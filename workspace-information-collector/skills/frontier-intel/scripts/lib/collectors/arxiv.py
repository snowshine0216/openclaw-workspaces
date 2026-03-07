from __future__ import annotations

import xml.etree.ElementTree as ET
from urllib.request import urlopen

from scripts.lib.collectors.base import Collector
from scripts.lib.models.item import FrontierItem
from scripts.utils.dates import current_digest_date, current_week_key, utc_now_iso
from scripts.utils.summarizer import Summarizer

ARXIV_API = "https://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


class ArxivCollector(Collector):
    source_type = "arxiv"

    def __init__(self, limit: int = 5) -> None:
        self.limit = limit
        self.summarizer = Summarizer()

    def collect(self) -> list[FrontierItem]:
        try:
            with urlopen(ARXIV_API.format(limit=self.limit)) as response:
                payload = response.read().decode()
        except Exception:
            return []

        root = ET.fromstring(payload)
        items: list[FrontierItem] = []
        for entry in root.findall("atom:entry", ATOM_NS):
            url = self._text(entry, "atom:id")
            pdf_url = self._pdf_url(entry)
            title = " ".join(self._text(entry, "atom:title").split())
            abstract = " ".join(self._text(entry, "atom:summary").split())
            published_at = self._text(entry, "atom:published")
            paper_id = url.rsplit("/", 1)[-1] if url else title
            summary = self.summarizer.summarize_text(item_type="arxiv", title=title, text=abstract)
            items.append(
                FrontierItem(
                    id=paper_id,
                    type="arxiv",
                    title=title,
                    source="arXiv",
                    url=url,
                    source_urls=[candidate for candidate in [url, pdf_url] if candidate],
                    pdf_url=pdf_url,
                    published_at=published_at,
                    collected_at=utc_now_iso(),
                    summary=summary,
                    executive_summary=summary,
                    highlights=[f"Published: {published_at[:10]}"] if published_at else [],
                    suggested_actions=[],
                    learning=[],
                    tags=["arxiv", "research"],
                    week_key=current_week_key(),
                    digest_date=current_digest_date(),
                    raw_source_type="arxiv",
                    score=100.0,
                )
            )
        return items

    def _text(self, entry: ET.Element, selector: str) -> str:
        node = entry.find(selector, ATOM_NS)
        return (node.text or "").strip() if node is not None else ""

    def _pdf_url(self, entry: ET.Element) -> str | None:
        for link in entry.findall("atom:link", ATOM_NS):
            if link.attrib.get("title") == "pdf":
                return link.attrib.get("href")
        return None
