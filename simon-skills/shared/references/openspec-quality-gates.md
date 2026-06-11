# OpenSpec Quality Gates Contract

Use this reference when an OpenSpec change has quality rules that must be made
explicit, executed and verified.

This file defines the gate contract. It is not a repository-specific gate
catalog. Concrete gates must be derived from the user's chat instructions, the
foundation/source file, a template, an OpenSpec Map, a Goal Brief, or verified
repo contracts.

This reference must be mirrored byte-for-byte in both local Codex skill roots:

```text
/mnt/c/Users/Simon/.codex/skills/shared/references/openspec-quality-gates.md
/home/simon/.codex/skills/shared/references/openspec-quality-gates.md
```

## Core rules

1. No implicit gates. A gate exists for a change only after it is written into
   `openspec/changes/<change-name>/quality-gates.md` or explicitly carried as
   a gate candidate that must be materialized before Apply.
2. All defined gates must be handled. Severity changes blocking behavior; it
   does not allow a gate to be ignored.
3. Every gate needs a source. Valid origins are `chat`, `source_file`,
   `template`, `openspec_map`, `goal_brief`, `cto_review`, `test_review`,
   `repo_contract`, or `accepted_decision`.
4. Every gate must say what to do, how to prove it, and what blocks if it is
   not satisfied.
5. A vague rule is not a gate yet. If the action, affected paths or evidence
   are unclear, the status is `needs_research` or `clarify_first`.
6. Every gate must label the claim class it closes. Evidence may only close
   the claim it directly proves; see
   `/home/simon/.codex/skills/shared/references/openspec-evidence-claim-integrity.md`.
7. Gate blocking must match evidence timing. A gate blocks `apply` only when
   the required evidence, decision or precondition must exist before productive
   implementation starts. If the evidence is produced during Apply, the gate
   should normally block `verify`, `review` and `archive`, while its required
   actions guide the first Apply steps.

## Lifecycle

```text
Explore -> Gate Intake
Map     -> Gate Research
Propose -> quality-gates.md
Apply   -> Gate Execution
Verify  -> Gate Verification
Review  -> Gate Challenge
Archive -> Gate Closure Check
```

### Explore

Explore should surface gate candidates when the chat, source file or change
shape suggests one. It must not silently invent a gate from vibes.

Good prompts:

- "This sounds like a quality gate. Should it block Apply, Verify, Archive, or
  only produce a warning?"
- "This source file contains rules a builder could miss. I can turn them into
  explicit gates before proposal."
- "The paths are not precise enough yet. I can map them before we materialize
  the gate."

### Map

Map researches gate candidates when source/path/evidence detail matters. It
should identify affected paths, source contracts, concrete actions and evidence
requirements. It should not execute the gate.

### Propose

Propose writes `openspec/changes/<change-name>/quality-gates.md` when any gate
candidate exists. It links the file from `proposal.md`, `design.md`, `tasks.md`,
`goal.md` and `builder-plan.md` when those files exist.

Propose must classify each gate's evidence timing:

- `pre_apply`: review, source-reading, prompt-contract extraction, blocking
  decision, environment access or entry-contract proof required before
  implementation can safely start. These gates may block `apply`.
- `during_apply`: archive/deprecation inventories, productive prompt
  comparisons, runtime tests, migrations, write-read proof, browser evidence,
  Evidence Lab packages or handoff validation created by implementation. These
  gates should guide Apply and block `verify`, `review` and `archive`, not the
  opening of Apply.
- `post_apply`: promotion, A/B comparison, CEO review, archive readiness or
  downstream follow-up classification. These gates normally block `review` and
  `archive`.

If a gate has `blocks: [apply]`, its `required_evidence` must be obtainable
before Apply. Otherwise split it into a pre-Apply gate plus a during-Apply or
post-Apply gate.

### Apply

Apply executes the gate actions and records evidence. It must not mark a gate
complete without evidence or an accepted deferral decision.

### Verify

Verify reads `quality-gates.md` and checks every defined gate. It must report
open, failed, blocked, missing-evidence or unresearched gates.

### Review

Review challenges whether the gates were correct, complete and actually
proved. It should look for hidden gates that source material required but the
OpenSpec never materialized.

If a `pre_apply_red_review` gate is already `passed` and the change later adds
or materially changes specs, prompt contracts, quality gates, Builder Plan,
ledger rows, output-contract inventory, external side-effect claims or
implementation scope, the prior review is stale for the changed surface. The
gate must require a review addendum or a fresh `$openspec-review` before Apply
uses the modified contract.

