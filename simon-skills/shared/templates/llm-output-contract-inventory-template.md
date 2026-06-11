# <Change name> LLM Output Contract Inventory

> Pfad: `openspec/changes/<change-name>/llm-output-contract-inventory.md`

## Zweck

Dieses Inventar verbindet Prompt-Rückgabeform, Provider-Route, rohe Antwort,
Normalisierung, Parser/Validator, Fixtures, echte Run-Artefakte und downstream
Consumer. Es ist kein Prompt-Vertrag und keine vierte Stage-Wahrheit.

## Inventar

| Operation | Route class | Provider/model source | Output contract source | Output object | Required fields/enums | Extra-field policy | Error shape | Envelope/normalizer | Parser/validator | Positive fixtures | Negative fixtures | Actual run artifacts | Downstream consumer | Must-survive fields | Not proven |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `<operation_id>` | `<standard_llm/search_llm/perplexity_agent/provider_adapter/tool_call>` | `<admin_configured/explicit_runtime/runtime_resolved/...>` | `<prompt-contract path + locator>` | `<object>` | `<fields/enums>` | `<reject/allow/strip>` | `<fail_loud/error object>` | `<path or not_applicable>` | `<path>` | `<paths>` | `<paths>` | `<paths or missing_until_verify>` | `<path>` | `<fields>` | `<semantic_quality/workflow_success/...>` |

## Evidence-Regeln

- Fixtures beweisen Parser-/Validator-Verhalten, nicht echte Provider-Rückgabe.
- Echte Stage-Output-Claims brauchen run-bound Artefakte mit gleicher Operation,
  Provider-Route, Raw Response, Parsed Output, Validation und Consumer.
- Perplexity/Search-LLM-Quellen, Citations und `source_refs` bleiben nur dann
  Produkt- oder Crawl-Wahrheit, wenn der Zielvertrag diese Transformation
  ausdrücklich erlaubt.
- Defaulting, Repair und Normalisierung müssen ursprüngliche Fehler sichtbar
  lassen und dürfen fehlende Rückgabefelder nicht als valide erscheinen lassen.
