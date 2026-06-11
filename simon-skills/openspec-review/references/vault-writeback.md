# Vault Write-Back

Write Vault notes only after the report exists.

## What To Write

Up to 5 reusable learnings:

- recurring review self-deception;
- wrong evidence class;
- implementation pattern Verify cannot catch;
- runtime, trace, or spec drift pattern;
- useful auditor heuristic.

## What Not To Write

- raw findings;
- task lists;
- one-off trivia;
- change-specific details without reusable pattern;
- notes without evidence.

## Quality Gate

Each note needs:

- speaking title;
- 2+ sentences of context;
- evidence or numbers;
- exact source path;
- type: `pattern` or `finding`;
- tags including `source/openspec-review`.

Use `distill_vault_learnings.py` to prepare candidates, then write with the Second Brain vault writer when available.

