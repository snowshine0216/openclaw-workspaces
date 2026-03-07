from __future__ import annotations

import json
from urllib.request import Request, urlopen

from scripts.lib.collectors.base import Collector
from scripts.lib.models.item import FrontierItem
from scripts.utils.dates import current_digest_date, current_week_key, utc_now_iso
from scripts.utils.text import clean_summary_text

DEFAULT_SUBREDDITS = ["MachineLearning", "LocalLLaMA", "singularity"]
SKIP_TITLE_PREFIXES = (
    "[D] Monthly",
    "[D] Self-Promotion",
    "AMA ",
    "AMA with",
)
SKIP_TITLE_CONTAINS = (
    "who's hiring",
    "self-promotion",
)


class RedditCollector(Collector):
    source_type = "reddit"

    def __init__(self, subreddits: list[str] | None = None, per_subreddit: int = 3) -> None:
        self.subreddits = subreddits or DEFAULT_SUBREDDITS
        self.per_subreddit = per_subreddit

    def collect(self) -> list[FrontierItem]:
        items: list[FrontierItem] = []
        for subreddit in self.subreddits:
            try:
                payload = self._fetch_subreddit(subreddit)
            except Exception:
                continue
            children = payload.get("data", {}).get("children", [])[: self.per_subreddit]
            for child in children:
                data = child.get("data", {})
                permalink = data.get("permalink", "")
                url = f"https://www.reddit.com{permalink}" if permalink else data.get("url", "")
                title = data.get("title", "")
                if self._should_skip_title(title):
                    continue
                summary = clean_summary_text((data.get("selftext") or "").replace("\n", " "))
                score = float(data.get("score") or 0)
                post_id = data.get("id", url)
                items.append(
                    FrontierItem(
                        id=str(post_id),
                        type="reddit",
                        title=title,
                        source=f"Reddit r/{subreddit}",
                        url=url,
                        source_urls=[url] if url else [],
                        published_at=None,
                        collected_at=utc_now_iso(),
                        summary=summary or title,
                        executive_summary=summary or title,
                        highlights=[f"Subreddit: r/{subreddit}", f"Score: {int(score)}"],
                        suggested_actions=[f"Skim the Reddit thread if the discussion looks technically useful."],
                        learning=["Reddit is a community signal, not a primary source of truth."],
                        tags=["reddit", "community"],
                        week_key=current_week_key(),
                        digest_date=current_digest_date(),
                        raw_source_type="reddit",
                        score=score,
                    )
                )
        return items

    def _fetch_subreddit(self, subreddit: str) -> dict:
        request = Request(
            url=f"https://www.reddit.com/r/{subreddit}/hot.json?limit={self.per_subreddit}",
            headers={"User-Agent": "frontier-intel/1.0"},
        )
        with urlopen(request) as response:
            return json.loads(response.read().decode())

    def _should_skip_title(self, title: str) -> bool:
        lowered = title.lower()
        if any(title.startswith(prefix) for prefix in SKIP_TITLE_PREFIXES):
            return True
        if any(fragment in lowered for fragment in SKIP_TITLE_CONTAINS):
            return True
        return False
