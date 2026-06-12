#!/usr/bin/env python3
"""Back up Simon's Codex OpenSpec skill bundle into the OpenSpecSimon fork."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


BUNDLE_NAME = "openspec-simon"
DEFAULT_REPO = Path("/home/simon/projects/OpenSpecSimon")
DEST_SUBDIR = Path("simon-skills")

SKILL_NAMES = [
    "openspec-apply-change",
    "openspec-archive-change",
    "openspec-explore",
    "openspec-map",
    "openspec-prompt-optimizer",
    "openspec-propose",
    "openspec-review",
    "openspec-verify-change",
    "openspec-skill-backup",
]

SHARED_FILES = [
    "references/openspec-builder-plan.md",
    "references/openspec-clarification-ledger.md",
    "references/openspec-evidence-claim-integrity.md",
    "references/openspec-external-side-effect-reality.md",
    "references/openspec-foundation-coverage-matrix.md",
    "references/openspec-foundation-grilling.md",
    "references/openspec-implementation-ledger.md",
    "references/openspec-intent-driven-testschrift.md",
    "references/openspec-llm-output-contract-testing.md",
    "references/openspec-nordstern-task-bridge.md",
    "references/openspec-prompt-request-parity.md",
    "references/openspec-quality-gates.md",
    "references/openspec-subagent-policy.md",
    "references/openspec-ziel-weg-fitness.md",
    "scripts/openspec_meta_lint.py",
    "scripts/render_prompt_ab_review_surface.py",
    "scripts/validate_foundation_brief.py",
    "templates/llm-output-contract-inventory-template.md",
    "templates/openspec-prompt-improver/README.md",
    "templates/openspec-prompt-improver/assets/data.template.json",
    "templates/openspec-prompt-improver/index.template.html",
    "templates/openspec-foundation-brief-template.md",
]

IGNORE_DIRS = {"__pycache__", ".skill-forger-state", ".pytest_cache"}


def default_source_root() -> Path:
    return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def extract_frontmatter(text: str) -> tuple[list[str], int] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], index
    return None


def get_frontmatter_value(text: str, key: str) -> str | None:
    extracted = extract_frontmatter(text)
    if not extracted:
        return None
    lines, _ = extracted
    prefix = f"{key}:"
    for line in lines:
        if line.startswith(prefix):
            raw = line[len(prefix) :].strip()
            return raw.strip('"').strip("'")
    return None


def upsert_frontmatter(text: str, updates: dict[str, str]) -> str:
    extracted = extract_frontmatter(text)
    if not extracted:
        raise ValueError("missing YAML frontmatter")
    fm_lines, end_index = extracted
    body_lines = text.splitlines()[end_index + 1 :]

    rendered = {
        "bundle": f"bundle: {updates['bundle']}",
        "bundle_version": f"bundle_version: \"{updates['bundle_version']}\"",
    }

    new_fm: list[str] = []

    for line in fm_lines:
        if line.startswith("bundle:"):
            continue
        if line.startswith("bundle_version:"):
            continue
        new_fm.append(line)

    insert_at = None
    for idx, line in enumerate(new_fm):
        if line.startswith("version:"):
            insert_at = idx + 1
            break

    if insert_at is None:
        for idx, line in enumerate(new_fm):
            if line.startswith("name:"):
                insert_at = idx + 1
                break

    if insert_at is None:
        insert_at = 0
    new_fm.insert(insert_at, rendered["bundle_version"])
    new_fm.insert(insert_at, rendered["bundle"])

    return "\n".join(["---", *new_fm, "---", *body_lines]) + "\n"


def current_bundle_versions(source_root: Path, repo: Path) -> list[str]:
    versions: list[str] = []
    candidates = [
        source_root / "shared" / "openspec-simon-bundle.json",
        repo / DEST_SUBDIR / "shared" / "openspec-simon-bundle.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            try:
                data = json.loads(read_text(candidate))
                version = data.get("bundle_version")
                if isinstance(version, str):
                    versions.append(version)
            except json.JSONDecodeError:
                pass
    for skill_name in SKILL_NAMES:
        skill_md = source_root / skill_name / "SKILL.md"
        if skill_md.exists():
            value = get_frontmatter_value(read_text(skill_md), "bundle_version")
            if value:
                versions.append(value)
    return versions


def latest_bundle_version(source_root: Path, repo: Path) -> str | None:
    versions = current_bundle_versions(source_root, repo)
    parsed: list[tuple[str, list[int]]] = []
    for version in versions:
        parts = version.split(".")
        if all(part.isdigit() for part in parts):
            parsed.append((version, [int(part) for part in parts]))
    if not parsed:
        return versions[-1] if versions else None
    return max(parsed, key=lambda item: item[1])[0]


def next_bundle_version(source_root: Path, repo: Path) -> str:
    today = datetime.now().strftime("%Y.%m.%d")
    max_suffix = 0
    pattern = re.compile(rf"^{re.escape(today)}\.(\d+)$")
    for version in current_bundle_versions(source_root, repo):
        match = pattern.match(version)
        if match:
            max_suffix = max(max_suffix, int(match.group(1)))
    return f"{today}.{max_suffix + 1}"


def require_paths(source_root: Path, repo: Path) -> None:
    missing = []
    if not source_root.exists():
        missing.append(str(source_root))
    if not repo.exists():
        missing.append(str(repo))
    for skill_name in SKILL_NAMES:
        skill_md = source_root / skill_name / "SKILL.md"
        if not skill_md.exists():
            missing.append(str(skill_md))
    for rel in SHARED_FILES:
        shared_file = source_root / "shared" / rel
        if not shared_file.exists():
            missing.append(str(shared_file))
    if missing:
        raise FileNotFoundError("Missing required paths:\n" + "\n".join(missing))


def copytree_clean(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)

    def ignore(_dir: str, names: list[str]) -> set[str]:
        return {name for name in names if name in IGNORE_DIRS or name.endswith(".pyc")}

    shutil.copytree(src, dest, ignore=ignore)


def is_ignored_file(path: Path) -> bool:
    return (
        any(part in IGNORE_DIRS for part in path.parts)
        or path.name.endswith(".pyc")
        or path.name == ".DS_Store"
    )


def iter_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file() and not is_ignored_file(path.relative_to(root))
    )


def build_readme(bundle_version: str) -> str:
    skills = "\n".join(f"- `{name}`" for name in SKILL_NAMES)
    return f"""# Simon OpenSpec skill bundle

