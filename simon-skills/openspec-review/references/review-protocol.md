# Review Protocol

## Modes

- `post-verify`: recommended default after `$openspec-verify-change`.
- `post-archive`: audit an archived change.
- `early-paranoia`: challenge assumptions before formal Verify.
- `foundation-cto-review`: automatically selected when the target is
  recognizably a CTO Review memo; audits the memo before OpenSpec relies on it
  as planning foundation.
- `foundation_artifact_review`: automatically selected when the target is a
  pre-OpenSpec target-contract artifact or mini-spec; audits the artifact
  before OpenSpec relies on it as planning foundation.
- `prompt-only`: generate a Team-Red prompt instead of executing the review.

## Workflow

1. Resolve target.
2. Inventory artifacts. For CTO Review targets, inventory the memo, linked
   evidence, `BD-*`, Stop-Regeln, Evidence Gates, `target_openspec_change`, and
   OpenSpec-Rückkanal instead of treating the memo as a change directory. For
   foundation artifact targets, inventory the artifact, frontmatter,
   `carry_forward_from`, `depends_on`, inline links, source-polarity labels,
   Must-Survive-Facts, and named OpenSpec/stage/runtime/prompt targets.
3. Run pre-scan. For CTO Review targets, pre-scan means reasoning-risk scan,
   not OpenSpec task/verify hygiene.
4. Build Scope Anchor.
5. Build Red System Map.
6. Launch auditors.
7. Consolidate findings.
8. Classify as FIX or DECISION.
9. Apply safe FIX findings only.
10. Write the Red Review report. For CTO Review and foundation artifact
    targets, write a clearly named sidecar next to the source document instead
    of treating it as an OpenSpec folder.
11. Validate the report.
12. Run the Chat Debrief with Simon.
13. If chat resolves, challenges, or changes a finding, update and revalidate
    the report.
14. Distill Vault learnings.
15. Produce final chat summary and handoff.

## Chat Debrief

The report is a reference artifact. The review outcome must still be actively
discussed in chat whenever the review found relevant issues, uncertainties,
`DECISION` items, `BLOCKED`, or `PAUSED_FOR_DECISION`.

Required chat behavior:

- explain the core finding in plain language before citing the report;
- lead with the highest-severity issue, not with the report path;
- turn `DECISION` findings into concrete options and a Red recommendation;
- let Simon challenge or refine the reasoning;
- update the report when the chat changes the outcome;
- handle multiple real decisions one at a time.

Do not bury important findings in the markdown file and leave Simon to read
them alone.

## Review Lenses

- assumption correctness;
- implementation sense;
- evidence reality;
- spec drift;
- test reality;
- archive hygiene;
- contract polarity;
- proportionality;
- downstream truth;
- system understanding and Must-Survive-Facts.
- foundation logic for CTO Review targets: decision polarity, evidence jumps,
  open decisions versus `spec_mode_status`, proposed-shape labeling, and
  OpenSpec write-back completeness.
- foundation artifact logic for target-contract artifacts: source polarity,
  carry-forward completeness, linked-source coverage, Must-Survive-Facts,
  Stage truth split, and OpenSpec handoff safety.

## Verdicts

- `APPROVED`: no relevant blind spots remain.
- `APPROVED_WITH_NOTES`: usable with minor FIXes or non-blocking notes.
- `BLOCKED`: do not archive or use as a foundation until fixed.
- `PAUSED_FOR_DECISION`: Simon must decide at least one DECISION finding.

For `foundation-cto-review`, `APPROVED` means the memo is safe enough as
OpenSpec foundation. It does not mean the architecture is implemented,
promoted, or accepted by Simon.

For `foundation_artifact_review`, `APPROVED` means the artifact is safe enough
as OpenSpec foundation. It does not mean the target contract is implemented,
runtime-validated, or accepted as architecture by Simon.
