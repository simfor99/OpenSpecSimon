---
name: openspec-apply-change
version: "1.2.4-sanctum"
bundle: openspec-simon
bundle_version: "2026.06.11.2"
description: "WHAT: Executes and builds tasks from an OpenSpec change. WHEN: Use when the user wants to start implementing, continue implementation, or work through tasks."
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.2.4-sanctum"
  generatedBy: "1.3.1"
---

Implement tasks from an OpenSpec change.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **Select the change**

   If a name is provided, use it. Otherwise:
   - Infer from conversation context if the user mentioned a change
   - Auto-select if only one active change exists
   - If ambiguous, run `openspec list --json` to get available changes and use the **AskUserQuestion tool** to let the user select

   Always announce: "Using change: <name>" and how to override (e.g., `/opsx:apply <other>`).

2. **Check status to understand the schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand:
   - `schemaName`: The workflow being used (e.g., "spec-driven")
   - Which artifact contains the tasks (typically "tasks" for spec-driven, check status for others)

3. **Get apply instructions**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   This returns:
   - `contextFiles`: artifact ID -> array of concrete file paths (varies by schema - could be proposal/specs/design/tasks or spec/tests/implementation/docs)
   - Progress (total, complete, remaining)
   - Task list with status
   - Dynamic instruction based on current state

   **Handle states:**
   - If `state: "blocked"` (missing artifacts): show message, suggest using openspec-continue-change
   - If `state: "all_done"`: do not suggest archive yet; run or route to
     `$openspec-verify-change` first. If `goal.md` exists, verification must
     include Goal Evidence, dependency gates, testing contract, traces and CEO
     Review readiness.
   - Otherwise: proceed to implementation

4. **Read context files**

   Read every file path listed under `contextFiles` from the apply instructions output.
   The files depend on the schema being used:
   - **spec-driven**: proposal, specs, design, tasks
   - Other schemas: follow the contextFiles from CLI output

4.25. **Source Foundation bridge check**

   Before implementation, scan the context files for explicit source
   foundations such as `Source Foundation`, `source foundation`, `target
   contract`, `foundation file`, `foundation blog`, `source_file`, `CTO
   Review`, `source locator`, or exact paths that the proposal/design/gates say
   are the basis for the change.

   If source foundations are named, read those exact files before productive
   edits and treat them as provenance above summaries in `tasks.md` or chat.
   This is especially important for OpenSpec changes generated from a dense
   Zielbild, CTO Review, map, prompt contract, or business/domain strategy
   document.

   Pause before editing when:

   - a required source foundation path is missing, unreadable, or ambiguous;
   - `quality-gates.md`, `builder-plan.md`, `goal.md` or specs reference a
     source foundation but only summarize it;
   - implementation would rely on chat memory instead of the named source
     file;
   - the source foundation conflicts with the OpenSpec-local contracts and no
     accepted artifact update resolves the conflict.

   If a concrete source foundation exists, also read and enforce:

   ```text
   /home/simon/.codex/skills/shared/references/openspec-foundation-coverage-matrix.md
   ```

   Before productive edits, confirm that every material `must_check`,
   Must-Survive-Fact, prompt contract, runtime target, quality-gate candidate,
   accepted decision, non-goal, A/B recommendation and backchannel obligation
   is represented in the correct downstream artifact type: spec, task, gate,
   ledger row, builder-plan task, prompt-contract, test/evidence package,
   non-goal, accepted override or accepted deferral.

   Pause before editing when a material source item is only mentioned in
   `proposal.md` prose or chat memory. Do not "just implement" the implied
   behavior; update the OpenSpec artifacts or ask Simon for the controlling
   decision first.

4.3. **OpenSpec Map bridge check**

   Before implementation, check whether the existing change has a concrete
   source/target implementation map. This is especially important when:

   - the proposal exists but the user asks what still has to be built;
   - the change mentions Stage Source Map, Source Map, Implementation Map,
     source/target inventory, stage boundaries, trace/evidence surfaces, or
     cleanup;
   - `tasks.md` is large, broad, or contains many abstract tasks without
     concrete paths;
   - implementation would touch multiple stages, services, schemas, prompts,
     traces, tests, or docs;
   - a CTO Review or Test Review says the map/inventory is still missing.

   If a map exists, read it together with the context files and preserve its
   `propose_readiness`, component map, target paths, test obligations,
   prompt contracts, CTO Review map backchannel, Goal Brief recommendation,
   and later gates while implementing.

   If the map contains `prompt_contracts_required: true`,
   `prompt_contracts_status: created`, a `Prompt Contracts` section, or a
   `prompt-contracts/` directory is present in the change, read every listed
   prompt-contract file before implementation. Treat those files as the prompt
   source of truth above summaries in `proposal.md`, `design.md`, `tasks.md`,
   or chat.

   Prefer `openspec/changes/<name>/prompt-contracts/*.md` over prompt-contract
   files in daily/map folders. External prompt-contract files are provenance or
   fallback sources once an OpenSpec-local copy exists. If artifacts reference
   external prompt contracts but no local `prompt-contracts/` directory exists,
   pause before editing productive prompt files and require localization into
   the change directory or an explicit artifact update.

   If both local and external prompt-contract files exist and their prompt
   bodies materially differ, pause and report the conflict. Do not choose a
   prompt version from memory, chat, or summaries.

   After creating or editing any productive prompt file from a prompt
   contract, run the deterministic fidelity check before marking the related
   task complete:

   ```bash
   python3 ~/.codex/skills/shared/scripts/validate_prompt_fidelity.py \
     --change-dir openspec/changes/<name>
   ```

   Errors (frontmatter drift, paraphrased or missing contract lines,
   placeholder/naming drift, output-JSON key drift) are blockers: fix the
   productive prompt file, or pause and update the artifacts when the
   divergence is intentional and Simon-approved. Do not mark prompt tasks
   complete on LLM judgment alone when the mechanical check fails or was
   skipped.

   Pause before editing productive prompt files when:

   - a prompt contract is referenced but the file is missing or unreadable;
   - the OpenSpec tasks do not name how the prompt contract is to be applied;
   - implementation would paraphrase, shorten, reorder, or "improve" a
     `target_contract` prompt without an artifact update;
   - examples marked `example_only` would leak into productive prompt logic;
   - the prompt contract has no provenance such as source path, source locator,
     contract kind, or extraction mode.

   If no map exists and implementation would otherwise start from generic
   tasks or stale chat memory, pause and create or route to
   `/home/simon/.codex/skills/openspec-map/SKILL.md` first. Treat this as a
   soft bridge for narrow work and a required bridge when source/target
   inventory controls correctness or safety.

