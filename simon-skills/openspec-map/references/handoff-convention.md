# Handoff Convention

`/openspec-map` prepares `/openspec-propose`; it does not hard-wire itself into
that skill.

## Principle

Use a lightweight handoff:

```text
$openspec-explore / $cto-review  ->  $openspec-map  ->  $openspec-propose
                                                   ->  $goal-brief when needed
```

The map briefing is a durable input that the user or next agent passes to
`$openspec-propose`. `$openspec-propose` should not globally block when no map
exists, but when a map is provided it must preserve the map's explicit
decision, reading, CTO Review backchannel, Goal Brief, and evidence handoffs.

## Required Final Handoff Section

Every map briefing should end with:

```markdown
## Handoff To `$openspec-propose`

Status: `ready_for_propose` | `not_ready_for_propose`

Primary briefing:
- `<path>`

Required follow-up before propose:
- `<none | list of gaps>`

CTO Review backchannel:
- `<not_applicable | update <cto-review-path> after proposal | create linked addendum>`

Goal Brief / Reading Contract:
- `<not_applicable | create goal.md | use existing reading contract | create reading contract>`

Suggested next prompt:

    $openspec-propose <change-name> using <path> as the primary briefing source.
```

## When To Mention Reading Contracts

If the map depends on many large source files, prompt folders, traces, schemas,
or daily artifacts, recommend that `$openspec-propose` treats the map as a
Pre-Proposal Reading Contract input or creates one before artifact generation.

Do not turn that recommendation into a hard dependency unless the source set is
too large or fragile to trust from the map alone.

## When To Mention CTO Review

If the map read a CTO Review, list it under `source_cto_reviews` and state
whether `$openspec-propose` must update the memo or create a linked addendum
after proposal generation. This keeps the CTO Review as the decision/history
artifact while OpenSpec becomes the technical execution truth.

If the map itself discovers new CTO-relevant facts, do not wait for
`$openspec-propose`. Update the source CTO Review immediately or create a
linked addendum, then record `map_backchannel_status` as `updated` or
`addendum_created`. Examples of CTO-relevant facts: concrete source/target
paths that change the architecture assumption, a new evidence gate, a missing
test layer, a scope split, or a blocker that moved from abstract risk to
verified inventory fact.

If the CTO Review has unresolved `BD-*` decisions or a blocking
`spec_mode_status`, keep `propose_readiness.status: not_ready_for_propose`
unless Simon already resolved those decisions. A map may clarify a blocker, but
it must not downgrade the blocker into a note.

If no CTO Review exists but the map reveals broad architecture risk, unclear
rollback, LLM/pipeline dataflow risk, production side effects, or evidence
gates Simon should decide, add `$cto-review` as a recommended or required
handoff before `$openspec-propose`.
