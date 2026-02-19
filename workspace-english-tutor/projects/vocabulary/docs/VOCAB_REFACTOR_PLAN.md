# Vocabulary System Refactor Plan

**Date**: 2026-02-19  
**Status**: Proposed  
**Goal**: Restructure vocabulary management for scalability, maintainability, and automated backups

---

## Current Issues

1. **Bloat**: 370 items in a single JSON file, growing daily
2. **Review inefficiency**: As the list grows, items get reviewed less frequently
3. **No archival strategy**: "mastered" items (7+ reviews) stay in active pool forever
4. **Performance**: Loading/parsing a massive JSON on every review will slow down
5. **Backup is manual**: Cron just generates docx, no actual backup/archival
6. **Mixed concerns**: Data and logic live together in `skills/`

---

## Proposed Structure

### Directory Layout

```
workspace-english-tutor/
├── projects/
│   └── vocabulary/
│       ├── data/
│       │   ├── active.json           ← Current learning (< 100 items)
│       │   └── archive/
│       │       ├── 2026-02.json      ← Monthly snapshots
│       │       ├── 2026-01.json      ← January archive
│       │       └── mastered.json     ← Graduated words (7+ reviews)
│       ├── output/
│       │   └── daily_review.docx     ← Generated reviews
│       └── README.md                 ← Project documentation
│
├── skills/
│   └── vocab-review/
│       ├── SKILL.md                  ← Skill documentation
│       ├── vocab_manager.py          ← Core logic (add/archive/select)
│       ├── generate_review.py        ← Review generator
│       ├── requirements.txt          ← Dependencies
│       └── .venv/                    ← Virtual environment
│
├── AGENTS.md                         ← Documents workspace conventions
└── ...
```

---

## Key Principles

### Skills = Reusable Tools
- **Pure logic**, no user data
- Can be shared/published
- Version controlled separately
- Example: `vocab_manager.py` with functions like `add_word()`, `archive_mastered()`, `select_for_review()`

### Projects = User Data + Workflows
- **Your specific vocabulary list**
- Personal learning progress
- Generated outputs
- Not meant to be shared

---

## Data Management Strategy

### 1. Archive Mastered Words
Move items with `status: "mastered"` to `archive/mastered.json` after they've been stable for 30+ days. Keeps active list lean.

### 2. Tiered Review System
- **Learning** (0-2 reviews): Daily pool
- **Reviewing** (3-6 reviews): Every 3 days
- **Mastered** (7+ reviews): Every 7 days, then archive

### 3. Monthly Snapshots
Export new additions each month to `archive/YYYY-MM.json` for historical tracking.

### 4. Smart Selection Algorithm
Weight selection by:
- Time since last review (older = higher priority)
- Status (learning > reviewing > mastered)
- Review count (lower = higher priority)

---

## Backup Strategy: Git (Simplest)

### Why Git?
- ✅ Already installed
- ✅ Version history
- ✅ Free (GitHub/GitLab)
- ✅ Works with cron
- ✅ Zero maintenance

```json
{
  "name": "vocab-backup",
  "schedule": { "kind": "cron", "expr": "0 2 * * *", "tz": "UTC" },
  "payload": {
    "kind": "systemEvent",
    "text": "cd /root/openclaw-workspaces/workspace-english-tutor && git add projects/vocabulary/data && git commit -m 'Daily vocab backup' && git push"
  },
  "sessionTarget": "main"
}
```

---

## Implementation Plan

### Phase 1: Create New Structure (5 min)
```bash
# Create project structure
mkdir -p projects/vocabulary/{data/archive,output}

# Move data files
mv skills/vocab-review/vocab.json projects/vocabulary/data/active.json
mv skills/vocab-review/daily_review.docx projects/vocabulary/output/ 2>/dev/null || true

# Create README
cat > projects/vocabulary/README.md << 'EOF'
# Vocabulary Learning Project

## Data Files
- `data/active.json`: Current learning items (< 100)
- `data/archive/`: Historical snapshots and mastered words

## Output
- `output/daily_review.docx`: Generated daily review

## Tools
See `../../skills/vocab-review/` for management scripts.
EOF
```