4.35. **Prompt-Request-Parity execution check**

   Before editing or relying on any LLM, model, agent, provider, prompt,
   Prompt Contract, prompt operation registry, model routing, provider adapter,
   trace viewer, raw response, or effective request path, read and enforce:

   ```text
   /home/simon/.codex/skills/shared/references/openspec-prompt-request-parity.md
   ```

   Apply must prove or preserve the chain:

   ```text
   prompt contract -> rendered system/user prompt -> effective provider request
   -> trace artifact/test evidence -> review surface
   ```

   If the prompt contract defines a System Prompt or User Prompt, do not mark
   the related task complete until the effective provider request transports
   those parts or the OpenSpec artifacts explicitly accept a provider-specific
   transport strategy such as embedding the system instruction into the input.

   Pause instead of editing when implementation would let a prompt file,
   prompt contract or Stage description claim model-visible behavior that is
   not proven in the active provider request. Also pause when Provider Raw
   internals such as provider system instructions or internal model labels
   would be shown as our prompt truth instead of isolated as raw debug data.

4.37. **LLM Output Contract execution check**

Before editing or relying on any structured LLM/Search-LLM/Perplexity/agent/
provider output, parsed-output artifact, provider normalizer, parser, output
schema, post-LLM transformation, repair layer, projection or handoff consumer,
read and enforce:

```text
/home/simon/.codex/skills/shared/references/openspec-llm-output-contract-testing.md
```

Apply must prove or preserve the chain:

```text
User Prompt output contract -> raw provider/model response -> parsed output artifact
-> runtime validator / typed schema -> downstream handoff or consumer input
```

For provider routes whose raw response is an envelope, tool result,
Perplexity/Search response or adapter output, preserve this expanded chain:

```text
User Prompt output contract -> raw provider response -> provider envelope /
normalization -> parsed output artifact -> runtime validator / typed schema ->
downstream handoff or consumer input
```

For multi-operation changes, create or maintain
`openspec/changes/<name>/llm-output-contract-inventory.md` before marking any
related output-contract task complete.

Do not mark the related task complete until tests cover a valid representative
output plus relevant invalid outputs: missing required field, wrong type,
invalid enum, malformed JSON, null/empty value and unknown extra field when
the contract disallows extras.

Also test must-survive fields through any post-LLM transformation. If a
provider normalizer or transformation collapses, renames, defaults, repairs or
projects model output, it must either preserve the stronger target contract or
fail/record repair status explicitly. Silent default masking is a blocker.

Fixture tests can close parser/validator behavior. They cannot close a claim
that the actual provider route or Stage substep returned the target shape.
Verify/Review/Archive claims about real provider output need run-bound
artifacts for the same operation id, provider route/model, raw response, parsed
output, validation result and downstream consumer.

Pause instead of editing when the OpenSpec prompt defines a concrete output
shape but tasks, Builder Plan, ledger or quality gates do not identify the
route class, inventory row, parser/validator target, provider normalizer when
applicable, output-contract tests, real-run evidence requirement or downstream
consumer check.

