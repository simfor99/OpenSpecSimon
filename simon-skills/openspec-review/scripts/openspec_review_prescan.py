#!/usr/bin/env python3
"""Structural pre-scan for an OpenSpec review target."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from openspec_review_lib import inventory_for_change, is_change_dir, json_dump, markdown_files, read_text


MARKERS = {
    "decision_marker": re.compile(r"\b(entscheidung|decision|option [abc]|scope decision|owner)\b", re.IGNORECASE),
    "blocked_marker": re.compile(r"\b(blocked|blocker|nicht archivieren|stop-regel|stop rule)\b", re.IGNORECASE),
    "assumption_marker": re.compile(r"\b(assumption|annahme|assumed|vermutet|nicht verifiziert)\b", re.IGNORECASE),
    "runtime_claim": re.compile(r"\b(runtime validated|runtime_validated|production|live|api-test|browser-test|trace)\b", re.IGNORECASE),
    "weak_evidence": re.compile(
        r"\b(console output|manuell geprüft|smoke only|fixture only|fixture-only|fixtures only|parser-only|artifact replay)\b",
        re.IGNORECASE,
    ),
}


def marker_hits(change_dir: Path) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in markdown_files(change_dir):
        text = read_text(path)
        for marker, pattern in MARKERS.items():
            for match in pattern.finditer(text):
                line_no = text[: match.start()].count("\n") + 1
                hits.append(
                    {
                        "marker": marker,
                        "file": str(path.relative_to(change_dir)),
                        "line": str(line_no),
                        "snippet": text[match.start() : match.start() + 120].replace("\n", " "),
                    }
                )
                break
    return hits


def pre_scan(change_dir: Path) -> dict[str, object]:
    inv = inventory_for_change(change_dir)
    findings: list[dict[str, object]] = []
    artifacts = inv["artifacts"]
    task_counts = inv["task_counts"]

    if not artifacts["tasks"]:
        findings.append(
            {
                "id": "PRESCAN-001",
                "severity": "HIGH",
                "class_hint": "DECISION",
                "title": "tasks.md fehlt",
                "why_it_matters": "Verify kann ohne Aufgabenliste keinen vollstaendigen Task-Abgleich behaupten.",
            }
        )
    elif task_counts["open"] > 0:
        findings.append(
            {
                "id": "PRESCAN-002",
                "severity": "HIGH",
                "class_hint": "FIX_OR_DECISION",
                "title": "Offene Tasks gefunden",
                "task_counts": task_counts,
                "why_it_matters": "Offene Aufgaben koennen echte Restarbeit oder veraltete Task-Hygiene sein.",
            }
        )

    if not artifacts["verification"]:
        findings.append(
            {
                "id": "PRESCAN-003",
                "severity": "MEDIUM",
                "class_hint": "DECISION",
                "title": "Kein Verify-Artefakt gefunden",
                "why_it_matters": "Der Review darf dann nur als Early-Paranoia laufen, nicht als Post-Verify-Freigabe.",
            }
        )

    if not artifacts["red_reviews"]:
        findings.append(
            {
                "id": "PRESCAN-004",
                "severity": "LOW",
                "class_hint": "FIX",
                "title": "Noch kein OpenSpec Red Review gefunden",
                "why_it_matters": "Erwartet beim ersten Lauf; Report wird unter 00-OPENSPEC-RED-REVIEW.md geschrieben.",
            }
        )

    if artifacts["delta_specs"] and not artifacts["design"]:
        findings.append(
            {
                "id": "PRESCAN-005",
                "severity": "MEDIUM",
                "class_hint": "DECISION",
                "title": "Delta-Specs ohne design.md",
                "why_it_matters": "Komplexe Spec-Aenderungen ohne Design koennen verdeckte Architekturannahmen enthalten.",
            }
        )

    hits = marker_hits(change_dir)
    return {
        "ok": True,
        "change": inv,
        "prescan_findings": findings,
        "marker_hits": hits[:80],
        "marker_hit_count": len(hits),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change_dir", help="OpenSpec change directory")
    args = parser.parse_args()

    change_dir = Path(args.change_dir).expanduser()
    if not change_dir.exists() or not is_change_dir(change_dir):
        print(json_dump({"ok": False, "error": f"not an OpenSpec change directory: {change_dir}"}))
        return 2
    print(json_dump(pre_scan(change_dir)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
