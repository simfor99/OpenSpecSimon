# Arbeitsfluss und Handoff

> [Zurück zum Index](./INDEX.md) | [Warum](./01-warum-und-zielbild.md) | **Ablauf** | [Vertrag](./03-output-contract-und-validierung.md)

## Vom Problemgefühl zur belastbaren Karte

Der Skill beginnt nicht bei null. Er wird sinnvoll, wenn Exploration bereits
eine Form erzeugt hat: Es gibt einen möglichen Change-Namen, eine Wave, eine
Komponentengruppe oder ein Set von Quellen, das im Proposal nicht verloren
gehen darf. Der erste Schritt ist deshalb immer Scope-Klärung. Der Skill fragt
nicht breit nach allem, sondern versucht aus Pfaden, Tagesartefakten,
OpenSpec-Ordnern und Architekturentscheidungen den kleinsten belastbaren Scope
zu rekonstruieren.

Wenn ein CTO Review im Spiel ist, wird er nicht wie normale Doku behandelt. Er
ist die Risiko-, Entscheidungs- und Stop-Regel-Quelle. Die Map übernimmt daraus
`spec_mode_status`, Blocking Decisions, Stop-Regeln, Evidence Gates und
Rückschreibziele. Sie entscheidet diese Punkte nicht neu, sondern macht
sichtbar, was später in OpenSpec übergehen muss und welcher Rückkanal nach
`$openspec-propose` nötig ist.

Wenn die Map selbst neue Fakten erzeugt, reicht diese spätere Übergabe nicht.
Dann schreibt die Map direkt zurück: Der Quell-CTO-Review bekommt einen
`OpenSpec-Map-Rückkanal` oder ein verlinktes Addendum. Das gilt zum Beispiel,
wenn konkrete Source-/Target-Pfade eine alte Annahme ersetzen, wenn aus einem
Risiko ein belegter Blocker wird oder wenn die Map zeigt, dass vor Apply erst
ein anderes Skill-Gate nötig ist.

Danach trennt der Skill Quellenklassen. Das ist der wichtigste praktische
Schritt. Aktiver Code, Architektur-Doku, Entscheidungen, Archive, Templates,
Traces und Tests dürfen nicht in einer Liste verschwimmen. Eine alte
Implementation kann wertvoll sein, aber sie ist nicht automatisch Wahrheit.
Eine Architekturentscheidung kann knapp sein, aber sie kann eine größere
Codefläche überstimmen. Diese Rollen sichtbar zu machen, ist die eigentliche
Arbeit der Map.

Wenn konkrete Prompts im Quellmaterial stehen, behandelt die Map sie nicht als
Fließtext. Zielprompts werden als Prompt-Contracts extrahiert oder als
Pflichtquelle markiert. Jede Contract-Datei trägt Provenienz, Contract-Klasse
und Extraction Mode. Dadurch kann `$openspec-propose` später auf echte Dateien
verweisen und `$openspec-apply-change` gegen diese Dateien bauen, statt einen
Prompt aus Review-Prosa nachzuerzählen.

## Mapping-Modi

Bei kleinen Scopes kann der Hauptagent lokal arbeiten. Bei größeren Scopes
können Subagents helfen, wenn die aktuelle Laufzeit Delegation erlaubt oder
Simon sie ausdrücklich wünscht. Dann arbeiten sie als read-only Scouts für
Komponenten oder Komponentengruppen, lesen selbst und liefern strukturierte
Reports. Der Hauptagent bleibt Eigentümer der Map. Er zieht die Reports
zusammen, prüft die genannten Quellen, markiert Konflikte und schreibt das
finale Briefing.

Subagents bekommen bewusst nicht den ganzen Gesprächskontext. Sie bekommen
Komponente, Pfadhinweise und das Output-Schema. Das reduziert Kontextdruck und
verhindert, dass ein einzelner großer Chatverlauf zur unsichtbaren Quelle der
Wahrheit wird.

Die gemeinsame Grenze steht in
`/home/simon/.codex/skills/shared/references/openspec-subagent-policy.md`:
Subagent-Reports sind Evidenz, nicht Wahrheit. Prompt-Contract-Sidecars,
`propose_readiness`, Validator-Ergebnisse und die finale Map bleiben beim
Hauptagenten.

## Das Briefing als Übergabe

Am Ende steht ein Markdown-Artefakt. Es enthält Komponenten-Mapping,
Quellenklassen, Zielpfade, Verträge, Assets, Tests, Aufwand, Cleanup,
Cross-Component-Findings und offene Fragen. Der wichtigste Block ist
`propose_readiness`. Dort steht, ob die Map bereit für Propose ist oder ob
vorher noch zentrale Quellen, Zielpfade oder Entscheidungen fehlen.

Der Handoff bleibt leicht:

```text
$openspec-propose <change-name> using <map-path> as the primary briefing source.
```

Das ist kein vollständiger technischer Vertrag, aber es enthält jetzt die
Skill-Netzwerk-Pflichten. Wenn der Scope sehr quellenlastig ist, kann die Map
zusätzlich empfehlen, dass `$openspec-propose` die Map als Pre-Proposal Reading
Contract behandelt oder einen solchen Contract erstellt. Wenn ein CTO Review
gelesen wurde, muss die Map den späteren Rückkanal benennen: Nach
Proposal-Erzeugung aktualisiert `$openspec-propose` den Quell-Review oder legt
ein verlinktes Addendum an. Wenn spätere Execution ein eigenes Ziel- und
Evidence-Gate braucht, empfiehlt die Map außerdem `goal.md` über
`$goal-brief`.

Wenn Prompt-Contracts erzeugt wurden, benennt der Handoff zusätzlich die
Contract-Dateien und die Fidelity-Pflicht: Propose muss sie verlinken, Apply
muss sie umsetzen, Review muss vollständige Übernahme und fehlende
Halluzination prüfen.

Wenn der Scope evidence-sensitiv ist, benennt der Handoff außerdem die neuen
OpenSpec-Meta-Oberflächen: ob `implementation-ledger.md`, `builder-plan.md`,
Intent-Driven-Testschrift-Zeilen oder `quality-gates.md` empfohlen, erforderlich
oder bereits vorhanden sind. Die Map schreibt diese Artefakte nicht als zweiten
Taskgraphen aus, sondern liefert Seeds, damit `$openspec-propose` sie später im
OpenSpec-Change materialisieren kann.

Für bereits existierende OpenSpec-Changes ist die Map auch vor
`$openspec-apply-change` sinnvoll. Ein Proposal kann formal fertig sein und
trotzdem noch keine belastbare Implementation Map besitzen. Signale dafür sind
Fragen wie "was muss noch gebaut werden?", "welche Source Map fehlt?", "welche
Pfade sind betroffen?" oder eine große Taskliste ohne konkrete Source- und
Zielpfade.

> [Zurück zum Index](./INDEX.md) | [Warum](./01-warum-und-zielbild.md) | **Ablauf** | [Vertrag](./03-output-contract-und-validierung.md)
