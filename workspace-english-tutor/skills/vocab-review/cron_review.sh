#!/bin/bash
# Daily Vocabulary Review Cron Job
# Runs at 7 AM GMT+8 (11 PM UTC previous day)
# Generates .docx and sends directly to Feishu

set -e

WORKSPACE_DIR="/root/openclaw-workspaces/workspace-english-tutor"
SCRIPT_DIR="$WORKSPACE_DIR/skills/vocab-review"
GENERATE_SCRIPT="$SCRIPT_DIR/generate_review.py"
SEND_SCRIPT="$SCRIPT_DIR/send_to_feishu.mjs"
LOG_FILE="$SCRIPT_DIR/review.log"

echo "$(date): Starting vocabulary review" >> "$LOG_FILE"

# Load environment variables
export $(grep -v '^#' /root/.openclaw/.env | xargs)

# Run Python script to generate .docx
cd "$SCRIPT_DIR"
source .venv/bin/activate
python3 "$GENERATE_SCRIPT" >> "$LOG_FILE" 2>&1

# Send to Feishu
node "$SEND_SCRIPT" >> "$LOG_FILE" 2>&1

echo "$(date): Review generated and sent" >> "$LOG_FILE"
