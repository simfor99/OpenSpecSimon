# OpenSpec Intent-Driven Testschrift Contract

Use this reference when an OpenSpec change needs tests and evidence that prove
the original intent, not just that tasks were edited or commands turned green.

The Testschrift is not a new source of truth. It is the executable testing layer
inside `builder-plan.md`, below OpenSpec specs, prompt contracts,
`quality-gates.md`, `implementation-ledger.md`, `goal.md`, source maps and
accepted Simon decisions.

## Core principle

```text
Intent -> claim class -> public interface -> smallest sufficient test surface
-> RED/evidence-before-change -> minimal GREEN -> fresh evidence -> not_proven
```

The selected test surface must be the lowest public interface that actually
proves the claim. "End-to-end" means "through the real boundary that closes the
claim", not "always browser".

## Authority order

Special deterministic contracts outrank the generic Testschrift:

1. OpenSpec-local prompt contracts, specs, design, proposal, `goal.md`, maps,
   ledgers, quality gates and accepted Simon decisions.
2. Deterministic shared contracts such as Prompt Fidelity,
   Prompt-Request-Parity, LLM Output Contract Testing, External Side-Effect
   Reality and Evidence Claim Integrity.
3. The Intent-Driven Testschrift rows inside `builder-plan.md`.
4. Chat memory and inferred test intent.

The Testschrift must reference deterministic contracts when they apply. It must
not invent prompt text, JSON shapes, field names, enum values, fallback
behavior, repair policy, provider routing, persistence semantics or hidden
compatibility bridges.

## Test surface ladder

For each material claim, choose and justify one primary public interface:

| Claim shape | Normal public interface | Extra evidence often required |
|---|---|---|
| User can see or do something | Browser/user-visible path | Screenshot, browser trace/video/report, linked API/runtime/persistence proof |
| HTTP/API route exists or changed | Direct HTTP request through active registry | Route registry proof, auth/session assertions, downstream proof |
| Product/workflow entry path works | Product-entry or resume contract | Trace, status, handoff, persistence and downstream reference checks |
| Runtime/dataflow behavior changes | Public runtime runner or orchestrator boundary | Trace/handoff artifacts and must-survive assertions |
| Parser/validator behavior changes | Parser/validator public API | Positive and negative fixture tests |
| Structured LLM/provider output changes | LLM output contract inventory row | Raw provider response, envelope/normalizer, parsed output, validator, downstream consumer |
| Prompt text/routing changes | Deterministic prompt fidelity and request-parity checks | Rendered prompt, effective provider request and trace/review evidence |
| Durable external state changes | Real entry path plus same-target write-read proof | Target environment, IDs, status/error assertions, cleanup/retention stance |
| Docs-only or governance change | Source-linked doc validation/review | No-test rationale plus affected downstream gate if any |

Browser evidence is required when acceptance depends on a real user-visible
entry path, form, navigation, authentication/session flow, visual state, review
UI, report surface or browser-visible product workflow. It is not a substitute
for API, trace, handoff, provider-output or persistence evidence.

## Row schema

Use this shape for each Testschrift row under `builder-plan.md` `## TDD /
evidence tasks`. Markdown bullets are fine; YAML is preferred when the row is
complex.

