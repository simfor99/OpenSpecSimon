---
name: openspec-verify-change
version: "1.1.12-sanctum"
bundle: openspec-simon
bundle_version: "2026.06.11.3"
description: Verify implementation matches change artifacts. Use when the user wants to validate that implementation is complete, correct, and coherent before archiving.
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.1.12-sanctum"
  generatedBy: "1.3.1"
---

Verify that an implementation matches the change artifacts (specs, tasks, design).

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **If no change name provided, prompt for selection**

   Run `openspec list --json` to get available changes. Use the **AskUserQuestion tool** to let the user select.

   Show changes that have implementation tasks (tasks artifact exists).
   Include the schema used for each change if available.
   Mark changes with incomplete tasks as "(In Progress)".

   **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Check status to understand the schema**
   ```bash
   openspec status --change "<name>" --json
   ```
   Parse the JSON to understand:
   - `schemaName`: The workflow being used (e.g., "spec-driven")
   - Which artifacts exist for this change

3. **Get the change directory and load artifacts**

   ```bash
   openspec instructions apply --change "<name>" --json
   ```

   This returns the change directory and `contextFiles` (artifact ID -> array of concrete file paths). Read all available artifacts from `contextFiles`.

   Also check whether the change has an OpenSpec Red Review:

   ```bash
   test -f "openspec/changes/<name>/00-OPENSPEC-RED-REVIEW.md"
   ```

   If it exists, read it and classify its `Review-Modus`:

   - `pre_apply_red_review` is an execution-readiness review. Verify must
     check that safe `FIX` findings were handled before or during Apply, that
     unresolved `DECISION`, `BLOCKED`, or `PAUSED_FOR_DECISION` findings were
     routed to Simon, and that no one treated the pre-Apply verdict as archive
     or implementation approval.
   - `post_verify_red_review` is the later semantic review. If Verify is being
     rerun after that report, preserve its findings and do not overwrite their
     polarity.
   - Missing or ambiguous mode is a WARNING for narrow changes and CRITICAL
     when `goal.md`, `proposal.md`, `design.md`, or tasks required a pre-Apply
     Red Review before execution.

   Also check whether the change has an OpenSpec-local Goal Brief:

   ```bash
   test -f "openspec/changes/<name>/goal.md"
   ```

   If it exists, read it and verify against its Stop Condition, Doctrine
   Checks, LLM Container Contract, Dataflow Integrity Contract, Testing
   Contract, Browser Runtime Contract, Required Evidence, Deferred Evidence,
   OpenSpec dependency gates, Verification Gate, and Completion Review Plan.
   Treat `goal.md` as the execution control file above `tasks.md`; do not
   treat checked task boxes as sufficient when the Goal Brief requires more
   evidence.

   Also check whether the change has an OpenSpec-local implementation ledger:

   ```bash
   test -f "openspec/changes/<name>/implementation-ledger.md"
   ```

   If it exists, read it and verify row-level completion for folders, files,
   prompts, contracts, tests, traces, docs, Sections, central docs and review
   gates. Read
   `/home/simon/.codex/skills/shared/references/openspec-implementation-ledger.md`
   for the shared contract.

   If `proposal.md`, `design.md`, `tasks.md`, `goal.md`, an OpenSpec Map, CTO
   Review, Reading Contract or Simon's original request says a ledger is
   required but `implementation-ledger.md` is missing, add a CRITICAL issue.

   Also check whether the change has an OpenSpec-local Builder Plan:

   ```bash
   test -f "openspec/changes/<name>/builder-plan.md" || test -f "openspec/changes/<name>/implementation-plan.md"
   ```

   If it exists, read it and verify it against
   `/home/simon/.codex/skills/shared/references/openspec-builder-plan.md`.
   Prefer `builder-plan.md`; treat `implementation-plan.md` as a legacy alias.
   The Builder Plan is an execution layer below OpenSpec contracts, not a new
   source of truth.
   If the Builder Plan, proposal, design, tasks, map, goal, quality gates,
   review or Simon's request says an Intent-Driven Testschrift is recommended
   or required, also read
   `/home/simon/.codex/skills/shared/references/openspec-intent-driven-testschrift.md`.
   Verify that required Testschrift rows exist and that each material claim has
   claim class, public interface, test surface, RED/no-test rationale, minimal
   GREEN, fresh evidence and `not_proven` boundaries. Missing or wrong-surface
   rows are CRITICAL when they control completion, review or archive readiness.

   If `proposal.md`, `design.md`, `tasks.md`, `goal.md`, an OpenSpec Map, CTO
   Review, Reading Contract or Simon's original request says a Builder Plan is
   required but `builder-plan.md` is missing, add a CRITICAL issue.

   Also check whether the change has OpenSpec-local Quality Gates:

   ```bash
   test -f "openspec/changes/<name>/quality-gates.md"
   ```

   If it exists, read it and verify every defined gate against
   `/home/simon/.codex/skills/shared/references/openspec-quality-gates.md`.

   If `proposal.md`, `design.md`, `tasks.md`, `goal.md`, an OpenSpec Map, CTO
   Review, Test Review, source/template artifact or Simon's original request
   says quality gates are required but `quality-gates.md` is missing, add a
   CRITICAL issue.

   Also scan for concrete source foundations (`## Source foundation`,
   Foundation Brief, OpenSpec Map, CTO Review, Goal Brief, Test Review or
   target-contract artifact). If present, read
   `/home/simon/.codex/skills/shared/references/openspec-foundation-coverage-matrix.md`
   and verify that source items are covered by the correct artifact types.
   Add CRITICAL when a material `must_check`, Must-Survive-Fact, prompt
   contract, runtime target, quality-gate candidate, accepted decision,
   non-goal, A/B recommendation or backchannel obligation is only mentioned in
   prose or is absent from specs, tasks, gates, ledger, builder-plan,
   prompt-contracts, tests/evidence packages, non-goals, accepted overrides or
   accepted deferrals.

   Scan loaded artifacts for LLM, model, agent, provider, prompt, Prompt
   Contract, prompt operation registry, model routing, trace viewer, raw
   response, or effective request claims. If present, read
   `/home/simon/.codex/skills/shared/references/openspec-prompt-request-parity.md`
   and verify that the change proves Prompt-Request-Parity or records an
   accepted deferral. Missing evidence is CRITICAL when the change claims
   model-visible prompt behavior, prompt contract implementation, provider
   request correctness, trace truth or review UI correctness.

   Scan loaded artifacts for structured LLM/Search-LLM/Perplexity/agent/
   provider output contracts: output JSON skeletons in User Prompts, required
   fields, enums, nullable fields, `response_format`, `generateObject`,
   Zod/Pydantic/JSON Schema, parser contracts, provider response envelopes,
   normalizers, `*_parsed-output.json`, post-LLM transformations, repair layers,
   projections or downstream handoffs that consume provider/model fields. If
   present, read
   `/home/simon/.codex/skills/shared/references/openspec-llm-output-contract-testing.md`
   and verify that the implementation has output-contract tests covering raw
   provider response, provider envelope/normalization when applicable, parsed
   output, runtime validator/schema and downstream consumer conformance.
   Multi-operation changes must have
   `openspec/changes/<name>/llm-output-contract-inventory.md` or equivalent
   row-level fields. Missing positive/negative fixture tests, missing
   must-survive checks, missing provider-normalizer tests, or fixture-only proof
   for a real provider/Stage-output claim are CRITICAL unless an accepted
   deferral records owner, risk and follow-up.

   If the change contains a `prompt-contracts/` directory, run the
   deterministic prompt-fidelity check:

   ```bash
   python3 ~/.codex/skills/shared/scripts/validate_prompt_fidelity.py \
     --change-dir openspec/changes/<name>
   ```

   Any reported error — frontmatter drift, paraphrased or missing contract
   lines, placeholder/naming drift, output-JSON key drift, or a missing built
   prompt file — is a CRITICAL issue unless an artifact records an accepted,
   Simon-approved deviation. A green LLM-side fidelity claim does not replace
   this mechanical check. Record `prompt_fidelity_status: ran_clean |
   ran_with_findings | tool_missing | not_applicable` in the report.

   Scan loaded artifacts for external side-effect claims: Supabase, Postgres,
   database, DB, storage, bucket, queue, webhook, auth, billing, email,
   notification, external API mutation, persisted workflow/status updates, or
   remote trace indexing. If present, read
   `/home/simon/.codex/skills/shared/references/openspec-external-side-effect-reality.md`
   and verify that the change has an explicit matching Quality Gate or an
   accepted deferral. Missing side-effect gates are CRITICAL when the side
   effect controls correctness, archive readiness, status transitions or
   downstream consumers.

