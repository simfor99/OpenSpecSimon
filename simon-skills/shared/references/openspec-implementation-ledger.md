# OpenSpec Implementation Ledger

Use an OpenSpec-local implementation ledger when a change is broad enough that
tasks alone can hide missed files, folders, prompts, contracts, tests, traces,
docs, or review gates.

Canonical path:

```text
openspec/changes/<change-name>/implementation-ledger.md
```

## When Required

Create or require the ledger for OpenSpec work involving any of these:

- broad documentation cleanup, migration, deprecation, folder moves, or archive
  separation;
- three or more components, folders, stages, prompts, schemas, test surfaces,
  trace surfaces, or docs clusters;
- explicit "review every file", "every folder", "all sections", "all prompts",
  "all first-level directories", or similar complete-scope requirements;
- source maps, implementation maps, component inventories, or CTO/CEO review
  evidence gates;
- large `tasks.md` files where grouped tasks could hide skipped files;
- `goal.md` requirements for complete evidence, Section sync, link checks,
  prompt contracts, trace review, or documentation refresh.

Do not force a ledger for narrow one-file or two-file fixes unless Simon asks
for one or the existing artifacts require it.

## Required Rows

A ledger must include every concrete thing that must be inspected or changed:

- components and folders;
- individual files;
- prompt-contract files and productive prompt files;
- LLM/Search-LLM/Perplexity/agent/provider output contracts, the canonical
  `llm-output-contract-inventory.md` when required, provider normalizers,
  parser/validator files, parsed-output fixtures, actual run artifacts,
  post-LLM transformation files and downstream consumer tests;
- specs, schemas, migrations, traces, fixtures, eval sets and test files when
  they are in scope;
- concrete source-foundation coverage targets: each Foundation Brief, CTO
  Review, Goal Brief, OpenSpec Map or target-contract item that creates a
  required spec, task, quality gate, builder-plan task, prompt-contract,
  productive prompt, runtime contract, test, evidence package or backchannel;
- architecture Sections and central docs;
- external or symlinked source targets when a map includes them;
- verification, review, backchannel, documentation and archive-readiness gates.

For file-heavy work, do not stop at folder rows. Add individual file rows when
the user, map, goal, CTO review, proposal or evidence gate says each file must
be reviewed.

## Recommended Columns

Use Markdown checkboxes so the file is easy to scan and easy for agents to
maintain:

| Done | Target | Source class | Required action | Template / contract | Status | Evidence / note |
|---|---|---|---|---|---|---|
| [ ] | `path/or/component` | `source_truth` | inspect/update/move/delete/keep | template or contract | `todo` | concrete evidence |

Allowed final statuses:

- `updated`
- `moved`
- `deleted`
- `created`
- `reviewed_unaffected`
- `not_impacted`
- `deferred_with_reason`
- `blocked`

`todo` is never an archive-ready state.

## Evidence Rules

Each row needs evidence before the related OpenSpec task can be checked:

- source files read;
- current truth source such as code, prompt, trace, schema, map, CTO review or
  runtime evidence;
- actual changed path or no-change reason;
- test, link check, content check, trace review or verification result when
  relevant.

`reviewed_unaffected` must still explain why no change was needed. It is not a
shortcut for "not read".

## Skill Responsibilities

`$openspec-map`

- inventories candidate ledger targets;
- identifies when a ledger is required or recommended;
- lists component, file, prompt, test, trace and doc rows that `$openspec-propose`
  should materialize.
- seeds ledger rows from the Foundation Coverage Matrix when a concrete source
  foundation controls the change.

`$openspec-propose`

- creates `implementation-ledger.md` when the ledger is required and enough
  source inventory exists;
- otherwise adds an explicit task requiring the ledger before Apply;
- links the ledger from `proposal.md`, `design.md`, `tasks.md`, and `goal.md`
  when present.
- must not leave concrete foundation obligations only in `proposal.md` prose
  when a ledger is present or required. Add rows for the artifacts that prove
  coverage: specs, prompt-contracts, productive prompt targets, runtime entry
  contracts, LLM output-contract inventory, parser/validator targets,
  provider-envelope/normalizer targets, parsed-output fixtures/artifacts,
  actual provider-output run artifacts, downstream consumer tests, migrations,
  Evidence Lab/Test Review packages, review reports and backchannels.

`$openspec-apply-change`

- reads and maintains the ledger before editing;
- marks rows as final only with evidence;
- refuses to mark related tasks done while required ledger rows are `todo`,
  missing, or evidence-free.

`$openspec-verify-change`

- treats the ledger as a verification artifact;
- reports CRITICAL when required rows are missing, still `todo`, contradictory,
  or lack evidence;
- checks that file-heavy scope includes file rows, not only parent folders.

`$openspec-review`

- challenges whether the ledger itself is sane;
- looks for skipped targets, alibi statuses, weak evidence, bad scope cuts,
  missing files, and "reviewed_unaffected" without real source reading.

## Completion Rule

The ledger is not complete until every required row has a final status and
evidence. A change may have all `tasks.md` boxes checked and still be blocked
when its ledger is incomplete.
