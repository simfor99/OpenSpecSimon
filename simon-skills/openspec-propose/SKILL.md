---
name: openspec-propose
version: "1.3.14-sanctum"
bundle: openspec-simon
bundle_version: "2026.06.11.6"
description: Propose a new change with all artifacts generated in one step. Use when the user wants to quickly describe what they want to build and get a complete proposal with design, specs, and tasks ready for implementation.
argument-hint: "[change-name or description] [optional context paths, CTO review, map, or ledger]"
disable-model-invocation: false
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.3.14-sanctum"
  generatedBy: "1.3.1"
---

Propose a new change - create the change and generate all artifacts in one step.

I'll create a change with artifacts:
- proposal.md (what & why)
- design.md (how)
- tasks.md (implementation steps)

When ready to implement, use the Sanctum execution chain:
`CTO Review backchannel when used` -> pre-Apply `$openspec-review` when the
proposal is broad/high-risk -> `goal.md` when needed ->
`$openspec-apply-change` -> `$openspec-verify-change` -> post-Verify
`$openspec-review` -> `$ceo-review` when required.

For broad, high-risk, LLM/pipeline, migration, browser workflow, CEO-facing or
dependency-heavy changes, route to a pre-Apply Red Review via
`/home/simon/.codex/skills/openspec-review/SKILL.md` before creating or
running a runnable OpenSpec-local `goal.md`. After apply, archive readiness
must be checked with
`/home/simon/.codex/skills/openspec-verify-change/SKILL.md`.

When the proposal itself depends on many large source files, prompt folders,
schemas, traces or daily artifacts, first use
`/home/simon/.codex/skills/goal-brief/SKILL.md` to create a Pre-Proposal
Reading Contract. That contract preserves what must be deeply read before
OpenSpec artifacts are written; it is not a substitute for reading the sources.

For broad proposals where subagents are available or explicitly authorized,
follow `/home/simon/.codex/skills/shared/references/openspec-subagent-policy.md`.
Subagents may audit source coverage, prompt-contract/routing risk, quality-gate
coverage, or builder-plan completeness before artifacts are written. The main
agent owns `proposal.md`, `design.md`, specs, tasks, local meta-artifacts,
validator runs, and the final handoff.

---

**Input**: The user's request should include a change name (kebab-case) OR a description of what they want to build.

**Steps**

1. **If no clear input provided, ask what they want to build**

   Use the **AskUserQuestion tool** (open-ended, no preset options) to ask:
   > "What change do you want to work on? Describe what you want to build or fix."

   From their description, derive a kebab-case name (e.g., "add user authentication" → `add-user-auth`).

   **IMPORTANT**: Do NOT proceed without understanding what the user wants to build.

1.3. **Clarification Ledger gate**

   Before creating the change, identify assumptions that would materially change
   the proposal if Simon resolved them differently than the AI agent.

   Read `/home/simon/.codex/skills/shared/references/openspec-clarification-ledger.md`.
   If Explore, CTO Review, OpenSpec Map, Goal Brief, Test Review, Red Review or
   chat context already contains a Clarification Ledger, carry it forward.

   Build or refresh a compact ledger for:
   - intended runtime/product effect, not just component behavior;
   - effect handoff from persistence, UI, prompt, trace, schema or runtime source
     to the downstream consumer;
   - required evidence class (`formal_status`, `source_truth`,
     `runtime_evidence`, `review_truth`, etc.);
   - release/archive boundary versus follow-up scope;
   - performance or cost semantics behind limits and budgets;
   - change isolation when the workspace or source set is mixed;
   - unresolved Simon decisions.

   If every item is `cleared`, continue normally and preserve the evidence in
   artifacts where relevant.

   If an item is `carry_visible`, proposal may continue only if `proposal.md`,
   `design.md`, specs or `tasks.md` keep the assumption explicit as a non-goal,
   requirement, evidence gate, dependency or follow-up boundary. Do not phrase
   it as completed behavior.

   If any item is `clarify_first`, ask Simon before writing OpenSpec artifacts.
   If any item is `map_first`, route to `$openspec-map` before proposal. If any
   item is `cto_first`, route to `$cto-review` before proposal.

   Never turn unresolved ledger items into conservative defaults unless an
   accepted CEO decision or canonical policy explicitly authorizes that default.

1.35. **Blocking Gap Check**

   Before writing artifacts, close only gaps that would make the proposal
   wrong, misleading, unverifiable or unsafe to execute.

   If the answer can be found by reading source files, OpenSpec artifacts,
   maps, ledgers, prompt contracts, tests, traces or architecture docs, inspect
   those sources instead of asking the user.

   If a genuine user decision is still required, ask one focused blocking
   question at a time. Include the recommended answer or default and the reason
   it follows from the current evidence. Do not run a full grilling session
   inside `$openspec-propose`.

   If the remaining gap branches into multiple dependent decisions, source
   ownership questions, terminology conflicts, quality-gate semantics or
   architecture tradeoffs, stop proposal generation and route back to
   `$openspec-explore`, `$openspec-map` or `$cto-review` as appropriate. If the
   ambiguity is low-risk and does not control acceptance, carry it visibly in
   `proposal.md`, `design.md`, specs, `tasks.md`, `goal.md` or
   `quality-gates.md` rather than blocking.

1.4. **Ziel-Weg-Fitness and Nordstern bridge gate**

   Before finalizing artifacts, read
   `/home/simon/.codex/skills/shared/references/openspec-ziel-weg-fitness.md`
   and `/home/simon/.codex/skills/shared/references/openspec-nordstern-task-bridge.md`.
   Prove that the selected solution path is the smallest sufficient path to
   reach Simon's goal without quality loss, then translate each important
   outcome into `Nordstern -> target system state -> task IDs -> evidence gate`.
   If the path is `overbuilt`, `underbuilt`, `unclear`, `needs_cto` or
   `needs_ceo`, stop or carry the blocker visibly. If path quality depends on
   empirical behavior, include a `$ab-test-lab` handoff; for LLM, prompt,
   schema, crawler, ranking, filtering, UX or pipeline-quality choices, A/B is
   usually recommended unless source truth already decides.

1.45. **Work Slice and Coverage Pass**

   When the Explore/Map/CTO/chat plan contains more than one independently
   verifiable unit, or when `tasks.md` would otherwise become broad and
   generic, convert the plan into a compact set of work slices. A work slice is
   one coherent, independently verifiable unit of behavior, contract, cleanup,
   migration, evidence or documentation work.

   Work Slices are an optional compass, not a mandatory template. Skip them for
   narrow changes where the target files, tests and acceptance evidence are
   already obvious. This is a translation aid inside existing OpenSpec
   artifacts, not a new `plans/` or `features/` folder.

   For each slice, capture enough structure to keep proposal, specs, tasks and
   apply aligned:
   - stable work-slice id such as `WS-01`;
   - short name and one-sentence goal;
   - dependency ids, if any;
   - target behavior or contract surface;
   - likely target paths, tests, traces or evidence when known;
   - acceptance/evidence criteria;
   - Intent-Driven Testschrift candidate when a slice needs a vertical
     proof loop: claim class, public interface, test surface, RED/no-test
     expectation, minimal GREEN target, fresh evidence and `not_proven`
     boundary;
   - whether the slice can be implemented in parallel after dependencies pass.

   Order slices by dependency: foundation, data/contracts, core behavior,
   integrations/runtime, UX/reporting, cleanup/evidence. Use the actual
   problem shape; do not force all categories when they do not apply.

   Run a coverage pass before finalizing artifacts:
   - every Nordstern outcome, accepted decision, Must-Survive-Fact, source
     contract, quality-gate candidate, non-goal and evidence expectation must
     map to at least one slice or be explicitly recorded as a global
     requirement, global gate or non-goal;
   - every material work slice must land in `proposal.md`, `design.md`, specs
     and `tasks.md` unless the schema makes one artifact inapplicable;
   - `tasks.md` should preserve work-slice ids or clear slice headings so
     `$openspec-apply-change` can execute by dependency and verify per-slice
     acceptance;
   - broad slices that need exact file targets, red/green commands or
     step-level evidence should be carried into `builder-plan.md`;
   - user-visible, browser, API, product-entry, LLM-output, prompt, trace,
     persistence, schema, migration or runtime-handoff slices should carry
     Testschrift candidates into `builder-plan.md` using
     `/home/simon/.codex/skills/shared/references/openspec-intent-driven-testschrift.md`;
   - slice-specific acceptance, evidence or archive constraints should be
     linked to `quality-gates.md` when Quality Gates are materialized.

   If a material slice lacks source ownership, target paths, dependencies,
   acceptance evidence or a controlling user decision, do not invent it from
   memory. Ask one blocking question, route to `$openspec-map`, require a
   Builder Plan before Apply, or carry the blocker visibly in the relevant
   artifact.

