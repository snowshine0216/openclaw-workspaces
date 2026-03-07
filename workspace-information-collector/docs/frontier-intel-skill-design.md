# Frontier Intel Skill Plan

## Status

This document is the **source of truth** for both design and progress tracking.

### Progress Tracker

- [x] Capture current cron-based AI intel flow
- [x] Decide skill-first refactor direction
- [x] Confirm unified daily digest recommendation
- [x] Confirm Notion parent page + two databases recommendation
- [x] Confirm weekend executive summary direction
- [x] Add explicit Twitter and/or Reddit coverage requirement
- [x] Refine plan around `agent-reach` install guidance
- [x] Require `skill-creator` during skill design
- [x] Require `code-quality-orchestrator` during implementation
- [x] Require organized `scripts/` layout with subfolders
- [x] Scaffold `skills/frontier-intel/`
- [x] Write `SKILL.md`
- [x] Write `README.md`
- [x] Write `references/` docs
- [x] Implement collection pipeline
- [x] Implement normalization + dedup
- [x] Implement digest generation
- [x] Implement Notion sync
- [ ] Add new cron jobs as thin triggers
- [ ] Keep existing cron jobs untouched during rollout
- [ ] Retire old cron jobs only after new flow is proven
- [ ] Run daily dry run
- [ ] Run weekly dry run
- [x] Tighten GitHub collector to use trending momentum
- [x] Document Twitter/X auth setup blocker and fix path
- [x] Clean summary quality for shareable output
- [x] Complete first real Notion setup and write
- [x] Refactor Notion presentation toward one readable daily page per day
- [x] Identify summary quality as the main remaining blocker
- [x] Create shared summary skill under `~/.openclaw/skills/`
- [x] Integrate shared summary skill into frontier-intel
- [ ] Validate output quality end-to-end

## Confirmed Requirements

These are now locked in unless Snow changes them.

- Build this as a **skill**, not as logic embedded in cron payloads.
- Put the skill under `workspace-information-collector/skills/frontier-intel/`.
- Keep dependency/setup instructions in a `README.md` inside the skill.
- Keep the design/progress tracker in `docs/`.
- Use `agent-reach` guidance as the research collection foundation.
- Include **Twitter and/or Reddit** in the source mix.
- Keep the recommendation of **one unified daily digest**.
- Use **one Notion parent page with two databases**.
- Generate a **weekly executive-style summary** on weekends.
- Design the Notion output so it can be **shared with other people** cleanly.
- Include a source URL in every message and digest item.
- For `arXiv`, always include the direct PDF URL as well as the paper/source page.
- Use these skills in the workflow:
  - `skill-creator`
  - `code-quality-orchestrator`
- Organize `skills/frontier-intel/scripts/` into subfolders such as `lib/`, `tests/`, `utils/`, and source-specific modules. Do **not** keep it flat.

## Goal

Refactor the current AI information cron setup into a reusable, well-structured skill that:
- collects frontier AI information from multiple sources
- normalizes and deduplicates collected items across all sources
- generates structured daily and weekly summaries
- syncs item-level entries and digest-level summaries to Notion
- sends concise Feishu delivery separately from the archive layer
- documents dependencies and setup clearly for both humans and agents

## Current State

### Current cron source of truth

- `/root/.openclaw/cron/jobs.json`

### Relevant current jobs

1. `AI Intel Digest for github and arxiv`
2. `Daily AI Intel Morning Digest for tavily search`

### Current behavior

The current setup already does these things:
- runs on cron via the `information-collector` agent
- gathers web/news updates, GitHub repos, and arXiv papers
- deduplicates with local JSON state files
- posts the digest to Feishu

### Current state files

- `memory/last-digest-state.json`
- `memory/last-arxiv-github-state.json`
- `memory/RESEARCH_LOG.md`

### Current weaknesses

The current design works, but it is too brittle.

Weak points:
- too much logic is embedded directly inside cron prompt text
- source handling is split across multiple flows without one canonical schema
- deduplication is local to each flow instead of shared globally
- storage is not structured for downstream sync and rollups
- Notion sync does not exist yet
- weekly summaries are not built from a durable local archive
- the workflow is not packaged as a reusable skill

