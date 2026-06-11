# OpenSpec Map Output Schema

Use this schema for every component in an `/openspec-map` briefing. Leave
fields empty only when they truly do not apply. Do not invent paths.

## Component Schema

```yaml
component_id: <stable id>
display_name: <human-readable name>

upstream_decision_sources:
  cto_reviews:
    - path: <path>
      spec_mode_status: <pending | clarify_first | proceed_to_spec | dont_build_yet | not_applicable>
      role: <why this review matters>
      blocking_decisions:
        - id: <BD-001>
          status: <open | accepted | rejected | changed>
          must_survive_to_openspec: <true | false>
      stop_rules:
        - <stop rule that must survive>
      evidence_gates:
        - <gate that must survive>
      backchannel_required_after_propose: <true | false>
  goal_or_reading_contracts:
    - path: <path>
      role: <goal.md | pre_proposal_reading_contract | rough_goal>
      mandatory_deep_reads:
        - <path or source set>
      readiness: <ready_for_exploration | ready_for_proposal | draft_only | unknown>

sources:
  - path_or_url: <path or url>
    class: <source class>
    role: <why this source matters>
    size_estimate: <optional>
    read_status: <read | not_read | missing | inaccessible>

target_paths:
  - path: <path>
    action: <create | modify | delete | verify | preserve>
    notes: <optional>

contracts_or_schemas:
  existing:
    - path: <path>
      change_notes: <what changes or what must survive>
  new:
    - path: <path>
      purpose: <why it exists>

prompt_contracts:
  required: <true | false>
  status: <not_applicable | created | required_missing | blocked>
  files:
    - path: <path>
      contract_kind: <target_contract | proposed_shape | example_only | current_runtime_evidence>
      source_path: <path>
      source_locator: <heading, section, or line range>
      extraction_mode: <verbatim | structural_copy>
      downstream_obligation: <what propose/apply must do with it>
  quality_gate:
    completeness_check: <how to prove full prompt transfer>
    no_hallucination_check: <how to prove nothing was invented>
    example_boundary_check: <how examples are separated from target contracts>

builder_plan_seed:
  status: <not_required | recommended | required | present | blocked>
  reason: <why this classification fits>
  existing_patterns:
    - path: <path>
      role: <helper API, similar implementation, local test style, etc.>
  candidate_tasks:
    - openspec_task: <task id or text>
      target_files:
        - <path>
      test_files:
        - <path>
      command: <exact command when known>
      evidence_gate: <what proves this task is done>
  contract_risks:
    - <where a concrete plan could invent field names, shapes, examples, fallbacks, or hidden bridges>
  shadow_workbench:
    status: <not_applicable | proposed | present | blocked>
    path: <path when applicable>
    active_loader_exclusion: <how to prove it is not active before cutover>
    cutover_or_cleanup: <promotion, deletion, or rename obligation>

external_side_effect_reality:
  status: <not_applicable | candidates | required | blocked>
  target_systems:
    - system: <supabase | postgres | storage | queue | webhook | auth | billing | email | external_api | other>
      environment_class: <local | remote | staging | production | unknown>
      mutation_claim: <what durable state is expected to change>
      entry_path: <highest product/user/API entry path that causes it>
      run_identifiers:
        - <workflow_id | request_id | run_id | trace_id | other>
      expected_records:
        - target: <table/bucket/queue/message/external record>
          key_fields:
            - <field>
          required_assertions:
            - <field/status/error assertion>
      downstream_consumer: <stage/service/user path that must reload or reference it>
      required_evidence_class: <production_fresh_intake_database | write_read_probe | accepted_deferral | other>
      cleanup_or_retention: <delete test data | retain as evidence | not_applicable | unknown>
  entry_point_matrix_required: <true | false>
  quality_gate_obligation: <gate id suggestion or not_applicable>
  blockers:
    - <missing environment, unsafe write, missing credentials, unknown cleanup, etc.>

assets:
  - path: <path>
    type: <prompt | template | config | fixture | trace | example | other>
    role: <why it matters>

tests:
  existing:
    - path: <path>
      purpose: <what it already protects>
  new_to_create:
    - path: <path>
      purpose: <what it must prove>

effort_estimate:
  range: <low-high in the project's normal unit>
  basis: <why this range is plausible>

obsolete_paths:
  - path: <path>
    reason: <why it becomes obsolete>

open_questions:
  - <question>

skill_handoffs:
  before_propose:
    - skill: <$cto-review | $goal-brief | $openspec-explore | other>
      reason: <why this must happen before proposal generation>
      required: <true | false>
  during_propose:
    - skill: <$openspec-propose>
      obligation: <what the proposal must preserve or reconcile>
  after_propose:
    - skill: <$goal-brief | CTO Review backchannel | other>
      obligation: <what must happen after artifacts are created>
  later_gates:
    - skill: <$openspec-verify-change | $ceo-review | $test-review | other>
      obligation: <later evidence or readiness gate>

notes: <2-3 lines of hidden complexity or dependency context>
```

