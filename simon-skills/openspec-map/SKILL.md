---
name: openspec-map
version: "1.1.9-sanctum"
bundle: openspec-simon
bundle_version: "2026.06.12.1"
description: |
  WHAT: Creates deterministic pre-proposal source maps for complex OpenSpec changes.
  WHEN: Use when preparing openspec-propose for multi-component, multi-wave, migration, schema, contract, cleanup, or source-heavy work.
  Orchestration: Optional bridge between openspec-explore and openspec-propose.
argument-hint: "[change-or-scope-name] [path-to-briefing-or-scope]"
disable-model-invocation: false
license: MIT
compatibility: Requires repository filesystem access; OpenSpec CLI recommended.
metadata:
  author: openspec
  version: "1.1.9-sanctum"
  generatedBy: "skill-forger"
---

# OpenSpec Map

Create a durable pre-proposal mapping artifact that turns exploration into
concrete input for `$openspec-propose`.

This skill is a bridge, not a gate:

```text
$openspec-explore / $cto-review  ->  $openspec-map  ->  $openspec-propose
                                          ->  $goal-brief when needed
```

It does not modify `$openspec-propose`, does not create proposal artifacts, and
does not implement code. It inventories sources, target paths, contracts,
schemas, prompt contracts, tests, cleanup obligations, effort, and unresolved
blockers so the next proposal can be grounded in real files instead of chat
memory.

When a CTO Review is part of the source set, the map must preserve it as a
decision and risk source for `$openspec-propose`. If mapping discovers new
facts that change, sharpen, or contradict the CTO Review, the map owns an
immediate CTO Review backchannel before final response. If mapping only passes
existing CTO decisions through to proposal generation, it records the later
`$openspec-propose` backchannel obligation.

## When to Use

Use this skill when a future OpenSpec proposal spans:

- more than three components, modules, stages, services, or packages;
- multiple source classes, such as active code, archive, specs, external docs,
  prior art, templates, traces, or design notes;
- staged migration, runtime rewrite, prompt/schema handoff, or parity work;
- cross-cutting contracts, APIs, data models, or test surfaces;
- explicit cleanup, deprecation, removal, or sunset paths;
- enough source context that `$openspec-propose` would otherwise become generic.

Do not use it for:

- single-file fixes or narrow implementation tasks;
- open-ended architecture thinking before the scope is shaped;
- execution, verification, archiving, or CEO approval;
- replacing mandatory source reading in `$openspec-propose`.

Use `$openspec-explore` first when the problem shape is still unclear. Use
`$openspec-propose` directly when the scope is small and already concrete.

Consider `$openspec-map` before `$openspec-propose` or `$openspec-apply-change`
when the conversation reveals phrases like "source map", "welche Pfade",
"was muss gebaut werden", "bin nicht up to date", "Source-/Target-Inventur",
"Stage Map", "Implementation Map", "42 Tasks", or any similar signal that the
OpenSpec exists but the concrete source, target, test, trace, or cleanup
surface is not yet grounded. Skip the map when the change is narrow, paths and
tests are already known, and no inventory-dependent decision remains.

## Process

### 1. Resolve Scope

Identify the intended change, wave, module set, or component list.

Read, when present:

- daily workspace artifacts or CTO memos named by the user;
- existing OpenSpec artifacts under `openspec/changes/<name>/`;
- architecture docs and decisions that define the source of truth;
- earlier map artifacts for the same scope.

If a CTO Review is read, extract and preserve:

- concrete file path;
- `spec_mode_status`;
- `target_openspec_change`;
- open and accepted `BD-*` decisions;
- Hidden Complexity IDs;
- Stop-Regeln;
- Evidence Gates;
- `Zurückzuschreiben nach`;
- any Arbeitsstand checklist item that proposal generation may change.

If a Goal Brief, Pre-Proposal Reading Contract, Test Review, CEO Review, or
OpenSpec Verify artifact is named, record its role instead of flattening it
into generic notes. These artifacts control different gates and should remain
distinct in the map.

### 1.5. GTM Stage Authoring Preflight

When the scope touches GTM stages, Stage Source Map, Stage Evidence Lab,
stage-boundary cleanup, prompt/runtime handoffs, or any path under
`services/gtm-agents/prompts/stage-XX/`,
`services/gtm-ts-runtime/stage-XX/`, or
`docs/architecture/stages/stage-XX/`, read and enforce the compact agent
entrypoint first:

```text
docs/architecture/testing-agent-entrypoints/gtm-stage-authoring.md
```

