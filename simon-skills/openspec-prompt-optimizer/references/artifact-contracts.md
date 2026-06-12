# Artifact Contracts

## Round Folder

Each real round lives under the campaign:

```text
03_rounds/
  round-N-<lever>/
    01_experiment-brief.md
    02_b-mechanism.md
    03_prompt-schema-architecture-review.md
    04_testset-ledger.md
    05_run-ledger.md
    06_comparison-matrix.md
    07_decision.md
    08_vault-learning.md
    09_review-surface.md
    10_trace-measurement.md
    11_improvement-levers.md
    artifacts/cases/
    html/index.html
    html/assets/data.json
```

## Case Artifact Set

Each provider/fixture run writes:

```text
<case>__<variant>__01_request.json
<case>__<variant>__02_rendered-prompt.txt
<case>__<variant>__03_raw-response.json
<case>__<variant>__04_response-text.txt
<case>__<variant>__05_parsed-output.json
<case>__<variant>__06_metrics.json
```

The request file never contains authorization headers or secrets.

## Metrics

The standard metrics file contains:

```json
{
  "schema_ok": true,
  "parse_error": null,
  "related_count": 3,
  "source_ref_count": 8,
  "first_party_source_ref_count": 8,
  "citation_marker_count": 0,
  "example_leak_count": 0,
  "strings_with_citation_markers": [],
  "example_leak_strings": [],
  "source_ref_urls": [],
  "duration_ms": 0
}
```

Additional domain metrics may be added, but the standard keys should stay
stable so comparison matrices and HTML adapters keep working.

## Review Surface Data

Use the existing shared schema from:

```text
~/.codex/skills/shared/templates/openspec-prompt-improver/assets/data.template.json
```

Diagnostic metadata such as lever, diagnosis class, and gate status should be
written into Markdown ledgers and into existing text fields like
`recommendation.body` or `interpretationNotes`.

If the round needs a radar/spider chart or feedback carry-forward, the adapter
may add these optional display-only keys:

```json
{
  "assistantEvaluation": {
    "provenance": "assistant_review",
    "scale": { "min": 0, "max": 5, "label": "0 = weak, 5 = strong" },
    "standardAxes": [],
    "contextAxes": [],
    "cases": {
      "case-id": {
        "variants": {
          "variant-id": {
            "standard": {},
            "context": {}
          }
        }
      }
    }
  },
  "iterationPath": []
}
```

These keys are review support, not provider metrics. They must be agreed in
chat or clearly marked as Codex `assistant_review`, and Simon/HITL feedback can
override them in the next round.

`cases[].results[].prompt.system` and `cases[].results[].prompt.user` must be
filled. The adapter should read these from the result summary when present or
recover them from `<case>__<variant>__02_rendered-prompt.txt`.

The output comparison panels open expanded by default. System/User prompt panels
may stay collapsed by default, but the prompt text must still be present in the
DOM and available through the maximize controls.

Each result should include trace provenance for the six lab-runner artifacts:

```text
request
renderedPrompt
rawResponse
responseText
parsedOutput
metrics
```

The HTML may display these as paths and `sha256` hashes. The hashes are review
evidence, not a substitute for the underlying files.

Each result may also include observed provider metadata from the raw response:
`model`, `tokenUsage`, and `maxOutputTokens`. If the provider does not return
token usage, keep the field empty or `n/a`; never estimate token counts.

Before browser handoff, run:

```bash
python ~/.codex/skills/openspec-prompt-optimizer/scripts/verify_review_surface_trace.py \
  --results <round>/artifacts/results-summary.json \
  --data <round>/html/assets/data.json \
  --out <round>/artifacts/trace-integrity-report.json
```

If the report status is not `pass`, do not present the HTML as valid evidence.

## JSON Tree Review

The shared HTML review surface should render parseable `parsedOutput` values as
a foldable JSON tree, with object key counts, array lengths, scalar values and a
large-array guard. Raw/Code text remains available as provenance and fallback.

## Review Surface Browser Handoff

After `html/index.html` is rendered, the agent must ask Simon whether to open
the surface.

In WSL2 on Windows, the browser handoff must use a file URI:

```text
file://///wsl.localhost/<distro>/home/simon/projects/.../html/index.html
```

Raw UNC paths can be interpreted by Firefox as `https://wsl.localhost/...`,
which does not open the WSL file. Use:

```bash
python ~/.codex/skills/openspec-prompt-optimizer/scripts/open_review_surface.py \
  <round>/html/index.html \
  --browser firefox
```

## Decision States

Round decisions:

```text
promote_candidate
iterate_same_lever
change_lever
split_decision
reject
inconclusive
```

Campaign write-back states:

```text
not_started
approved_pending_writeback
written
hold
stale
```