1.47. **External Side-Effect Reality gate derivation**

   Before finalizing artifacts, scan the request, sources, specs, design,
   tasks, maps, CTO Reviews, Goal Briefs and work slices for external side
   effects. Read
   `/home/simon/.codex/skills/shared/references/openspec-external-side-effect-reality.md`
   and
   `/home/simon/.codex/skills/shared/references/openspec-quality-gates.md`
   when any trigger appears.

   Triggers include Supabase, Postgres, database, DB, storage, bucket, queue,
   webhook, auth, billing, email, notification, external API mutation,
   persisted workflow/status updates, trace indexing in a remote table, or any
   claim that a production/product entry path writes durable state.

   When triggered, materialize or require a Quality Gate that proves the real
   side effect with write-read evidence from the same target system the run
   uses. The gate must name the target environment, entry path,
   run/workflow/request identifiers, expected external records, required field
   assertions, success/error/status checks, downstream reference/reload proof
   and cleanup or retention stance.

   Do not close the proposal with only local migration files, generated types,
   unit tests, trace artifacts, fixture replay, browser submit success or API
   responses as persistence evidence. Those are partial evidence. If the real
   external write cannot be executed in this change, record an explicit
   deferral with owner, risk and follow-up path in `quality-gates.md`,
   `tasks.md` and `goal.md` when present.

   For pipeline, workflow or stage changes, include an entry-point matrix
   obligation in `builder-plan.md` or `quality-gates.md`:

   ```text
   Entry point -> new runtime path -> new adapter/writer -> trace write ->
   external write
   ```

1.48. **Evidence Claim Integrity gate derivation**

   Before finalizing artifacts, scan the request, sources, specs, design,
   tasks, maps, CTO Reviews, Goal Briefs and work slices for evidence that
   could be over-promoted from one claim to another. Read
   `/home/simon/.codex/skills/shared/references/openspec-evidence-claim-integrity.md`
   and
   `/home/simon/.codex/skills/shared/references/openspec-quality-gates.md`
   when any trigger appears.

   Triggers include workflow success, bounded stage/task ranges, trace
   generation, trace indexing, trace/viewer visibility, status transitions,
   downstream consumers, dataflow handoffs, historical-match selection,
   resume-from-existing behavior, cache/idempotent reuse, scenario
   fingerprints, or any test that intentionally proves only a partial claim
   such as persistence, API reachability or browser submit.

   When triggered, materialize or require a Quality Gate that states the
   claim classes and subject IDs it will close. Use narrow claim labels such
   as `persistence_write`, `workflow_success`, `bounded_stage_run`,
   `dataflow_handoff`, `trace_generation`, `trace_visibility`,
   `status_transition`, `current_run`, `historical_match`,
   `resume_from_existing` and `runtime_config`.

   The gate must also state adjacent claims that are explicitly not proven.
   Examples: a persistence-only E2E must not be promoted to workflow success;
   a generated trace file must not be promoted to indexed trace visibility; a
   historical best match must not be promoted to current-run proof; a recorded
   stage range must not be promoted to an enforced runtime boundary.

1.49. **Prompt-Request-Parity gate derivation**

   Before finalizing artifacts, scan the request, sources, specs, design,
   tasks, maps, CTO Reviews, Goal Briefs and work slices for LLM, model,
   agent, provider, prompt, Prompt Contract, Stage prompt/runtime handoff,
   model routing, trace viewer, raw response, or effective request work. Read
   `/home/simon/.codex/skills/shared/references/openspec-prompt-request-parity.md`
   when any trigger appears.

   When triggered, materialize or require a concrete acceptance path proving
   that every prompt contract part survives into the active provider request:

   ```text
   prompt contract -> rendered system/user prompt -> effective provider request
   -> trace artifact/test evidence -> review surface
   ```

   Do not let OpenSpec artifacts say "the LLM sees this" only because a prompt
   file contains it. Specs, tasks, Builder Plan or Quality Gates must require
   evidence that the active runtime transports the System Prompt and User
   Prompt through the provider adapter. If a provider has no separate system
   field, the proposal must make the explicit embedding strategy and tests
   visible.

   For trace/review UI work, require Provider Raw internals such as provider
   system instructions, internal model labels, usage objects or tool internals
   to stay out of productive trace/review artifacts. The default review truth is
   our effective provider request and the fachliche model output.

1.495. **LLM Output Contract Testing gate derivation**

Before finalizing artifacts, scan prompt contracts, User Prompt templates,
specs, design, maps, CTO Reviews, Goal Briefs and work slices for structured
LLM, Search-LLM, Perplexity, agent, provider-adapter or tool-call return
contracts. Read
`/home/simon/.codex/skills/shared/references/openspec-llm-output-contract-testing.md`
when any trigger appears.

Triggers include output JSON skeletons in the User Prompt, required fields,
enums, arrays, nullable fields, `response_format`, `generateObject`,
Zod/Pydantic/JSON Schema, parser contracts, provider response envelopes,
normalizers, `*_parsed-output.json`, post-LLM transformations, repair layers,
projections, Stage parsed outputs or downstream handoffs that consume
provider/model-returned fields.

When triggered, materialize or require:

- a spec/task that names the expected output contract source;
- route class and provider/model source for each operation;
- `llm-output-contract-inventory.md` for multi-operation changes, using
  `/home/simon/.codex/skills/shared/templates/llm-output-contract-inventory-template.md`
  when a template is useful;
- provider-envelope/normalizer target path when raw provider output is not the
  business object;
- runtime parser/validator target paths;
- positive and negative contract tests for valid output, missing fields, wrong
  types, invalid enums, malformed JSON, null/empty cases and unknown fields
  when relevant;
- actual run-artifact evidence requirements for Verify/Review/Archive claims
  about real provider or Stage output conformance;
- must-survive assertions for fields that must not be dropped, renamed,
  defaulted or weakened by provider normalizers or post-LLM transformations;
- a `llm_output_contract_validation` quality gate with
  `evidence_timing: during_apply`, blocking `verify`, `review` and `archive`;
- Builder Plan and ledger rows for parser/schema tests, parsed-output trace
  artifacts, provider normalizers, actual run artifacts and downstream
  handoff/consumer checks when those artifacts are present or required.

Do not let a prompt with an inline JSON skeleton count as implementation
evidence. The proposal must require raw provider response, provider envelope or
normalization, parsed output, runtime validator and downstream handoff to be
checked after implementation. Fixture-only tests can prove parser behavior but
not actual provider-output or Stage-output claims.

1.5. **Pre-proposal reading contract preflight**

