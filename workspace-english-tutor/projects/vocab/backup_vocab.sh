#!/bin/bash
# Vocab list daily backup script

VOCAB_SOURCE="/root/.openclaw/workspace-english-tutor/skills/vocab-review/vocab.json"
BACKUP_DIR="/root/.openclaw/workspace-english-tutor/projects/vocab/backup"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/vocab_backup_$TIMESTAMP.json"

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Count words in vocab file
WORD_COUNT=$(python3 -c "import json; print(len(json.load(open('$VOCAB_SOURCE'))['items']))")

# Copy the vocab file
cp "$VOCAB_SOURCE" "$BACKUP_FILE"

# Keep only last 7 backups
cd "$BACKUP_DIR" && ls -t vocab_backup_*.json | tail -n +8 | xargs -r rm

# Output result for notification
echo "✅ Vocab backup complete: $WORD_COUNT words backed up to projects/vocab/backup/"
