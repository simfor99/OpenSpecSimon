#!/usr/bin/env python3
"""Validate the OpenSpec Red Review report contract."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from openspec_review_lib import json_dump, read_text


REQUIRED_SECTIONS = [
    "## 0. Zusammenfassung für Simon",
    "## 1. Abschlussentscheidung, die dieser Review vorbereitet",
    "## 2. Was behauptet wurde",
    "## 3. Was Red geprüft hat",
    "## 4. Systemverständnis und Must-Survive-Facts",
    "## 5. Übersehene Komplexität und falsche Annahmen",
    "## 6. Findings",
    "## 7. Evidence Reality Check",
    "## 8. Stop-Regeln",
    "## 9. Zurückzuschreiben nach",
    "## 10. Vault-Learnings",
]
VERDICTS = {"APPROVED", "APPROVED_WITH_NOTES", "BLOCKED", "PAUSED_FOR_DECISION"}
PLACEHOLDER_RE = re.compile(r"({{[^}]+}}|<[^>\n]+>|\bTBD\b|\bTODO\b)")
FINDING_RE = re.compile(r"^###\s+(?P<id>[A-Za-z0-9_.:-]+)\s*(?P<title>.*)$", re.MULTILINE)
FIELD_RE = re.compile(r"^\s*[-*]?\s*\*?\*?(?P<field>Klasse|Status|Severity|Evidence)\*?\*?\s*:\s*(?P<value>.+)$", re.MULTILINE)


def extract_section(text: str, section: str) -> str:
    start = text.find(section)
    if start == -1:
        return ""
    next_section = re.search(r"^##\s+\d+\.", text[start + len(section) :], re.MULTILINE)
    end = start + len(section) + next_section.start() if next_section else len(text)
    return text[start:end]


def validate(report: Path) -> dict[str, object]:
    text = read_text(report)
    errors: list[str] = []
    warnings: list[str] = []

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing required section: {section}")

    verdicts_found = sorted(verdict for verdict in VERDICTS if re.search(rf"\b{verdict}\b", text))
    if not verdicts_found:
        errors.append("missing required verdict")

    placeholders = [match.group(0) for match in PLACEHOLDER_RE.finditer(text)]
    if placeholders:
        errors.append(f"unresolved placeholders found: {sorted(set(placeholders))[:10]}")

    system_map = extract_section(text, "## 4. Systemverständnis und Must-Survive-Facts")
    if system_map:
        if not re.search(r"Must-Survive-Fact|Must-Survive-Facts", system_map, re.I):
            errors.append("system map section must mention Must-Survive-Facts")
        coverage_match = re.search(r"Coverage(?: Gate)?\s*:\s*`?(yes|partial|no)`?", system_map, re.I)
        if not coverage_match:
            errors.append("system map section must include Coverage Gate: yes|partial|no")
        elif coverage_match.group(1).lower() in {"partial", "no"}:
            if verdicts_found == ["APPROVED"]:
                errors.append("plain APPROVED is invalid when Coverage Gate is partial or no")
        if re.search(r"Ziel-Weg-Fitness|minimum sufficient path|selected path", system_map, re.I):
            if not re.search(r"A/B status\s*:\s*`?(required|recommended|not_needed|bypassed)`?", system_map, re.I):
                errors.append("Ziel-Weg-Fitness system map must include A/B status")

    matches = list(FINDING_RE.finditer(text))
    if not matches:
        warnings.append("no findings found")

    finding_errors: list[dict[str, object]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start() : end]
        fields = {m.group("field").lower(): m.group("value").strip() for m in FIELD_RE.finditer(block)}
        missing = [name for name in ("klasse", "status", "severity", "evidence") if not fields.get(name)]
        klasse = fields.get("klasse", "")
        if missing:
            finding_errors.append({"id": match.group("id"), "missing_fields": missing})
        if "DECISION" in klasse.upper():
            option_count = len(re.findall(r"\bOption\s+[A-Z]\b", block))
            has_recommendation = bool(re.search(r"(Red recommendation|Red-Empfehlung|Empfehlung)", block, re.I))
            has_not_changed = bool(re.search(r"(nicht geaendert|nicht geändert|not changed)", block, re.I))
            decision_errors = []
            if option_count < 2:
                decision_errors.append("DECISION finding needs at least two options")
            if not has_recommendation:
                decision_errors.append("DECISION finding needs a Red recommendation")
            if not has_not_changed:
                decision_errors.append("DECISION finding needs explicit not-changed statement")
            if decision_errors:
                finding_errors.append({"id": match.group("id"), "decision_errors": decision_errors})

    if finding_errors:
        errors.append("finding contract errors")

    return {
        "ok": not errors,
        "report": str(report),
        "errors": errors,
        "warnings": warnings,
        "verdicts_found": verdicts_found,
        "finding_count": len(matches),
        "finding_errors": finding_errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_path")
    args = parser.parse_args()

    report = Path(args.report_path).expanduser()
    if not report.exists():
        print(json_dump({"ok": False, "errors": [f"not found: {report}"], "warnings": []}))
        return 2
    result = validate(report)
    print(json_dump(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