## Required Skill Governance

## Skill usage requirements

This work must explicitly follow these skills:

### 1. `skill-creator`

Use it to shape the skill package correctly:
- keep `SKILL.md` concise and procedural
- move detailed schemas and setup docs into references and README
- bundle deterministic logic into scripts instead of giant prompt blobs
- keep the skill reusable for future cron jobs and manual runs

### 2. `code-quality-orchestrator`

Use it when implementation starts:
- TDD-first where realistic
- organize code with strong module boundaries
- separate pure logic from side effects
- require tests for changed public behavior
- run review/refactor gates instead of dumping a blob of scripts into the skill

This means the implementation phase should not be “just write some scripts.” It should be structured, reviewed, and testable.

## Architecture Principle

The cron job should become a **thin trigger**.

The real workflow should live inside a dedicated skill under:
- `workspace-information-collector/skills/frontier-intel/`

The skill should own:
- source selection
- collection workflow
- normalization rules
- deduplication rules
- scoring and filtering
- executive summary generation
- Notion sync logic
- daily and weekly digest generation
- setup requirements and dependencies

## `agent-reach` Research Foundation

## Refined interpretation

`agent-reach` is the correct foundation here, but the important detail from its install guide is this:
- **after installation, use upstream tools directly**
- `agent-reach` itself is primarily the installer, config helper, and doctor/watch command

So the skill should be designed around **agent-reach-compatible upstream tools**, not around forcing every collection path through one wrapper CLI.

## What can be used now

Based on the `agent-reach` install guidance, the intended usable tools include:
- `xreach` for Twitter/X
- `gh` for GitHub
- `curl` + Jina Reader for web pages
- `mcporter` for Exa search and certain MCP-backed platforms
- `yt-dlp` for YouTube/Bilibili when needed
- `curl` or Exa-backed alternatives for Reddit
- RSS support where available

For this skill, the immediately relevant source classes are:
- web/news frontier AI coverage
- GitHub AI/ML repos
- arXiv AI papers
- Twitter/X AI leaders and org accounts
- Reddit AI communities or discussions

## Source policy

### Day-one required sources

The first implementation pass should support:
- `news/web`
- `github`
- `arxiv`
- `twitter`
- `reddit`

Twitter and Reddit do not need identical weight.

Recommended weighting:
- `news/web`: primary signal
- `github`: primary builder signal
- `arxiv`: primary research signal
- `twitter`: fast-moving frontier commentary and release signals
- `reddit`: secondary validation / community signal

## Refined source strategy

### News / frontier AI updates

Use agent-reach-compatible web search patterns and/or existing search capability to find:
- new model releases
- frontier labs announcements
- important product launches
- notable benchmark or capability claims
- industry moves that materially affect the AI landscape

### GitHub

Use `gh`-based collection for:
- trending AI/ML repos
- repos with strong recent traction
- tools that appear relevant for experimentation or adoption

### arXiv

Use the existing arXiv workflow, but normalize output into the unified schema.

### Twitter/X

Use `xreach` for:
- frontier AI leaders
- labs and official accounts
- noteworthy tweets or threads that add signal rather than noise

### Reddit

Use Reddit as a secondary signal source for:
- repeated discussion spikes
- practitioner reactions
- interesting technical threads worth surfacing

The skill should avoid low-value Reddit noise.

## Proposed skill layout

The skill must be structured and the `scripts/` directory must **not** be flat.