### Phase 2: Refactor Code (15 min)

**skills/vocab-review/vocab_manager.py** (new):
```python
"""
Vocabulary Management Library
Handles: add, archive, select, status updates
"""
from pathlib import Path
import json
from datetime import datetime, timedelta

class VocabManager:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.active_file = self.data_dir / "active.json"
        self.archive_dir = self.data_dir / "archive"
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def load_active(self):
        """Load active vocabulary data."""
        with open(self.active_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_active(self, data):
        """Save active vocabulary data."""
        with open(self.active_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_word(self, word_data):
        """Add new word to active.json."""
        data = self.load_active()
        max_id = max((item['id'] for item in data['items']), default=0)
        word_data['id'] = max_id + 1
        word_data['added_date'] = datetime.now().strftime('%Y-%m-%d')
        word_data['review_count'] = 0
        word_data['last_reviewed'] = None
        word_data['status'] = 'learning'
        data['items'].append(word_data)
        self.save_active(data)
        return word_data['id']
    
    def select_for_review(self, max_items=20):
        """Smart selection with spaced repetition."""
        data = self.load_active()
        items = data.get('items', [])
        
        if not items:
            return []
        
        # Sort by: status priority, review count, last reviewed
        def sort_key(item):
            status = item.get('status', 'learning')
            review_count = item.get('review_count', 0)
            last_reviewed = item.get('last_reviewed', '')
            
            status_priority = {
                'learning': 0,
                'reviewing': 1,
                'mastered': 2
            }.get(status, 0)
            
            return (status_priority, review_count, last_reviewed or '')
        
        sorted_items = sorted(items, key=sort_key)
        return sorted_items[:max_items]
    
    def update_review_status(self, reviewed_ids):
        """Update review count and status for reviewed items."""
        data = self.load_active()
        today = datetime.now().strftime('%Y-%m-%d')
        
        for item in data['items']:
            if item['id'] in reviewed_ids:
                item['review_count'] = item.get('review_count', 0) + 1
                item['last_reviewed'] = today
                
                # Update status based on review count
                count = item['review_count']
                if count >= 7:
                    item['status'] = 'mastered'
                elif count >= 3:
                    item['status'] = 'reviewing'
        
        self.save_active(data)
    
    def archive_mastered(self, days_threshold=30):
        """Move mastered words to archive/mastered.json."""
        data = self.load_active()
        today = datetime.now()
        cutoff = today - timedelta(days=days_threshold)
        
        mastered_file = self.archive_dir / "mastered.json"
        
        # Load existing mastered archive
        if mastered_file.exists():
            with open(mastered_file, 'r', encoding='utf-8') as f:
                mastered_data = json.load(f)
        else:
            mastered_data = {'items': []}
        
        # Find items to archive
        to_archive = []
        remaining = []
        
        for item in data['items']:
            if item.get('status') == 'mastered':
                last_reviewed = item.get('last_reviewed')
                if last_reviewed:
                    review_date = datetime.strptime(last_reviewed, '%Y-%m-%d')
                    if review_date < cutoff:
                        to_archive.append(item)
                        continue
            remaining.append(item)
        
        if to_archive:
            # Add to mastered archive
            mastered_data['items'].extend(to_archive)
            with open(mastered_file, 'w', encoding='utf-8') as f:
                json.dump(mastered_data, f, ensure_ascii=False, indent=2)
            
            # Update active list
            data['items'] = remaining
            self.save_active(data)
        
        return len(to_archive)
    
    def monthly_snapshot(self):
        """Export this month's additions to archive/YYYY-MM.json."""
        data = self.load_active()
        today = datetime.now()
        month_str = today.strftime('%Y-%m')
        snapshot_file = self.archive_dir / f"{month_str}.json"
        
        # Get items added this month
        month_items = [
            item for item in data['items']
            if item.get('added_date', '').startswith(month_str)
        ]
        
        if month_items:
            snapshot_data = {
                'month': month_str,
                'items': month_items,
                'snapshot_date': today.strftime('%Y-%m-%d')
            }
            with open(snapshot_file, 'w', encoding='utf-8') as f:
                json.dump(snapshot_data, f, ensure_ascii=False, indent=2)
        
        return len(month_items)
```