4. **Initialize verification report structure**

   Create a report structure with these dimensions:
   - **Completeness**: Track tasks and spec coverage
   - **Correctness**: Track requirement implementation and scenario coverage
   - **Coherence**: Track design adherence and pattern consistency
   - **Ziel-Weg Fitness**: Track whether the implemented path stayed aligned
     with the minimum sufficient path, alternatives, A/B route and quality
     guardrails recorded in artifacts
   - **Goal Evidence**: Track Goal Brief stop condition, required evidence,
     LLM/dataflow trace contract, testing contract, browser runtime proof and
     completion review readiness
   - **Implementation Ledger**: Track whether required row-level target
     coverage exists and every row has a final status plus evidence
   - **Builder Plan**: Track whether required task-level TDD/evidence execution
     exists, is complete, and stays below OpenSpec contracts
   - **Intent-Driven Testschrift**: Track whether required vertical
     test/evidence rows prove the intended claims through the smallest
     sufficient public interface, with RED/no-test rationale, minimal GREEN,
     fresh evidence, browser proof for user-visible claims and `not_proven`
     boundaries
   - **Quality Gates**: Track whether every defined acceptance/evidence/review/
     archive gate is handled and has required evidence or an accepted deferral
   - **Foundation Coverage**: Track whether concrete source-foundation items
     landed in the correct artifact types and did not remain prose-only
   - **Prompt-Request-Parity**: Track whether prompt contracts, rendered
     prompts, effective provider requests, trace artifacts and review surfaces
     agree on what the model actually received
   - **Prompt Fidelity**: Track the deterministic
     `validate_prompt_fidelity.py` result for every prompt-contract pair
     (mechanical evidence, not LLM judgment)
   - **LLM Output Contract Testing**: Track whether User Prompt return shapes,
     provider route/model, raw provider responses, provider envelope or
     normalization, parsed outputs, runtime validators, fixture tests, actual
     run artifacts and downstream handoffs are tested for positive and negative
     cases without promoting fixture-only evidence to real Stage-output proof
   - **OpenSpec Red Review Handoff**: Track whether pre-Apply Red Review
     findings were handled and whether post-Verify Red Review is still required
   - **External Side-Effect Reality**: Track whether claimed database, storage,
     queue, webhook, auth, billing, email, status, trace-index or external API
     mutations have real write-read evidence from the target system
   - **Contract Polarity**: Track whether source blockers, unresolved
     decisions, non-promotable states and CEO-owned questions were preserved
     as blockers instead of downgraded to defaults, warnings or passing paths

   Each dimension can have CRITICAL, WARNING, or SUGGESTION issues.

