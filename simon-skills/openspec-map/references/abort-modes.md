# Abort Modes

Stop or mark the map `not_ready_for_propose` instead of producing a misleading
briefing in these cases.

## Missing Scope

Condition: the component list, wave, module set, or target change cannot be
inferred.

Action: ask one concise question. If still unresolved, stop.

## Source Truth Conflict

Condition: active code, architecture docs, decisions, or archive sources
contradict each other on a central point.

Action: record the conflict and set `not_ready_for_propose` unless an explicit
decision source resolves it.

## Unread Mandatory Sources

Condition: the briefing would depend on central files that cannot be opened or
were not actually read by the main agent or subagents.

Action: list those paths in `required_followup_before_propose`.

## Target Shape Unknown

Condition: source inventory is clear, but target paths or target contracts are
still unknown.

Action: produce a partial map only if useful, but mark it
`not_ready_for_propose`.

## Unresolved CTO Review Gate

Condition: a source CTO Review has `spec_mode_status: pending`,
`clarify_first`, or `dont_build_yet`, or contains open `BD-*` decisions that
control proposal scope, architecture path, governance, production risk, or
evidence gates.

Action: preserve the CTO Review path and blockers in the map, set
`not_ready_for_propose`, and route to Simon/`$cto-review` unless the relevant
decision was already accepted elsewhere. Do not downgrade the blocker into a
watch item.

## Execution Request

Condition: the user asks to implement, verify, archive, or approve during a map
run.

Action: finish or pause the map, then route to the appropriate skill:
`$openspec-propose`, `$goal-brief`, `$openspec-apply-change`,
`$openspec-verify-change`, `$openspec-archive-change`, or `$ceo-review`.