## Wave Aggregation Schema

Use only when the scope has multiple waves or batches.

```yaml
wave_id: <id>
components: [<component_id>]
total_effort_range: <low-high>
preparation_audits:
  - <audit to run before propose or apply>
acceptance_criteria_seed:
  - <criterion that should appear in proposal/design/tasks>
cross_component_concerns:
  - <shared schema, asset, dependency, sequencing, or cleanup issue>
```

## Propose Readiness Schema

Every map briefing must include exactly one readiness block.

```yaml
propose_readiness:
  status: <ready_for_propose | not_ready_for_propose>
  target_change: <kebab-case name>
  change_name_suggestion: <kebab-case name>
  primary_briefing_path: <path>
  foundation_brief_status: <not_applicable | used | validated | created_guided | declined_by_decision>
  source_cto_reviews:
    - <path>
  source_red_reviews:
    - <path>
  map_backchannel_status: <not_applicable | no_update_needed | updated | addendum_created | blocked>
  cto_review_backchannel_required: <true | false>
  goal_brief_recommended: <true | false>
  pre_proposal_reading_contract_required: <true | false>
  prompt_contracts_required: <true | false>
  prompt_contracts_status: <not_applicable | created | required_missing | blocked>
  prompt_contract_extraction_gate:
    status: <passed | failed | not_applicable>
    command: <command used, or not_applicable>
    checked_at: <ISO-8601 with timezone, or not_applicable>
  prompt_contract_files:
    - <path>
  quality_gate_status: <none | candidates | clarify_first | map_first | ready_for_propose>
  implementation_ledger_status: <not_required | recommended | required | present | blocked>
  builder_plan_status: <not_required | recommended | required | present | blocked>
  builder_plan_required_before_apply: <true | false>
  builder_plan_seed_summary: <one-line summary or not_applicable>
  external_side_effect_reality_status: <not_applicable | candidates | required | blocked>
  external_side_effect_gate_required: <true | false>
  external_side_effect_summary: <one-line summary or not_applicable>
  required_followup_before_propose:
    - <missing source, decision, or read obligation>
  suggested_next_prompt: <one-line prompt for /openspec-propose>
```

`ready_for_propose` means proposal generation can start with this briefing as
the primary source. It does not mean implementation is ready, verified, or
approved.

`not_ready_for_propose` means the map is still useful, but the next step is to
resolve the listed gaps before creating proposal artifacts.

When `prompt_contracts_required: true`, `ready_for_propose` is only valid if
`prompt_contracts_status: created` and every prompt contract file is listed
under `prompt_contract_files`.

Use real empty lists (`[]`) or omit optional lists when empty. Do not use
sentinel list entries such as `- none`, because downstream skills and
validators cannot distinguish them from real paths without special casing.
