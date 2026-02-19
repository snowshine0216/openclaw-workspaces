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