### Archive

Normal archive requires every gate to be in a final handled state:

- `passed`
- `not_applicable_with_reason`
- `deferred_with_accepted_decision`

Any gate still in `planned`, `in_progress`, `needs_research`,
`clarify_first`, `missing_evidence`, `failed`, or `blocked` prevents normal
archive. Forced archive with open gates must be explicit and recorded.

## Status values

| Status | Meaning | Normal archive |
|---|---|---|
| `candidate` | Mentioned, not yet materialized | blocked before Apply |
| `needs_research` | Source/path/evidence details must be researched | blocked |
| `clarify_first` | Simon or a source decision is needed | blocked |
| `planned` | Gate is defined but not executed | blocked |
| `in_progress` | Work started, evidence incomplete | blocked |
| `passed` | Action done and evidence accepted | allowed |
| `not_applicable_with_reason` | Gate does not apply; reason and source recorded | allowed |
| `deferred_with_accepted_decision` | Not done now, but owner accepted risk and follow-up | allowed |
| `missing_evidence` | Claimed done but proof is absent or weak | blocked |
| `failed` | Gate check failed | blocked |
| `blocked` | Cannot proceed without outside action or decision | blocked |

## Severity values

| Severity | Meaning |
|---|---|
| `CRITICAL` | Failed or open gate blocks Apply/Verify/Archive unless Simon explicitly forces archive with known blockers. |
| `WARNING` | Must still be handled. May be deferred only with accepted decision, risk and follow-up. |
| `SUGGESTION` | Must still be handled when defined. Can become `not_applicable_with_reason` if intentionally skipped. |

Severity is not a license to ignore a gate. It only changes how serious the
failure is.

## Gate schema

Use this shape inside `openspec/changes/<change-name>/quality-gates.md`:

```yaml
gate_id: <stable snake_case id>
title: <human-readable title>
origin:
  type: chat | source_file | template | openspec_map | goal_brief | cto_review | test_review | repo_contract | accepted_decision
  source: <path, artifact, quote summary, or decision id>
  source_locator: <heading, line, quote, or not_applicable>
applies_when:
  - <concrete condition>
evidence_timing: pre_apply | during_apply | post_apply
severity: CRITICAL | WARNING | SUGGESTION
status: candidate | needs_research | clarify_first | planned | in_progress | passed | not_applicable_with_reason | deferred_with_accepted_decision | missing_evidence | failed | blocked
required_actions:
  - <explicit action>
required_evidence:
  - <concrete evidence path, command, inventory, report, trace, or review proof>
blocks:
  - apply
  - verify
  - review
  - archive
allowed_final_statuses:
  - passed
  - not_applicable_with_reason
  - deferred_with_accepted_decision
decision_escape_hatch:
  owner: Simon | accepted_policy | not_allowed
  required_record: <where the decision must be recorded>
evidence:
  status: missing | partial | complete
  paths:
    - <path>
claim_integrity:
  claim_classes:
    - ui_visibility | browser_entry | api_entry | persistence_write | status_transition | workflow_success | bounded_stage_run | dataflow_handoff | llm_output_contract | trace_generation | trace_visibility | current_run | historical_match | resume_from_existing | runtime_config
  subject_ids:
    - <run/request/workflow/job/trace/row/artifact/scenario id>
  not_proven:
    - <important adjacent claim this evidence must not be promoted to>
notes: <short rationale>
```

## `quality-gates.md` template

```markdown
# <Change name> Quality Gates

> Pfad: `openspec/changes/<change-name>/quality-gates.md`

## Gate summary

| Gate | Severity | Status | Blocks | Evidence |
|---|---|---|---|---|

## Gates

### `<gate_id>` - <title>

```yaml
<gate schema here>
```

## Open gate decisions

## Final gate state

Normal archive is allowed only when every gate is `passed`,
`not_applicable_with_reason`, or `deferred_with_accepted_decision`.
```

## Standard gate derivation

### From chat

If Simon says something "must", "darf nicht", "blockt", "quality gate",
"before archive", "beim Neubau", "beim Cutover", or "falls prompts genutzt
werden", treat it as a gate candidate. Capture the rule explicitly and clarify
missing path/evidence detail.

### From a source file or template

If the foundation/template/source file contains rules the builder must obey,
extract them as gate candidates. Do not flatten a long source into a vague
"follow source" gate. The gate must list concrete actions and evidence.

### From touched paths

