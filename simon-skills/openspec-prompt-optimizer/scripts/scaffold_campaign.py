#!/usr/bin/env python3
"""Scaffold a Pre-Spec prompt optimization campaign folder."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from datetime import datetime
from pathlib import Path


SHARED_EXTRACTOR = Path.home() / ".codex/skills/shared/scripts/extract_prompt_contracts_from_foundation.py"


def load_extractor():
    spec = importlib.util.spec_from_file_location("prompt_extractor", SHARED_EXTRACTOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load shared extractor: {SHARED_EXTRACTOR}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-").lower()
    return value or "openspec-prompt-optimization"


def normalize(text: str) -> str:
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def source_day_dir(source: Path) -> Path:
    parts = source.resolve().parts
    for idx, part in enumerate(parts):
        if part == "docs" and idx + 2 < len(parts) and parts[idx + 1] == "todo":
            return Path(*parts[: idx + 3])
    today = datetime.now().strftime("%Y_%m_%d")
    return Path("docs") / "todo" / today


def next_prefix(day_dir: Path) -> int:
    max_prefix = 0
    if day_dir.exists():
        for path in day_dir.rglob("[0-9][0-9][0-9]_*"):
            match = re.match(r"^(\d{3})_", path.name)
            if match:
                max_prefix = max(max_prefix, int(match.group(1)))
    return max_prefix + 1


def write_if_missing(path: Path, text: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--campaign", type=Path)
    args = parser.parse_args()

    source = args.source
    text = source.read_text(encoding="utf-8")
    extractor = load_extractor()
    blocks = extractor.discover_prompt_blocks(text)
    if not blocks:
        raise SystemExit("No canonical prompt blocks found.")

    day_dir = source_day_dir(source)
    timestamp = datetime.now().strftime("%Y_%m_%d__%H-%M")
    campaign = args.campaign
    if campaign is None:
        prefix = next_prefix(day_dir)
        campaign = day_dir / "07_experiments" / f"{prefix:03d}_openspec-prompt-optimization-{slugify(args.slug)}__{timestamp}"
    campaign.mkdir(parents=True, exist_ok=True)

    ops = []
    for block in blocks:
        op = block.operation_id
        safe = slugify(op)
        block_hash = hashlib.sha256(normalize(block.payload).encode("utf-8")).hexdigest()[:16]
        ops.append(
            {
                "operation_id": op,
                "source_locator": block.source_locator,
                "source_block_hash": block_hash,
                "provider_route": block.frontmatter.get("llm_route", ""),
                "llm_provider": block.frontmatter.get("llm_provider", ""),
                "status": "scope_pending",
            }
        )
        write_if_missing(
            campaign / "02_operation-profiles" / f"{safe}.md",
            f"""# Operation Profile: `{op}`

| Feld | Wert |
|---|---|
| Operation | `{op}` |
| Source Locator | `{block.source_locator}` |
| Source Block Hash | `{block_hash}` |
| Provider Route | `{block.frontmatter.get("llm_route", "")}` |
| LLM Provider | `{block.frontmatter.get("llm_provider", "")}` |

## Scope

`scope_status`: `scope_pending`

## Must-Survive-Facts

- TBD

## Known Risks

- TBD
""",
        )

    state = {
        "schema_version": 1,
        "source": str(source),
        "campaign": str(campaign),
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "current_phase": "scope_register",
        "operations": ops,
        "rounds": [],
        "approvals": [],
    }
    write_if_missing(campaign / "campaign-state.json", json.dumps(state, ensure_ascii=False, indent=2))
    write_if_missing(
        campaign / "00_prompt-optimization-overview.md",
        "# Prompt Optimization Overview\n\n"
        f"Source: `{source}`\n\n"
        "| Operation | Source Hash | Scope | Final Hash | HITL | Write-back |\n"
        "|---|---|---|---|---|---|\n"
        + "\n".join(
            f"| `{op['operation_id']}` | `{op['source_block_hash']}` | `scope_pending` |  |  |  |"
            for op in ops
        )
        + "\n",
    )
    write_if_missing(
        campaign / "01_prompt-scope-register.md",
        "# Prompt Scope Register\n\n"
        "| Operation | Provider Route | Scope Status | Scope Reason |\n"
        "|---|---|---|---|\n"
        + "\n".join(
            f"| `{op['operation_id']}` | `{op['provider_route']}` | `scope_pending` | TBD |"
            for op in ops
        )
        + "\n",
    )
    write_if_missing(campaign / "04_hitl-decisions.md", "# HITL Decisions\n\n")
    write_if_missing(campaign / "06_open-issues.md", "# Open Issues\n\n")
    (campaign / "03_rounds").mkdir(exist_ok=True)
    (campaign / "05_writeback").mkdir(exist_ok=True)
    (campaign / "html" / "assets").mkdir(parents=True, exist_ok=True)
    print(campaign)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
