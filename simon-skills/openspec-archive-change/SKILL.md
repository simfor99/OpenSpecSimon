---
name: openspec-archive-change
version: "1.1.3-sanctum"
bundle: openspec-simon
bundle_version: "2026.06.22.1"
description: "WHAT: Archives a completed OpenSpec change after readiness checks. WHEN: Use when the user wants to finalize and archive a change after implementation is complete."
license: MIT
compatibility: Requires openspec CLI.
metadata:
  author: openspec
  version: "1.1.3-sanctum"
  generatedBy: "1.3.1"
---

Archive a completed change in the experimental workflow.

**Input**: Optionally specify a change name. If omitted, check if it can be inferred from conversation context. If vague or ambiguous you MUST prompt for available changes.

**Steps**

1. **If no change name provided, prompt for selection**

   Run `openspec list --json` to get available changes. Use the **AskUserQuestion tool** to let the user select.

   Show only active changes (not already archived).
   Include the schema used for each change if available.

   **IMPORTANT**: Do NOT guess or auto-select a change. Always let the user choose.

2. **Check artifact completion status**

   Run `openspec status --change "<name>" --json` to check artifact completion.

   Parse the JSON to understand:
   - `schemaName`: The workflow being used
   - `artifacts`: List of artifacts with their status (`done` or other)

   **If any artifacts are not `done`:**
   - Display warning listing incomplete artifacts
   - Use **AskUserQuestion tool** to confirm user wants to proceed
   - Proceed if user confirms

3. **Check task completion status**

   Read the tasks file (typically `tasks.md`) to check for incomplete tasks.

   Count tasks marked with `- [ ]` (incomplete) vs `- [x]` (complete).

   **If incomplete tasks found:**
   - Display warning showing count of incomplete tasks
   - Use **AskUserQuestion tool** to confirm user wants to proceed
   - Proceed if user confirms

   **If no tasks file exists:** Proceed without task-related warning.

