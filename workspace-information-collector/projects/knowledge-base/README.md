# Knowledge Base

Your curated collection of frontier AI knowledge.

## Structure

```
projects/knowledge-base/
├── ai-models/      # Model releases, benchmarks, capabilities
├── ai-research/    # Papers, breakthroughs, academic work
├── ai-tools/       # New tools, platforms, frameworks
├── ai-industry/    # Company news, funding, deals, trends
└── ai-qa/          # Q&A, explanations, how-tos
```

## Entry Format

**Filename:** `YYYY-MM-DD-slug.md`

**Template:**
```markdown
# [Title]

**Date:** YYYY-MM-DD  
**Source:** [Link](URL)  
**Tags:** #tag1 #tag2

## Key Takeaways
- Point 1
- Point 2
- Point 3

## Why It Matters
One-line context about significance

## Related
- [[other-entry.md]] (if applicable)
```

## Usage

### Adding Entries

When Scout analyzes a link and you say "save this":
1. Scout determines the topic (or asks)
2. Creates the entry file
3. Updates MEMORY.md index
4. Confirms location

### Searching

**Quick search:**
```bash
bash projects/knowledge-base/search.sh "query"
```

**Manual grep:**
```bash
grep -r "multimodal" projects/knowledge-base/ -i -C 3
```

### Listing Topics

Say "show me saved topics" to see all categories with entry counts.

## Tips

- Use descriptive slugs in filenames
- Add relevant tags for cross-topic search
- Link related entries with `[[filename.md]]`
- Keep "Why It Matters" concise (1-2 sentences)

---

Built: 2026-02-19
