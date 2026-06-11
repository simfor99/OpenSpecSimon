# OpenSpec Clarification Ledger

The Clarification Ledger prevents proposal-time self-deception: it records
assumptions that an AI agent might otherwise resolve silently, but that can
change scope, architecture, evidence, runtime behavior, cost, release readiness
or Simon-owned decisions.

Use it before writing or updating OpenSpec artifacts when the conversation has
become concrete enough to propose, but important meaning still depends on
unstated assumptions.

## Core questions

| Field | Question it answers | Example failure |
|-------|---------------------|-----------------|
| `intended_effect` | What must be true in the real system, not just in a component? | "Admin can save settings" was treated as "runtime consumes settings". |
| `effect_handoff` | Which handoff must carry the effect from source to consumer? | Stored `ai_config` was not proven to reach normal Stage-02 runs. |
| `evidence_class_required` | What evidence class is needed for the claim? | A fixture with `0` candidates proved a boundary, not successful PDF discovery. |
| `release_boundary` | What blocks release/archive and what can be follow-up? | Desktop admin passed while mobile release readiness was undecided. |
| `performance_or_cost_semantics` | Does a limit affect acceptance, parser/runtime work, spend or latency? | `max_pages_per_pdf` was post-extraction, not parser-level stopping. |
| `change_isolation` | Must this change be separable from parallel workspace changes? | A mixed dirty tree made archive/commit truth hard to prove. |
| `unresolved_simon_decisions` | Which choices must Simon make before artifacts are written? | Scope, release, runtime data flow or evidence bar hidden as defaults. |

## Status labels

| Status | Meaning |
|--------|---------|
| `cleared` | Evidence or Simon decision resolved the assumption. |
| `carry_visible` | Safe to propose only if artifacts preserve the assumption and gate it. |
| `clarify_first` | Ask Simon before writing `proposal.md`, `design.md`, specs or tasks. |
| `map_first` | Needs source/target inventory before proposal can be responsible. |
| `cto_first` | Needs risk, stop-rule or architecture framing before proposal. |

## Minimal ledger shape

```yaml
clarification_ledger:
  intended_effect:
    status: cleared | carry_visible | clarify_first | map_first | cto_first
    statement: ""
    evidence_or_question: ""
  effect_handoff:
    status: cleared | carry_visible | clarify_first | map_first | cto_first
    statement: ""
    evidence_or_question: ""
  evidence_class_required:
    status: cleared | carry_visible | clarify_first | map_first | cto_first
    statement: ""
    evidence_or_question: ""
  release_boundary:
    status: cleared | carry_visible | clarify_first | map_first | cto_first
    statement: ""
    evidence_or_question: ""
  unresolved_simon_decisions:
    - decision: ""
      why_simon: ""
      recommended_route: ceo_decision | cto_review | openspec_map | proposal_blocker
```

## Routing rules

If every item is `cleared`, write the proposal normally and cite the source or
decision where relevant.

If an item is `carry_visible`, proposal may continue only if the uncertainty is
preserved in `proposal.md`, `design.md`, specs or `tasks.md` as a requirement,
non-goal, evidence gate or follow-up boundary. Do not phrase it as done.

If any item is `clarify_first`, ask Simon before creating proposal artifacts.
Do not turn it into a conservative default unless an accepted policy already
authorizes that default.

If any item is `map_first`, route to `$openspec-map` before proposal.

If any item is `cto_first`, route to `$cto-review` before proposal.

## Regression prompt

Before finishing Explore or starting Propose, ask:

```text
If Red Review ran after this plan, which DECISION finding would embarrass us?
```

For the PDF inclusion case, this would have surfaced:

- whether persisted Admin settings must affect normal Stage-02 runs;
- whether URSA with `0` candidates proves success or only a boundary;
- whether mobile Admin UX blocks archive;
- whether PDF page budget means acceptance gate or parser runtime stop;
- whether mixed workspace changes are acceptable for archive truth.
