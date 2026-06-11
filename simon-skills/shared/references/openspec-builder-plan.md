# OpenSpec Builder Plan Contract

Use this reference when an OpenSpec change needs a concrete implementation
plan that a builder can execute task by task.

The Builder Plan is not a fourth source of truth. It is an execution layer
below OpenSpec contracts.

## Canonical path

```text
openspec/changes/<change-name>/builder-plan.md
```

`implementation-plan.md` is accepted only as a legacy alias. New artifacts
should use `builder-plan.md`.

## When required

Create or require a Builder Plan when any of these are true:

- `tasks.md` is broad, abstract, or does not name concrete file/test targets.
- The change spans multiple services, stages, prompts, schemas, traces, docs,
  migrations, cleanup paths, or runtime boundaries.
- The change claims an external side effect such as database persistence,
  status writes, queue/webhook writes, auth/billing/email mutations, storage
  writes, or remote trace indexing.
- The change is LLM-, prompt-, crawler-, ranking-, schema-, handoff-, trace-,
  Evidence-Lab-, browser-, or pipeline-quality sensitive.
- The change defines or consumes structured LLM/Search-LLM/Perplexity/agent/
  provider output fields from a User Prompt, parser, schema, provider
  normalizer, parsed-output trace artifact or post-LLM transformation.
- A map, Goal Brief, CTO Review, Test Review, or Simon says implementation
  needs a concrete plan, source map, execution map, TDD plan, or task-by-task
  guide.
- A Foundation Coverage Matrix has items whose implementation could otherwise
  be satisfied by vague tasks, broad folder rows, or prose-only references.

For narrow changes with known files, known tests, and no contract-sensitive
shape decisions, record `builder_plan_status: not_required` and continue.

## Authority order

When artifacts disagree, use this order:

1. OpenSpec-local prompt contracts, specs, design, proposal, `goal.md`,
   `implementation-ledger.md`, OpenSpec Map and explicit Simon decisions.
2. `builder-plan.md`.
3. Chat memory and inferred implementation intent.

If the Builder Plan conflicts with a higher-authority contract, pause and
update artifacts before editing productive code or prompts. Do not silently
choose the more concrete artifact.

## Required sections

Every Builder Plan should include:

```markdown
# <Change name> Builder Plan

> Pfad: `openspec/changes/<change-name>/builder-plan.md`

## Goal

## Contract sources

## File structure

## OpenSpec task map

## TDD / evidence tasks

## Contract-fidelity checks

## Shadow workbench and cutover

## Self-review
```

## Task contract

Each executable task should include:

- linked OpenSpec task ID or task text;
- source contract path and, when useful, section/field locator;
- foundation coverage item or `not_applicable` when a concrete foundation
  source controls the change;
- files to create, modify, delete, or inspect;
- test file and exact command;
- expected failing result before implementation, or an explicit `no_test`
  rationale when a red test is not practical;
- minimal implementation target;
- passing verification command;
- ledger row or evidence gate that proves the work is done.
- for external side effects, the real entry path, target environment, write-read
  query or proof, expected status/error assertions, downstream reference check
  and cleanup/retention stance.
- for production/product-entry evidence, the accepted product-entry or resume
  contract that triggers the path. Direct imports of the target stage/module
  may support unit or fixture evidence but cannot replace entry-contract proof.
- for browser or user-visible paths, the real page/workflow, representative
  test data, expected visible success state, durable screenshot/trace/report
  artifact path, and linked runtime/API/persistence/trace boundary.
- for API routes, the handler file, every active route registry/router wiring
  used by the project, local-dev route wiring when separate, direct HTTP smoke
  command, auth/admin/session assertions, and expected success/error fields.
- for stage, trace viewer, replay, resume, handoff or dashboard status work,
  the runtime ID inventory source: runtime code, constants, real traces,
  accepted trace artifacts or target contract.
- for workflow, dataflow, trace, status, persistence, browser or API evidence,
  the claim class being closed, the subject ID, the evidence class and adjacent
  claims that are explicitly not proven. Use
  `/home/simon/.codex/skills/shared/references/openspec-evidence-claim-integrity.md`.
- for structured LLM/Search-LLM/Perplexity/agent/provider output, the
  `llm-output-contract-inventory.md` row or equivalent row-level fields, User
  Prompt output contract source, route class, provider/model source,
  raw-provider-response/parsed-output evidence, provider-envelope or normalizer
  owner when applicable, runtime parser/validator path, positive and negative
  fixture tests, actual run artifact requirements for real Stage-output claims,
  must-survive fields, default/repair behavior and downstream handoff/consumer
  check. Use
  `/home/simon/.codex/skills/shared/references/openspec-llm-output-contract-testing.md`.
- for A/B recommendations, the exact `$ab-test-lab` handoff or the artifact
  where `not_applicable_with_reason` must be recorded before promotion/archive.

