#!/usr/bin/env python3

from pathlib import Path

from scripts.lib.models.item import FrontierItem
from scripts.lib.notion.schema import build_digest_page_properties, build_item_page_properties


def main() -> None:
    skill_root = Path(__file__).resolve().parents[2]
    sample_item = FrontierItem(
        id="sample-item",
        type="arxiv",
        title="Sample Frontier Paper",
        source="arXiv",
        url="https://arxiv.org/abs/1234.5678",
        pdf_url="https://arxiv.org/pdf/1234.5678.pdf",
        executive_summary="This is a dry-run payload preview.",
        digest_date="2026-03-07",
        week_key="2026-W10",
    )
    item_payload = build_item_page_properties(sample_item)
    digest_payload = build_digest_page_properties(
        title="Daily Frontier AI Wrap-up — 2026-03-07",
        period="Daily",
        digest_date="2026-03-07",
        week_key="2026-W10",
        executive_summary="Dry-run digest payload preview.",
        top_highlights=["Highlight one"],
        suggested_actions=["Action one"],
        learning_themes=["Learning one"],
        item_count=1,
    )
    print(f"frontier-intel notion dry-run scaffold: {skill_root}")
    print(f"item fields={sorted(item_payload.keys())}")
    print(f"digest fields={sorted(digest_payload.keys())}")


if __name__ == "__main__":
    main()