**skills/vocab-review/generate_review.py** (refactored):
```python
#!/usr/bin/env python3
"""
Generate daily vocabulary review .docx
Usage: python generate_review.py [--data-dir PATH]
"""
import argparse
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from datetime import datetime

from vocab_manager import VocabManager

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
        synonyms = item.get('synonyms', [])
        if synonyms:
            p = doc.add_paragraph()
            p.add_run('Synonyms: ').bold = True
            p.add_run(', '.join(synonyms))
        
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
    parser.add_argument('--data-dir', type=str, 
                       default='../../projects/vocabulary/data',
                       help='Path to vocabulary data directory')
    parser.add_argument('--output-dir', type=str,
                       default='../../projects/vocabulary/output',
                       help='Path to output directory')
    args = parser.parse_args()
    
    # Resolve paths relative to script location
    script_dir = Path(__file__).parent
    data_dir = (script_dir / args.data_dir).resolve()
    output_dir = (script_dir / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 50)
    print("📚 Vocabulary Review Generator")
    print("=" * 50)
    
    # Initialize manager
    manager = VocabManager(data_dir)
    
    # Select items for review
    items = manager.select_for_review(max_items=20)
    print(f"[INFO] Selected {len(items)} items for review")
    
    # Generate .docx
    doc = generate_docx(items)
    output_file = output_dir / "daily_review.docx"
    doc.save(str(output_file))
    print(f"[INFO] Generated: {output_file}")
    
    # Update review status
    reviewed_ids = [item['id'] for item in items]
    manager.update_review_status(reviewed_ids)
    print(f"[INFO] Updated review status for {len(items)} items")
    
    print("=" * 50)
    print("✅ Daily review document generated!")
    print("=" * 50)

if __name__ == '__main__':
    main()
```

### Phase 3: Update AGENTS.md (2 min)

Replace the "Vocabulary Management" section with:

```markdown
## 📖 Vocabulary Management

### File Locations
- **Data**: `projects/vocabulary/data/active.json` (current learning)
- **Archive**: `projects/vocabulary/data/archive/` (monthly + mastered)
- **Output**: `projects/vocabulary/output/daily_review.docx`
- **Tools**: `skills/vocab-review/` (management scripts)

### Backup
- **Git**: Auto-commit daily at 2 AM UTC
- **Remote**: GitHub (private repo)

### Adding Words
Use the Python helper in `skills/vocab-review/vocab_manager.py`:

```python
from vocab_manager import VocabManager

manager = VocabManager('projects/vocabulary/data')
manager.add_word({
    'type': 'word',
    'content': 'example',
    'ipa': '/ɪɡˈzæm.pəl/',
    'english': 'A thing characteristic of its kind',
    'chinese': '例子；榜样',
    'example': 'This is an example sentence.',
    'synonyms': ['sample', 'instance'],
    'memory_trick': ''
})
```

### Review System
- **Script**: `skills/vocab-review/generate_review.py`
- **Cron**: Morning 7AM + Evening 7PM (GMT+8)
- **Selection**: Spaced repetition (learning → reviewing → mastered)

### Archival
- **Monthly**: Auto-snapshot new additions to `archive/YYYY-MM.json`
- **Mastered**: Words with 7+ reviews and 30+ days since last review → `archive/mastered.json`
```

### Phase 4: Update Cron Jobs (3 min)

