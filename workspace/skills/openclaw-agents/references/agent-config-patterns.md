# Agent Configuration Patterns

Copy-paste ready agent configuration examples for `agents.list[]`.

## Table of Contents

- [Single Agent (Default)](#single-agent-default)
- [Two Agents with Different Models](#two-agents-with-different-models)
- [Agent with Sandbox and Tool Restrictions](#agent-with-sandbox-and-tool-restrictions)
- [Group-Only Agent with Mentions](#group-only-agent-with-mentions)
- [Agent with Custom Identity](#agent-with-custom-identity)

---

## Single Agent (Default)

**Use case:** Minimal config for single-agent setup (OpenClaw default).

```json5
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        name: "Main",
        // workspace defaults to ~/.openclaw/workspace
        // agentDir defaults to ~/.openclaw/agents/main/agent
      },
    ],
  },
}
```

**Notes:**
- This is the implicit default if no agents are configured
- All channels route to "main" automatically
- No explicit bindings needed for single-agent mode

---

## Two Agents with Different Models

**Use case:** Personal agent (fast/cheap) + Work agent (powerful).

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        default: true,
        name: "Personal",
        workspace: "~/.openclaw/workspace-personal",
        model: "anthropic/claude-sonnet-4-5",  // Fast, efficient
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
        model: "anthropic/claude-opus-4-6",  // Most capable
      },
    ],
  },

  bindings: [
    { agentId: "work", match: { channel: "slack" } },
    { agentId: "personal", match: { channel: "whatsapp" } },
    { agentId: "personal", match: { channel: "telegram" } },
  ],
}
```

**Notes:**
- Each workspace has its own AGENTS.md, SOUL.md, USER.md
- Model aliases supported: `claude-sonnet`, `claude-opus`, `glm-5`, etc.
- `default: true` ensures fallback routing

---

## Agent with Sandbox and Tool Restrictions

**Use case:** Family/kiosk agent with limited capabilities for safety.

```json5
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        workspace: "~/.openclaw/workspace",
        // No sandbox, all tools available
      },
      {
        id: "family",
        name: "Family",
        workspace: "~/.openclaw/workspace-family",
        agentDir: "~/.openclaw/agents/family/agent",
        sandbox: {
          mode: "all",           // Always sandboxed
          scope: "agent",        // One container per agent
          docker: {
            // Runs once on container creation
            setupCommand: "apt-get update && apt-get install -y git curl",
          },
        },
        tools: {
          // Whitelist approach: only these tools
          allow: [
            "read",
            "web_search",
            "web_fetch",
            "sessions_list",
            "sessions_history",
            "sessions_send",
          ],
          // Explicitly deny dangerous tools
          deny: [
            "exec",
            "write",
            "edit",
            "browser",
            "nodes",
            "cron",
            "gateway",
          ],
        },
      },
    ],
  },
}
```

**Notes:**
- `tools.allow/deny` applies to tool names (exec, write), not skills
- If a skill needs `exec`, ensure it's allowed and the binary exists in sandbox
- `scope: "agent"` creates a dedicated container; `scope: "shared"` uses a common one
- `tools.elevated` is global and sender-based, not configurable per agent

---

## Group-Only Agent with Mentions

**Use case:** Agent that only responds when mentioned in a group chat.

```json5
{
  agents: {
    list: [
      {
        id: "family",
        name: "Family Bot",
        workspace: "~/.openclaw/workspace-family",
        identity: {
          name: "Family Bot",
        },
        groupChat: {
          // Only respond when mentioned these ways
          mentionPatterns: [
            "@family",
            "@familybot",
            "@Family Bot",
            "hey family bot",
          ],
        },
        // Optional: lighter model for group chat
        model: "anthropic/claude-sonnet-4-5",
      },
    ],
  },

  bindings: [
    {
      agentId: "family",
      match: {
        channel: "whatsapp",
        peer: { kind: "group", id: "1203630xxxxxxxxxx@g.us" },
      },
    },
  ],
}
```

**Notes:**
- Without `mentionPatterns`, agent responds to all messages in bound groups
- Patterns are case-insensitive by default
- Works best with channel-level group allowlists for additional gating

---

## Agent with Custom Identity

**Use case:** Named bot with a specific personality for a community.

```json5
{
  agents: {
    list: [
      {
        id: "community",
        name: "Clawd",
        workspace: "~/.openclaw/workspace-community",
        agentDir: "~/.openclaw/agents/community/agent",
        identity: {
          name: "Clawd",
          emoji: "🦀",
        },
        model: "anthropic/claude-sonnet-4-5",
        groupChat: {
          mentionPatterns: ["@clawd", "@bot", "@help"],
        },
        // Slightly restricted for public-facing bot
        tools: {
          deny: ["gateway", "nodes"],
        },
      },
    ],
  },

  bindings: [
    {
      agentId: "community",
      match: { channel: "discord", guildId: "123456789012345678" },
    },
  ],
}
```

**Notes:**
- `identity.name` may be used in responses or UI (implementation-dependent)
- Customize persona in workspace's `SOUL.md` and `AGENTS.md`
- Consider `tools.deny: ["gateway"]` to prevent config changes from chat

---

## Field Reference

### Agent Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique agent identifier |
| `name` | No | Display name |
| `default` | No | Fallback agent when no binding matches |
| `workspace` | No | Working directory (default: `~/.openclaw/workspace-<id>`) |
| `agentDir` | No | State directory (default: `~/.openclaw/agents/<id>/agent`) |
| `model` | No | Model override for this agent |
| `identity` | No | `{ name, emoji }` for bot identity |
| `groupChat` | No | `{ mentionPatterns: string[] }` |
| `sandbox` | No | `{ mode, scope, docker }` |
| `tools` | No | `{ allow: string[], deny: string[] }` |

### Sandbox Fields

| Field | Values | Description |
|-------|--------|-------------|
| `mode` | `"off"` \| `"all"` | Whether to sandbox tool execution |
| `scope` | `"agent"` \| `"shared"` | Per-agent container or shared |
| `docker.setupCommand` | string | Command run once on container creation |

### Tools Configuration

```json5
tools: {
  allow: ["read", "write", "exec", ...],  // Whitelist (optional)
  deny: ["gateway", "nodes", ...],        // Blacklist (optional)
}
```

If both are specified, deny takes precedence. If neither is specified, all tools are available.
