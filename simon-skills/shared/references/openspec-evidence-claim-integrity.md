# OpenSpec Evidence Claim Integrity Contract

Use this reference when an OpenSpec change proves behavior with tests, traces,
database rows, browser evidence, status records, handoffs, logs or reports.

The contract prevents one evidence class from being used to close a stronger or
different claim.

## Core rule

Evidence may only close the claim it directly proves.

A browser submit can prove browser reachability. A database row can prove
persistence. A trace artifact can prove an observed execution record. A status
field can prove the status source recorded that state. None of these
automatically proves workflow success, downstream consumption, trace visibility
or dataflow integrity unless the evidence explicitly covers those claims.

## Claim classes

Use narrow labels in gates, builder tasks and reports:

- `ui_visibility`: the product/browser view shows the expected state.
- `browser_entry`: a user-visible/browser path can be exercised.
- `api_entry`: an API/HTTP entry path accepts and validates a request.
- `persistence_write`: durable external state was written.
- `status_transition`: the selected status source recorded the expected state.
- `workflow_success`: the workflow reached the expected terminal or bounded
  stage state without unexpected failure.
- `bounded_stage_run`: execution respected an explicit start/end/range limit.
- `dataflow_handoff`: a producer output was consumed by the next consumer in
  the expected contract shape.
- `llm_output_contract`: raw and parsed provider/model output, including
  LLM, Search-LLM, Perplexity/agent and tool-call outputs, conforms to the
  output shape requested by the User Prompt or runtime schema.
- `trace_generation`: traces/logs/artifacts were produced by the run.
- `trace_visibility`: traces/logs/artifacts are queryable through the intended
  index/viewer/API.
- `current_run`: evidence belongs to the run/request/workflow under review.
- `historical_match`: evidence comes from a previous comparable run.
- `resume_from_existing`: execution intentionally resumed from an existing
  run/artifact boundary.
- `runtime_config`: required env flags, feature flags, adapters or writers were
  active in the runtime that produced the evidence.

## Non-substitution rules

- `persistence_write` does not prove `workflow_success`.
- `browser_entry` does not prove `persistence_write`, `workflow_success` or
  `trace_visibility`.
- `api_entry` does not prove UI behavior or downstream consumption.
- `trace_generation` on disk or logs does not prove indexed
  `trace_visibility`.
- `historical_match` does not prove the `current_run`, unless the claim is
  explicitly comparison or resume.
- `status_transition` does not prove the real dataflow unless the selected
  status source is the authoritative truth and is cross-checked against the
  produced/consumed artifacts.
- A successful upstream producer does not prove `dataflow_handoff` until the
  downstream consumer accepts the same contract fields.
- Prompt-Request-Parity does not prove `llm_output_contract`; the provider may
  have received the right prompt while returning a structurally invalid,
  provider-envelope-specific or post-processed output.
- `llm_output_contract` does not prove semantic model quality or
  `workflow_success`; it only proves the returned/parsed shape and required
  fields.
- A failed workflow can close a persistence-only or expected-failure test, but
  cannot close `workflow_success` without an explicit expected-failure claim.

## Required claim ledger

For changes with workflow, dataflow, trace, persistence or user-visible entry
claims, include a compact claim ledger in `quality-gates.md`, `builder-plan.md`
or the Verify report:

| Claim | Claim class | Subject ID | Evidence class | Required proof | Not proven |
|---|---|---|---|---|---|

`Subject ID` should be the concrete run, request, workflow, job, trace, row,
artifact or scenario identifier that binds evidence to the claim.

`Not proven` is required when evidence intentionally closes only a narrower
claim. This prevents a useful partial proof from being promoted silently.

## Minimum evidence by claim class

### `workflow_success`

Requires:

- real entry path used;
- run/request/workflow identifier;
- expected start/end/range or terminal condition;
- final status or expected bounded stop from the authoritative runtime/status
  source;
- failure/error fields checked;
- downstream handoff or result evidence when success means later consumption.

### `bounded_stage_run`

Requires:

- explicit start/end/range input;
- proof that the runtime enforced the range, not only recorded it;
- proof no out-of-range stage ran unless the accepted contract allows it;
- visible status when the range is recorded-only or not yet executable.

### `dataflow_handoff`

Requires:

- producer artifact/output identifier;
- consumer input identifier;
- must-survive fields and contract shape;
- validation/cleanup result;
- proof that the consumer used the same values or references;
- explicit failure when legacy or weaker shapes are used unintentionally.

### `llm_output_contract`

Requires:

- exact prompt output contract source or typed schema;
- raw provider/model response or controlled fixture;
- parsed output artifact or parser return value;
- runtime validator/schema proof;
- positive and negative contract tests for required fields, wrong types,
  invalid enums, malformed JSON, null/empty values and unknown fields when
  relevant;
- must-survive fields checked through any post-LLM transformation;
- explicit handling for repair/default behavior so missing model data cannot
  look valid silently.
- when the claim is about a real run rather than parser behavior, run-bound
  evidence for the actual provider route; fixture-only tests close parser
  behavior, not actual provider-output behavior.

### `trace_visibility`

Requires:

- runtime config proof for the trace/log/index writer;
- run/request/workflow identifier;
- generated trace/log/artifact proof;
- indexed/queryable proof through the intended API/table/viewer;
- proof that the visible trace belongs to the current run, historical match or
  resume boundary named in the claim.

### `status_transition`

Requires:

- declared authoritative status source;
- expected statuses and terminal/bounded condition;
- success and error/failure fields;
- reconciliation with trace/artifact/output truth when available;
- explicit explanation when status rows are advisory, pending, stale or not the
  completion truth.

### `current_run`, `historical_match`, `resume_from_existing`

Requires:

- the relationship between the run under review and any reused run/artifact;
- matching keys or fingerprint inputs;
- tie-breaker rules when multiple runs match;
- whether the evidence proves the current run, a comparison baseline or a
  resume source.

## Review questions

Verify and Review must ask:

```text
What exact claim does this evidence close?
Could this evidence be true while the claimed workflow/dataflow/trace/status
behavior is still false?
Is the evidence bound to the current run, or only to a historical/comparable run?
Did the runtime configuration needed for the evidence actually exist in the run?
Did the downstream consumer accept the same handoff contract the producer wrote?
```

If yes or unknown, the claim is incomplete or mislabeled.
