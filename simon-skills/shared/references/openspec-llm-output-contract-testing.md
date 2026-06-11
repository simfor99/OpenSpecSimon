# OpenSpec LLM Output Contract Testing

Use this reference when an OpenSpec change defines, changes or relies on
structured output from an LLM, Search-LLM, Perplexity/agent route, provider
adapter or model tool call: JSON objects, arrays, enums, field names, required
values, nullable fields, output skeletons, parser contracts, typed schemas,
Stage parsed outputs, handoffs, or downstream consumers.

Prompt-Request-Parity proves that the provider received the right instruction.
This contract proves that the provider response, parser, normalizer and runtime
handoff obey the requested output shape.

## Core rule

If the User Prompt tells an LLM, Search-LLM, Perplexity/agent route, provider
adapter or model tool call to return a concrete data shape, the OpenSpec must
require tests that compare the actual returned and parsed data against that
shape.

The required chain is:

```text
User Prompt output contract
-> raw provider/model response
-> provider adapter / response-envelope normalization
-> parsed output artifact
-> runtime validator / typed schema
-> downstream handoff or consumer input
```

Each link needs evidence or an accepted deferral. A prompt containing a JSON
skeleton is not proof that runtime output matches the skeleton.

Fixtures are allowed to prove parser and validator behavior during Apply. They
do not prove that the actual provider operation returned the target shape. For
Verify, Review or Archive claims about real Stage/output behavior, require a
run artifact or accepted equivalent that binds prompt operation id, provider
route/model, raw response, parsed output, validation status and downstream
consumer to the same run/request/workflow.

## Trigger

Activate this contract when any source contains:

- an output JSON skeleton in a User Prompt;
- "return JSON", "output schema", "parsed output", "structured output",
  `response_format`, `generateObject`, Zod/Pydantic/JSON Schema, or typed
  parser references;
- Search-LLM, Perplexity, agent, provider-adapter or tool-call routes that
  return a structured object or normalize a provider response envelope into one;
- GTM Stage prompt contracts with `*_parsed-output.json`, handoff files or
  trace artifacts;
- post-LLM transformation, repair, projection or compatibility logic;
- downstream tasks depending on fields, enums, IDs, citations/source refs,
  references or arrays from provider/model output.

## Required OpenSpec coverage

For each affected LLM/Search-LLM/agent/provider operation, Propose must include
or require:

- prompt operation id and source prompt contract;
- provider route/model source and whether the raw response is a direct model
  message, tool-call result, Perplexity/Search response envelope or normalized
  adapter output;
- expected output contract source: prompt skeleton, typed schema, parser type
  or explicit `target_contract`;
- provider-response normalizer or adapter path when the raw provider shape is
  not already the parsed target object;
- runtime parser and validator path;
- parsed-output trace artifact path or test fixture path;
- downstream consumer or handoff path that uses the parsed data;
- positive contract test: valid representative output passes;
- negative contract tests: missing required field, wrong type, invalid enum,
  unknown extra field when not allowed, malformed JSON and null/empty cases
  fail loud or produce the accepted error shape;
- must-survive assertions for fields that must not be dropped, renamed,
  defaulted or weakened by post-LLM transformation;
- no-default-masking assertion when default values could hide missing LLM
  output.
- for Search-LLM/Perplexity routes, citation/source-ref assertions: source refs
  survive as provenance/evidence when required, do not silently become crawl
  candidates or product truth unless the target contract explicitly says so,
  and provider-internal envelope fields are not mistaken for the business
  output contract.

## Canonical inventory

For multi-operation changes, especially GTM Stage changes, create or require a
dedicated inventory at:

```text
openspec/changes/<change-name>/llm-output-contract-inventory.md
```

This inventory is the row-level bridge between prompt contracts, provider
routes, parsers, fixtures, run artifacts and downstream consumers. It prevents
`tasks.md`, `quality-gates.md` or `builder-plan.md` from saying "test structured
outputs" without naming exactly which operation and return shape is covered.

Each row should include:

- operation id and substep id;
- route class: `standard_llm`, `search_llm`, `perplexity_agent`,
  `provider_adapter`, `tool_call`, or accepted equivalent;
- provider/model source, such as admin-configured, explicit runtime or runtime
  resolved;
- output contract source: User Prompt section, prompt contract, typed schema or
  explicit target contract;
- output object name and required fields/enums;
- extra-field policy and accepted error shape;
- provider envelope/normalizer owner when the raw provider response is not the
  business object;
