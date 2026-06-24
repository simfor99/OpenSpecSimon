---
name: openspec-prompt-optimizer
version: "1.0.0-sanctum"
bundle: openspec-simon
bundle_version: "2026.06.24.1"
description: "Use to optimize fenced Pre-Spec or Foundation-Brief prompt contracts with HITL A/B evidence, fixtures, write-back, and resume state."
argument-hint: "[foundation-brief-path] [--campaign docs/todo/.../07_experiments/... optional]"
disable-model-invocation: false
allowed-tools: Read, Write, Bash, Grep, Glob
---
<!-- TOKEN_BUDGET: 15000 -->

# OpenSpec Prompt Optimizer

This skill turns a Foundation Brief / Pre-Spec Zielbild with fenced prompt
contracts into a resumable HITL prompt-optimization campaign. Markdown ledgers
remain the source of truth; `html/assets/data.json` is the review data
contract; the React route `/app/review/prompt-ab?path=...` is the canonical
interactive review surface. Static `html/index.html` is only an export,
archive snapshot, or offline fallback.

## When to Use

Use this skill when Simon wants to:

- optimize embedded Foundation-Brief prompt contracts before `$openspec-map` or
  `$openspec-propose`;
- run A/B prompt rounds with real provider evidence instead of simulated agent
  output;
- compare current prompt A against B/B2/B3 while preserving prompt, schema,
  route, input, output, and downstream boundaries;
- keep Perplexity/Search operations separate from standard admin-routed LLM
  operations;
- write an accepted prompt contract back into the original Pre-Spec safely;
- resume a multi-round campaign after a session break.

Do not use this skill for already-promoted production Stage tests. Use the GTM
Evidence Lab / workflow-stage-test path there.

## Process

1. **Load the process contract.** Read the source Foundation Brief and the
   canonical resource:
   `docs/todo/2026_06_04/06_resources/056_prespec-prompt-optimization-hitl-loop__resource__2026_06_10__20-58.md`.
   For Sanctum daily work, keep the active day-space from the source artifact.

2. **Discover prompt contracts.** Run the shared extractor in check mode:
   `python ~/.codex/skills/shared/scripts/extract_prompt_contracts_from_foundation.py --source <brief> --check`.
   If no canonical blocks are found, stop; free-form prompt prose is not safe to
   optimize.

3. **Create or resume the campaign.** Use:
   `python ~/.codex/skills/openspec-prompt-optimizer/scripts/scaffold_campaign.py --source <brief> --slug <slug>`.
   If `--campaign` is supplied or a campaign state already exists, load
   `campaign-state.json` and continue from the next incomplete phase.

4. **Build the scope register.** Classify every operation as `optimize`,
   `sanity_check`, `downstream_impact_check`, `defer_until_upstream_stable`, or
   `out_of_scope`. Ask Simon only for real scope decisions; keep trivial
   formatting and metric choices local.

5. **Choose provider profile per operation.** Perplexity/Search routes use
   `perplexity_sonar`. Admin-configured LLM routes use the runtime profile if
   known, otherwise `generic_llm` and a visible uncertainty note. Pass that
   profile explicitly when delegating to `$prompt-improver`. When a rendered
   prompt is available, run the deterministic preflight:
   `python scripts/preflight_prompt_contract.py --prompt <rendered-prompt.txt> --variant-id <id> --provider-route <route> --out <round>/artifacts/preflight/<case>__<variant>.json`.
   It checks provider fit, simplicity, anti-overfit/hardcoding risk and
   generalization evidence. It is review evidence, not automatic promotion.

6. **Run baseline and variants through the Lab Runner.** Use real provider
   calls when evidence class requires provider behavior:
   `python scripts/lab_runner.py --case <case.json> --variant-id A_current --system <system.txt> --user <user.txt> --out-dir <round>/artifacts/cases`.
   Fixture runs are allowed only when clearly labeled `fixture_core`.

7. **Agree review dimensions before rendering.** After the first evidence pass,
   propose standard axes plus round-specific focus metrics in chat. Do not hide
   this as a template default. Once Simon agrees, store the final axes and
   scores as `assistant_review` evidence, separate from provider/runtime facts.
   User feedback becomes `must_survive`, `must_reject`, `evaluation_focus`, or
   `investigation_question` in the iteration path and must influence the next
   round.

