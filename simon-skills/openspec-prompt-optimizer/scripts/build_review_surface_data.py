#!/usr/bin/env python3
"""Build Prompt A/B Review Surface data.json from Pre-Spec round evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


EXPECTED_ARTIFACT_LOAD_ERRORS = (
    FileNotFoundError,
    PermissionError,
    UnicodeDecodeError,
    json.JSONDecodeError,
)


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_rendered_prompt(text: str) -> dict[str, str]:
    system, separator, user = text.partition("\n\n")
    if not separator:
        return {"system": "", "user": text}
    return {"system": system.rstrip(), "user": user.rstrip()}


def prompt_from_artifacts(item: dict[str, object], summary_path: Path | None) -> dict[str, str]:
    prompt = item.get("prompt")
    if isinstance(prompt, dict):
        return {
            "system": str(prompt.get("system") or ""),
            "user": str(prompt.get("user") or ""),
        }

    system_prompt = item.get("system_prompt")
    user_prompt = item.get("user_prompt")
    if isinstance(system_prompt, str) or isinstance(user_prompt, str):
        return {
            "system": str(system_prompt or ""),
            "user": str(user_prompt or ""),
        }

    artifact_base = item.get("artifact_base") or item.get("artifactBase")
    if not isinstance(artifact_base, str) or not artifact_base:
        return {"system": "", "user": ""}

    base = Path(artifact_base)
    candidates = [base.with_name(base.name + "__02_rendered-prompt.txt")]
    if summary_path is not None and not base.is_absolute():
        candidates.append((summary_path.parent / base).with_name(base.name + "__02_rendered-prompt.txt"))
        candidates.append((summary_path.parent.parent / base).with_name(base.name + "__02_rendered-prompt.txt"))

    for candidate in candidates:
        if candidate.exists():
            return split_rendered_prompt(candidate.read_text(encoding="utf-8"))

    return {"system": "", "user": ""}


def artifact_paths(item: dict[str, object], summary_path: Path | None) -> dict[str, Path]:
    artifact_base = item.get("artifact_base") or item.get("artifactBase")
    if not isinstance(artifact_base, str) or not artifact_base:
        return {}
    base = Path(artifact_base)
    names = {
        "request": "__01_request.json",
        "renderedPrompt": "__02_rendered-prompt.txt",
        "rawResponse": "__03_raw-response.json",
        "responseText": "__04_response-text.txt",
        "parsedOutput": "__05_parsed-output.json",
        "metrics": "__06_metrics.json",
    }
    if summary_path is not None and not base.is_absolute():
        candidates = [
            base,
            Path.cwd() / base,
            summary_path.parent / base,
            summary_path.parent.parent / base,
        ]
        for candidate in candidates:
            raw_candidate = candidate.with_name(candidate.name + names["rawResponse"])
            if raw_candidate.exists():
                base = candidate
                break
    return {key: base.with_name(base.name + suffix) for key, suffix in names.items()}


def provider_metadata(item: dict[str, object], summary_path: Path | None) -> dict[str, object]:
    model = item.get("model")
    token_usage = item.get("token_usage") or item.get("tokenUsage")

    paths = artifact_paths(item, summary_path)
    raw_path = paths.get("rawResponse")
    if raw_path and raw_path.exists():
        try:
            raw = load_json(raw_path)
            if isinstance(raw, dict):
                model = model or raw.get("model")
                usage = raw.get("usage")
                if token_usage is None and isinstance(usage, dict):
                    token_usage = usage
        except EXPECTED_ARTIFACT_LOAD_ERRORS as exc:
            print(f"Warning: could not load provider metadata from {raw_path}: {exc}", file=sys.stderr)

    request = item.get("request_without_secret") or item.get("requestWithoutSecret")
    if not isinstance(request, dict):
        paths = artifact_paths(item, summary_path)
        request_path = paths.get("request")
        if request_path and request_path.exists():
            try:
                loaded = load_json(request_path)
                request = loaded if isinstance(loaded, dict) else {}
            except EXPECTED_ARTIFACT_LOAD_ERRORS as exc:
                print(f"Warning: could not load request metadata from {request_path}: {exc}", file=sys.stderr)
                request = {}

    return {
        "model": model,
        "tokenUsage": token_usage if isinstance(token_usage, dict) else None,
        "maxOutputTokens": request.get("max_output_tokens") if isinstance(request, dict) else item.get("max_output_tokens"),
    }


def artifact_trace(item: dict[str, object], summary_path: Path | None) -> dict[str, object]:
    paths = artifact_paths(item, summary_path)
    refs = {}
    hashes = {}
    for key, path in paths.items():
        refs[key] = str(path)
        hashes[key] = sha256_file(path)
    return {
        "artifactBase": item.get("artifact_base") or item.get("artifactBase"),
        "artifactRefs": refs,
        "artifactSha256": hashes,
        "provenance": "lab_runner_artifact_set",
    }


def build_from_summary(summary: dict[str, object], summary_path: Path | None = None) -> dict[str, object]:
    variants = summary.get("variants", [])
    cases = summary.get("cases", [])
    results = summary.get("results", [])
    by_case: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in results if isinstance(results, list) else []:
        if isinstance(item, dict):
            by_case[str(item.get("case_id") or item.get("caseId") or "")].append(item)

    surface_cases = []
    for case in cases if isinstance(cases, list) else []:
        if not isinstance(case, dict):
            continue
        case_id = str(case.get("id"))
        surface_results = []
        for item in by_case.get(case_id, []):
            variant_id = str(item.get("variant_id") or item.get("variantId"))
            provider_meta = provider_metadata(item, summary_path)
            surface_results.append(
                {
                    "caseId": case_id,
                    "variantId": variant_id,
                    "variantShortLabel": variant_id.split("_", 1)[0],
                    "variantLabel": item.get("variant_label") or item.get("variantLabel") or variant_id,
                    "providerRoute": item.get("provider_route") or item.get("providerRoute"),
                    "model": provider_meta["model"],
                    "tokenUsage": provider_meta["tokenUsage"],
                    "maxOutputTokens": provider_meta["maxOutputTokens"],
                    "durationMs": item.get("duration_ms") or item.get("durationMs"),
                    "parsedOk": item.get("parsed_ok") if "parsed_ok" in item else item.get("parsedOk"),
                    "parseError": item.get("parse_error") or item.get("parseError"),
                    "metrics": item.get("metrics") or {},
                    "prompt": prompt_from_artifacts(item, summary_path),
                    "responseText": item.get("response_text") or item.get("responseText") or "",
                    "parsedOutput": item.get("parsed_output") or item.get("parsedOutput"),
                    "artifactBase": item.get("artifact_base") or item.get("artifactBase"),
                    "trace": artifact_trace(item, summary_path),
                }
            )
        surface_cases.append(
            {
                "id": case_id,
                "companyName": case.get("companyName") or case.get("company_name") or case_id,
                "results": surface_results,
            }
        )

    variant_ids = [item.get("id") for item in variants if isinstance(item, dict)]
    left = variant_ids[0] if variant_ids else "A_current"
    right = variant_ids[-1] if len(variant_ids) > 1 else "B_candidate"
    review_data = {
        "title": summary.get("experiment") or "Pre-Spec Prompt A/B Review",
        "kicker": "Pre-Spec Prompt Review",
        "heroTitleHtml": "Prompt-Runde: <em>A gegen B</em>",
        "lede": "Kompaktes Briefing für Prompt-Contract, echte Provider-Rückgabe, Review-Metriken und HITL-Entscheidung.",
        "evidenceClass": summary.get("evidence_class") or "pre_spec_prompt_ab",
        "leftVariantId": left,
        "defaultCaseId": surface_cases[0]["id"] if surface_cases else "",
        "defaultRightVariant": right,
        "sourcePromptContract": summary.get("source_prompt_contract"),
        "sourceFoundation": summary.get("source_foundation"),
        "testsetSource": summary.get("testset_source"),
        "outputViewMode": "tree_only",
        "outputTreeDefaultExpanded": "all",
        "recommendation": {
            "label": "Empfehlung",
            "title": "HITL-Entscheidung erforderlich",
            "body": "Die HTML-Fläche visualisiert Evidence. Die Entscheidung bleibt im Markdown-Ledger.",
        },
        "notProven": {
            "label": "Nicht bewiesen",
            "items": summary.get("not_proven") or ["production_readiness"],
        },
        "variants": variants,
        "cases": surface_cases,
        "interpretationNotes": {},
    }
    if isinstance(summary.get("assistant_evaluation"), dict):
        review_data["assistantEvaluation"] = summary["assistant_evaluation"]
    if isinstance(summary.get("iteration_path"), list):
        review_data["iterationPath"] = summary["iteration_path"]
    return review_data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--assistant-evaluation", type=Path)
    parser.add_argument("--iteration-path", type=Path)
    args = parser.parse_args()

    summary = load_json(args.results)
    if not isinstance(summary, dict):
        raise SystemExit("results summary must be a JSON object")
    if args.assistant_evaluation:
        evaluation = load_json(args.assistant_evaluation)
        if not isinstance(evaluation, dict):
            raise SystemExit("assistant evaluation must be a JSON object")
        summary["assistant_evaluation"] = evaluation
    if args.iteration_path:
        iteration_path = load_json(args.iteration_path)
        if not isinstance(iteration_path, list):
            raise SystemExit("iteration path must be a JSON array")
        summary["iteration_path"] = iteration_path
    data = build_from_summary(summary, args.results)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