5. **Verify Completeness**

   **Task Completion**:
   - If `contextFiles.tasks` exists, read every file path in it
   - Parse checkboxes: `- [ ]` (incomplete) vs `- [x]` (complete)
   - Count complete vs total tasks
   - If incomplete tasks exist:
     - Add CRITICAL issue for each incomplete task
     - Recommendation: "Complete task: <description>" or "Mark as done if already implemented"

   **Spec Coverage**:
   - If delta specs exist in `openspec/changes/<name>/specs/`:
     - Extract all requirements (marked with "### Requirement:")
     - For each requirement:
       - Search codebase for keywords related to the requirement
       - Assess if implementation likely exists
     - If requirements appear unimplemented:
       - Add CRITICAL issue: "Requirement not found: <requirement name>"
       - Recommendation: "Implement requirement X: <description>"

6. **Verify Correctness**

   **Requirement Implementation Mapping**:
   - For each requirement from delta specs:
     - Search codebase for implementation evidence
     - If found, note file paths and line ranges
     - Assess if implementation matches requirement intent
     - If divergence detected:
       - Add WARNING: "Implementation may diverge from spec: <details>"
       - Recommendation: "Review <file>:<lines> against requirement X"

   **Scenario Coverage**:
   - For each scenario in delta specs (marked with "#### Scenario:"):
     - Check if conditions are handled in code
     - Check if tests exist covering the scenario
     - If scenario appears uncovered:
       - Add WARNING: "Scenario not covered: <scenario name>"
       - Recommendation: "Add test or implementation for scenario: <description>"

   **Goal Brief Testing Contract**:
   - If `goal.md` contains `## Testing Contract`:
     - Extract required test layers and critical workflows/scenarios
     - Verify that each required layer has a concrete command, report, trace,
       screenshot, or artifact path
     - If a required layer is missing evidence, add CRITICAL:
       "Required Goal Brief test evidence missing: <layer>"
     - If a layer is deferred, verify reason, risk, owner and follow-up path
       are present; otherwise add WARNING or CRITICAL based on risk
     - If a broad test command exists but does not cover the named critical
       workflow, add WARNING or CRITICAL with the missing workflow

   **Goal Brief Dependency And Verification Gates**:
   - If `goal.md` says the change is secondary, downstream, blocked until
     another OpenSpec change produces fresh evidence, or must run only after a
     named upstream goal/change, verify that upstream change first:
     - Run or inspect `openspec instructions apply --change "<upstream>" --json`
       when the upstream change name is explicit.
     - If upstream tasks are incomplete, add CRITICAL:
       "Upstream OpenSpec dependency incomplete: <upstream>".
     - If upstream Goal Evidence, traces, CEO Review or Evidence Map are named
       as prerequisites but cannot be verified, add CRITICAL.
   - If `goal.md` contains an `OpenSpec Executor Contract` or `Execution
     router`, verify that `openspec status` and `openspec instructions apply`
     were used as task/progress truth; if not evidenced, add WARNING or
     CRITICAL based on risk.
   - If `goal.md` contains a Verification Gate, verify that this verification
     report exists before archive is recommended. The current verify run may
     satisfy this gate, but any required sibling or upstream verify report must
     be present or explicitly deferred with reason, risk, owner and follow-up.

   **OpenSpec Red Review Handoff Gate**:
   - If `00-OPENSPEC-RED-REVIEW.md` exists, verify every `FIX` finding that was
     marked `fixed`, `accepted`, or required-before-Apply has matching changed
     artifacts, evidence, or an explicit no-longer-applies reason.
   - If a pre-Apply Red Review contains `DECISION`, `BLOCKED`, or
     `PAUSED_FOR_DECISION` findings, verify there is a Simon/CEO decision or a
     still-open blocker with preserved polarity. If execution proceeded without
     that, add CRITICAL.
   - If `goal.md` required a pre-Apply Red Review and the report is missing,
     add CRITICAL: "Required pre-Apply OpenSpec Red Review missing."
   - If a pre-Apply verdict such as `APPROVED_WITH_NOTES` is used as evidence
     for archive, completion, production readiness, or implementation success,
     add CRITICAL: "Pre-Apply Red Review overpromoted beyond execution
     readiness."
   - If implementation is complete, verify that the Completion Review Plan
     still requires a post-Verify `$openspec-review`; the pre-Apply report does
     not replace it.

   **Implementation Ledger Gate**:
   - If `implementation-ledger.md` exists, verify:
     - every required row has a final status, not `todo`;
     - final statuses are backed by concrete evidence or no-impact reason;
     - `reviewed_unaffected` rows explain what was checked;
     - file-heavy scope includes individual file rows, not only parent folder
       rows;
     - user-scoped complete sets such as "all Sections", "all prompts" or
       "every first-level folder" are actually represented;
     - changed files are represented in the ledger or have an explicit
       out-of-ledger reason.
   - If a row is missing, `todo`, contradictory, evidence-free, or uses
     `deferred_with_reason` without reason/risk/owner/follow-up, add CRITICAL
     when it controls completion or archive readiness.
   - If `tasks.md` checkboxes are complete but ledger rows are not complete,
     add CRITICAL: "Tasks complete but Implementation Ledger incomplete."

   **Builder Plan Gate**:
   - If `builder-plan.md` or legacy `implementation-plan.md` exists, verify:
     - every executable Builder Plan task has a final status or clear evidence;
     - OpenSpec task mapping exists for important Builder Plan tasks;
     - red-test, `no_test` rationale, passing command, ledger row or evidence
       gate is present for each task where applicable;
     - file targets and test targets are concrete enough for a builder to
       reproduce the work;
     - the plan's self-review is present or its checks are visibly satisfied.
   - Verify that field names, JSON shapes, prompt text, prompt examples, enum
     values, fallback behavior and handoff semantics in the Builder Plan trace
     to higher-authority OpenSpec contracts, prompt contracts, specs, map,
     ledger, `goal.md`, source code, traces or accepted Simon decisions.
   - If the Builder Plan contains contract-conflicting snippets or invented
     shape details, add CRITICAL:
     "Builder Plan contract drift: <detail>".
   - If `tasks.md` checkboxes are complete but required Builder Plan tasks are
     incomplete, evidence-free, or contradicted by implementation, add
     CRITICAL: "Tasks complete but Builder Plan incomplete."
   - If an Intent-Driven Testschrift is required, verify each row:
     - claim class and human intent are named;
     - public interface and test surface are the smallest sufficient proof;
     - RED result or `no_test_with_reason` is recorded before the minimal
       GREEN step, or the missed RED is explicitly marked as deferred/blocked;
     - minimal GREEN and exact command/evidence action are recorded;
     - fresh evidence exists or an accepted deferral records owner, risk and
       follow-up;
     - `not_proven` prevents partial evidence from being promoted;
     - browser/user-visible claims have durable screenshot, trace, video,
       report or accepted deferral plus linked non-browser evidence when
       required.
   - If the Testschrift replaces deterministic prompt, LLM-output, persistence
     or evidence-claim contracts with generic test language, add CRITICAL:
     "Testschrift bypasses deterministic contract: <detail>."
   - If a shadow workbench is present or proposed, verify active-loader
     exclusion, cutover criteria, cleanup/promotion plan and tests/checks that
     prevent accidental production loading. Missing evidence is CRITICAL when
     it affects runtime, prompt, Source Map, route or archive readiness.

   **Quality Gates Gate**:
   - If `quality-gates.md` exists, verify every gate has a valid status from
     the shared contract.
   - Normal completion requires every gate to be in one of:
     `passed`, `not_applicable_with_reason`, or
     `deferred_with_accepted_decision`.
   - If any gate is `candidate`, `needs_research`, `clarify_first`, `planned`,
     `in_progress`, `missing_evidence`, `failed`, or `blocked`, add an issue.
     Use CRITICAL when the gate blocks Apply, Verify, Review or Archive, or
     when severity is CRITICAL. Use WARNING/SUGGESTION only when the gate itself
     defines that lower severity and does not block archive readiness.
   - Verify that required actions and required evidence are concrete. A gate
     that only says "follow source" without actions/evidence is incomplete.
   - Verify that evidence paths, commands, inventories, reports or traces exist
     enough to support the gate claim. If a gate is marked `passed` but evidence
     is missing or weak, add CRITICAL or WARNING based on the gate's severity
     and blocking effect.
   - If a gate is deferred, verify accepted decision, owner, risk and follow-up
     are recorded. Otherwise add CRITICAL when it affects archive readiness.
   - If a gate claims Browser Evidence or a user-visible product path, verify
     the evidence proves the visible UI/browser path and is linked to the
     runtime/API/persistence/trace boundary it claims. Backend route success,
     fixture replay, direct stage imports, console output, or CDP reachability
     alone are not a substitute for Browser Evidence.
   - If a browser/user-visible gate is marked final, require a durable success
     artifact path such as screenshot, Playwright trace/video, browser report,
     or an accepted deferral with owner/risk/follow-up. A passed command
     without a saved success artifact is weak evidence; add CRITICAL when the
     browser path blocks archive readiness.
   - If an API route gate is marked final, verify handler file, every active
     route registry or router wiring used by the project, a direct HTTP smoke
     result against the target runtime, auth/admin/session assertions, and
     success/error fields. A route handler file without runtime registry proof
     is incomplete evidence.
   - If a runtime/stage/trace-viewer gate is marked final, verify that current
     stage/substage IDs, trace keys, replay/resume IDs or status identifiers
     came from runtime code, constants, real traces, or accepted trace
     artifacts. Proposal/design text alone is not enough when runtime evidence
     exists.
   - If a gate or report claims workflow success, bounded execution, trace
     visibility, status transition, current-run proof, historical-match proof,
     resume behavior or dataflow handoff integrity, verify claim class, subject
     IDs and "not proven" boundaries from the Evidence Claim Integrity
     contract. Add CRITICAL when evidence closes a stronger claim than it
     proves.

   **External Side-Effect Reality Gate**:
   - For each claimed external mutation, verify that the OpenSpec materialized
     an explicit side-effect gate or recorded an accepted deferral.
   - Database/persistence gates must show target environment identity and
     target class, the real entry path used, run/workflow/request identifiers,
     schema/column proof in that same target, row-level query proof for
     expected records, success and error/status field assertions, downstream
     reload/reference proof when relevant, and cleanup/retention stance.
     Acceptable target classes include local emulator/dev service, staging,
     production-like environment, or an explicitly redacted project/account/
     cluster/tenant identifier. Missing target class is CRITICAL when it can
     make local and remote evidence indistinguishable.
   - Treat local migration files, generated types, unit tests, trace artifacts,
     fixture replay, browser submit success and API responses as partial
     evidence only. If those are the only proofs for a persistence/status
     claim, add CRITICAL:
     "External side-effect evidence incomplete: <claim>".
   - Verify that changed productive insert/update/upsert/RPC/storage/queue/
     webhook/auth/billing/email calls check and surface errors. If a mutation
     can fail silently while Verify would pass, add CRITICAL:
     "Silent external mutation failure path: <file/path or gate>".
   - Ask the review question from the shared contract: could the external
     target still be empty, stale, missing a column, or in a failed/running
     status if all listed evidence were true? If yes, add CRITICAL or WARNING
     based on whether the side effect controls archive readiness.

   **Evidence Claim Integrity Gate**:
   - When workflow, dataflow, trace, status, persistence, browser or API
     evidence is used, read
     `/home/simon/.codex/skills/shared/references/openspec-evidence-claim-integrity.md`.
   - Verify that each material claim names its claim class and subject ID:
     run, request, workflow, job, trace, row, artifact or scenario identifier.
   - Verify that partial evidence is not promoted to adjacent claims it cannot
     prove. Persistence-only evidence cannot close workflow success; browser
     submit cannot close persistence/write success; disk trace generation
     cannot close indexed trace visibility; historical-match evidence cannot
     close current-run proof; status rows cannot close dataflow integrity
     without consumer/handoff evidence.
   - Verify bounded execution claims prove runtime enforcement, not only UI/API
     recording of a desired range.
   - Verify dataflow handoff claims prove the downstream consumer accepted the
     same contract fields the producer wrote.
   - Verify trace visibility claims include runtime config, generated trace
     evidence and indexed/queryable evidence in the intended table/API/viewer.
   - If any evidence could be true while the claimed workflow/dataflow/trace/
     status behavior remains false, add CRITICAL:
     "Evidence claim overreach: <claim>".

   **Contract Polarity Audit**:
   - Scan `goal.md`, `design.md`, `proposal.md`, `tasks.md`, delta specs and
     named source artifacts for unresolved-decision and blocker markers:
     `Blocking Decision`, `BD-`, `CEO-Entscheidung`, `decision_owner`,
     `open`, `pending`, `clarify_first`, `review_required`,
     `non-promotable`, `non_promotable`, `fail-loud`, `blocked`, `not green`,
     `nicht grün`, and `DONT_BUILD_YET`.
   - For each marker, verify that the OpenSpec preserved the original polarity:
     a source-level blocker remains a blocker, `review_required` is not treated
     as passing evidence, and a `non-promotable` marker is not converted into a
     completed acceptance path.
   - If an unresolved decision affects architecture, governance, product logic,
     scope, cost, risk, promotion, launch readiness, archive readiness or
     future workflow, verify that there is an explicit Simon/CEO decision or a
     canonical accepted policy before the implementation or report claims
     readiness.
   - Treat owner labels such as `Team`, `CTO`, `Builder` or `Codex` as
     advisory only. If a decision remains unresolved and cannot be
     autonomously decided from accepted policy, it requires Simon's CEO
     decision before archive.
   - If the proposal, tasks, implementation or verification report downgraded a
     blocker into a warning/default, add CRITICAL:
     "Contract polarity drift: <source marker> became <weaker state>".
   - If a default was applied to an unresolved decision without a prior CEO
     decision or accepted policy, add CRITICAL:
     "Unapproved default applied to open decision: <decision>".

   **LLM Container And Dataflow Contract**:
   - If `goal.md` contains `### LLM Container Boundary`,
     `### Dataflow Integrity Contract`, or `### Trace Quality Gate` with
     status `applies`:
     - Verify that evidence identifies selected input, prompt source, rendered
       prompt, expected JSON/schema, raw LLM answer, parsed JSON,
       validation/cleanup result, canonical handoff, downstream consumer, and
       Must-Survive-Facts where relevant
     - Verify that trace/report paths exist, are non-empty, and are parseable
     - Read at least one representative trace/report enough to judge whether
       it is meaningful, not merely present
     - If the chain cannot be inspected or the trace only proves an end output,
       add CRITICAL for LLM/pipeline work

   **Browser Runtime Contract**:
   - If `goal.md` contains `### Browser Runtime Contract` with status
     `applies`:
     - Verify runtime class, browser/tool route, project runtime contract path
       where applicable, required E2E report path, screenshot/trace path, and
       rejected runtimes are present
     - Verify the tool policy: integrated browser/browser automation for
       simple isolated browser proof when available; `chrome-devtools-axi`
       when available and better for live, authenticated, session-bound, CDP,
       performance or user-browser-adjacent proof; direct Chrome DevTools MCP
       as fallback or unsupported-AXI special case; Playwright or available
       test runner as deterministic regression; no Browser Evidence claim when
       no browser-capable tool was available. Reference:
       `/home/simon/.codex/references/chrome-devtools-axi.md`
     - If live/authenticated/external/extension proof is required, do not
       accept headless, Xvfb, cookie transplant, wrong-CDP endpoint, or CDP
       reachability alone as proof
     - If browser evidence is missing or the runtime proof contradicts the
       contract, add CRITICAL

