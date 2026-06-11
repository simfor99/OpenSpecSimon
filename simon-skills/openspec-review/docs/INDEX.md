# OpenSpec Review — Skill-Hub

> **Skill:** `openspec-review`
> **Status:** Erstfassung
> **Erstellt:** 2026-06-02
> **Letztes Update:** 2026-06-02

---

## Warum dieser Skill existiert

OpenSpec hat bereits einen formalen Prüfschritt: `$openspec-verify-change` gleicht Aufgaben, Requirements, Goal Evidence und Archivfähigkeit ab. Genau darin liegt aber eine Lücke. Ein grüner Verify kann beweisen, dass der vereinbarte Vertrag formal erfüllt wurde, aber er beweist nicht automatisch, dass der Vertrag klug war, dass die Annahmen stimmten oder dass die Evidence wirklich die behauptete Realität trägt. Vor `openspec-review` blieb diese zweite Frage oft im Kopf hängen: “Ja, es ist grün, aber war es auch sinnvoll?”

Der Skill löst dieses Problem als misstrauischer Zweitblick. Er nimmt den Verify nicht weg, sondern stellt sich dahinter und fragt andere Dinge: Wurde eine Entscheidung still als Implementierungsdetail behandelt? Wurde ein Testlauf mit echter Runtime-Wahrheit verwechselt? Hat ein Report nur behauptet, was eigentlich eine Trace-, API-, Browser- oder Source-Evidence gebraucht hätte? Dadurch wird der Review nicht zum weiteren Checkbox-Zähler, sondern zum Schutz gegen Selbsttäuschung.

Das ermöglicht einen klareren Übergang zwischen Build, Verify, Review, Entscheidung und Archiv. Simon bekommt nicht nur “fertig” oder “nicht fertig”, sondern ein belastbares Bild: Welche Issues darf Codex direkt reparieren, welche gehören als echte Entscheidung auf den Tisch, welche Learnings sind wiederverwendbar genug für die Vault und was ist der nächste konkrete Schritt.

| Vorher | Nachher |
|--------|---------|
| Verify war die letzte harte Station vor dem Archiv. | Verify bleibt formal, `openspec-review` ergänzt den adversarial Zweitblick. |
| Unsichere Punkte wurden leicht zu Bauchgefühl oder Chat-Kontext. | Findings werden als `FIX` oder `DECISION` mit Evidence dokumentiert. |
| Learnings aus Reviews konnten verschwinden. | Wiederverwendbare Muster werden für Vault-Writeback vorbereitet. |

---

## Wie der Skill funktioniert

Wenn der Skill mit einem Namen wie `gtm-runtime-stage-packet-standardization` gestartet wird, sucht er zuerst den passenden OpenSpec-Ordner. Findet er einen exakten aktiven Change, kann er direkt starten; findet er mehrere plausible aktive oder archivierte Änderungen, zeigt er eine Auswahl. Ohne Argument übernimmt die Smart-Discovery denselben Job wie ein vorsichtiger Commit-Assistent: Sie scannt aktive Changes, Archive, Spec-Cluster und vorhandene Review-Artefakte, bevor teure Review-Arbeit beginnt.

Danach baut der Skill ein Inventar. Er liest nicht nur `proposal.md`, `design.md`, `goal.md`, `tasks.md` und Delta-Spec-Dateien unter dem Change-Ordner, sondern sucht auch nach Verify-Reports, Evidence-Dateien, referenzierten Codepfaden und vorhandenen Red Reviews. Aus diesem Inventar entsteht ein Scope Anchor: Was darf geprüft werden, was wurde behauptet, welche Pfade sind erlaubt und welche Annahmen wurden nicht wirklich verifiziert?

Erst dann beginnt der Team-Red-Teil. Die Auditoren prüfen Annahmen, Implementierungssinn, Evidence-Qualität, Spec-Drift, Testrealität und Archivhygiene. Jedes Finding wird klassifiziert. `FIX` bedeutet: eindeutig, sicher, innerhalb des erlaubten Scopes reparierbar. `DECISION` bedeutet: Simon muss entscheiden, weil Scope, Architektur, Public Contract, Spec-Sync, Runtime-Schreibzugriff oder ein echter Trade-off betroffen ist.

### Kerndaten

| Feld | Wert |
|------|------|
| Aufruf | `Skill("openspec-review", args: "<change-name>")` |
| Ohne Argument | Discovery über aktive und archivierte OpenSpec-Changes |
| Standardreport | `00-OPENSPEC-RED-REVIEW.md` im Change-Ordner |
| Direkte Fixes | Nur sichere `FIX`-Findings |
| Simon-Entscheidungen | Alle `DECISION`-Findings bleiben unverändert |
| Hilfsskripte | 7 Python-Skripte unter `../scripts/` |
| Tests | Pytest-Suite unter `../tests/` |

---

## Wie es zusammenhängt

Der Skill verbindet sich mit `$openspec-verify-change`, weil er dessen Ergebnis nicht dupliziert, sondern herausfordert. Verify fragt: “Ist der OpenSpec-Vertrag formal erfüllt?” OpenSpec Review fragt: “Ist das, was wir gerade erfüllen, als Grundlage wirklich vertrauenswürdig?” Ohne diese Trennung würde der Review entweder zu weich werden oder Verify-Arbeit wiederholen.