Prefer small tasks that can be verified independently. Do not group unrelated
runtime, prompt, docs, and cleanup work into one untestable task.

## Contract-fidelity rules

- Field names, JSON shapes, prompt text, prompt examples, enum values and
  handoff semantics must be derived from OpenSpec-local contracts, prompt
  contracts, source code, traces, or accepted Simon decisions.
- Code blocks are allowed only when they are contract-grounded. Otherwise mark
  them `implementation_sketch`.
- Examples that show form but not current truth must be marked `example_only`.
- The plan must not invent compatibility bridges, fallback shapes, prompt
  rules, semantic gates, or hidden post-LLM transformations.
- For GTM Stage work, keep prompt truth, runtime truth, human architecture
  truth, Source Map references, traces, replay, validation and handoff owners
  separate.
- For runtime/stage dashboards or trace viewers, do not derive stage/substage
  IDs only from proposal or design prose when runtime code or trace evidence
  exists. Name the source class used for each ID inventory.
- For external side effects, never treat local migration files, generated
  types, unit tests, trace artifacts, fixture replay, browser submit success or
  API responses as complete persistence proof. They are partial evidence until
  a real write-read check proves the target system state.
- For browser evidence, command output alone is not enough when a user-visible
  path blocks archive readiness. The plan must require a durable success
  artifact or an accepted deferral.
- For API routes, handler existence is not runtime proof. Registry/wiring and
  HTTP smoke evidence are required before the route claim is closed.
- For workflow/dataflow/trace/status evidence, do not promote a partial proof
  to a stronger claim. Persistence-only evidence does not prove workflow
  success, generated trace files do not prove trace visibility, historical
  matches do not prove the current run, and recorded-only configuration does
  not prove runtime enforcement.
- For structured LLM/Search-LLM/Perplexity/agent/provider output, do not treat
  prompt text, TypeScript-only types, a single green model answer, parser
  existence or fixture-only tests as proof that the actual provider route
  returned the target shape. The plan must require tests of parsed shape,
  invalid outputs, provider-envelope/normalizer behavior when applicable, real
  run artifacts for real Stage-output claims and any downstream consumer that
  uses the fields.
- Productive external mutations must fail loud: changed insert/update/upsert,
  RPC, queue, webhook, storage, auth, billing or email calls need checked
  errors or an explicit source-grounded reason why the call is fire-and-forget.

## Shadow workbench rules

Temporary shadow paths are allowed only when the plan declares:

- the shadow path and why it exists;
- proof that no active loader, registry, Source Map, route, or runtime entry
  uses it before cutover;
- cutover criteria;
- deletion, promotion, or rename plan;
- tests or checks that prevent accidental production loading.

Shadow workbenches are execution scaffolding, not a fourth OpenSpec or Stage
truth.

## Self-review

Before Apply uses the Builder Plan, review it for:

- every important OpenSpec outcome has a task and evidence gate;
- no `TBD`, `TODO`, vague "handle edge cases", or "similar to previous task";
- type names, field names, enum values and file paths are consistent;
- each snippet is either contract-grounded or clearly `implementation_sketch`;
- no task can pass while violating a higher-authority OpenSpec contract.
- no external side-effect task can pass while the external target could still
  be empty, stale, missing required schema, or left in a failed/running status.
- no browser/user-visible task can pass with only console output when a
  screenshot, browser trace, video, or report artifact was required.
- no API-route task can pass while the handler exists but the active runtime
  route is unregistered or untested.
- no runtime/stage UI task can pass with stale or unproven stage/substage IDs.
- no evidence task can pass while its claim class, subject ID or explicit
  "not proven" boundaries are missing for workflow/dataflow/trace/status
  claims.
- no foundation-source item can remain only in narrative prose when the plan is
  required to guide Apply. It must map to a task, gate, ledger row, test,
  evidence package, non-goal, accepted override or accepted deferral.
- no structured provider-output task can pass without either a
  `llm-output-contract-inventory.md` row or equivalent explicit row fields; for
  Verify/Review/Archive claims about actual Stage output, fixture-only evidence
  is insufficient.

## Downstream gates

`$openspec-verify-change` must treat a required Builder Plan as a completion
artifact. Missing required plans, incomplete task evidence, untraceable concrete
contract details, or unresolved shadow-workbench cutover/cleanup are archive
blockers.

`$openspec-review` must review the Builder Plan adversarially. The key question
is whether a competent builder following only this plan would deliver the
OpenSpec outcome, or whether the plan is concrete but contract-drifting.

`$openspec-archive-change` must not archive normally while required Builder
Plan work remains incomplete or while Verify/Review reports Builder Plan
CRITICAL issues. A forced archive with known CRITICAL blockers must be explicit
and recorded.
