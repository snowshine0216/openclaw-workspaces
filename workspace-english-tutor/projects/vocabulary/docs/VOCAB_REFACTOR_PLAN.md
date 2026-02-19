# Vocabulary System Refactor Plan

**Date**: 2026-02-20
**Status**: Proposed  
**Goal**: Migrate from monolithic JSON to SQLite for scalability, safety, and simplicity

---

## Current Issues

1. **Bloat**: 370 items in a single JSON file (225 KB, 5,983 lines), growing daily
2. **Full-file rewrite on every change**: Adding 1 word or bumping 1 review count rewrites the entire file
3. **No concurrent access safety**: If cron job and agent write simultaneously, one clobbers the other
4. **No query capability**: Must load all items into memory just to select 20 for review
5. **No archival strategy**: "Mastered" items (7+ reviews) stay in active pool forever
6. **Mixed concerns**: Data and logic live together in `skills/`

---

## Decision: SQLite over JSON

### Why not keep splitting JSON files?

The original plan proposed splitting into `active.json` + `archive/mastered.json` + monthly snapshots. This adds **more complexity** (multiple files, merge logic, snapshot management) while still suffering from full-file rewrites and no concurrent access safety.

### Why SQLite?

| Concern | SQLite Answer |
| :--- | :--- |
| **Single file, no server** | ✅ Just a `.db` file, like the current `.json` |
| **Concurrent access** | ✅ WAL mode handles agent + cron race conditions |
| **Querying** | ✅ SQL replaces in-memory sorting/filtering |
| **Partial updates** | ✅ Single-row UPDATE, no full-file rewrite |
| **Archival** | ✅ `WHERE archived_date IS NULL` — no file juggling |
| **Dependencies** | ✅ `sqlite3` is in Python's standard library |
| **Backup** | ✅ `.backup()` API creates consistent snapshots |
| **Size** | ✅ 370 items ≈ 50-100 KB in SQLite |

### What about Git diffs?

Not needed. Git diffs on a vocabulary list weren't providing real value — you don't code-review word additions. What you actually need is:
- **History**: `SELECT * FROM vocab WHERE added_date = '2026-02-15'` (built-in)
- **Rollback**: Daily `.db.bak` snapshot (file copy to restore)
- **Offsite backup**: Git-track the `.db.bak` file

---

## Proposed Structure

### Directory Layout

```
workspace-english-tutor/
├── projects/
│   └── vocabulary/
│       ├── data/
│       │   ├── vocab.db              ← Primary storage (SQLite)
│       │   └── vocab.db.bak          ← Daily backup snapshot (git-tracked)
│       ├── output/
│       │   └── daily_review.docx     ← Generated reviews
│       └── docs/
│           └── VOCAB_REFACTOR_PLAN.md
│
├── skills/
│   └── vocab-review/
│       ├── SKILL.md                  ← Skill documentation
│       ├── vocab_manager.py          ← Core logic (add/archive/select/migrate)
│       ├── generate_review.py        ← Review generator
│       ├── requirements.txt          ← Dependencies (python-docx only)
│       └── .venv/                    ← Virtual environment
│
├── AGENTS.md
└── ...
```

---

## Database Schema

```sql
CREATE TABLE vocab (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL DEFAULT 'word',           -- 'word', 'phrase', 'sentence'
    content TEXT NOT NULL,
    ipa TEXT DEFAULT '',
    english TEXT DEFAULT '',
    chinese TEXT DEFAULT '',
    original_context TEXT DEFAULT '',
    example TEXT DEFAULT '',
    synonyms TEXT DEFAULT '[]',                  -- JSON array stored as text
    fun_fact TEXT DEFAULT '',
    memory_trick TEXT DEFAULT '',
    added_date TEXT NOT NULL,
    review_count INTEGER DEFAULT 0,
    last_reviewed TEXT,
    status TEXT DEFAULT 'learning',              -- 'learning', 'reviewing', 'mastered'
    archived_date TEXT                           -- NULL = active, set when graduated
);

CREATE INDEX idx_status ON vocab(status);
CREATE INDEX idx_review_count ON vocab(review_count);
CREATE INDEX idx_last_reviewed ON vocab(last_reviewed);
CREATE INDEX idx_added_date ON vocab(added_date);
```

---

## Key Principles

### Skills = Reusable Tools
- **Pure logic**, no user data
- Can be shared/published
- Example: `vocab_manager.py` with functions like `add_word()`, `archive_mastered()`, `select_for_review()`

### Projects = User Data + Workflows
- **Your specific vocabulary database**
- Personal learning progress
- Generated outputs
- Not meant to be shared

