#!/usr/bin/env python3
"""Lint Sanctum OpenSpec meta-artifacts.

This is a deterministic structure checker. It does not decide whether a gate,
ledger row, or builder-plan task is fachlich correct.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import yaml


MODES = {"propose", "apply", "verify", "archive"}
SEVERITIES = {"CRITICAL", "WARNING", "SUGGESTION"}
GATE_STATUSES = {
    "candidate",
    "needs_research",
    "clarify_first",
    "planned",
    "in_progress",
    "passed",
    "not_applicable_with_reason",
    "deferred_with_accepted_decision",
    "missing_evidence",
    "failed",
    "blocked",
}
FINAL_GATE_STATUSES = {
    "passed",
    "not_applicable_with_reason",
    "deferred_with_accepted_decision",
}
GATE_BLOCKS = {"apply", "verify", "review", "archive"}
GATE_REQUIRED_FIELDS = {
    "gate_id",
    "title",
    "origin",
    "applies_when",
    "severity",
    "status",
    "required_actions",
    "required_evidence",
    "blocks",
    "allowed_final_statuses",
    "decision_escape_hatch",
    "evidence",
}
CLAIM_CLASSES = {
    "ui_visibility",
    "browser_entry",
    "api_entry",
    "persistence_write",
    "status_transition",
    "workflow_success",
    "bounded_stage_run",
    "dataflow_handoff",
    "llm_output_contract",
    "trace_generation",
    "trace_visibility",
    "current_run",
    "historical_match",
    "resume_from_existing",
    "runtime_config",
}
LEDGER_FINAL_STATUSES = {
    "updated",
    "moved",
    "deleted",
    "created",
    "reviewed_unaffected",
    "not_impacted",
    "deferred_with_reason",
    "blocked",
}
LEDGER_EARLY_STATUSES = {"todo", "in_progress"}
BUILDER_REQUIRED_SECTIONS = [
    "Goal",
    "Contract sources",
    "File structure",
    "OpenSpec task map",
    "TDD / evidence tasks",
    "Contract-fidelity checks",
    "Shadow workbench and cutover",
    "Self-review",
]
TASK_REQUIRED_HINTS = [
    r"OpenSpec link",
    r"Source contract",
    r"Files to (inspect|create|update|create or update|inspect/update|inspect/use)",
    r"(Expected failing result|Red/evidence-before-change command|no_test)",
    r"Minimal implementation target",
    r"Passing verification",
    r"Ledger/gate evidence",
]
HIGH_RISK_BUILDER_PATTERNS = [
    r"\bbrowser\b",
    r"\buser-visible\b",
    r"\bfrontdoor\b",
    r"\bAPI route\b",
    r"\broute registry\b",
    r"\bSupabase\b",
    r"\bdatabase\b",
    r"\bpersistence\b",
    r"\bexternal side[- ]effect\b",
    r"\btrace\b",
    r"\bruntime\b",
    r"\bhandoff\b",
    r"\bauth\b",
    r"\bqueue\b",
    r"\bwebhook\b",
    r"\bstorage\b",
    r"\bmigration\b",
    r"\bschema\b",
]


@dataclass
class Finding:
    severity: str
    artifact: str
    code: str
    message: str
    blocking: bool


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_markdown_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`]*`", "", text)


def add(
    findings: list[Finding],
    *,
    severity: str,
    artifact: str,
    code: str,
    message: str,
    blocking: bool,
) -> None:
    findings.append(Finding(severity, artifact, code, message, blocking))


def yaml_blocks(markdown: str) -> list[str]:
    return re.findall(r"```yaml\s*\n(.*?)\n```", markdown, flags=re.S)


def ensure_list(value: Any) -> bool:
    return isinstance(value, list) and all(item is not None for item in value)


def high_risk_builder_context(change_dir: Path) -> bool:
    markdown = "\n".join(read_text(path) for path in change_dir.glob("*.md") if path.is_file())
    return any(re.search(pattern, markdown, flags=re.I) for pattern in HIGH_RISK_BUILDER_PATTERNS)


def lint_quality_gates(change_dir: Path, mode: str, findings: list[Finding]) -> None:
    path = change_dir / "quality-gates.md"
    if not path.exists():
        return
    text = read_text(path)
    blocks = yaml_blocks(text)
    if not blocks:
        add(
            findings,
            severity="ERROR",
            artifact="quality-gates.md",
            code="gate.no_yaml_blocks",
            message="quality-gates.md exists but contains no yaml gate blocks.",
            blocking=True,
        )
        return

    seen_ids: set[str] = set()
    for index, block in enumerate(blocks, start=1):
        try:
            data = yaml.safe_load(block)
        except Exception as exc:  # noqa: BLE001 - command-line diagnostic
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.yaml_parse_error",
                message=f"Gate block {index} does not parse as YAML: {exc}",
                blocking=True,
            )
            continue

        if not isinstance(data, dict):
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.not_mapping",
                message=f"Gate block {index} must be a YAML mapping.",
                blocking=True,
            )
            continue

        gate_id = str(data.get("gate_id") or f"block-{index}")
        missing = sorted(GATE_REQUIRED_FIELDS - set(data))
        if missing:
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.missing_fields",
                message=f"{gate_id} misses required fields: {', '.join(missing)}.",
                blocking=True,
            )

        if gate_id in seen_ids:
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.duplicate_id",
                message=f"Duplicate gate_id: {gate_id}.",
                blocking=True,
            )
        seen_ids.add(gate_id)

        severity = data.get("severity")
        if severity not in SEVERITIES:
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.invalid_severity",
                message=f"{gate_id} has invalid severity {severity!r}.",
                blocking=True,
            )

        status = data.get("status")
        if status not in GATE_STATUSES:
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.invalid_status",
                message=f"{gate_id} has invalid status {status!r}.",
                blocking=True,
            )
        elif mode in {"verify", "archive"} and status not in FINAL_GATE_STATUSES:
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.open_in_late_mode",
                message=f"{gate_id} has status {status!r}; {mode} mode requires a final status.",
                blocking=True,
            )
        elif mode in {"propose", "apply"} and status in {"planned", "in_progress"}:
            add(
                findings,
                severity="INFO",
                artifact="quality-gates.md",
                code="gate.open_allowed_early",
                message=f"{gate_id} is {status!r}; this is allowed in {mode} mode.",
                blocking=False,
            )
        elif mode == "apply" and status in {"candidate", "needs_research", "clarify_first"}:
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.not_apply_ready",
                message=f"{gate_id} has status {status!r}; Apply needs a materialized gate or accepted decision.",
                blocking=True,
            )

        blocks_value = data.get("blocks", [])
        if not ensure_list(blocks_value) or any(item not in GATE_BLOCKS for item in blocks_value):
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.invalid_blocks",
                message=f"{gate_id} has invalid blocks list.",
                blocking=True,
            )

        for list_field in ("applies_when", "required_actions", "required_evidence", "allowed_final_statuses"):
            if list_field in data and not ensure_list(data[list_field]):
                add(
                    findings,
                    severity="ERROR",
                    artifact="quality-gates.md",
                    code=f"gate.invalid_{list_field}",
                    message=f"{gate_id}.{list_field} must be a non-null list.",
                    blocking=True,
                )

        allowed_final = set(data.get("allowed_final_statuses") or [])
        if allowed_final and not allowed_final.issubset(FINAL_GATE_STATUSES):
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.invalid_allowed_final_statuses",
                message=f"{gate_id} has invalid allowed final statuses: {sorted(allowed_final - FINAL_GATE_STATUSES)}.",
                blocking=True,
            )

        if "origin" in data and not isinstance(data["origin"], dict):
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.invalid_origin",
                message=f"{gate_id}.origin must be a mapping.",
                blocking=True,
            )
        if "decision_escape_hatch" in data and not isinstance(data["decision_escape_hatch"], dict):
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.invalid_decision_escape_hatch",
                message=f"{gate_id}.decision_escape_hatch must be a mapping.",
                blocking=True,
            )
        if "evidence" in data and not isinstance(data["evidence"], dict):
            add(
                findings,
                severity="ERROR",
                artifact="quality-gates.md",
                code="gate.invalid_evidence",
                message=f"{gate_id}.evidence must be a mapping.",
                blocking=True,
            )
        if "claim_integrity" in data:
            claim_integrity = data["claim_integrity"]
            if not isinstance(claim_integrity, dict):
                add(
                    findings,
                    severity="ERROR",
                    artifact="quality-gates.md",
                    code="gate.invalid_claim_integrity",
                    message=f"{gate_id}.claim_integrity must be a mapping.",
                    blocking=True,
                )
            else:
                claim_classes = claim_integrity.get("claim_classes")
                subject_ids = claim_integrity.get("subject_ids")
                not_proven = claim_integrity.get("not_proven")
                if not ensure_list(claim_classes):
                    add(
                        findings,
                        severity="ERROR",
                        artifact="quality-gates.md",
                        code="gate.invalid_claim_classes",
                        message=f"{gate_id}.claim_integrity.claim_classes must be a non-null list.",
                        blocking=True,
                    )
                else:
                    invalid = sorted({str(item) for item in claim_classes if str(item) not in CLAIM_CLASSES})
                    if invalid:
                        add(
                            findings,
                            severity="ERROR",
                            artifact="quality-gates.md",
                            code="gate.unknown_claim_classes",
                            message=f"{gate_id}.claim_integrity.claim_classes contains unknown values: {invalid}.",
                            blocking=True,
                        )
                if not ensure_list(subject_ids):
                    add(
                        findings,
                        severity="ERROR",
                        artifact="quality-gates.md",
                        code="gate.invalid_claim_subject_ids",
                        message=f"{gate_id}.claim_integrity.subject_ids must be a non-null list.",
                        blocking=True,
                    )
                if not ensure_list(not_proven):
                    add(
                        findings,
                        severity="ERROR",
                        artifact="quality-gates.md",
                        code="gate.invalid_claim_not_proven",
                        message=f"{gate_id}.claim_integrity.not_proven must be a non-null list.",
                        blocking=True,
                    )


def parse_markdown_tables(text: str) -> list[list[list[str]]]:
    tables: list[list[list[str]]] = []
    current: list[list[str]] = []
    for line in text.splitlines():
        if line.strip().startswith("|") and line.strip().endswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            current.append(cells)
        else:
            if current:
                tables.append(current)
                current = []
    if current:
        tables.append(current)
    return tables


def lint_ledger(change_dir: Path, mode: str, findings: list[Finding]) -> None:
    path = change_dir / "implementation-ledger.md"
    if not path.exists():
        return
    text = read_text(path)
    tables = parse_markdown_tables(text)
    ledger_table: list[list[str]] | None = None
    for table in tables:
        if table and "Status" in table[0] and "Target" in table[0]:
            ledger_table = table
            break
    if not ledger_table or len(ledger_table) < 3:
        add(
            findings,
            severity="ERROR",
            artifact="implementation-ledger.md",
            code="ledger.table_missing",
            message="No ledger table with Target and Status columns found.",
            blocking=True,
        )
        return

    header = ledger_table[0]
    status_index = header.index("Status")
    target_index = header.index("Target")
    evidence_index = None
    for name in ("Evidence / note", "Evidence", "Note"):
        if name in header:
            evidence_index = header.index(name)
            break

    concrete_file_rows = 0
    parent_folder_rows = 0
    for row_number, row in enumerate(ledger_table[2:], start=1):
        if len(row) <= max(status_index, target_index):
            continue
        target = row[target_index].strip("` ")
        status = row[status_index].strip("` ")
        evidence = row[evidence_index] if evidence_index is not None and len(row) > evidence_index else ""

        if not target or set(target) <= {"-"}:
            continue

        if target.endswith("/") or target.endswith("/`"):
            parent_folder_rows += 1
        elif re.search(r"\.[A-Za-z0-9]+$", target):
            concrete_file_rows += 1

        if status in LEDGER_EARLY_STATUSES:
            if mode in {"verify", "archive"}:
                add(
                    findings,
                    severity="ERROR",
                    artifact="implementation-ledger.md",
                    code="ledger.open_in_late_mode",
                    message=f"Ledger row {row_number} for {target} is {status!r}; {mode} mode requires a final status.",
                    blocking=True,
                )
            continue

        if status not in LEDGER_FINAL_STATUSES:
            add(
                findings,
                severity="ERROR",
                artifact="implementation-ledger.md",
                code="ledger.invalid_status",
                message=f"Ledger row {row_number} for {target} has invalid status {status!r}.",
                blocking=True,
            )
            continue

        if not evidence.strip():
            add(
                findings,
                severity="ERROR",
                artifact="implementation-ledger.md",
                code="ledger.missing_evidence",
                message=f"Ledger row {row_number} for {target} has final status without evidence.",
                blocking=True,
            )
        if status == "reviewed_unaffected" and not re.search(r"review|read|checked|gelesen|geprüft|quelle", evidence, re.I):
            add(
                findings,
                severity="WARNING",
                artifact="implementation-ledger.md",
                code="ledger.weak_reviewed_unaffected",
                message=f"Ledger row {row_number} for {target} is reviewed_unaffected without clear source-reading evidence.",
                blocking=False,
            )

    if parent_folder_rows and concrete_file_rows == 0:
        add(
            findings,
            severity="WARNING",
            artifact="implementation-ledger.md",
            code="ledger.parent_only_scope",
            message="Ledger has parent-folder rows but no concrete file rows; file-heavy scope may be under-specified.",
            blocking=False,
        )


def lint_builder_plan(change_dir: Path, mode: str, findings: list[Finding]) -> None:
    path = change_dir / "builder-plan.md"
    if not path.exists():
        return
    text = read_text(path)
    high_risk = high_risk_builder_context(change_dir)
    strict_builder_mode = high_risk and mode in {"apply", "verify", "archive"}
    section_titles = set(re.findall(r"^##\s+(.+?)\s*$", text, flags=re.M))
    for section in BUILDER_REQUIRED_SECTIONS:
        if section not in section_titles:
            add(
                findings,
                severity="ERROR",
                artifact="builder-plan.md",
                code="builder.missing_section",
                message=f"Missing required section: {section}.",
                blocking=True,
            )

    tdd_match = re.search(
        r"^##\s+TDD / evidence tasks\s*$\n(?P<body>.*?)(?=^##\s+Contract-fidelity checks\s*$)",
        text,
        flags=re.M | re.S,
    )
    task_source = tdd_match.group("body") if tdd_match else ""
    task_blocks = re.split(r"^###\s+", task_source, flags=re.M)[1:]
    tdd_section_present = "TDD / evidence tasks" in section_titles
    if tdd_section_present and not task_blocks:
        add(
            findings,
            severity="ERROR" if strict_builder_mode else "WARNING",
            artifact="builder-plan.md",
            code="builder.no_task_blocks",
            message="Builder Plan has TDD / evidence tasks section but no task blocks.",
            blocking=strict_builder_mode,
        )

    for raw in task_blocks:
        title = raw.splitlines()[0].strip()
        missing_hints = [hint for hint in TASK_REQUIRED_HINTS if not re.search(hint, raw, flags=re.I)]
        if missing_hints:
            add(
                findings,
                severity="ERROR" if strict_builder_mode else "WARNING",
                artifact="builder-plan.md",
                code="builder.task_missing_hints",
                message=f"Task {title!r} may miss task-contract hints: {', '.join(missing_hints)}.",
                blocking=strict_builder_mode,
            )

    vague = re.findall(r"\b(TBD|TODO|handle edge cases|unqualified similar)\b", task_source)
    if vague:
        add(
            findings,
            severity="WARNING",
            artifact="builder-plan.md",
            code="builder.vague_language",
            message=f"Builder Plan contains potentially vague markers: {sorted(set(vague))}.",
            blocking=False,
        )

    open_work_text = strip_markdown_code(text)
    if mode in {"verify", "archive"} and re.search(r"\b(TODO|todo|planned|missing)\b", open_work_text):
        add(
            findings,
            severity="WARNING",
            artifact="builder-plan.md",
            code="builder.possible_open_work_late_mode",
            message=f"{mode} mode found possible open-work language in builder-plan.md; semantic review should confirm.",
            blocking=False,
        )


def lint(change_dir: Path, mode: str) -> dict[str, Any]:
    findings: list[Finding] = []
    if not change_dir.exists() or not change_dir.is_dir():
        add(
            findings,
            severity="ERROR",
            artifact=str(change_dir),
            code="change_dir.not_found",
            message="Change directory does not exist.",
            blocking=True,
        )
    else:
        lint_quality_gates(change_dir, mode, findings)
        lint_ledger(change_dir, mode, findings)
        lint_builder_plan(change_dir, mode, findings)

    checked_files = [
        name
        for name in ("quality-gates.md", "implementation-ledger.md", "builder-plan.md")
        if (change_dir / name).exists()
    ]
    blocking_count = sum(1 for item in findings if item.blocking)
    return {
        "ok": blocking_count == 0,
        "mode": mode,
        "change_dir": str(change_dir),
        "checked_files": checked_files,
        "finding_count": len(findings),
        "blocking_count": blocking_count,
        "findings": [asdict(item) for item in findings],
        "semantic_boundary": "This linter checks meta-contract structure only; fachliche correctness belongs to OpenSpec Review, Verify, tests, and CEO/CTO review.",
    }


def print_text(result: dict[str, Any]) -> None:
    status = "PASS" if result["ok"] else "FAIL"
    print(f"OpenSpec Meta Lint: {status}")
    print(f"Mode: {result['mode']}")
    print(f"Change: {result['change_dir']}")
    print(f"Checked: {', '.join(result['checked_files']) if result['checked_files'] else 'none'}")
    print(f"Findings: {result['finding_count']} ({result['blocking_count']} blocking)")
    if result["findings"]:
        for item in result["findings"]:
            marker = "BLOCK" if item["blocking"] else "NOTE"
            print(f"- [{marker}] {item['artifact']} {item['code']}: {item['message']}")
    print(result["semantic_boundary"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--change-dir", required=True, help="OpenSpec change directory to lint.")
    parser.add_argument("--mode", required=True, choices=sorted(MODES))
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    result = lint(Path(args.change_dir), args.mode)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print_text(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
