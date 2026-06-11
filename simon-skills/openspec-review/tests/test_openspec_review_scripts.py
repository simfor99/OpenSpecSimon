from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_DIR / "scripts"


def run_script(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def write_change(root: Path, name: str, archived: bool = False, verified: bool = True) -> Path:
    base = root / "openspec" / "changes"
    change_dir = base / ("archive" if archived else "") / name if archived else base / name
    spec_dir = change_dir / "specs" / "demo-capability"
    spec_dir.mkdir(parents=True)
    (change_dir / "proposal.md").write_text(
        "# Proposal\n\nChange references `services/demo.ts` and needs review.\n",
        encoding="utf-8",
    )
    (change_dir / "tasks.md").write_text(
        "- [x] Build thing\n- [ ] Verify tricky assumption\n",
        encoding="utf-8",
    )
    (spec_dir / "spec.md").write_text(
        "# Demo capability\n\n## ADDED Requirements\n\n### Requirement: Demo\n",
        encoding="utf-8",
    )
    if verified:
        (change_dir / "verification-report.md").write_text("APPROVED_WITH_NOTES\n", encoding="utf-8")
    return change_dir


def test_inventory_counts_tasks_and_specs(tmp_path: Path) -> None:
    change_dir = write_change(tmp_path, "demo-change")
    result = run_script("inventory_openspec_archive.py", str(change_dir))
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["task_counts"] == {"done": 1, "open": 1, "total": 2}
    assert data["artifacts"]["verification"] == ["verification-report.md"]
    assert data["artifacts"]["delta_specs"] == ["specs/demo-capability/spec.md"]
    assert data["referenced_paths"] == ["services/demo.ts"]


def test_inventory_accepts_canonical_openspec_verify_report(tmp_path: Path) -> None:
    change_dir = write_change(tmp_path, "demo-change", verified=False)
    (change_dir / "00-OPENSPEC-VERIFY.md").write_text("APPROVED_WITH_NOTES\n", encoding="utf-8")
    (change_dir / "00-OPENSPEC-VERIFY-REPORT.md").write_text("Detailed report\n", encoding="utf-8")

    result = run_script("inventory_openspec_archive.py", str(change_dir))
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["artifacts"]["verification"] == [
        "00-OPENSPEC-VERIFY.md",
        "00-OPENSPEC-VERIFY-REPORT.md",
    ]


def test_discover_finds_exact_active_change(tmp_path: Path) -> None:
    write_change(tmp_path, "demo-change")
    write_change(tmp_path, "2026-06-01-demo-change", archived=True)
    result = run_script("discover_openspec_review_targets.py", str(tmp_path), "--query", "demo-change")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["candidates"][0]["id"] == "demo-change"
    assert data["candidates"][0]["recommendation"] == "review_start"


def test_prescan_flags_open_tasks_and_missing_red_review(tmp_path: Path) -> None:
    change_dir = write_change(tmp_path, "demo-change", verified=False)
    result = run_script("openspec_review_prescan.py", str(change_dir))
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    titles = {finding["title"] for finding in data["prescan_findings"]}
    assert "Offene Tasks gefunden" in titles
    assert "Kein Verify-Artefakt gefunden" in titles
    assert "Noch kein OpenSpec Red Review gefunden" in titles


def test_report_validator_accepts_fix_and_decision_contract(tmp_path: Path) -> None:
    report = tmp_path / "00-OPENSPEC-RED-REVIEW.md"
    report.write_text(
        """# demo-change - OpenSpec Red Review

## 0. Zusammenfassung für Simon

- Verdict: `PAUSED_FOR_DECISION`

## 1. Abschlussentscheidung, die dieser Review vorbereitet

Review prepares archive decision.

## 2. Was behauptet wurde

Claims were checked.

## 3. Was Red geprüft hat

Red checked evidence paths.

## 4. Systemverständnis und Must-Survive-Facts

| Subsystem | What Red Checked | Why It Matters | Must-Survive-Facts | Coverage |
|---|---|---|---|---|
| Demo | `services/demo.ts` | Carries the claim | Build result remains visible | yes |

Coverage Gate: yes

## 5. Übersehene Komplexität und falsche Annahmen

Hidden complexity exists.

## 6. Findings

### F-001 Missing evidence

- Klasse: FIX
- Status: OPEN
- Severity: HIGH
- Evidence: `openspec/changes/demo-change/verification-report.md`

### F-002 Scope choice

- Klasse: DECISION
- Status: SIMON
- Severity: HIGH
- Evidence: `openspec/changes/demo-change/design.md`
- Option A: Keep scope.
- Option B: Split scope.
- Red-Empfehlung: Option B.
- Nicht geändert: Keine DECISION-Änderung wurde umgesetzt.

## 7. Evidence Reality Check

Runtime claims were separated from code pass claims.

## 8. Stop-Regeln

Stop before archive until decision.

## 9. Zurückzuschreiben nach

OpenSpec change folder.

## 10. Vault-Learnings

Keine wiederverwendbaren Learnings.
""",
        encoding="utf-8",
    )
    result = run_script("validate_openspec_review_report.py", str(report))
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["finding_count"] == 2


def test_report_validator_rejects_approved_with_partial_coverage(tmp_path: Path) -> None:
    report = tmp_path / "00-OPENSPEC-RED-REVIEW.md"
    report.write_text(
        """# demo-change - OpenSpec Red Review

## 0. Zusammenfassung für Simon

- Verdict: `APPROVED`

## 1. Abschlussentscheidung, die dieser Review vorbereitet

Review prepares archive decision.

## 2. Was behauptet wurde

Claims were checked.

## 3. Was Red geprüft hat

Red checked evidence paths.

## 4. Systemverständnis und Must-Survive-Facts

Must-Survive-Facts: `services/demo.ts` must carry the claim.

Coverage Gate: partial

## 5. Übersehene Komplexität und falsche Annahmen

Hidden complexity exists.

## 6. Findings

### F-001 Missing evidence

- Klasse: FIX
- Status: OPEN
- Severity: HIGH
- Evidence: `openspec/changes/demo-change/verification-report.md`

## 7. Evidence Reality Check

Runtime claims were separated from code pass claims.

## 8. Stop-Regeln

Stop before archive until decision.

## 9. Zurückzuschreiben nach

OpenSpec change folder.

## 10. Vault-Learnings

Keine wiederverwendbaren Learnings.
""",
        encoding="utf-8",
    )
    result = run_script("validate_openspec_review_report.py", str(report))
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert data["ok"] is False
    assert any("plain APPROVED is invalid" in error for error in data["errors"])


def test_report_validator_requires_ab_status_for_ziel_weg_fitness(tmp_path: Path) -> None:
    report = tmp_path / "00-OPENSPEC-RED-REVIEW.md"
    report.write_text(
        """# demo-change - OpenSpec Red Review

## 0. Zusammenfassung für Simon

- Verdict: `APPROVED_WITH_NOTES`

## 1. Abschlussentscheidung, die dieser Review vorbereitet

Review prepares archive decision.

## 2. Was behauptet wurde

Claims were checked.

## 3. Was Red geprüft hat

Red checked evidence paths.

## 4. Systemverständnis und Must-Survive-Facts

Must-Survive-Facts: `services/demo.ts` must carry the claim.

Coverage Gate: yes

### Ziel-Weg-Fitness
- Goal: Demo works.
- Selected path: Larger mechanism.

## 5. Übersehene Komplexität und falsche Annahmen

Hidden complexity exists.

## 6. Findings

### F-001 Missing evidence

- Klasse: FIX
- Status: OPEN
- Severity: HIGH
- Evidence: `openspec/changes/demo-change/verification-report.md`

## 7. Evidence Reality Check

Runtime claims were separated from code pass claims.

## 8. Stop-Regeln

Stop before archive until decision.

## 9. Zurückzuschreiben nach

OpenSpec change folder.

## 10. Vault-Learnings

Keine wiederverwendbaren Learnings.
""",
        encoding="utf-8",
    )
    result = run_script("validate_openspec_review_report.py", str(report))
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert data["ok"] is False
    assert any("A/B status" in error for error in data["errors"])


def test_report_validator_rejects_placeholders(tmp_path: Path) -> None:
    report = tmp_path / "bad.md"
    report.write_text("# {{CHANGE_NAME}}\n", encoding="utf-8")
    result = run_script("validate_openspec_review_report.py", str(report))
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert data["ok"] is False
    assert any("unresolved placeholders" in error for error in data["errors"])


def test_distill_vault_learning_rows(tmp_path: Path) -> None:
    report = tmp_path / "review.md"
    report.write_text(
        """# Review

## 9. Vault-Learnings

| Titel | Evidence | Ziel |
|---|---|---|
| Verify ist nicht Red Review | `openspec/changes/demo/00-OPENSPEC-RED-REVIEW.md` zeigt, dass Verify nur Vertragserfüllung prüft. | `07-research/patterns/verify-vs-red-review.md` |
""",
        encoding="utf-8",
    )
    result = run_script("distill_vault_learnings.py", str(report))
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["candidates"][0]["title"] == "Verify ist nicht Red Review"
