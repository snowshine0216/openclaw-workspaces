---
title: "Claude Code Creator YC Interview - Software Engineer Title Disappearing"
date: 2026-02-19
source: https://mp.weixin.qq.com/s/FonqAKISY7Zew6pQbkLWIg
tags: claude-code, anthropic, ai-coding, software-engineering, agent-topology, boris-cherny
---

# Claude Code Creator YC Interview Analysis

## Key Takeaways

### 1. "Software Engineer" Title Disappearing
Boris Cherny (Claude Code founder) predicts the role will evolve to "builder" or "product manager" as coding becomes a default capability rather than a core skill. Engineers will write specs and communicate with users, not just code.

### 2. 150% Productivity Boost at Anthropic
- Anthropic engineers are 70-100% AI-coded
- Per-engineer output increased by **150%** since Claude Code launch
- Boris compares this to Meta where a 2% productivity gain required hundreds of engineers for a year

### 3. Build for "6 Months from Now" Models
Critical advice for LLM founders:
- Don't optimize for today's model limitations
- What's "barely usable" now will be native in 6 months
- Betting against model progress = creating technical debt

### 4. Code Shelf Life: Months
- Claude Code has been rewritten repeatedly
- Code from 6 months ago is almost entirely gone
- Refactoring isn't an exception, it's the norm

### 5. Plan Mode Will Disappear
- It's just a prompt saying "don't write code yet"
- As models improve, this becomes automatic
- Boris: "Maybe in a month I won't need it"

### 6. Latent Demand > Education
- Every Claude Code feature (plan mode, CLAUDE.md, co-work) came from observing what users were already doing
- Productize existing behavior rather than trying to change user habits

### 7. Agent Topologies = Next Frontier
- Multiple agents with "uncorrelated context windows" working in parallel
- Test-time compute + context isolation
- Example: One engineer gave Claude a spec → Claude created Asana tickets, spawned self-assigning agents, built plugins over a weekend with minimal human intervention

## Notable Quotes

> "We are not building products for 'today's model' but for 'models six months from now.'"

> "The biggest capability is beginner mindset: being able to admit you're wrong, discard old experience, and think from first principles."

> "Models want to use tools. They just want to use tools."

> "Build for what models want to do, not what you want them to do."

## Agent Collaboration Patterns

### Multi-Agent Parallel Workflows
- Debug with 3-10 parallel sub-agents: one reads logs, one analyzes code paths
- Research-intensive tasks benefit from multiple agents investigating in parallel
- Spawn sub-agents when task difficulty warrants it

### Uncorrelated Context Windows
- Multiple agents with clean上下文, no contamination from each other's history
- Test-time compute + appropriate topology = ability to build larger, more complex systems

### Self-Organizing Swarms
- Give Claude a spec → it creates tickets → spawns agents → agents self-assign tasks
- Minimal human intervention required once the spec is clear

## CLAUDE.md Best Practices

Boris's CLAUDE.md is only **2 lines**:
1. "Every PR enables automerge; auto-merge when approved"
2. "Post PR to internal stamps channel for quick review"

Key insight: Over-engineering becomes obsolete as models improve. Start minimal, add instructions only when needed.

## Implications for Product Strategy

### What to Build
- Features that emerge from latent user demand
- Scaffolding that will be "free" in next-gen models
- Tools that amplify what users are already doing

### What to Avoid
- Heavy engineering around current model limitations
- Scaffolding that bets against model progress
- Forcing users to change behavior

## Related Developments
- Anthropic raised $30B at $380B valuation (Feb 2026)
- Figma partnered with Anthropic for AI-generated editable designs
- Claude Code expanding into enterprise (India partnerships)
- "Post-Chatbot Era" has begun - agents replacing chat interfaces

## Why This Matters

The terminal survived because it's a universal interface for any tool, language, or workflow. Claude Code demonstrates that:

1. **Interface to code = interface to everything**
2. **Build for model behavior, not user education**
3. **Speed of iteration is the moat** - 20 prototypes/day beats "perfect design"
4. **Code quality is less important than code existence** - AI will rewrite it anyway

## Actions

| Priority | Action |
|----------|--------|
| High | Review product roadmap for "scaffolding" that next-gen models will make obsolete |
| High | Start experimenting with multi-agent parallel workflows (3-10 sub-agents) |
| Medium | Simplify CLAUDE.md and agent instructions |
| Medium | Build for what users *already* do, not what you want them to do |
| Low | Track "babysitting" ratio - how often you need to watch AI output |

## Sources
- [Business Insider: Software Engineer title "going away" in 2026](https://www.businessinsider.com/anthropic-claude-code-founder-ai-impacts-software-engineer-role-2026-2)
- [Axios: Anthropic raises $30B at $380B valuation](https://www.axios.com/2026/02/12/anthropic-raises-30b-at-380b-valuation)
- [CNBC: Figma + Anthropic partnership](https://www.cnbc.com/2026/02/17/figma-anthropic-ai-code-designs.html)
- [The Atlantic: "The Post-Chatbot Era Has Begun"](https://www.theatlantic.com/technology/2026/02/post-chatbot-claude-code-ai-agents/686029/)