Before creating the change, classify whether the proposal writing step
itself is context-heavy. This applies when the user references many files,
large prompt directories, source clusters, traces, schemas, prior daily
   artifacts or says the context window is already crowded.

   If a Pre-Proposal Reading Contract already exists, read it first. Before
   writing artifacts, open and read every source marked `required_deep_read` or
   `unread`, and re-read sources whose re-read rule is triggered by context
   compaction. Carry the resulting source-grounded Must-Survive-Facts,
   non-goals, open questions and evidence gates into `proposal.md`,
   `design.md`, specs and `tasks.md`.

   Treat `required_deep_read` as an explicit source-reading obligation for this
   proposal-writing phase, regardless of which workflow created the contract.
   Do not assume the source was already read. If mandatory reads cannot be
   completed, list them as proposal blockers instead of silently writing around
   them.

   If no reading contract exists, continue normally by reading the source files
   needed for an accurate proposal. When source reading is unusually large,
   fragile, or likely to be lost across compaction, create or route to a
   Pre-Proposal Reading Contract via
   `/home/simon/.codex/skills/goal-brief/SKILL.md`.
   This is especially important for LLM/pipeline, prompt, JSON/schema,
   data-shape, migration or trace-heavy work.

   Do not ask for confirmation when the need is clear from context. If the user
   references `$openspec-propose` together with multiple files, a large prompt
   directory, trace/schema folders, readiness artifacts, or context-window risk,
   create or require the reading contract automatically. Ask only when no source
   set can be inferred or two unrelated source sets are equally plausible.

1.55. **Source Foundation block gate**

When the proposal is based on a concrete foundation artifact, target-contract
document, CTO memo, source map, reading contract or user-provided planning file,
include a `## Source foundation` section in `proposal.md`.

Use this compact YAML shape:

```yaml
primary_foundation:
  path: "<path to the main foundation/source artifact>"
  role: "target_contract | source_truth | cto_review | source_map | reading_contract"
  review_mode: "completeness_baseline"
  must_check:
    - "<major area the review must verify for coverage>"
supporting_sources:
  - path: "<path>"
    role: "<source_target_map | prompt_contracts | evidence | repo_contract>"
accepted_overrides:
  - "<accepted deviation from the foundation, if any>"
explicit_non_goals:
  - "<foundation-related item intentionally out of scope>"
```

The block is not a second design document. It tells `$openspec-review` what to
read as the counter-checking template for completeness. If no concrete
foundation exists, omit the section. If a concrete foundation exists but its
path or role is unclear, resolve that before finalizing proposal artifacts or
carry the blocker visibly.

A Foundation Brief (shared template
`/home/simon/.codex/skills/shared/templates/openspec-foundation-brief-template.md`,
frontmatter `binding_status: pre_spec_zielbild`) is always a
`primary_foundation` with `role: "target_contract"`. Derive `must_check` from
its mandatory sections: scope/non-scope, prompt contracts, runtime contract
targets, Must-Survive-Facts, quality-gate candidates, assumed defaults and
open decisions. Scan its `assumed_default` markers in the CEO Decision Gate
like other decision markers. After the OpenSpec artifacts exist, the brief is
demoted to provenance: the OpenSpec-local artifacts (specs, tasks,
`prompt-contracts/`, `quality-gates.md`) become the build truth, and any later
conflict with the brief is a drift finding, not a choice.

1.56. **Foundation Coverage Matrix gate**

When the proposal has a concrete foundation source, read
`/home/simon/.codex/skills/shared/references/openspec-foundation-coverage-matrix.md`
before finalizing artifacts.

Build a coverage pass from the source foundation's `must_check` list,
Must-Survive-Facts, prompt contracts, runtime contract targets, quality-gate
candidates, accepted decisions, open decisions, non-goals and backchannel
obligations.

Every material source item must land in the correct artifact type:

- target behavior or contract -> spec requirement/scenario and task;
- non-goal -> proposal/design non-goal and, when risky, guard task or gate;
- Must-Survive-Fact -> spec scenario, task and evidence/quality gate;
- prompt contract -> OpenSpec-local `prompt-contracts/`, productive prompt
  target, prompt-fidelity gate and request-parity evidence;
- structured provider/model output contract -> spec/task,
  `llm-output-contract-inventory.md` when multi-operation, route/provider
  source, provider normalizer when applicable, parser or schema target,
  output-contract gate, fixture tests, actual run-artifact requirement for
  real output claims and downstream handoff check;
- runtime contract target -> spec requirement, runtime task, test target and
  ledger row when a ledger is present or required;
- external side effect -> quality gate, builder-plan entry path and ledger row;
- evidence claim boundary -> claim-class gate with explicit `not_proven`
  boundaries;
- A/B recommendation -> task and gate, or a planned
  `not_applicable_with_reason` decision before promotion/archive;
- backchannel obligation -> task, ledger row or explicit writeback target.

A mention in `proposal.md` alone is not coverage. "Follow the foundation" is
not coverage. If an item cannot be represented safely, mark it
`clarify_first`, `cto_first`, `ceo_first`, `non_goal_with_reason`,
`accepted_override` or `deferred_with_accepted_decision`. Do not silently drop
it.

For broad/high-risk changes, add a compact `Foundation coverage matrix`
section to `builder-plan.md` or `design.md`, or make the equivalent coverage
visible across `quality-gates.md`, `implementation-ledger.md` and `tasks.md`.
If any required item remains `missing` or `clarify_first`, do not hand off the
change as Apply-ready.

