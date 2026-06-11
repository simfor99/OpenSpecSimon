# OpenSpec Subagent Policy

This policy applies to the OpenSpec skill chain when subagents are available or
explicitly authorized by the current Codex/Claude runtime.

## Core principle

Subagents are an isolation and parallelism tool, not a correctness gate.

Use them to reduce context pressure, inspect independent source surfaces, or
challenge a conclusion. Do not use them to outsource ownership of the critical
OpenSpec path.

The main agent always owns:

- canonical artifact creation and final edits;
- final FIX/DECISION classification;
- validator execution and interpretation;
- prompt-contract extraction handoff;
- archive readiness and user-facing verdicts;
- final handoff to the next skill.

Subagent output is evidence to verify, not source of truth.

## Safe uses by skill

| Skill | Good subagent uses | Must stay main-agent owned |
|---|---|---|
| Explore | read-only source scouts, prior-art/context inventory | Simon conversation, decision tree, Foundation Brief |
| Map | read-only component/source inventory, evidence tracing | final map, `propose_readiness`, prompt-contract sidecars, validators |
| Propose | pre-artifact coverage audit, source-foundation audit, gate completeness audit | `proposal.md`, `design.md`, specs, tasks, local meta-artifacts |
| Review | bounded auditor lenses, adversarial evidence checks, assumption challenges | verdict, FIX/DECISION list, final report, safe-FIX approval |
| Apply | disjoint implementation slices with explicit file ownership and tests | shared contracts, prompt text, schemas, task completion verdict |
| Verify | independent evidence-surface audits | verification verdict, scorecard, archive-readiness classification |
| Archive | usually none; at most read-only hygiene checks | archive decision, move operation, spec sync choice, Rückkanal entry |
| Goal Brief | source inventory for large inputs | route decision, stop condition, runnable goal, `goal.md` |

## Hard boundaries

- Prefer parallel file/tool reads before subagents when that is enough.
- Do not delegate canonical artifact creation on the critical path unless the
  artifact has a single owner, a bounded write set, a deterministic validator,
  and a clear recovery path.
- Prompt-contract sidecars are generated or checked by deterministic scripts
  when the source template supports extraction. Subagents may point to source
  blocks; they do not author prompt contracts from memory.
- Subagents must read referenced files themselves. Do not paste file contents as
  a literal payload when a path is available.
- Subagents must return structured reports with paths, source classes,
  unresolved questions, and evidence gaps.
- If a subagent times out, hangs, or returns partial output twice in one
  workflow, stop delegating for that workflow and continue locally or block
  with the exact reason.
- External second opinions in `$openspec-review` are separate from internal
  subagents; treat their reports as sidecar evidence and verify claims before
  acting on them.

## Delegation prompt minimum

A subagent assignment must include:

- exact component or question;
- allowed paths or path hints;
- required output schema;
- read-only versus bounded-write mode;
- explicit exclusions;
- expected evidence paths;
- instruction to report blockers instead of guessing.

The main agent must re-open the cited files or run the cited validators before
using a subagent report in a final artifact or verdict.