4.4. **GTM Stage Authoring execution check**

   Before editing any GTM Stage prompt, runtime, Source Map, Evidence Lab,
   trace/evidence, replay, validation, handoff, or architecture-stage-doc path,
   read and enforce the compact agent entrypoint:

   ```text
   docs/architecture/testing-agent-entrypoints/gtm-stage-authoring.md
   ```

   This entrypoint is the lightweight Stage folder convention for
   implementation. Deep-read
   `docs/architecture/sections/95-gtm-stage-prompt-runtime-contract-boundaries.md`
   only when the entrypoint says the longform source is needed, such as new
   Runtime Stage folders, structural stage cleanup, Source Map/replay/trace/
   validation/handoff changes, prompt/runtime drift, or a bundling-vs-drift
   judgment.

   Also read `services/gtm-agents/prompts/PROMPT-FILE-CONVENTION.md` before
   editing `services/gtm-agents/prompts/stage-XX/`, and read
   `services/gtm-ts-runtime/pipeline/stage-boundary-source-map.ts` before
   editing or relying on Stage ownership, replay, trace, validation, handoff,
   or Evidence Lab boundaries.

   Implementation must keep the three Stage truths separate:

   - Prompt files describe what the LLM sees.
   - Runtime Stage folders define accepted inputs, outputs, handoffs,
     deterministic guards, validation, replay boundaries, traces and tests.
   - Architecture Stage docs explain the flow, drift, owners and review
     context for humans.

   Before productive edits, create a compact Stage Authoring classification
   from the OpenSpec artifacts and source paths:

   - prompt truth affected: yes/no, with paths or not-affected reason;
   - runtime truth affected: yes/no, with paths or not-affected reason;
   - human architecture truth affected: yes/no, with paths or not-affected
     reason;
   - Source Map, trace, replay, validation, handoff and tests/evidence
     affected: yes/no, with paths or not-affected reason.

   Continue only if `tasks.md`, `builder-plan.md`, `implementation-ledger.md`,
   `quality-gates.md` or the OpenSpec Map visibly carries the affected
   surfaces. For narrow changes, a concise not-affected statement is enough.
   For broad or path-sensitive Stage work, pause before editing if the
   artifacts do not tell Apply which truth surfaces and owners to update.

   When creating or rewriting `services/gtm-ts-runtime/stage-XX/`, implement
   or consciously preserve the Stage Authoring runtime role set:
   `index.ts`, `contract.ts`, `runner.ts`, `gates.ts`/`validation.ts` or
   contract-near guards, `replay.ts` or Source-Map-bound replay boundary,
   deterministic helpers, and `__tests__/`. Exact filenames are preferred for
   new or cleaned-up stages. Existing bundled stages may stay bundled only
   when the role is findable, tested, and represented as current runtime
   evidence or a documented target contract.

   Pause instead of editing when:

   - the OpenSpec tasks imply a Stage folder shape that conflicts with the
     Stage Authoring entrypoint or, when deep-read, Section 95;
   - Stage Authoring classification shows an affected prompt, runtime,
     architecture, Source Map, trace, replay, validation, handoff or
     tests/evidence surface that is absent from tasks, Builder Plan, ledger,
     quality gates, map or an explicit not-affected rationale;
   - prompt, runtime, architecture docs, Source Map, trace, validation,
     handoff, or replay responsibilities are mixed into one undocumented
     fourth truth;
   - implementation would define semantic Stage rules in the Source Map,
     Evidence Lab, docs, trace review scripts, or compatibility bridges instead
     of the prompt/runtime owner;
   - affected architecture Stage docs or generated business-logic docs are
     omitted without an explicit not-affected rationale.

4.5. **Goal Brief bridge check**

   Before implementation, check for:

   ```bash
   test -f "openspec/changes/<name>/goal.md"
   ```

   If `goal.md` exists, read it together with the context files and treat it as
   the execution control file above `tasks.md`. Tasks still come from OpenSpec,
   but the Goal Brief owns the holistic objective, Nordstern, stopping
   condition, doctrine checks, LLM Container Contract, Dataflow Integrity
   Contract, Must-Survive-Facts, checkpoints, validation expectations, Testing
   Contract, Browser Runtime Contract, Completion Review Plan, and pause
   rules.

   If `goal.md` is missing and the change is broad, migration-like,
   LLM-/pipeline-related, high-risk, or expected to run under `/goal`, offer to
   create it with `/home/simon/.codex/skills/goal-brief/SKILL.md` before
   implementing. This is a soft bridge, not a hard gate.

   If the user wants speed or the change is narrow, continue without `goal.md`
   and mention that execution will follow OpenSpec tasks only.

   Pause before implementation if an existing `goal.md` is marked `draft_only`,
   if it says to pause on unresolved CTO/OpenSpec decisions, or if its doctrine
   checks, LLM Container Contract, Dataflow Integrity Contract, Testing
   Contract, Browser Runtime Contract, or Completion Review Plan require a
   missing boundary/evidence decision.

4.6. **Implementation Ledger bridge check**

   Check for:

   ```bash
   test -f "openspec/changes/<name>/implementation-ledger.md"
   ```

   If present, read it together with the context files and treat it as the
   row-level execution control file for concrete folders, files, prompts,
   contracts, tests, traces, docs, Sections, central docs and review gates.
   Read
   `/home/simon/.codex/skills/shared/references/openspec-implementation-ledger.md`
   for the shared contract.

   If `proposal.md`, `design.md`, `tasks.md`, `goal.md`, an OpenSpec Map, CTO
   Review, Reading Contract or Simon's request says a ledger is required but
   the file is missing, pause before implementation and create or route to
   creation of `openspec/changes/<name>/implementation-ledger.md`.

   During implementation:

   - update ledger rows as work is completed;
   - final statuses must be `updated`, `moved`, `deleted`, `created`,
     `reviewed_unaffected`, `not_impacted`, `deferred_with_reason`, or
     `blocked`;
   - every final row needs concrete evidence or a no-impact reason;
   - `todo` rows block the related OpenSpec task from being marked complete;
   - file-heavy scope must have file rows, not only parent folder rows;
   - `reviewed_unaffected` means the target was actually read or otherwise
     source-verified, not skipped.

