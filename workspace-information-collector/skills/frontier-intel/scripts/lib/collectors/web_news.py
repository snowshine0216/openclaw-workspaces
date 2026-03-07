from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit

from scripts.lib.collectors.base import Collector
from scripts.lib.models.item import FrontierItem
from scripts.utils.command import run_command
from scripts.utils.dates import current_digest_date, current_week_key, utc_now_iso
from scripts.utils.fetcher import fetch_url_text
from scripts.utils.quality import is_bad_summary
from scripts.utils.summarizer import Summarizer

BASE_DIR = Path('/root/openclaw-workspaces/workspace-information-collector')
TAVILY_SCRIPT = BASE_DIR / 'skills' / 'tavily-search' / 'scripts' / 'search.mjs'
NEWS_QUERIES = [
    'frontier AI model release OR new AI model launch OR multimodal model',
    'Anthropic OpenAI Google DeepMind Meta AI latest news last 24 hours',
    'agentic AI enterprise infrastructure data center physical AI robotics last 24 hours',
    'AI policy legal Pentagon regulation supply chain risk AI last 24 hours',
    'AI research breakthrough benchmark reasoning inference last 24 hours',
]
LOW_QUALITY_DOMAINS = {
    'markets.financialcontent.com',
    'aibusinessreview.org',
    'theglobeandmail.com',
    'newsfilecorp.com',
    'bitrue.com',
}
HIGH_SIGNAL_DOMAINS = {
    'fortune.com', 'techcrunch.com', 'cnbc.com', 'axios.com', 'forbes.com',
    'www.microsoft.com', 'openai.com', 'www.theverge.com', 'roboticsandautomationnews.com',
}


class WebNewsCollector(Collector):
    source_type = 'news'

    def __init__(self, limit: int = 7) -> None:
        self.limit = limit
        self.summarizer = Summarizer()

    def collect(self) -> list[FrontierItem]:
        raw_results = self._fetch_results()
        items: list[FrontierItem] = []
        for result in raw_results:
            url = result.get('url', '')
            title = result.get('title', '')
            snippet = (result.get('text') or result.get('summary') or '').strip()
            full_text = self._fetch_full_text(url) or snippet
            summary = self.summarizer.summarize_text(item_type='news', title=title, text=full_text)
            if is_bad_summary(title, summary):
                continue
            score = self._news_score(title=title, url=url, summary=summary)
            items.append(FrontierItem(
                id=url, type='news', title=title,
                source=result.get('author') or result.get('source') or result.get('retrieval_source') or 'Web',
                url=url, source_urls=[url] if url else [],
                published_at=result.get('publishedDate') or result.get('published_at'),
                collected_at=utc_now_iso(), summary=summary, executive_summary=summary or title,
                highlights=[], suggested_actions=[], learning=[], tags=['news', 'web'],
                week_key=current_week_key(), digest_date=current_digest_date(),
                raw_source_type=result.get('retrieval_source', 'mixed_news'), score=score,
            ))
        items.sort(key=lambda current: current.score, reverse=True)
        return items[: self.limit]

    def _fetch_full_text(self, url: str) -> str:
        try:
            return fetch_url_text(url)
        except Exception:
            return ''

    def _fetch_results(self) -> list[dict]:
        merged: list[dict] = []
        seen_urls: set[str] = set()
        seen_titles: set[str] = set()
        for query in NEWS_QUERIES:
            for result in self._run_tavily_query(query) + self._run_exa_query(query):
                url = (result.get('url') or '').strip()
                title = (result.get('title') or '').strip().lower()
                if not url or url in seen_urls or title in seen_titles:
                    continue
                seen_urls.add(url)
                if title:
                    seen_titles.add(title)
                merged.append(result)
        return merged

    def _run_tavily_query(self, query: str) -> list[dict]:
        command = ['node', str(TAVILY_SCRIPT), query, '--topic', 'news', '--days', '1', '-n', '5']
        result = run_command(command, timeout=90)
        if not result.ok:
            return []
        results = self._parse_tavily_output(result.stdout)
        for item in results:
            item['retrieval_source'] = 'tavily'
        return results

    def _run_exa_query(self, query: str) -> list[dict]:
        command = ['mcporter', 'call', f'exa.web_search_exa(query: "{query}", numResults: 5)']
        result = run_command(command, timeout=90)
        if not result.ok:
            return []
        results = self._parse_exa_output(result.stdout)
        for item in results:
            item['retrieval_source'] = 'exa'
        return results

    def _parse_tavily_output(self, text: str) -> list[dict]:
        lines = [line.rstrip() for line in text.splitlines()]
        results: list[dict] = []
        current: dict[str, str] | None = None
        in_sources = False
        for line in lines:
            stripped = line.strip()
            if stripped == '## Sources':
                in_sources = True
                continue
            if not in_sources or not stripped:
                continue
            if stripped.startswith('- **'):
                if current and current.get('title') and current.get('url'):
                    results.append(current)
                current = {'title': stripped[4:].split('**', 1)[0].strip()}
                continue
            if current is None:
                continue
            if stripped.startswith('http://') or stripped.startswith('https://'):
                current['url'] = stripped
            else:
                current['text'] = f"{current.get('text', '')} {stripped}".strip()
        if current and current.get('title') and current.get('url'):
            results.append(current)
        return results

    def _parse_exa_output(self, text: str) -> list[dict]:
        results: list[dict] = []
        current: dict[str, str] | None = None
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('Title: '):
                if current and current.get('title') and current.get('url'):
                    results.append(current)
                current = {'title': stripped.removeprefix('Title: ').strip()}
                continue
            if current is None:
                continue
            if stripped.startswith('URL: '):
                current['url'] = stripped.removeprefix('URL: ').strip()
            elif stripped.startswith('Author: '):
                current['author'] = stripped.removeprefix('Author: ').strip()
            elif stripped.startswith('Published Date: '):
                current['publishedDate'] = stripped.removeprefix('Published Date: ').strip()
            elif stripped.startswith('Text: '):
                current['text'] = stripped.removeprefix('Text: ').strip()
            else:
                current['text'] = f"{current.get('text', '')} {stripped}".strip()
        if current and current.get('title') and current.get('url'):
            results.append(current)
        return results

    def _news_score(self, *, title: str, url: str, summary: str) -> float:
        score = 30.0
        domain = urlsplit(url).netloc.lower()
        title_lower = title.lower()
        summary_lower = summary.lower()
        if domain in HIGH_SIGNAL_DOMAINS:
            score += 20.0
        if domain in LOW_QUALITY_DOMAINS:
            score -= 25.0
        if any(term in title_lower for term in ('anthropic', 'openai', 'google', 'microsoft', 'meta', 'deepmind', 'phi-4', 'dexterity', 'world labs')):
            score += 8.0
        if any(term in summary_lower for term in ('model', 'research', 'policy', 'robot', 'agent', 'deployment', 'reasoning', 'world model')):
            score += 6.0
        return score
