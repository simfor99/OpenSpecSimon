---
type: openspec-map-briefing
phase: pre-propose
date: "{{ISO_DATETIME}}"
target_change: "{{CHANGE_NAME}}"
prepared_by: "{{PREPARED_BY}}"
decision_owner: "{{DECISION_OWNER}}"
status: "{{READY_STATUS}}"
---

# {{TITLE}}

> Pfad: `{{REPO_RELATIVE_PATH}}`

## Purpose

{{PURPOSE}}

## Scope

{{SCOPE}}

## Upstream Decision Sources

{{UPSTREAM_DECISION_SOURCES_OR_NONE}}

## Source Classes

{{SOURCE_CLASS_SUMMARY}}

## Prompt Contracts

{{PROMPT_CONTRACTS_OR_NOT_APPLICABLE}}

## Builder Plan Seed

**Status:** `{{BUILDER_PLAN_STATUS}}`

{{BUILDER_PLAN_SEED_OR_NOT_APPLICABLE}}

## External Side-Effect Reality

**Status:** `{{EXTERNAL_SIDE_EFFECT_REALITY_STATUS}}`

{{EXTERNAL_SIDE_EFFECT_REALITY_OR_NOT_APPLICABLE}}

## Component Map

{{COMPONENT_SECTIONS}}

## Cross-Component Findings

{{CROSS_COMPONENT_FINDINGS}}

## Wave Aggregation

{{WAVE_AGGREGATION_OR_NONE}}

## Open Questions And Blockers

{{OPEN_QUESTIONS_AND_BLOCKERS}}

## Skill Network Handoff

### Before `$openspec-propose`

{{BEFORE_PROPOSE_HANDOFFS_OR_NONE}}

### During `$openspec-propose`

{{DURING_PROPOSE_OBLIGATIONS_OR_NONE}}

### After `$openspec-propose`

{{AFTER_PROPOSE_OBLIGATIONS_OR_NONE}}

### Later Gates

{{LATER_GATES_OR_NONE}}

## CTO Review Map Backchannel

**Status:** `{{CTO_MAP_BACKCHANNEL_STATUS}}`

**Source CTO Reviews:**

{{SOURCE_CTO_REVIEWS_MARKDOWN}}

**New CTO-Relevant Findings:**

{{NEW_CTO_RELEVANT_FINDINGS_OR_NONE}}

**Backchannel Action:**

{{CTO_MAP_BACKCHANNEL_ACTION}}

## Propose Readiness

```yaml
propose_readiness:
  status: {{READY_STATUS}}
  target_change: {{CHANGE_NAME}}
  change_name_suggestion: {{CHANGE_NAME}}
  primary_briefing_path: {{REPO_RELATIVE_PATH}}
  foundation_brief_status: {{FOUNDATION_BRIEF_STATUS}}
  source_cto_reviews:
{{SOURCE_CTO_REVIEWS_YAML}}
  source_red_reviews:
{{SOURCE_RED_REVIEWS_YAML}}
  map_backchannel_status: {{CTO_MAP_BACKCHANNEL_STATUS}}
  cto_review_backchannel_required: {{CTO_REVIEW_BACKCHANNEL_REQUIRED}}
  goal_brief_recommended: {{GOAL_BRIEF_RECOMMENDED}}
  pre_proposal_reading_contract_required: {{PRE_PROPOSAL_READING_CONTRACT_REQUIRED}}
  prompt_contracts_required: {{PROMPT_CONTRACTS_REQUIRED}}
  prompt_contracts_status: {{PROMPT_CONTRACTS_STATUS}}
  prompt_contract_extraction_gate:
    status: {{PROMPT_CONTRACT_EXTRACTION_GATE_STATUS}}
    command: "{{PROMPT_CONTRACT_EXTRACTION_GATE_COMMAND}}"
    checked_at: "{{PROMPT_CONTRACT_EXTRACTION_GATE_CHECKED_AT}}"
  prompt_contract_files:
{{PROMPT_CONTRACT_FILES_YAML}}
  quality_gate_status: {{QUALITY_GATE_STATUS}}
  implementation_ledger_status: {{IMPLEMENTATION_LEDGER_STATUS}}
  builder_plan_status: {{BUILDER_PLAN_STATUS}}
  builder_plan_required_before_apply: {{BUILDER_PLAN_REQUIRED_BEFORE_APPLY}}
  builder_plan_seed_summary: "{{BUILDER_PLAN_SEED_SUMMARY}}"
  external_side_effect_reality_status: {{EXTERNAL_SIDE_EFFECT_REALITY_STATUS}}
  external_side_effect_gate_required: {{EXTERNAL_SIDE_EFFECT_GATE_REQUIRED}}
  external_side_effect_summary: "{{EXTERNAL_SIDE_EFFECT_SUMMARY}}"
  required_followup_before_propose:
{{REQUIRED_FOLLOWUP_YAML}}
  suggested_next_prompt: "{{SUGGESTED_NEXT_PROMPT}}"
```

## Handoff To `$openspec-propose`

Status: `{{READY_STATUS}}`

Primary briefing:
- `{{REPO_RELATIVE_PATH}}`

Required follow-up before propose:
{{REQUIRED_FOLLOWUP_MARKDOWN}}

CTO Review backchannel:
- {{CTO_REVIEW_BACKCHANNEL_HANDOFF}}

Goal Brief / Reading Contract:
- {{GOAL_OR_READING_CONTRACT_HANDOFF}}

Prompt Contracts:
- {{PROMPT_CONTRACT_HANDOFF}}

Builder Plan:
- {{BUILDER_PLAN_HANDOFF}}

External Side-Effect Reality:
- {{EXTERNAL_SIDE_EFFECT_HANDOFF}}

Suggested next prompt:

```text
{{SUGGESTED_NEXT_PROMPT}}
```
