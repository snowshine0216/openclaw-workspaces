# Frontier Intel

Reusable skill for collecting frontier AI intelligence, generating daily and weekly digests, and syncing structured outputs to Notion.

## Purpose

This skill replaces brittle cron-prompt logic with a structured pipeline that:
- collects AI frontier information from multiple sources
- normalizes and deduplicates items
- creates daily and weekly summaries
- syncs shareable outputs to Notion
- keeps Feishu as a delivery surface

## Planned sources

- Web/news
- GitHub
- arXiv
- Twitter/X
- Reddit

## Output expectations

Every output should include source URLs.
For `arXiv`, every relevant output should include:
- paper page URL
- direct PDF URL

## Planned script layout

```text
scripts/
├── bin/
├── lib/
│   ├── collectors/
│   ├── models/
│   ├── notion/
│   ├── pipeline/
│   └── storage/
├── tests/
│   ├── integration/
│   └── unit/
└── utils/
```

## Dependencies to set up

These are the intended dependencies. Setup is not finished yet.

### Required

- Python 3
- Notion integration token in `~/.config/notion/api_key`
- Access to a target Notion parent page shared with the integration

### Source/runtime dependencies

- `agent-reach` ecosystem guidance
- `xreach` for Twitter/X
- `gh` for GitHub
- `curl` for web/Jina/Reddit paths
- `mcporter` where applicable

## Recommended checks

- Verify Notion token exists
- Verify `gh` auth status
- Verify Twitter/X access path
- Verify Reddit access path

## Status

This is a scaffold README. Concrete setup commands and validation steps will be filled in during implementation.
