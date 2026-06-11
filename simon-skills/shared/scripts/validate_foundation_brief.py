#!/usr/bin/env python3
"""Strukturvalidator für OpenSpec Foundation Briefs.

Prüft Briefs gegen den Shared-Vertrag
~/.codex/skills/shared/templates/openspec-foundation-brief-template.md.

Aufruf:
    python3 validate_foundation_brief.py <brief-pfad> [--json]

Exit-Codes: 0 = keine Fehler (Warnungen erlaubt), 1 = Fehler, 2 = Aufruf-/Lesefehler.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

PROVENANCE_TOKENS = (
    "example_only",
    "target_contract",
    "proposed_shape",
    "current_runtime_evidence",
    "llm_visible_contract",
    "runtime_only_context",
    "n8n_prior_art",
    "Quelle:",
)

DECISION_MARKERS = ("clarify_first", "map_first", "cto_first", "BD-", "assumed_default")

ALLOWED_PROVENANCE_CLASS = ("target_contract", "proposed_shape")

STATUS_LINE = "Zielbild, nicht aktuelle Runtime-Wahrheit"


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def info(self, msg: str) -> None:
        self.infos.append(msg)


def parse_frontmatter(lines: list[str]) -> dict[str, str]:
    """Flaches Key-Value-Parsing des YAML-Frontmatters (keine Nested-Strukturen nötig)."""
    if not lines or lines[0].strip() != "---":
        return {}
    fm: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if match:
            fm[match.group(1)] = match.group(2).strip().strip('"')
    return fm


def check_frontmatter(fm: dict[str, str], report: Report) -> None:
    if not fm:
        report.error("Frontmatter fehlt (kein '---'-Block am Dateianfang).")
        return
    if "date" not in fm:
        report.error("Frontmatter: Pflichtfeld `date` fehlt.")
    pclass = fm.get("provenance_class", "")
    if not pclass:
        report.error("Frontmatter: Pflichtfeld `provenance_class` fehlt.")
    elif pclass not in ALLOWED_PROVENANCE_CLASS:
        report.error(
            f"Frontmatter: `provenance_class: {pclass}` unzulässig; "
            f"erlaubt: {', '.join(ALLOWED_PROVENANCE_CLASS)}."
        )
    if fm.get("binding_status", "") != "pre_spec_zielbild":
        report.error(
            "Frontmatter: `binding_status: pre_spec_zielbild` fehlt — "
            "ohne Bindungsstatus droht der Brief als Dauerwahrheit gelesen zu werden."
        )
    if "depends_on" not in fm:
        report.warn("Frontmatter: `depends_on` fehlt (Quellen-Verankerung empfohlen).")
    if "resulting_openspec_change" not in fm:
        report.warn(
            "Frontmatter: `resulting_openspec_change` fehlt "
            "(Backlink-Feld; `none_yet` bis $openspec-propose es setzt)."
        )


def check_status_line(text: str, report: Report) -> None:
    h1_match = re.search(r"^# .+$", text, flags=re.MULTILINE)
    if not h1_match:
        report.error("Kein H1 gefunden.")
        return
    window = text[h1_match.end() : h1_match.end() + 600]
    if STATUS_LINE not in window:
        report.error(
            f'Pflicht-Statuszeile "{STATUS_LINE}" fehlt direkt unter dem H1.'
        )


def headings(text: str) -> list[str]:
    return re.findall(r"^#{1,4}\s+(.+)$", text, flags=re.MULTILINE)


def has_heading(text: str, *needles: str) -> bool:
    return any(
        all(needle.lower() in h.lower() for needle in needles) for h in headings(text)
    )


def check_core_sections(text: str, report: Report) -> None:
    if not has_heading(text, "In einem Satz"):
        report.error("Kern-Sektion `## In einem Satz` fehlt.")
    if not (has_heading(text, "nicht macht") or has_heading(text, "Scope")):
        report.error("Kern-Sektion Scope/Nicht-Scope fehlt.")
    if not has_heading(text, "Quellen"):
        report.error("Kern-Sektion `## Quellen` fehlt.")
    if not has_heading(text, "Lebenszyklus"):
        report.error(
            "Kern-Sektion `## Lebenszyklus dieses Briefs` fehlt — "
            "die Demotions-Regel ist der Vierte-Wahrheit-Schutz."
        )
    if not has_heading(text, "Als gegeben"):
        report.warn(
            "Sektion `## Als gegeben angenommene Punkte` fehlt "
            "(Korb 2 des Grilling-Protokolls; weglassen nur, wenn es keine Annahmen gab)."
        )
    if not (has_heading(text, "Entscheidungen") or has_heading(text, "Offene Fragen")):
        report.warn("Sektion für geklärte/offene Entscheidungen fehlt.")
    if not has_heading(text, "Handoff"):
        report.warn("Map-/Propose-Handoff-Sektion fehlt.")
    if not has_heading(text, "Rückkanal"):
        report.error(
            "Kern-Sektion `## OpenSpec-Rückkanal` fehlt — ohne datierte "
            "Status-Einträge wird ein nicht umgesetzter Spec übersehen."
        )


def check_json_fence_provenance(text: str, report: Report) -> None:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if re.match(r"^```jsonc?\s*$", line.strip()):
            context = "\n".join(lines[max(0, idx - 20) : idx])
            fence_body_end = idx + 1
            while fence_body_end < len(lines) and not lines[fence_body_end].strip().startswith("```"):
                fence_body_end += 1
            body = "\n".join(lines[idx : fence_body_end])
            haystack = context + "\n" + body
            if not any(token in haystack for token in PROVENANCE_TOKENS):
                report.error(
                    f"JSON-Block ab Zeile {idx + 1} ohne Provenienzmarkierung "
                    "(example_only / target_contract / proposed_shape / `Quelle:` davor oder darin)."
                )


def check_decision_markers(text: str, report: Report) -> None:
    mentions_open = re.search(r"^\s*Offen:?\s*$", text, flags=re.MULTILINE) or has_heading(
        text, "Offene"
    )
    if mentions_open and not any(marker in text for marker in DECISION_MARKERS):
        report.warn(
            "Offene Punkte vorhanden, aber keine kanonischen Marker "
            "(clarify_first / map_first / cto_first / BD-* / assumed_default) — "
            "das CEO-Decision-Gate von $openspec-propose findet sie so nicht."
        )


def check_self_contained_claims(text: str, report: Report) -> None:
    claim = re.search(
        r"self-contained|vollständige[rn]?\s+operative", text, flags=re.IGNORECASE
    )
    if not claim:
        return
    sources_section = re.search(r"^#{1,4}\s+.*Quellen.*$", text, flags=re.MULTILINE)
    table_rows = len(re.findall(r"^\|.+\|$", text, flags=re.MULTILINE))
    if sources_section and table_rows >= 3:
        report.info(
            "Self-contained-Anspruch gefunden; Quellen-Tabelle vorhanden — zulässig "
            "(jede wiederholte Regel muss dort belegt sein)."
        )
    else:
        report.error(
            "Self-contained-Anspruch ohne belegende Quellen-Tabelle — "
            "verboten laut Lebenszyklus-Vertrag des Templates."
        )


def check_runtime_module(text: str, report: Report) -> None:
    if not has_heading(text, "Must-Survive"):
        return
    if not (has_heading(text, "Stop-Regeln") or has_heading(text, "Fehlerfälle")):
        report.error(
            "Runtime-Stage-Modul aktiv (Must-Survive-Facts vorhanden), aber "
            "Fehlerfälle/Stop-Regeln fehlen — bei Runtime-Stage-Arbeit nicht optional."
        )
    if not has_heading(text, "Handoff"):
        report.error(
            "Runtime-Stage-Modul aktiv, aber Handoff-Sektion fehlt — "
            "bei Runtime-Stage-Arbeit nicht optional."
        )
    if not has_heading(text, "Datenmodell"):
        report.warn(
            "Runtime-Stage-Modul aktiv, aber keine Ziel-Datenmodell-Sektion — "
            "ohne kommentiertes Datenmodell und Bewusste Nicht-Felder rät der "
            "Builder die JSON-Verträge."
        )
    if not (has_heading(text, "Deprecation") or has_heading(text, "Limits")):
        report.error(
            "Runtime-Stage-Modul aktiv, aber Sektion `Deprecation, Limits und "
            "Cleanup` fehlt — ohne Deprecation-Vertrag bleiben alte Wahrheiten "
            "aktiv neben dem neuen Schnitt (Lektion Stage-00-Slug-Drift)."
        )


def _jsonc_top_level_fields(text: str) -> set[str]:
    """Top-Level-Feldnamen (Einrückung <= 2 Spaces) aus jsonc-Fences."""
    fields: set[str] = set()
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^```jsonc?\s*$", stripped):
            in_fence = True
            continue
        if in_fence and stripped.startswith("```"):
            in_fence = False
            continue
        if in_fence:
            match = re.match(r"^ {0,2}\"([a-z0-9_]+)\"\s*:", line)
            if match:
                fields.add(match.group(1))
    return fields


def check_field_owner_parity(text: str, report: Report) -> None:
    """Kein Feld ohne Erzeuger: Datenmodell-Felder brauchen eine Eigentümer-Zeile."""
    if not has_heading(text, "Datenmodell"):
        return
    table_rows = [l for l in text.splitlines() if l.strip().startswith("|")]
    has_owner_table = any("Eigentümer" in row for row in table_rows)
    if not has_owner_table:
        report.error(
            "Ziel-Datenmodell vorhanden, aber keine Feld-Eigentümer-Tabelle "
            "(Spalte `Eigentümer`) — die Kein-Feld-ohne-Erzeuger-Regel ist "
            "nicht prüfbar (Lektion `url_evidence_map`-Doppler)."
        )
        return
    rows_text = "\n".join(table_rows)
    fields = _jsonc_top_level_fields(text)
    missing = sorted(f for f in fields if f not in rows_text)
    if missing:
        report.warn(
            "Datenmodell-Felder ohne Zeile in einer Eigentümer-/Vertrags-Tabelle "
            f"({len(missing)}): {', '.join(missing[:12])}"
            f"{' …' if len(missing) > 12 else ''} — pro Feld Erzeuger benennen "
            "oder Feld streichen."
        )


def _has_substantive_lines(body: str) -> bool:
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("```"):
            continue
        if re.fullmatch(r"\[[^\]]*\]|TBD|\.{3}", stripped):
            continue
        return True
    return False


def check_prompt_blocks(text: str, report: Report) -> None:
    """Prompt-Vollständigkeit: voller Wortlaut Pflicht, außer Block trägt Marker."""
    lines = text.splitlines()
    starts = [i for i, l in enumerate(lines) if re.match(r"^###\s+Prompt\b", l)]
    for pos, start in enumerate(starts):
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if re.match(r"^#{2,3}\s+", lines[j]) and not re.match(r"^###\s+Prompt\b", lines[j]):
                end = j
                break
            if j in starts:
                end = j
                break
        block = "\n".join(lines[start:end])
        title = lines[start].lstrip("# ").strip()
        has_marker = any(m in block for m in ("clarify_first", "BD-", "cto_first", "map_first"))
        emit = report.warn if has_marker else report.error
        suffix = " (Block trägt Marker — nur Warnung)" if has_marker else ""
        if "operation_id" not in block:
            emit(f"Prompt-Block `{title}`: kein `operation_id` im yaml-/Frontmatter-Teil.{suffix}")
        sys_match = re.search(r"^#\s*System Prompt\s*$", block, flags=re.MULTILINE)
        usr_match = re.search(r"^#\s*User Prompt\s*$", block, flags=re.MULTILINE)
        if not sys_match:
            emit(f"Prompt-Block `{title}`: `# System Prompt` fehlt.{suffix}")
        if not usr_match:
            emit(f"Prompt-Block `{title}`: `# User Prompt` fehlt.{suffix}")
        if sys_match and usr_match and usr_match.start() > sys_match.end():
            sys_body = block[sys_match.end() : usr_match.start()]
            usr_body = block[usr_match.end() :]
            if not _has_substantive_lines(sys_body):
                emit(f"Prompt-Block `{title}`: System-Prompt-Wortlaut fehlt (nur Platzhalter).{suffix}")
            if not _has_substantive_lines(usr_body):
                emit(f"Prompt-Block `{title}`: User-Prompt-Wortlaut fehlt (nur Platzhalter).{suffix}")
            elif "{" not in usr_body:
                emit(f"Prompt-Block `{title}`: kein Output-JSON inline im User Prompt.{suffix}")
            block_names = re.findall(r"-\s*name:\s*([a-z0-9_]+)", block)
            unused = [v for v in block_names if f"${v}" not in block]
            if unused:
                report.warn(
                    f"Prompt-Block `{title}`: input_context_blocks ohne "
                    f"$-Verwendung im Prompt: {', '.join(unused)}."
                )


def validate(path: Path) -> Report:
    report = Report()
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    check_frontmatter(parse_frontmatter(lines), report)
    check_status_line(text, report)
    check_core_sections(text, report)
    check_json_fence_provenance(text, report)
    check_decision_markers(text, report)
    check_self_contained_claims(text, report)
    check_runtime_module(text, report)
    check_field_owner_parity(text, report)
    check_prompt_blocks(text, report)
    return report


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    as_json = "--json" in argv
    if len(args) != 1:
        print("Aufruf: validate_foundation_brief.py <brief-pfad> [--json]", file=sys.stderr)
        return 2
    path = Path(args[0]).expanduser()
    if not path.is_file():
        print(f"Datei nicht gefunden: {path}", file=sys.stderr)
        return 2
    report = validate(path)
    if as_json:
        print(
            json.dumps(
                {
                    "file": str(path),
                    "errors": report.errors,
                    "warnings": report.warnings,
                    "infos": report.infos,
                    "ok": not report.errors,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for msg in report.errors:
            print(f"ERROR   {msg}")
        for msg in report.warnings:
            print(f"WARNUNG {msg}")
        for msg in report.infos:
            print(f"INFO    {msg}")
        verdict = "FEHLER" if report.errors else "OK"
        print(
            f"\n{verdict}: {len(report.errors)} Fehler, "
            f"{len(report.warnings)} Warnungen — {path.name}"
        )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
