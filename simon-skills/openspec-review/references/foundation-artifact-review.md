# Foundation Artifact Review

Use `foundation_artifact_review` for pre-OpenSpec artifacts that behave like a
mini-spec or target contract, especially Sanctum daily workspace artifacts such
as:

```text
docs/todo/YYYY_MM_DD/03_artifacts/*__artifact__*.md
```

The strongest signal is frontmatter like:

```yaml
kind: artifact
provenance_class: target_contract
status: starter_zielbild
```

This mode reviews whether the artifact is safe to become OpenSpec foundation.
It does not approve implementation, architecture, or archive readiness.

## Mental Model

Sherlock finds reasoning breaks.
OpenSpec Review finds contract breaks.

For a foundation artifact, use both movements:

```text
material system map -> artifact thesis -> contract polarity check ->
OpenSpec handoff risk -> FIX/DECISION report
```

The question is:

```text
Would a reasonable openspec-propose or builder create a wrong spec if it copied
this artifact as-is?
```

## Target Resolution

Select this mode automatically when the target path or content shows all or
most of these signals:

- path under `docs/todo/**/03_artifacts/`;
- filename contains `__artifact__`;
- frontmatter has `kind: artifact`;
- frontmatter has `provenance_class: target_contract`, `proposed_shape`,
  `example_only`, or similar source-polarity markers;
- body claims to be a Zielbild, target contract, mini-spec, operative contract,
  Stage contract, handoff contract, prompt contract, evidence contract, or
  OpenSpec foundation.

If the artifact is only a reflection, meeting note, draft idea, or research
summary without target-contract polarity, route to `sherlock-review` instead.

## Inventory

Read the artifact first, then directly read the artifact's controlling sources:

- `depends_on`, `carry_forward_from`, and inline links;
- referenced architecture docs, stage docs, prompt folders, runtime folders,
  contracts, trace artifacts, test runs, Vault patterns, and business docs;
- existing target OpenSpec change, if named;
- prior artifact chain when `carry_forward_from` is present.

Search snippets are leads. Contract claims need direct source reads.

When the artifact contains concrete prompt text, run the deterministic
foundation prompt extractor in check mode:

```bash
python3 ~/.codex/skills/shared/scripts/extract_prompt_contracts_from_foundation.py \
  --source <artifact-path> \
  --check
```

The check is deliberately template-based rather than keyword-based: it looks
for fenced prompt-file payloads with YAML frontmatter containing `operation_id`
and both `# System Prompt` and `# User Prompt`. It must not depend on GTM,
Stage numbers, English/German heading prose, or file-name patterns.

## Source Polarity Checks

Every important claim must keep its source class visible:

- `current_runtime_evidence`: observed code, prompt, trace, parsed output,
  handoff, run artifact, or test result;
- `target_contract`: desired future contract;
- `proposed_shape`: proposed but not yet accepted shape;
- `example_only`: illustrative example, not observed truth;
- `human_architecture_truth`: explanatory architecture doc;
- `runtime_only`: exists in runtime, not LLM-visible;
- `llm_visible`: actually present in rendered prompt or effective provider
  request;
- `trace_only`: visible in trace/review artifacts, not necessarily model input
  or downstream handoff.

Finding rule:

- Mark `FIX` when wording, labels, links, source class, or evidence boundaries
  can be corrected without changing the intended contract.
- Mark `DECISION` when the source class itself changes scope, architecture,
  public contract, evidence standard, stage boundary, prompt behavior, runtime
  behavior, or Simon-owned strategy.

## Artifact Auditor Lens

Add this lens in addition to the normal OpenSpec Review auditors.

Check:

- Does the artifact clearly state what is target contract versus current
  runtime truth?
- Are `depends_on` and `carry_forward_from` sources actually reflected, or did
  the artifact silently drop a Must-Survive-Fact?
- Are Stage prompt truth, runtime truth, trace truth, app result, and human
  architecture truth kept separate?
- Are proposed JSON shapes, prompt snippets, handoff examples, enum values,
  substage IDs, trace names, and evidence gates labeled as observed truth,
  target contract, proposed shape, or example only?
- Are concrete IDs and names grounded in runtime code, trace artifacts, or
  explicit target contract rather than inherited from old docs?
- Does the artifact define enough Stop-Regeln and evidence gates for a future
  OpenSpec to test the claim?
- Could a builder satisfy the text while losing a Must-Survive-Fact Simon would
  care about?
- Could `$openspec-propose` copy the artifact and create a plausible but wrong
  proposal, design, task list, prompt contract, Builder Plan, or quality gate?
- If concrete prompt text exists, is it mechanically extractable through the
  shared template shape, or would Map/Propose still need to hand-copy and risk
  paraphrase, routing drift or fence-boundary mistakes?

For GTM stages, also use the Stage Authoring Boundary lens from `SKILL.md`.
The Stage Boundary Source Map remains a navigation and evidence index, not a
fourth stage truth.

## Scope Anchor Adaptation

For foundation artifacts, the Scope Anchor changes shape:

- ground truth: what the artifact claims, recommends, labels as target
  contract, labels as current evidence, and expects OpenSpec to mirror;
- source foundation: artifact path, frontmatter source class, carry-forward
  chain, dependencies, inline links, and explicit non-goals;
- allowed paths: artifact, directly linked sources, named target OpenSpec
  folder if present, and directly referenced code/test/doc/prompt/runtime
  paths;
- decision triggers: target contract change, prompt/runtime/handoff boundary,
  Stage truth split, evidence standard, public contract, DB/API/LLM/runtime
  write, or out-of-scope path;
- ground truth verification: which artifact claims were checked against real
  sources and which were assumed.

An empty `assumed_not_verified` list is suspicious. A foundation artifact often
contains future truth, so the report must name what could not yet be proven.

## Report Location

Write a clearly named `openspec-red-review` sidecar next to the artifact:

```text
docs/todo/YYYY_MM_DD/03_artifacts/NNN_slug__openspec-red-review__YYYY_MM_DD__HH-MM.md
```

Use the daily workspace global `NNN_` prefix rule when the repo's AGENTS.md
requires it: scan the whole `docs/todo/YYYY_MM_DD/` tree and use
`max(NNN)+1`.

Use the normal report template and set:

```text
Review-Modus: `foundation_artifact_review`
Gegenstück: pre-OpenSpec target-contract artifact
```

The verdict means:

- `APPROVED`: safe enough as OpenSpec foundation.
- `APPROVED_WITH_NOTES`: usable as foundation with documented caveats or safe
  FIXes.
- `BLOCKED`: do not use as OpenSpec foundation until material breaks are fixed.
- `PAUSED_FOR_DECISION`: Simon must decide at least one DECISION finding before
  the artifact becomes spec input.

## Chat Debrief

Chat debrief is mandatory when there are material findings, any `DECISION`, or
any finding that would change OpenSpec scope, stage boundaries, prompt/runtime
contracts, evidence gates, or Simon-owned product strategy.

Explain the core risk in plain language:

```text
If OpenSpec copied this artifact today, what wrong thing could it build?
```

Then walk Simon through one CEO decision at a time when the finding is
strategic.
