#!/bin/bash
# Daily Vocabulary Review - Run via cron or manually
# Sends .docx to Feishu using OpenClaw message tool

set -e

SCRIPT_DIR="/root/.openclaw/agents/english-tutor/workspace/skills/vocab-review"
VOCAB_SCRIPT="$SCRIPT_DIR/vocab.py"
OUTPUT_FILE="$SCRIPT_DIR/daily_review.docx"
FEISHU_CHAT_ID="oc_55bf80b97398600ff6da478ae62937de"

echo "========================================"
echo "📚 Daily Vocabulary Review"
echo "$(date)"
echo "========================================"

# Run Python script to generate .docx
cd "$SCRIPT_DIR"
source .venv/bin/activate
python3 "$VOCAB_SCRIPT"

# Send to Feishu via OpenClaw message tool
# Note: This script is designed to be called from within OpenClaw
# When run via cron, use the openclaw CLI or API
if command -v openclaw &> /dev/null; then
    openclaw message send \
        --channel feishu \
        --account default \
        --target "$FEISHU_CHAT_ID" \
        --file "$OUTPUT_FILE" \
        --message "📚 Your daily vocabulary review is here!"
    echo "[INFO] Sent to Feishu via openclaw CLI"
else
    echo "[INFO] Generated $OUTPUT_FILE"
    echo "[INFO] To send to Feishu, run manually from OpenClaw session"
fi

echo "========================================"
echo "✅ Done!"
echo "========================================"