4.62. **Quality Gates bridge check**

   Check for:

   ```bash
   test -f "openspec/changes/<name>/quality-gates.md"
   ```

   If present, read it together with the context files and read
   `/home/simon/.codex/skills/shared/references/openspec-quality-gates.md`.
   Treat Quality Gates as execution gates, not just lint input. The
   Meta-Contract Linter checks their structure; Apply must execute or preserve
   their required actions and evidence obligations.

   During implementation:

   - execute gate `required_actions` when the gate applies to the current task
     or work slice;
   - record concrete evidence in the gate's `evidence` block before moving a
     gate to `passed`;
   - keep `planned` gates open when they are future Verify/Review/Archive
     obligations, but report them in the final Apply status;
   - do not mark an OpenSpec task complete when a gate that blocks `apply`
     is `candidate`, `needs_research`, `clarify_first`, `missing_evidence`,
     `failed`, or `blocked`;
   - use `deferred_with_accepted_decision` only when the required decision is
     recorded at the gate's `decision_escape_hatch.required_record`.

   Pause before editing when:

   - a gate blocks `apply` and is unresolved;
   - a gate's action/evidence requirement is too vague to execute safely;
   - a gate origin references a source file that has not been read;
   - implementation would satisfy a gate by assertion instead of evidence.

4.63. **External Side-Effect Reality bridge check**

   After reading Quality Gates, specs, design, `goal.md`, Builder Plan and the
   OpenSpec Map, scan for external side-effect claims: Supabase, Postgres,
   database, DB, storage, bucket, queue, webhook, auth, billing, email,
   notification, external API mutation, persisted workflow/status updates, or
   remote trace indexing.

   If triggered, read:

   ```text
   /home/simon/.codex/skills/shared/references/openspec-external-side-effect-reality.md
   ```

   If no matching Quality Gate exists, pause before productive edits unless
   the current work is only to materialize that gate. Broad implementation must
   not proceed with an implicit persistence/status-write obligation.

   During implementation:

   - preserve an entry-point matrix for the affected workflow or stage:
     product/user entry path, new runtime path, adapter/writer, trace write and
     external write;
   - run the highest applicable real entry path before closing the gate;
   - verify target schema/column existence in the same external system the run
     uses;
   - query the expected external rows or records by run/workflow/request IDs;
   - check success/error/status fields, not only response status or trace
     presence;
   - verify downstream reload/reference behavior when the side effect exists
     to feed another stage or consumer;
   - check that changed productive mutations fail loud on write errors.

   Local migration files, generated types, unit tests, trace artifacts, fixture
   replay, browser submit success and API responses are partial evidence only.
   Do not mark a persistence/status side-effect gate `passed` until real
   write-read evidence exists or an accepted deferral records owner, risk and
   follow-up.

4.64. **Browser/API/Runtime Evidence bridge check**

   After reading Quality Gates and Builder Plan, scan for browser, user-visible
   path, API route, route registry, trace viewer, stage/substage, replay,
   resume, handoff or runtime-ID claims.

   If a browser/user-visible gate is present, do not close it with command
   output alone. Save or reference a durable success artifact: screenshot,
   Playwright trace/video, browser report, or an accepted deferral. The
   evidence must name the visible success state and the linked runtime/API/
   persistence/trace boundary.

   If an API route is added or relied on, verify handler file plus every active
   route registry/wiring used by the project, including local dev routing when
   separate from production/server routing. Run a direct HTTP smoke test
   against the active runtime and verify success/error fields and auth/admin
   behavior.

   If stage/substage IDs, trace artifact keys, resume/replay IDs or dashboard
   status IDs are used, extract them from current runtime code, constants,
   actual traces or accepted trace artifacts before implementing UI or logic.
   Do not trust proposal/design names alone when runtime evidence exists.

4.645. **Evidence Claim Integrity bridge check**

   After reading Quality Gates and Builder Plan, scan for evidence that could
   be accidentally promoted beyond what it proves. Read
   `/home/simon/.codex/skills/shared/references/openspec-evidence-claim-integrity.md`
   when workflow success, bounded stage/task ranges, trace visibility, status
   transitions, dataflow handoffs, historical-match selection, resume behavior,
   cache/idempotent reuse or partial E2E evidence is in scope.

   During implementation:

   - record the claim class for each material proof, such as
     `persistence_write`, `workflow_success`, `bounded_stage_run`,
     `dataflow_handoff`, `trace_generation`, `trace_visibility`,
     `status_transition`, `current_run`, `historical_match`,
     `resume_from_existing` or `runtime_config`;
   - bind every proof to the concrete subject ID: run, request, workflow, job,
     trace, row, artifact or scenario identifier;
   - explicitly state adjacent claims not proven by partial evidence;
   - do not accept `failed`, `running`, `pending`, historical-match evidence or
     recorded-only configuration as workflow success unless the contract says
     the test is expected-failure, comparison-only or recorded-only;
   - for bounded execution claims, prove the runtime enforced the boundary,
     not merely that UI/API stored the requested range;
   - for trace visibility claims, prove both generation and indexed/queryable
     visibility through the intended table/API/viewer;
   - for dataflow handoff claims, prove the downstream consumer accepted the
     same contract fields the producer wrote.