---

## Data Management Strategy

### 1. Tiered Review System
- **Learning** (0-2 reviews): Daily pool
- **Reviewing** (3-6 reviews): Every 3 days
- **Mastered** (7+ reviews): Every 7 days, then archive

### 2. Archive Mastered Words
Set `archived_date` on items with `status = 'mastered'` that haven't been reviewed in 30+ days. They stay in the same DB but are excluded from active queries via `WHERE archived_date IS NULL`.

### 3. Smart Selection Algorithm
Single SQL query replaces the in-memory sorting logic:

```sql
SELECT * FROM vocab
WHERE archived_date IS NULL
ORDER BY
    CASE status
        WHEN 'learning' THEN 0
        WHEN 'reviewing' THEN 1
        WHEN 'mastered' THEN 2
    END,
    review_count ASC,
    COALESCE(last_reviewed, '') ASC
LIMIT 20;
```

---

## Backup Strategy: SQLite .backup + Git

### Why `.backup()` instead of committing `.db` directly?
Committing the live `.db` while the agent might be writing could catch it mid-transaction. The `.backup` command creates a **consistent snapshot** first.

```json
{
  "name": "vocab-backup",
  "schedule": { "kind": "cron", "expr": "0 2 * * *", "tz": "UTC" },
  "payload": {
    "kind": "systemEvent",
    "text": "cd /root/.openclaw/workspace-english-tutor && sqlite3 projects/vocabulary/data/vocab.db '.backup projects/vocabulary/data/vocab.db.bak' && git add projects/vocabulary/data/vocab.db.bak && git commit -m 'Daily vocab backup' && git push"
  },
  "sessionTarget": "main"
}
```

---

## Implementation Plan

### Phase 1: Create New Structure (5 min)

```bash
# Create project structure
mkdir -p projects/vocabulary/{data,output,docs}
```

### Phase 2: Migration Script + Core Logic (20 min)

**skills/vocab-review/vocab_manager.py** (new):