This directory preserves Simon's Codex-native OpenSpec skill chain.

Canonical local source at snapshot time:

```text
~/.codex/skills
```

Bundle version:

```text
{bundle_version}
```

Included skills:

{skills}

The `shared/` directory contains the OpenSpec-specific references, templates
and validators required by the bundle. The checksum manifest lives at:

```text
simon-skills/shared/openspec-simon-bundle.json
```

When updating this snapshot, treat `~/.codex/skills` as the source of truth,
refresh the copied files, update the bundle version, and recalculate the
manifest checksums.
"""


def generate_manifest(source_root: Path, repo: Path, bundle_version: str) -> dict:
    skills = {}
    for skill_name in SKILL_NAMES:
        skill_md = source_root / skill_name / "SKILL.md"
        text = read_text(skill_md)
        version = get_frontmatter_value(text, "version") or "unversioned"
        skills[skill_name] = {
            "version": version,
            "path": f"{skill_name}/SKILL.md",
            "sha256": sha256_file(skill_md),
        }

    shared_dependencies = {}
    for rel in SHARED_FILES:
        path = source_root / "shared" / rel
        shared_dependencies[rel] = sha256_file(path)

    return {
        "$schema": "sanctum-openspec-skill-bundle-v1",
        "name": BUNDLE_NAME,
        "bundle_version": bundle_version,
        "canonical_source": "codex",
        "canonical_root": str(source_root),
        "destination_repo": str(repo),
        "destination_path": str(repo / DEST_SUBDIR),
        "created_for": "OpenSpecSimon fork backup and drift detection",
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "self_referential": True,
        "skills": skills,
        "shared_dependencies": shared_dependencies,
    }


def apply_snapshot(source_root: Path, repo: Path, bundle_version: str) -> None:
    for skill_name in SKILL_NAMES:
        skill_md = source_root / skill_name / "SKILL.md"
        text = read_text(skill_md)
        updated = upsert_frontmatter(
            text,
            {"bundle": BUNDLE_NAME, "bundle_version": bundle_version},
        )
        if updated != text:
            write_text(skill_md, updated)

    manifest = generate_manifest(source_root, repo, bundle_version)
    manifest_path = source_root / "shared" / "openspec-simon-bundle.json"
    write_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    dest_root = repo / DEST_SUBDIR
    dest_root.mkdir(parents=True, exist_ok=True)
    for skill_name in SKILL_NAMES:
        copytree_clean(source_root / skill_name, dest_root / skill_name)

    shared_dest = dest_root / "shared"
    if shared_dest.exists():
        shutil.rmtree(shared_dest)
    for rel in SHARED_FILES:
        src = source_root / "shared" / rel
        dest = shared_dest / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    shutil.copy2(manifest_path, shared_dest / "openspec-simon-bundle.json")
    write_text(dest_root / "README.md", build_readme(bundle_version))


def run_git(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.stdout.strip()


def status_summary(repo: Path) -> str:
    return run_git(repo, ["status", "--short", "--branch", "--", str(DEST_SUBDIR)])


def remote_status(repo: Path) -> tuple[str, str]:
    branch = run_git(repo, ["status", "--short", "--branch"]).splitlines()
    branch_line = branch[0] if branch else "unknown"
    dirty = bool(run_git(repo, ["status", "--porcelain"]))
    if dirty:
        return "working_tree_dirty", branch_line
    if "ahead" in branch_line and "behind" in branch_line:
        return "diverged", branch_line
    if "ahead" in branch_line:
        return "local_ahead_remote", branch_line
    if "behind" in branch_line:
        return "local_behind_remote", branch_line
    return "in_sync", branch_line


def expected_snapshot_files(source_root: Path) -> dict[str, Path]:
    expected: dict[str, Path] = {}
    for skill_name in SKILL_NAMES:
        skill_root = source_root / skill_name
        for rel in iter_files(skill_root):
            expected[f"{skill_name}/{rel.as_posix()}"] = skill_root / rel
    for rel in SHARED_FILES:
        expected[f"shared/{rel}"] = source_root / "shared" / rel
    return expected


def actual_snapshot_files(repo: Path) -> set[str]:
    dest_root = repo / DEST_SUBDIR
    actual: set[str] = set()
    for skill_name in SKILL_NAMES:
        skill_root = dest_root / skill_name
        for rel in iter_files(skill_root):
            actual.add(f"{skill_name}/{rel.as_posix()}")
    shared_root = dest_root / "shared"
    for rel in iter_files(shared_root):
        label = f"shared/{rel.as_posix()}"
        if label == "shared/openspec-simon-bundle.json":
            continue
        actual.add(label)
    return actual


def compare_source_to_snapshot(source_root: Path, repo: Path) -> dict[str, list[str]]:
    expected = expected_snapshot_files(source_root)
    actual = actual_snapshot_files(repo)
    dest_root = repo / DEST_SUBDIR

    missing: list[str] = []
    changed: list[str] = []
    for label, source_path in expected.items():
        dest_path = dest_root / label
        if not dest_path.exists():
            missing.append(label)
            continue
        if sha256_file(source_path) != sha256_file(dest_path):
            changed.append(label)

    stale = sorted(actual - set(expected))
    return {
        "changed": sorted(changed),
        "missing": sorted(missing),
        "stale": stale,
    }


def has_drift(drift: dict[str, list[str]]) -> bool:
    return any(drift[key] for key in ("changed", "missing", "stale"))


def validate_manifest(repo: Path) -> tuple[bool, list[str]]:
    manifest_path = repo / DEST_SUBDIR / "shared" / "openspec-simon-bundle.json"
    if not manifest_path.exists():
        return False, [f"missing {manifest_path}"]
    manifest = json.loads(read_text(manifest_path))
    errors: list[str] = []
    for name, meta in manifest.get("skills", {}).items():
        path = repo / DEST_SUBDIR / meta["path"]
        if not path.exists():
            errors.append(f"missing skill file: {path}")
            continue
        actual = sha256_file(path)
        if actual != meta["sha256"]:
            errors.append(f"checksum mismatch for {name}: {actual} != {meta['sha256']}")
    for rel, expected in manifest.get("shared_dependencies", {}).items():
        path = repo / DEST_SUBDIR / "shared" / rel
        if not path.exists():
            errors.append(f"missing shared file: {path}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            errors.append(f"checksum mismatch for {rel}: {actual} != {expected}")
    return not errors, errors


def print_plan(source_root: Path, repo: Path, bundle_version: str) -> None:
    print(f"bundle={BUNDLE_NAME}")
    print(f"planned_bundle_version={bundle_version}")
    print(f"source_root={source_root}")
    print(f"destination={repo / DEST_SUBDIR}")
    print("skills:")
    for skill_name in SKILL_NAMES:
        skill_md = source_root / skill_name / "SKILL.md"
        version = get_frontmatter_value(read_text(skill_md), "version") if skill_md.exists() else "missing"
        print(f"  - {skill_name}: {version}")
    print(f"shared_files={len(SHARED_FILES)}")


def print_drift_report(source_root: Path, repo: Path, planned_bundle_version: str) -> bool:
    drift = compare_source_to_snapshot(source_root, repo)
    drift_detected = has_drift(drift)
    remote_state, branch_line = remote_status(repo)
    current_version = latest_bundle_version(source_root, repo) or "unknown"

    print(f"remote_status={remote_state}")
    print(f"remote_branch={branch_line}")
    print(f"source_vs_snapshot={'drift_detected' if drift_detected else 'in_sync'}")
    print(f"current_bundle_version={current_version}")
    print(f"next_bundle_version={planned_bundle_version}")
    print(f"action_needed={'apply_backup' if drift_detected else 'none'}")
    if drift_detected:
        print(
            "suggested_commit_message="
            f"chore(skills): backup OpenSpec Simon bundle {planned_bundle_version}"
        )
        print(
            "decision_question="
            "Soll ich diesen Snapshot jetzt anwenden, validieren, committen und nach GitHub pushen?"
        )

    for key, title in [
        ("changed", "changed_files"),
        ("missing", "missing_in_snapshot"),
        ("stale", "stale_in_snapshot"),
    ]:
        values = drift[key]
        print(f"{title}={len(values)}")
        for value in values[:40]:
            print(f"  - {value}")
        if len(values) > 40:
            print(f"  ... {len(values) - 40} more")

    return drift_detected


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["preview", "apply", "status"])
    parser.add_argument("--source-root", type=Path, default=default_source_root())
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--bundle-version", default=None)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    source_root = args.source_root.expanduser().resolve()
    repo = args.repo.expanduser().resolve()

    try:
        require_paths(source_root, repo)
        bundle_version = args.bundle_version or next_bundle_version(source_root, repo)
        if args.command == "preview":
            print_plan(source_root, repo, bundle_version)
            print("\nbackup_status:")
            print_drift_report(source_root, repo, bundle_version)
            print("\nrepo_status:")
            print(status_summary(repo) or "clean for simon-skills")
            return 0
        if args.command == "apply":
            print_plan(source_root, repo, bundle_version)
            apply_snapshot(source_root, repo, bundle_version)
            ok, errors = validate_manifest(repo)
            print("\nvalidation=" + ("ok" if ok else "failed"))
            for error in errors:
                print(f"  - {error}")
            print("\nrepo_status:")
            print(status_summary(repo) or "clean for simon-skills")
            return 0 if ok else 1
        if args.command == "status":
            ok, errors = validate_manifest(repo)
            print("validation=" + ("ok" if ok else "failed"))
            for error in errors:
                print(f"  - {error}")
            print("\nbackup_status:")
            print_drift_report(source_root, repo, bundle_version)
            print("\nrepo_status:")
            print(status_summary(repo) or "clean for simon-skills")
            return 0 if ok else 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
