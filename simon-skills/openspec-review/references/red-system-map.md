# Red System Map

Build the Red System Map after the Scope Anchor and before auditor judgment.
It is the OpenSpec Review version of Sherlock's "system map before verdict"
rule: no confident criticism without material understanding.

The map is not a long inventory and not a second OpenSpec Map. It is a compact
explanation of the system that the reviewed change claims to have made true.
It also asks whether the chosen solution path was fit for the goal or whether
the team became operationally blind to a smaller, better, or empirically safer
path.

## When to build it

Always build a compact map. Expand it when the change touches:

- runtime folders, loaders, imports, stage packets, prompts, schemas, traces, or
  handoffs;
- downstream consumers such as later stages, UI, reports, docs, tests, archive
  workflows, or human operators;
- historical cleanup, rename, merge, deletion, migration, or boundary work;
- a Verify claim that depends on evidence outside the OpenSpec folder.

For a narrow docs-only change, the map may be only a short table. For stage,
pipeline, prompt, contract, or archive changes, the map must name the concrete
subsystems that can carry or break the claim.

## Map shape

Use this shape in the review notes and summarize it in the report:

```markdown
| Subsystem | What Red Checked | Why It Matters | Must-Survive-Facts | Coverage |
|---|---|---|---|---|
```

Then add:

```markdown
### Must-Survive-Facts
- `<fact>` — where it must remain true and which later task, test, consumer, or
  artifact must prove it.

### Coverage Gate
- Checked:
- Not checked:
- Gaps that could change the verdict:
- Is the map enough for Red Review? yes/no/partial
```

Also summarize Ziel-Weg-Fitness when relevant:

```markdown
### Ziel-Weg-Fitness
- Goal:
- Selected path:
- Minimum sufficient path:
- Cut candidates missed:
- A/B status: required/recommended/not_needed/bypassed
```

## Must-Survive-Facts

A Must-Survive-Fact is a fact that Simon's human-language goal would consider
essential even if a task checklist could be checked without it.

Common examples:

- a folder was actually merged, renamed, deleted, or rewired;
- a prompt-visible field reaches the model, not only a runtime object;
- a runtime-only trace field is not described as LLM input;
- a stronger output shape is not flattened by a post-LLM adapter;
- a downstream stage, UI, report, or archive workflow reads the new contract;
- a Verify report proves the same evidence class that the OpenSpec claims.

If a Must-Survive-Fact has no task binding or evidence path, create a finding.
If fixing it would change scope, contract, architecture, public behavior, or
archive truth, classify it as `DECISION`.

## Coverage gate

Before final verdict, answer:

| Question | Required answer |
|---|---|
| Which subsystems were checked? | concrete paths, artifacts, commands, or traces |
| Which thesis-critical subsystem was not checked? | say `none found` only after search/direct reads |
| Which Must-Survive-Facts are visible? | bullet list or table |
| Which gaps could change the verdict? | list gaps or `none found` with evidence basis |
| Is coverage enough for Red Review? | `yes`, `partial`, or `no` |
| Was the selected path fit for the goal? | `fit`, `overbuilt`, `underbuilt`, `unclear`, or `needs_ab_test` |

Verdict rule:

- `yes`: normal verdict allowed.
- `partial`: `APPROVED_WITH_NOTES`, `BLOCKED`, or `PAUSED_FOR_DECISION`; never
  plain `APPROVED`.
- `no`: `BLOCKED` or `PAUSED_FOR_DECISION`.

## Source discipline

Search snippets are leads, not evidence. Central claims need direct source
reads, command output, trace artifacts, or user-provided material.

Prefer:

1. OpenSpec artifacts and Verify reports;
2. referenced implementation, docs, tests, prompts, schemas, traces, and
   archive artifacts;
3. `repo_search` or `vault_search` for historic patterns and related material;
4. direct `rg`, `sed`, `jq`, `git show`, and command output for verification.

## What not to do

- Do not turn the map into a file dump.
- Do not invent symmetrical alternatives when the material does not create a
  real choice.
- Do not use the map to approve architecture. Route architecture choices to
  `cto-review` or Simon.
- Do not hide an unchecked critical subsystem inside a positive verdict.
- Do not accept a plausible-sounding path when the artifact required or
  strongly recommended empirical comparison through `$ab-test-lab`.
