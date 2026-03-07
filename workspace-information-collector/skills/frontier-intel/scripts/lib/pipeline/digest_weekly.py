from __future__ import annotations

from collections import Counter

from scripts.lib.models.item import FrontierItem


def build_weekly_digest_markdown(week_key: str, items: list[FrontierItem]) -> str:
    lines: list[str] = [f"# Weekly Frontier AI Summary — {week_key}", ""]
    lines.extend(_build_week_summary(items))
    lines.append("")
    lines.extend(_build_theme_section(items))
    lines.append("")
    lines.extend(_build_actions_section(items))
    return "\n".join(line.rstrip() for line in lines).strip() + "\n"


def _build_week_summary(items: list[FrontierItem]) -> list[str]:
    return [
        "## Week in One Paragraph",
        "",
        f"- This week captured `{len(items)}` frontier AI items with a mix of research, tooling, and fast-moving social signals.",
        "- The weekly digest is designed to be shareable: concise, source-linked, and readable out of context.",
    ]


def _build_theme_section(items: list[FrontierItem]) -> list[str]:
    counts = Counter(item.type for item in items)
    return [
        "## Biggest Themes",
        "",
        f"- Research volume: `{counts.get('arxiv', 0)}` arXiv items.",
        f"- Builder/tooling signal: `{counts.get('github', 0)}` GitHub items.",
        f"- Social/community signal: `{counts.get('tweet', 0) + counts.get('reddit', 0)}` Twitter/Reddit items.",
        f"- News signal: `{counts.get('news', 0)}` web/news items.",
    ]


def _build_actions_section(items: list[FrontierItem]) -> list[str]:
    actions = [action for item in items for action in item.suggested_actions][:5]
    lines = ["## Suggested Actions for Next Week", ""]
    if not actions:
        lines.append("- Review top weekly items and decide which ones deserve deeper follow-up.")
        return lines
    for action in actions:
        lines.append(f"- {action}")
    return lines
