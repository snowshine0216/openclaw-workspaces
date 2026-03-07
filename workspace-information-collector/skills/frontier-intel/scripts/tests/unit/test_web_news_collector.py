import unittest
from unittest.mock import patch

from scripts.lib.collectors.web_news import WebNewsCollector


class WebNewsCollectorTest(unittest.TestCase):
    @patch("scripts.lib.collectors.web_news.fetch_url_text", return_value="Microsoft released a compact multimodal model that selectively invokes reasoning, which matters because it aims to improve efficiency without paying the full reasoning cost on every request.")
    @patch("scripts.lib.collectors.web_news.Summarizer.summarize_text", return_value="Microsoft released a compact multimodal model that selectively invokes reasoning, which matters because it aims to improve efficiency without paying the full reasoning cost on every request.")
    @patch.object(WebNewsCollector, "_fetch_results")
    def test_collect_maps_results_into_items(self, mocked_fetch_results, _mocked_summarize_text, _mocked_fetch_url_text) -> None:
        mocked_fetch_results.return_value = [
            {
                "title": "Important AI News",
                "url": "https://example.com/news",
                "text": "A useful summary.",
                "source": "Example",
                "retrieval_source": "tavily",
            }
        ]
        collector = WebNewsCollector(limit=1)

        items = collector.collect()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].title, "Important AI News")
        self.assertEqual(items[0].url, "https://example.com/news")
        self.assertIn("compact multimodal model", items[0].executive_summary)


if __name__ == "__main__":
    unittest.main()
