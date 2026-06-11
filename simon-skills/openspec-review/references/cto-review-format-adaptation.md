# CTO Review Format Adaptation

Use the CTO Review memo style, not the CTO Review status vocabulary.

When a target is recognizably a CTO Review memo, use
`foundation-cto-review` automatically. Do not require a special flag and do not
ask Simon which mode to use.

The review must challenge the memo's reasoning, not merely list its open
questions. Open `BD-*` entries are evidence inputs; they are not the whole
review.

For CTO Review foundation targets, the Chat Debrief is mandatory. The reviewer
must walk Simon through any logic break, evidence jump, or dangerous OpenSpec
handoff risk in chat, because the purpose is to repair the foundation before it
becomes spec truth.

## Keep

- CEO-readable summary;
- decision prepared by the review;
- Hidden Complexity;
- Blocking Decisions;
- Stop rules;
- Evidence and Gate contract;
- write-back targets;
- recommendation versus Simon decision separation.

## Replace

- `spec_mode_status` -> OpenSpec Red Review verdict;
- `PROCEED_TO_SPEC` -> `APPROVED`;
- `CLARIFY_FIRST` -> `PAUSED_FOR_DECISION`;
- `DONT_BUILD_YET` -> `BLOCKED`;
- OpenSpec skeleton -> "Zurückzuschreiben nach".

## Mental Model

CTO Review is an input gate.
OpenSpec Red Review is an output gate.

Foundation Red Review sits between them:

```text
CTO Review -> Foundation Red Review -> OpenSpec Proposal/Execution
```
