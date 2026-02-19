# HEARTBEAT.md - Periodic Checks

## Daily Tasks

### Vocabulary Review Sender
If `/root/.openclaw/agents/english-tutor/workspace/skills/vocab-review/.send_pending` exists:
1. Send `daily_review.docx` to Feishu chat `oc_55bf80b97398600ff6da478ae62937de`
2. Delete the `.send_pending` flag file
3. Log the result

This enables cron-generated reviews to be sent via OpenClaw's Feishu integration.
