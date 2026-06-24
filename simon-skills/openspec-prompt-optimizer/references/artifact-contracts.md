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
  "goalProgress": {
    "label": "Stand der Zielerreichung",
    "title": "Rundenziel messbar; finale Produktentscheidung bleibt HITL.",
    "summary": "What the round tried to achieve, how much closer it got, what remains open.",
    "metrics": [],
    "items": []
  },
  "overallAnalysis": {
    "label": "Overall-Endurteil",
    "title": "Gesamtbefund über alle Cases",
    "summary": "Cross-case interpretation for the next iteration.",
    "metrics": [],
    "items": []
  },
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

For reviewable A/B rounds, the adapter should also write the shared
decision-support contract. Missing evidence must be represented as
`not_available`, `neutral`, `inconclusive`, or an empty list; never invent
content just to fill the template.

```json
{
  "testIntent": {
    "label": "Testdesign",
    "title": "What this A/B round is actually testing",
    "intent": "round-level test intent",
    "expected_behavior": "expected behavior across the test set"
  },
  "cases": [
    {
      "id": "case-id",
      "testIntent": {
        "title": "case-level test intent",
        "intent": "what this case is meant to prove or falsify",
        "expected_behavior": "what the better variant should do",
        "expected": {
          "preflight_action": "proceed|warn_confirm|cannot_use",
          "needs_user_confirmation": true,
          "is_good_analysis_start": false
        },
        "watch_for": "failure mode to watch"
      }
    }
  ],
  "decisionScorecard": {
    "provenance": "derived_from_metric_matrix",
    "primary": {
      "status": "green|yellow|red|neutral",
      "summary": "neutral comparison summary",
      "recommendedVariant": "variant-id|none|inconclusive"
    },
    "guardrails": {
      "status": "green|red|neutral",
      "blockingGuardrails": []
    },
    "monitoring": {
      "status": "info",
      "summary": "tokens/runtime/cost are side-effect evidence"
    },
    "evidenceCompleteness": {
      "status": "green|yellow|red",
      "summary": "trace completeness summary"
    },
    "decisionState": {
      "status": "hitl_required",
      "summary": "Promotion remains HITL"
    },
    "reviewerAttention": []
  },
  "traceIntegrity": {
    "provenance": "lab_runner_artifact_set",
    "status": "pass|fail|not_available",
    "expectedArtifacts": [
      "request",
      "renderedPrompt",
      "rawResponse",
      "responseText",
      "parsedOutput",
      "metrics"
    ],
    "summary": "short trace completeness summary",
    "items": []
  },
  "hitlDecision": {
    "provenance": "pending_hitl_decision|markdown_decision_ledger_or_summary",
    "status": "pending|decided",
    "decision": "promote_candidate|iterate_same_lever|change_lever|split_decision|reject|inconclusive|null",
    "hitl_required": true
  },
  "preflightChecks": {
    "provenance": "deterministic_prompt_preflight",
    "status": "green|yellow|red|neutral",
    "variants": {},
    "items": [
      {
        "caseId": "case-id",
        "variantId": "variant-id",
        "status": "green|yellow|red",
        "providerFit": {},
        "simplicity": {},
        "hardcodingScan": {},
        "antiOverfit": {},
        "generalization": {}
      }
    ]
  },
  "assistant_recommendation": {
    "provenance": "assistant_recommendation_from_metric_matrix",
    "recommended_variant": "A|B|none|inconclusive|variant-id",
    "recommendation_type": "promote_candidate|keep_baseline|iterate_candidate|reject_candidate|rerun_needed|hitl_required",
    "confidence": "low|medium|high",
    "rationale_short": "short neutral recommendation",
    "blocking_guardrails": [],
    "hitl_required": true
  },
  "decisionMetrics": {
    "label": "Metrik-Auswertung",
    "title": "Prompt-A/B: Pflichtmetriken im Spinnennetz",
    "note": "Radar and detail cards are assistant_review decision support, not automatic promotion gates.",
    "provenance": "assistant_review",
    "axes": [
      {
        "id": "round_goal_fit",
        "label": "Rundenziel-Fit",
        "shortLabel": "Ziel",
        "description": "What this axis evaluates."
      }
    ],
    "cases": {
      "case-id": {
        "primarySentences": [],
        "variants": {
          "variant-id": {
            "scores": {},
            "values": {},
            "interpretations": {}
          }
        },
        "guardrails": [],
        "monitoring": []
      }
    }
  },
  "metricMatrix": [
    {
      "id": "round_goal_fit",
      "group": "primary|guardrail|monitoring|assistant_review",
      "label": "Rundenziel",
      "meaning": "what this row evaluates",
      "provenance": "provider_runtime_metric|assistant_review|lab_runner_artifact_set|metric_proxy_or_not_available",
      "values": {
        "variant-id": {
          "score": 4.7,
          "rawValue": null,
          "display": "4,7 von 5",
          "status": "green|yellow|red|neutral"
        }
      }
    }
  ],
  "interpretationNotes": {
    "case-id": {
      "contentTitle": "Was wir im Chat klären müssen",
      "content": [
        "Round-goal, evidence, downstream, and write-back questions for this case."
      ],
      "riskTitle": "Risiko",
      "risk": "short risk note",
      "nextTitle": "Nächster sinnvoller Schritt",
      "next": "short next step"
    },
    "primary": [],
    "guardrails": [],
    "monitoring": [],
    "assistant_review": [],
    "assistant_recommendation": {
      "recommended_variant": "variant-id|none|inconclusive",
      "summary": "short recommendation",
      "hitl_required": true
    }
  }
}
```

