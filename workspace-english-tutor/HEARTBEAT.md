# HEARTBEAT.md - Periodic Checks

## Daily Tasks

### Vocabulary Review
Cron job handles generation and delivery directly to Feishu (no heartbeat action needed).
- **Schedule:** 7 AM GMT+8 (11 PM UTC previous day)
- **Chat:** oc_eb619c8fea8c56afb88b44bf92abaca1 (English Tutor)
- **Script:** `/root/openclaw-workspaces/workspace-english-tutor/skills/vocab-review/cron_review.sh`

If you need to manually send a review:
1. Check `projects/vocabulary/output/daily_review.docx` exists
2. Run: `cd skills/vocab-review && node send_to_feishu.mjs`
