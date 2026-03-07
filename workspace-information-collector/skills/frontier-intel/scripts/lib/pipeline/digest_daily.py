from __future__ import annotations

from scripts.lib.models.item import FrontierItem
from scripts.lib.pipeline.selection import build_highlight_items, select_digest_items


def build_daily_digest_markdown(digest_date: str, items: list[FrontierItem]) -> str:
    grouped = select_digest_items(items)

    lines: list[str] = [f"# Daily Frontier AI Wrap-up — {digest_date}", ""]
    lines.extend(_build_exec_summary(items))
    lines.append("")
    lines.extend(_build_highlights(items))
    lines.append("")

    for section_name, item_type in (
        ("Top News", "news"),
        ("Top GitHub Repos", "github"),
        ("Top arXiv Papers", "arxiv"),
        ("Top Twitter Signals", "tweet"),
        ("Top Reddit Signals", "reddit"),
    ):
        section_items = grouped.get(item_type, [])
        if not section_items:
            continue
        lines.append(f"## {section_name}")
        lines.append("")
        for index, item in enumerate(section_items, start=1):
            lines.extend(_render_item(index, item))
            lines.append("")

    return "\n".join(line.rstrip() for line in lines).strip() + "\n"


def _build_exec_summary(items: list[FrontierItem]) -> list[str]:
    item_count = len(items)
    source_mix = sorted({item.type for item in items})
    summary = ", ".join(source_mix) if source_mix else "no sources"
    return [
        "## Executive Summary",
        "",
        f"- Collected `{item_count}` frontier AI items across: {summary}.",
        "- Every item below includes source links; arXiv items include direct PDF links.",
    ]


def _build_highlights(items: list[FrontierItem]) -> list[str]:
    highlights: list[str] = ["## Key Highlights", ""]
    top_items = build_highlight_items(items)
    if not top_items:
        highlights.append("- No high-signal items collected yet.")
        return highlights
    for item in top_items:
        bullet = item.executive_summary or item.summary or item.title
        prefix = item.type.upper()
        highlights.append(f"- [{prefix}] {bullet}")
    return highlights


def _render_item(index: int, item: FrontierItem) -> list[str]:
    lines = [f"### {index}. {item.title}"]
    if item.executive_summary:
        lines.append(f"- **Executive Summary:** {item.executive_summary}")
    elif item.summary:
        lines.append(f"- **Summary:** {item.summary}")
    if item.highlights:
        lines.append(f"- **Highlights:** {'; '.join(item.highlights)}")
    if item.suggested_actions:
        lines.append(f"- **Suggested Actions:** {'; '.join(item.suggested_actions)}")
    if item.learning:
        lines.append(f"- **Learning:** {'; '.join(item.learning)}")
    lines.append(f"- **Source:** {item.url}")
    if item.type == "arxiv" and item.pdf_url:
        lines.append(f"- **PDF:** {item.pdf_url}")
    return lines