```text
workspace-information-collector/
├── docs/
│   └── frontier-intel-skill-design.md
└── skills/
    └── frontier-intel/
        ├── SKILL.md
        ├── README.md
        ├── scripts/
        │   ├── bin/
        │   │   ├── run_daily.py
        │   │   ├── run_weekly.py
        │   │   └── sync_notion.py
        │   ├── lib/
        │   │   ├── models/
        │   │   ├── collectors/
        │   │   │   ├── web_news.py
        │   │   │   ├── github.py
        │   │   │   ├── arxiv.py
        │   │   │   ├── twitter.py
        │   │   │   └── reddit.py
        │   │   ├── pipeline/
        │   │   │   ├── normalize.py
        │   │   │   ├── dedupe.py
        │   │   │   ├── scoring.py
        │   │   │   ├── digest_daily.py
        │   │   │   └── digest_weekly.py
        │   │   ├── notion/
        │   │   │   ├── client.py
        │   │   │   ├── schema.py
        │   │   │   └── sync.py
        │   │   └── storage/
        │   │       ├── items_store.py
        │   │       └── state_store.py
        │   ├── utils/
        │   │   ├── dates.py
        │   │   ├── urls.py
        │   │   ├── text.py
        │   │   └── logging.py
        │   └── tests/
        │       ├── unit/
        │       └── integration/
        ├── references/
        │   ├── notion-schema.md
        │   ├── source-policy.md
        │   ├── summary-format.md
        │   └── setup.md
        └── assets/
```

Notes:
- `SKILL.md` stays lean.
- `README.md` is allowed here because the user explicitly asked for dependency/setup documentation.
- `scripts/bin/` holds thin entrypoints.
- `scripts/lib/` holds reusable code.
- `scripts/utils/` holds low-level helpers.
- `scripts/tests/` holds tests.
- source-specific logic belongs in dedicated collector modules, not one giant file.

## Canonical workflow

### Step 1: Collect

Use one skill entrypoint to collect from:
- frontier AI web/news sources
- GitHub AI/ML repos
- arXiv AI papers
- Twitter/X leader and lab signals
- Reddit discussion spikes and technical threads

### Step 2: Normalize

Every raw item must be converted into one canonical schema.

Suggested item schema:

```json
{
  "id": "stable-dedup-key",
  "type": "news|github|arxiv|tweet|reddit",
  "title": "...",
  "source": "...",
  "url": "primary source URL",
  "source_urls": ["https://..."],
  "pdf_url": "https://arxiv.org/pdf/...",
  "published_at": "ISO-8601",
  "collected_at": "ISO-8601",
  "summary": "short factual summary",
  "executive_summary": "why this matters",
  "highlights": ["...", "..."],
  "suggested_actions": ["...", "..."],
  "learning": ["...", "..."],
  "tags": ["agents", "multimodal"],
  "week_key": "2026-W10",
  "digest_date": "2026-03-07",
  "raw_source_type": "web|github|arxiv|xreach|reddit"
}
```

### Step 3: Deduplicate

Dedup must be unified across all source types.

Recommended state storage:
- `projects/frontier-intel/state/dedup-index.json`
- `projects/frontier-intel/state/last-run.json`
- `projects/frontier-intel/state/source-cursors.json`

Recommended dedup keys:
- news/web: canonical URL hash
- arXiv: arXiv ID
- GitHub: `owner/repo`
- Twitter/X: tweet URL or tweet ID
- Reddit: post permalink or Reddit post ID

### Step 4: Store locally

Do not keep pipeline state in `memory/`.

Recommended structure:

```text
projects/frontier-intel/
├── items/
│   └── YYYY-MM-DD.json
├── digests/
│   ├── daily/
│   │   └── YYYY-MM-DD.md
│   └── weekly/
│       └── YYYY-Www.md
└── state/
    ├── dedup-index.json
    ├── notion-sync-state.json
    ├── source-cursors.json
    └── config.json
```

### Step 5: Sync to Notion

Every daily run should sync:
- item-level entries
- digest-level summary

Every weekend run should sync:
- weekly executive summary
- optionally updated weekly item links or rollup references

### Step 6: Deliver to Feishu

Feishu should receive the concise digest.

Notion should receive the structured knowledge archive.

That separation is deliberate:
- Feishu = alert surface
- Notion = searchable long-term system

## Notion design

## Confirmed recommendation

Use **one parent page with two databases**.

## Concrete Notion information architecture

## Sharing and collaboration requirement

This Notion system is not just a private scratchpad.
It should be readable and shareable with other people.

