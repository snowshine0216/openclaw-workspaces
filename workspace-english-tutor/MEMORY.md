# Long-term Memory

## User Preferences
- **Channel**: Feishu (primary)
- **No Tailscale** - prefers simpler setups without tunnel services

## Integrations

### Feishu (Working)
- App ID: cli_a90f0d922e795cc7
- Account: "default" (critical naming requirement)
- dmPolicy: "open" (bypassed pairing for testing)
- Test user: ou_6f7951d4e2d259e02ef5791ee86d38d6
- Chat ID: oc_55bf80b97398600ff6da478ae62937de

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

## Notes
- Credentials exposed in chat - user should rotate App Secret after testing
- User is direct: wants results, not explanation-heavy responses
- User communicates in both English and Chinese
- 163.com email: snowshine@163.com (IMAP blocked - needs user to enable in settings)
