# Vocabulary Review System

Daily vocabulary review for Snow's English learning.

## Structure

```
skills/vocab-review/
├── vocab.py        # Main script (generates .docx, sends to Feishu)
├── vocab.json      # Vocabulary storage
├── daily_review.docx  # Generated output
├── .venv/          # Python 3.13 virtual environment
└── README.md       # This file
```

## Setup

```bash
cd /root/.openclaw/agents/english-tutor/workspace/skills/vocab-review
source .venv/bin/activate
python3 vocab.py
```

## Configuration

In `vocab.json`:
- `items_per_review`: 20 (items per daily review)
- `timezone`: Asia/Shanghai (GMT+8)
- `review_time`: 20:00 (8 PM)
- `feishu_chat_id`: oc_55bf80b97398600ff6da478ae62937de

## Cron Job

Daily at 8 PM GMT+8 (12 PM UTC):

```bash
0 12 * * * cd /root/.openclaw/agents/english-tutor/workspace/skills/vocab-review && source .venv/bin/activate && python3 vocab.py
```

## Adding Vocabulary

Vocabulary is added by Alex (the tutor) during conversations. Each item has:

**For Words:**
```json
{
  "id": 1,
  "type": "word",
  "content": "serendipity",
  "ipa": "/ˌsɛr.ənˈdɪp.ɪ.ti/",
  "english": "finding something good by accident",
  "chinese": "意外发现美好事物的运气",
  "example": "Meeting her was pure serendipity.",
  "synonyms": ["luck", "fortune", "chance"],
  "memory_trick": "Seren-dip-ity: a DIP into SERENity brings joy",
  "added_date": "2026-02-13",
  "review_count": 0,
  "last_reviewed": null,
  "status": "learning"
}
```

**For Phrases:**
```json
{
  "id": 2,
  "type": "phrase",
  "content": "It's not rocket science.",
  "ipa": "/ɪts nɒt ˈrɒk.ɪt ˈsaɪ.əns/",
  "chinese": "这不是什么难事。",
  "context": "Used when something is not complicated",
  "alternatives": ["It's pretty straightforward", "It's not that hard"],
  "key_phrases": ["rocket science"],
  "added_date": "2026-02-13",
  "review_count": 0,
  "last_reviewed": null,
  "status": "learning"
}
```

## Spaced Repetition

- **learning** → 0-2 reviews
- **reviewing** → 3-6 reviews
- **mastered** → 7+ reviews

Items are prioritized: learning > reviewing > mastered
