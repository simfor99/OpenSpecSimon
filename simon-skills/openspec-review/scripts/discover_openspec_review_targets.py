#!/usr/bin/env python3
"""Discover plausible OpenSpec review targets."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

from openspec_review_lib import (
    Candidate,
    detect_artifacts,
    find_change_dirs,
    git_status_paths,
    inventory_for_change,
    json_dump,
    normalize_change_name,
    similarity,
)


def score_change(change_dir: Path, query: str | None, dirty_paths: list[str]) -> Candidate:
    inv = inventory_for_change(change_dir)
    artifacts = inv["artifacts"]
    reasons: list[str] = []
    score = 0.0

    if query:
        score += similarity(query, inv["name"]) * 100
        if normalize_change_name(query) == inv["normalized_name"]:
            reasons.append("exact normalized name match")
        elif normalize_change_name(query) in inv["normalized_name"]:
            reasons.append("query is contained in change name")
        else:
            reasons.append("fuzzy name similarity")
    else:
        if inv["kind"] == "active_change":
            score += 45
            reasons.append("active change")
        else:
            score += 20
            reasons.append("archived change")
        if artifacts["verification"]:
            score += 18
            reasons.append("verification artifact exists")
        if not artifacts["red_reviews"]:
            score += 15
            reasons.append("no red review found")
        if artifacts["delta_specs"]:
            score += min(len(artifacts["delta_specs"]) * 2, 12)
            reasons.append("delta specs found")
        if inv["task_counts"]["open"] > 0:
            score += 8
            reasons.append("open tasks still exist")

    change_rel = str(change_dir)
    dirty_related = [path for path in dirty_paths if path.startswith(change_rel) or change_rel in path]
    if dirty_related:
        score += 15
        reasons.append("git status has files under this change")

    if artifacts["red_reviews"]:
        recommendation = "already_reviewed"
        risk_note = "Red review already exists; rerun only if implementation changed since review."
    elif inv["kind"] == "active_change" and not artifacts["verification"]:
        recommendation = "review_after_verify"
        risk_note = "Active change has no verification artifact; review can run early but should label evidence as pre-verify."
    else:
        recommendation = "review_start"
        risk_note = "Good candidate for paranoid OpenSpec review."

    preview_artifacts = {
        "proposal": artifacts["proposal"],
        "design": artifacts["design"],
        "tasks": artifacts["tasks"],
        "goal": artifacts["goal"],
        "verification": artifacts["verification"],
        "red_review": artifacts["red_reviews"],
        "delta_spec_count": len(artifacts["delta_specs"]),
        "task_counts": inv["task_counts"],
    }

    return Candidate(
        id=inv["normalized_name"],
        kind=inv["kind"],
        paths=[str(change_dir)],
        score=score,
        recommendation=recommendation,
        risk_note=risk_note,
        reasons=reasons,
        artifacts=preview_artifacts,
    )


def active_archive_pairs(candidates: list[Candidate]) -> list[Candidate]:
    active = [c for c in candidates if c.kind == "active_change"]
    archived = [c for c in candidates if c.kind == "archive_change"]
    pairs: list[Candidate] = []
    for item in active:
        related = [a for a in archived if similarity(item.id, a.id) >= 0.72]
        if not related:
            continue
        best = sorted(related, key=lambda c: c.score, reverse=True)[0]
        pairs.append(
            Candidate(
                id=f"{item.id}__with_archive_context",
                kind="active_archive_pair",
                paths=item.paths + best.paths,
                score=item.score + 6,
                recommendation="choose",
                risk_note="Active change has archived neighbor context; review may need both folders.",
                reasons=["active/archive similarity", *item.reasons[:2], *best.reasons[:1]],
                artifacts={"primary": item.artifacts, "archive_context": best.artifacts},
            )
        )
    return pairs


def spec_clusters(candidates: list[Candidate], root: Path, limit: int) -> list[Candidate]:
    by_spec: dict[str, list[Candidate]] = defaultdict(list)
    for candidate in candidates:
        path = Path(candidate.paths[0])
        for rel in detect_artifacts(path)["delta_specs"]:
            parts = Path(rel).parts
            if len(parts) >= 2:
                by_spec[parts[1]].append(candidate)

    clusters: list[Candidate] = []
    for spec_name, items in by_spec.items():
        if len(items) < 2:
            continue
        ranked = sorted(items, key=lambda c: c.score, reverse=True)[:limit]
        clusters.append(
            Candidate(
                id=f"spec_cluster__{spec_name}",
                kind="spec_cluster",
                paths=[path for item in ranked for path in item.paths],
                score=max(item.score for item in ranked) + len(ranked),
                recommendation="choose",
                risk_note="Multiple changes touch the same spec capability.",
                reasons=[f"shared spec: {spec_name}"],
                artifacts={"change_count": len(ranked), "root": str(root)},
            )
        )
    return clusters


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    parser.add_argument("--query", "-q", help="Change name or fuzzy query")
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(json_dump({"ok": False, "error": f"root not found: {root}"}))
        return 2

    dirty = git_status_paths(root)
    changes = find_change_dirs(root)
    scored = [score_change(path, args.query, dirty) for path in changes]
    if args.query:
        scored = [candidate for candidate in scored if candidate.score >= 45]

    groups = []
    if not args.query:
        groups.extend(active_archive_pairs(scored))
        groups.extend(spec_clusters(scored, root, args.limit))

    candidates = sorted([*scored, *groups], key=lambda c: c.score, reverse=True)[: args.limit]
    exact_selected = None
    if args.query and candidates:
        query_norm = normalize_change_name(args.query)
        if candidates[0].id == query_norm and candidates[0].score >= 100:
            exact_selected = candidates[0]

    output = {
        "ok": True,
        "root": str(root),
        "query": args.query,
        "candidate_count": len(candidates),
        "candidates": [candidate.to_dict() for candidate in candidates],
        "selected_candidate": exact_selected.to_dict() if exact_selected else None,
        "selection_required": False if exact_selected else len(candidates) != 1,
    }
    print(json_dump(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
