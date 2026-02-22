# Long-term Memory

## User Preferences
- **Channel**: Feishu (primary)
- **No Tailscale** - prefers simpler setups without tunnel services
- **Research tool**: Tavily Search (AI-optimized, always use for AI news/research)

## Integrations

### Feishu (Working)
- App ID: cli_a90f0d922e795cc7
- Account: "default" (critical naming requirement)
- dmPolicy: "open" (bypassed pairing for testing)
- User ID: ou_ac0664ae2ad545cdbfa0ffe2c56a9328 (Snow, primary DM target)

### Gmail (Working ✅)
- Email: xue.yin.0216@gmail.com
- GCP Project: snows-project-472022
- **Credentials stored in:** `/root/.openclaw/agents/main/agent/auth-profiles.json` (`gmail:default` profile)
- Refresh token: stored and permanent
- Scope: `https://www.googleapis.com/auth/gmail.readonly`
- No webhook - uses polling via refresh token

## Model Provider
- **GLM-5 (zai/glm-5)** - Current primary model
- MiniMax M2.1 (backup)
- Gemini 2.0 Flash configured but unused
- Zai provider: `https://api.z.ai/api/anthropic`

## Knowledge Base Index

Recent entries in `projects/knowledge-base/`:
- 2026-02-21: AI Agent Testing: Dev to Production → ai-tools/2026-02-21-ai-agent-testing-production.md
- 2026-02-20: Django REST API Optimization → ai-tools/2026-02-20-django-rest-api-optimization.md
- 2026-02-19: Example entry (setup) → ai-models/2026-02-19-example-entry.md

Topics: ai-models, ai-research, ai-tools, ai-industry, ai-qa  
Search: `bash projects/knowledge-base/search.sh "query"`

## Notes
- Credentials exposed in chat - user should rotate App Secret after testing
- User is direct: wants results, not explanation-heavy responses
- User communicates in both English and Chinese
- 163.com email: snowshine@163.com (IMAP blocked - needs user to enable in settings)
