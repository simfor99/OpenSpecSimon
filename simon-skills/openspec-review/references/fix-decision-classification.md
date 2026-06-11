# FIX/DECISION Classification

Every finding is classified before action.

## FIX

Use `FIX` only when all are true:

- inside `scope.allowed_paths`;
- preserves ground truth;
- does not change public contract;
- does not sync specs;
- does not apply migrations or external writes;
- does not alter architecture, product scope, cost, or governance;
- Simon would not need to choose between real tradeoffs.

Examples:

- typo in report;
- missing link to existing evidence;
- stale status line;
- failed placeholder cleanup;
- small test assertion correction when behavior is unchanged.

## DECISION

Use `DECISION` when any is true:

- outside allowed paths;
- changes architecture or public contract;
- changes specs or syncs specs;
- requires DB/API/LLM/live-system write;
- resolves an open CEO decision;
- downgrades blocker polarity;
- trades off performance, cost, scope, or launch readiness;
- evidence contradicts external reality.

When uncertain, classify as `DECISION`.

DECISION findings must be brought into the Chat Debrief. Do not leave Simon to
discover them only inside the report.