4.65. **Builder Plan bridge check**

   Check for:

   ```bash
   test -f "openspec/changes/<name>/builder-plan.md" || test -f "openspec/changes/<name>/implementation-plan.md"
   ```

   If present, read it together with the context files and read
   `/home/simon/.codex/skills/shared/references/openspec-builder-plan.md`.
   Prefer `builder-plan.md`; treat `implementation-plan.md` as a legacy alias.

   Treat the Builder Plan as an execution layer below OpenSpec contracts. It
   can tell you exact files, tests, commands and red/green steps, but it cannot
   override specs, prompt contracts, maps, `goal.md`, ledger rows, accepted
   Simon decisions or Stage Authoring rules.

   If OpenSpec artifacts, map, `goal.md`, ledger or Simon's request require a
   Builder Plan and it is missing, pause before implementation and create or
   route to creation of `openspec/changes/<name>/builder-plan.md`.

   Pause before editing when:

   - `tasks.md` is broad or abstract and no Builder Plan exists, even though
     implementation touches multiple services, stages, prompts, schemas,
     traces, cleanup paths or evidence surfaces;
   - the Builder Plan names fields, JSON shapes, prompt text, enum values,
     examples, fallback behavior or compatibility bridges that cannot be traced
     to a higher-authority OpenSpec contract;
   - the Builder Plan conflicts with prompt contracts, specs, map, ledger,
     `goal.md`, Stage Authoring rules or accepted Simon decisions;
   - a proposed shadow workbench lacks active-loader exclusion, cutover
     criteria or cleanup/promotion evidence.

4.66. **Work Slice execution check**

   After reading context files, identify whether `proposal.md`, `design.md`,
   specs, `tasks.md`, `goal.md` or `builder-plan.md` define work slices, slice
   ids such as `WS-01`, legacy `FS-01`, dependency-ordered work sections, or
   per-slice acceptance criteria.

   Treat work slices as an optional execution grouping below OpenSpec
   contracts.
   They help preserve the plan-to-spec structure from Explore/Propose; they do
   not override specs, tasks, prompt contracts, maps, `goal.md`, quality gates
   or accepted Simon decisions.

   If slices are present:
   - build a compact slice status table with id, dependency ids, related task
     ids, acceptance/evidence target and current status;
   - execute slices in dependency order unless artifacts explicitly mark them
     independent or parallelizable;
   - when a task belongs to a slice, state the slice while working on the task;
   - do not mark a slice-related task complete until the task evidence and the
     slice acceptance/evidence criteria are satisfied or explicitly deferred by
     an accepted decision;
   - after the last task in a slice, run or record the slice-level acceptance
     check before moving to a dependent slice.

   If the change is narrow and tasks are already concrete, do not require work
   slices. If the change is broad, multi-surface or migration-like and
   artifacts do not preserve traceable slices while `tasks.md` is abstract,
   pause before implementation and suggest updating artifacts or creating
   `builder-plan.md`. Do not invent a private work breakdown from chat memory
   and implement against it.

4.67. **Subagent execution boundary**

   If subagents are available or explicitly authorized for implementation, read
   `/home/simon/.codex/skills/shared/references/openspec-subagent-policy.md`
   before delegating.

   Use subagents only for disjoint work slices with explicit file ownership,
   clear tests/evidence, and no shared-contract ambiguity. The main agent owns
   integration, task completion, validator runs, prompt fidelity, and final
   handoff. Do not delegate shared prompt text, schemas, handoff contracts,
   quality gates, `goal.md`, or task checkbox completion unless the artifact
   has a bounded owner, deterministic validator, and recovery path.

   If a subagent times out, hangs, or returns partial output twice in the same
   workflow, stop delegating for that workflow and continue locally or block
   with the exact reason.

4.7. **Ziel-Weg-Fitness execution check**

   Read `/home/simon/.codex/skills/shared/references/openspec-ziel-weg-fitness.md`
   when the artifacts mention Ziel-Weg-Fitness, minimum sufficient path,
   alternative paths, A/B, or `$ab-test-lab`.

   Do not inflate the selected path during implementation. If implementation
   reveals a simpler equivalent path, a materially better alternative, or an
   empirical uncertainty that the proposal did not route to A/B, pause and
   suggest artifact update, `$ab-test-lab`, `$cto-review`, or Simon decision
   instead of silently changing the path.

4.75. **Meta-Contract Linter apply preflight**

   After reading context files and before productive edits, if the change
   contains `quality-gates.md`, `implementation-ledger.md` or
   `builder-plan.md`, run:

   ```bash
   python3 ~/.codex/skills/shared/scripts/openspec_meta_lint.py \
     --change-dir openspec/changes/<name> \
     --mode apply
   ```

   If the linter exits non-zero, stop before code, prompt, docs, migration or
   move work begins. Fix safe structural meta-artifact problems first, or
   report the blocker if it needs an artifact/source decision.

   The linter is mechanical only. It checks parseability, required fields,
   allowed values, phase-aware status rules and required sections. It does not
   prove that a gate is fachlich correct or that implementation evidence is
   sufficient; Verify and OpenSpec Review still own that.

5. **Show current progress**

   Display:
   - Schema being used
   - Progress: "N/M tasks complete"
   - Remaining tasks overview
   - Dynamic instruction from CLI
   - OpenSpec Map status: `present`, `missing_not_needed`,
     `missing_recommended`, or `missing_required`
   - Prompt Contract status: `not_applicable`, `present`,
     `missing_required`, or `blocked`
   - Goal Brief status: `present`, `missing`, or `draft_only`
   - Goal Brief doctrine status: semantic boundary, prompt boundary,
     LLM container boundary, Must-Survive-Facts, and required evidence when
     present
   - Goal Brief dataflow status: input/prompt/JSON/check/handoff trace
     requirements when present
   - Goal Brief testing status: required test layers, browser runtime contract,
     missing required evidence, and deferred evidence when present
   - Source Foundation status: `not_applicable`, `present`, `missing_required`,
     or `blocked`
   - Implementation Ledger status: `not_applicable`, `present`,
     `missing_required`, `in_progress`, `blocked`, or `complete`
   - Quality Gates status: `not_applicable`, `present`, `missing_required`,
     `blocked`, `in_progress`, or `complete`
   - Builder Plan status: `not_applicable`, `present`, `legacy_alias_present`,
     `missing_required`, `blocked`, or `not_required`
   - Meta-Contract Linter status: `not_applicable`, `ran_clean`, or
     `ran_with_findings`
   - Work Slice status: `not_applicable`, `present`,
     `missing_recommended`, `missing_required`, or `blocked`

