#!/usr/bin/env python3

from pathlib import Path

from scripts.lib.pipeline.run_weekly import run_weekly
from scripts.utils.dates import current_digest_date


def main() -> None:
    skill_root = Path(__file__).resolve().parents[2]
    week_key, markdown = run_weekly(skill_root, current_digest_date())
    print(
        f"frontier-intel weekly run complete: week={week_key} chars={len(markdown)}"
    )


if __name__ == "__main__":
    main()