7. **Verify Coherence**

   **Design Adherence**:
   - If `contextFiles.design` exists:
     - Extract key decisions (look for sections like "Decision:", "Approach:", "Architecture:")
     - Verify implementation follows those decisions
     - If contradiction detected:
       - Add WARNING: "Design decision not followed: <decision>"
       - Recommendation: "Update implementation or revise design.md to match reality"
   - If no design.md: Skip design adherence check, note "No design.md to verify against"

   **Code Pattern Consistency**:
   - Review new code for consistency with project patterns
   - Check file naming, directory structure, coding style
   - If significant deviations found:
     - Add SUGGESTION: "Code pattern deviation: <details>"
     - Recommendation: "Consider following project pattern: <example>"

   **Goal Brief Doctrine And Completion Review**:
   - If `goal.md` contains Doctrine Checks, verify the implementation does not
     violate semantic-boundary, prompt-boundary, handoff-boundary or evidence
     rules.
   - If `goal.md` contains LLM Container/Dataflow sections, verify they are
     mirrored in actual trace, report, or contract evidence and that the
     canonical handoff is clearly identified.
   - If `goal.md` contains Required Evidence, verify each evidence path exists,
     is non-empty and supports the claim at a shallow but real level.
   - If `goal.md` contains a Completion Review Plan and execution claims
     completion, verify that a CEO Review exists or add WARNING:
     "CEO Review not yet created". If the change is trace-heavy,
     LLM/pipeline/routing/browser/customer-facing work, missing CEO Evidence
     Map is at least WARNING and may be CRITICAL when it blocks review.

