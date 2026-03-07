from __future__ import annotations

from pathlib import Path
from typing import Any

from scripts.lib.models.item import FrontierItem
from scripts.lib.notion.client import NotionClient
from scripts.lib.notion.schema import build_digest_page_properties, build_item_page_properties
from scripts.lib.storage.state_store import JsonStateStore


class NotionSyncState:
    def __init__(self, base_dir: Path) -> None:
        self.store = JsonStateStore(base_dir / "state" / "notion-sync-state.json")

    def read(self) -> dict[str, Any]:
        return self.store.read(default={"items": {}, "digests": {}})

    def write(self, payload: dict[str, Any]) -> None:
        self.store.write(payload)


class NotionSyncService:
    def __init__(self, client: NotionClient, project_dir: Path) -> None:
        self.client = client
        self.state = NotionSyncState(project_dir)

    def sync_items(self, database_id: str, items: list[FrontierItem]) -> list[dict]:
        state = self.state.read()
        synced_items: list[dict] = []
        for item in items:
            if item.id in state["items"]:
                continue
            payload = {
                "parent": {"database_id": database_id},
                "properties": build_item_page_properties(item),
            }
            result = self.client.create_page(payload)
            state["items"][item.id] = result.get("id")
            synced_items.append(result)
        self.state.write(state)
        return synced_items

    def sync_digest(
        self,
        *,
        database_id: str,
        digest_key: str,
        title: str,
        period: str,
        digest_date: str,
        week_key: str,
        executive_summary: str,
        top_highlights: list[str],
        suggested_actions: list[str],
        learning_themes: list[str],
        item_count: int,
    ) -> dict | None:
        state = self.state.read()
        if digest_key in state["digests"]:
            return None
        payload = {
            "parent": {"database_id": database_id},
            "properties": build_digest_page_properties(
                title=title,
                period=period,
                digest_date=digest_date,
                week_key=week_key,
                executive_summary=executive_summary,
                top_highlights=top_highlights,
                suggested_actions=suggested_actions,
                learning_themes=learning_themes,
                item_count=item_count,
            ),
        }
        result = self.client.create_page(payload)
        state["digests"][digest_key] = result.get("id")
        self.state.write(state)
        return result
