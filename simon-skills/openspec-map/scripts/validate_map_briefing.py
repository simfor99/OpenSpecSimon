#!/usr/bin/env python3
"""Lightweight structural validator for openspec-map briefing artifacts.

Zusätzlich erzwingt er Gate A (Extraction Fidelity) selbst: Wenn
`prompt_contracts_required: true` und `prompt_contracts_status: created`,
werden die gelisteten Contract-Dateien aufgelöst und durch
`validate_prompt_fidelity.py --extraction-check` geprüft. Ein `created`-Claim
ohne grünes Gate und maschinenlesbare Gate-Evidenz ist ein Fehler — die
Sicherheit hängt damit nicht an Skill-Prosa (Lektion Stage-00, 2026-06-10)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

FIDELITY_CHECKER = (
    Path(__file__).resolve().parents[2] / "shared" / "scripts" / "validate_prompt_fidelity.py"
)


def normalize_scalar(raw: str) -> str:
    """Return a YAML-ish scalar without surrounding quotes/backticks."""
    value = raw.strip().strip("`").strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1].strip()
    return value


def scalar_values(text: str, key: str) -> list[str]:
    """Extract simple `key: value` scalars from markdown/YAML-ish blocks."""
    return [
        normalize_scalar(match.group(1))
        for match in re.finditer(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    ]


def has_true_scalar(text: str, key: str) -> bool:
    return any(value.lower() == "true" for value in scalar_values(text, key))


def resolve_contract_path(raw: str, map_path: Path) -> Path | None:
    """Listeneinträge können repo-relativ, map-relativ oder absolut sein."""
    raw = raw.strip().strip("`").strip()
    for base in (Path.cwd(), map_path.parent, map_path.parent.parent):
        candidate = (base / raw).expanduser()
        if candidate.exists():
            return candidate
    candidate = Path(raw).expanduser()
    return candidate if candidate.exists() else None


def run_extraction_gate(files: list[str], map_path: Path) -> bool:
    """Führt Gate A für alle gelisteten Contract-Dateien aus. True = grün."""
    if not FIDELITY_CHECKER.is_file():
        print(f"ERROR: extraction gate checker not found: {FIDELITY_CHECKER}")
        return False
    ok = True
    for raw in files:
        resolved = resolve_contract_path(raw, map_path)
        if resolved is None:
            print(f"ERROR: listed prompt contract not found on disk: {raw}")
            ok = False
            continue
        result = subprocess.run(
            [sys.executable, str(FIDELITY_CHECKER), "--extraction-check", str(resolved)],
            capture_output=True,
            check=False,
            text=True,
        )
        if result.returncode != 0:
            print(f"ERROR: extraction gate (Gate A) failed for {resolved}:")
            for line in result.stdout.splitlines():
                if "ERROR" in line:
                    print(f"  {line.strip()}")
            ok = False
    return ok


REQUIRED_PATTERNS = {
    "frontmatter": r"\A---\n",
    "path_line": r"^> Pfad: `[^`]+`",
    "component_map": r"^## Component Map\b",
    "propose_readiness": r"propose_readiness:",
    "readiness_status": r"status:\s*(ready_for_propose|not_ready_for_propose)",
    "primary_briefing_path": r"primary_briefing_path:",
    "suggested_next_prompt": r"suggested_next_prompt:",
    "handoff": r"^## Handoff To `\$openspec-propose`",
}

OPTIONAL_NETWORK_PATTERNS = {
    "upstream_decision_sources": r"^## Upstream Decision Sources\b",
    "prompt_contracts": r"^## Prompt Contracts\b",
    "skill_network_handoff": r"^## Skill Network Handoff\b",
    "cto_review_map_backchannel": r"^## CTO Review Map Backchannel\b",
    "source_cto_reviews": r"source_cto_reviews:",
    "map_backchannel_status": r"map_backchannel_status:",
    "cto_review_backchannel_required": r"cto_review_backchannel_required:",
    "goal_brief_recommended": r"goal_brief_recommended:",
}


def gate_evidence_errors(text: str) -> list[str]:
    match = re.search(
        r"prompt_contract_extraction_gate:\n(?P<block>(?:\s+[A-Za-z_]+:\s*.*\n?)+)",
        text,
        flags=re.MULTILINE,
    )
    if not match:
        return [
            "machine-readable `prompt_contract_extraction_gate:` block missing "
            "in propose_readiness (required: status, command, checked_at)."
        ]
    block = match.group("block")
    errors: list[str] = []
    status_values = scalar_values(block, "status")
    command_values = scalar_values(block, "command")
    checked_at_values = scalar_values(block, "checked_at")
    if not status_values or status_values[0] != "passed":
        errors.append("`prompt_contract_extraction_gate.status` fehlt oder ist ungültig.")
    if not command_values or not (
        "validate_prompt_fidelity.py" in command_values[0]
        and "--extraction-check" in command_values[0]
    ):
        errors.append("`prompt_contract_extraction_gate.command` fehlt oder ist ungültig.")
    if not checked_at_values or not checked_at_values[0]:
        errors.append("`prompt_contract_extraction_gate.checked_at` fehlt oder ist ungültig.")
    return errors


def warn_none_sentinel_lists(text: str) -> None:
    """Warn when YAML-ish lists use `- none` instead of [] or omission."""
    for field in (
        "source_cto_reviews",
        "source_red_reviews",
        "required_followup_before_propose",
        "prompt_contract_files",
    ):
        pattern = rf"^\s*{re.escape(field)}:\s*\n(?P<block>(?:\s+-\s+.+\n?)+)"
        for match in re.finditer(pattern, text, flags=re.MULTILINE):
            block = match.group("block")
            if re.search(r"^\s+-\s*(none|null|n/a|not_applicable)\s*$", block, re.I | re.M):
                print(
                    f"WARN: `{field}` uses a sentinel list item; prefer `[]` "
                    "or omit the list when empty."
                )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map_briefing", type=Path, help="openspec-map briefing Markdown file")
    args = parser.parse_args(argv)

    path = args.map_briefing
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1
    if path.stat().st_size == 0:
        print(f"ERROR: file is empty: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    missing = [
        name
        for name, pattern in REQUIRED_PATTERNS.items()
        if not re.search(pattern, text, flags=re.MULTILINE)
    ]

    if missing:
        print("ERROR: missing required map briefing sections:")
        for name in missing:
            print(f"- {name}")
        return 1

    optional_missing = [
        name
        for name, pattern in OPTIONAL_NETWORK_PATTERNS.items()
        if not re.search(pattern, text, flags=re.MULTILINE)
    ]
    if optional_missing:
        print("WARN: missing optional skill-network sections/fields:")
        for name in optional_missing:
            print(f"- {name}")

    warn_none_sentinel_lists(text)

    component_ids = re.findall(r"component_id:\s*(.+)", text)
    if not component_ids:
        print("WARN: no component_id entries found; map may be too shallow.")

    prompt_contracts_required = has_true_scalar(text, "prompt_contracts_required")
    if prompt_contracts_required:
        if not re.search(r"^## Prompt Contracts\b", text, flags=re.MULTILINE):
            print("ERROR: prompt_contracts_required is true but ## Prompt Contracts is missing.")
            return 1
        status_values = scalar_values(text, "prompt_contracts_status")
        if "created" not in status_values:
            print("ERROR: prompt contracts are required but status is not created.")
            return 1
        prompt_files_block = re.search(
            r"prompt_contract_files:\n(?P<block>(?:\s+-\s+.+\n)+)",
            text,
        )
        if not prompt_files_block:
            print("ERROR: prompt contracts are required but no prompt_contract_files are listed.")
            return 1
        listed_files = re.findall(r"^\s+-\s+(.+)$", prompt_files_block.group("block"), re.MULTILINE)
        if not run_extraction_gate(listed_files, path):
            print(
                "ERROR: prompt_contracts_status is `created` but Gate A "
                "(extraction fidelity) is red — contracts are NOT created."
            )
            return 1
        evidence_errors = gate_evidence_errors(text)
        if evidence_errors:
            for error in evidence_errors:
                print(f"ERROR: {error}")
            return 1

    print(f"OK: {path} looks like an openspec-map briefing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
