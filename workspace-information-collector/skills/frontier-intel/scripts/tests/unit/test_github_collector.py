import unittest
from unittest.mock import patch

from scripts.lib.collectors.github import GitHubCollector


class GitHubCollectorTest(unittest.TestCase):
    @patch.object(GitHubCollector, "_fetch_trending_payload", return_value=[])
    @patch("scripts.lib.collectors.github.load_json_output")
    def test_collect_maps_github_repos(self, mocked_load_json_output, _mocked_trending_payload) -> None:
        mocked_load_json_output.return_value = [
            {
                "nameWithOwner": "openai/openai-python",
                "description": "OpenAI Python client",
                "url": "https://github.com/openai/openai-python",
                "updatedAt": "2026-03-07T00:00:00Z",
                "stargazersCount": 123,
            }
        ]
        collector = GitHubCollector(limit=1)

        items = collector.collect()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id, "openai/openai-python")
        self.assertEqual(items[0].score, 123.0)


if __name__ == "__main__":
    unittest.main()
