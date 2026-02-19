#!/bin/bash
# Daily Vocabulary Review Cron Job
# Runs at 8 PM GMT+8 (12 PM UTC)
# Generates .docx and sets flag for OpenClaw heartbeat to send

set -e

SCRIPT_DIR="/root/.openclaw/agents/english-tutor/workspace/skills/vocab-review"
VOCAB_SCRIPT="$SCRIPT_DIR/vocab.py"
FLAG_FILE="$SCRIPT_DIR/.send_pending"
LOG_FILE="$SCRIPT_DIR/review.log"

echo "$(date): Starting vocabulary review" >> "$LOG_FILE"

# Run Python script to generate .docx and update vocab.json
cd "$SCRIPT_DIR"
source .venv/bin/activate
python3 "$VOCAB_SCRIPT" >> "$LOG_FILE" 2>&1

# Create flag file to signal OpenClaw heartbeat to send the file
touch "$FLAG_FILE"

echo "$(date): Review generated, flag set for sending" >> "$LOG_FILE"
