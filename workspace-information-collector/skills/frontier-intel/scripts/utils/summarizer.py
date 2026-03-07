from __future__ import annotations

import json
import re
import shutil
import subprocess

from scripts.utils.command import run_command
from scripts.utils.text import concise_summary

SHARED_SUMMARY_SCRIPT = "/root/.openclaw/skills/frontier-summary/scripts/summarize_item.py"
HTML_TAGS = re.compile(r"<[^>]+>")
SCRIPT_STYLE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL)
SPACE = re.compile(r"\s+")


class Summarizer:
    def __init__(self, binary: str = "summarize") -> None:
        self.binary = binary
        self.binary_path = shutil.which(binary)

    @property
    def available(self) -> bool:
        return self.binary_path is not None

    def summarize_url(self, url: str, *, item_type: str = "news", fallback_title: str = "", fallback_text: str = "") -> str:
        if self.available and url:
            command = [
                self.binary_path,
                url,
                "--length",
                "short",
                "--max-output-tokens",
                "220",
                "--json",
            ]
            result = run_command(command, timeout=120)
            if result.ok:
                return self._parse_summary_output(result.stdout, fallback_title, fallback_text)
        return self.summarize_text(item_type=item_type, title=fallback_title, text=fallback_text)

    def summarize_text(self, *, item_type: str, title: str, text: str) -> str:
        cleaned_text = self.clean_source_text(text)
        payload = json.dumps({"type": item_type, "title": title, "text": cleaned_text})
        try:
            completed = subprocess.run(
                ["python3", SHARED_SUMMARY_SCRIPT],
                input=payload,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            if completed.returncode == 0 and completed.stdout.strip():
                parsed = json.loads(completed.stdout)
                summary = parsed.get("summary", "").strip()
                if summary:
                    return summary
        except Exception:
            pass
        return concise_summary(title=title, text=cleaned_text)

    def clean_source_text(self, text: str) -> str:
        text = SCRIPT_STYLE.sub(" ", text or "")
        text = HTML_TAGS.sub(" ", text)
        text = SPACE.sub(" ", text).strip()
        return text[:12000]

    def _parse_summary_output(self, output: str, fallback_title: str, fallback_text: str) -> str:
        try:
            payload = json.loads(output)
        except json.JSONDecodeError:
            return concise_summary(title=fallback_title, text=output or fallback_text)
        summary = (
            payload.get("summary")
            or payload.get("text")
            or payload.get("output")
            or payload.get("answer")
            or ""
        )
        if not summary:
            return concise_summary(title=fallback_title, text=fallback_text)
        return concise_summary(title=fallback_title, text=summary)
