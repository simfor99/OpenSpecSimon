# Boundary To `$openspec-verify-change`

`$openspec-verify-change` is the formal verifier.
`openspec-review` is the paranoid second pass.

## Formal Verifier Questions

- Are tasks complete?
- Are requirements and scenarios covered?
- Is Goal Evidence present?
- Was Contract Polarity preserved?
- Is the change ready to archive?

## Paranoid Review Questions

- Were the ground assumptions correct?
- Did the implementation solve the right problem?
- Was a green test confused with runtime truth?
- Did a report present a claim as evidence?
- Was an open decision softened into a default?
- Is the solution sensible, maintainable, and proportional?
- Which blind spots remain even when Verify is green?

## Recommended Chain

```text
openspec-apply-change
-> openspec-verify-change
-> openspec-review
-> Simon decision for DECISION findings
-> openspec-archive-change
```

Post-archive review is allowed, but the skill must not move archive folders or silently reopen changes.

Early mode is allowed:

```text
openspec-review --early-paranoia
```

That is a challenge pass, not Archive Readiness.

## Non-Overlap Rules

Do not repeat as final judgment:

- task-checkbox counting;
- OpenSpec status;
- generic requirement keyword search;
- "ready for archive".

Read the same artifacts to ask different questions: evidence quality, assumptions, semantic drift, implementation sense, and review self-deception.