8. **Generate Verification Report**

   **Summary Scorecard**:
   ```
   ## Verification Report: <change-name>

   ### Summary
   | Dimension    | Status           |
   |--------------|------------------|
   | Completeness | X/Y tasks, N reqs|
   | Correctness  | M/N reqs covered |
   | Coherence    | Followed/Issues  |
   | Ziel-Weg Fitness | Fit/Issues/A-B needed |
   | Goal Evidence| Required evidence/tests/review |
   | Implementation Ledger | Rows complete / Issues |
   | Builder Plan | Tasks/evidence complete / Issues |
   | Quality Gates | Gates final / Issues |
   | Prompt Fidelity | ran_clean / ran_with_findings / tool_missing / not_applicable |
   | OpenSpec Red Review Handoff | Pre-Apply findings handled / post-Verify pending |
   | External Side-Effect Reality | Write-read evidence / Issues |
   | Contract Polarity | Blockers/decisions preserved |
   ```

   **Foundation Brief Rückkanal**: If `proposal.md`'s `## Source foundation`
   names a Foundation Brief (frontmatter `binding_status: pre_spec_zielbild`),
   append a dated status line to the brief's `## OpenSpec-Rückkanal` section
   after the verdict, e.g. `- Stand <YYYY-MM-DD>: verify abgeschlossen —
   <verdict>`. Dated entries only; never rewrite earlier entries and never add
   a live status field.

   **Issues by Priority**:

   1. **CRITICAL** (Must fix before archive):
      - Incomplete tasks
      - Missing requirement implementations
      - Missing required Goal Brief evidence, required test layer, or required
        browser runtime proof
      - Incomplete upstream OpenSpec dependency or unsatisfied Goal Brief
        dependency gate
      - Missing required `$openspec-verify-change` report before archive
      - Missing or meaningless LLM Container/Dataflow trace evidence when
        required by `goal.md`
      - Contract polarity drift: source blocker, `review_required`,
        `non-promotable`, `clarify_first`, `pending` or open CEO decision was
        downgraded to a warning, default, completed task or passing evidence
      - Missing or bypassed required/recommended `$ab-test-lab` handoff when
        the artifacts say empirical comparison is needed before promotion
      - Missing required `implementation-ledger.md`, incomplete ledger rows,
        ledger rows without evidence, file-heavy scope represented only as
        parent folders, or task completion claimed while ledger rows remain
        unfinished
      - Missing required `builder-plan.md`, incomplete Builder Plan tasks,
        missing red-test/no-test/pass evidence, untraceable contract details,
        or task completion claimed while required Builder Plan work remains
        unfinished
      - Builder Plan contract drift: concrete snippets, field names, JSON
        shapes, prompt text, examples, enum values, fallbacks or hidden bridges
        conflict with higher-authority OpenSpec contracts
      - Shadow workbench archive risk: active-loader exclusion, cutover or
        cleanup evidence is missing for a temporary builder path
      - Missing required `quality-gates.md`, open gate status, missing gate
        evidence, vague gate actions, or a gate marked passed without proof
      - Deterministic prompt-fidelity errors (`validate_prompt_fidelity.py`)
        for any prompt-contract pair without an accepted, Simon-approved
        deviation, or a skipped fidelity run while `prompt-contracts/` exists
      - Missing required pre-Apply `00-OPENSPEC-RED-REVIEW.md`, unresolved
        pre-Apply Red Review `DECISION`/`BLOCKED` findings, unhandled safe
        `FIX` findings that were required before execution, or treating a
        pre-Apply review verdict as archive/completion/implementation approval
      - Missing External Side-Effect Reality Gate for claimed persistence,
        status write, storage, queue, webhook, auth, billing, email, remote
        trace-index or external API mutation
      - Persistence/status side-effect gate closed using only local migration,
        generated types, unit tests, trace artifacts, fixture replay, browser
        submit success or API response evidence
      - Productive external mutation can fail silently because write errors are
        not checked or surfaced
      - Implemented path is materially larger, weaker, or different than the
        recorded minimum sufficient path without updated approval/evidence
      - Unapproved default applied to an unresolved decision that controls
        architecture, governance, product logic, scope, cost, risk, promotion,
        launch readiness, archive readiness or future workflow
      - Each with specific, actionable recommendation

   2. **WARNING** (Should fix):
      - Spec/design divergences
      - Missing scenario coverage
      - Missing CEO Review or CEO Evidence Map when completion is claimed
      - Each with specific recommendation

   3. **SUGGESTION** (Nice to fix):
      - Pattern inconsistencies
      - Minor improvements
      - Each with specific recommendation

   **Final Assessment**:
   - If CRITICAL issues: "X critical issue(s) found. Fix before archiving."
   - If only warnings: "No critical issues. Y warning(s) to consider. Ready for archive (with noted improvements)."
   - If all clear: "All checks passed. Ready for archive."

   **Auto-Archive Handoff**: When the assessment is "Ready for archive" AND
   every remaining chain gate is already satisfied — post-Verify
   `$openspec-review` done with `APPROVED`/`APPROVED_WITH_NOTES` and no open
   `DECISION`, CEO Review done or not required by `goal.md`, all quality gates
   final — proceed directly into `$openspec-archive-change <name>` in the same
   session instead of ending with a suggestion. Do not wait for a new user
   prompt. If any gate is still open (most commonly the post-Verify Red
   Review), name the exact next gate instead and do not archive. The archive
   skill keeps its own gates as the second lock; never bypass them. If
   `$openspec-archive-change` asks for delta-spec sync, force-archive
   confirmation, or another archive-owned choice, surface that archive prompt
   instead of treating the auto-handoff as permission to skip it.

