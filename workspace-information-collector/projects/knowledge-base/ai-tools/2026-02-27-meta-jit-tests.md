# Meta JiTTests: Just-in-Time Testing for Agentic Development

**Date:** 2026-02-27  
**Source:** [Engineering at Meta](https://engineering.fb.com/2026/02/11/developer-tools/the-death-of-traditional-testing-agentic-development-jit-testing-revival/)  
**Tags:** testing, meta, llm, agentic-development, dev-tools

## Key Takeaways

- **JiTTests (Just-in-Time Tests)** are LLM-generated regression tests created on-the-fly for each pull request
- **Problem:** Agentic dev moves faster than traditional test suites can handle — maintenance overhead and false positives are becoming unsustainable
- **Solution:** Instead of static test suites, LLMs infer code intent, generate mutants (faulty versions), create tests to catch those mutants, and filter false positives using rule-based + LLM assessors
- **Key benefits:** No test maintenance, no test code review needed, engineers only see alerts when a real bug is caught

## How It Works

1. New code lands in codebase
2. System infers intention of the change
3. Creates "mutants" (code with deliberate faults)
4. Generates and runs tests to catch those faults
5. Ensemble of assessors filters false positives
6. Engineers get actionable bug reports

## Why It Matters

- Shifts testing focus from generic code quality → specific fault detection per change
- Complements (doesn't replace) traditional test suites
- Enables testing to keep pace with AI-powered coding agents

## Paper

[Just-in-Time Catching Test Generation at Meta](https://arxiv.org/pdf/2601.22832) — Full technical paper on arXiv

## Related

- [mgks.dev: Just-in-Time Tests for Agentic Era](https://mgks.dev/blog/2026-02-21-just-in-time-tests-how-meta-is-rethinking-software-testing-for-the-agentic-era/)
