---
name: tavily-search
description: Web search using Tavily API with summarization. Activate when the user asks you to search the web, find information online, look up something on the internet, or needs current/real-time information. Uses Tavily's search API with the provided API key and returns summarized results.
---

# Tavily Search Skill

## When to Use

Trigger this skill when the user asks you to:
- Search the web
- Find information online
- Look something up
- Research a topic
- Find current/recent information

## Setup

The Tavily API key is stored in the environment variable `TAVILY_API_KEY`. For development/testing, you can also use the preview key format.

## Usage

### Direct Search

When user requests a search, use the `scripts/tavily_search.py` script:

```bash
python scripts/tavily_search.py "search query"
```

The script returns JSON with search results. Parse and summarize the key findings.

### Response Format

Always provide:
1. **Summary** - A concise synthesis of the search results (2-4 sentences)
2. **Key Findings** - 3-5 bullet points of the most relevant information
3. **Sources** - Include the top 2-3 source URLs for reference

### Example Response Structure

```
[Summary of findings]

**Key Findings:**
- Finding 1
- Finding 2
- Finding 3

**Sources:**
- [Title](URL)
- [Title](URL)
```

## Script Details

The `scripts/tavily_search.py` script:
- Accepts a search query as argument
- Makes API call to Tavily Search API
- Returns JSON with results including URLs, titles, and content
- Handles errors gracefully

## Notes

- Always verify the API key is set before running searches
- For complex queries, consider breaking into multiple focused searches
- Prioritize recent and authoritative sources