1.7. **OpenSpec Map triage**

   Before creating the proposal, decide whether a deterministic source/target
   map is actually useful. Do not recommend `$openspec-map` by default. Use a
   four-outcome triage:

   - `not_required`: continue without a map.
   - `use_existing`: read an existing map and carry it into artifacts.
   - `recommended_before_apply`: create the proposal now, but make the map the
     next step before `$openspec-apply-change`.
   - `required_before_propose`: route to
     `/home/simon/.codex/skills/openspec-map/SKILL.md` before writing OpenSpec
     artifacts.

   Set `not_required` when the change is narrow and concrete:
   - one or two files/components;
   - target paths and test paths are already known;
   - no migration, cleanup, stage-boundary, trace/evidence, schema/contract, or
     data-shape uncertainty;
   - no CTO Review or decision artifact says inventory/map/source truth is
     missing;
   - the tasks can be written without guessing source ownership.

   Set `use_existing` when a relevant OpenSpec Map already exists.

   If an OpenSpec Map already exists, read it before artifact generation and
   carry its component map, source classes, target paths, tests, cleanup paths,
   prompt contracts, skill-network handoffs, CTO Review map backchannel, Goal
   Brief recommendation and `propose_readiness` into `proposal.md`,
   `design.md`, specs and `tasks.md`.

   Treat the map's `propose_readiness` as the bridge contract, not just prose.
   Accept both `target_change` and legacy `change_name_suggestion` as the
   intended change name. Empty optional lists must be `[]` or omitted; ignore
   sentinel list items such as `none` only as legacy input and do not reproduce
   them in OpenSpec artifacts.

   If the map says `propose_readiness.status: not_ready_for_propose`, do not
   bypass it silently. Resolve the listed follow-up first, ask Simon for the
   controlling decision, or keep the proposal blocked/`clarify_first`.

   Set `recommended_before_apply` when the proposal can responsibly define
   scope and acceptance criteria, but implementation would still benefit from a
   concrete source/target inventory. Typical signals:
   - three or more components, modules, stages, services, schemas, prompts,
     trace surfaces, or test surfaces;
   - broad task list where implementation paths are only partly known;
   - cleanup or deprecation work with obsolete paths to verify;
   - user says they are "not up to date", asks what still has to be built, or
     asks whether a source map / implementation map is needed.

   In this case, do not block proposal generation. Instead add explicit tasks
   and handoff language requiring `$openspec-map <change-name>` before
   `$openspec-apply-change`, and include the map's expected scope in
   `tasks.md`, `design.md`, or `goal.md` as appropriate.

   Set `required_before_propose` only when a responsible proposal cannot be
   written without source/target inventory. Typical signals:
   - source-of-truth conflict across active code, architecture, CTO Review,
     archive, specs, or traces;
   - central target paths or ownership boundaries are unknown;
   - stage-boundary, Stage Source Map, trace/evidence, LLM handoff, schema, or
     cleanup contracts define the change itself rather than only execution
     detail;
   - a CTO Review, Reading Contract, Test Review, or CEO/Verify artifact says
     map/inventory/source truth is missing before spec;
   - unresolved decisions depend on knowing which components and paths are
     affected.

   If `required_before_propose`, stop proposal artifact generation and route to
   `$openspec-map` with the current source set. Do not ask for confirmation
   when the need is clear; ask only when two unrelated mapping scopes are
   equally plausible.

   **Prompt Contract Gate:** When a map or source briefing says
   `prompt_contracts_required: true`, do not create OpenSpec artifacts unless
   the map lists concrete `prompt_contract_files` and their status is
   `created`. Read every listed prompt-contract file before artifact
   generation. Treat those files as target contracts above narrative
   summaries, CTO prose, or chat memory.

   Do not trust the map's `created` claim blindly: re-run the mechanical
   extraction gate before artifact generation —

   ```bash
   python3 ~/.codex/skills/shared/scripts/validate_prompt_fidelity.py \
     --extraction-check <prompt-contracts-dir>
   ```

   A failing gate means the contracts drifted from their source (paraphrased
   prompts, routing overridden by convention defaults, missing provenance
   frontmatter). Stop and route back to `$openspec-map` repair instead of
   building artifacts on drifted contracts. A green localization gate (Gate B)
   never compensates a red extraction gate (Gate A): faithfully copied drift
   is still drift — discard the local copies together with the repaired
   sidecars. Require maps whose `propose_readiness` carries a
   `prompt_contract_extraction_gate` evidence block with `status: passed`,
   `command`, and `checked_at`; if it is missing or malformed, route back to
   `$openspec-map` repair before artifact generation (the re-run above stays
   mandatory).

   If listed prompt-contract files live outside the target OpenSpec change,
   copy them into `openspec/changes/<name>/prompt-contracts/` immediately after
   creating the change directory. Preserve the original files as provenance;
   do not delete or move the daily/map sidecars. OpenSpec artifacts, `goal.md`,
   and downstream skill handoffs must link the OpenSpec-local copies as the
   primary build/read source, while the copied files should retain or add
   provenance fields such as `source_path`, `map_path` and
   `origin_prompt_contract_path`.

   If concrete prompt text exists in a CTO Review or briefing but no
   prompt-contract file exists yet, set map triage to `required_before_propose`
   unless the change is narrow and the prompt can be safely copied directly
   into the OpenSpec artifacts with exact provenance. For prompt-heavy LLM
   pipeline changes, prefer `$openspec-map` first so prompt contracts become
   linkable files.

   A Pre-Proposal Reading Contract preserves mandatory reads; an OpenSpec Map
   grounds components, source/target paths, contracts, tests, cleanup and skill
   handoffs. Use both when the source set is both large and structurally
   complex.

   **Map status bridge:** Maps use compact pre-proposal statuses; convert them
   into Propose-owned actions before artifact writing:

   - `builder_plan_status: required` -> `required_create_now` when the map has
     a Builder Plan Seed, concrete component map, prompt contracts, gate seeds,
     or target paths; otherwise `required_before_apply`.
   - `builder_plan_status: recommended` -> `recommended_create_now` when the
     map contains enough implementation detail; otherwise
     `required_before_apply` only if Apply would have to guess.
   - `implementation_ledger_status: required` -> `required_create_now` when the
     map names concrete files, folders, prompts, specs, traces or docs;
     otherwise `required_before_apply`.
   - `quality_gate_status: ready_for_propose` -> `materialize_now`.
   - `quality_gate_status: candidates` -> `materialize_now` when candidates
     have concrete source/action/evidence, otherwise `map_first` or
     `clarify_first`.
   - `prompt_contracts_status: created` is usable only with a green Gate A and
     concrete `prompt_contract_files`; then localize the sidecars before
     writing artifacts.

   Preserve these conversions visibly in `proposal.md`, `design.md`,
   `tasks.md` and any created `quality-gates.md`, `implementation-ledger.md`
   or `builder-plan.md`.

1.8. **GTM Stage Authoring gate**

   Before creating OpenSpec artifacts for any change that touches GTM stages,
   Stage Source Map, Stage Evidence Lab, stage-boundary cleanup,
   prompt/runtime handoffs, or paths under
   `services/gtm-agents/prompts/stage-XX/`,
   `services/gtm-ts-runtime/stage-XX/`, or
   `docs/architecture/stages/stage-XX/`, read the compact agent entrypoint:

   ```text
   docs/architecture/testing-agent-entrypoints/gtm-stage-authoring.md
   ```

   This entrypoint is the lightweight Stage folder convention for proposal
   writing. Deep-read
   `docs/architecture/sections/95-gtm-stage-prompt-runtime-contract-boundaries.md`
   only when the entrypoint says the longform source is needed, such as new
   Runtime Stage folders, structural stage cleanup, Source Map/replay/trace/
   validation/handoff changes, prompt/runtime drift, or a bundling-vs-drift
   judgment.

   Also read `services/gtm-agents/prompts/PROMPT-FILE-CONVENTION.md` when
   prompt assets are in scope, and
   `services/gtm-ts-runtime/pipeline/stage-boundary-source-map.ts` when source
   ownership, replay, trace, validation, handoff, or Evidence Lab boundaries
   are in scope.

   Carry the Stage Authoring entrypoint into `proposal.md`, `design.md`, specs
   and `tasks.md` as a concrete contract, not as background reading:

   - Prompt truth belongs under `services/gtm-agents/prompts/stage-XX/` and
     describes what the LLM sees.
   - Runtime truth belongs under `services/gtm-ts-runtime/stage-XX/` and
     describes accepted inputs, outputs, handoffs, deterministic guards,
     validation, replay boundaries, traces and tests.
   - Human architecture truth belongs under
     `docs/architecture/stages/stage-XX/` and
     `docs/architecture/sections/` and explains the flow, drift, owners and
     review context.
   - Prompt truth is only fulfilled when the effective provider request
     transports the rendered System Prompt and User Prompt according to
     `/home/simon/.codex/skills/shared/references/openspec-prompt-request-parity.md`.

   When this gate is active, artifacts must make the classification visible
   enough for a later builder to act without rediscovering it from chat:

   - `proposal.md` or `design.md` must name which Stage truth surfaces are in
     scope: prompt truth, runtime truth, human architecture truth, Source Map,
     trace, replay, validation, handoff, tests/evidence or drift cleanup.
   - `tasks.md` must translate each in-scope surface into at least one concrete
     task, explicit not-affected statement, Builder Plan obligation, Map
     obligation or Quality Gate candidate.
   - `builder-plan.md` is required or recommended when the affected Stage
     surfaces are too broad or path-sensitive for `tasks.md` to guide Apply
     safely.
   - `quality-gates.md` is materialized only when the Stage Authoring contract
     controls Apply, Verify, Review or Archive acceptance; do not create a
     vague "follow Stage Authoring" gate.

   For new or changed Runtime Stage folders, proposal tasks must cover the
   Section-95 role set or explicitly justify intentional bundling:
   `index.ts`, `contract.ts`, `runner.ts`, `gates.ts`/`validation.ts` or
   contract-near guards, `replay.ts` or Source-Map-bound replay boundary,
   deterministic helpers, and `__tests__/`. Exact filenames are preferred
   target standard, but existing bundled stages may remain bundled only when
   the role is findable, tested, and documented as current runtime evidence or
   target contract.

   Do not create a fourth Stage truth. Proposals must classify every Stage
   change as prompt, runtime, architecture docs, tests/evidence, Source Map
   reference, or visible drift cleanup. Source Map work may reference owners
   and required artifacts; it must not define new semantic gates, prompt rules,
   output shapes, or compatibility bridges.

   If the proposal would otherwise need to guess affected Stage owners, file
   roles, replay boundaries, trace artifacts, validation artifacts, handoff
   artifacts, or architecture docs, set OpenSpec Map triage to
   `required_before_propose`.

