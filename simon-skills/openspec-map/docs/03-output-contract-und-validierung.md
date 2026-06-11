# Output-Contract und Validierung

> [Zurück zum Index](./INDEX.md) | [Warum](./01-warum-und-zielbild.md) | [Ablauf](./02-arbeitsfluss-und-handoff.md) | **Vertrag**

## Warum der Output-Vertrag zählt

Eine Map ist nur dann nützlich, wenn sie später wirklich gelesen und verwendet
werden kann. Dafür reicht ein gutes Memo nicht aus. Das Briefing braucht eine
stabile Form, damit `/openspec-propose` daraus konkrete Proposal-, Design- und
Task-Inhalte ableiten kann. Der Output-Vertrag zwingt die Map deshalb, nicht
nur Absichten zu beschreiben, sondern auch Pfade, Rollen, Tests, Verträge und
offene Lücken explizit zu machen.

Die vollständige Struktur liegt in
[`../references/output-schema.md`](../references/output-schema.md). Pro
Komponente werden Quellen, Zielpfade, Verträge oder Schemas, Assets, Tests,
Aufwand, obsolete Pfade und offene Fragen festgehalten. Das ist absichtlich
generisch. Der Skill soll nicht nur Migrationen abbilden, sondern auch
Library-Wechsel, Domänen-Splits, Datenmodell-Konsolidierungen und komplexe
Greenfield-Features.

Seit Version 1.1.0 enthält der Vertrag zusätzlich Skill-Netzwerk-Felder. Eine
Map kann CTO Reviews, Goal Briefs, Pre-Proposal Reading Contracts, Test
Reviews, CEO Reviews oder Verify-Artefakte als eigene Steuerquellen benennen.
Das verhindert, dass ein CTO-Blocker, eine Deep-Read-Pflicht oder ein späteres
Evidence-Gate in normalen Notizen verschwindet.

Seit Version 1.1.1 kann die Map außerdem Prompt-Contracts aus konkreten
Prompt-Blöcken erzeugen. Dafür gibt es im Briefing einen eigenen Abschnitt
`Prompt Contracts` und im Readiness-Block die Felder
`prompt_contracts_required`, `prompt_contracts_status` und
`prompt_contract_files`. Wenn Prompt-Contracts erforderlich sind, darf eine Map
nur `ready_for_propose` sein, wenn diese Dateien wirklich existieren und als
Pflichtquelle für `$openspec-propose` und `$openspec-apply-change` gelistet
sind.

Der Vertrag unterscheidet zwei Rückkanäle: `map_backchannel_status` beschreibt,
ob die Map selbst neue CTO-relevante Befunde zurückgeschrieben hat.
`cto_review_backchannel_required` beschreibt, ob `$openspec-propose` nach
Proposal-Erzeugung den Quell-Review erneut aktualisieren muss.

## Propose Readiness

Der Readiness-Block ist die rote oder grüne Ampel für den nächsten Schritt. Er
kennt nur zwei Zustände: `ready_for_propose` und `not_ready_for_propose`.
`ready_for_propose` heißt nicht, dass die Arbeit fertig, richtig implementiert
oder CEO-approved ist. Es heißt nur: Das Briefing ist gut genug, damit
`$openspec-propose` daraus sinnvolle OpenSpec-Artefakte bauen kann.

Die Ampel berücksichtigt jetzt auch CTO- und Goal-Brief-Pflichten. Ein
strukturell vollständiges Briefing bleibt `not_ready_for_propose`, wenn ein
CTO Review noch offene Blocking Decisions enthält, die Proposal-Scope oder
Architekturpfad steuern. Umgekehrt kann eine Map `ready_for_propose` sein und
trotzdem `goal_brief_recommended: true` setzen, wenn die spätere Umsetzung ein
eigenes Execution-Control-File braucht.

`not_ready_for_propose` ist kein Fehlschlag. Es ist der wichtigste Schutz des
Skills. Wenn zentrale Quellen nicht gelesen wurden, Zielpfade fehlen oder
Entscheidungen widersprüchlich sind, muss die Map das sichtbar machen. Ein
ehrliches `not_ready_for_propose` ist besser als ein schönes Proposal auf
wackeligem Boden.

## Validierung und Grenzen

Der Validator
[`../scripts/validate_map_briefing.py`](../scripts/validate_map_briefing.py)
prüft nur Struktur: Frontmatter, Pfadzeile, Component Map,
`propose_readiness`, Handoff und zentrale Felder. Skill-Netzwerk-Abschnitte wie
Upstream Decision Sources, Skill Network Handoff oder CTO Review Backchannel
werden als Warnsignale geprüft, nicht als harte Fehler, damit ältere Map-
Artefakte lesbar bleiben. Der Validator beweist nicht, dass die Map fachlich
vollständig ist. Diese Grenze ist bewusst: Ein Skript kann erkennen, ob ein
Briefing wie eine Map aussieht. Es kann nicht beurteilen, ob alle Quellen
richtig gelesen wurden.

Für Prompt-Contracts gibt es eine härtere Strukturprüfung: Wenn
`prompt_contracts_required: true` gesetzt ist, verlangt der Validator den
Abschnitt `Prompt Contracts`, den Status `created` und mindestens eine Datei
unter `prompt_contract_files`. Er prüft nicht semantisch, ob der Prompt
vollständig korrekt kopiert wurde; diese Fidelity-Prüfung bleibt Aufgabe von
Map-Ersteller, `$openspec-propose`, `$openspec-apply-change` und
`$openspec-review`.

Die fachliche Prüfung bleibt deshalb menschlich und agentisch. Eine gute Map
muss beim Lesen beantworten: Warum gehört diese Komponente in den Scope?
Welche Quelle ist aktiv? Welche Quelle ist nur Referenz? Welche Tests schützen
den späteren Change? Was wird obsolet? Und was muss vor Propose noch geklärt
werden?

> [Zurück zum Index](./INDEX.md) | [Warum](./01-warum-und-zielbild.md) | [Ablauf](./02-arbeitsfluss-und-handoff.md) | **Vertrag**