That means the structure should optimize for:
- clean executive summaries that can be skimmed quickly
- low dependence on private shorthand or internal context
- clear source links so readers can verify claims
- consistent weekly navigation
- pages that make sense when opened out of context

Design implication:
- the digest database and weekly digest pages should be the main shareable surfaces
- the raw items database can remain more operational, but still readable
- avoid exposing messy internal state, debug notes, or implementation details in shareable Notion content

### Parent page: `Frontier AI Intel`

This should be the human-facing dashboard.

Recommended sections on the parent page:
- current week quick links
- latest daily digest view
- latest weekly digest view
- filtered views into `AI Research Items`
- setup notes or operating notes for the integration

Recommended parent page layout:
1. Header / purpose block
2. Linked view: `This Week's Weekly Digest`
3. Linked view: `Latest Daily Digests`
4. Linked view: `This Week's Top Items`
5. Linked view: `Top arXiv This Week`
6. Linked view: `Top GitHub This Week`
7. Linked view: `Top Twitter/Reddit Signals This Week`

### Database 1: `AI Research Items`

This is the source-of-truth item database.
Each row is one collected item.

Suggested properties:
- `Title` — title
- `Type` — select: `News`, `GitHub`, `arXiv`, `Tweet`, `Reddit`
- `Source` — rich text or select
- `Published At` — date
- `Collected At` — date
- `URL` — url
- `PDF URL` — url
- `Executive Summary` — rich text
- `Highlights` — rich text
- `Suggested Actions` — rich text
- `Learning` — rich text
- `Digest Date` — date
- `Week` — rich text such as `2026-W10`
- `Dedup Key` — rich text
- `Tags` — multi-select
- `Score` — number
- `Included In Daily Digest` — checkbox
- `Included In Weekly Digest` — checkbox

Recommended views:
- `This Week`
- `Today`
- `arXiv This Week`
- `GitHub This Week`
- `Twitter + Reddit`
- `High Signal`

### Database 2: `AI Research Digests`

This is the digest-level summary database.
Each row is one daily or weekly digest.

Suggested properties:
- `Title` — title
- `Period` — select: `Daily`, `Weekly`
- `Digest Date` — date
- `Week` — rich text
- `Executive Summary` — rich text
- `Top Highlights` — rich text
- `Suggested Actions` — rich text
- `Learning Themes` — rich text
- `Item Count` — number
- `Status` — select: `Draft`, `Published`
- `Primary Link` — url or rich text

Recommended views:
- `Latest Daily`
- `Latest Weekly`
- `This Week`
- `Archive`

## Week organization model

Use **week as an organizing dimension**, not as the only storage unit.

That means:
- each item row belongs to a week via the `Week` property
- each digest row belongs to a week via the `Week` property
- weekly navigation happens through filtered views and weekly digest entries
- the database remains searchable across all time

This is better than one giant page per week because it preserves:
- searchability
- deduplication
- cross-week comparisons
- source-specific filtering
- easier future automation

## Page templates inside the digest database

Digest rows can have page bodies for richer reading.
That gives the best of both worlds:
- structured database fields
- readable long-form page content

### Daily digest page template

Recommended sections in the page body:
- `Executive Summary`
- `Top Highlights`
- `Suggested Actions`
- `What I Learned`
- `Top News`
- `Top GitHub Repos`
- `Top arXiv Papers`
- `Top Twitter/Reddit Signals`

### Weekly digest page template

Recommended sections in the page body:
- `Week in One Paragraph`
- `Biggest Themes`
- `What Changed This Week`
- `Top Repos Worth Trying`
- `Top Papers Worth Reading`
- `Top Social Signals Worth Attention`
- `Suggested Actions for Next Week`
- `Key Learnings`

## Recommended default navigation

If Snow or a shared viewer opens the parent page, the ideal flow should be:
1. see this week's executive summary first
2. scan the latest daily digest if needed
3. drill into filtered item views by type
4. open the weekly digest page for a narrative summary

## Shareability design rules

