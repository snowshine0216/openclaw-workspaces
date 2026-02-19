# Binding Patterns

Copy-paste ready routing examples for `openclaw.json`.

## Table of Contents

- [Two Accounts → Two Agents](#two-accounts--two-agents)
- [DM Split by Phone Number](#dm-split-by-phone-number)
- [Channel Split](#channel-split)
- [Single Peer Override](#single-peer-override)
- [Group Binding](#group-binding)
- [Complex Multi-Rule Setup](#complex-multi-rule-setup)

---

## Two Accounts → Two Agents

**Use case:** Two WhatsApp accounts (personal + business) routed to different agents.

```json5
{
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
      },
    ],
  },

  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],

  channels: {
    whatsapp: {
      accounts: {
        personal: {
          // authDir defaults to ~/.openclaw/credentials/whatsapp/personal
        },
        biz: {
          // authDir defaults to ~/.openclaw/credentials/whatsapp/biz
        },
      },
    },
  },
}
```

**Notes:**
- Each `accountId` needs its own credentials directory
- Order doesn't matter here since accountIds are distinct

---

## DM Split by Phone Number

**Use case:** One WhatsApp account shared by multiple people; route each DM to their own agent.

```json5
{
  agents: {
    list: [
      { id: "alex", workspace: "~/.openclaw/workspace-alex" },
      { id: "mia", workspace: "~/.openclaw/workspace-mia" },
    ],
  },

  bindings: [
    {
      agentId: "alex",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230001" } },
    },
    {
      agentId: "mia",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230002" } },
    },
  ],

  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551230001", "+15551230002"],
    },
  },
}
```

**Notes:**
- `dmPolicy` and `allowFrom` are global per WhatsApp account, not per agent
- Replies come from the same WhatsApp number (no per-agent sender identity)
- Direct chats collapse to each agent's main session key

---

## Channel Split

**Use case:** Route WhatsApp to a fast everyday agent, Telegram to a powerful deep-work agent.

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },

  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

**Notes:**
- If you have multiple accounts per channel, add `accountId` to the match
- Peer-specific bindings override channel-wide rules

---

## Single Peer Override

**Use case:** Keep WhatsApp on a fast agent, but route one specific DM to a premium agent.

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "opus",
        name: "VIP",
        workspace: "~/.openclaw/workspace-opus",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },

  bindings: [
    // Peer override MUST come before channel-wide rule
    {
      agentId: "opus",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551234567" } },
    },
    // Channel-wide fallback
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

**Notes:**
- Peer bindings always win over channel-wide rules
- Order matters: put specific matches first

---

## Group Binding

**Use case:** Bind a dedicated agent to a single WhatsApp group with mention gating.

```json5
{
  agents: {
    list: [
      {
        id: "family",
        name: "Family Bot",
        workspace: "~/.openclaw/workspace-family",
        identity: { name: "Family Bot" },
        groupChat: {
          mentionPatterns: ["@family", "@familybot", "@Family Bot"],
        },
        sandbox: {
          mode: "all",
          scope: "agent",
        },
        tools: {
          allow: ["read", "sessions_list", "sessions_send"],
          deny: ["exec", "write", "edit", "browser", "cron"],
        },
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
- `mentionPatterns` gates when the agent responds in groups
- Tool restrictions apply to the `tools` layer (exec, write, etc.), not skills
- Group ID can be found in WhatsApp group invite links or via debugging

---

## Complex Multi-Rule Setup

**Use case:** Multiple channels, accounts, and peer overrides in one config.

```json5
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        name: "Main",
        workspace: "~/.openclaw/workspace",
        model: "anthropic/claude-sonnet-4-5",
      },
      {
        id: "vip",
        name: "VIP",
        workspace: "~/.openclaw/workspace-vip",
        model: "anthropic/claude-opus-4-6",
      },
      {
        id: "team",
        name: "Team",
        workspace: "~/.openclaw/workspace-team",
      },
    ],
  },

  bindings: [
    // 1. Specific peer overrides (highest priority)
    {
      agentId: "vip",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15559999999" } },
    },
    {
      agentId: "team",
      match: { channel: "discord", guildId: "123456789012345678" },
    },

    // 2. Account-level routing
    {
      agentId: "vip",
      match: { channel: "whatsapp", accountId: "biz" },
    },

    // 3. Channel-level fallbacks
    { agentId: "main", match: { channel: "whatsapp" } },
    { agentId: "main", match: { channel: "telegram" } },
    { agentId: "main", match: { channel: "discord" } },
  ],

  channels: {
    whatsapp: {
      accounts: {
        personal: {},
        biz: {},
      },
    },
  },
}
```

**Routing order explained:**
1. Peer match → VIP agent for `+15559999999`
2. Guild match → Team agent for Discord guild `123456789012345678`
3. Account match → VIP agent for WhatsApp `biz` account
4. Channel match → Main agent for remaining WhatsApp/Telegram/Discord
5. Default → Main agent (marked `default: true`)