6. **Implement tasks (loop until done or blocked)**

   For each pending task:
   - Show which task is being worked on
   - Show the matching work slice when present and respect slice dependency
     order
   - Read the matching Builder Plan task when present; if none matches, use
     OpenSpec task context and state that execution is task-only
   - Write or run the failing test first when the task is testable; otherwise
     record a concrete `no_test` rationale tied to the evidence gate
   - Verify the expected failure when a red test exists
   - Make the minimal code, prompt, runtime, docs or cleanup change required
   - Run the exact passing verification command or required evidence check
   - Run or record the slice-level acceptance check when this task completes
     the final open task for a slice
   - Update implementation-ledger rows and Builder Plan checkboxes/evidence
     before marking the OpenSpec task complete
   - Update applicable Quality Gate evidence/status before marking the
     OpenSpec task complete
   - Mark task complete in the tasks file: `- [ ]` → `- [x]` only after its
     evidence gate is satisfied
   - Continue to next task

   **Pause if:**
   - Task is unclear → ask for clarification
   - Implementation reveals a design issue → suggest updating artifacts
   - A matching Builder Plan task is required but missing, too vague, or
     conflicts with higher-authority OpenSpec contracts
   - A broad or multi-surface change has abstract tasks and no traceable work
     slices, Builder Plan or accepted artifact update
   - A task would be marked complete while its work-slice acceptance,
     dependency or evidence target remains unmet
   - A concrete Builder Plan step would invent or drift field names, JSON
     shapes, prompt text, example semantics, enum values, fallback behavior or
     compatibility bridges
   - A red test is required but cannot be written or run, and the artifacts do
     not allow a `no_test` rationale
   - A required source foundation is named but unread, missing, or conflicting
   - Goal Brief stop/pause rule triggers → pause and report the specific rule
   - A `goal.md` doctrine check is about to be violated, especially lists for
     semantic judgments, prompt examples as hidden case logic, shape/fact loss
     across handoffs, or missing required evidence
   - A `goal.md` LLM Container Contract or Dataflow Integrity Contract is about
     to be bypassed: selected input, rendered prompt, raw LLM answer, parsed
     JSON, validation/cleanup, canonical handoff, or next consumer would become
     untraceable
   - A map, spec, design, task, or `goal.md` names prompt-contract files and
     the implementation is not using the OpenSpec-local prompt-contracts as the
     target for productive prompt text
   - A prompt contract defines a System Prompt or User Prompt but the effective
     provider request does not prove that those parts are transported according
     to the Prompt-Request-Parity gate
   - A GTM Stage change violates the Stage Authoring entrypoint by mixing
     prompt truth, runtime truth, architecture explanation, Source Map
     references, trace/evidence checks, validation, handoff, or replay
     responsibilities without a clear owner and test/evidence path
   - A target prompt contract would be partially copied, paraphrased, or
     silently changed without an OpenSpec artifact update and explicit reason
   - The deterministic prompt-fidelity check
     (`validate_prompt_fidelity.py`) reports errors for a touched prompt
     operation
   - A Quality Gate that blocks `apply` is unresolved, evidence-free, failed,
     blocked, or would be marked complete by assertion
   - A required External Side-Effect Reality Gate is missing, has no real
     write-read evidence, uses only local/code/trace/browser/API partial
     evidence, lacks target-environment identity, omits status/error checks, or
     leaves productive mutation errors unchecked
   - A required test layer, browser runtime proof, E2E report, screenshot,
     trace, or other Testing Contract evidence is missing
   - A required implementation-ledger row is missing, still `todo`, lacks
     evidence, or a related row is not final while the task would be marked
     complete
   - Error or blocker encountered → report and wait for guidance
   - User interrupts

7. **On completion or pause, show status**

   Display:
   - Tasks completed this session
   - Overall progress: "N/M tasks complete"
   - Work Slice status: completed slices, blocked slices and remaining
     slice-level evidence
   - Quality Gates status: completed gates, open gates, deferred gates and
     missing evidence
   - Vault Write-Back status: `written`, `skipped_no_vault_worthy_learning`,
     `skipped_quality_gate`, or `skipped_unavailable`
   - If all OpenSpec tasks are done but Goal Brief required evidence is still
     missing: report `implementation_tasks_done_but_goal_evidence_open`
   - If all OpenSpec tasks and required Goal Brief evidence appear done, run
     or route to `/home/simon/.codex/skills/openspec-verify-change/SKILL.md`
     before claiming archive readiness. Verification is the gate between
     "implementation tasks done" and "ready to archive".
   - If verify finds CRITICAL issues, report `verification_failed` and keep the
     change open.
   - If verify passes and `goal.md` has a Completion Review Plan, create or
     prepare CEO Review using `/home/simon/.codex/skills/ceo-review/SKILL.md`;
     suggest archive only after verify and CEO Review readiness are clear.
   - If paused: explain why and wait for guidance