```yaml
id: TDD-01
depends_on: []
openspec_task: "tasks.md 2.3"
work_slice: "WS-02"
claim_class: browser_entry | ui_visibility | api_entry | persistence_write | status_transition | workflow_success | bounded_stage_run | dataflow_handoff | llm_output_contract | prompt_fidelity | prompt_request_parity | trace_generation | trace_visibility | current_run | historical_match | resume_from_existing | runtime_config | docs_contract
intent: "<human-language outcome this row proves>"
contract_source:
  - "<spec, prompt-contract, gate, map, goal, source file or accepted decision>"
public_interface: "<browser path, API route, product-entry, runner, parser, validator, checker, etc.>"
test_surface: browser | api | product_entry | resume_entry | cli | runtime_runner | parser_validator_fixture | deterministic_checker | provider_route | trace_verifier | database_write_read | doc_validation | no_test_with_reason
surface_choice_reason: "<why this surface is the smallest sufficient proof>"
lower_surface_rejected:
  - "<why a lower-level/unit-only test would not prove the claim>"
higher_surface_not_required:
  - "<why a broader/browser/e2e test would add cost without closing more claim>"
expected_red: "<failing command/result before implementation, or evidence-before-change gap>"
minimal_green: "<smallest implementation/evidence step that should pass>"
command:
  - "<exact test/check command, browser script, query, or reviewer command>"
fresh_evidence:
  - "<expected durable path, run id, screenshot, trace, report, DB query result, etc.>"
not_proven:
  - "<adjacent claim this row must not be promoted to>"
unlocks:
  - "<next Testschrift row or Work Slice id>"
status: planned | red_confirmed | green_confirmed | passed | no_test_with_reason | deferred_with_accepted_decision | blocked
```

## RED/GREEN rules

- Prefer one vertical test/evidence row per behavior or claim. Do not write all
  tests first and all implementation later when a vertical loop is possible.
- A RED result can be a failing test, a missing route, a missing browser state,
  a failing validator, an absent trace, a failed same-target read, or an
  evidence-before-change gap. It must be concrete enough to distinguish "not
  implemented" from "not checked".
- RED or evidence-before-change must be recorded before the minimal GREEN step:
  command plus output summary, durable evidence path, missing-artifact proof or
  reviewer note with timestamp/source. If Apply missed this before changing the
  target, the row cannot be silently marked `passed`; record the miss as
  `no_test_with_reason`, `deferred_with_accepted_decision` or `blocked`.
- GREEN must be the minimal code, prompt, runtime, docs or evidence change that
  closes the current claim. Do not pre-build later rows unless a higher
  contract explicitly requires shared foundation work.
- Never mark a row `passed` with only the agent's assertion. Use fresh evidence
  paths, command output summaries, run IDs, screenshots, traces, reports,
  validator output or accepted deferral records.
- Use `no_test_with_reason` only when an executable RED/GREEN loop is not
  practical. The reason must name the replacement evidence and the residual
  risk.

## Anti-fake rules

- Every material claim needs a claim class, subject or target, public
  interface, test surface, command or evidence action, and `not_proven`
  boundary.
- Command output alone is not enough for browser/user-visible claims; require a
  durable success artifact or accepted deferral.
- Fixture/parser tests prove fixture behavior only. They do not prove actual
  provider, Stage or workflow output.
- API 200/202 proves route reachability only. It does not prove persistence,
  downstream handoff or workflow success unless those claims have their own
  evidence.
- Browser submit success proves a user-visible entry path only. It does not
  prove workflow success, trace visibility, provider output or durable external
  writes.
- Local migrations, generated types, unit tests, trace files and fixture replay
  are partial evidence for external side effects until same-target write-read
  proof exists.
- Historical matches and cached/resumed artifacts must not be promoted to
  current-run proof.

## Apply and verify behavior

`$openspec-apply-change` should execute Testschrift rows in dependency order
when they exist. It should not mark a row, work slice or OpenSpec task complete
while the row's evidence is missing, contradicted, over-promoted or blocked.

`$openspec-verify-change`, `$openspec-review` and `$openspec-archive-change`
must treat a required Testschrift as an archive-readiness artifact. Missing
rows, missing RED/no-test rationale, missing fresh evidence, wrong test
surface, missing browser evidence for user-visible claims, contract drift or
evidence over-promotion are blockers unless Simon accepts a recorded deferral.

## When not required

Skip a formal Testschrift for narrow, low-risk changes where `tasks.md` already
names exact files, exact tests and exact evidence, and no user-visible,
external-state, prompt, LLM-output, trace, API-route, schema, migration or
runtime handoff claim is involved. Record `testschrift_status: not_required`
with a short reason when the decision matters downstream.
