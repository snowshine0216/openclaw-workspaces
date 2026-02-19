#!/bin/bash
# Knowledge Base Search Script

if [ -z "$1" ]; then
    echo "Usage: bash search.sh \"query\""
    exit 1
fi

echo "Searching knowledge base for: $1"
echo "---"

grep -r "$1" projects/knowledge-base/*/*.md -i -C 3 --color=always 2>/dev/null

if [ $? -ne 0 ]; then
    echo "No results found."
fi
