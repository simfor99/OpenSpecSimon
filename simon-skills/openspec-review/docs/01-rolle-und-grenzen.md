> [Zurueck zum Index](./INDEX.md) | **Rolle und Grenzen** | [Review-Ablauf](02-review-ablauf.md) | [Discovery und Skripte](03-discovery-und-skripte.md) | [Report und Vault](04-report-und-vault.md)

# Rolle und Grenzen

> **Status:** Erstfassung
> **Erstellt:** 2026-06-02
> **Verlinkt mit:** [SKILL.md](../SKILL.md), [verify-boundary.md](../references/verify-boundary.md)

---

## Warum diese Grenze wichtig ist

Ein formaler Verify ist notwendig, aber er ist nicht dasselbe wie Vertrauen. `$openspec-verify-change` kann zeigen, dass Aufgaben erledigt, Requirements abgedeckt und Reports vorhanden sind. Was er nicht zuverlässig leisten soll, ist die skeptische Frage, ob die ursprüngliche Richtung klug war, ob ein Test wirklich das benannte Risiko beweist oder ob eine offene Entscheidung versehentlich als technische Selbstverständlichkeit behandelt wurde.

`openspec-review` ist deshalb der Kollege, der nach dem grünen Haken noch einmal stehen bleibt. Er fragt nicht “Sind alle Kästchen abgehakt?”, sondern “Haben wir uns gerade selbst überzeugt, obwohl die Evidence dünner ist als die Behauptung?” Diese Rolle ist unbequem, aber sie verhindert, dass ein formal sauberer Change zu früh als belastbare Wahrheit ins Archiv wandert.

## Was der Skill übernimmt

Der Skill übernimmt den adversarial Zweitblick auf OpenSpec-Changes. Er darf aktive Changes, archivierte Changes und zusammenhängende Change-Gruppen prüfen. Er darf Evidence sortieren, Annahmen markieren, Testrealität hinterfragen und kleine sichere `FIX`-Findings reparieren. Er darf außerdem einen Report schreiben, der Simon in wenigen Minuten zeigt, ob ein Change archivfähig, blockiert oder entscheidungsbedürftig ist.

Das macht ihn besonders wertvoll in der Kette nach `$openspec-verify-change`. Dort liegt bereits ein formales Ergebnis vor, und der Review kann sich auf die Fragen konzentrieren, die ein formaler Prüfer absichtlich nicht abschließend beantwortet: Sinnhaftigkeit, Proportionalität, Blind Spots, Scope-Drift und Evidence-Verwechslungen.

## Was der Skill nicht übernimmt

Der Skill ersetzt nicht `$openspec-verify-change`, implementiert keinen OpenSpec-Change von Grund auf und archiviert keine Ordner. Er synchronisiert keine Specs still, führt keine Migrationen aus, schreibt nicht in externe Systeme und ändert keine öffentlichen Verträge ohne ausdrückliche Entscheidung. Diese Begrenzung ist kein Mangel, sondern der Schutzmechanismus des Skills.

Wenn ein Finding eine echte Wahl enthält, wird es als `DECISION` behandelt. Das gilt auch dann, wenn Codex technisch in der Lage wäre, etwas direkt zu ändern. Der Skill soll nicht heimlich Strategie machen; er soll Strategiebedarf sichtbar machen. Genau dadurch bleibt Simon Entscheidungseigner und der Review bleibt glaubwürdig.

## Die einfache Regel

`FIX` ist der lose Nagel im vorhandenen Brett. `DECISION` ist die Frage, ob das Brett überhaupt an diese Wand gehört. Der Skill darf den losen Nagel einschlagen, aber nicht die Wand versetzen.

Diese Unterscheidung verbindet sich mit [Report und Vault](./04-report-und-vault.md), weil jedes Finding im Abschlussbericht diese Grenze sichtbar machen muss. Sie verbindet sich außerdem mit [Review-Ablauf](./02-review-ablauf.md), weil die Klassifikation nicht am Ende als Kosmetik passiert, sondern vor jeder Aktion.