- parser/validator owner;
- positive and negative fixture paths;
- actual run artifact paths when Verify/Review/Archive claim real Stage output
  conformance;
- downstream handoff or consumer path;
- must-survive fields and "not proven" boundaries.

If a change has only one affected operation, the same fields may live directly
in `quality-gates.md` or `builder-plan.md`; otherwise the inventory is required.

## Quality gate

When active, materialize a gate such as
`llm_output_contract_validation` in `quality-gates.md`.

Recommended gate properties:

```yaml
gate_id: llm_output_contract_validation
title: LLM output matches prompt/runtime contract
evidence_timing: during_apply
severity: CRITICAL
blocks:
  - verify
  - review
  - archive
claim_integrity:
  claim_classes:
    - llm_output_contract
    - dataflow_handoff
  not_proven:
    - model_semantic_quality
    - workflow_success
```

The gate proves structural contract conformance, not that the model made a
good semantic decision.

Gate evidence must separate:

- `fixture_core`: controlled fixtures proving parser, validator, repair and
  negative cases;
- `actual_provider_output`: run-bound evidence proving the actual provider route
  returned, normalized, parsed and validated the target shape;
- `dataflow_handoff`: downstream consumer evidence proving the same values or
  IDs were accepted after parsing/transformation.

Fixture-only evidence cannot close `actual_provider_output` or real Stage
output claims.

## Evidence classes

Accepted evidence:

- `prompt_output_contract`: exact User Prompt section or prompt-contract file
  that defines the output shape.
- `raw_provider_response`: raw model, Search-LLM, Perplexity/agent or provider
  response artifact from a run, or a controlled fixture for parser-only tests.
- `provider_normalization`: adapter/normalizer output or test that turns the
  provider envelope into the parsed business object without dropping required
  fields, citations or error status.
- `parsed_output`: parsed JSON artifact or parser return value.
- `runtime_validator`: schema/type/validator code that accepts/rejects output.
- `contract_test`: deterministic unit/integration test for valid and invalid
  outputs.
- `handoff_consumer`: downstream consumer test proving the same fields are
  accepted after parsing/transformation.

Not sufficient alone:

- prompt text without parser/validator evidence;
- a TypeScript type that is never used at runtime;
- a green model response without negative tests;
- fixture-only tests used as proof that the real provider operation returned the
  target shape;
- parser code without representative parsed artifacts or tests;
- downstream success that does not inspect the same fields;
- default values that silently fill missing model output.

## Anti-loss rules

Post-LLM transformation layers are productive logic. They must not:

- rename fields without a typed contract and tests;
- collapse rich output into a weaker legacy shape;
- drop arrays, IDs, citations, evidence refs, confidence/reason fields or
  rejection reasons without explicit accepted contract;
- treat Perplexity/Search citations, source refs or provider envelope metadata
  as crawl candidates, product facts or prompt truth unless the target contract
  explicitly owns that transformation;
- fill required fields with defaults that make missing LLM data look valid;
- repair malformed output into a successful handoff without recording repair
  status and original failure evidence.

## Apply obligations

Apply must add or update tests near the runtime parser/validator, not only near
the prompt file. For GTM stages, tests should live near the Stage runtime or
pipeline parser that consumes the parsed output.

Do not mark a prompt/runtime task complete until:

1. the expected output contract is sourced from the User Prompt or typed schema;
2. valid and invalid examples are tested;
3. parsed-output artifact shape is checked;
4. downstream handoff or consumer accepts the same fields;
5. must-survive fields are asserted through any post-LLM transformation;
6. provider-specific envelopes and normalizers are tested when the operation is
   Search-LLM, Perplexity, agent-based or tool-call based.

## Verify and Review obligations

Verify must report CRITICAL when a structured provider/model output contract
exists but no runtime contract tests validate the actual parsed output shape.
When the claim is about a real Stage run rather than parser behavior, fixture
tests alone are incomplete evidence.

Review must ask:

```text
Could the prompt be correct and the provider request be correct, while the
parsed output or downstream handoff is still structurally wrong?
Could a Perplexity/Search/provider response envelope be normalized incorrectly
before validation sees the target object?
Could fixture tests pass while the actual provider route returns a different
shape, source-ref convention or error envelope?
Could a post-LLM transformation make a good model answer worse?
Could defaults hide missing model data?
```

If yes or unknown, output contract evidence is incomplete.
