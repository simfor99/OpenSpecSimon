> [Zurück zum Index](./INDEX.md) | [Rolle und Grenzen](01-rolle-und-grenzen.md) | [Review-Ablauf](02-review-ablauf.md) | **Discovery und Skripte** | [Report und Vault](04-report-und-vault.md)

# Discovery und Skripte

> **Status:** Aktiv
> **Erstellt:** 2026-06-02
> **Verlinkt mit:** [target-discovery.md](../references/target-discovery.md), [artifact-inventory.md](../references/artifact-inventory.md)

---

## Warum die Skripte existieren

Ein adversarial Review darf skeptisch sein, aber er darf nicht erraten, worüber er skeptisch ist. Die Skripte geben dem Skill deshalb eine deterministische Grundlage: Sie finden Kandidaten, zählen Tasks, lesen Delta-Specs, sammeln Evidence-Hinweise und prüfen den fertigen Report. Das LLM bleibt für Urteil, Synthese und Sprache zuständig; die Skripte halten die Fakten sortiert.

Diese Trennung macht den Skill wiederholbarer. Wenn ein OpenSpec-Ordner heute als exakter Treffer erkannt wird, soll er morgen nicht wegen einer anderen Formulierung im Chat plötzlich als unklar gelten. Wenn ein Report Pflichtsektionen vermisst, soll das nicht Geschmackssache sein. Die Skripte sind damit die nüchterne Gegenseite zum Team-Red-Teil.

## Die wichtigsten Hilfsskripte

| Skript | Aufgabe |
|--------|---------|
| `discover_openspec_review_targets.py` | Findet aktive, archivierte und fuzzy passende OpenSpec-Review-Ziele. |
| `inventory_openspec_archive.py` | Baut ein Inventar aus Standarddateien, Delta-Specs, Tasks, Evidence und referenzierten Pfaden. |
| `openspec_review_prescan.py` | Markiert strukturelle Risiken wie offene Tasks, fehlenden Verify oder fehlenden Red Review. |
| `classify_review_findings.py` | Zählt `FIX`/`DECISION`, Severity und fehlende Finding-Felder in einem Report. |
| `validate_openspec_review_report.py` | Prüft Pflichtsektionen, Verdicts, Platzhalter und Decision-Contract. |
| `distill_vault_learnings.py` | Extrahiert mögliche Vault-Learning-Kandidaten aus dem fertigen Report. |
| `openspec_review_lib.py` | Gemeinsame Hilfsfunktionen für Namen, Pfade, Inventar und JSON-Ausgabe. |

## Wie Discovery gedacht ist

Mit Argument ist der Alltagspfad direkt. Ein Aufruf mit `gtm-runtime-stage-packet-standardization` findet zuerst `openspec/changes/gtm-runtime-stage-packet-standardization/`. Wenn dieser exakte aktive Change existiert, setzt Discovery `selected_candidate` und der Skill muss Simon nicht künstlich um Auswahl bitten.

Ohne Argument wird Discovery vorsichtiger. Sie zeigt Kandidaten mit Score, Art, Pfaden, gefundenen Artefakten, Risk Note und Recommendation. Das ist absichtlich ähnlich zur Idee von `$smart-commit`: Erst zusammenhängende Arbeit erkennen, dann entscheiden, was wirklich gemeint ist. Der Skill soll nicht automatisch den “plausibelsten” Change reviewen, wenn mehrere echte Kandidaten existieren.

## Was die Skripte nicht entscheiden

Die Skripte liefern Hinweise, keine Freigabe. Ein fehlender Verify-Report ist ein Signal, aber die endgültige Bewertung hängt vom Review-Modus ab. Offene Tasks können echte Restarbeit oder veraltete Hygiene sein. Ein vorhandener Test-Review kann starke Evidence oder nur ein gut formulierter Claim sein. Diese Unterscheidung bleibt Aufgabe des Reviews.

Das verbindet die Skripte mit [Review-Ablauf](./02-review-ablauf.md): Sie bauen den Boden, auf dem Auditoren argumentieren. Ohne sie wäre der Review zu weich; ohne Auditoren wären die Skripte zu blind für Bedeutung.
