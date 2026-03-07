import unittest

from scripts.lib.models.item import FrontierItem
from scripts.lib.pipeline.digest_weekly import build_weekly_digest_markdown


class WeeklyDigestTest(unittest.TestCase):
    def test_weekly_digest_is_shareable_and_source_aware(self) -> None:
        item = FrontierItem(
            id="repo-1",
            type="github",
            title="Useful Repo",
            source="GitHub",
            url="https://github.com/example/repo",
            suggested_actions=["Try the repo this week."],
        )

        markdown = build_weekly_digest_markdown("2026-W10", [item])

        self.assertIn("# Weekly Frontier AI Summary", markdown)
        self.assertIn("## Suggested Actions for Next Week", markdown)
        self.assertIn("Try the repo this week.", markdown)


if __name__ == "__main__":
    unittest.main()
