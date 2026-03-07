import unittest

from scripts.lib.models.item import FrontierItem
from scripts.lib.notion.schema import build_digest_page_properties, build_item_page_properties


class NotionSchemaTest(unittest.TestCase):
    def test_item_payload_contains_pdf_url_for_arxiv(self) -> None:
        item = FrontierItem(
            id="paper-1",
            type="arxiv",
            title="Paper",
            source="arXiv",
            url="https://arxiv.org/abs/1234.5678",
            pdf_url="https://arxiv.org/pdf/1234.5678.pdf",
        )

        payload = build_item_page_properties(item)

        self.assertEqual(payload["URL"]["url"], "https://arxiv.org/abs/1234.5678")
        self.assertEqual(payload["PDF URL"]["url"], "https://arxiv.org/pdf/1234.5678.pdf")
        self.assertEqual(payload["Type"]["select"]["name"], "arXiv")

    def test_digest_payload_contains_expected_fields(self) -> None:
        payload = build_digest_page_properties(
            title="Daily Wrap-up",
            period="Daily",
            digest_date="2026-03-07",
            week_key="2026-W10",
            executive_summary="Summary",
            top_highlights=["A"],
            suggested_actions=["B"],
            learning_themes=["C"],
            item_count=3,
        )

        self.assertEqual(payload["Period"]["select"]["name"], "Daily")
        self.assertEqual(payload["Item Count"]["number"], 3)
        self.assertIn("Executive Summary", payload)


if __name__ == "__main__":
    unittest.main()
