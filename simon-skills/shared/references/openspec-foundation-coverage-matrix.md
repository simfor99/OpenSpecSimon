# OpenSpec Foundation Coverage Matrix

Use this reference when an OpenSpec proposal, map, review or goal is based on
a concrete foundation source such as a Foundation Brief, CTO Review, OpenSpec
Map, Goal Brief, target-contract artifact, prompt-contract folder, Test Review
or user-supplied planning document.

The coverage matrix closes the gap between "the source says it" and "the
OpenSpec chain will actually build, test and verify it".

## Required trigger

Create or require a coverage matrix when any of these exists:

- `proposal.md` contains a `## Source foundation` block.
- A Foundation Brief with `binding_status: pre_spec_zielbild` is used.
- An OpenSpec Map has `propose_readiness.status: ready_for_propose` or
  `quality_gate_status`, `builder_plan_status`, `implementation_ledger_status`
  or `prompt_contracts_status` other than `not_required`/`none`.
- A CTO Review, Goal Brief, Test Review or source artifact has explicit
  `must_check`, `Must-Survive-Facts`, Stop-Regeln, Evidence Gates,
  prompt-contracts, runtime contract targets, accepted decisions, non-goals or
  backchannel obligations.

For narrow changes without a concrete foundation source, record
`foundation_coverage_status: not_applicable`.

## Coverage rule

Each foundation item must land in the correct OpenSpec artifact type. A mention
in `proposal.md` alone is not coverage.

| Foundation item type | Must be represented as |
|---|---|
| target behavior or contract | spec requirement/scenario and task |
| non-goal or scope exclusion | proposal/design non-goal and, when risky, a guard task or gate |
| Must-Survive-Fact | spec scenario, task and evidence/quality gate |
| prompt contract | OpenSpec-local `prompt-contracts/`, productive prompt target, prompt-fidelity gate and request-parity evidence |
| structured LLM/Search-LLM/Perplexity/provider output contract | spec/task, `llm-output-contract-inventory.md` for multi-operation changes, provider normalizer when applicable, runtime parser or schema, output-contract quality gate, positive/negative fixture tests, actual run-artifact requirements for real Stage-output claims and downstream handoff check |
| runtime contract target | spec requirement, runtime task, test target and ledger row |
| external side effect | quality gate with same-target write-read proof, builder-plan entry path and ledger row |
| evidence claim boundary | quality gate with claim class, subject ID and explicit `not_proven` boundaries |
| accepted decision/default | proposal/design record and task/gate if it changes execution |
| open or risky decision | `clarify_first`, `cto_first`, `ceo_first` or explicit accepted deferral |
| A/B recommendation | task and gate or `not_applicable_with_reason` before promotion/archive |
| backchannel obligation | task, ledger row or explicit writeback target |

## Matrix shape

The matrix may live in `proposal.md`, `design.md`, `builder-plan.md`, or a
dedicated section of the map. For broad changes, prefer `builder-plan.md` plus
`quality-gates.md` and `implementation-ledger.md`.

Use this compact shape:

```markdown
## Foundation coverage matrix

| Source item | Source locator | Artifact coverage | Status | Gap handling |
|---|---|---|---|---|
| <item> | <path#heading or line> | <spec/task/gate/ledger/builder/prompt-contract refs> | covered | <none> |
| <item> | <path#heading or line> | <refs or missing> | missing | <fix before apply / clarify_first / non_goal / accepted_deferral> |
```

Allowed statuses:

- `covered`
- `non_goal_with_reason`
- `accepted_override`
- `deferred_with_accepted_decision`
- `clarify_first`
- `missing`

`missing` and `clarify_first` block using the OpenSpec as an Apply basis.

## Propose obligations

`$openspec-propose` must perform this pass before finalizing artifacts:

1. Extract the source foundation's `must_check` list, Must-Survive-Facts,
   quality-gate candidates, prompt contracts, runtime target contracts,
   accepted decisions, open decisions and non-goals.
2. For every item, write the correct artifact coverage or mark the item as
   non-goal, accepted override, accepted deferral or blocker.
3. If any item needs `quality-gates.md`, `implementation-ledger.md` or
   `builder-plan.md`, materialize those artifacts now when source detail is
   sufficient; otherwise add a blocking pre-Apply task that must create them.
4. Do not treat broad "follow the foundation" wording as coverage.

## Map obligations

`$openspec-map` must seed the matrix by listing concrete source items and their
target artifact types. It should not execute gates or write proposal artifacts,
but it must tell `$openspec-propose` which items need specs, tasks, gates,
ledger rows, builder-plan tasks, prompt-contract sidecars, tests or follow-up
decisions.

## Review obligations

`$openspec-review` must challenge the matrix:

- If no matrix exists while the trigger applies, record a material finding.
- If a foundation item is only mentioned in prose, record it as uncovered.
- If coverage lands in the wrong artifact type, record the exact missing
  artifact type.
- If the user asked for skill-chain or meta-process improvement, do not patch
  the target OpenSpec as the default fix. Extract the pattern, update the
  relevant skill/reference contract, and report whether the target OpenSpec is
  still locally unfixed.

## Apply and Verify obligations

`$openspec-apply-change` must read the matrix or the artifacts derived from it
before editing. `$openspec-verify-change` must treat uncovered required
foundation items as completion blockers unless the item is explicitly
`non_goal_with_reason`, `accepted_override` or
`deferred_with_accepted_decision`.