```python
"""
Vocabulary Management Library (SQLite)
Handles: add, archive, select, status updates, migration
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from contextlib import contextmanager


# --- Database Connection ---

@contextmanager
def get_connection(db_path):
    """Context manager for SQLite connections with WAL mode."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# --- Schema ---

def init_db(db_path):
    """Create tables and indexes if they don't exist."""
    with get_connection(db_path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS vocab (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL DEFAULT 'word',
                content TEXT NOT NULL,
                ipa TEXT DEFAULT '',
                english TEXT DEFAULT '',
                chinese TEXT DEFAULT '',
                original_context TEXT DEFAULT '',
                example TEXT DEFAULT '',
                synonyms TEXT DEFAULT '[]',
                fun_fact TEXT DEFAULT '',
                memory_trick TEXT DEFAULT '',
                added_date TEXT NOT NULL,
                review_count INTEGER DEFAULT 0,
                last_reviewed TEXT,
                status TEXT DEFAULT 'learning',
                archived_date TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_status ON vocab(status);
            CREATE INDEX IF NOT EXISTS idx_review_count ON vocab(review_count);
            CREATE INDEX IF NOT EXISTS idx_last_reviewed ON vocab(last_reviewed);
            CREATE INDEX IF NOT EXISTS idx_added_date ON vocab(added_date);
        """)


# --- Core Operations ---

def add_word(db_path, word_data):
    """Add a new word to the database. Returns the new ID."""
    with get_connection(db_path) as conn:
        cursor = conn.execute("""
            INSERT INTO vocab (type, content, ipa, english, chinese,
                               original_context, example, synonyms,
                               fun_fact, memory_trick, added_date,
                               review_count, last_reviewed, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL, 'learning')
        """, (
            word_data.get('type', 'word'),
            word_data['content'],
            word_data.get('ipa', ''),
            word_data.get('english', ''),
            word_data.get('chinese', ''),
            word_data.get('original_context', ''),
            word_data.get('example', ''),
            json.dumps(word_data.get('synonyms', []), ensure_ascii=False),
            word_data.get('fun_fact', ''),
            word_data.get('memory_trick', ''),
            word_data.get('added_date', datetime.now().strftime('%Y-%m-%d')),
        ))
        return cursor.lastrowid


def select_for_review(db_path, max_items=20):
    """Select items for review using spaced repetition. Returns list of dicts."""
    with get_connection(db_path) as conn:
        rows = conn.execute("""
            SELECT * FROM vocab
            WHERE archived_date IS NULL
            ORDER BY
                CASE status
                    WHEN 'learning' THEN 0
                    WHEN 'reviewing' THEN 1
                    WHEN 'mastered' THEN 2
                END,
                review_count ASC,
                COALESCE(last_reviewed, '') ASC
            LIMIT ?
        """, (max_items,)).fetchall()
        return [dict(row) for row in rows]


def update_review_status(db_path, reviewed_ids):
    """Update review count and status for reviewed items."""
    today = datetime.now().strftime('%Y-%m-%d')
    with get_connection(db_path) as conn:
        for item_id in reviewed_ids:
            conn.execute("""
                UPDATE vocab
                SET review_count = review_count + 1,
                    last_reviewed = ?,
                    status = CASE
                        WHEN review_count + 1 >= 7 THEN 'mastered'
                        WHEN review_count + 1 >= 3 THEN 'reviewing'
                        ELSE 'learning'
                    END
                WHERE id = ?
            """, (today, item_id))


def archive_mastered(db_path, days_threshold=30):
    """Archive mastered words older than threshold. Returns count archived."""
    cutoff = (datetime.now() - timedelta(days=days_threshold)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    with get_connection(db_path) as conn:
        cursor = conn.execute("""
            UPDATE vocab
            SET archived_date = ?
            WHERE status = 'mastered'
              AND archived_date IS NULL
              AND last_reviewed < ?
        """, (today, cutoff))
        return cursor.rowcount


def get_active_count(db_path):
    """Get count of active (non-archived) items."""
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM vocab WHERE archived_date IS NULL"
        ).fetchone()
        return row[0]


def get_total_count(db_path):
    """Get total item count (including archived)."""
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT COUNT(*) FROM vocab").fetchone()
        return row[0]


# --- Migration ---

def migrate_from_json(json_path, db_path):
    """One-time migration from vocab.json to vocab.db."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    init_db(db_path)

    with get_connection(db_path) as conn:
        for item in data.get('items', []):
            conn.execute("""
                INSERT INTO vocab (id, type, content, ipa, english, chinese,
                                   original_context, example, synonyms,
                                   fun_fact, memory_trick, added_date,
                                   review_count, last_reviewed, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.get('id'),
                item.get('type', 'word'),
                item.get('content', ''),
                item.get('ipa', ''),
                item.get('english', ''),
                item.get('chinese', ''),
                item.get('original_context', ''),
                item.get('example', ''),
                json.dumps(item.get('synonyms', []), ensure_ascii=False),
                item.get('fun_fact', ''),
                item.get('memory_trick', ''),
                item.get('added_date', ''),
                item.get('review_count', 0),
                item.get('last_reviewed'),
                item.get('status', 'learning'),
            ))

    return len(data.get('items', []))
```

**skills/vocab-review/generate_review.py** (refactored):

