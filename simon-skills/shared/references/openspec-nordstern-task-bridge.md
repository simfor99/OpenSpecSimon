# OpenSpec Nordstern-to-Task Bridge

The Nordstern-to-Task Bridge prevents intent loss between a human goal and
OpenSpec tasks. It forces the proposal writer to prove that each important
human-language outcome has a concrete task and a concrete evidence gate.

Use it after the Clarification Ledger and before writing or finalizing
`proposal.md`, `design.md`, specs and `tasks.md`.

## Why this exists

Detailed tasks can still miss the user's intent. A task can say "move or
redirect", "rename or retitle", "mark or archive" and still be checked off even
when the user's real goal was physical movement, folder merge, hard deletion or
runtime wiring.

The bridge makes the translation explicit:

```text
Human Nordstern -> required system state -> task -> evidence gate
```

If any link is weak, the proposal is not ready.

## Bridge fields

| Field | Meaning |
|-------|---------|
| `nordstern_statement` | The user's goal in simple human language. |
| `must_survive_fact` | The part that must not be softened during artifact generation. |
| `target_system_state` | What must be true in files, runtime, docs, tests, UI, data or workflow after apply. |
| `physical_or_runtime_change` | Whether the change requires real file movement, rename, deletion, wiring, persistence-to-runtime handoff, loader update, import update or user-visible behavior. |
| `allowed_alternatives` | Alternatives Simon explicitly accepted. Empty means no silent alternative. |
| `forbidden_interpretations` | Plausible shortcuts that would satisfy wording but violate intent. |
| `task_binding` | Exact `tasks.md` task IDs that implement the target state. |
| `evidence_gate` | Exact command, file existence check, test, grep, screenshot, trace or review proof that confirms the target state. |

## Minimal shape

```yaml
nordstern_task_bridge:
  - id: N1
    nordstern_statement: ""
    must_survive_fact: ""
    target_system_state: ""
    physical_or_runtime_change: ""
    allowed_alternatives: []
    forbidden_interpretations: []
    task_binding: []
    evidence_gate: []
    status: clear | needs_clarification | blocked
```

## Ambiguity markers

Treat task wording as ambiguous when it uses alternatives without a recorded
Simon decision:

```text
or, maybe, if useful, where needed, where appropriate, can, may,
move or mark, move or redirect, rename or retitle, archive or deprecate,
equivalent path chosen by implementer, follow-up if needed
```

Ambiguous wording is allowed only when the bridge records:

- which alternatives Simon accepted;
- what evidence proves each alternative;
- which alternatives are forbidden.

Otherwise, ask Simon before finalizing artifacts.

## Mandatory checks

For every `must_survive_fact`, ask:

1. Can a builder check off the task without making this fact true?
2. Can a verifier pass the change by reading documentation while the physical or runtime state is still wrong?
3. Does the task require a real action or only a claim/source-map/doc update?
4. Is the evidence gate strong enough to distinguish "implemented" from "wired and used"?
5. If this is a folder/path goal, does the gate check actual filesystem state?

If any answer exposes a gap, revise the task before proposal completion.

## Boundary-cleanup regression example

If Simon's Nordstern is "Stage `02c` must be folded under Stage `02`", do not
write only:

```text
Move or redirect active Stage-02c documentation into Stage-02 docs root.
```

That can be checked off by leaving a sibling redirect folder. Instead record:

```yaml
nordstern_statement: "Stage 02c is no longer a sibling stage."
target_system_state: "No active sibling Stage-02c folder remains; any retained sibling folder is explicitly redirect/prior-art and not active."
allowed_alternatives:
  - "Physical removal/rename"
  - "Temporary redirect folder, only if Simon accepts it and evidence proves it is non-active"
forbidden_interpretations:
  - "Leaving an active-looking sibling docs folder because source-map text says it is not active"
evidence_gate:
  - "find docs/architecture/stages -maxdepth 1 -name '*stage-02c*'"
  - "README/status of any retained folder says redirect/prior-art"
  - "active stages README points to Stage-02-owned path"
```

This is the trust mechanism: the task cannot pass unless the Nordstern has a
specific proof path.
