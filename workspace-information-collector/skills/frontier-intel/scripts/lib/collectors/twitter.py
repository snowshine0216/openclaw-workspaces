from __future__ import annotations

import re
from datetime import UTC, datetime

from scripts.lib.collectors.base import Collector
from scripts.lib.models.item import FrontierItem
from scripts.utils.command import load_json_output, run_command
from scripts.utils.dates import current_digest_date, current_week_key, utc_now_iso
from scripts.utils.text import clean_summary_text

DEFAULT_HANDLES = [
    "AndrewYNg",
    "drfeifei",
    "karpathy",
    "demishassabis",
    "goodfellow_ian",
    "ylecun",
    "jeremyphoward",
    "rsalakhu",
    "geoffreyhinton",
    "smolix",
    "kaliouby",
    "DaphneKoller",
    "sama",
    "ilyasut",
    "fchollet",
    "lexfridman",
    "YoshuaBengio",
    "AravSrinivas",
]
DEFAULT_QUERY = "OpenAI OR Anthropic OR DeepMind OR GPT-5.4 OR frontier AI"
MAX_TWEETS_TOTAL = 8
AI_SIGNAL_PATTERN = re.compile(
    r"\b(ai|agent|agents|model|models|llm|openai|anthropic|deepmind|gemini|gpt|reasoning|training|inference|robot|robots|benchmark|research|paper|papers|course|jax|multimodal|coding|spatial|diffusion)\b",
    re.IGNORECASE,
)


class TwitterCollector(Collector):
    source_type = "tweet"

    def __init__(self, handles: list[str] | None = None, per_handle: int = 1, search_limit: int = 5) -> None:
        self.handles = handles or DEFAULT_HANDLES
        self.per_handle = per_handle
        self.search_limit = search_limit

    def collect(self) -> list[FrontierItem]:
        items: list[FrontierItem] = []
        for handle in self.handles:
            items.extend(self._collect_handle(handle))
        if items:
            ranked = sorted(items, key=lambda item: item.score, reverse=True)
            return ranked[:MAX_TWEETS_TOTAL]
        return self._collect_search_fallback()

    def _collect_handle(self, handle: str) -> list[FrontierItem]:
        try:
            payload = load_json_output(["xreach", "tweets", f"@{handle}", "-n", str(self.per_handle * 5), "--json"])
        except Exception:
            return []
        tweets = payload.get("items", []) if isinstance(payload, dict) else payload
        tweet_dicts = [tweet for tweet in tweets if isinstance(tweet, dict) and self._is_relevant(tweet)]
        ranked = sorted(tweet_dicts, key=self._fresh_signal_score, reverse=True)
        limited = ranked[: self.per_handle]
        return [self._tweet_to_item(handle, tweet) for tweet in limited]

    def _collect_search_fallback(self) -> list[FrontierItem]:
        result = run_command(["xreach", "search", DEFAULT_QUERY, "-n", str(self.search_limit), "--json"])
        if not result.ok:
            return []
        try:
            payload = load_json_output(["xreach", "search", DEFAULT_QUERY, "-n", str(self.search_limit), "--json"])
        except Exception:
            return []
        tweets = payload.get("items", []) if isinstance(payload, dict) else payload
        tweet_dicts = [tweet for tweet in tweets if isinstance(tweet, dict) and self._is_relevant(tweet)]
        ranked = sorted(tweet_dicts, key=self._fresh_signal_score, reverse=True)
        items: list[FrontierItem] = []
        for tweet in ranked[: self.search_limit]:
            handle = tweet.get("username") or tweet.get("user", {}).get("screenName") or tweet.get("user", {}).get("screen_name") or "unknown"
            items.append(self._tweet_to_item(handle, tweet))
        return items

    def _tweet_to_item(self, handle: str, tweet: dict) -> FrontierItem:
        tweet_id = str(tweet.get("id") or "")
        screen_name = tweet.get("user", {}).get("screenName") or tweet.get("user", {}).get("screen_name") or handle
        url = tweet.get("url") or tweet.get("tweetUrl") or self._tweet_url(screen_name, tweet_id)
        text = (tweet.get("text") or tweet.get("full_text") or "").strip()
        published_at = tweet.get("createdAt") or tweet.get("created_at")
        preview = clean_summary_text(text.replace("\n", " "))
        score = float(self._fresh_signal_score(tweet))
        return FrontierItem(
            id=tweet_id or url,
            type="tweet",
            title=f"@{screen_name}",
            source="X/Twitter",
            url=url,
            source_urls=[url] if url else [],
            published_at=published_at,
            collected_at=utc_now_iso(),
            summary=preview,
            executive_summary=preview,
            highlights=[f"Handle: @{screen_name}", f"Fresh signal: {int(score)}"],
            suggested_actions=[f"Open @{screen_name}'s post if it looks like a meaningful frontier signal."],
            learning=["Use social signals as early alerts, not final truth."],
            tags=["twitter", "signal"],
            week_key=current_week_key(),
            digest_date=current_digest_date(),
            raw_source_type="xreach",
            score=score,
        )

    def _tweet_url(self, handle: str, tweet_id: str) -> str:
        if not handle or not tweet_id:
            return ""
        return f"https://x.com/{handle}/status/{tweet_id}"

    def _fresh_signal_score(self, tweet: dict) -> int:
        engagement = int(tweet.get("likeCount") or 0) + int(tweet.get("retweetCount") or 0) + int(tweet.get("quoteCount") or 0)
        created_at = tweet.get("createdAt") or tweet.get("created_at")
        freshness_bonus = self._freshness_bonus(created_at)
        return engagement + freshness_bonus

    def _freshness_bonus(self, created_at: str | None) -> int:
        if not created_at:
            return 0
        try:
            created = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y").astimezone(UTC)
        except ValueError:
            return 0
        hours_old = max((datetime.now(UTC) - created).total_seconds() / 3600.0, 0.0)
        if hours_old <= 24:
            return 5000
        if hours_old <= 72:
            return 2500
        if hours_old <= 168:
            return 1000
        if hours_old <= 720:
            return 250
        return 0

    def _is_relevant(self, tweet: dict) -> bool:
        text = ((tweet.get("text") or tweet.get("full_text") or "") + " " + (tweet.get("quotedText") or ""))
        return bool(AI_SIGNAL_PATTERN.search(text))
