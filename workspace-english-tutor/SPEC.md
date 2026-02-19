# SPEC.md - English Tutor Feature Specification

**User:** Snow (Intermediate level, Chinese native speaker, GMT+8)
**Channel:** Feishu
**Review Frequency:** Daily at 8:00 PM GMT+8 (12:00 PM UTC)
**Items per Review:** 20

---

## Part 1: Teaching Behavior (✅ Implemented in IDENTITY.md)

### For WORDS:
1. **Explain in English** — definition, nuance, context
2. **Explain in Chinese** — 中文解释
3. **Show how/when to use it** — example sentences, common situations
4. **Give synonyms** — similar words with subtle differences
5. **Help you memorize** — memory tricks, associations
6. **Add to vocab.json** — for daily cron reminders

### For SENTENCES/PARAGRAPHS:
1. **Explain in Chinese** — translate and break down meaning
2. **Show how/when to use it** — contexts where this phrasing fits
3. **Give synonyms/alternatives** — other ways to say the same thing
4. **Help you memorize** — key phrases to remember
5. **Add to vocab.json** — for daily cron reminders

### My Behavior:
- Talk naturally like a native English speaker
- Be patient, friendly, and clear
- Make sure I understand before moving forward
- Correct mistakes gently (e.g., "besure" → "be sure")

---

## Part 2: Vocabulary Review System (✅ Implemented)

### Requirements:
1. **Storage:** ✅ `skills/vocab-review/vocab.json`
2. **Delivery:** ✅ Word document (.docx) — script generates it
3. **Rotation:** ✅ Spaced repetition based on review count
4. **Technical:** ✅ Python script + cron job

### File Location:
```
skills/vocab-review/
├── vocab.py        # Main script ✅
├── vocab.json      # Vocabulary storage ✅
├── daily_review.docx  # Generated output
├── .venv/          # Python 3.13 environment ✅
└── README.md       # Documentation ✅
```

### Cron Job: ✅
```
0 12 * * * (runs daily at 12 PM UTC = 8 PM GMT+8)
```

---

## Part 3: Feishu Integration

- **Chat ID:** oc_55bf80b97398600ff6da478ae62937de
- **Account:** default
- **Delivery:** Daily vocabulary review as .docx attachment
- **Status:** ⏳ Pending — script generates .docx, need to wire up Feishu attachment sending

---

## Status

| Component | Status |
|-----------|--------|
| Teaching behavior | ✅ Implemented in IDENTITY.md |
| Vocabulary storage format | ✅ vocab.json |
| Python script | ✅ vocab.py |
| Python environment | ✅ uv + Python 3.13 + python-docx |
| Cron job | ✅ Daily at 8 PM GMT+8 |
| Feishu attachment delivery | ⏳ TODO |

---

## How Alex Adds Vocabulary

When teaching, Alex should add new items to `skills/vocab-review/vocab.json`:

```python
# Alex can use this helper function concept
new_item = {
    "id": <next_id>,
    "type": "word" | "sentence",
    "content": "...",
    "english": "...",  # for words
    "chinese": "...",
    "example": "...",  # for words
    "synonyms": [...],  # for words
    "memory_trick": "...",  # for words
    "context": "...",  # for sentences
    "alternatives": [...],  # for sentences
    "key_phrases": [...],  # for sentences
    "added_date": "YYYY-MM-DD",
    "review_count": 0,
    "last_reviewed": null,
    "status": "learning"
}
```

---

*Last updated: 2026-02-13*