7.8. **Vault Write-Back — OpenSpec Apply Learnings (Automatic)**
<!-- requires: vault_writer >= 1.0.0, vault_search >= 1.0.0 -->

   Read before writing:
   - `~/.codex/references/knowledge-distillation-protocol.md`
   - `~/projects/second-brain/98-templates/pattern-template.md`
   - `~/projects/second-brain/98-templates/finding-template.md`

   After completion or a meaningful pause, synthesize vault-worthy insights
   from this apply run. Do not dump raw bullets. Only write insights the LLM
   understood and can ground in concrete OpenSpec artifacts, code changes,
   tests, traces, or Goal Evidence.

   Run this only when at least one condition is true:
   - tasks were completed and a non-obvious implementation learning emerged
   - implementation paused because the spec, design, map, tasks, or `goal.md`
     was incomplete
   - a bug/root cause/fix pattern was discovered
   - Goal Brief, OpenSpec Map, tests, traces, or verification prep corrected an
     assumption
   - evidence requirements changed how the implementation had to be done

   Skip silently when the run was routine and produced no reusable learning.
   Report the skip as `skipped_no_vault_worthy_learning` in the final or pause
   status.

   **Type routing:**

   Use `write_pattern` only when the insight is reusable beyond this one
   change: a repeatable implementation, evidence, mapping, verification, or
   recovery pattern.

   A Pattern must follow `pattern-template.md`, including:
   - `## Problem`
   - `## Lösung`
   - `## Implementation Blueprint`
   - `## Nutzungsbeispiel`
   - `## Wann anwenden`
   - `## Wann NICHT anwenden`
   - `## Systemkontext`
   - `## Quellen & Research`
   - `## Herkunft`
   - `## Learning Log`
   - `## Related`
   - at least one meaningful `interacts/...` tag when possible

   Use `write_finding` when the insight is a factual discovery, bug, benchmark,
   gap, failed assumption, trace result, or verification finding.

   A Finding must follow `finding-template.md`, including:
   - `**Kontext:**`
   - `**Insight:**`
   - `**Evidence:**`
   - `**Quelle:**`
   - `## Related`

   **OpenSpec-specific extraction priority:**
   1. Spec-to-implementation gaps
   2. Goal Brief / evidence gate learnings
   3. OpenSpec Map source/target mapping learnings
   4. Bug/root-cause/fix patterns
   5. Verification-prep learnings for `$openspec-verify-change`

   **Hard quality gate:**

   Skip the note unless all are true:
   - the LLM understood the source material, not just extracted bullets
   - the title is searchable and max 80 characters
   - the body is German prose with real umlauts and `ß`
   - evidence is concrete: test output, trace, changed path, error, count,
     diff, or artifact
   - source path is exact, e.g. `openspec/changes/<name>/tasks.md`,
     `openspec/changes/<name>/goal.md`,
     `openspec/changes/<name>/design.md`, test report, trace file, or changed
     implementation file
   - tags include `source/openspec-apply-change`, `type/pattern` or
     `type/finding`, and a fitting `domain/...`
   - no direct file writes into the Vault; always use `vault_writer.py`
   - use heredoc for Python writer calls, never `python3 -c`

   Write at most 3 notes per apply run. If a candidate cannot fill the required
   template sections with real evidence, do not write it and report
   `skipped_quality_gate`.

   Writer call shape:
   ```bash
   source ~/.venvs/sanctum/bin/activate 2>/dev/null && python3 << 'VAULT_EOF'
   import sys
   sys.path.insert(0, str(__import__('pathlib').Path.home() / '.codex/skills/second-brain/scripts'))
   try:
       from vault_writer import write_pattern, write_finding

       # Replace this block with real, template-compliant insights from this
       # apply run. Do not write examples or placeholders.
       #
       # write_finding(
       #     title='Sprechender Titel mit OpenSpec-Bezug',
       #     content=(
       #         '# Sprechender Titel mit OpenSpec-Bezug\n\n'
       #         '**Kontext:** ...\n\n'
       #         '**Insight:** ...\n\n'
       #         '**Evidence:** ...\n\n'
       #         '**Quelle:** `openspec/changes/<name>/tasks.md`\n\n'
       #         '## Related\n'
       #     ),
       #     tags=[
       #         'source/openspec-apply-change',
       #         'domain/openspec',
       #         'type/finding',
       #     ],
       #     source='openspec-apply-change',
       #     description=(
       #         'WHAT: ...\n'
       #         'Trigger: ...\n'
       #         'Betrifft: ...\n'
       #         'Ermöglicht: ...'
       #     ),
       # )

       print('Vault write-back: insights persisted.')
   except Exception as e:
       print(f'Vault write-back skipped: {e}')
   VAULT_EOF
   ```

**Output During Implementation**

```
## Implementing: <change-name> (schema: <schema-name>)

Working on task 3/7: <task description>
[...implementation happening...]
✓ Task complete

Working on task 4/7: <task description>
[...implementation happening...]
✓ Task complete
```

**Output On Completion**

```
## Implementation Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 7/7 tasks complete ✓

### Completed This Session
- [x] Task 1
- [x] Task 2
...

All implementation tasks are complete. Run `$openspec-verify-change` next;
Goal Brief evidence, verification result and CEO Review readiness determine
whether this is ready to archive.
```

**Output On Pause (Issue Encountered)**

