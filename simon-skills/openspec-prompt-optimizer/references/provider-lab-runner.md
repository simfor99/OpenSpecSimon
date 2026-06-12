# Provider Lab Runner

## Purpose

The Lab Runner executes Pre-Spec prompt candidates without pretending to be the
production Stage runner. It is a thin evidence harness:

- render system/user prompt variables from a case JSON;
- send the prompt to the selected provider surface or use a labeled fixture;
- write request/raw/text/parsed/metrics artifacts;
- keep provider behavior visible for HITL review.

## Perplexity Agent API

For Perplexity/Search operations, prefer the Agent API surface when the prompt
needs web research with tool-loop behavior:

```bash
python ~/.codex/skills/openspec-prompt-optimizer/scripts/lab_runner.py \
  --surface perplexity-agent \
  --case case.json \
  --variant-id B2_provider_fit_compact \
  --system system.txt \
  --user user.txt \
  --domain-filter babtec.de \
  --expected-object product_world_context \
  --expected-host babtec.de \
  --out-dir round-01/artifacts/cases
```

Environment:

```text
PERPLEXITY_API_KEY
```

The request stored on disk omits the authorization header.

## Fixture Mode

Use fixture mode for script validation, replay, or cost-free development:

```bash
python scripts/lab_runner.py \
  --surface fixture \
  --fixture-response response.txt \
  --case case.json \
  --variant-id A_current \
  --system system.txt \
  --user user.txt \
  --expected-object product_world_context \
  --out-dir artifacts/cases
```

Fixture evidence must be labeled as fixture evidence in the round ledgers. It
cannot prove provider behavior or production readiness.

## Provider Profiles

- `llm_provider: perplexity` or `llm_route: perplexity_*` -> `perplexity_sonar`.
- `llm_provider: admin_configured` -> runtime profile if known.
- Unknown model -> `generic_llm` plus an explicit uncertainty note.

When delegating analysis to `$prompt-improver`, pass the selected profile
explicitly. A generic call loses provider-specific failure modes.
