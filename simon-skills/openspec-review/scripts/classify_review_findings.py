#!/usr/bin/env python3
"""Summarize FIX/DECISION findings in an OpenSpec Red Review report."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

from openspec_review_lib import json_dump, read_text


FINDING_RE = re.compile(r"^###\s+(?P<id>[A-Za-z0-9_.:-]+)\s*(?P<title>.*)$", re.MULTILINE)
FIELD_RE = re.compile(r"^\s*[-*]?\s*\*?\*?(?P<field>Klasse|Status|Severity|Evidence)\*?\*?\s*:\s*(?P<value>.+)$", re.MULTILINE)


def classify(report: Path) -> dict[str, object]:
    text = read_text(report)
    matches = list(FINDING_RE.finditer(text))
    findings = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start() : end]
        fields = {m.group("field").lower(): m.group("value").strip() for m in FIELD_RE.finditer(block)}
        findings.append(
            {
                "id": match.group("id"),
                "title": match.group("title").strip(),
                "class": fields.get("klasse"),
                "status": fields.get("status"),
                "severity": fields.get("severity"),
                "evidence": fields.get("evidence"),
                "missing_fields": [
                    name for name in ("klasse", "status", "severity", "evidence") if not fields.get(name)
                ],
            }
        )

    classes = Counter((item.get("class") or "MISSING").split()[0].strip("`") for item in findings)
    severities = Counter((item.get("severity") or "MISSING").split()[0].strip("`") for item in findings)
    return {
        "ok": True,
        "report": str(report),
        "finding_count": len(findings),
        "class_counts": dict(classes),
        "severity_counts": dict(severities),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_path")
    args = parser.parse_args()

    report = Path(args.report_path).expanduser()
    if not report.exists():
        print(json_dump({"ok": False, "error": f"not found: {report}"}))
        return 2
    print(json_dump(classify(report)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
