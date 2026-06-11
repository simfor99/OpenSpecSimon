> [Zurück zum Index](./INDEX.md) | [Rolle und Grenzen](01-rolle-und-grenzen.md) | [Review-Ablauf](02-review-ablauf.md) | [Discovery und Skripte](03-discovery-und-skripte.md) | **Report und Vault**

# Report und Vault

> **Status:** Erstfassung
> **Erstellt:** 2026-06-02
> **Verlinkt mit:** [report-contract.md](../references/report-contract.md), [vault-writeback.md](../references/vault-writeback.md), [report-template.md](../templates/report-template.md)

---

## Warum der Report mehr ist als ein Review-Protokoll

Der Report ist die Akte, nicht das Gespräch. Ein guter Red Review darf nicht nur sagen, dass etwas “komisch wirkt”; er muss zeigen, welche Evidence vorliegt, was genau das Risiko ist, warum Verify es übersehen konnte und ob Codex es reparieren durfte. Danach muss Codex die wichtigen Findings aktiv im Chat mit Simon durchgehen, statt sie nur in Markdown abzulegen.

`00-OPENSPEC-RED-REVIEW.md` ist deshalb bewusst CTO-Review-inspiriert, aber nicht identisch mit dem CTO-Review-Format. Der Skill bereitet keine Vorab-Architekturentscheidung vor, sondern ein Abschlussurteil über einen konkreten OpenSpec-Change. Die Struktur ist kompakt: Zusammenfassung, behauptete Claims, geprüfter Scope, Systemverständnis mit Must-Survive-Facts, versteckte Komplexität, Findings, Evidence Reality Check, Stop-Regeln, Writeback-Ziele und Vault-Learnings.

Die Sektion `Systemverständnis und Must-Survive-Facts` schützt gegen einen typischen Planungsfehler: Der Review darf nicht nur prüfen, ob die Aufgaben formal erledigt aussehen, sondern muss auch sagen, ob der menschliche Zielzustand wirklich im System angekommen ist. Dort stehen die geprüften Subsysteme, die Fakten, die nicht verloren gehen dürfen, und das Coverage Gate. Wenn dieses Gate `partial` oder `no` ist, ist ein glattes `APPROVED` nicht zulässig.

## Verdicts und Findings

Der Report kennt vier Verdicts. `APPROVED` bedeutet, dass keine relevanten Blind Spots übrig sind. `APPROVED_WITH_NOTES` erlaubt Weiterarbeit mit kleineren dokumentierten Risiken oder bereits erledigten Fixes. `BLOCKED` sagt klar, dass der Change nicht archiviert oder als Grundlage genutzt werden sollte. `PAUSED_FOR_DECISION` bedeutet, dass mindestens eine echte Entscheidung bei Simon liegt.

Jedes Finding braucht Evidence, Klasse, Status und Severity. Bei `FIX` muss sichtbar sein, was gefunden und was repariert wurde. Bei `DECISION` muss sichtbar sein, warum es eine Entscheidung ist, welche Optionen existieren, was Red empfiehlt und dass nichts heimlich geändert wurde. Diese Formalität schützt den Report vor zwei typischen Fehlern: kleine Fixes unnötig aufzublasen und echte Entscheidungen als technische Aufräumarbeit zu tarnen.

Materiale Findings gehören zusätzlich in den Chat-Debrief. Wenn Simon ein Finding dort anders bewertet, mehr Kontext gibt oder eine Entscheidung trifft, muss der Report anschließend aktualisiert werden. Der Report unterstützt die Diskussion; er ersetzt sie nicht.

## Evidence Reality Check

Die wichtigste inhaltliche Sektion ist oft der Evidence Reality Check. Dort trennt der Report `claim`, `formal_status`, `runtime_evidence`, `source_truth` und `review_truth`. Ein Verify-Report ist Review-Wahrheit, aber keine Runtime-Evidence. Ein bestandener Unit-Test ist Code-Evidence, aber nicht automatisch Browser-, API- oder Production-Evidence. Diese Unterscheidung ist besonders wichtig in Pipeline-, LLM-, Trace- und Stage-Arbeit, weil dort Daten an mehreren Stellen existieren können, ohne an jeder Stelle dieselbe Bedeutung zu haben.

Ohne diese Trennung kann ein Change grün wirken, obwohl nur bewiesen wurde, dass ein enger Ausschnitt funktioniert. Mit der Trennung kann Simon sehen, ob die behauptete Sicherheit wirklich zur geprüften Evidence-Klasse passt.

## Vault-Writeback

Die Vault ist nicht der Ablageort für jeden einzelnen Review-Fund. Sie ist der Ort für Muster, die später wieder Schutz bieten. Der Skill destilliert deshalb erst nach dem Report bis zu fünf Learning-Kandidaten. Ein Kandidat braucht Kontext, Evidence oder Zahlen, einen genauen Quellpfad und einen wiederverwendbaren Kern.

Ein gutes Vault-Learning wäre zum Beispiel ein Muster wie “formaler Verify kann Evidence-Klassen verwechseln, wenn Reports Claims und Runtime-Beweise nicht sichtbar trennen”. Ein schlechtes Learning wäre “Change X hatte Finding Y”. Das erste hilft beim nächsten Review, das zweite ist nur Historie und gehört in den Report.

## Validierung

Der Report wird mit `validate_openspec_review_report.py` geprüft. Diese Validierung sucht Pflichtsektionen, Verdicts, Platzhalter und Decision-Felder. Sie ersetzt nicht das Urteil, verhindert aber, dass der Abschlussbericht unvollständig oder unfertig wirkt.

Das verbindet den Report mit [Discovery und Skripte](./03-discovery-und-skripte.md): Die Skripte halten die Form stabil, während der Review die Bedeutung trägt. Beide Teile zusammen machen den Skill nützlich.