Use it as the Stage folder convention for mapping: preserve prompt truth,
runtime truth, and human architecture truth as separate source classes; map
the runtime role set; and prevent a fourth Stage truth. Deep-read
`docs/architecture/sections/95-gtm-stage-prompt-runtime-contract-boundaries.md`
only when the entrypoint says the longform source is needed, such as new
Runtime Stage folders, structural stage cleanup, Source Map/replay/trace/
validation/handoff changes, prompt/runtime drift, or a bundling-vs-drift
judgment.

Also read `services/gtm-agents/prompts/PROMPT-FILE-CONVENTION.md` when prompt
assets are in scope, and
`services/gtm-ts-runtime/pipeline/stage-boundary-source-map.ts` when source
ownership, replay, trace, validation, or handoff boundaries are in scope.

If the scope cannot be inferred, ask one concise question. Prefer reasonable
defaults when the source set is discoverable from paths or prior artifacts.

### 1.6. Foundation Brief Gate

A Foundation Brief is a pre-spec Zielbild artifact per
`/home/simon/.codex/skills/shared/templates/openspec-foundation-brief-template.md`
(frontmatter `provenance_class: target_contract`,
`binding_status: pre_spec_zielbild`, status line "Zielbild, nicht aktuelle
Runtime-Wahrheit").

When the mapped scope creates a new GTM runtime stage folder or structurally
re-cuts an existing stage/substage layout (the Section-95 sense of new or
re-cut Runtime Stage folders), a Foundation Brief is **required input**. For
all other scopes it stays recommended input, never a gate.

- If a Foundation Brief exists, treat it as a primary `target_contract`
  source — not as a new source type: extract prompt contracts per step 4.4,
  quality-gate candidates per 4.35, Builder Plan seed per 4.3, ledger
  candidates per 4.2, and carry its open decision markers (`clarify_first`,
  `map_first`, `cto_first`, `BD-*`, `assumed_default`) into
  `propose_readiness` and the map's open questions. Never reclassify brief
  content as `current_runtime_evidence`; verify against real runtime files.
- If the gate applies and no Foundation Brief exists, do not just block.
  Start the guided creation flow from
  `/home/simon/.codex/skills/shared/references/openspec-foundation-grilling.md`:
  read-only research, assumptions package first, dependency-ordered blocking
  questions, soft-stop; then write the brief using the shared template (daily
  workspace artifact by default), validate it, and continue mapping with the
  brief as source.
- If Simon explicitly declines the brief for a stage re-cut, set
  `propose_readiness.status: not_ready_for_propose` with reason
  `foundation_brief_missing`, unless Simon explicitly accepts proceeding
  without it; record that acceptance as a decision in the map.
- Validate any brief created or used here:
  `python3 /home/simon/.codex/skills/shared/scripts/validate_foundation_brief.py <brief-path>`.
- Required briefs must additionally pass the Final-Lücken-Pass from the
  grilling reference (two independent external reviews via `codex exec` and
  `agy -p`, with in-session `foundation_artifact_review` as fallback)
  before the map consumes them. Record the pass as a dated entry in the
  brief's `## OpenSpec-Rückkanal`.

### 2. Check OpenSpec Context

When a change name is known or likely, run:

```bash
openspec list --json
openspec status --change "<name>" --json
```

Use this for context only. Do not create or edit OpenSpec proposal artifacts.

### 2.5. Skill Network Preflight

Before component inventory, classify the map's upstream and downstream skill
relationships.

Upstream sources can include:

- `$openspec-explore` for shaped but pre-spec requirements;
- `$cto-review` for architecture risk, decisions, stop rules and evidence
  gates;
- `$goal-brief` Pre-Proposal Reading Contracts for mandatory deep-read
  obligations;
- `$test-review`, `$ceo-review` or prior verification artifacts for evidence
  and readiness state.

Downstream handoffs can include:

- `$openspec-propose` as the normal next step;
- `$goal-brief` when execution will need an OpenSpec-local `goal.md`;
- `$cto-review` when the map finds material architecture risk and no adequate
  CTO Review exists yet;
- `$openspec-verify-change` and `$ceo-review` as later gates when the map
  already reveals archive-readiness or CEO-facing evidence requirements.

If a CTO Review exists with `spec_mode_status: pending`, `clarify_first`, or
`dont_build_yet`, the map may still be created, but set
`propose_readiness.status: not_ready_for_propose` unless Simon has already
resolved or explicitly accepted the relevant decisions. Do not convert CTO
blockers into mere map notes.

If no CTO Review exists and the mapped scope is broad, migration-like,
LLM-/pipeline-related, data-shape-sensitive, production-facing, or has unclear
rollback/evidence gates, add a recommended `$cto-review` handoff before
proposal generation or mark it as required when the missing decision controls
proposal safety.

### 3. Choose Mapping Mode

Use local mapping for small scopes with up to three components.

For larger scopes, consider subagents only when the current session/tool policy
permits delegation or Simon explicitly asks for it. Read
`/home/simon/.codex/skills/shared/references/openspec-subagent-policy.md`
before delegating. In Map, subagents are report-only component scouts; they are
not artifact owners.

Each subagent receives only:

- component or component group;
- relevant path hints;
- required output schema;
- instruction to read files itself and return a structured report.

Subagents must not edit product code, map artifacts, prompt-contract sidecars,
proposal artifacts, or unrelated docs. They produce reports; the main agent
consolidates them and owns the final map, `propose_readiness`,
prompt-contract extraction, Gate A, and validator interpretation.

### 4. Inventory Components

For each component, identify:

- sources and their classes;
- target paths to create, modify, or delete;
- contracts, schemas, APIs, data structures, and handoffs;
- assets such as prompts, templates, config, fixtures, traces, or examples;
- existing and new tests;
- cleanup and obsolete paths;
- effort range and basis;
- hidden complexity, drift, or unresolved decisions.
- related skill handoffs, especially CTO Review backchannel, Goal Brief,
  verification, CEO Review, or Test Review obligations.
- implementation-ledger obligations: concrete folders, files, prompts,
  contracts, tests, traces, docs, Sections, central docs, symlinks or external
  source targets that later Apply/Verify/Review must track row by row.
- external side-effect surfaces: target system, environment class, entry path,
  mutation/write owner, required write-read evidence, status/error fields,
  downstream reference consumer and cleanup/retention stance.
- evidence claim surfaces: claim class, subject ID, evidence class, adjacent
  claims that must not be inferred, and whether the evidence is current-run,
  historical-match or resume-source proof.
- structured LLM/Search-LLM/Perplexity/agent/provider output surfaces: User
  Prompt output skeletons, route class, provider/model source, provider
  envelope or normalizer owner, required fields/enums, parser/validator paths,
  `*_parsed-output.json` artifacts, actual run-artifact needs,
  post-LLM transformations and downstream consumers.
- API route surfaces: handler/source file, production/server route registry,
  local dev route registry when separate, direct HTTP smoke target, auth/admin
  behavior, and downstream runtime/persistence/trace proof.
- runtime identifier surfaces: stage/substage IDs, trace artifact keys,
  replay/resume IDs, handoff keys and dashboard status IDs, with source class
  (`runtime_code`, `current_runtime_evidence`, `trace_artifact` or
  `target_contract`).
- foundation coverage obligations: source items from Foundation Briefs, CTO
  Reviews, Goal Briefs, Test Reviews or target-contract artifacts that must
  later become specs, tasks, quality gates, ledger rows, builder-plan tasks,
  prompt-contract sidecars, tests or explicit non-goals/accepted deferrals.

Use [output-schema.md](references/output-schema.md) as the component contract.
Use [source-classes.md](references/source-classes.md) to label sources.
Read
`/home/simon/.codex/skills/shared/references/openspec-foundation-coverage-matrix.md`
when a concrete foundation source controls the map. The map should seed the
coverage matrix; `$openspec-propose` owns materializing it into OpenSpec
artifacts.
Use `/home/simon/.codex/skills/shared/references/openspec-implementation-ledger.md`
when the map is broad, file-heavy, cleanup/deprecation-oriented, or Simon asks
that every file/folder/Section be reviewed.

Read
`/home/simon/.codex/skills/shared/references/openspec-evidence-claim-integrity.md`
when workflow success, bounded stage/task ranges, status records, trace
visibility, dataflow handoffs, historical-match selection, resume behavior,
cache/idempotent reuse or partial E2E evidence is in scope. The map must
identify which claim classes require gates and which evidence classes are only
partial.

Read
`/home/simon/.codex/skills/shared/references/openspec-llm-output-contract-testing.md`
when structured LLM/Search-LLM/Perplexity/agent/provider output, parsed-output
artifacts, parser schemas, provider normalizers, post-LLM transformations or
downstream consumers of provider/model fields are in scope. The map must
identify which operations need output-contract gates, whether
`llm-output-contract-inventory.md` is required, and which tests should prove raw
provider response -> provider envelope/normalization -> parsed output ->
runtime validator -> handoff/consumer conformance. The map must also separate
fixture/parser evidence from actual run-artifact evidence.

When any component writes or mutates external state, also read
`/home/simon/.codex/skills/shared/references/openspec-external-side-effect-reality.md`.
Map the highest product/user entry path that must cause the side effect and
list the concrete external records that later `$openspec-propose` must turn
into an External Side-Effect Reality Gate. Do not let local migrations,
generated types, unit tests, trace artifacts, fixture replay, browser submit
success or API responses stand in for a real write-read proof.

### 4.2. Implementation Ledger Inventory

Classify the map's ledger status:

- `not_required`: narrow change; tasks can safely name every target.
- `recommended`: implementation would benefit from a row-level control file.
- `required`: correctness depends on a row-level list of targets and evidence.
- `present`: an OpenSpec-local `implementation-ledger.md` already exists.

Set `required` for broad cleanup, migration, deprecation, folder moves,
multi-component work, source maps with many target paths, or any instruction
like "review every file", "every folder", "all Sections", "all prompts", or
"all first-level directories".

When required or recommended, the map must list ledger candidate rows by
target class:

- folders/components;
- individual files;
- prompt contracts and productive prompt files;
- specs, schemas, migrations, tests, traces, fixtures or eval sets;
- architecture Sections and central docs;
- symlinked or external targets included by the map;
- verification, review, backchannel and documentation gates.

This map does not need to create the final ledger unless the OpenSpec change
directory already exists and Simon asked to store the map inside it. Otherwise
it must tell `$openspec-propose` to create or require
`openspec/changes/<name>/implementation-ledger.md`.

### 4.3. Builder Plan Seed Inventory

Read
`/home/simon/.codex/skills/shared/references/openspec-builder-plan.md` when the
change is broad, implementation-sensitive, or Explore/chat signals
`builder_plan_status: recommended` or `required`.
Also read
`/home/simon/.codex/skills/shared/references/openspec-intent-driven-testschrift.md`
when Explore/chat signals `testschrift_status: recommended` or `required`, or
when mapped surfaces include user-visible paths, browser proof, API routes,
product-entry workflows, runtime/dataflow handoffs, prompts, structured LLM
output, persistence, traces, migrations or schemas.

Classify the map's Builder Plan status:

- `not_required`: narrow change; `tasks.md` can name exact files, tests and
  evidence without guessing.
- `recommended`: proposal can be written safely, but Apply would benefit from a
  task-by-task TDD/evidence plan.
- `required`: implementation correctness depends on a concrete executable plan
  because tasks alone would be too abstract or contract-sensitive.
- `present`: `openspec/changes/<name>/builder-plan.md` already exists.
- `blocked`: a Builder Plan cannot be seeded until missing source, ownership,
  contract or Simon-decision gaps are resolved.

When recommended or required, include a `Builder Plan Seed` section in the map:

- existing implementation patterns, helper APIs, similar files and local test
  styles that a builder should follow;
- candidate create/modify/delete target files and target test files;
- candidate red/green/evidence loops with exact commands when known;
- Intent-Driven Testschrift seed rows for material claims: candidate
  `claim_class`, public interface, test surface, RED/evidence-before-change
  expectation, minimal GREEN target, fresh evidence path and `not_proven`
  boundaries. Do not create a second task graph outside OpenSpec; these seed
  rows are input for `builder-plan.md`.
- OpenSpec tasks or future outcomes that need a concrete builder task;
- contract-risk warnings where a concrete plan might invent field names, JSON
  shapes, prompt examples, enum values, fallback behavior or hidden
  compatibility bridges;
- shadow-workbench classification if temporary shadow folders are proposed,
  including active-loader exclusion, cutover criteria and cleanup obligations.
- browser success artifact requirement when user-visible proof is in scope:
  expected route/page, visible success state, screenshot/trace/report path, and
  linked runtime/API/persistence/trace boundary.
- API route registry and runtime-ID inventory tasks when those surfaces are in
  scope.
- evidence-claim ledger tasks when an E2E, trace, status, persistence or
  workflow proof could otherwise be promoted to a stronger claim.

The map seeds the Builder Plan; it should not write implementation code and
should not turn sketches into target contracts.

### 4.35. Quality Gate Research

Read
`/home/simon/.codex/skills/shared/references/openspec-quality-gates.md` when
Explore, chat, a source file, a template, `goal.md`, a CTO Review, or the
change shape carries `quality_gates.status: candidates`, `clarify_first`, or
`map_first`.

Map does not execute gates and does not create proposal artifacts. It researches
gate candidates only when details matter for a safe proposal:

- affected paths, owners and source contracts;
- concrete required actions;
- concrete required evidence;
- missing detail or Simon-owned decisions;
- whether the gate can be materialized by `$openspec-propose`, needs more
  mapping, or must pause for clarification.

Do not turn touched paths into implicit gates. Touched paths can suggest a
gate; the map must still name the semantic acceptance/evidence/archive
constraint and its source.

Include a `Quality Gates` section in the map when candidates exist, with:

- `quality_gates.status: none | candidates | clarify_first | map_first |
  ready_for_propose`;
- each candidate's origin, source, source locator, applies-when condition,
  missing detail, recommended severity, required actions, required evidence and
  suggested next step;
- each external side-effect gate candidate's target environment, entry path,
  expected external records, required status/error assertions, write-read proof
  and evidence class such as `production_fresh_intake_database`;
- a downstream obligation for `$openspec-propose` to materialize
  `openspec/changes/<name>/quality-gates.md` when any candidate remains.

If the source foundation contains a quality gate candidate, Must-Survive-Fact,
scope freeze, A/B recommendation, prompt-contract obligation, external
side-effect rule, Evidence Lab rule or backchannel obligation, do not leave it
only in source prose. Add it to the map's foundation coverage obligations with
the expected downstream artifact type: spec, task, gate, ledger, builder-plan,
prompt-contract, test/evidence package or non-goal/deferral record.

Structured LLM output contracts are quality-gate candidates when the User
Prompt or typed schema defines concrete fields. Map must name the expected
parser/validator and test surface when known, or mark that detail as
`needs_research` for `$openspec-propose`.

### 4.4. Prompt Contract Extraction

When a CTO Review, Goal Brief, Reading Contract, Test Review, or source prompt
file contains concrete prompt text that a future builder must preserve, the map
must treat it as a first-class `prompt_contract`, not as narrative context.

Concrete prompt signals include:

- headings such as `System Prompt`, `User Prompt`, `Prompt-Template`,
  `Prompt-Contract`, `Vorgeschlagenes System-Prompt-Template`,
  `Vorgeschlagenes User-Prompt-Template`, or equivalent;
- fenced prompt blocks intended as `target_contract` or `proposed_shape`;
- source text saying the prompt must be included, mirrored, copied, preserved,
  or used as a build target.

For each concrete prompt contract, create or require a sidecar file:

```text
<map-dir>/<same-prefix>_<slug>__prompt-contracts__YYYY_MM_DD__HH-MM/
  system-prompt.md
  user-prompt.md
  prompt-view-input-contract.md
```

If the OpenSpec change directory already exists and Simon wants the map stored
with the change, use:

```text
openspec/changes/<name>/prompt-contracts/
```

If the OpenSpec change directory does not exist yet, create the sidecar files
in the map/daily workspace and record them as provenance contracts. The map
must then tell `$openspec-propose` to copy those files into:

```text
openspec/changes/<name>/prompt-contracts/
```

The OpenSpec-local copy becomes the primary build/read source for Apply,
Verify, Goal Brief and Review. The original map/daily files remain provenance
and must not be deleted merely because the OpenSpec-local copy exists.

Prompt-contract files must not be invented. They may only be:

- verbatim copies from source prompt blocks; or
- structural copies that preserve every requirement while explicitly saying
  what was normalized, such as heading removal or placeholder naming.

For Foundation Briefs that follow the shared template's canonical prompt-block
form, do not hand-write sidecars. Use the deterministic extractor first:

```bash
python3 ~/.codex/skills/shared/scripts/extract_prompt_contracts_from_foundation.py \
  --source <foundation-brief> \
  --out-dir <prompt-contracts-dir> \
  --map-path <map-path> \
  --target-change <change-name>
```

The extractor recognizes the template contract by block shape — fenced
Markdown payload with YAML frontmatter containing `operation_id` plus
`# System Prompt` and `# User Prompt` sections. It must not key off
project-specific heading words, stage names, GTM terms, file numbers, or
speaker language. If the extractor cannot find a concrete prompt block, the
map must not invent one; set `propose_readiness.status:
not_ready_for_propose` or record the missing prompt contract as a blocker.

When creating prompt-contract sidecar directories in a Tagesraum, follow the
global Tagesraum prefix rule for directories too: inspect the whole
`docs/todo/YYYY_MM_DD/` tree and allocate the next free `NNN_` prefix. Do not
reuse the map artifact's prefix for a sibling sidecar directory unless Simon
has explicitly chosen a bundle naming exception for that session.

Mechanical extraction sequence:

1. Choose the final map path and prompt-contract directory path.
2. Generate sidecars with the extractor.
3. Write the map artifact at the exact `map_path` referenced by the sidecars.
4. Run Gate A with `validate_prompt_fidelity.py --extraction-check <dir>`.
5. Run `validate_map_briefing.py <map-path>`.

Gate A treats a missing `map_path` target as an error. A directory of green
prompt-contract sidecars without the map file is not a completed map output
and must not be reported as `prompt_contracts_status: created`.

Extraction-mode rules (not a style choice):

- When the source already carries full System/User prompt wording (foundation
  briefs validated by `validate_foundation_brief.py` always do), `verbatim` is
  the mandatory default. `structural_copy` is only valid with an explicit
  `## Normalisierungen` list naming every normalization; without that list the
  contract is invalid.
- LLM routing frontmatter (`llm_route`, `llm_provider`, `llm_model`,
  `llm_model_source`) is copied from the source block, never derived from
  convention defaults when the source is explicit. A deliberate routing change
  is a map finding plus Simon decision, not a silent normalization.
- Wrap extracted prompts in four-backtick `````text` fences when the prompt
  text itself contains triple-backtick blocks.

Each prompt-contract file must include frontmatter:

```yaml
type: prompt-contract
contract_kind: target_contract | proposed_shape | example_only | current_runtime_evidence
source_path: <exact source path>
source_locator: <heading/section, or explicit line range like L10-L20>
extraction_mode: verbatim | structural_copy
map_path: <map briefing path>
target_change: <change name>
```

Quality gate:

- If concrete prompts exist but cannot be extracted with clear provenance, set
  `propose_readiness.status: not_ready_for_propose`.
- If examples and target prompts are both present, separate them into different
  files or mark examples `example_only`.
- The map must include a `Prompt Contracts` section listing every contract
  file, source locator, contract kind, extraction mode, and downstream
  obligation for `$openspec-propose` and `$openspec-apply-change`.
- When prompt contracts are stored outside `openspec/changes/<name>/`, the map
  must include a downstream obligation that `$openspec-propose` localizes them
  into `openspec/changes/<name>/prompt-contracts/` and that downstream skills
  read the localized copies first.
- Do not "improve" prompt wording during mapping. Any proposed improvement is a
  map finding or open question, not a silent edit to the prompt contract.
- Prompt-Optimierungshinweise außerhalb eines fenced Prompt-Contract-Blocks
  sind audit-only. `$openspec-map` folgt diesen Links nicht und nutzt nur den
  aktiven fenced Prompt-Contract-Block als Prompt-Quelle.
- Mechanical extraction gate (mandatory): before the map reports any
  `prompt_contracts_status: created`, run

  ```bash
  python3 ~/.codex/skills/shared/scripts/validate_prompt_fidelity.py \
    --extraction-check <prompt-contracts-dir>
  ```

  It verifies the required frontmatter (`type`, `contract_kind`,
  `source_path`, `source_locator`, `extraction_mode`, `map_path`,
  `target_change`), prompt-text fidelity against the located source block,
  routing parity with the source frontmatter, and the `## Normalisierungen`
  list for `structural_copy`. A failing gate means the contracts are NOT
  `created`; fix them or set
  `propose_readiness.status: not_ready_for_propose`. Prose compliance is not
  enough — this gate exists because a paraphrased contract once passed silent
  review (Stage-00 lesson, 2026-06-10).
- After a green gate, record machine-readable evidence in
  `propose_readiness` so downstream skills see more than a bare `created`:

  ```yaml
  prompt_contract_extraction_gate:
    status: passed
    command: "python3 ~/.codex/skills/shared/scripts/validate_prompt_fidelity.py --extraction-check <dir>"
    checked_at: "<ISO-8601 mit TZ>"
  ```

  `validate_map_briefing.py` re-runs Gate A itself on every listed contract
  file and fails the map when the gate is red or this evidence block is absent
  or malformed, regardless of claimed status.

### 5. Consolidate

Merge component reports into one briefing.

For maps derived from a Foundation Brief, each material component should make
the comparison shape explicit:

- target from Foundation Brief or accepted decision;
- current runtime/prompt/architecture/storage evidence;
- drift or unresolved gap;
- proposal task or gate that must carry the difference forward.

Do not collapse this into a generic component note. This shape is what keeps a
target contract from being mistaken for current runtime truth.

Call out:

- conflicting source-of-truth claims;
- missing required files or unreadable paths;
- schema or contract drift across components;
- upstream or downstream dependency gates;
- CTO Review decisions or stop rules that must survive into OpenSpec;
- Goal Brief or Pre-Proposal Reading Contract obligations that require deep
  reads before proposal writing or execution;
- prompt contracts that must be linked and built verbatim or structurally by
  `$openspec-propose` and `$openspec-apply-change`;
- implementation-ledger status and candidate rows that must survive into
  `$openspec-propose`, `$goal-brief`, `$openspec-apply-change`,
  `$openspec-verify-change`, and `$openspec-review`;
- Builder Plan status, seed tasks, contract-risk warnings, shadow-workbench
  constraints and whether `$openspec-propose` must create
  `openspec/changes/<name>/builder-plan.md`;
- Quality Gate status, researched gate candidates, missing path/evidence detail
  and whether `$openspec-propose` must create
  `openspec/changes/<name>/quality-gates.md`;
- External Side-Effect Reality status, target systems, required write-read
  evidence, entry-point matrix gaps and whether database/external persistence
  proof must block Verify/Review/Archive;
- GTM Stage Authoring obligations from
  `docs/architecture/testing-agent-entrypoints/gtm-stage-authoring.md`,
  including the three-truth source split, affected Stage Source Map entries,
  runtime role completeness, architecture-stage-doc obligations, and required
  docs scan or refresh checks when business logic, stage backbone, or prompts
  change;
- questions that must be answered before proposal generation.

If the initiative has waves, add a wave aggregation section using the schema in
[output-schema.md](references/output-schema.md).

### 6. Write the Map Briefing

Create a Markdown artifact using
[map-artifact-template.md](templates/map-artifact-template.md).

Preferred output location:

- daily workspace artifact when working inside Sanctum daily planning;
- `openspec/changes/<name>/` only when an OpenSpec change already exists and
  the user wants the map stored with that change.

Every human-readable artifact must include a path line directly below the H1.

### 7. CTO Review Map Backchannel

If the map read one or more CTO Reviews, compare the final map findings against
those memos before final response.

Update the source CTO Review in place when it is an active daily/planning
artifact and the map discovers material new state, such as:

- source or target paths that make a CTO assumption stale;
- a scope split between the CTO Review, existing OpenSpec, and implementation
  map;
- a new blocker, source-of-truth conflict, missing evidence gate, or required
  test layer;
- a previously open item now resolved by concrete inventory;
- a recommended change in next skill route, such as `$openspec-propose`,
  `$goal-brief`, `$openspec-apply-change`, `$test-review`, or
  `$ceo-review`.

If the original CTO Review is archival, immutable, or unsafe to edit, create a
linked addendum next to the map or in the same daily workspace. Do not silently
skip the backchannel.

Prefer a compact section named `OpenSpec-Map-Rückkanal`:

```markdown
## OpenSpec-Map-Rückkanal

**Stand:** <YYYY-MM-DD HH:MM>  
**Map:** `<map-path>`  
**Status:** `no_update_needed | updated | addendum_created | blocked`

**Neue Befunde:** <source/target/test/evidence facts discovered by the map>
**Auswirkung auf CTO Review:** <what changed, sharpened, or stayed blocking>
**Auswirkung auf OpenSpec:** <proposal/apply/goal/verify route>
**Offen:** <remaining decisions or evidence gaps>
```

If the map finds no new CTO-relevant facts, explicitly record
`map_backchannel_status: no_update_needed` in the final response. If it finds
new facts but cannot update or add an addendum, report
`map_backchannel_status: blocked` with the exact reason.

### 8. Set Propose Readiness

Set `propose_readiness.status`:

- `ready_for_propose` when the map contains enough source, path, contract,
  test, cleanup, and open-risk context for `$openspec-propose`;
- `not_ready_for_propose` when central sources, target shape, ownership,
  decisions, or required reads are still missing.

Readiness must account for CTO and Goal-Brief obligations:

- A map can be structurally complete but still `not_ready_for_propose` when a
  CTO Review contains unresolved blocking decisions that control proposal
  scope.
- A map can be `ready_for_propose` while still recommending `goal.md` for
  execution, as long as proposal-safe decisions are resolved.
- A source-heavy map should tell `$openspec-propose` whether the map itself is
  enough or whether a Pre-Proposal Reading Contract must be used or created.

End with a lightweight handoff plus explicit skill-network obligations:

```text
Next: Run $openspec-propose <change-name> with <map-path> as the primary briefing source.
```

Use [handoff-convention.md](references/handoff-convention.md) for this section.

### 9. Validate

Before finalizing, run the bundled validator when possible:

```bash
python3 /home/simon/.codex/skills/openspec-map/scripts/validate_map_briefing.py <map-path>
```

Then run repo-required checks for changed files. In Sanctum, documentation
changes under `docs/` require:

```bash
npm run content:check:de-umlauts -- <changed-doc-paths>
npx tsc --noEmit
```

## Output

After creating or updating the map, report:

- map path;
- target change or scope;
- `propose_readiness.status`;
- CTO Review sources used, if any;
- `map_backchannel_status`: `not_applicable`, `no_update_needed`, `updated`,
  `addendum_created`, or `blocked`;
- whether `$openspec-propose` still owes a CTO Review backchannel after
  proposal generation;
- Prompt Contract status: `not_applicable`, `created`, `required_missing`, or
  `blocked`;
- Foundation Brief status: `not_applicable`, `used`, `created_guided`, or
  `declined_by_decision`;
- Implementation Ledger status: `not_required`, `recommended`, `required`,
  `present`, or `blocked`;
- Builder Plan status: `not_required`, `recommended`, `required`, `present`,
  or `blocked`;
- Quality Gate status: `none`, `candidates`, `clarify_first`, `map_first`, or
  `ready_for_propose`;
- Goal Brief / Pre-Proposal Reading Contract status: `not_applicable`,
  `recommended`, `required`, or `present`;
- next skill route: `$openspec-propose`, `$cto-review`, `$goal-brief`,
  `$openspec-apply-change`, `$test-review`, or blocker resolution.

Use real empty YAML lists (`[]`) or omit optional list fields. Do not write
sentinel list items such as `- none`, because downstream skills may treat them
as real paths.

## Resources

- [docs/INDEX.md](docs/INDEX.md): narrative documentation hub for why the skill
  exists, how to use it, and how it hands off to `$openspec-propose`.
- [output-schema.md](references/output-schema.md): required component and
  readiness schema.
- [source-classes.md](references/source-classes.md): default source class
  vocabulary.
- [handoff-convention.md](references/handoff-convention.md): lightweight
  handoff to `$openspec-propose`.
- `/home/simon/.codex/skills/shared/references/openspec-implementation-ledger.md`:
  shared ledger gate for row-level folder/file/prompt/doc/test/evidence
  tracking across Map, Propose, Apply, Verify and Review.
- `/home/simon/.codex/skills/shared/references/openspec-builder-plan.md`:
  shared Builder Plan contract for task-by-task TDD/evidence execution below
  OpenSpec contracts.
- `/home/simon/.codex/skills/shared/references/openspec-quality-gates.md`:
  shared Quality Gates contract for explicit acceptance, evidence, review and
  archive constraints.
- `/home/simon/.codex/skills/shared/references/openspec-subagent-policy.md`:
  shared boundary for when subagents may support OpenSpec work and what must
  stay main-agent owned.
- [abort-modes.md](references/abort-modes.md): when to stop instead of
  producing a misleading map.
- [component-inventory-prompt.md](templates/component-inventory-prompt.md):
  subagent prompt template.
- [map-artifact-template.md](templates/map-artifact-template.md): briefing
  artifact template.
- `docs/architecture/testing-agent-entrypoints/gtm-stage-authoring.md`:
  compact repo-local GTM Stage authoring entrypoint for Stage folders, Source
  Map, Evidence Lab, prompts, runtime contracts, replay, trace, validation,
  handoff, or stage docs. It points to Section 95 only when the longform source
  is needed.
- `/home/simon/.codex/skills/shared/templates/prompt-contract-template.md`:
  sidecar template for concrete prompts that must survive into OpenSpec and
  implementation.
- `/home/simon/.codex/skills/shared/scripts/extract_prompt_contracts_from_foundation.py`:
  deterministic extractor for canonical Foundation Brief prompt blocks; use
  before hand-authored sidecars whenever the shared template's prompt block
  shape is present.
- `/home/simon/.codex/skills/shared/templates/openspec-foundation-brief-template.md`:
  pre-spec Zielbild contract consumed by the Foundation Brief Gate (1.6).
- `/home/simon/.codex/skills/shared/references/openspec-foundation-grilling.md`:
  three-basket assumption/question protocol for guided Foundation Brief
  creation.
- [validate_map_briefing.py](scripts/validate_map_briefing.py): structural
  sanity check for generated map briefings.