```
## Implementation Paused

**Change:** <change-name>
**Schema:** <schema-name>
**Progress:** 4/7 tasks complete

### Issue Encountered
<description of the issue>

**Options:**
1. <option 1>
2. <option 2>
3. Other approach

What would you like to do?
```

**Guardrails**
- Keep going through tasks until done or blocked
- Always read context files before starting (from the apply instructions output)
- If task is ambiguous, pause and ask before implementing
- If implementation reveals issues, pause and suggest artifact updates
- If source/target inventory is missing for a broad, stage-boundary,
  trace/evidence, cleanup, migration, schema/contract, or multi-component
  change, route to `$openspec-map` before implementing from generic tasks.
- For GTM Stage changes, read and enforce
  `docs/architecture/testing-agent-entrypoints/gtm-stage-authoring.md`;
  keep prompt assets, Runtime Stage folders and architecture-stage docs as
  separate truths, and preserve the Runtime Stage role set or document
  intentional bundling.
- If an OpenSpec Map exists, enforce its component map, target paths, tests,
  CTO Review map backchannel, Goal Brief recommendation and later gates as
  implementation context.
- If `builder-plan.md` exists, execute through it as the task-level TDD/evidence
  guide while keeping OpenSpec contracts above it. If a broad or
  contract-sensitive change requires a Builder Plan and it is missing, pause
  before editing productive code or prompts.
- If work slices exist, preserve their dependency order and per-slice
  acceptance/evidence checks while implementing. If a narrow change has
  concrete tasks, work slices are not required. If a broad change lacks
  traceable slices and tasks are generic, pause for an artifact update or
  Builder Plan instead of executing from memory.
- Do not let concrete Builder Plan snippets override specs, prompt contracts,
  map, ledger, `goal.md`, Stage Authoring, or accepted Simon decisions. A more
  concrete but less faithful plan is a blocker, not an implementation shortcut.
- If an OpenSpec Map or OpenSpec artifact includes prompt-contract files,
  enforce the OpenSpec-local `prompt-contracts/` copies as build targets. The
  final prompt implementation must be traceable back to those contract files,
  and any deliberate divergence must be reflected in OpenSpec artifacts before
  code changes continue.
- If `goal.md` exists, keep implementation aligned with it; do not treat
  `tasks.md` checkboxes as sufficient when the Goal Brief says the broader
  stopping condition is unmet
- If `goal.md` contains Doctrine Checks, enforce them as execution guardrails:
  lists must not replace semantic judgments, prompt examples must not become
  hidden case logic, Must-Survive-Facts must survive handoffs, and required
  evidence must exist before done
- If artifacts contain Ziel-Weg-Fitness or A/B routing, preserve the selected
  path and do not bypass a recommended/required `$ab-test-lab` promotion gate
  with plausible-sounding implementation claims.
- If `goal.md` contains an LLM Container Contract or Dataflow Integrity
  Contract, enforce it as a done gate: for material LLM/JSON work, the final
  evidence must let a reviewer inspect selected input, rendered prompt, raw
  LLM answer, parsed JSON, validation/cleanup result, canonical handoff, and
  next consumer. File existence alone is not enough when the trace is empty,
  unparseable, or semantically meaningless.
- If `goal.md` contains a Testing Contract, enforce it as a done gate:
  required unit, integration, golden/parity, browser E2E, workflow, trace,
  screenshot, report, or runtime evidence must exist before claiming the goal
  complete
- If `goal.md` contains a Browser Runtime Contract, use
  the available browser-capable toolchain according to this order: integrated
  browser or browser-automation tool for simple isolated browser proof;
  `chrome-devtools-axi` when available and better fits live, authenticated,
  session-bound, CDP, performance, or user-browser-adjacent proof; direct
  Chrome DevTools MCP as fallback or for unsupported AXI-special cases;
  Playwright or the available test runner as deterministic regression. Do not
  substitute headless/Xvfb/wrong-CDP proof for live runtime proof when the
  contract forbids it. If no browser-capable tool is available, record a
  blocked/deferred evidence state instead of claiming Browser Evidence. See
  `/home/simon/.codex/references/chrome-devtools-axi.md`.
- If `goal.md` contains a Completion Review Plan, finish by creating or
  preparing a CEO Review via `/home/simon/.codex/skills/ceo-review/SKILL.md`;
  this can establish `READY_FOR_CEO_REVIEW`, never CEO approval
- After all implementation tasks are complete, run or route to
  `/home/simon/.codex/skills/openspec-verify-change/SKILL.md`;
  do not suggest archive until verification has no CRITICAL issues and any
  required CEO Review readiness is clear
- If `implementation-ledger.md` exists or is required, keep it aligned with
  actual work. Do not mark a task complete while its ledger rows are missing,
  `todo`, evidence-free, or contradicted by changed files.
- If local meta-artifacts exist, run the Meta-Contract Linter apply preflight
  before productive edits and do not proceed through blocking structural
  findings.
- Keep code changes minimal and scoped to each task
- Update task checkbox immediately after completing each task
- Pause on errors, blockers, or unclear requirements - don't guess
- Use contextFiles from CLI output, don't assume specific file names

**Fluid Workflow Integration**

This skill supports the "actions on a change" model:

- **Can be invoked anytime**: Before all artifacts are done (if tasks exist), after partial implementation, interleaved with other actions
- **Allows artifact updates**: If implementation reveals design issues, suggest updating artifacts - not phase-locked, work fluidly