8. **Measure and prepare the canonical review surface.** Parse provider
   returns, write request/raw/text/parsed/metrics artifacts, then build
   `html/assets/data.json` via `build_review_surface_data.py`. Treat this file
   as the single UI data contract for both React and static export.
   The data payload must include the shared decision-support contract when the
   evidence allows it: `goalProgress`, `overallAnalysis`, `decisionScorecard`,
   `assistant_recommendation`, `metricMatrix`, `decisionMetrics`,
   `interpretationNotes`, `iterationPath`, `traceIntegrity`, `hitlDecision`,
   `preflightChecks`, and the test-design fields `testIntent` /
   `cases[].testIntent` when the round has explicit expectations.
   `metricMatrix` is the typed comparison ledger; `decisionMetrics` is the
   render-ready spider/scorecard bundle derived from the same evidence. Do not
   hand-create `decisionMetrics` unless you are adding explicit
   `assistant_review` overrides; the builder must be able to derive a usable
   default from cases, variants, metrics, trace, and assistant axes.
   `goalProgress` answers what the round tried to achieve, whether it moved
   closer to that goal, what remains open, and what must happen next.
   `cases[].testIntent` answers what the selected case is testing, what
   behavior was expected, and what would count as a failure. The observed
   behavior must still come from `parsedOutput`, metrics, and trace artifacts;
   never write a manual "observed" claim that contradicts the provider output.
   `interpretationNotes[case-id]` should include case-level decision prompts
   such as `contentTitle: "Was wir im Chat klären müssen"` and a `content`
   list for the open questions Simon should discuss. These fields are display
   and recommendation support; they do not replace the Markdown ledger or HITL
   decision.
   Before showing any review surface, verify that each
   `cases[].results[].prompt.system`
   and `.prompt.user` is non-empty in `html/assets/data.json`; if not, rebuild
   from `*__02_rendered-prompt.txt` artifacts or stop.
   Run `verify_review_surface_trace.py` against `results-summary.json` and
   `html/assets/data.json`; if request, rendered prompt, response text, parsed
   output, metrics, or surface payload diverge from the artifact set, stop.
   Open the React route `/app/review/prompt-ab?path=<urlencoded relative path
   to html/assets/data.json>` as the primary review UI when the Sanctum dev
   server is available. Render static `html/index.html` with
   `render_prompt_ab_review_surface.py` only as an archive/export snapshot or
   when the app route is unavailable. If Simon asks for visual, layout,
   collapse, navigation, theme, or interaction changes, apply them to the React
   route first; static HTML may follow only after the React route is green.
   If a static snapshot is opened in WSL2 on Windows, never pass a raw UNC path
   to Firefox; use
   `scripts/open_review_surface.py <round>/html/index.html --browser firefox`
   so the path becomes `file://///wsl.localhost/<distro>/...`.

9. **HITL decision.** Show Simon the HTML path and the Markdown round ledgers.
   Record exactly one round decision:
   `promote_candidate`, `iterate_same_lever`, `change_lever`,
   `split_decision`, `reject`, or `inconclusive`.

10. **Respect chaining.** Optimize operations in topological order. Downstream
   rounds use frozen `chained_fixture` outputs from the accepted upstream
   operation. A final downstream approval also needs at least one live chained
   run. Upstream write-back after downstream approval marks the downstream
   approval `stale`.

11. **Write back only after approval.** Save the approved full fenced block in
    `05_writeback/`, then run:
    `python ~/.codex/skills/shared/scripts/rewrite_prompt_contract_block_in_foundation.py --source <brief> --operation-id <op> --candidate <approved-block> --out <brief> --ledger <ledger.md>`.
    No LLM edits the source brief by hand.

## Quick Reference

| Need | Command |
|---|---|
| Scaffold campaign | `python scripts/scaffold_campaign.py --source <brief> --slug <slug>` |
| Provider run | `python scripts/lab_runner.py --case <case.json> --variant-id <id> --system <system.txt> --user <user.txt> --out-dir <dir>` |
| Metrics only | `python scripts/evaluate_prompt_run.py --response-text <txt> --expected-object <name> --expected-host <host>` |
| Prompt preflight | `python scripts/preflight_prompt_contract.py --prompt <rendered-prompt.txt> --variant-id <id> --provider-route <route> --out <round>/artifacts/preflight/<case>__<variant>.json` |
| Build review data | `python scripts/build_review_surface_data.py --results <results-summary.json> --out <round>/html/assets/data.json` |
| Verify surface trace | `python scripts/verify_review_surface_trace.py --results <results-summary.json> --data <round>/html/assets/data.json --out <round>/artifacts/trace-integrity-report.json` |
| Open canonical React review | `/app/review/prompt-ab?path=<round>/html/assets/data.json` |
| Render/open static snapshot | `python ~/.codex/skills/shared/scripts/render_prompt_ab_review_surface.py --data <round>/html/assets/data.json --out <round>/html/index.html` then `python scripts/open_review_surface.py <round>/html/index.html --browser firefox` |
| Write-back | `python ~/.codex/skills/shared/scripts/rewrite_prompt_contract_block_in_foundation.py ...` |