```python
#!/usr/bin/env python3
"""
Generate daily vocabulary review .docx
Usage: python generate_review.py [--db-path PATH]
"""
import argparse
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import datetime

from vocab_manager import select_for_review, update_review_status, get_active_count


def generate_docx(items):
    """Generate a .docx file with vocabulary review content."""
    doc = Document()

    # Title
    title = doc.add_heading('📚 Daily Vocabulary Review', level=0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Date
    date_para = doc.add_paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    date_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    doc.add_paragraph()  # Spacer

    if not items:
        doc.add_paragraph("No vocabulary items to review today. Great job! 🎉")
        return doc

    for i, item in enumerate(items, 1):
        content = item.get('content', '')

        # Section header
        doc.add_heading(f"{i}. {content}", level=1)

        # IPA pronunciation
        ipa = item.get('ipa', '')
        if ipa:
            p = doc.add_paragraph()
            p.add_run('IPA: ').bold = True
            p.add_run(ipa)

        # English definition
        english = item.get('english', '')
        if english:
            p = doc.add_paragraph()
            p.add_run('English: ').bold = True
            p.add_run(english)

        # Chinese definition
        chinese = item.get('chinese', '')
        if chinese:
            p = doc.add_paragraph()
            p.add_run('中文: ').bold = True
            p.add_run(chinese)

        # Example
        example = item.get('example', '')
        if example:
            p = doc.add_paragraph()
            p.add_run('Example: ').bold = True
            p.add_run(example).italic = True

        # Synonyms
        synonyms = item.get('synonyms', '[]')
        if isinstance(synonyms, str):
            import json
            synonyms = json.loads(synonyms)
        if synonyms:
            p = doc.add_paragraph()
            p.add_run('Synonyms: ').bold = True
            p.add_run(', '.join(synonyms))

        # Original context
        original_context = item.get('original_context', '')
        if original_context:
            p = doc.add_paragraph()
            p.add_run('📝 Original Context: ').bold = True
            p.add_run(original_context).italic = True

        # Fun fact
        fun_fact = item.get('fun_fact', '')
        if fun_fact:
            p = doc.add_paragraph()
            p.add_run('🎯 Fun Fact: ').bold = True
            p.add_run(fun_fact)

        # Memory trick
        memory_trick = item.get('memory_trick', '')
        if memory_trick:
            p = doc.add_paragraph()
            p.add_run('💡 Memory Trick: ').bold = True
            p.add_run(memory_trick)

        # Review status
        review_count = item.get('review_count', 0)
        status = item.get('status', 'learning')
        p = doc.add_paragraph()
        p.add_run(f"Review #: {review_count} | Status: {status}").italic = True

        doc.add_paragraph()  # Spacer

    return doc


def main():
    parser = argparse.ArgumentParser(description='Generate daily vocabulary review')
    parser.add_argument('--db-path', type=str,
                       default='../../projects/vocabulary/data/vocab.db',
                       help='Path to vocabulary database')
    parser.add_argument('--output-dir', type=str,
                       default='../../projects/vocabulary/output',
                       help='Path to output directory')
    args = parser.parse_args()

    # Resolve paths relative to script location
    script_dir = Path(__file__).parent
    db_path = (script_dir / args.db_path).resolve()
    output_dir = (script_dir / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 50)
    print("📚 Vocabulary Review Generator")
    print("=" * 50)

    # Select items for review
    items = select_for_review(str(db_path), max_items=20)
    print(f"[INFO] Selected {len(items)} items for review")
    print(f"[INFO] Active vocabulary: {get_active_count(str(db_path))}")

    # Generate .docx
    doc = generate_docx(items)
    output_file = output_dir / "daily_review.docx"
    doc.save(str(output_file))
    print(f"[INFO] Generated: {output_file}")

    # Update review status
    reviewed_ids = [item['id'] for item in items]
    update_review_status(str(db_path), reviewed_ids)
    print(f"[INFO] Updated review status for {len(items)} items")

    print("=" * 50)
    print("✅ Daily review document generated!")
    print("=" * 50)


if __name__ == '__main__':
    main()
```

### Phase 3: One-Time Migration (2 min)

```bash
cd skills/vocab-review
source .venv/bin/activate
python -c "
from vocab_manager import migrate_from_json, init_db
count = migrate_from_json(
    'vocab.json',
    '../../projects/vocabulary/data/vocab.db'
)
print(f'Migrated {count} items to SQLite')
"
```

Verify:
```bash
sqlite3 ../../projects/vocabulary/data/vocab.db "SELECT COUNT(*), status FROM vocab GROUP BY status"
```

### Phase 4: Update AGENTS.md (5 min)

Replace the "Vocabulary Management" section with:

```markdown
## 📖 Vocabulary Management

### ⚠️ SINGLE SOURCE OF TRUTH

**All vocabulary lives in:** `projects/vocabulary/data/vocab.db` (SQLite)

### Adding Words

```python
from vocab_manager import add_word

