---
name: openclaw-agents
description: "Configure OpenClaw agents, multi-agent routing, and per-agent settings. Use when: (1) Creating or managing agents via CLI or config, (2) Setting up multi-agent routing with bindings, (3) Configuring per-agent models, sandbox, or tool restrictions, (4) Understanding agentId, accountId, workspace, agentDir concepts, (5) Applying configuration changes to openclaw.json. Covers agents.list, bindings, per-agent sandbox/tools, and the openclaw agents CLI."
---

# OpenClaw Agent Configuration

Guide for configuring agents, multi-agent routing, and per-agent settings in OpenClaw.

## What is an Agent?

An agent is a fully scoped "brain" with its own:

- **Workspace** - Files, AGENTS.md, SOUL.md, USER.md, persona rules
- **Agent directory** - Auth profiles, model registry, per-agent config
- **Session store** - Chat history under `~/.openclaw/agents/<agentId>/sessions`
- **Optional isolation** - Sandbox, tool restrictions, model override

Multiple agents = multiple people or personalities sharing one Gateway server with isolated data and auth.

## Core Concepts

| Term | Description |
|------|-------------|
| `agentId` | Unique identifier for an agent (e.g., "main", "work", "family") |
| `accountId` | Channel account instance (e.g., WhatsApp "personal" vs "biz") |
| `workspace` | Directory for agent files (default: `~/.openclaw/workspace-<agentId>`) |
| `agentDir` | State directory for auth/config (default: `~/.openclaw/agents/<agentId>/agent`) |
| `binding` | Rule that routes inbound messages to an agentId |

## Key Paths

```
~/.openclaw/
├── openclaw.json              # Main config (agents + bindings)
├── workspace/                 # Default workspace (agent: main)
├── workspace-<profile>/       # Profile-specific workspace
├── workspace-<agentId>/       # Per-agent workspace
└── agents/
    └── <agentId>/
        ├── agent/             # agentDir: auth-profiles.json, model registry
        └── sessions/          # Session store
```

## Agent Management

### CLI Workflow (Recommended)

```bash
# Add a new agent interactively
openclaw agents add work

# List agents with their bindings
openclaw agents list --bindings

# Verify routing
openclaw agents list --bindings
```

The CLI wizard handles workspace creation, config updates, and basic binding setup.

### Manual Config

Add entries to `agents.list[]` in `~/.openclaw/openclaw.json`:

```json5
{
  agents: {
    list: [
      {
        id: "work",
        name: "Work Agent",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
        model: "anthropic/claude-sonnet-4-5",
      },
    ],
  },
}
```

## Multi-Agent Routing

### How Bindings Work

Bindings route inbound messages to agents. First match wins (most-specific first).

**Routing priority (highest to lowest):**
1. `peer` match (exact DM/group/channel id)
2. `guildId` (Discord) / `teamId` (Slack)
3. `accountId` match
4. Channel-level match (`accountId: "*"`)
5. Default agent (`agents.list[].default: true`, else first entry, else "main")

### Binding Structure

```json5
{
  bindings: [
    {
      agentId: "work",
      match: {
        channel: "whatsapp",
        accountId: "biz",                    // optional
        peer: { kind: "direct", id: "+15551234567" },  // optional
      },
    },
  ],
}
```

### Match Examples

| Goal | Match Rule |
|------|------------|
| All WhatsApp to agent | `{ channel: "whatsapp" }` |
| Specific account | `{ channel: "whatsapp", accountId: "biz" }` |
| Specific DM | `{ channel: "whatsapp", peer: { kind: "direct", id: "+15551234567" } }` |
| Specific group | `{ channel: "whatsapp", peer: { kind: "group", id: "1203630xx@g.us" } }` |

See [binding-patterns.md](references/binding-patterns.md) for complete copy-paste examples.

## Per-Agent Configuration

### Model Override

Each agent can use a different model:

```json5
{
  id: "opus",
  workspace: "~/.openclaw/workspace-opus",
  model: "anthropic/claude-opus-4-6",
}
```

### Sandbox Configuration

Isolate an agent's tool execution:

```json5
{
  id: "family",
  sandbox: {
    mode: "all",           // "off" | "all"
    scope: "agent",        // "agent" (per-agent container) | "shared"
    docker: {
      setupCommand: "apt-get update && apt-get install -y git",
    },
  },
}
```

### Tool Restrictions

Allow/deny tools per agent:

```json5
{
  id: "kiosk",
  tools: {
    allow: ["read", "web_search", "web_fetch"],
    deny: ["exec", "write", "edit", "browser", "nodes"],
  },
}
```

### Group Chat Settings

Control when agent responds in groups:

```json5
{
  id: "family",
  groupChat: {
    mentionPatterns: ["@family", "@familybot", "@Family Bot"],
  },
}
```

See [agent-config-patterns.md](references/agent-config-patterns.md) for complete examples.

## Applying Configuration Changes

### Option 1: Config Patch (Safe Partial Update)

Merges changes with existing config, validates, then restarts:

```bash
# Via gateway tool
gateway config.patch with the patch object

# Or via CLI
openclaw gateway config patch --patch '{"agents":{"list":[{"id":"work"}]}}'
```

### Option 2: Config Apply (Full Replace)

Replaces entire config, validates, then restarts:

```bash
# Via gateway tool
gateway config.apply with the full config

# Or via CLI
openclaw gateway config apply --file openclaw.json
```

### Option 3: Manual Edit + Restart

```bash
# Edit the file
nano ~/.openclaw/openclaw.json

# Restart to apply
openclaw gateway restart
```

**Recommendation:** Use `config.patch` for incremental changes. Use `config.apply` only when replacing the entire config.

## Common Patterns

| Scenario | Reference |
|----------|-----------|
| Two WhatsApp accounts → two agents | [binding-patterns.md](references/binding-patterns.md#two-accounts) |
| DM split by phone number | [binding-patterns.md](references/binding-patterns.md#dm-split) |
| Channel split (chat vs deep work) | [binding-patterns.md](references/binding-patterns.md#channel-split) |
| Agent with sandbox + tool restrictions | [agent-config-patterns.md](references/agent-config-patterns.md#sandbox-tools) |
| Group-only agent with mentions | [agent-config-patterns.md](references/agent-config-patterns.md#group-agent) |

## Troubleshooting

### Messages going to wrong agent

1. Check binding order (most-specific first)
2. Verify `openclaw agents list --bindings`
3. Ensure `peer.id` matches exactly (E.164 for phones)

### Auth not working

- Auth profiles are per-agent: check `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- Main agent credentials are NOT shared automatically
- Copy `auth-profiles.json` between agentDirs if needed

### Config not applying

- Use `config.patch` for incremental changes
- Check JSON5 syntax (trailing commas OK, comments OK)
- Verify with `openclaw gateway config get`
