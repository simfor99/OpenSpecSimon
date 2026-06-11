#!/usr/bin/env python3
"""Shared helpers for the openspec-review skill."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-")
CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[(?P<state>[ xX])\]", re.MULTILINE)
PATH_RE = re.compile(
    r"(?:^|[\s`'\"])(?P<path>(?:services|types|lib|api|server|pages|components|docs|tests|openspec|\.planning)/[A-Za-z0-9_./@:+-]+)",
    re.MULTILINE,
)
EVIDENCE_NAME_RE = re.compile(
    r"(verification|verify|test-review|test-run|evidence|trace|handoff|parsed-output|prompt|manifest|summary|result)",
    re.IGNORECASE,
)


def normalize_change_name(name: str) -> str:
    return DATE_PREFIX_RE.sub("", name)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def json_dump(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)


def similarity(left: str, right: str) -> float:
    left_norm = normalize_change_name(left).lower()
    right_norm = normalize_change_name(right).lower()
    if not left_norm or not right_norm:
        return 0.0
    if left_norm == right_norm:
        return 1.0
    if left_norm in right_norm or right_norm in left_norm:
        return 0.88
    return SequenceMatcher(None, left_norm, right_norm).ratio()


def is_change_dir(path: Path) -> bool:
    return path.is_dir() and any((path / name).exists() for name in ("proposal.md", "tasks.md", "specs"))


def find_change_dirs(root: Path) -> list[Path]:
    changes = root / "openspec" / "changes"
    if not changes.exists():
        return []
    active = [p for p in changes.iterdir() if p.name != "archive" and is_change_dir(p)]
    archive_root = changes / "archive"
    archived = [p for p in archive_root.iterdir() if is_change_dir(p)] if archive_root.exists() else []
    return sorted(active) + sorted(archived)


def change_kind(path: Path) -> str:
    return "archive_change" if path.parent.name == "archive" else "active_change"


def checkbox_counts(text: str) -> dict[str, int]:
    done = 0
    open_count = 0
    for match in CHECKBOX_RE.finditer(text):
        if match.group("state").lower() == "x":
            done += 1
        else:
            open_count += 1
    return {"done": done, "open": open_count, "total": done + open_count}


def task_counts(change_dir: Path) -> dict[str, int]:
    tasks = change_dir / "tasks.md"
    if not tasks.exists():
        return {"done": 0, "open": 0, "total": 0}
    return checkbox_counts(read_text(tasks))


def delta_specs(change_dir: Path) -> list[str]:
    specs = change_dir / "specs"
    if not specs.exists():
        return []
    result: list[str] = []
    for spec in specs.rglob("*.md"):
        if spec.name == "spec.md":
            result.append(str(spec.relative_to(change_dir)))
    return sorted(result)


def markdown_files(change_dir: Path) -> list[Path]:
    return sorted(path for path in change_dir.rglob("*.md") if path.is_file())


def evidence_files(change_dir: Path) -> list[str]:
    result = []
    for path in change_dir.rglob("*"):
        if path.is_file() and EVIDENCE_NAME_RE.search(path.name):
            result.append(str(path.relative_to(change_dir)))
    return sorted(result)


def referenced_paths(change_dir: Path) -> list[str]:
    found: set[str] = set()
    for path in markdown_files(change_dir):
        for match in PATH_RE.finditer(read_text(path)):
            found.add(match.group("path").rstrip(".,);:"))
    return sorted(found)


def detect_artifacts(change_dir: Path) -> dict[str, Any]:
    verification = [
        rel
        for rel in (
            "verification.md",
            "verification-report.md",
            "verify.md",
            "00-VERIFY.md",
            "00-OPENSPEC-VERIFY.md",
            "00-OPENSPEC-VERIFY-REPORT.md",
        )
        if (change_dir / rel).exists()
    ]
    red_reviews = [
        str(path.relative_to(change_dir))
        for path in change_dir.rglob("00-OPENSPEC-RED-REVIEW.md")
        if path.is_file()
    ]
    return {
        "proposal": (change_dir / "proposal.md").exists(),
        "design": (change_dir / "design.md").exists(),
        "tasks": (change_dir / "tasks.md").exists(),
        "goal": (change_dir / "goal.md").exists(),
        "verification": verification,
        "red_reviews": red_reviews,
        "delta_specs": delta_specs(change_dir),
        "evidence_files": evidence_files(change_dir),
    }


def inventory_for_change(change_dir: Path) -> dict[str, Any]:
    change_dir = change_dir.resolve()
    artifacts = detect_artifacts(change_dir)
    counts = task_counts(change_dir)
    return {
        "path": str(change_dir),
        "name": change_dir.name,
        "normalized_name": normalize_change_name(change_dir.name),
        "kind": change_kind(change_dir),
        "artifacts": artifacts,
        "task_counts": counts,
        "referenced_paths": referenced_paths(change_dir),
        "markdown_files": [str(path.relative_to(change_dir)) for path in markdown_files(change_dir)],
    }


def git_status_paths(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        raw = line[3:] if len(line) > 3 else line.strip()
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw.strip())
    return paths


@dataclass(frozen=True)
class Candidate:
    id: str
    kind: str
    paths: list[str]
    score: float
    recommendation: str
    risk_note: str
    reasons: list[str]
    artifacts: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "paths": self.paths,
            "score": round(self.score, 3),
            "recommendation": self.recommendation,
            "risk_note": self.risk_note,
            "reasons": self.reasons,
            "artifacts": self.artifacts,
        }
