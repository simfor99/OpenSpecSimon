# Auditor Contracts

Each auditor writes findings with evidence. Auditors are skeptical but bounded.

## Universal Rules

- No finding without evidence.
- Distinguish `claim`, `formal_status`, `runtime_evidence`, and `source_truth`.
- Do not repeat `$openspec-verify-change` as a final judgment.
- Mark uncertainty honestly.
- Read the Red System Map when present and challenge any missing
  Must-Survive-Fact in your owned lens.
- Do not fix anything unless assigned as a FIX implementer.

## Assumption Auditor

OWNS:

- ground assumptions;
- `goal.md`, `proposal.md`, `design.md` defaults;
- hidden CEO decisions;
- assumed-not-verified items.

EXCLUDES:

- line-by-line code style;
- task checkbox counting as final judgment.

## Implementation Sense Auditor

OWNS:

- whether the solution is proportional and in the right layer;
- unnecessary complexity;
- Ziel-Weg-Fitness: whether the selected path was the smallest sufficient path
  to reach the goal without quality loss;
- missed or bypassed `$ab-test-lab` when empirical comparison should decide;
- wrong abstraction;
- hidden coupling.

EXCLUDES:

- formal spec completeness;
- Vault writeback.

## Evidence Skeptic

OWNS:

- claim versus evidence;
- runtime evidence;
- trace quality;
- `CODE_PASS` versus `RUNTIME_VALIDATED`.

EXCLUDES:

- proposing architecture alternatives unless evidence reveals a decision.

## Spec Drift Auditor

OWNS:

- delta specs versus main spec truth;
- scenario drift;
- public contract drift;
- downstream handoff drift.

EXCLUDES:

- test implementation detail except when tied to scenario coverage.

## Test Reality Auditor

OWNS:

- whether tests prove the named risk;
- mock/fixture circularity;
- missing edge cases;
- stale or skipped tests.

EXCLUDES:

- broad security review unless tests claim security coverage.

## Archive Hygiene Auditor

OWNS:

- archive or active folder health;
- `verification.md` / `verification-report.md` claims;
- open blockers;
- polarity drift;
- prior Red Review presence.

EXCLUDES:

- proposing runtime fixes.

## Foundation Logic Auditor

Use only for `foundation-cto-review`.

OWNS:

- logical breaks inside a CTO Review memo;
- open decisions versus `spec_mode_status`;
- recommendation versus accepted Simon decision;
- evidence anchors that do not support the memo claim;
- proposed shape versus observed runtime evidence;
- Stop-Regeln and Evidence Gates that are too vague to survive OpenSpec;
- whether `$openspec-propose` would create a bad spec by copying the memo as-is.

EXCLUDES:

- rewriting the CTO Review as a new architecture memo;
- accepting CEO decisions for Simon;
- implementing the proposed OpenSpec change.

## Foundation Artifact Auditor

Use only for `foundation_artifact_review`.

OWNS:

- source-polarity mistakes inside pre-OpenSpec target-contract artifacts;
- `current_runtime_evidence`, `target_contract`, `proposed_shape`, and
  `example_only` separation;
- carry-forward and `depends_on` completeness;
- Must-Survive-Facts that could be lost before OpenSpec;
- prompt truth, runtime truth, trace truth, app-result truth, and human
  architecture truth separation;
- whether `$openspec-propose` would create a bad spec by copying the artifact
  as-is.

EXCLUDES:

- approving architecture for Simon;
- replacing Sherlock for broad idea exploration without contract polarity;
- implementing runtime behavior;
- turning the artifact into a full OpenSpec proposal.

## Team-Red Synthesis

OWNS:

- de-duplication;
- whether the Red System Map coverage is enough for the final verdict;
- Must-Survive-Facts that were not bound to tasks, evidence, or consumers;
- severity;
- FIX/DECISION classification;
- final verdict;
- report writing;
- handoff;
- vault learning candidates.