Touched paths may suggest gates, but do not make them implicit. The agent may
recommend a gate and research it, then Propose materializes it.

### From external side effects

If a change claims that a real external system is mutated, durable state is
created, or a workflow/status transition is persisted, derive an explicit
External Side-Effect Reality Gate. Read
`/home/simon/.codex/skills/shared/references/openspec-external-side-effect-reality.md`
for the full contract.

Common triggers include Supabase, Postgres, database, DB, storage, bucket,
queue, webhook, auth, billing, email, notification, external API mutations and
workflow/status writes.

The gate must require write-read evidence from the same target system the run
uses. Local migration files, generated types, unit tests, trace artifacts,
fixture replay, browser submit success and API responses are partial evidence
only; they cannot close a persistence gate by themselves.

For database persistence, required evidence must include:

- target environment or Supabase project/schema identity;
- real entry path and run/workflow/request identifiers;
- schema/column existence proof in that target database;
- row-level query proof for the expected tables and fields;
- success-status/error-field proof, such as `status = completed` and
  `failure_reason`/`error_bucket` being null where applicable;
- downstream reload/reference proof when another stage consumes persisted rows.

Use narrow evidence classes such as `production_fresh_intake_browser`,
`production_fresh_intake_api`, `production_fresh_intake_trace` and
`production_fresh_intake_database`. A gate that claims database persistence
needs database evidence or an accepted deferral; browser/API/trace evidence may
support it but does not replace it.

### From workflow, dataflow, trace or status claims

If a change claims a workflow ran successfully, stopped at a requested boundary,
produced/consumed a handoff, made traces visible, updated statuses, or reused a
historical/resume source, derive an Evidence Claim Integrity Gate. Read
`/home/simon/.codex/skills/shared/references/openspec-evidence-claim-integrity.md`.

Common triggers include workflow success, stage/task ranges, trace generation,
trace indexing, viewer visibility, status tables, downstream consumers,
handoffs, reusable historical runs, resume logic, cache hits, idempotent
upserts and scenario fingerprints.

The gate must require a claim ledger that names:

- the exact claim class;
- the subject ID under review;
- the evidence class used;
- what is proven;
- what adjacent claims are explicitly not proven.

Do not let `persistence_write`, `browser_entry`, `api_entry`,
`trace_generation`, `historical_match` or `status_transition` close
`workflow_success`, `dataflow_handoff`, `trace_visibility` or `current_run`
unless the evidence explicitly covers those claim classes.

### From structured provider/model output contracts

If a change defines or relies on concrete LLM/Search-LLM/Perplexity/agent/
provider return fields in a User Prompt, prompt contract, typed parser, JSON
Schema, Zod/Pydantic schema, parsed-output artifact or downstream handoff,
derive an LLM Output Contract Validation Gate.
Read
`/home/simon/.codex/skills/shared/references/openspec-llm-output-contract-testing.md`.

Common triggers include output JSON skeletons, required fields, enums,
structured output, `response_format`, `generateObject`, parser contracts,
provider response envelopes, normalizers, `*_parsed-output.json`,
post-LLM transformations and Stage handoffs.

The gate must require:

- `llm-output-contract-inventory.md` for multi-operation changes, or the same
  row-level fields directly in the gate/Builder Plan for a single operation;
- positive and negative fixture tests for parser, validator, repair/default
  behavior and malformed/missing-field failures;
- route-specific evidence for standard LLM, Search-LLM, Perplexity/agent,
  provider adapter or tool-call operations;
- provider-envelope/normalizer tests when raw provider output is not already
  the business object;
- actual run artifacts when Verify/Review/Archive claim that real Stage or
  provider output matched the target shape;
- handoff/consumer checks when downstream code uses the parsed data;
- must-survive assertions for fields, IDs, citations/source refs and evidence
  refs that must not be dropped, renamed, defaulted or weakened.

Prompt text, TypeScript-only types, fixture-only tests, or a single green model
response are not enough to close a real provider-output or Stage-output claim.
Fixture-only evidence may close parser/validator behavior, but not
`actual_provider_output`, `current_run`, `workflow_success` or a real
`dataflow_handoff`.

## Example: Prompting quality gate

Use when productive prompts, prompt contracts, rendered prompts or LLM-output
contracts are in scope.

Sources may include:

```text
/home/simon/projects/second-brain/07-research/patterns/prompting-best-practices-hub-fuer-llm-pipelines.md
services/gtm-agents/prompts/PROMPT-FILE-CONVENTION.md
```

Required actions should be concrete, for example:

- prompt is a versioned file with YAML frontmatter;
- System Prompt and User Prompt Template are separated and both visible;
- output JSON skeleton is inline in the User Prompt where the LLM sees it;
- external/source content is delimited and explicitly treated as data, not
  instructions;
- unknown handling is explicit (`null`, `[]`, or explicit unknown signal);
- prompt language and output/content language are separate;
- canonical prompt source and rendered prompt trace are linked;
- examples are marked `example_only` and cannot become hidden case logic.

Required evidence should name prompt files, rendered prompt trace paths,
validation commands, review reports or trace artifacts.

## Example: GTM Stage Authoring gate

Use when GTM stages, Stage Source Map, Stage Evidence Lab, prompt/runtime
handoffs or paths under these roots are in scope:

```text
services/gtm-agents/prompts/stage-XX/
services/gtm-ts-runtime/stage-XX/
docs/architecture/stages/stage-XX/
docs/architecture/sections/
```

Source:

```text
docs/architecture/testing-agent-entrypoints/gtm-stage-authoring.md
```

Required actions should explicitly preserve:

- Prompt truth: what the LLM sees;
- Runtime truth: accepted input/output, validation, replay, trace and handoff;
- Human architecture truth: explanation, drift and downstream readers;
- no fourth Stage truth;
- Source Map remains an index, not a semantic owner;
- Runtime Stage role set is present or intentionally bundled and documented.

## Example: GTM trace contract gate

Use when tests, traces, Evidence Lab, stage-runs or trace artifacts are in
scope.

Sources may include:

```text
docs/architecture/tracing/02-tracing.md
services/gtm-ts-runtime/pipeline/trace-contract.ts
```

Required actions should explicitly check:

- Run folder is the entry unit under `<surface-root>/runs/<run-id>/`;
- Stage folders are direct children under the run;
- Run overview and Stage overview slots exist when required;
- LLM artifacts use standard slots:
  `01_input.json`, `02_system-prompt.md`, `03_user-prompt.md`,
  `04_llm-raw-response.json`, `05_llm-parsed-output.json`,
  `06_input-output-alignment-check.json`,
  `07_output-contract-validation.json`;
- new persisted JSON trace artifacts use Trace Envelope v1 when applicable;
- legacy trace path patterns are not introduced as new contract evidence.

## Example: Stage 00 deprecated move gate

Use only when the change explicitly rebuilds, replaces or cuts over Stage 00
content. Do not apply it to a narrow Stage 00 bugfix unless chat/source says
the move is required.

Candidate roots from the current discussion:

```text
docs/architecture/stages/stage-00-ingestion
services/gtm-agents/prompts/stage-00
services/gtm-ts-runtime/stage-00
```

If the actual Stage 00 prompt root differs from
`services/gtm-agents/prompts/stage-00`, Map must resolve and write the concrete
affected prompt root before Apply. Do not guess.

Move rule:

```text
<root>/<relative_path>
  -> <root>/_deprecated/<YYYY_MM_DD>__<relative_path>
```

Definitions:

- `<root>` is one of the concrete roots listed in the gate.
- `<relative_path>` is the original path relative to `<root>`, without leading
  slash.
- There is no reason slug in the path. The reason belongs in
  `quality-gates.md`, not in the archive path.
- If replacing the whole active root, move each replaced top-level file or
  directory under that root. Do not move the root itself, because the root must
  remain available for the rebuilt target structure.
- Do not move `_deprecated` itself, already deprecated content, or unrelated
  files.
- Preserve the directory structure below the prefixed first segment.
- If the destination already exists, stop. Do not overwrite. Record a collision
  decision before continuing.

Examples:

```text
services/gtm-ts-runtime/stage-00/runner.ts
  -> services/gtm-ts-runtime/stage-00/_deprecated/2026_06_07__runner.ts

services/gtm-ts-runtime/stage-00/operations/00a/foo.ts
  -> services/gtm-ts-runtime/stage-00/_deprecated/2026_06_07__operations/00a/foo.ts

services/gtm-agents/prompts/stage-00/rules/shared.md
  -> services/gtm-agents/prompts/stage-00/_deprecated/2026_06_07__rules/shared.md
```

Required evidence:

- pre-move inventory for every affected root;
- list of moved paths with source and destination;
- post-move inventory showing active root and `_deprecated` state;
- explicit list of kept active files with reason, if any;
- no replaced legacy file remains in active root unless explicitly kept;
- collision check result;
- follow-up tests or docs checks that prove the rebuilt active root is used.
