# Delegation Rules - Intent-Based Task Routing

Clover delegates tasks to specialized agents based on **message intent**, not sender address.

## Routing Rules

### Rule 1: English Language Questions → english-tutor

**Trigger patterns:**
- "What's the meaning of [word/phrase]?"
- "What does [word] mean?"
- "How do you say [X] in English?"
- "Is this sentence correct?"
- "Can you help me with my English?"
- Grammar, vocabulary, pronunciation questions
- Any language learning related query

**Delegate to:** `english-tutor`
**Feishu chat ID:** `oc_eb619c8fea8c56afb88b44bf92abaca1`

### Rule 2: Research / Information Collection → information-collector

**Trigger patterns:**
- "Do research on [topic]"
- "What's happening with [person/company/event]?"
- "Find out about [X]"
- "What does [X] mean in the context of [Y]?" (conceptual research)
- "Look up information about [X]"
- Current events, news, trends
- Deep dives into topics
- "What happened to [X]?" (e.g., "What happened to Karpathy?")

**Delegate to:** `information-collector`
**Feishu chat ID:** `oc_46c066f92eff10bb928f4ec9f0ec20c0`

## Delegation Workflow

1. **Identify intent** - Match user message to routing rules
2. **Spawn subagent** - Use the appropriate agent for the task
3. **Wait for completion** - Don't just fire and forget
4. **Report back** - Summarize results to the user

## How to Delegate

Use the message tool to send the task to the specialized agent's Feishu chat:

```json
{
  "action": "send",
  "channel": "feishu",
  "target": "oc_eb619c8fea8c56afb88b44bf92abaca1",
  "message": "[Task from Clover] <user's question>"
}
```

## Notes

- If unsure which agent, ask the user for clarification
- If task spans multiple domains, handle what you can and delegate the rest
- Always follow up on delegated tasks
- Report completion back to the user's original chat

---

## Agent Registry

| Agent | ID | Feishu Chat ID | Purpose |
|-------|-----|----------------|---------|
| english-tutor | english-tutor | `oc_eb619c8fea8c56afb88b44bf92abaca1` | Language learning, grammar, vocabulary |
| information-collector | information-collector | `oc_46c066f92eff10bb928f4ec9f0ec20c0` | Research, news, information gathering |
| main (Clover) | main | `oc_55bf80b97398600ff6da478ae62937de` | Clover's main chat, orchestration |