**Subagent verification boundary**

If subagents are available or explicitly authorized, follow
`/home/simon/.codex/skills/shared/references/openspec-subagent-policy.md`.
Verify may use independent evidence auditors for disjoint surfaces such as
tests, traces, browser proof, dataflow, prompt fidelity, or external side
effects. The main agent owns the final `00-OPENSPEC-VERIFY.md`, scorecard,
severity classification, archive-readiness verdict, and auto-archive handoff.
Subagent output is not sufficient evidence until cited files, traces or
commands have been checked.

**Verification Heuristics**

- **Completeness**: Focus on objective checklist items (checkboxes, requirements list)
- **Correctness**: Use keyword search, file path analysis, reasonable inference - don't require perfect certainty
- **Coherence**: Look for glaring inconsistencies, don't nitpick style
- **Ziel-Weg Fitness**: If artifacts mention Ziel-Weg-Fitness, minimum
  sufficient path, alternatives, or A/B routing, verify the implementation and
  evidence preserve that path. Plausible reasoning is not enough when the
  artifact required empirical comparison.
- **Goal Evidence**: If `goal.md` exists, verify the Goal Brief's Testing
  Contract, LLM Container/Dataflow Contract, Trace Quality Gate and Required
  Evidence directly. Also verify dependency gates and verification gates.
  Missing required evidence is not a harmless skip.
