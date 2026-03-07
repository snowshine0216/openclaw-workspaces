from __future__ import annotations

from datetime import UTC, datetime


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def current_digest_date() -> str:
    return datetime.now(UTC).date().isoformat()


def current_week_key() -> str:
    now = datetime.now(UTC)
    year, week, _ = now.isocalendar()
    return f"{year}-W{week:02d}"