Der Skill verbindet sich außerdem mit `$openspec-archive-change`, weil er als letzte skeptische Station vor dem Archiv laufen kann. Ein `APPROVED` oder `APPROVED_WITH_NOTES` macht die Archiventscheidung leichter, während `BLOCKED` und `PAUSED_FOR_DECISION` verhindern, dass offene Risiken in die Historie wegsortiert werden. Das Archiv wird dadurch nicht nur sauberer, sondern erklärbarer.

Die Vault-Anbindung macht den Skill langfristig wertvoller. Ein einzelnes Finding bleibt im Change-Report, aber ein wiederkehrendes Muster wie “CODE_PASS wurde als RUNTIME_VALIDATED gelesen” gehört in die Vault. So wird aus einem lokalen Fehler ein wiederverwendbarer Review-Schutz für spätere Arbeit.

---

## Schlüsselentscheidungen

### Verify-Grenze statt Verify-Ersatz

**Kontext:** Der neue Skill sollte nach `$openspec-verify-change` laufen können, ohne dessen Rolle zu verwischen. Wenn beide Skills dieselben Fragen stellen, entsteht nur ein zweiter grüner Stempel.

**Entscheidung:** `openspec-review` prüft nicht primär Task-Checkboxen und formale Archivfähigkeit, sondern Annahmen, Evidence-Realität, Implementierungssinn und übersehene Entscheidungen.

**Konsequenzen:**
- (+) Der Review ergänzt Verify mit echter Skepsis.
- (-) Der Skill braucht mehr Kontext als ein reiner Statuscheck.
- (~) Frühere Läufe sind möglich, müssen aber als `early-paranoia` und nicht als Archivfreigabe gelesen werden.

### FIX/DECISION als Aktionsgrenze

**Kontext:** Der Skill soll gefundene Issues nicht nur beschreiben, sondern sichere Probleme direkt reparieren können. Gleichzeitig darf Codex keine CEO-, Architektur- oder Scope-Entscheidungen heimlich treffen.

**Entscheidung:** Jedes Finding wird vor einer Aktion als `FIX` oder `DECISION` klassifiziert. Nur `FIX` darf umgesetzt werden; `DECISION` wird mit Optionen und Red-Empfehlung im Report festgehalten.

**Konsequenzen:**
- (+) Kleine, klare Fehler verschwinden sofort.
- (-) Manche Findings bleiben absichtlich offen, obwohl Codex technisch etwas ändern könnte.
- (~) Bei Unsicherheit gewinnt `DECISION`, weil ein falscher Automatismus teurer wäre als eine kurze Entscheidung.

### Report vor Vault

**Kontext:** Vault-Learnings sind wertvoll, aber nur, wenn sie echte wiederverwendbare Muster enthalten. Rohe Findings oder change-spezifische Details würden die Vault verrauschen.

**Entscheidung:** Der Skill schreibt zuerst den Red-Review-Report und destilliert danach höchstens fünf Vault-Learning-Kandidaten mit Evidence und Quelle.

**Konsequenzen:**
- (+) Die Vault bekommt Muster statt Protokollreste.
- (-) Manche Reviews erzeugen bewusst kein Learning.
- (~) Der Report bleibt die primäre Wahrheit für den einzelnen Change.

---

## Dokument-Map

### Skill-Dokumente in diesem Ordner

| Nr | Dokument | Zeilen | Beschreibung |
|----|----------|--------|--------------|
| 01 | [Rolle und Grenzen](01-rolle-und-grenzen.md) | 33 | Warum der Skill neben Verify existiert und was er nicht übernimmt. |
| 02 | [Review-Ablauf](02-review-ablauf.md) | 39 | Der Weg von Zielauflösung über Auditoren bis Report. |
| 03 | [Discovery und Skripte](03-discovery-und-skripte.md) | 39 | Wie die Hilfsskripte Bodenhaftung geben. |
| 04 | [Report und Vault](04-report-und-vault.md) | 39 | Wie Findings, Verdicts und Learnings geschrieben werden. |

### Verwandte Dateien im Skill

| Datei | Relevanz |
|------|----------|
| [SKILL.md](../SKILL.md) | Operativer Router und Prozessvertrag des Skills. |
| [verify-boundary.md](../references/verify-boundary.md) | Harte Abgrenzung zu `$openspec-verify-change`. |
| [review-protocol.md](../references/review-protocol.md) | Detaillierter Ablauf und Review-Lenses. |
| [fix-decision-classification.md](../references/fix-decision-classification.md) | Regelwerk für direkte Fixes versus Simon-Entscheidungen. |
| [report-template.md](../templates/report-template.md) | Vorlage für `00-OPENSPEC-RED-REVIEW.md`. |

---

## Leseempfehlung

Der beste Einstieg ist dieses `INDEX.md`, danach [Rolle und Grenzen](./01-rolle-und-grenzen.md). Wer den Skill ausführen oder debuggen will, liest anschließend [Review-Ablauf](./02-review-ablauf.md) und [Discovery und Skripte](./03-discovery-und-skripte.md). Wer wissen will, was am Ende herauskommt, springt direkt zu [Report und Vault](./04-report-und-vault.md).

---

## Änderungshistorie

| Datum | Was |
|-------|-----|
| 2026-06-02 | Initiale Dokumentation des neuen `openspec-review`-Skills erstellt. |
