import unittest

from scripts.lib.models.item import FrontierItem
from scripts.lib.pipeline.dedupe import dedupe_items


class DedupeItemsTest(unittest.TestCase):
    def test_dedupe_items_collapses_same_github_repo(self) -> None:
        first = FrontierItem(
            id="",
            type="github",
            title="Repo A",
            source="GitHub",
            url="https://github.com/openai/openai-python",
        )
        second = FrontierItem(
            id="",
            type="github",
            title="Repo A duplicate",
            source="GitHub",
            url="https://github.com/openai/openai-python/",
        )

        items = dedupe_items([first, second])

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id, "openai/openai-python")


if __name__ == "__main__":
    unittest.main()