`testIntent` and `cases[].testIntent` are the review contract for intent,
expected behavior, and failure criteria. They are authored before or during
testset assembly. Observed behavior is not hand-authored there; the HTML derives
it from `cases[].results[].parsedOutput`, metrics, and trace evidence. If
expected behavior is unknown, say so explicitly instead of filling the template
with generic copy.

`goalProgress`, `overallAnalysis`, and `interpretationNotes[case-id]` are
decision scaffolding for Simon's chat review. They must be derived from visible
round evidence, metric matrix, assistant review, or explicitly marked open
questions. They are not provider output and must not be represented as runtime
truth.

`decisionMetrics` is the render-ready companion to `metricMatrix`. The builder
must derive it automatically for reviewable A/B rounds so the spider chart,
metric cards, inline details, guardrails and monitoring can render without
round-local JavaScript enrichment. Human-written copy may override generated
phrasing, but scores and values must remain traceable to provider metrics,
`metricMatrix`, trace artifacts, or explicit `assistant_review`.
Render-facing five-point score text uses natural labels: whole-number scores are
written as `5 von 5`, while fractional values keep one meaningful decimal such
as `4,7 von 5`. Avoid `5.0/5`, `5,0/5`, or `5,0 von 5` in display fields.

`assistant_recommendation` is a recommendation only. The final promotion state
must be recorded as HITL in the Markdown decision ledger.

`traceIntegrity` is the compact surface-level summary. The stricter verifier
report from `verify_review_surface_trace.py` still decides whether the HTML can
be presented as valid evidence.

`preflightChecks` are deterministic review evidence for provider fit,
simplicity, anti-overfit/hardcoding risk and generalization evidence. A red
preflight finding does not rewrite provider results, but it must be fixed or
accepted in the decision ledger before write-back.

`cases[].results[].prompt.system` and `cases[].results[].prompt.user` must be
filled. The adapter should read these from the result summary when present or
recover them from `<case>__<variant>__02_rendered-prompt.txt`.

The default HTML load state is decision-first: `Endurteil` / `Stand der
Zielerreichung` stays open, while Header, Prompt run-lanes, Metrik-Auswertung,
and Evidence Map start compact. Prompt text, provider response, parsed output,
and trace data must still be present in the DOM or reachable through the
collapse/maximize controls.

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

The canonical interactive Sanctum/OpenSpec review UI is the React route:

```text
http://localhost:3000/app/review/prompt-ab?path=<urlencoded relative path to html/assets/data.json>
```

Use this route first whenever the dev server is available. It reads the same
`html/assets/data.json` payload and is the place where durable UI behavior
belongs.

Static `html/index.html` is an export/archive snapshot or offline fallback. If
it is rendered, the agent must ask Simon whether to open the static surface.

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
