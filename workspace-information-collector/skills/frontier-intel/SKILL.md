---
name: frontier-intel
description: Collect, normalize, deduplicate, summarize, and sync frontier AI intelligence across web/news, GitHub, arXiv, Twitter/X, and Reddit. Use when building or running a reusable AI research pipeline, generating daily or weekly AI digests, syncing research outputs to Notion, or refactoring cron-based AI collection into a skill-driven workflow.
---

# Frontier Intel

Use this skill to run the frontier AI intelligence workflow from a reusable skill instead of embedding logic in cron payloads.

## What this skill owns

- Collect frontier AI updates from supported source types
- Normalize all collected items into one canonical schema
- Deduplicate items across source types and runs
- Generate daily and weekly digests
- Sync items and digests to Notion
- Produce concise Feishu-ready summaries

## Operating rules

- Always include source URLs in outputs
- For `arXiv`, always include both the abstract/source URL and the direct PDF URL
- Treat the Notion digest as shareable with other people
- Keep weekly summaries polished and executive-readable
- Keep raw collection state out of `memory/`

## File layout

- Read `README.md` for dependency and setup requirements
- Read `references/setup.md` before environment setup or first run
- Read `references/notion-schema.md` before implementing or changing Notion sync
- Read `references/source-policy.md` before changing source mix or filtering rules
- Read `references/summary-format.md` before changing digest output structure

## Entrypoints

Use these thin runners:
- `scripts/bin/run_daily.py`
- `scripts/bin/run_weekly.py`
- `scripts/bin/sync_notion.py`

## Implementation notes

- Keep reusable logic in `scripts/lib/`
- Keep helper functions in `scripts/utils/`
- Keep tests in `scripts/tests/unit/` and `scripts/tests/integration/`
- Do not flatten the `scripts/` tree

## Current status

This scaffold is phase-one structure only. Implementation comes next.
