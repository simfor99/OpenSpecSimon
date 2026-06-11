> [Zurück zum Index](./INDEX.md) | [Rolle und Grenzen](01-rolle-und-grenzen.md) | **Review-Ablauf** | [Discovery und Skripte](03-discovery-und-skripte.md) | [Report und Vault](04-report-und-vault.md)

# Review-Ablauf

> **Status:** Erstfassung
> **Erstellt:** 2026-06-02
> **Verlinkt mit:** [review-protocol.md](../references/review-protocol.md), [auditor-contracts.md](../references/auditor-contracts.md)

---

## Vom Ziel zum Urteil

Ein guter Red Review beginnt nicht mit Meinung, sondern mit Bodenhaftung. Der Skill löst zuerst das Ziel auf: Ist ein direkter Pfad übergeben worden, ein Change-Name oder gar kein Argument? Erst wenn klar ist, welcher OpenSpec-Ordner geprüft wird, liest er die Artefakte und baut das Inventar. Diese Reihenfolge verhindert, dass ein Review mit falschem Change-Kontext startet und später nur noch elegante, aber wertlose Schlussfolgerungen produziert.

Danach entsteht der Scope Anchor. Er beschreibt, was behauptet wurde, welche Quellen als Evidence gelten, welche Pfade geprüft werden dürfen und welche Annahmen nur angenommen, aber nicht wirklich verifiziert wurden. Dieser Scope Anchor ist der Sicherheitsgurt des Skills: Ohne ihn könnte ein skeptischer Review schnell zu breit werden und anfangen, das halbe System zu bewerten.

Vor dem Auditorenteam baut der Skill zusätzlich eine Red System Map. Das ist die Sherlock-Schicht im Review: Erst muss Red in einfachen Worten sagen können, welches System der Change wirklich verändert, welche Subsysteme geprüft wurden und welche Must-Survive-Facts nicht verloren gehen dürfen. Ein Must-Survive-Fact ist ein Ziel-Fakt, der auch dann wahr sein muss, wenn ein Task formal abgehakt werden kann. Wenn Simon zum Beispiel eine echte Ordnerzusammenführung wollte, reicht ein neuer Hinweistext nicht aus; der physische Merge, die Umbenennung, die Loader-Pfade und die Evidence dafür müssen sichtbar sein.

Die Systemkarte endet mit einem Coverage Gate. Dort steht, ob die geprüften Quellen für ein verantwortliches Red-Urteil reichen. Bei `partial` oder `no` darf der Skill kein glattes `APPROVED` geben, weil sonst ein bekanntes Loch hinter einem positiven Verdict verschwindet.

## Die Auditoren

Der Skill nutzt mehrere Review-Linsen, weil ein einzelner Blickwinkel leicht blinde Flecken hat. Der Assumption Auditor sucht stille Grundannahmen und versteckte CEO-Entscheidungen. Der Implementation Sense Auditor fragt, ob die Lösung proportional und im richtigen Layer sitzt. Der Evidence Skeptic trennt Claims von Runtime-Evidence, Trace-Wahrheit und Source-Truth. Spec Drift, Test Reality und Archive Hygiene prüfen jeweils die Stellen, an denen formale Fertigkeit besonders leicht mit echter Belastbarkeit verwechselt wird.

Diese Auditoren sollen nicht alle alles tun. Ihre Verträge trennen Zuständigkeiten, damit Findings nicht zu allgemeinen Bauchgefühlen werden. Ein Test Reality Auditor bewertet zum Beispiel, ob Tests das benannte Risiko beweisen; er soll nicht nebenbei eine neue Architektur erfinden. Alle Auditoren lesen die Red System Map und challengen in ihrer eigenen Linse, ob ein Must-Survive-Fact ohne Task, Evidence oder Consumer geblieben ist. Die Team-Red-Synthese sammelt die Ergebnisse, entfernt Dubletten, bewertet Severity und schreibt den Report.

## Der Aktionspunkt

Nach der Synthese entscheidet die `FIX`/`DECISION`-Klassifikation, was passieren darf. Ein `FIX` kann direkt umgesetzt werden, wenn es im erlaubten Scope liegt, keine Verträge verändert und keine echte Wahl für Simon enthält. Eine `DECISION` bleibt unverändert und wird mit Optionen, Empfehlung und “nicht geändert”-Statement in den Report geschrieben.

Der Ablauf endet nicht beim Report. Der Skill validiert den Report gegen seinen Contract, extrahiert mögliche Vault-Learnings und gibt im Chat eine knappe Zusammenfassung aus: Verdict, Counts, gefixte Punkte, offene Entscheidungen und nächster Command. Dadurch kann Simon nach dem Review direkt entscheiden, ob der Change ins Archiv darf, ob ein Fix-Lauf nötig ist oder ob erst eine CEO-Entscheidung geklärt werden muss.

## Standardkette

```text
openspec-apply-change
-> openspec-verify-change
-> openspec-review
-> Simon-Entscheidung bei DECISION-Findings
-> openspec-archive-change
```

Diese Kette ist wichtig, weil jede Station eine andere Verantwortung hat. Apply baut, Verify prüft den Vertrag, Review prüft die Vertrauenswürdigkeit, Simon entscheidet echte Trade-offs und Archive konserviert den finalen Zustand.
