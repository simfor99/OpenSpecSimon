# OpenSpec Elons Principles order-of-operations guard

Use this reference when an OpenSpec workflow could otherwise turn a plausible
solution shape into proposal, tasks, implementation, verification, or archive
truth before checking whether the requirement or process step should exist.

The name is a mnemonic from Elon Musk's five-step engineering algorithm, not an
authority claim. In OpenSpec, the guard operationalizes the same question as
Ziel-Weg-Fitness: choose the smallest good path that reaches Simon's goal
without damaging quality.

Apply the sequence in this order:

1. Make the requirement less dumb.
2. Delete a part or process step.
3. Simplify or optimize.
4. Accelerate cycle time.
5. Automate.

## Trigger

Apply this guard when OpenSpec work includes any of:

- ambiguous, expandable, or solution-shaped scope;
- new workflow, process, stage, pipeline, prompt chain, agent, abstraction, or
  reusable mechanism;
- optimization, speed, throughput, orchestration, parallelization, or
  automation;
- broad tasks that support each other more than the user-visible outcome;
- a change created from a Foundation Brief, OpenSpec Map, CTO Review, Goal
  Brief, or chat thread that may contain inherited assumptions;
- archive or completion claims where the implemented path seems larger than the
  accepted goal.

Do not use it for trivial mechanical fixes where the target behavior is already
settled and the change has no meaningful carrying cost.

## Core rule

Do not skip forward in the sequence:

| Step | OpenSpec question | Bad shortcut it prevents |
|---|---|---|
| Requirement | Is this Simon's actual goal, or an inherited solution assumption? | Turning a bad premise into a clean OpenSpec. |
| Delete | Which requirement, task, field, prompt step, agent, gate, or process step can disappear? | Planning or verifying unnecessary machinery. |
| Simplify | Can the kept path become smaller, clearer, or more direct? | Preserving accidental architecture. |
| Accelerate | Is the remaining loop stable enough to make faster? | Speeding up churn or rework. |
| Automate | Is the remaining process understood, repeatable, and worth carrying? | Automating a brittle workaround. |

If a later step looks attractive, first state why the earlier steps are already
satisfied or not applicable.

## Skill behavior

### `openspec-explore`

Use this as an exploration and proposal-readiness guard:

- pressure-test the user's requested shape against the real goal;
- surface smaller or deletion-oriented alternatives before recommending
  proposal, map, CTO Review, Goal Brief, or automation;
- carry unresolved requirement or scope questions into the Clarification Ledger;
- do not route to proposal just because the solution shape sounds concrete when
  the requirement is still unclear.

### `openspec-propose`

Use this as an artifact-subtraction guard:

- before writing artifacts, prove the selected path is not overbuilt;
- make cut candidates explicit in Ziel-Weg-Fitness, non-goals, deferred scope,
  quality gates, or tasks;
- remove or defer tasks, work slices, gates, ledgers, agents, abstractions, and
  automation that do not serve the accepted goal;
- do not delete Must-Survive-Facts, evidence obligations, safety, correctness,
  accessibility, rollback, or downstream consumer contracts;
- preserve traceability when deleting scope: a deliberate cut is recorded, not
  silently dropped.

### `openspec-apply-change`

Use this lightly during implementation:

- execute the accepted OpenSpec path; do not reopen product scope just because a
  smaller idea appears during coding;
- pause when implementation reveals that a task mainly supports avoidable
  complexity or premature automation;
- prefer the simplest implementation that satisfies specs, gates, goal.md,
  builder-plan rows, and evidence obligations;
- do not add scripts, agents, broad parallelism, or automation beyond the
  OpenSpec unless the process is stable and the artifact contract supports it.

### `openspec-verify-change`

Use this as a sanity check inside Ziel-Weg Fitness:

- verify that required cuts, non-goals, and deferrals were preserved;
- flag overbuilt implementation, extra automation, or unapproved process
  machinery when it changes carrying cost, risk, or archive readiness;
- do not treat "more complete than requested" as automatically better.

### `openspec-review`

Use this as a Team-Red lens:

- challenge whether the contract itself professionalized the wrong thing;
- classify premature automation, unnecessary abstraction, or hidden scope growth
  as a finding when it affects trust, cost, maintainability, or evidence.

## Output expectations

When this guard materially changes an OpenSpec stance or artifact, make the
result visible:

```text
OpenSpec Elons Principles Guard: applied
Requirement check: <kept/reframed/deferred>
Deleted or avoided: <requirement/task/process/automation, or none with reason>
Simplified before speed/automation: <yes/no/not_applicable>
Automation stance: <not_needed/deferred/planned_with_reason>
Artifact location: <proposal/design/tasks/goal/gate/review section>
```

For lightweight work, a one-line note in Ziel-Weg-Fitness or the final handoff
is enough. For broad or risky work, fold the result into proposal scope,
design rationale, task slicing, quality gates, builder-plan rows, verify
findings, or review findings.

## Non-goals

- This guard does not override safety, security, evidence, compliance,
  accessibility, rollback, or Simon-owned decisions.
- Deleting scope is not the same as dropping accepted behavior silently.
- Simplicity is not anti-quality: diagnostics, tests, observability and
  evidence gates are good when their value is clear.
- Automation is not bad. Premature automation is the failure mode.
