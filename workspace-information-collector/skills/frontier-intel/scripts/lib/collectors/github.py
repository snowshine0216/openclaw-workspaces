from __future__ import annotations

import json
import re
from html import unescape
from urllib.parse import quote
from urllib.request import Request, urlopen

from scripts.lib.collectors.base import Collector
from scripts.lib.models.item import FrontierItem
from scripts.utils.command import load_json_output
from scripts.utils.dates import current_digest_date, current_week_key, utc_now_iso
from scripts.utils.summarizer import Summarizer

GITHUB_SEARCH_API = "https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"
GITHUB_REPO_API = "https://api.github.com/repos/{name}"
GITHUB_TRENDING_URL = "https://github.com/trending?since=daily"
ARTICLE_PATTERN = re.compile(r'<article class="Box-row">(.*?)</article>', re.S)
HREF_PATTERN = re.compile(r'href="/([^"/]+/[^"/]+)"')
DESCRIPTION_PATTERN = re.compile(r'<p class="col-9 color-fg-muted my-1 pr-4">(.*?)</p>', re.S)
LANGUAGE_PATTERN = re.compile(r'<span itemprop="programmingLanguage">(.*?)</span>')
STAR_TODAY_PATTERN = re.compile(r'([\d,]+) stars today')
TOTAL_STARS_PATTERN = re.compile(r'href="/[^"]+/stargazers"[^>]*>.*?</svg>\s*([\d,]+)</a>', re.S)
TAG_PATTERN = re.compile(r"<[^>]+>")


class GitHubCollector(Collector):
    source_type = "github"

    def __init__(self, query: str = "AI OR LLM OR agent OR diffusion", limit: int = 5) -> None:
        self.query = query
        self.limit = limit
        self.summarizer = Summarizer()

    def collect(self) -> list[FrontierItem]:
        payload = self._fetch_trending_payload() or self._fetch_search_payload()
        if not payload:
            return []

        items: list[FrontierItem] = []
        for repo in payload[: self.limit]:
            name = repo.get("nameWithOwner") or repo.get("full_name") or ""
            repo = self._enrich_repo(repo, name)
            description = repo.get("description") or ""
            stars = repo.get("stargazersCount") or repo.get("stargazers_count") or 0
            stars_today = repo.get("starsToday") or 0
            url = repo.get("html_url") or repo.get("url") or self._html_url(name)
            updated_at = repo.get("updatedAt") or repo.get("updated_at")
            language = repo.get("language")
            highlights = []
            if language:
                highlights.append(f"Language: {language}")
            if repo.get("topics"):
                highlights.append("Topics: " + ", ".join(repo.get("topics")[:3]))
            if repo.get("homepage"):
                highlights.append(f"Homepage: {repo.get('homepage')}")
            summary = self.summarizer.summarize_text(item_type="github", title=name, text=description)
            items.append(
                FrontierItem(
                    id=name,
                    type="github",
                    title=name,
                    source="GitHub Trending" if stars_today else "GitHub",
                    url=url,
                    source_urls=[candidate for candidate in [url, repo.get("homepage")] if candidate],
                    published_at=updated_at,
                    collected_at=utc_now_iso(),
                    summary=summary,
                    executive_summary=summary,
                    highlights=highlights,
                    suggested_actions=[],
                    learning=[],
                    tags=["github", "tooling", "trending"],
                    week_key=current_week_key(),
                    digest_date=current_digest_date(),
                    raw_source_type="github_trending" if stars_today else "github",
                    score=float(stars_today or stars),
                )
            )
        return items

    def _fetch_trending_payload(self) -> list[dict]:
        request = Request(GITHUB_TRENDING_URL, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urlopen(request) as response:
                html = response.read().decode()
        except Exception:
            return []
        payload: list[dict] = []
        for article in ARTICLE_PATTERN.findall(html):
            href_match = HREF_PATTERN.search(article)
            if not href_match:
                continue
            name = href_match.group(1)
            description = self._clean(DESCRIPTION_PATTERN.search(article).group(1)) if DESCRIPTION_PATTERN.search(article) else ""
            language = self._clean(LANGUAGE_PATTERN.search(article).group(1)) if LANGUAGE_PATTERN.search(article) else ""
            stars_today = self._int_value(STAR_TODAY_PATTERN.search(article))
            stars = self._int_value(TOTAL_STARS_PATTERN.search(article))
            payload.append(
                {
                    "nameWithOwner": name,
                    "description": description,
                    "html_url": self._html_url(name),
                    "updatedAt": None,
                    "stargazersCount": stars,
                    "starsToday": stars_today,
                    "language": language,
                }
            )
        return payload

    def _fetch_search_payload(self) -> list[dict]:
        try:
            payload = load_json_output(
                [
                    "gh",
                    "search",
                    "repos",
                    self.query,
                    "--limit",
                    str(self.limit),
                    "--json",
                    "nameWithOwner,description,url,updatedAt,stargazersCount",
                ]
            )
            return payload if isinstance(payload, list) else []
        except Exception:
            return self._fetch_public_api()

    def _fetch_public_api(self) -> list[dict]:
        request = Request(
            GITHUB_SEARCH_API.format(query=quote(self.query), limit=self.limit),
            headers={"Accept": "application/vnd.github+json", "User-Agent": "frontier-intel/1.0"},
        )
        with urlopen(request) as response:
            payload = json.loads(response.read().decode())
        return payload.get("items", [])

    def _enrich_repo(self, repo: dict, name: str) -> dict:
        if repo.get("description") and repo.get("language"):
            return repo
        if not name:
            return repo
        try:
            request = Request(
                GITHUB_REPO_API.format(name=name),
                headers={"Accept": "application/vnd.github+json", "User-Agent": "frontier-intel/1.0"},
            )
            with urlopen(request) as response:
                payload = json.loads(response.read().decode())
            merged = dict(repo)
            merged.update(payload)
            return merged
        except Exception:
            return repo

    def _html_url(self, name: str) -> str:
        return f"https://github.com/{name}" if name else ""

    def _int_value(self, match: re.Match[str] | None) -> int:
        if not match:
            return 0
        return int(match.group(1).replace(",", ""))

    def _clean(self, text: str) -> str:
        no_tags = TAG_PATTERN.sub(" ", text)
        return " ".join(unescape(no_tags).split())
