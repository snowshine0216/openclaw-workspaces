from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class FrontierItem:
    id: str
    type: str
    title: str
    source: str
    url: str
    source_urls: list[str] = field(default_factory=list)
    pdf_url: str | None = None
    published_at: str | None = None
    collected_at: str | None = None
    summary: str = ""
    executive_summary: str = ""
    highlights: list[str] = field(default_factory=list)
    suggested_actions: list[str] = field(default_factory=list)
    learning: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    week_key: str | None = None
    digest_date: str | None = None
    raw_source_type: str = ""
    score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "FrontierItem":
        return cls(**payload)
