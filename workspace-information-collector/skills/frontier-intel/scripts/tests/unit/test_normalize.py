import unittest

from scripts.lib.pipeline.normalize import normalize_item


class NormalizeItemTest(unittest.TestCase):
    def test_normalize_item_includes_primary_url_in_source_urls(self) -> None:
        item = normalize_item(
            {
                "type": "arxiv",
                "title": "Test Paper",
                "source": "arXiv",
                "url": "https://arxiv.org/abs/1234.5678",
                "pdf_url": "https://arxiv.org/pdf/1234.5678.pdf",
            }
        )

        self.assertEqual(item.url, "https://arxiv.org/abs/1234.5678")
        self.assertEqual(item.source_urls[0], "https://arxiv.org/abs/1234.5678")
        self.assertEqual(item.pdf_url, "https://arxiv.org/pdf/1234.5678.pdf")


if __name__ == "__main__":
    unittest.main()