3.5. **Check archive-readiness gates**

   Archive is a move operation, not a verification substitute. Before moving the
   change, inspect the saved readiness artifacts and block on open CRITICAL
   gates.

   Required checks:

   - Verify report:
     ```text
     openspec/changes/<name>/00-OPENSPEC-VERIFY.md
     ```
     If missing, pause and run or route to
     `$openspec-verify-change <name>` before archive. Do not treat missing
     Verify as a warning unless Simon explicitly requests
     `archive_without_verify` and accepts that archive readiness is unproven.

   - Red review:
     ```text
     openspec/changes/<name>/00-OPENSPEC-RED-REVIEW.md
     ```
     Required when `goal.md`, Verify, tasks, CTO Review, CEO Review, or
     Simon's request says Red Review / OpenSpec Review / Team Red is a gate.
     If the report exists, scan verdict and open findings. `BLOCKED`,
     `PAUSED_FOR_DECISION`, unresolved `DECISION`, or CRITICAL findings block
     normal archive.

   - Goal Brief:
     ```text
     openspec/changes/<name>/goal.md
     ```
     If present, inspect its Verification Gate, Completion Review Plan,
     Required Evidence, Deferred Evidence, dependency gates and pause rules.
     Missing required Verify, Review, CEO Review, evidence, upstream change or
     decision blocks normal archive.

   - Implementation Ledger:
     ```text
     openspec/changes/<name>/implementation-ledger.md
     ```
     If present or required by artifacts, verify no required row remains
     `todo`, `blocked`, evidence-free, or deferred without reason/risk/owner/
     follow-up. Incomplete ledger rows block normal archive.

   - Builder Plan:
     ```text
     openspec/changes/<name>/builder-plan.md
     ```
     Also accept legacy `implementation-plan.md` as a signal to inspect, but do
     not create new legacy files. Read
     `/home/simon/.codex/skills/shared/references/openspec-builder-plan.md`
     when a Builder Plan is present or required by proposal, design, tasks,
     map, goal, Verify, Review, CTO Review or Simon's request. Incomplete
     Builder Plan tasks, missing red-test/no-test/pass evidence, contract drift
     findings, or unresolved shadow-workbench cutover/cleanup block normal
     archive.
     If an Intent-Driven Testschrift is present or required by any artifact,
     also read
     `/home/simon/.codex/skills/shared/references/openspec-intent-driven-testschrift.md`.
     Normal archive requires every required Testschrift row to be `passed`,
     `no_test_with_reason`, or `deferred_with_accepted_decision` with accepted
     owner/risk/follow-up. Missing rows, wrong test surfaces, missing browser
     evidence for user-visible claims, missing fresh evidence, missing
     `not_proven` boundaries, over-promoted partial evidence, or generic tests
     that bypass deterministic prompt/LLM/persistence contracts block normal
     archive.

   - Quality Gates:
     ```text
     openspec/changes/<name>/quality-gates.md
     ```
     Read
     `/home/simon/.codex/skills/shared/references/openspec-quality-gates.md`
     when Quality Gates are present or required by proposal, design, tasks,
     map, goal, Verify, Review, CTO Review, Test Review, a source/template
     artifact or Simon's request. Normal archive requires every defined gate to
     be `passed`, `not_applicable_with_reason`, or
     `deferred_with_accepted_decision`. Any gate still open, unresearched,
     failed, blocked, missing evidence, or only candidate/planned blocks normal
     archive.

   - Foundation Coverage:
     When `proposal.md`, `design.md`, `tasks.md`, `goal.md`, an OpenSpec Map,
     CTO Review, Foundation Brief, Test Review or source/template artifact
     names concrete foundation items, read
     `/home/simon/.codex/skills/shared/references/openspec-foundation-coverage-matrix.md`.
     Normal archive requires every required source item to be covered by the
     correct artifact type or explicitly marked `non_goal_with_reason`,
     `accepted_override`, or `deferred_with_accepted_decision`. Missing,
     prose-only or `clarify_first` coverage blocks normal archive.

   - LLM Output Contract Testing:
     When artifacts define structured LLM/Search-LLM/Perplexity/agent/provider
     outputs, parsed-output artifacts, provider normalizers, parser schemas,
     post-LLM transformations or downstream consumers of provider/model fields,
     read
     `/home/simon/.codex/skills/shared/references/openspec-llm-output-contract-testing.md`.
     Normal archive requires the related quality gate, inventory, tests,
     actual run artifacts or accepted deferral to prove raw provider response ->
     provider envelope/normalization -> parsed output -> runtime validator ->
     handoff/consumer conformance. Fixture-only tests can close parser behavior;
     they cannot close actual provider-output or real Stage-output claims.

   If any gate is blocked, show a concise blocker list and ask only if Simon
   wants to force `archive_with_known_critical`. A forced archive must record
   the known blockers and reason in the final summary. Do not silently convert
   CRITICAL gates into ordinary warnings.

4. **Assess delta spec sync state**

   Check for delta specs at `openspec/changes/<name>/specs/`. If none exist, proceed without sync prompt.

   **If delta specs exist:**
   - Compare each delta spec with its corresponding main spec at `openspec/specs/<capability>/spec.md`
   - Determine what changes would be applied (adds, modifications, removals, renames)
   - Show a combined summary before prompting

   **Prompt options:**
   - If changes needed: "Sync now (recommended)", "Archive without syncing"
   - If already synced: "Archive now", "Sync anyway", "Cancel"

   If user chooses sync, use Task tool (subagent_type: "general-purpose", prompt: "Use Skill tool to invoke openspec-sync-specs for change '<name>'. Delta spec analysis: <include the analyzed delta spec summary>"). This is an explicit user-selected sync action, not blanket archive delegation. Proceed to archive regardless of choice.

