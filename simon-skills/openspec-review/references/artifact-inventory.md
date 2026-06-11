# Artifact Inventory

The inventory is a map of claims and evidence, not a verdict.

## Standard Files

Look for:

- `.openspec.yaml`
- `proposal.md`
- `design.md`
- `goal.md`
- `tasks.md`
- `specs/**/spec.md`
- `verification.md`
- `verification-report.md`
- `00-OPENSPEC-VERIFY.md`
- `00-OPENSPEC-VERIFY-REPORT.md`
- `00-OPENSPEC-RED-REVIEW.md`

For CTO Review targets, look for:

- the source CTO Review memo;
- frontmatter fields such as `spec_mode_status`, `default_decisions_accepted`,
  `target_openspec_change`, `decision_owner`, and `scope`;
- `BD-*` Blocking Decisions;
- `HC-*` Hidden Complexity;
- Stop-Regeln;
- Evidence- und Gate-Vertrag;
- `Zurückzuschreiben nach`;
- `OpenSpec-Rückkanal`;
- the linked target OpenSpec folder, if it already exists.

## Evidence-Like Files

Also collect:

- `implementation-evidence.md`
- `source-target-map.md`
- `source-audit.md`
- `parity-report.md`
- `verification-report.md`
- `verification.md`
- `00-OPENSPEC-VERIFY.md`
- `00-OPENSPEC-VERIFY-REPORT.md`
- `cleanup-carry-forward.md`
- `matrix-evidence.md`
- `*_review*.md`
- `*_report*.md`
- `*_evidence*.md`
- trace or output paths named by the reports

## Evidence Classes

- `formal_status`: OpenSpec status, tasks, validation output.
- `contract`: specs, goal, design, proposal, decisions.
- `claim`: reports, summaries, completion statements.
- `runtime_evidence`: traces, DB/API/LLM/browser evidence, command output.
- `source_truth`: actual code, tests, docs, schemas.
- `review_truth`: Verify report and Red Review report.
- `foundation_truth`: CTO Review memo claims, recommendations, open decisions,
  and OpenSpec handoff expectations.

The reviewer must not treat `claim` as `runtime_evidence`.
The reviewer must not treat `foundation_truth` as accepted CEO decision or
runtime evidence unless a linked artifact proves that status.