2. **Soft CTO Review preflight for high-risk work**

   Before creating the proposal, briefly consider whether this change is broad
   enough to benefit from a CTO Review memo. This is a soft offer, not a hard
   gate.

   Offer a CTO Review memo first when the request involves:
   - broad migrations or rewrites
   - LLM pipeline behavior, prompt ownership, model routing, or semantic judges
   - cross-language parity, golden tests, or data-shape preservation
   - production side effects, promotion decisions, or unclear rollback paths
   - many unknown architecture decisions or validation gates

   If the user wants speed or the change is narrow, continue with the proposal.
   If a CTO Review already exists, read it before generating artifacts and carry
   its blocking decisions, stop rules, and evidence expectations into
   `proposal.md`, `design.md`, specs, and `tasks.md`.

   When an existing CTO Review is used as an input source, record its concrete
   file path as a `source_cto_review`. Extract and preserve:
   - `spec_mode_status`
   - `target_openspec_change`
   - open and accepted `BD-*` decisions
   - Stop-Regeln
   - Evidence Gates
   - `Zurückzuschreiben nach`
   - any Arbeitsstand checklist items that OpenSpec generation may change

   Treat those items as a bidirectional contract: the CTO Review informs the
   OpenSpec, and the finished OpenSpec must update the CTO Review so the memo
   no longer reads as if proposal creation is still pending.

   If an existing CTO Review has `spec_mode_status: pending`,
   `clarify_first`, or `dont_build_yet`, raise that status with the user before
   generating artifacts. Do not hard-block by default; ask whether to continue,
   update the CTO Review, or resolve the open decisions first.

   Use this wording when helpful:
   > "This looks like CTO-review territory. I can either draft the OpenSpec now,
   > or first create a short CTO Review memo to surface risks, blocking
   > decisions, stop rules, and evidence gates. Which path do you want?"

2.5. **Execution-control preflight**

   Before writing artifacts, classify whether the future implementation needs
   an OpenSpec-local Goal Brief and verification gates.

   Default to requiring or strongly recommending `goal.md` when the change
   involves:
   - broad migrations or rewrites
   - LLM pipeline behavior, prompt ownership, model routing, semantic judges or
     JSON/schema handoffs
   - cross-language parity, golden tests, trace-heavy evidence or data-shape
     preservation
   - browser/runtime workflows, screenshots, live/authenticated proof or visual
     evidence
   - downstream/upstream OpenSpec dependencies
   - production side effects, promotion decisions, archive-readiness claims or
     CEO-facing completion

   Carry this into `proposal.md`, `design.md`, specs and `tasks.md` as
   appropriate:
   - Apply must use `$openspec-apply-change`.
   - Verify must use `$openspec-verify-change` before archive.
   - Goal Evidence, dependency gates, traces, Testing Contract and Completion
     Review Plan can block archive even when task checkboxes are complete.

2.6. **Implementation Ledger gate**

   Read
   `/home/simon/.codex/skills/shared/references/openspec-implementation-ledger.md`
   when the change is broad, file-heavy, cleanup/deprecation-oriented,
   migration-like, source-map-driven, or Simon asks that every file, folder,
   prompt, Section, schema, test or trace be reviewed.

   Classify ledger status before finalizing artifacts:

   - `not_required`: narrow change and `tasks.md` can name every target.
   - `required_create_now`: proposal has enough inventory to create
     `openspec/changes/<name>/implementation-ledger.md`.
   - `required_before_apply`: proposal can be written, but Apply must create
     or complete the ledger before edits.
   - `present`: an existing ledger is part of the change.
   - `blocked`: a complete target list cannot be derived without more mapping
     or Simon decision.

   Default to `required_create_now` when an OpenSpec Map, Goal Brief, CTO
   Review, Reading Contract, or chat instruction names concrete target sets.
   The ledger should include all concrete folders and all individual files
   that must be inspected, not just parent directories. Include prompt
   contracts, productive prompt files, architecture Sections, central docs,
   tests, traces, schemas, migrations, symlinked targets, external mapped
   targets and review/backchannel gates when they are in scope.

   When a ledger is created or present, link it from `proposal.md`,
   `design.md`, `tasks.md` and `goal.md` if one is created. Add a task saying
   Apply must maintain it and that Verify/Review must treat unfinished ledger
   rows as blockers. If the ledger is required but cannot be created yet, add
   a pre-Apply task to create it before implementation and explain why.

2.65. **Executable Builder Plan gate**

   Read
   `/home/simon/.codex/skills/shared/references/openspec-builder-plan.md`
   when the change is broad, implementation-sensitive, or the Explore/Map/chat
   context says `builder_plan_status: recommended` or `required`.
   Read
   `/home/simon/.codex/skills/shared/references/openspec-intent-driven-testschrift.md`
   when Explore/Map/chat says `testschrift_status: recommended` or `required`,
   or when important claims require browser, API, product-entry, runtime,
   prompt/LLM-output, trace, persistence, schema, migration or handoff proof.

   Classify Builder Plan status before finalizing artifacts:

   - `not_required`: narrow change; `tasks.md` can name exact files, tests and
     evidence without guessing.
   - `recommended_create_now`: create
     `openspec/changes/<name>/builder-plan.md` after the required OpenSpec
     artifacts exist, because it will materially improve Apply quality.
   - `required_create_now`: create `builder-plan.md` before Apply, because a
     builder could otherwise check off tasks while missing the human-language
     outcome or inventing contract details.
   - `required_before_apply`: proposal can be written, but the concrete plan
     depends on an inventory, ledger or decision that must be completed before
     implementation.
   - `present`: an existing Builder Plan is part of the change.
   - `blocked`: a responsible proposal cannot define a build path until a
     source, ownership, contract or Simon-decision gap is resolved.

   Default to `required_create_now` for broad GTM Stage, LLM/prompt, schema,
   handoff, trace/evidence, migration, cleanup, browser workflow or quality
   pipeline changes when `tasks.md` would otherwise be abstract. Default to
   `recommended_create_now` when OpenSpec contracts are clear but the work has
   enough moving parts that a task-by-task TDD/evidence guide reduces drift.
   If `testschrift_status: required`, Builder Plan status is normally
   `required_create_now` unless a blocking source/decision gap requires
   `required_before_apply`. If `testschrift_status: recommended`, default to
   `recommended_create_now` when enough source/test-surface detail exists.

   The Builder Plan is below OpenSpec contracts. It may include concrete
   commands, file targets and code sketches, but it must cite its source
   contracts and must pause rather than invent field names, JSON shapes, prompt
   examples, enum values, fallback behavior or compatibility bridges.

   If a map has a `Builder Plan Seed`, carry its implementation patterns,
   candidate test files, contract-risk warnings and shadow-workbench constraints
   into `builder-plan.md` or into an explicit `required_before_apply` task.

2.66. **Quality Gates materialization gate**

   Read
   `/home/simon/.codex/skills/shared/references/openspec-quality-gates.md`
   when Explore, Map, chat, a source file, template, `goal.md`, CTO Review,
   Test Review, or the proposal context carries quality-gate candidates.

   Quality Gates are not a separate workflow. They are an OpenSpec-local
   artifact for explicit acceptance, evidence, review and archive constraints.

   Classify Quality Gate status before finalizing artifacts:

   - `none`: no quality-gate candidates are present.
   - `materialize_now`: enough source/action/evidence detail exists to create
     `openspec/changes/<name>/quality-gates.md`.
   - `map_first`: proposal would need source/path/evidence research before
     concrete gates can be written.
   - `clarify_first`: the gate depends on user intent, scope, severity,
     allowed deferral or acceptance semantics that must be clarified first.
   - `blocked`: a required gate cannot be materialized responsibly.

   Do not use keyword matching as the decision rule. A gate is warranted when a
   constraint from the user's intent, a source/template file, architecture
   contract, test/evidence contract, map, goal or repo convention controls
   whether the implementation can be accepted, verified, reviewed or archived.

   If `map_first`, route to `$openspec-map` or add a pre-Apply task requiring
   gate research before implementation, depending on proposal readiness. If
   `clarify_first`, ask before creating misleading artifacts.