## Operating Rules

- Markdown ledgers are canonical; HTML never hides the only decision.
- The React route `/app/review/prompt-ab` is the canonical interactive review
  UI. Static `html/index.html` is an export/archive snapshot, not the product
  surface and not the place to land durable UI improvements first.
- UI changes follow React-first order: update the React route, verify it
  against `html/assets/data.json`, then optionally update the static snapshot
  template for offline parity.
- One variant changes one main lever. If prompt, schema, provider, testset, and
  runtime all change together, the result is a system redesign, not a prompt
  A/B round.
- Parse/schema success is a guardrail, not proof of semantic quality.
- Must-Survive-Facts and Must-Reject leaks are decision inputs.
- Class C fields (`operation_id`, route, provider/model source, input blocks,
  output objects) do not change silently. If they need to change, stop for a
  Simon/OpenSpec decision.
- Perplexity `source_refs` are provenance, not crawl candidates.
- Requests are stored without authorization headers or secrets.
- Review HTML must expose trace provenance for each result: request, rendered
  prompt, raw response, response text, parsed output, metrics, and hashes.
- Radar/spider charts are `assistant_review` decision support, not provider
  metrics and not automatic promotion gates. They must show provenance, use
  agreed axes, and remain overridable by Simon/HITL feedback.
- `assistant_recommendation` is required for reviewable A/B rounds. It is
  neutral: it may recommend the candidate, keep baseline A, reject all
  variants, request a rerun, or mark the outcome inconclusive. It must set
  `hitl_required: true`; promotion is never automatic.
- Primary rows are neutral. They answer which variant, if any, fulfills the
  round goal better. Never phrase Primary as "why B wins"; B may be worse than
  A or blocked by guardrails.
- `metricMatrix` rows must keep roles separate: `primary`, `guardrail`,
  `monitoring`, and `assistant_review`. Red guardrails dominate green primary
  metrics. Monitoring explains cost, latency, token use, and side effects; it
  is not a quality proof unless the round explicitly optimizes budget/runtime.
- `decisionMetrics` must be present for reviewable A/B rounds and must be
  renderable without a round-local enrichment script. It may use generic
  fallback wording when case-specific copy is unavailable, but scores and
  values must come from `metricMatrix`, provider metrics, trace artifacts, or
  explicitly supplied `assistant_review` axes.
- `preflightChecks` cover provider fit, simplicity, anti-overfit/hardcoding
  risk and generalization evidence. They are reviewer-attention evidence. They
  do not override observed provider output, but a red preflight finding must be
  resolved or explicitly accepted before write-back.
- Multi-round or multi-case campaigns must record generalization evidence:
  eval-suite hash when evaluation files exist, train/test split status when
  claimed, and mutation-history references for discarded prompt attempts. A
  single focused repair may mark these as `not_available` or `neutral`, but it
  must not claim generalization.
- Round feedback is structured as iteration path data. Critical feedback must
  reappear in the next round as a prompt constraint, focus metric, investigation
  question, or stop-rule risk.
- `html/assets/data.json` is display data only. It must be reproducible from
  the lab-runner artifact set; never invent prompt or response fields.
- `html/assets/data.json` is the stable bridge between evidence and UI. Do not
  fork the data shape for a static-only design.
- Render-facing five-point scores must be human-readable: integer scores as
  `5 von 5`, decimal scores only when meaningful such as `4,6 von 5`. Do not
  emit UI copy like `5.0/5` or `5,0 von 5` in `decisionMetrics`, metric
  details, or assistant-review prose.
- For Windows browsers launched from WSL2, use `file://///wsl.localhost/<distro>/...`
  file URIs. Raw `\\wsl.localhost\...` arguments may be misread by Firefox as
  `https://wsl.localhost/...`.

## Resources

- [Full workflow](references/workflow.md)
- [Artifact contracts](references/artifact-contracts.md)
- [Provider lab runner](references/provider-lab-runner.md)
- [Write-back contract](references/writeback-contract.md)
- `scripts/scaffold_campaign.py` creates the campaign folder and state.
- `scripts/lab_runner.py` executes real provider or fixture runs.
- `scripts/evaluate_prompt_run.py` computes parse/schema/source metrics.
- `scripts/build_review_surface_data.py` adapts run evidence to the shared HTML
  data contract.
- `scripts/verify_review_surface_trace.py` fails if review-surface display data
  differs from the actual lab-runner artifacts.
- `scripts/open_review_surface.py` opens rendered HTML with correct WSL2 to
  Windows file URI handling.
- Shared script:
  `~/.codex/skills/shared/scripts/rewrite_prompt_contract_block_in_foundation.py`.