**Morning Review (7 AM GMT+8)**:
```json
{
  "name": "vocab-morning",
  "schedule": { "kind": "cron", "expr": "0 23 * * *", "tz": "UTC" },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate vocabulary review: cd skills/vocab-review && python generate_review.py"
  },
  "sessionTarget": "isolated"
}
```

**Evening Review (7 PM GMT+8)**:
```json
{
  "name": "vocab-evening",
  "schedule": { "kind": "cron", "expr": "0 11 * * *", "tz": "UTC" },
  "payload": {
    "kind": "agentTurn",
    "message": "Generate vocabulary review: cd skills/vocab-review && python generate_review.py"
  },
  "sessionTarget": "isolated"
}
```

**Daily Backup (2 AM UTC)**:
```json
{
  "name": "vocab-backup",
  "schedule": { "kind": "cron", "expr": "0 2 * * *", "tz": "UTC" },
  "payload": {
    "kind": "systemEvent",
    "text": "cd /root/.openclaw/workspace-english-tutor && git add projects/vocabulary/data && git commit -m 'Daily vocab backup' && git push"
  },
  "sessionTarget": "main"
}
```

**Monthly Cleanup (1st of month, 3 AM UTC)**:
```json
{
  "name": "vocab-monthly-cleanup",
  "schedule": { "kind": "cron", "expr": "0 3 1 * *", "tz": "UTC" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run monthly vocab cleanup: cd skills/vocab-review && python -c 'from vocab_manager import VocabManager; m = VocabManager(\"../../projects/vocabulary/data\"); archived = m.archive_mastered(); snapshot = m.monthly_snapshot(); print(f\"Archived {archived} mastered words, snapshot {snapshot} new words\")'"
  },
  "sessionTarget": "isolated"
}
```

### Phase 5: Update AGENTS.md (1 min)

Replace the vocabulary section with:


### Vocabulary Review Sender
If `/root/.openclaw/workspace-english-tutor/projects/vocabulary/output/.send_pending` exists:
1. Send `daily_review.docx` to Feishu chat `oc_55bf80b97398600ff6da478ae62937de`
2. Delete the `.send_pending` flag file
3. Log the result

This enables cron-generated reviews to be sent via OpenClaw's Feishu integration.
```

---

## Migration Checklist

- [ ] Create new directory structure
- [ ] Move `vocab.json` → `active.json`
- [ ] Create `vocab_manager.py`
- [ ] Refactor `generate_review.py`
- [ ] Update AGENTS.md
- [ ] Update HEARTBEAT.md
- [ ] Setup Git repository
- [ ] Add `.gitignore`
- [ ] Create initial commit
- [ ] Add remote repository
- [ ] Update cron jobs
- [ ] Test review generation
- [ ] Test backup automation
- [ ] Archive old mastered words (optional)

---

## Benefits

1. **Separation of Concerns**
   - Skills = shareable tools
   - Projects = your personal data

2. **Scalability**
   - Active list stays small (< 100 items)
   - Archives grow without slowing down daily reviews

3. **Backup-Friendly**
   - `projects/vocabulary/` synced to cloud via Git
   - Version history for all changes

4. **Reusability**
   - Someone else can use your `vocab-review` skill
   - Just point it to their own `projects/vocabulary/data/`

5. **Maintainability**
   - Clear separation between data and logic
   - Easy to debug and extend

---

## Estimated Time

- **Phase 1**: 5 minutes (create structure)
- **Phase 2**: 15 minutes (refactor code)
- **Phase 3**: 2 minutes (update AGENTS.md)
- **Phase 4**: 3 minutes (update cron)
- **Phase 5**: 1 minute (update HEARTBEAT.md)

**Total**: ~30 minutes

---

## References

- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [Creating Skills Guide](https://docs.openclaw.ai/tools/creating-skills)
- [AgentSkills Spec](https://agentskills.io)