- **Implementation Ledger**: If `implementation-ledger.md` exists or artifacts
  require one, verify row coverage, final status and evidence directly. `todo`
  rows, missing file rows in file-heavy scope, and evidence-free
  `reviewed_unaffected` rows block archive readiness.
- **Builder Plan**: If `builder-plan.md` exists or artifacts require one,
  verify task-level red/green/evidence completion directly. The Builder Plan
  must make implementation reproducible, but it remains below OpenSpec
  contracts. Concrete-but-wrong plan details are CRITICAL when they can guide a
  builder into contract drift.
- **Intent-Driven Testschrift**: If artifacts require it, verify vertical
  proof rows directly. Missing claim class, wrong test surface, missing
  browser evidence for user-visible claims, missing RED/no-test rationale,
  missing fresh evidence or missing `not_proven` boundaries block archive
  readiness unless an accepted deferral records owner, risk and follow-up.
- **Quality Gates**: If `quality-gates.md` exists or artifacts require it,
  verify every defined gate directly. All gates must be handled; severity
  changes issue priority and blocking, not whether the gate can be ignored.
- **External Side-Effect Reality**: If artifacts claim durable external state
  changes, verify a real write-read proof from the target system. Do not accept
  local/code/trace/browser/API proof as a substitute for database, storage,
  queue, webhook, auth, billing, email, status or external API mutation proof.
