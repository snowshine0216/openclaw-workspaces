# AI Agent Testing: Dev to Production

**Date:** 2026-02-21  
**Source:** https://medium.com/@v31u/your-ai-agent-works-in-dev-why-does-it-fail-in-production-e591adfe6518  
**Author:** @v31u  
**Tags:** ai-agents, testing, production, devops, llm

---

## Key Takeaways

1. **Mock LLMs in unit tests** — Real API calls are slow, costly, and non-deterministic
2. **4 categories of test data** — Happy path, edge cases, error cases, adversarial
3. **LLM-as-judge replaces human eval** — Scales evaluation without burning human time
4. **Consistency testing = embedding similarity** — Detects non-determinism (min_similarity > 0.8 = stable)
5. **Metrics beyond pass/fail** — completion rate, p95 latency, error rate
6. **A/B test with p-value < 0.05** — Data-driven decisions
7. **Production monitoring with deviation alerts** — Catch regressions early

## Why It Matters

Traditional software testing doesn't apply to AI agents because:
- Non-deterministic outputs
- External LLM dependencies (slow, expensive)
- Complex reasoning chains
- Tool orchestration complexity

## Actions to Take

| Priority | Action | How |
|----------|--------|-----|
| P0 | Mock LLM in test suite | Use `unittest.mock.AsyncMock` |
| P0 | Build test dataset (4 categories) | 10 cases per category |
| P1 | Add LLM-as-judge eval | GPT-4o with temp=0 |
| P1 | Track metrics | Implement `AgentMetrics` dataclass |
| P2 | Set up CI/CD gate | Fail if eval score < 0.8 |
| P2 | A/B test prompts/models | Statistical significance check |

## Related

- [State of AI Agents 2026 (Databricks)](https://lovelytics.com/post/state-of-ai-agents-2026-lessons-on-governance-evaluation-and-scale/)
- [Agent Testing Complete Guide](https://www.openlayer.com/blog/post/agent-testing-complete-guide-validating-ai-systems)
- [GitHub Repo](https://github.com/ksankaran/ai-agent-testing)
