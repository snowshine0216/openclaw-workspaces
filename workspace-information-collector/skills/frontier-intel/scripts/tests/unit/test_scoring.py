import unittest

from scripts.lib.models.item import FrontierItem
from scripts.lib.pipeline.scoring import apply_scores


class ScoringTest(unittest.TestCase):
    def test_reddit_score_is_capped_below_arxiv(self) -> None:
        reddit = FrontierItem(id="r1", type="reddit", title="Reddit", source="Reddit", url="https://reddit.com", score=100000)
        arxiv = FrontierItem(id="a1", type="arxiv", title="Paper", source="arXiv", url="https://arxiv.org/abs/1")

        scored = apply_scores([reddit, arxiv])

        score_by_id = {item.id: item.score for item in scored}
        self.assertLess(score_by_id["r1"], score_by_id["a1"])


if __name__ == "__main__":
    unittest.main()
