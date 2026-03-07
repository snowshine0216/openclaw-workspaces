import unittest

from scripts.lib.models.item import FrontierItem
from scripts.lib.pipeline.digest_daily import build_daily_digest_markdown


class DailyDigestTest(unittest.TestCase):
    def test_daily_digest_contains_source_and_pdf_links_for_arxiv(self) -> None:
        item = FrontierItem(
            id="paper-1",
            type="arxiv",
            title="A Good Paper",
            source="arXiv",
            url="https://arxiv.org/abs/1234.5678",
            pdf_url="https://arxiv.org/pdf/1234.5678.pdf",
            executive_summary="Why it matters.",
        )

        markdown = build_daily_digest_markdown("2026-03-06", [item])

        self.assertIn("https://arxiv.org/abs/1234.5678", markdown)
        self.assertIn("https://arxiv.org/pdf/1234.5678.pdf", markdown)
        self.assertIn("## Executive Summary", markdown)


if __name__ == "__main__":
    unittest.main()