2.7. **CEO Decision Gate preflight**

   Before writing OpenSpec artifacts, scan all mandatory sources, Reading
   Contracts, CTO Reviews, maps, decisions and prior planning artifacts for
   unresolved decision markers:

   ```text
   Blocking Decision, BD-*, CEO-Entscheidung, decision_owner, open, pending,
   clarify_first, review_required, non-promotable, non_promotable, not green,
   nicht grün, DONT_BUILD_YET, assumed_default
   ```

   `assumed_default` markers from a Foundation Brief are basket-2 assumptions:
   they were presented to Simon with a one-line rationale during brief
   creation. Treat them as accepted defaults unless they control architecture,
   governance, product logic, scope, cost, risk or promotion — in that case
   raise them like any other unresolved decision.

   If any unresolved decision controls architecture, governance, product logic,
   scope, cost, risk, promotion, archive readiness, launch readiness or future
   workflow, do not turn it into a default, warning or implementation option.
   Switch to the CEO decision format from
   `/home/simon/.codex/references/ceo-entscheidungen.md` and ask Simon for the
   decision in chat before creating `proposal.md`, `design.md`, specs or
   `tasks.md`.

   Owner labels such as `Team`, `CTO`, `Builder` or `Codex` are not an escape
   hatch. If the decision is truly autonomous, decide it immediately and mark it
   as decided in the proposal rationale. If it remains open, Simon is the
   effective decision owner for this workflow.

   Defaults are recommendations until Simon has accepted them. Do not apply a
   conservative default to an unresolved decision unless an existing accepted
   CEO decision or canonical policy explicitly authorizes that default.

   Preserve contract polarity. If a source says `non-promotable`,
   `review_required`, `fail-loud`, `blocked`, `not green` or `nicht grün`, the
   OpenSpec may record a trace marker or evidence artifact, but it must keep the
   state blocking unless Simon explicitly decides otherwise. Never convert a
   red marker into a passing acceptance path.

   If multiple small unresolved decisions are independent and low-risk, prepare
   one CEO decision table with recommended answers and ask Simon to accept,
   change or drill into items. If an upstream decision can change downstream
   decisions, ask it first as a single CEO decision.

3. **Create the change directory**
   ```bash
   openspec new change "<name>"
   ```
   This creates a scaffolded change at `openspec/changes/<name>/` with `.openspec.yaml`.

3.5. **Localize prompt contracts when present**

   If the map, reading contract, CTO review or source briefing lists concrete
   prompt-contract files, ensure they exist under:

   ```text
   openspec/changes/<name>/prompt-contracts/
   ```

   Rules:
   - If the files are already there, use them.
   - If they exist only in a daily/map folder, copy them into the OpenSpec
     change before writing `proposal.md`, `design.md`, specs, `tasks.md`, or
     `goal.md`.
   - Keep the external files as provenance and add or preserve provenance
     frontmatter in the local copies.
   - Link the OpenSpec-local paths in artifacts as the primary target
     contracts; mention external paths only as provenance.
   - Prompt-Optimierungshinweise außerhalb eines fenced Prompt-Contract-Blocks
     sind audit-only. `$openspec-propose` folgt diesen Links nicht; lokalisiert
     und materialisiert wird nur der aktive Prompt-Contract.
   - Pause if copying would overwrite a different local prompt contract without
     an explicit artifact update or Simon decision.
   - Mechanical localization gate (mandatory after copying): verify the local
     copies still match the map sidecars —

     ```bash
     python3 ~/.codex/skills/shared/scripts/validate_prompt_fidelity.py \
       --change-dir openspec/changes/<name> \
       --map-contracts <map-prompt-contracts-dir>
     ```

     Localization is a copy, not a rewrite. The gate compares prompt bodies
     strictly and allows added provenance frontmatter fields, but never
     changed sidecar values. A failing gate means the local copies are not
     build truth.

4. **Get the artifact build order**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to get:
   - `applyRequires`: array of artifact IDs needed before implementation (e.g., `["tasks"]`)
   - `artifacts`: list of all artifacts with their status and dependencies

5. **Create artifacts in sequence until apply-ready**

   Use the **TodoWrite tool** to track progress through the artifacts.

   Loop through artifacts in dependency order (artifacts with no pending dependencies first):

   a. **For each artifact that is `ready` (dependencies satisfied)**:
      - Get instructions:
        ```bash
        openspec instructions <artifact-id> --change "<name>" --json
        ```
      - The instructions JSON includes:
        - `context`: Project background (constraints for you - do NOT include in output)
        - `rules`: Artifact-specific rules (constraints for you - do NOT include in output)
        - `template`: The structure to use for your output file
        - `instruction`: Schema-specific guidance for this artifact type
        - `outputPath`: Where to write the artifact
        - `dependencies`: Completed artifacts to read for context
      - Read any completed dependency files for context
      - If a map lists `prompt_contract_files`, read them and then read the
        OpenSpec-local copies under `prompt-contracts/` before creating or
        updating this artifact
      - Create the artifact file using `template` as the structure
      - Apply `context` and `rules` as constraints - but do NOT copy them into the file
      - Show brief progress: "Created <artifact-id>"

   b. **Continue until all `applyRequires` artifacts are complete**
      - After creating each artifact, re-run `openspec status --change "<name>" --json`
      - Check if every artifact ID in `applyRequires` has `status: "done"` in the artifacts array
      - Stop when all `applyRequires` artifacts are done

   c. **If an artifact requires user input** (unclear context):
      - Use **AskUserQuestion tool** to clarify
      - Then continue with creation

5.5. **Create Builder Plan when required or recommended**

   If Builder Plan status is `recommended_create_now` or
   `required_create_now`, create:

   ```text
   openspec/changes/<name>/builder-plan.md
   ```

   Use
   `/home/simon/.codex/skills/shared/references/openspec-builder-plan.md` as
   the contract. Read the completed OpenSpec artifacts, localized
   prompt-contract files, map, ledger and `goal.md` if present before writing
   the plan.

   The plan must map OpenSpec outcomes to executable builder tasks:

   - work-slice id, dependency and acceptance/evidence target when slices
     exist;
   - exact create/modify/delete/inspect file targets when known;
   - test files and exact commands;
   - expected failing result or explicit `no_test` rationale;
   - Intent-Driven Testschrift rows for required material claims: claim class,
     contract source, public interface, test surface, surface-choice rationale,
     RED/no-test expectation, minimal GREEN, command/evidence action, fresh
     evidence and `not_proven` boundaries;
   - minimal implementation target;
   - passing verification command;
   - ledger row or evidence gate;
   - contract source path for every field name, JSON shape, prompt text,
     example boundary, enum value, handoff or runtime behavior.

   Run the Builder Plan self-review from the shared reference before final
   response. If the plan cannot be written without guessing contract details,
   do not invent them. Set Builder Plan status to `required_before_apply` or
   `blocked`, add the missing source/decision/inventory as a task or blocker,
   and report it.

   If Builder Plan status is `required_before_apply`, add an explicit pre-Apply
   task or handoff requiring `builder-plan.md` before
   `$openspec-apply-change`. If status is `not_required`, state the reason in
   the final output.

5.6. **Create Quality Gates when candidates exist**

   If Quality Gate status is `materialize_now`, create:

   ```text
   openspec/changes/<name>/quality-gates.md
   ```

   Use
   `/home/simon/.codex/skills/shared/references/openspec-quality-gates.md` as
   the contract. Read the completed OpenSpec artifacts, map, localized prompt
   contracts, `goal.md`, `implementation-ledger.md` and `builder-plan.md` when
   present before writing the gate file.

   Each gate must state:

   - origin and source locator;
   - concrete applies-when conditions;
   - severity;
   - current status;
   - explicit required actions;
   - explicit required evidence;
   - blocks: apply, verify, review and/or archive;
   - allowed final statuses;
   - decision escape hatch, if any.

   Do not write vague "follow this source" gates. Extract concrete actions and
   evidence. If a candidate is still vague, use `needs_research` or
   `clarify_first` and make that visible in `quality-gates.md` or route to Map.

   Link `quality-gates.md` from `proposal.md`, `design.md`, `tasks.md`,
   `goal.md` and `builder-plan.md` when those files exist. Add a task saying
   Apply must handle every defined gate and Verify/Archive must block normal
   completion while any gate is not in an allowed final status.
   When a gate is slice-specific, record the affected work-slice ids so Apply
   and Verify can connect the gate to concrete tasks and evidence.