Every digest intended for sharing should follow these rules:
- start with the executive summary, not raw links
- use plain English and avoid unexplained jargon where possible
- keep each highlight self-contained
- attach source links to every major claim or item
- include at least one explicit source URL for every item mentioned
- for `arXiv`, include both the abstract/source page URL and the direct PDF URL
- keep suggested actions practical and audience-readable
- separate opinion from fact clearly

Recommended shareable output style:
- weekly digest = polished and presentation-friendly
- daily digest = concise but still readable by someone outside the workflow
- item entries = factual, source-linked, and easy to scan

## Minimum viable Notion schema

Start with the smallest schema that still supports automation cleanly.
Additional fields can be added later, but these should be the initial required set.

### `AI Research Items` — minimum viable fields

- `Title` — `title`
- `Type` — `select`
- `Source` — `rich_text`
- `Published At` — `date`
- `URL` — `url`
- `PDF URL` — `url`
- `Executive Summary` — `rich_text`
- `Highlights` — `rich_text`
- `Suggested Actions` — `rich_text`
- `Learning` — `rich_text`
- `Digest Date` — `date`
- `Week` — `rich_text`
- `Dedup Key` — `rich_text`

### `AI Research Digests` — minimum viable fields

- `Title` — `title`
- `Period` — `select`
- `Digest Date` — `date`
- `Week` — `rich_text`
- `Executive Summary` — `rich_text`
- `Top Highlights` — `rich_text`
- `Suggested Actions` — `rich_text`
- `Learning Themes` — `rich_text`
- `Item Count` — `number`

## Recommended extended Notion schema

Use this when creating the initial databases if we want the structure to be future-proof from day one.

### `AI Research Items` — extended fields and types

- `Title` — `title`
- `Type` — `select`
  - options: `News`, `GitHub`, `arXiv`, `Tweet`, `Reddit`
- `Source` — `rich_text`
- `Published At` — `date`
- `Collected At` — `date`
- `URL` — `url`
- `PDF URL` — `url`
- `Executive Summary` — `rich_text`
- `Highlights` — `rich_text`
- `Suggested Actions` — `rich_text`
- `Learning` — `rich_text`
- `Digest Date` — `date`
- `Week` — `rich_text`
- `Dedup Key` — `rich_text`
- `Tags` — `multi_select`
- `Score` — `number`
- `Included In Daily Digest` — `checkbox`
- `Included In Weekly Digest` — `checkbox`

### `AI Research Digests` — extended fields and types

- `Title` — `title`
- `Period` — `select`
  - options: `Daily`, `Weekly`
- `Digest Date` — `date`
- `Week` — `rich_text`
- `Executive Summary` — `rich_text`
- `Top Highlights` — `rich_text`
- `Suggested Actions` — `rich_text`
- `Learning Themes` — `rich_text`
- `Item Count` — `number`
- `Status` — `select`
  - options: `Draft`, `Published`
- `Primary Link` — `url`

## Schema design advice

A few strong opinions here:
- keep `Week` as `rich_text` initially; it is simple and durable
- keep `Highlights`, `Suggested Actions`, and `Learning` as newline-formatted `rich_text` first; no need to over-model them yet
- avoid complex Notion relations in phase one unless they prove necessary
- do not over-optimize for fancy Notion rollups before the pipeline works reliably

## Summary content requirements

Every Notion sync must include:
- executive summary
- highlights
- suggested actions to take
- learnings

This is mandatory at both levels:
- per item
- per digest

### Daily digest structure

For each daily digest:
- executive summary
- top highlights
- suggested actions
- learnings / why it matters
- linked source items

### Weekly digest structure

Weekend summary should be built from stored weekly items, not from fresh search.

Recommended weekly sections:
- executive summary of the week
- biggest model/news/research themes
- top GitHub repos worth trying
- top papers worth reading
- top Twitter/X signals worth paying attention to
- strongest Reddit threads worth a skim
- repeated signals across multiple sources
- suggested actions for next week
- learnings and trend interpretation

## Cron refactor

## Current state

Today the crons contain too much intelligence directly in the payload.

## Target state

Crons should only invoke the skill workflow.

Recommended cron split:

