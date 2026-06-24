# OpenSpec Ziel-Weg-Fitness

Ziel-Weg-Fitness prevents operational blindness before OpenSpec tasks become
execution truth. It asks whether the chosen solution path is the right and
smallest sufficient path to reach Simon's goal without damaging quality.

Use it for any non-trivial OpenSpec planning, not only prompt work.

Core question:

```text
What do we want to achieve, and is this the best path to get there?
```

For scope that involves new processes, pipelines, agents, optimization,
acceleration or automation, also read
`/home/simon/.codex/skills/shared/references/openspec-elons-principles-order-of-operations.md`.
That guard makes the order explicit: requirement -> delete -> simplify ->
accelerate -> automate.

## When it applies

Always run a compact check before proposal handoff. Expand it when the change:

- touches prompts, schemas, runtime logic, UI, dataflows, traces, migrations,
  cleanup, routing, automation, business logic, tests, or docs that control
  downstream behavior;
- introduces a larger mechanism than the goal visibly requires;
- relies on an LLM-sounding assumption that has not been empirically proven;
- could be solved by multiple plausible paths;
- carries cost, latency, quality, maintainability, complexity, or recall risk.

For tiny typo, formatting, or obvious one-file fixes, record `minimal_path_ok`
briefly and continue.

## Minimal shape

```yaml
ziel_weg_fitness:
  goal_plain_language: ""
  selected_path: ""
  minimum_sufficient_path: ""
  cut_candidates:
    - ""
  order_of_operations:
    requirement_checked: true|false
    deleted_or_avoided:
      - ""
    simplified_before_speed_or_automation: true|false|not_applicable
    automation_stance: not_needed|deferred|planned_with_reason
  quality_must_not_drop:
    - ""
  plausible_alternatives:
    - id: A
      path: ""
      why_considered: ""
      tradeoff: ""
  path_verdict: fit | overbuilt | underbuilt | unclear | needs_ab_test | needs_cto | needs_ceo
  ab_test_recommendation:
    status: required | recommended | not_needed
    why: ""
    route: "$ab-test-lab <experiment goal>"
  task_bridge:
    - "Exact task/evidence that proves the chosen path reaches the goal"
```

## The cut question

Before writing tasks, ask:

```text
What can we remove while still achieving the goal and preserving quality?
```

Cut candidates may be:

- data the model/user/system does not need;
- generic context that belongs in trace, not in decision input;
- UI flows that do not serve the primary workflow;
- migrations or refactors not required for the target behavior;
- abstractions that do not remove real complexity;
- tests that duplicate proof without covering a new risk;
- docs that claim behavior instead of proving it.

Do not cut:

- Must-Survive-Facts;
- evidence needed to prove the goal;
- user-visible quality;
- recall, safety, correctness, or rollback paths;
- required downstream consumer contracts.

## A/B routing rule

Prefer A/B testing when the path choice depends on empirical behavior. In
practice, assume A/B is worth proposing for most LLM, prompt, schema, crawler,
ranking, filtering, UX, quality, heuristic, or pipeline-path choices unless the
better path is obvious from source truth or accepted policy.

Use:

- `required` when promotion would otherwise rely on a plausible but unproven
  assumption;
- `recommended` when A/B could materially reduce risk, cost, or debate;
- `not_needed` only when the path is mechanically forced, trivially reversible,
  or already proven by equivalent evidence.

If `required` or `recommended`, OpenSpec artifacts must include:

- the A/B question in plain language;
- A and B mechanisms;
- Must-Survive and Must-Reject;
- primary quality signal and guardrails;
- required trace/evidence;
- a handoff to `$ab-test-lab` before promotion or archive when relevant.

## Verdict rules

- `fit`: selected path is proportionate and evidence-backed.
- `overbuilt`: path carries unnecessary complexity, data, cost, surface area, or
  indirection. Cut before proposal or carry as a DECISION.
- `underbuilt`: path cannot actually reach the goal or protect quality.
- `unclear`: ask Simon, map first, or run a micro-spike.
- `needs_ab_test`: path may be right, but empirical comparison should decide.
- `needs_cto`: architecture, risk, rollback, or evidence gates need CTO Review.
- `needs_ceo`: product, scope, quality bar, cost, or tradeoff belongs to Simon.

Do not convert `needs_ab_test`, `needs_cto`, or `needs_ceo` into implementation
defaults. Carry them visibly into proposal, tasks, goal, verification, and Red
Review.

## Relationship to other OpenSpec gates

- Clarification Ledger asks: Which assumptions must not be hidden?
- Ziel-Weg-Fitness asks: Is this solution path actually the right way?
- Elons Principles asks: Did we check the requirement, delete, and simplify
  before accelerating or automating?
- Nordstern-to-Task Bridge asks: Did the chosen path become clear tasks and
  evidence?
- OpenSpec Map asks: Which sources and target paths control correctness?
- A/B Test Lab asks: Which path wins empirically?
- Red Review asks: Did the final result remain sane enough to trust?
