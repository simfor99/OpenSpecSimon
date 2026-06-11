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
    "scripts/validate_foundation_brief.py",
    "templates/llm-output-contract-inventory-template.md",
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
            print("\nrepo_status:")
            print(status_summary(repo) or "clean for simon-skills")
            return 0 if ok else 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