5.7. **Create Browser Fresh-Intake / User-Visible Path gate when needed**

   When a change touches or claims a real user-visible entry path, form,
   frontdoor, authenticated/session workflow, browser runtime, visual path, or
   production fresh-intake boundary, decide whether a browser evidence gate is
   required.

   The gate is required when acceptance depends on what a user can actually do
   in the product UI, not only on backend route behavior. Typical triggers:
   - ingestion forms, beta forms, checkout/signup flows, customer portals or
     admin workflows;
   - product-entry contracts such as fresh-intake routes whose values must flow
     into runtime, trace, persistence, downstream stages or reports;
   - claims about visible form options, navigation, auth/session behavior,
     screenshots, browser-visible report state or live user journeys.

   Materialize this as a Quality Gate, Builder Plan task and Verification task
   when enough source detail exists. The gate must say:
   - which real UI path is tested;
   - which representative test data or fixture source is used;
   - which success artifact must be saved: screenshot, Playwright trace/video,
     browser test report, or explicit accepted deferral with reason;
   - which runtime/API/persistence/trace artifact proves the UI submission
     reached the system boundary it claims to reach;
   - which part is verified by browser evidence and which later behavior is
     verified by runtime, trace, handoff, persistence or unit/integration tests.

   Use this browser tool policy in generated gates and tasks:

   ```text
   Use an integrated browser or browser-automation tool for simple isolated
   browser proof when available. If `chrome-devtools-axi` is available, prefer
   it for live, authenticated, session-bound, CDP, performance or
   user-browser-adjacent proof. Use direct Chrome DevTools MCP as fallback or
   for unsupported AXI-special cases. Use Playwright or the available test
   runner as fallback or when deterministic isolated regression is the better
   proof. If no browser-capable tool is available, do not claim Browser
   Evidence; leave the gate open, not applicable with reason, or deferred with
   an accepted decision. Reference:
   `/home/simon/.codex/references/chrome-devtools-axi.md`.
   ```

   Do not write "use Playwright" as the primary requirement unless Playwright
   itself is the product/runtime contract under review. The acceptance claim is
   the user-visible path and linked evidence, not the specific browser tool.

   Do not let command output alone close a browser gate. A passed command is a
   test signal; the gate's final evidence must include a durable artifact path
   or an accepted deferral. For success screenshots/traces, name the expected
   visible state, not just the route URL.

5.75. **Create API Route Registry gate when needed**

   When a change adds, moves, renames, or relies on an HTTP/API route, create a
   Quality Gate, Builder Plan task and Verification task that proves the route
   exists in every runtime registry used by the project.

   The gate must identify:

   - handler/source file;
   - production/server route registry or router wiring;
   - local dev/Vite route registry or router wiring, when separate;
   - direct HTTP smoke command against the local or target runtime;
   - auth/admin/session behavior and expected success/error fields;
   - downstream persistence, trace, workflow or UI proof when the route is an
     entry boundary.

   File existence is never enough for an API route claim. A handler without
   registry proof is a shadow file until a real runtime request succeeds.

5.76. **Create Runtime ID Inventory gate when needed**

   When a change touches stage/substage status, trace viewers, handoff
   routing, replay/resume, pipeline dashboards, or any UI that reflects runtime
   stage artifacts, create a Runtime ID Inventory gate.

   The gate must require current runtime identifiers to be extracted from
   runtime code, constants, actual traces, or accepted trace artifacts before
   implementation. Proposal/design text alone is not sufficient source truth
   for stage IDs. The gate must name the source class used:
   `runtime_code`, `current_runtime_evidence`, `trace_artifact`, or
   `target_contract`.

5.8. **Meta-Contract Linter preflight**

   After `quality-gates.md`, `implementation-ledger.md` or `builder-plan.md`
   exists, run the shared deterministic meta-linter before final success
   summary:

   ```bash
   python3 ~/.codex/skills/shared/scripts/openspec_meta_lint.py \
     --change-dir openspec/changes/<name> \
     --mode propose
   ```

   If the linter reports blocking findings, fix safe structural issues before
   finalizing the proposal, or report the blocker visibly when it requires a
   source decision. The linter checks meta-contract structure only:
   parseability, required fields, allowed values, status mode rules and
   required sections. It does not decide whether a gate is fachlich right.

6. **Show final status**
   ```bash
   openspec status --change "<name>"
   ```

7. **Create or route to Goal Brief for broad changes**

   If the change is broad, high-risk, LLM/pipeline, migration, browser
   workflow, CEO-facing, trace-heavy or dependency-heavy, create or offer to
   create:

   ```text
   openspec/changes/<name>/goal.md
   ```

   Use `/home/simon/.codex/skills/goal-brief/SKILL.md`. The Goal Brief should
   include the OpenSpec Executor Contract, OpenSpec Verification Gate, Testing
   Contract, dependency gates, Implementation Ledger gate, Builder Plan gate
   and Completion Review Plan where relevant.

   If the user asked for speed or the change is narrow, do not block proposal
   completion; state that apply will follow OpenSpec tasks only unless a
   `goal.md` is created before execution.

7.5. **Route to pre-Apply OpenSpec Review when required**

   If the change is broad, high-risk, source-foundation-driven, LLM/pipeline,
   GTM stage/runtime, trace/evidence-heavy, browser/runtime, migration-like,
   schema/data-shape, database/storage/queue/external-side-effect, CEO-facing,
   archive-sensitive, or contains `quality-gates.md`,
   `implementation-ledger.md`, `builder-plan.md`, `prompt-contracts/`, an
   OpenSpec Map, a CTO Review source, carry-visible decisions, or a
   `## Source foundation` block, the next execution step is:

   ```text
   $openspec-review <name>
   ```

   This review is a pre-Apply semantic gateway. It checks whether the freshly
   written spec is sane enough to execute. It does not replace
   `$openspec-verify-change` or the post-Verify `$openspec-review`.

   If a `goal.md` is created in the same proposal workflow before that review
   exists, mark it `draft_only` or `ready_after_red_review`, and make the
   runnable `/goal` block start with the required `$openspec-review` instead of
   `$openspec-apply-change`.

   Recommend direct `$openspec-apply-change` only for narrow, concrete changes
   where target files/tests are obvious, no local meta-artifacts or source
   foundation exist, and no Team-Red scrutiny is needed before execution.

8. **CTO Review backchannel reconciliation**

   If one or more CTO Reviews were used as `source_cto_review`, reopen each
   source memo after OpenSpec artifacts are created and reconcile it before the
   final response.

   Update the original memo in place when it is an active daily/planning
   artifact. If the original is explicitly archival, immutable, or cannot be
   safely edited, create an adjacent dated addendum and link it from the final
   response. Do not silently skip the backchannel.

   The reconciliation must make the CTO Review honest about the new state:
   - link the generated OpenSpec change path;
   - mark OpenSpec proposal/design/spec/tasks as created or still blocked;
   - record which `BD-*` decisions were accepted, changed, unresolved, or moved
     into the OpenSpec/CEO Decision Gate;
   - explain any scope split between the CTO Review and the new OpenSpec;
   - preserve polarity for blockers, `clarify_first`, `dont_build_yet`,
     `non-promotable`, `review_required`, `not green`, and `nicht grün`;
   - update Arbeitsstand checklist buckets when the review has them;
   - refresh `Zurückzuschreiben nach` so completed mirrors are marked done and
     remaining mirrors are explicit;
   - keep the CTO Review as the decision/history artifact and the OpenSpec as
     the technical execution truth.

   Prefer adding a compact section named `OpenSpec-Rückkanal` when no natural
   update slot exists. Include:

   ```markdown
   ## OpenSpec-Rückkanal

   **Stand:** <YYYY-MM-DD HH:MM>  
   **OpenSpec:** `openspec/changes/<name>/`  
   **Status:** `created | partially_created | blocked`

   **Gespiegelt:** <accepted decisions, scope, gates>
   **Offen:** <remaining blockers, evidence gaps, follow-up reviews>
   **Nächster Schritt:** `$openspec-apply-change <name>` or blocker action
   ```

   If the OpenSpec materially supersedes an old CTO Review assumption, name the
   supersession directly. Example: "Boundary Cleanup owns source cleanup;
   Evidence Lab consumes the Source Map." Do not leave stale pending language
   such as "OpenSpec ableiten" unqualified after the OpenSpec exists.

