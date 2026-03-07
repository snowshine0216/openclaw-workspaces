from __future__ import annotations

import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


NOTION_VERSION = "2025-09-03"
BASE_URL = "https://api.notion.com/v1"


class NotionClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key.strip()

    @classmethod
    def from_default_config(cls) -> "NotionClient":
        token_path = Path.home() / ".config" / "notion" / "api_key"
        if not token_path.exists():
            raise FileNotFoundError(f"Missing Notion API key: {token_path}")
        return cls(token_path.read_text().strip())

    def search(self, query: str) -> dict:
        return self._request("POST", "/search", {"query": query})

    def create_page(self, payload: dict) -> dict:
        return self._request("POST", "/pages", payload)

    def query_data_source(self, data_source_id: str, payload: dict | None = None) -> dict:
        return self._request("POST", f"/data_sources/{data_source_id}/query", payload or {})

    def create_data_source(self, payload: dict) -> dict:
        return self._request("POST", "/data_sources", payload)

    def append_block_children(self, block_id: str, children: list[dict]) -> dict:
        return self._request("PATCH", f"/blocks/{block_id}/children", {"children": children})

    def _request(self, method: str, path: str, payload: dict | None = None) -> dict:
        body = json.dumps(payload).encode() if payload is not None else None
        request = Request(
            url=f"{BASE_URL}{path}",
            data=body,
            method=method,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
        )
        try:
            with urlopen(request) as response:
                return json.loads(response.read().decode())
        except HTTPError as error:
            details = error.read().decode()
            raise RuntimeError(f"Notion API request failed: {error.code} {details}") from error
