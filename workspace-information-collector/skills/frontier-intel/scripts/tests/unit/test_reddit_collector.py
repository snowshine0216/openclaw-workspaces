import unittest

from scripts.lib.collectors.reddit import RedditCollector


class RedditCollectorTest(unittest.TestCase):
    def test_skip_meta_titles(self) -> None:
        collector = RedditCollector()

        self.assertTrue(collector._should_skip_title("[D] Monthly Who's Hiring and Who wants to be Hired?"))
        self.assertTrue(collector._should_skip_title("AMA with StepFun AI - Ask Us Anything"))
        self.assertFalse(collector._should_skip_title("Open-source agent framework ships new release"))


if __name__ == "__main__":
    unittest.main()
