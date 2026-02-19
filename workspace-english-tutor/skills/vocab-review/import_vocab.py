#!/usr/bin/env python3
"""
Import vocabulary from Excel files to vocab.json
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
VOCAB_FILE = SCRIPT_DIR / "vocab.json"

EXCEL_FILES = [
    "/root/uploads/kw_cookbook_20260102_043807.xlsx",
    "/root/uploads/kw2_cookbook_20260103_083155.xlsx",
    "/root/uploads/kw3_cookbook_20260117_091729.xlsx",
]

def load_existing_vocab():
    """Load existing vocab.json or create new structure."""
    if VOCAB_FILE.exists():
        with open(VOCAB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "items": [],
        "config": {
            "items_per_review": 20,
            "timezone": "Asia/Shanghai",
            "review_time": "20:00",
            "feishu_chat_id": "oc_55bf80b97398600ff6da478ae62937de"
        }
    }

def get_next_id(items):
    """Get the next available ID."""
    if not items:
        return 1
    return max(item.get("id", 0) for item in items) + 1

def import_excel(file_path, items, next_id):
    """Import vocabulary from an Excel file."""
    df = pd.read_excel(file_path)
    
    imported = 0
    for _, row in df.iterrows():
        word = row.get("word", "")
        if not word or pd.isna(word):
            continue
            
        # Check if word already exists
        if any(item.get("content", "").lower() == str(word).lower() for item in items):
            continue
        
        item = {
            "id": next_id,
            "type": "phrase" if " " in str(word) else "word",
            "content": str(word),
            "ipa": str(row.get("ipa", "")) if pd.notna(row.get("ipa", "")) else "",
            "english": str(row.get("definition", "")) if pd.notna(row.get("definition", "")) else "",
            "chinese": str(row.get("definition_zh", "")) if pd.notna(row.get("definition_zh", "")) else "",
            "original_context": str(row.get("original_context", "")) if pd.notna(row.get("original_context", "")) else "",
            "example": str(row.get("generated_use_case", "")) if pd.notna(row.get("generated_use_case", "")) else "",
            "synonyms": [],
            "memory_trick": "",
            "added_date": datetime.now().strftime("%Y-%m-%d"),
            "review_count": 0,
            "last_reviewed": None,
            "status": "learning"
        }
        
        items.append(item)
        next_id += 1
        imported += 1
    
    return imported, next_id

def main():
    print("=" * 50)
    print("📥 Importing Vocabulary from Excel")
    print("=" * 50)
    
    data = load_existing_vocab()
    items = data["items"]
    next_id = get_next_id(items)
    
    print(f"[INFO] Starting with {len(items)} existing items")
    
    total_imported = 0
    for file_path in EXCEL_FILES:
        print(f"\n[INFO] Processing: {file_path.split('/')[-1]}")
        imported, next_id = import_excel(file_path, items, next_id)
        print(f"[INFO] Imported {imported} items")
        total_imported += imported
    
    data["items"] = items
    
    with open(VOCAB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 50}")
    print(f"✅ Total imported: {total_imported}")
    print(f"📚 Total vocabulary: {len(items)}")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    main()
