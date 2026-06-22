---
name: openspec-prompt-optimizer
version: "1.0.0-sanctum"
bundle: openspec-simon
bundle_version: "2026.06.22.1"
description: "WHAT: Orchestrates HITL optimization of fenced Pre-Spec/Foundation-Brief prompt contracts with real provider evidence, A/B rounds, chained fixtures, deterministic write-back, and resume state. WHEN: use for pre-spec prompt optimization, Foundation Brief prompt A/B, prompt-contract write-back, or Stage target prompts before openspec-map/propose."
argument-hint: "[foundation-brief-path] [--campaign docs/todo/.../07_experiments/... optional]"
disable-model-invocation: false
allowed-tools: Read, Write, Bash, Grep, Glob
---
<!-- TOKEN_BUDGET: 15000 -->

# OpenSpec Prompt Optimizer

This skill turns a Foundation Brief / Pre-Spec Zielbild with fenced prompt
contracts into a resumable HITL prompt-optimization campaign. Markdown ledgers
remain the source of truth; HTML is only the review surface.

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
   profile explicitly when delegating to `$prompt-improver`.

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

8. **Measure and render.** Parse provider returns, write request/raw/text/
   parsed/metrics artifacts, then build `html/assets/data.json` via
   `build_review_surface_data.py` and render with the shared
   `render_prompt_ab_review_surface.py`.
   Before showing the HTML, verify that each `cases[].results[].prompt.system`
   and `.prompt.user` is non-empty in `html/assets/data.json`; if not, rebuild
   from `*__02_rendered-prompt.txt` artifacts or stop.
   Run `verify_review_surface_trace.py` against `results-summary.json` and
   `html/assets/data.json`; if request, rendered prompt, response text, parsed
   output, metrics, or surface payload diverge from the artifact set, stop.
   After rendering, ask Simon whether to open the HTML review surface. In WSL2
   on Windows, never pass a raw UNC path to Firefox; use
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
| Build HTML data | `python scripts/build_review_surface_data.py --results <results-summary.json> --out <round>/html/assets/data.json` |
| Verify surface trace | `python scripts/verify_review_surface_trace.py --results <results-summary.json> --data <round>/html/assets/data.json --out <round>/artifacts/trace-integrity-report.json` |
| Open HTML review | `python scripts/open_review_surface.py <round>/html/index.html --browser firefox` |
| Write-back | `python ~/.codex/skills/shared/scripts/rewrite_prompt_contract_block_in_foundation.py ...` |

## Operating Rules

- Markdown ledgers are canonical; HTML never hides the only decision.
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
- Round feedback is structured as iteration path data. Critical feedback must
  reappear in the next round as a prompt constraint, focus metric, investigation
  question, or stop-rule risk.
- `html/assets/data.json` is display data only. It must be reproducible from
  the lab-runner artifact set; never invent prompt or response fields.
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