add_word('projects/vocabulary/data/vocab.db', {
    'type': 'word',
    'content': 'example',
    'ipa': '/ɪɡˈzæm.pəl/',
    'english': 'A thing characteristic of its kind',
    'chinese': '例子；榜样',
    'example': 'This is an example sentence.',
    'synonyms': ['sample', 'instance'],
    'memory_trick': '',
})
```

### Review System
- **Script:** `skills/vocab-review/generate_review.py`
- **Database:** `projects/vocabulary/data/vocab.db`
- **Output:** `projects/vocabulary/output/daily_review.docx`
- **Cron:** Morning 7AM + Evening 7PM (GMT+8)
- **Selection:** Spaced repetition via SQL query

### Status Progression
- `learning`: 0-2 reviews
- `reviewing`: 3-6 reviews
- `mastered`: 7+ reviews → auto-archived after 30 days inactive

### Backup
- **Daily:** SQLite `.backup` → `vocab.db.bak` → git push
- **Restore:** Copy `vocab.db.bak` → `vocab.db`


### Phase 5: Update Cron Jobs (3 min)

> **Note:** Minutes are randomized (not `:00`) to avoid thundering herd at exact hour marks.

**Morning Review (7 AM GMT+8)**:
```json
{
  "agentId": "english-tutor",
  "name": "Vocab Morning Review",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "44 6 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Generate vocabulary review: cd skills/vocab-review && source .venv/bin/activate && python generate_review.py. Send the output from the script - nothing else.",
    "model": "zai/glm-5"
  },
  "delivery": {
    "channel": "feishu",
    "mode": "announce",
    "to": "chat:oc_55bf80b97398600ff6da478ae62937de"
  }
}
```

**Daily Backup (2:43 AM GMT+8)**:
```json
{
  "agentId": "english-tutor",
  "name": "Vocab Daily Backup",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "* 2 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run the backup: sqlite3 /root/.openclaw/workspace-english-tutor/projects/vocabulary/data/vocab.db '.backup /root/.openclaw/workspace-english-tutor/projects/vocabulary/data/vocab.db.bak' && cd /root/.openclaw/workspace-english-tutor && git add projects/vocabulary/data/vocab.db.bak && git commit -m 'Daily vocab backup' && git push. Just send the output - nothing else.",
    "model": "zai/glm-5"
  },
  "delivery": {
    "channel": "feishu",
    "mode": "announce",
    "to": "chat:oc_55bf80b97398600ff6da478ae62937de"
  }
}
```

**Monthly Cleanup (1st of month, 3:08 AM GMT+8)**:
```json
{
  "agentId": "english-tutor",
  "name": "Vocab Monthly Cleanup",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "* 3 1 * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "Run monthly vocab cleanup: cd skills/vocab-review && source .venv/bin/activate && python -c 'from vocab_manager import archive_mastered; archived = archive_mastered(\"../../projects/vocabulary/data/vocab.db\"); print(f\"Archived {archived} mastered words\")'. Just send the output - nothing else.",
    "model": "zai/glm-5"
  },
  "delivery": {
    "channel": "feishu",
    "mode": "announce",
    "to": "chat:oc_55bf80b97398600ff6da478ae62937de"
  }
}
```

### Phase 6: Update HEARTBEAT.md (1 min)

```markdown
### Vocabulary Review Sender
If `/root/.openclaw/workspace-english-tutor/projects/vocabulary/output/.send_pending` exists:
1. Send `daily_review.docx` to Feishu chat `oc_55bf80b97398600ff6da478ae62937de`
2. Delete the `.send_pending` flag file
3. Log the result

This enables cron-generated reviews to be sent via OpenClaw's Feishu integration.
```

---

## Migration Checklist

- [ ] Create new directory structure (`projects/vocabulary/{data,output,docs}`)
- [ ] Create `vocab_manager.py` with SQLite logic
- [ ] Refactor `generate_review.py` to use SQLite
- [ ] Run migration: `vocab.json` → `vocab.db`
- [ ] Verify migration: row count matches, spot-check data
- [ ] Update AGENTS.md (new paths, SQLite snippets)
- [ ] Update HEARTBEAT.md (new output path)
- [ ] Setup Git tracking for `vocab.db.bak`
- [ ] Add `.gitignore` (ignore `vocab.db`, `vocab.db-wal`, `vocab.db-shm`)
- [ ] Update cron jobs
- [ ] Test review generation from SQLite
- [ ] Test backup automation
- [ ] Keep `vocab.json` as read-only fallback for 1 week, then remove

---

## Benefits

1. **No more full-file rewrites**
   - Adding a word = 1 INSERT, not rewriting 225 KB
   - Updating review status = 1 UPDATE per item

2. **Concurrent access safety**
   - WAL mode handles agent + cron simultaneously
   - No more risk of data clobber

3. **Built-in querying**
   - Spaced repetition selection is a single SQL query
   - History queries: `SELECT * WHERE added_date = '2026-02-15'`
   - Stats: `SELECT status, COUNT(*) FROM vocab GROUP BY status`

4. **Archival without file juggling**
   - Mastered words get `archived_date` set, stay in same DB
   - No multiple JSON files to manage

5. **Separation of concerns**
   - Skills = shareable tools (SQLite logic)
   - Projects = your personal data (`vocab.db`)

6. **Zero new dependencies**
   - `sqlite3` is in Python's standard library

---

## Estimated Time

- **Phase 1**: 5 minutes (create structure)
- **Phase 2**: 20 minutes (write vocab_manager.py + refactor generate_review.py)
- **Phase 3**: 2 minutes (run migration, verify)
- **Phase 4**: 5 minutes (update AGENTS.md)
- **Phase 5**: 3 minutes (update cron jobs)
- **Phase 6**: 1 minute (update HEARTBEAT.md)

**Total**: ~35 minutes

---

## References

- [SQLite WAL Mode](https://www.sqlite.org/wal.html)
- [Python sqlite3 docs](https://docs.python.org/3/library/sqlite3.html)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [Creating Skills Guide](https://docs.openclaw.ai/tools/creating-skills)
