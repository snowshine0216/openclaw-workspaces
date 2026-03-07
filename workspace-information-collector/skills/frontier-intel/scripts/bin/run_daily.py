#!/usr/bin/env python3

from pathlib import Path

from scripts.lib.pipeline.run_daily import run_daily


def main() -> None:
    skill_root = Path(__file__).resolve().parents[2]
    digest_date, items, target = run_daily(skill_root)
    print(
        f"frontier-intel daily run complete: date={digest_date} items={len(items)} output={target}"
    )


if __name__ == "__main__":
    main()