- **Contract Polarity**: Source-level blockers stay blockers. Open decisions
  require Simon's CEO decision or an already accepted policy before archive.
  Defaults are recommendations until accepted; do not accept a warning as a
  substitute for a blocked promotion or non-promotable state.
- **False Positives**: When uncertain, prefer SUGGESTION over WARNING, WARNING over CRITICAL
- **Actionability**: Every issue must have a specific recommendation with file/line references where applicable

**Graceful Degradation**

- If only tasks.md exists: verify task completion only, skip spec/design checks
- If tasks + specs exist: verify completeness and correctness, skip design
- If full artifacts: verify all three dimensions
- If `builder-plan.md` exists without specs/design, still verify its task
  checkboxes, commands, evidence and contract-source claims against available
  artifacts. If artifacts say it is required but missing, do not degrade.
- If `quality-gates.md` exists without specs/design, still verify gate status,
  required actions and evidence. If artifacts say it is required but missing,
  do not degrade.
- Always note which checks were skipped and why

**Output Format**

Use clear markdown with:
- Table for summary scorecard
- Grouped lists for issues (CRITICAL/WARNING/SUGGESTION)
- Code references in format: `file.ts:123`
- Specific, actionable recommendations
- No vague suggestions like "consider reviewing"

Write the report to:

```text
openspec/changes/<name>/00-OPENSPEC-VERIFY.md
```

This saved report is the archive-readiness artifact that
`$openspec-archive-change` can inspect. If the change is already archived, write
the report inside the archived change directory. `00-OPENSPEC-VERIFY.md` is the
canonical machine-discoverable verify artifact. If you also write a richer
report such as `00-OPENSPEC-VERIFY-REPORT.md` or `verification-report.md`, also
create or update the canonical file with the verdict, required evidence paths
and a pointer to the richer report.
