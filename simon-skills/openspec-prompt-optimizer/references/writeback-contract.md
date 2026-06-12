# Deterministic Write-back Contract

## Principle

The final accepted prompt is written back by script, not by manual LLM editing.
The script replaces exactly one complete fenced Prompt-Contract block in the
original Foundation Brief.

## Inputs

```text
--source       original Foundation Brief / Pre-Spec
--operation-id target operation_id
--candidate   approved complete prompt payload or fenced block
--out         output path, usually the same brief path after review
--ledger      write-back ledger path under 05_writeback/
```

## Gates

- `single_block_match`: exactly one source block has the target operation.
- `candidate_operation_match`: candidate frontmatter has the same operation.
- `class_c_not_changed`: route, identity, input blocks, and output objects are
  unchanged unless an explicit contract-change override is used.
- `extract_after_writeback`: the rewritten file can be re-extracted.
- `outside_block_unchanged`: the unified diff shows only the target fenced
  block changed.

## Class C

Class C fields are identity and routing fields:

```text
operation_id
stage_id
substep_id
execution_group
execution_mode
llm_route
llm_provider
llm_model
llm_model_source
input_context_blocks
output_objects
```

If these need to change, the prompt optimizer stops. That is a Simon/OpenSpec
decision, not a prompt-copy improvement.

## Safe Usage

First write to a temporary output path:

```bash
python ~/.codex/skills/shared/scripts/rewrite_prompt_contract_block_in_foundation.py \
  --source foundation.md \
  --operation-id stage-00/00c-product-world-scout \
  --candidate 05_writeback/00c.approved-block.md \
  --out /tmp/foundation.rewritten.md \
  --ledger 05_writeback/00c.writeback-ledger.md
```

Inspect the ledger diff. Only then rerun with `--out foundation.md` when Simon
has approved the write-back.
