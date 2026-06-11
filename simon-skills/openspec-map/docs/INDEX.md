# OpenSpec Map — Dokumentationshub

> **[Index]** | [Warum](./01-warum-und-zielbild.md) | [Ablauf](./02-arbeitsfluss-und-handoff.md) | [Vertrag](./03-output-contract-und-validierung.md)

## Warum dieser Hub existiert

`/openspec-map` ist entstanden, weil zwischen guter Exploration und guter
Proposal-Erzeugung oft ein stiller Abgrund liegt. In `/openspec-explore` wird
ein Problem verstanden: Optionen werden verglichen, Architekturkräfte werden
sichtbar, Pfade tauchen auf, Risiken werden benannt. Danach soll
`/openspec-propose` daraus konkrete OpenSpec-Artefakte schreiben. Bei kleinen
Changes funktioniert das direkt. Bei breiten Migrationen, Stage-Wellen,
Prompt-/Schema-Handoffs oder vielen Quellklassen wird aus diesem Sprung aber
leicht ein Ratespiel.

Der Skill löst genau diesen Moment. Er macht aus der Erkenntnis kein Proposal,
sondern eine belastbare Karte: Welche Komponenten gehören zum Scope? Welche
Quellen sind aktiv, welche nur Archiv oder Referenz? Welche Zielpfade,
Verträge, Tests, Builder-Plan-Seeds, Testschrift-Zeilen,
Quality-Gate-Kandidaten und Cleanup-Pfade müssen im späteren Proposal
überleben? Diese
Karte schützt `/openspec-propose` davor, generische Tasks zu erzeugen, nur weil
der Chat viel wusste, aber keine dauerhafte, quellengebundene Struktur hinter-
lassen hat.

## Was gebaut wurde

Der Skill ist ein leichter Bridge-Skill in der OpenSpec-Familie. Er lebt unter
[`../SKILL.md`](../SKILL.md) und führt von Exploration zu Proposal, ohne beide
hart zu koppeln. Das ist die wichtigste Designentscheidung: `/openspec-map`
ist kein Gate und keine Erweiterung von `/openspec-propose`. Der Skill erzeugt
ein Map-Briefing und endet mit einem klaren nächsten Prompt. Danach kann Simon
oder der nächste Agent `$openspec-propose` mit diesem Briefing als primärer
Quelle starten.

Die operative Fassung besteht aus einem knappen Skill-Vertrag, vier Referenzen,
zwei Templates und einem kleinen Validator. Der aktuelle Vertrag kann außerdem
Implementation-Ledger-Bedarf, Builder-Plan-Seeds, Intent-Driven-Testschrift-
Seeds, Quality-Gate-Kandidaten, Prompt-/LLM-Output-Contract-Pflichten und
External-Side-Effect-Reality-Gates als Übergabepflichten sichtbar machen:

- Skill-Vertrag: [`../SKILL.md`](../SKILL.md)
- Output-Schema: [`../references/output-schema.md`](../references/output-schema.md)
- Quellenklassen: [`../references/source-classes.md`](../references/source-classes.md)
- Handoff-Konvention: [`../references/handoff-convention.md`](../references/handoff-convention.md)
- Abbruchmodi: [`../references/abort-modes.md`](../references/abort-modes.md)
- Subagent-Template: [`../templates/component-inventory-prompt.md`](../templates/component-inventory-prompt.md)
- Map-Artefakt-Template: [`../templates/map-artifact-template.md`](../templates/map-artifact-template.md)
- Strukturvalidator: [`../scripts/validate_map_briefing.py`](../scripts/validate_map_briefing.py)

## Wie der Skill in die OpenSpec-Kette passt

Die lesbare Kette ist bewusst einfach, aber nicht mehr isoliert:

```text
$openspec-explore / $cto-review -> $openspec-map -> $openspec-propose
                                               -> $goal-brief when needed
```

`/openspec-explore` bleibt der Ort für Denken, Fragen, Optionen und
Architekturgefühl. `/openspec-map` kommt erst dann ins Spiel, wenn die Form
des Problems erkennbar ist, aber noch zu viele Quellen, Komponenten oder
Abhängigkeiten offen herumliegen. Wenn ein CTO Review beteiligt ist, übernimmt
die Map dessen Entscheidungen, Stop-Regeln und Evidence Gates als benannte
Quellen, nicht als lose Notizen. `/openspec-propose` bleibt der Skill, der aus
dieser Vorbereitung echte OpenSpec-Artefakte baut und danach den CTO-Review-
Rückkanal aktualisiert. Für breite Umsetzung kann die Map außerdem ein
`goal.md` über `$goal-brief` empfehlen und konkrete Test-/Evidence-Oberflächen
für `builder-plan.md`, `quality-gates.md` oder `implementation-ledger.md`
vorbereiten.

Dadurch entsteht keine neue Bürokratie. Kleine Änderungen können weiterhin
direkt von Explore nach Propose gehen. Große Änderungen bekommen eine
Zwischenkarte, damit der spätere Proposal-Text nicht nur gut klingt, sondern
auf Pfaden, Tests, Verträgen und Cleanup-Evidence ruht.

## Dokumentkarte

| Nr | Dokument | Beschreibung |
|---:|---|---|
| 01 | [Warum und Zielbild](./01-warum-und-zielbild.md) | Erzählt die Lücke zwischen Explore und Propose und warum eine Map besser ist als ein harter Integrationsvertrag. |
| 02 | [Arbeitsfluss und Handoff](./02-arbeitsfluss-und-handoff.md) | Beschreibt den konkreten Ablauf vom Scope über Inventory und Konsolidierung bis zum nächsten `$openspec-propose`-Prompt. |
| 03 | [Output-Contract und Validierung](./03-output-contract-und-validierung.md) | Erklärt `propose_readiness`, Quellenklassen, Validator und die Grenzen des Skills. |

## Aktueller Status

Der Skill ist die aktive Quellen- und Contract-Brücke zwischen Explore/CTO
Review und Propose. Die Struktur folgt dem Skill-Forger-Standard: `SKILL.md`
bleibt knapp, Details liegen in `references/` und wiederverwendbare Formen in
`templates/`. Für echte komplexe Scopes bleibt der Maßstab konkret: Eine gute
Map muss genug Pfad-, Test-, Gate-, Ledger-, Builder-Plan- und Testschrift-
Information liefern, damit `$openspec-propose` daraus prüfbare OpenSpec-
Artefakte erzeugen kann, ohne aus Chat-Erinnerung zu raten.

> **[Index]** | [Warum](./01-warum-und-zielbild.md) | [Ablauf](./02-arbeitsfluss-und-handoff.md) | [Vertrag](./03-output-contract-und-validierung.md)
