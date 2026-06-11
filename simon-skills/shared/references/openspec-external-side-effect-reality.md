# OpenSpec External Side-Effect Reality Contract

Use this reference when an OpenSpec change claims that a real external system is
mutated or must contain new state after a workflow run.

## Core rule

If a requirement, task, gate, design note or user request says a change writes,
persists, upserts, inserts, updates, deletes, enqueues, sends, bills, authenticates
or stores something outside the local process, the change needs an explicit
External Side-Effect Reality Gate.

Local migrations, generated types, unit tests, trace artifacts, fixture replay,
browser submit success and API responses are useful partial evidence. They do
not prove the external side effect by themselves.

## Common triggers

- Supabase, Postgres, database, DB, storage, bucket, queue or webhook writes
- Auth, billing, email, notification or external API mutations
- Workflow/status changes that must be visible in a persisted table
- Trace indexing in a remote table
- Any promise that "production fresh intake" or a product entry path writes
  durable state

## Required gate shape

The concrete `quality-gates.md` gate must name:

- target system and environment class, such as `local_supabase`,
  `remote_supabase`, `staging`, or `production`;
- entry path used to cause the side effect;
- run/workflow/request identifiers produced by the entry path;
- exact tables, rows, buckets, queues, messages or external records expected;
- minimum field assertions, including null/error/status fields;
- write-read verification command, query, report or evidence package;
- cleanup or retention stance when the run writes durable test data;
- accepted deferral path when the external write cannot be safely executed.

## Database write-read minimum

For database persistence, a passing gate must include all of:

- a real run through the highest applicable entry path, not only a direct lower
  level module call;
- proof the target schema has the required columns or objects in the same
  database that the run uses;
- proof the run produced durable rows in the expected table or tables;
- proof expected fields are present and populated, including new columns;
- proof status/error columns show success, not only that the request returned;
- proof the downstream consumer can address the persisted rows by the promised
  key or reference.

## Evidence classes

Use narrow evidence labels instead of one broad success label:

- `production_fresh_intake_browser`
- `production_fresh_intake_api`
- `production_fresh_intake_trace`
- `production_fresh_intake_database`
- `artifact_replay`
- `fixture_core`

A gate that claims database persistence needs `*_database` evidence or an
explicit accepted deferral. Browser, API and trace evidence may support it, but
they do not replace it.

## Entry-point matrix

For pipeline, workflow or stage changes, record a compact matrix before closing
the gate:

| Entry point | New runtime path | New adapter/writer | Trace writes | External write |
|---|---:|---:|---:|---:|

The highest user/product entry path in scope must be checked. A lower-level
runner test is not enough when the product entry path wires adapters,
environment flags, credentials or workflow status separately.

## Fail-loud write rule

Every productive external mutation in the changed path must check and surface
write errors. Silent mutation failures block Verify/Review/Archive when the
change claims external persistence or status transitions.

## Review question

For every side-effect gate, Verify and Review must ask:

```text
Could the external target still be empty, stale, missing a column, or in a
failed/running status if all listed evidence were true?
```

If yes, the gate evidence is incomplete.