1. `collect-frontier-ai-daily`
- runs every morning
- collects all source types
- writes normalized items locally
- builds daily digest
- syncs to Notion
- sends short Feishu summary

2. `collect-frontier-ai-evening`
- optional second pass for late-breaking updates
- incremental lower-noise sync

3. `summarize-frontier-ai-weekly`
- runs on weekend
- reads the week’s stored items
- creates weekly executive summary
- syncs to Notion
- sends brief Feishu summary

## Responsibility split

### Cron should do
- schedule
- trigger the agent turn
- pass a mode such as `daily`, `evening`, or `weekly`

### Skill should do
- choose sources
- collect
- normalize
- deduplicate
- score/filter
- summarize
- sync to Notion
- generate Feishu-ready output

## Dependencies and setup required

These must be documented in `skills/frontier-intel/README.md`.

## Required setup

### 1. Notion integration

Still required.

Need:
- a Notion integration token stored locally
- the target Notion parent page shared with the integration
- IDs for the parent page and created databases

Current status:
- `~/.config/notion/api_key` is currently missing

### 2. `agent-reach` foundation

Important clarified rule from install docs:
- install `agent-reach`
- use **upstream tools directly** afterward
- use `agent-reach doctor` / `watch` for health and maintenance

This means the skill should declare support and checks for:
- `xreach`
- `gh`
- `curl`
- `mcporter` when available
- any additional source-specific tools required for enabled channels

### 3. Twitter/X access

To unlock strong Twitter collection, user cookies may be needed.

Expected setup path from `agent-reach` docs:
- configure Twitter cookies when needed
- ensure proxy handling works if network environment requires it

### 4. Reddit access

Reddit may be partially blocked or noisy depending on environment.

The skill should support:
- direct Reddit JSON collection where available
- fallback search/collection strategy where needed

### 5. GitHub CLI auth

Need to verify `gh` auth status for reliable GitHub collection.

### 6. Python runtime

Recommended for deterministic scripts and tests.

Need:
- Python 3
- test runner choice documented in README
- dependency installation instructions documented in README

### 7. Local storage path

Need to create and standardize:
- `projects/frontier-intel/`

## Documentation requirements

User instruction wins here.

Recommended split:
- `skills/frontier-intel/SKILL.md` — concise execution instructions for the agent
- `skills/frontier-intel/README.md` — human-readable setup and dependency guide
- `skills/frontier-intel/references/*.md` — detailed schemas, source policy, and formatting rules
- `docs/frontier-intel-skill-design.md` — design + progress tracker

## Implementation phases

### Phase 1 — Planning and design
- finalize plan doc
- lock source mix and architecture
- lock directory layout

### Phase 2 — Skill scaffold
- create `skills/frontier-intel/`
- add `SKILL.md`
- add `README.md`
- add `references/` docs
- create organized script tree

### Phase 3 — Core pipeline
- implement collectors
- implement normalization
- implement deduplication
- implement local storage

### Phase 4 — Digest + sync
- implement daily digest generation
- implement weekly digest generation
- implement Notion sync
- implement Feishu-ready output generation

### Phase 5 — Cron rollout
- add new thin skill-triggering cron jobs
- do not modify or delete existing cron jobs during initial rollout
- run the new flow in parallel until output quality is proven
- retire or disable old cron jobs only after the new flow is validated

### Phase 6 — Validation
- dry run daily flow
- dry run weekly flow
- verify Notion sync
- verify Feishu output quality
- review code quality gates

## Locked decisions

These decisions are now the default plan:
- one parent Notion page with two databases
- one unified daily digest
- include Twitter and Reddit in the source design
- weekly summary on Sunday morning GMT+8
- executive style first, with links to detailed items
- skill-first implementation in `workspace-information-collector/skills/frontier-intel/`
- organized `scripts/` layout, never flat

## Immediate next step

Only after this doc is accepted:
- scaffold `skills/frontier-intel/`
- add `SKILL.md`
- add `README.md`
- add `references/`
- create the organized `scripts/` tree

That’s the right order. Anything else first would be premature and messy.