8.5. **Foundation Brief Rückkanal**

   If a Foundation Brief (frontmatter `binding_status: pre_spec_zielbild`) was
   used as `primary_foundation`, update the brief immediately after the
   OpenSpec artifacts exist:

   - set its frontmatter `resulting_openspec_change` to the change name;
   - append a dated entry to its `## OpenSpec-Rückkanal` section, e.g.
     `- Stand <YYYY-MM-DD>: $openspec-propose hat openspec/changes/<name>/
     erzeugt; Brief ist ab jetzt Provenienz, Bauwahrheit sind die
     OpenSpec-Artefakte.`

   Dated entries only; never rewrite earlier entries and never add a live
   status field. Do not silently skip this backchannel — if the brief cannot
   be updated, report the blocker with the exact reason.

**Output**

After completing all artifacts, summarize:
- Change name/location and artifacts created.
- Clarification Ledger, Nordstern Bridge, Reading Contract, OpenSpec Map,
  CTO Review, CTO backchannel, CEO Decision Gate, Builder Plan and Goal Brief
  statuses.
- Quality Gate status and `quality-gates.md` path when created or required.
- Intent-Driven Testschrift status and whether rows were materialized in
  `builder-plan.md`, required before Apply, or not required with reason.
- Meta-Contract Linter status when local meta-artifacts exist:
  `not_applicable`, `ran_clean`, or `ran_with_findings`.
- Work Slice coverage status and where slice ids were preserved.
- State what is ready and what is blocked or carried visible.
- Prompt the next command: pre-Apply `$openspec-review` when required, then
  goal/apply, verify before archive, and post-Verify `$openspec-review` before
  CEO Review.

**Artifact Creation Guidelines**

- Follow the `instruction` field from `openspec instructions` for each artifact type
- The schema defines what each artifact should contain - follow it
- Read dependency artifacts for context before creating new ones
- If a Pre-Proposal Reading Contract exists, read it before artifact generation
  and fulfill its mandatory deep-read obligations before writing artifacts.
- If an OpenSpec Map or Reading Contract lists prompt-contract files, read each
  file, localize it into `openspec/changes/<name>/prompt-contracts/` when it is
  not already there, and carry the local copy into OpenSpec as a concrete target
  contract. Proposal, design, specs, tasks and `goal.md` must link the
  OpenSpec-local files and state whether the expected implementation is
  verbatim or structural-copy.
- Do not paraphrase a concrete prompt contract as "roughly this prompt". If the
  artifact must summarize it, also link the source prompt-contract file and add
  a prompt-fidelity task or acceptance criterion.
- Use `template` as the structure for your output file - fill in its sections
- Preserve work-slice ids or headings in the artifacts when the change has
  multiple independently verifiable units. Do not create separate
  `plans/<initiative>/features/` files unless the user explicitly asks for that
  separate planning format.
- **IMPORTANT**: `context` and `rules` are constraints for YOU, not content for the file
  - Do NOT copy `<context>`, `<rules>`, `<project_context>` blocks into the artifact
  - These guide what you write, but should never appear in the output

**Guardrails**
- Create ALL artifacts needed for implementation (as defined by schema's `apply.requires`)
- Always read dependency artifacts before creating a new one
- If context is critically unclear, ask the user - but prefer making reasonable decisions to keep momentum
- Do not let proposal speed hide a material assumption. If a later
  `$openspec-review` would likely classify it as `DECISION`, clarify it now,
  map it first, route to CTO Review, or carry it visibly as a blocker/evidence
  gate.
- Do not let tasks lose the Nordstern. If a builder could check off a task
  without making the human-language outcome true, rewrite the task or clarify.
- Do not let a broad Explore plan collapse into one generic implementation
  task. When useful, split it into dependency-ordered, independently
  verifiable work slices and preserve the slice ids through specs, tasks and
  builder-plan. For narrow changes, skip this structure and keep the artifacts
  simple.
- If a change with that name already exists, ask if user wants to continue it or create a new one
- Verify each artifact file exists after writing before proceeding to next
- Do not treat a crowded chat transcript as the only memory of large source
  files. If proposal-critical source reading obligations are not durable,
  create or request a Pre-Proposal Reading Contract before writing artifacts.
- Do not treat a reading contract, checklist or summary as a replacement for
  opening and reading mandatory source files.
- Do not imply that apply-ready means archive-ready or completion-ready.
- For broad/high-risk changes, ensure tasks include evidence and verification
  work, not only implementation work.
- If quality gates exist or are required, materialize
  `openspec/changes/<name>/quality-gates.md` or visibly route to Map/clarify.
  Do not hide acceptance, evidence, review or archive constraints only in chat
  or prose.
- Every defined quality gate must be handled. Severity affects blocking
  behavior; it does not make lower-severity gates optional.
- For broad or contract-sensitive changes, ensure `builder-plan.md` exists or
  is explicitly required before Apply when `tasks.md` is too abstract for a
  builder to execute safely.
- Do not let a concrete Builder Plan outrank OpenSpec contracts. If code
  snippets, test names, field names, JSON shapes or prompt text in the Builder
  Plan conflict with specs, prompt contracts, map, ledger, `goal.md` or accepted
  Simon decisions, pause and update artifacts instead of choosing from memory.
- For downstream changes, include explicit upstream dependency gates in design,
  tasks or `goal.md`; do not let local task completion hide upstream evidence
  gaps.
- Do not recommend `$openspec-map` as ritual. Recommend or require it only when
  source/target inventory materially affects proposal correctness or safe
  implementation.
- When map status is `recommended_before_apply`, include an explicit
  `$openspec-map <change-name>` handoff before `$openspec-apply-change`.
- When map status is `not_required`, briefly state why: narrow scope, known
  paths, known tests, no inventory-dependent decision, or equivalent.
- When prompt contracts exist, include an explicit apply obligation: builder
  must implement against the OpenSpec-local prompt-contract files under
  `prompt-contracts/` and must pause if productive prompt text would diverge
  without an artifact update.
- For GTM Stage changes, enforce
  `docs/architecture/testing-agent-entrypoints/gtm-stage-authoring.md` as the
  compact Stage folder convention:
  keep prompt truth, runtime truth and human architecture truth separate;
  include affected `services/gtm-agents/prompts/stage-XX/`,
  `services/gtm-ts-runtime/stage-XX/`,
  `docs/architecture/stages/stage-XX/`, Source Map, trace, validation,
  handoff, replay, tests and docs-scan obligations where relevant.
- If a CTO Review was used as input, do not finish with a stale source memo.
  Either update the source memo, create a linked addendum, or report the
  backchannel as blocked with the exact reason.
- Do not let OpenSpec and CTO Review drift into two truths. CTO Review records
  decision history and reasoning; OpenSpec controls execution after proposal
  generation.
- Do not translate unresolved decisions into OpenSpec defaults. If a source
  marks a decision `open`, `pending`, `clarify_first`, `review_required` or
  `non-promotable`, either obtain Simon's CEO decision, classify it as a pure
  evidence gap, or keep the proposal blocked/`clarify_first`.
- Preserve polarity from source to OpenSpec: a source-level blocker must remain
  a blocker in specs, tasks, goal and verification gates unless Simon explicitly
  accepts a different outcome.
- Do not delegate canonical OpenSpec artifact creation on broad proposals.
  Subagent reports may inform the proposal, but the main agent must verify
  cited sources and own all final proposal artifacts.