5. **Perform the archive**

   Create the archive directory if it doesn't exist:
   ```bash
   mkdir -p openspec/changes/archive
   ```

   Generate target name using current date: `YYYY-MM-DD-<change-name>`

   **Check if target already exists:**
   - If yes: Fail with error, suggest renaming existing archive or using different date
   - If no: Move the change directory to archive

   ```bash
   mv openspec/changes/<name> openspec/changes/archive/YYYY-MM-DD-<name>
   ```

5.5. **Foundation Brief Rückkanal**

   If the archived change's `proposal.md` has a `## Source foundation` naming a
   Foundation Brief (frontmatter `binding_status: pre_spec_zielbild`), append a
   dated entry to the brief's `## OpenSpec-Rückkanal` section, e.g.
   `- Stand <YYYY-MM-DD>: archiviert nach
   openspec/changes/archive/YYYY-MM-DD-<name>/.` Dated entries only; never
   rewrite earlier entries. If the brief cannot be updated, report the blocker
   in the summary instead of skipping silently.

6. **Display summary**

   Show archive completion summary including:
   - Change name
   - Schema that was used
   - Archive location
   - Whether specs were synced (if applicable)
   - Verify report status
   - Red review status when applicable
   - Goal Brief, Implementation Ledger and Builder Plan gate status when
     applicable
   - Intent-Driven Testschrift status when applicable
   - Quality Gates status when applicable
   - Foundation Coverage status when applicable
   - LLM Output Contract Testing status when applicable
   - Note about any warnings (incomplete artifacts/tasks)
   - Note about any forced archive with known CRITICAL blockers

**Output On Success**

```
## Archive Complete

**Change:** <change-name>
**Schema:** <schema-name>
**Archived to:** openspec/changes/archive/YYYY-MM-DD-<name>/
**Specs:** ✓ Synced to main specs (or "No delta specs" or "Sync skipped")
**Verify:** ✓ No CRITICAL issues (or forced with known CRITICAL)
**Review:** not required / ✓ cleared / blocked-but-forced
**Builder Plan:** not required / ✓ complete / blocked-but-forced
**Quality Gates:** not required / ✓ all handled / blocked-but-forced

All artifacts complete. All tasks complete.
```

**Guardrails**
- Always prompt for change selection if not provided
- Use artifact graph (openspec status --json) for completion checking
- Don't block archive on warnings - just inform and confirm
- Archive is sequential. Follow
  `/home/simon/.codex/skills/shared/references/openspec-subagent-policy.md`:
  do not delegate the archive decision, move operation, archive-readiness
  verdict, delta-spec choice, or Foundation Brief Rückkanal entry. Use
  subagents at most for read-only hygiene checks or the explicit sync action
  above.
- Do block normal archive on missing Verify, open CRITICAL issues, unresolved
  DECISION findings, incomplete required Goal Evidence, incomplete
  Implementation Ledger rows, incomplete required Builder Plan tasks, or
  unresolved shadow-workbench cutover/cleanup.
- Do block normal archive on incomplete required Intent-Driven Testschrift
  rows, missing RED/no-test rationale, missing fresh evidence, wrong test
  surface, missing browser proof for user-visible claims, or Testschrift rows
  that bypass deterministic prompt/LLM-output/persistence/evidence contracts.
- Do block normal archive when `quality-gates.md` is required but missing, or
  when any defined quality gate is not `passed`,
  `not_applicable_with_reason`, or `deferred_with_accepted_decision`. Proceed
  only if Simon explicitly chooses `archive_with_known_critical`.
- Do block normal archive when required Foundation Coverage is missing,
  prose-only, or still `clarify_first`.
- Do block normal archive when structured provider/model output contracts
  exist but inventory rows, fixture tests, provider-normalizer checks, runtime
  validation, downstream consumer proof, actual run artifacts for real output
  claims or accepted deferrals are missing.
- Preserve .openspec.yaml when moving to archive (it moves with the directory)
- Show clear summary of what happened
- If sync is requested, use openspec-sync-specs approach (agent-driven)
- If delta specs exist, always run the sync assessment and show the combined summary before prompting
