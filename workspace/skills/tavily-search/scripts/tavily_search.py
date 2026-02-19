#!/usr/bin/env python3
"""
Tavily Search Script

Searches the web using Tavily's Search API and returns results in JSON format.

Usage:
    python scripts/tavily_search.py "search query"

Environment Variables:
    TAVILY_API_KEY - Your Tavily API key (required)
"""

import os
import sys
import json
import argparse

try:
    import requests
except ImportError:
    print(json.dumps({"error": "requests library not installed. Install with: pip install requests"}))
    sys.exit(1)


def search_tavily(query: str, api_key: str = None) -> dict:
    """
    Perform a search using Tavily Search API.
    
    Args:
        query: The search query
        api_key: Tavily API key (optional, uses env var if not provided)
    
    Returns:
        Dictionary containing search results
    """
    # Get API key from environment if not provided
    if not api_key:
        api_key = os.environ.get("TAVILY_API_KEY")
    
    # Check for dev/test key pattern
    if not api_key and "TAVILY_API_KEY" not in os.environ:
        # Try using the dev key if it was passed directly
        api_key = "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"
    
    if not api_key:
        return {"error": "No Tavily API key provided. Set TAVILY_API_KEY environment variable."}
    
    # Tavily Search API endpoint
    url = "https://api.tavily.com/search"
    
    payload = {
        "query": query,
        "search_depth": "basic",
        "max_results": 10,
        "include_answer": True,
        "include_raw_content": False,
        "include_images": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def format_results(results: dict) -> str:
    """Format search results for output."""
    if "error" in results:
        return json.dumps(results)
    
    output = {
        "query": results.get("query", ""),
        "answer": results.get("answer", ""),
        "results": []
    }
    
    for item in results.get("results", []):
        output["results"].append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", "")[:500] if item.get("content") else "",  # Truncate content
            "score": item.get("score", 0)
        })
    
    return json.dumps(output, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Search the web using Tavily API"
    )
    parser.add_argument(
        "query",
        help="The search query"
    )
    parser.add_argument(
        "--api-key",
        "-k",
        help="Tavily API key (optional, uses TAVILY_API_KEY env var)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON"
    )
    
    args = parser.parse_args()
    
    results = search_tavily(args.query, args.api_key)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results))


if __name__ == "__main__":
    main()
