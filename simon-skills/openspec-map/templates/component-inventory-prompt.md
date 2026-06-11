# Component Inventory Subagent Prompt

You are helping build an `/openspec-map` pre-proposal briefing.

## Assignment

Component:
- `{{COMPONENT_ID}}`

Scope:
- `{{SCOPE_SUMMARY}}`

Path hints:
- `{{PATH_HINTS}}`

Source classes to use:
- `active`
- `architecture`
- `decision`
- `skill_control`
- `specification`
- `reference`
- `archive`
- `prior_art`
- `template`
- `trace`
- `test`
- `research_note`
- `external_doc`
- `unknown`

## Rules

- Read files yourself; do not rely on summary prose when a path is available.
- Do not edit files.
- Do not create OpenSpec proposal artifacts.
- Do not invent paths. If a path is inferred, mark it as an open question.
- Keep active code, archive, reference, and specification sources separate.
- If a CTO Review, Goal Brief, reading contract, Test Review, CEO Review, or
  verification artifact affects this component, preserve its role as a
  skill-network handoff instead of flattening it into generic notes.
- Keep CTO Review blockers and `BD-*` decisions blocking unless the source
  itself says they were accepted or changed.
- Return only the structured report plus brief notes.

## Output

```yaml
component_id: <id>
display_name: <name>
upstream_decision_sources:
  cto_reviews:
    - path: <path>
      spec_mode_status: <pending | clarify_first | proceed_to_spec | dont_build_yet | not_applicable>
      role: <why this review matters>
      blocking_decisions:
        - id: <BD-001>
          status: <open | accepted | rejected | changed>
          must_survive_to_openspec: <true | false>
      stop_rules:
        - <stop rule that must survive>
      evidence_gates:
        - <gate that must survive>
      backchannel_required_after_propose: <true | false>
  goal_or_reading_contracts:
    - path: <path>
      role: <goal.md | pre_proposal_reading_contract | rough_goal>
      mandatory_deep_reads:
        - <path or source set>
      readiness: <ready_for_exploration | ready_for_proposal | draft_only | unknown>
sources:
  - path_or_url: <path or url>
    class: <source class>
    role: <why this source matters>
    size_estimate: <optional>
    read_status: <read | not_read | missing | inaccessible>
target_paths:
  - path: <path>
    action: <create | modify | delete | verify | preserve>
    notes: <optional>
contracts_or_schemas:
  existing:
    - path: <path>
      change_notes: <what changes or must survive>
  new:
    - path: <path>
      purpose: <why it exists>
assets:
  - path: <path>
    type: <prompt | template | config | fixture | trace | example | other>
    role: <why it matters>
tests:
  existing:
    - path: <path>
      purpose: <what it protects>
  new_to_create:
    - path: <path>
      purpose: <what it must prove>
effort_estimate:
  range: <low-high>
  basis: <one sentence>
obsolete_paths:
  - path: <path>
    reason: <why obsolete>
open_questions:
  - <question>
skill_handoffs:
  before_propose:
    - skill: <$cto-review | $goal-brief | $openspec-explore | other>
      reason: <why this must happen before proposal generation>
      required: <true | false>
  during_propose:
    - skill: <$openspec-propose>
      obligation: <what the proposal must preserve or reconcile>
  after_propose:
    - skill: <$goal-brief | CTO Review backchannel | other>
      obligation: <what must happen after artifacts are created>
  later_gates:
    - skill: <$openspec-verify-change | $ceo-review | $test-review | other>
      obligation: <later evidence or readiness gate>
notes: <2-3 lines>
```
