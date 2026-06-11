#!/usr/bin/env python3
"""Prepare reusable Vault-learning candidates from an OpenSpec Red Review."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from openspec_review_lib import json_dump, read_text


LEARNING_ROW_RE = re.compile(r"^\|\s*(?P<title>[^|]+)\|\s*(?P<evidence>[^|]+)\|\s*(?P<target>[^|]+)\|", re.MULTILINE)


def extract_vault_section(text: str) -> str:
    match = re.search(r"^##\s+(?:9|10)\.\s+Vault-Learnings\b", text, re.MULTILINE)
    if not match:
        return ""
    start = match.start()
    next_section = text.find("\n## ", match.end())
    return text[start:] if next_section == -1 else text[start:next_section]


def distill(report: Path) -> dict[str, object]:
    text = read_text(report)
    section = extract_vault_section(text)
    candidates = []
    for row in LEARNING_ROW_RE.finditer(section):
        title = row.group("title").strip()
        if title.lower() in {"titel", "---"} or set(title) <= {"-"}:
            continue
        evidence = row.group("evidence").strip()
        target = row.group("target").strip()
        quality_notes = []
        if len(evidence.split()) < 8:
            quality_notes.append("evidence context is short")
        if "/" not in evidence and "/" not in target:
            quality_notes.append("no exact source path detected")
        candidates.append(
            {
                "title": title,
                "evidence": evidence,
                "suggested_target": target,
                "source_report": str(report),
                "writeback_ready": not quality_notes,
                "quality_notes": quality_notes,
            }
        )

    if not candidates:
        reusable_markers = []
        for pattern in (
            "Verify",
            "Evidence Reality Check",
            "runtime-only",
            "trace-only",
            "FIX",
            "DECISION",
            "assumption",
            "Annahme",
        ):
            if pattern.lower() in text.lower():
                reusable_markers.append(pattern)
        return {
            "ok": True,
            "report": str(report),
            "candidates": [],
            "writeback_ready_count": 0,
            "note": "No explicit Vault-learning table rows found.",
            "reusable_markers": reusable_markers,
        }

    return {
        "ok": True,
        "report": str(report),
        "candidates": candidates[:5],
        "writeback_ready_count": sum(1 for item in candidates[:5] if item["writeback_ready"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_path")
    args = parser.parse_args()

    report = Path(args.report_path).expanduser()
    if not report.exists():
        print(json_dump({"ok": False, "error": f"not found: {report}"}))
        return 2
    print(json_dump(distill(report)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
