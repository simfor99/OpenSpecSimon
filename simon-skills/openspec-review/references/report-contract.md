# Report Contract

Write the report to:

```text
<change-dir>/00-OPENSPEC-RED-REVIEW.md
```

For `foundation-cto-review` and `foundation_artifact_review`, write a clearly
named `openspec-red-review` sidecar next to the source document instead.

## Required Sections

1. `## 0. Zusammenfassung für Simon`
2. `## 1. Abschlussentscheidung, die dieser Review vorbereitet`
3. `## 2. Was behauptet wurde`
4. `## 3. Was Red geprüft hat`
5. `## 4. Systemverständnis und Must-Survive-Facts`
6. `## 5. Übersehene Komplexität und falsche Annahmen`
7. `## 6. Findings`
8. `## 7. Evidence Reality Check`
9. `## 8. Stop-Regeln`
10. `## 9. Zurückzuschreiben nach`
11. `## 10. Vault-Learnings`

The summary must state whether the Chat Debrief is `pending`, `in_progress`, or
`discussed`. If findings are still unresolved, the report must not imply that
Simon has accepted the review outcome.

## Required System Map Content

Section 4 must include:

- checked subsystems or an explicit narrow-scope reason;
- at least one `Must-Survive-Fact` entry or `none found` with reason;
- a Coverage Gate status: `yes`, `partial`, or `no`;
- unchecked gaps that could change the verdict, or `none found` with evidence basis.
- Ziel-Weg-Fitness when the source artifacts mention it, alternative paths,
  minimum sufficient path, or `$ab-test-lab`.

Plain `APPROVED` is not valid when Coverage Gate is `partial` or `no`.

If Section 4 includes Ziel-Weg-Fitness, it must include an A/B status:
`required`, `recommended`, `not_needed`, or `bypassed`.

## Required Verdict

One of:

- `APPROVED`
- `APPROVED_WITH_NOTES`
- `BLOCKED`
- `PAUSED_FOR_DECISION`

## Finding Format

Each finding needs:

- title;
- `Klasse: FIX | DECISION`;
- `Status`;
- `Severity`;
- `Evidence`;
- what was found;
- why Verify could miss it;
- what was fixed, if FIX.

DECISION findings also need:

- why it is DECISION;
- at least two options;
- Red recommendation;
- explicit "not changed" statement.

## Chat Contract

Do not treat a completed markdown report as the end of the skill when material
findings exist. The report should support the chat, not replace it.

If Simon resolves, rejects, reframes, or adds context to a finding in chat,
update the report before final handoff so the artifact reflects the discussed
state.
