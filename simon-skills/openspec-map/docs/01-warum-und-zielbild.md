# Warum und Zielbild

> [Zurück zum Index](./INDEX.md) | **Warum** | [Ablauf](./02-arbeitsfluss-und-handoff.md) | [Vertrag](./03-output-contract-und-validierung.md)

## Der eigentliche Zweck

OpenSpec-Arbeit scheitert selten daran, dass niemand eine Proposal-Datei
schreiben kann. Sie scheitert daran, dass das Proposal bei komplexen Vorhaben
zu früh geschrieben wird. Dann kennt der Chat vielleicht viele Details, aber
die wichtigen Verbindungen sind nicht dauerhaft festgehalten: Welche Datei ist
aktive Wahrheit, welche nur Archiv? Welche Schemafelder müssen erhalten
bleiben? Welche Tests müssen neu entstehen? Welche alten Pfade dürfen nicht
heimlich weiterleben?

`/openspec-map` schützt diesen Übergang. Der Skill nimmt ein ausreichend
geklärtes Vorhaben und macht daraus ein quellengebundenes Briefing. Das
Briefing ist noch kein Proposal. Es ist die Landkarte, die ein gutes Proposal
erst möglich macht, wenn der Scope mehrere Komponenten, Wellen, Quellklassen
oder Verträge umfasst.

## Warum kein harter Vertrag mit Propose

Die naheliegende Versuchung wäre, `/openspec-propose` umzubauen und immer nach
einer Map suchen zu lassen. Das wäre schwerer als nötig. `/openspec-explore`
bereitet heute auch auf Propose vor, ohne technisch daran gekoppelt zu sein.
`/openspec-map` folgt derselben Philosophie: Der Skill ist eine Option im
Arbeitsfluss, kein globales Pflicht-Gate.

Diese Entscheidung hält kleine Changes schnell. Wenn ein Change klar und eng
ist, kann Simon direkt nach `/openspec-propose` gehen. Wenn ein Change groß
ist, bietet Explore oder der Agent zuerst `/openspec-map` an. Der Nutzen liegt
nicht in technischer Kopplung, sondern in einer sozialen und dokumentierten
Konvention: Bei source-heavy Arbeit wird erst gemappt, dann vorgeschlagen.

## Was dadurch möglich wird

Mit `/openspec-map` bekommt die OpenSpec-Kette eine neue Zwischenform. Sie ist
konkreter als Exploration, aber leichter als ein Proposal. Sie kann unfertige
Stellen sichtbar machen, ohne sie zu verstecken. Sie kann `not_ready_for_propose`
sagen, wenn zentrale Quellen oder Entscheidungen fehlen. Und sie kann
`ready_for_propose` sagen, wenn genug Pfad-, Quellen-, Test- und Vertragswissen
gesammelt wurde, um ein Proposal sauber zu schreiben.

Das macht besonders breite Migrations- und Pipeline-Arbeit ruhiger. Die nächste
Session muss nicht aus Chat-Erinnerung rekonstruieren, warum eine Quelle
wichtig war. Sie liest die Map und sieht: Das ist der Scope, das sind die
Quellen, das muss überleben, das muss gelöscht werden, und das ist der nächste
konkrete `$openspec-propose`-Prompt.

> [Zurück zum Index](./INDEX.md) | **Warum** | [Ablauf](./02-arbeitsfluss-und-handoff.md) | [Vertrag](./03-output-contract-und-validierung.md)
