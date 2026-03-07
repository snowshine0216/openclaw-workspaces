from __future__ import annotations

from scripts.lib.models.item import FrontierItem


def build_items_database_properties() -> dict:
    return {
        "Title": {"title": {}},
        "Type": {"select": {"options": _options(["News", "GitHub", "arXiv", "Tweet", "Reddit"])}},
        "Source": {"rich_text": {}},
        "Published At": {"date": {}},
        "URL": {"url": {}},
        "PDF URL": {"url": {}},
        "Executive Summary": {"rich_text": {}},
        "Highlights": {"rich_text": {}},
        "Suggested Actions": {"rich_text": {}},
        "Learning": {"rich_text": {}},
        "Digest Date": {"date": {}},
        "Week": {"rich_text": {}},
        "Dedup Key": {"rich_text": {}},
    }


def build_digests_database_properties() -> dict:
    return {
        "Title": {"title": {}},
        "Period": {"select": {"options": _options(["Daily", "Weekly"])}},
        "Digest Date": {"date": {}},
        "Week": {"rich_text": {}},
        "Executive Summary": {"rich_text": {}},
        "Top Highlights": {"rich_text": {}},
        "Suggested Actions": {"rich_text": {}},
        "Learning Themes": {"rich_text": {}},
        "Item Count": {"number": {}},
    }


def build_item_page_properties(item: FrontierItem) -> dict:
    return {
        "Title": _title(item.title),
        "Type": {"select": {"name": _type_name(item.type)}},
        "Source": _rich_text(item.source),
        "Published At": _date(item.published_at),
        "URL": {"url": item.url or None},
        "PDF URL": {"url": item.pdf_url or None},
        "Executive Summary": _rich_text(item.executive_summary),
        "Highlights": _rich_text(_join_lines(item.highlights)),
        "Suggested Actions": _rich_text(_join_lines(item.suggested_actions)),
        "Learning": _rich_text(_join_lines(item.learning)),
        "Digest Date": _date(item.digest_date),
        "Week": _rich_text(item.week_key or ""),
        "Dedup Key": _rich_text(item.id),
    }


def build_digest_page_properties(
    *,
    title: str,
    period: str,
    digest_date: str,
    week_key: str,
    executive_summary: str,
    top_highlights: list[str],
    suggested_actions: list[str],
    learning_themes: list[str],
    item_count: int,
) -> dict:
    return {
        "Title": _title(title),
        "Period": {"select": {"name": period}},
        "Digest Date": _date(digest_date),
        "Week": _rich_text(week_key),
        "Executive Summary": _rich_text(executive_summary),
        "Top Highlights": _rich_text(_join_lines(top_highlights)),
        "Suggested Actions": _rich_text(_join_lines(suggested_actions)),
        "Learning Themes": _rich_text(_join_lines(learning_themes)),
        "Item Count": {"number": item_count},
    }


def _options(names: list[str]) -> list[dict]:
    return [{"name": name} for name in names]


def _title(content: str) -> dict:
    return {"title": [{"text": {"content": content}}]}


def _rich_text(content: str) -> dict:
    return {"rich_text": [{"text": {"content": content[:1900]}}]} if content else {"rich_text": []}


def _date(value: str | None) -> dict:
    return {"date": {"start": value}} if value else {"date": None}


def _join_lines(values: list[str]) -> str:
    return "\n".join(value for value in values if value)


def _type_name(item_type: str) -> str:
    mapping = {
        "news": "News",
        "github": "GitHub",
        "arxiv": "arXiv",
        "tweet": "Tweet",
        "reddit": "Reddit",
    }
    return mapping[item_type]
