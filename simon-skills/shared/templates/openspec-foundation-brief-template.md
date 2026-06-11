# Vorlage: OpenSpec Foundation Brief

> Datei: `~/.codex/skills/shared/templates/openspec-foundation-brief-template.md`
> Status: aktiver Shared-Vertrag der OpenSpec-Skillfamilie
> Konsumenten: `$openspec-explore` (bietet an), `$openspec-map` (verlangt bei Stage-Neuschnitt, konsumiert), `$openspec-propose` (liest als `primary_foundation` mit `role: target_contract`)
> Referenzbeispiel: `docs/todo/2026_06_04/03_artifacts/009_stage00-produktwelt-zielbild__artifact__________2026_06_04__18-52.md` (Sanctum-OS)
> Klärungsprotokoll vor dem Schreiben: [`../references/openspec-foundation-grilling.md`](../references/openspec-foundation-grilling.md)
> Validator: `python3 ~/.codex/skills/shared/scripts/validate_foundation_brief.py <brief-pfad>`
> Entschieden: 2026-06-10 (CEO-Entscheidungen 1-3, siehe `.teamred/openspec-foundation-brief-skillchain/00-RED-TEAM-REVIEW.md` im Sanctum-OS-Repo)

## Was dieses Artefakt ist

Ein Foundation Brief ist ein menschenlesbarer Pre-Spec-Zielvertrag: Er
beschreibt für ein komplexes OpenSpec-Vorhaben das **Soll** (Zielbild) so
konkret, dass `$openspec-map` und `$openspec-propose` später nicht raten
müssen, welche Prompt-, Runtime- und Architektur-Wahrheit gemeint ist.

Abgrenzung zu verwandten Artefakten:

| Artefakt | Frage | Wahrheitsklasse |
|---|---|---|
| Stage-Datenfluss-Brief (`documentation`-Skill) | Was **ist** belegt? | `current_runtime_evidence` |
| **Foundation Brief (diese Vorlage)** | Was **wollen wir bauen**? | `target_contract` / `proposed_shape` |
| OpenSpec-Artefakte (`proposal/design/specs/tasks`) | Was wird **verbindlich umgesetzt**? | Bauwahrheit nach Propose |

## Wann ein Foundation Brief entsteht

Der Test ist semantisch, keine Keyword-Liste:

- **Pflicht** (Gate in `$openspec-map`): Das Vorhaben erzeugt einen neuen
  GTM-Runtime-Stage-Ordner oder schneidet einen bestehenden Stage-/Substage-
  Zuschnitt strukturell um — im Sinne von Section 95
  (`docs/architecture/sections/95-gtm-stage-prompt-runtime-contract-boundaries.md`).
- **Empfohlen** (Angebot in `$openspec-explore`): Prompt-Wahrheit und
  Runtime-Wahrheit müssen zusammenpassen; Handoff oder Trace ist kritisch;
  Must-Survive-Facts, Quality Gates oder Evidence-Pflichten sind zentral; ein
  späterer Builder könnte aus Chat allein falsche Defaults ableiten.
- **Nicht verwenden** für kleine OpenSpec-Fixes, Einzeldatei-Änderungen oder
  Vorhaben, deren Zielpfade und Tests bereits offensichtlich sind.

Vor dem Schreiben gilt das Drei-Körbe-Klärungsprotokoll aus
[`openspec-foundation-grilling.md`](../references/openspec-foundation-grilling.md):
Annahmen-Paket zuerst, dann Grill-Fragen in Abhängigkeitsreihenfolge, alles
markiert im Brief persistiert. Ein Foundation Brief wird nie still
auto-generiert.

## Lebenszyklus und Bindungsregel (Vierte-Wahrheit-Schutz)

Diese Regeln sind Pflichtinhalt jedes Briefs (eigene Sektion, siehe Skeleton):

1. Der Brief ist autoritativ **nur bis** `$openspec-propose` die
   Change-Artefakte erzeugt hat. Danach sind `proposal.md`, `design.md`,
   specs, `tasks.md`, `prompt-contracts/` und `quality-gates.md` die
   Bauwahrheit; der Brief wird Provenienz (`## Source foundation` in
   `proposal.md` verlinkt ihn als `primary_foundation`).
2. Widerspricht der Brief später den OpenSpec-Artefakten, gewinnen die
   Artefakte. Der Widerspruch ist ein Drift-Fund, kein Wahlrecht.
3. Der Brief darf kanonische Regeln wiederholen, aber jede wiederholte Regel
   braucht Quelle plus Provenienzklasse in der Quellen-Tabelle. Ein pauschaler
   Self-contained-Anspruch ohne benannte Quellen-Gegenliste ist verboten.
4. Gates, die der Brief formuliert, sind Quality-Gate-**Kandidaten**
   (Vokabular aus `../references/openspec-quality-gates.md`), die
   `$openspec-propose` nach `quality-gates.md` materialisiert — nie eine
   eigene dauerhaft bindende Gate-Wahrheit neben der Runtime-Validation.
5. Die Statuszeile "Zielbild, nicht aktuelle Runtime-Wahrheit" direkt unter
   dem H1 ist Pflicht.

## Pflicht-Frontmatter

```yaml
---
date: "YYYY-MM-DD"
kind: "artifact"
topic: "<kebab-slug>-zielbild"
status: "zielbild_draft | zielbild_reviewed"
provenance_class: "target_contract"
binding_status: "pre_spec_zielbild"
depends_on:
  - "<pfad zu quellen, vorlagen, vorgaenger-artefakten>"
target_next_skills:
  - "openspec-map"
  - "openspec-propose"
resulting_openspec_change: "none_yet"
---
```

`resulting_openspec_change` ist ein statischer Backlink: `$openspec-propose`
trägt hier den Change-Namen ein, sobald die Artefakte existieren. Der Wert
veraltet nie, weil er kein Status ist — der Umsetzungsstand lebt in datierten
Einträgen im `## OpenSpec-Rückkanal` (siehe Aufbau) und in `openspec list`.

Kein neues Vokabular erfinden: `provenance_class` und die Klassen-Tabelle
unten sind das bestehende Set; `binding_status` folgt der GTM-Prompt-Konvention
(`proposed` für Prompt-Contracts im Brief).

Optionales Feld `extends:`: Liste fachlicher Erweiterungs-Vorlagen (Vertrag
und Referenzbeispiel unter `## Projekt-Erweiterungen`), die der Brief-Autor
vor dem Schreiben gelesen haben muss. Kein Validator-Zwang — der Wert macht
die genutzte Erweiterung nur maschinenlesbar sichtbar.

## Provenienzklassen

Jede konkrete Aussage über Datenmodelle, LLM-Sicht, Runtime-Kontext, Handoffs
oder Downstream-Verhalten bekommt eine Klasse. JSON-/Prompt-Beispiele ohne
echten Run-Nachweis werden ausdrücklich markiert.

| Klasse | Bedeutung |
|---|---|
| `current_runtime_evidence` | aktive Runtime, aktueller Contract, aktueller Prompt, echtes Trace-Artefakt |
| `target_contract` | gewünschter neuer Vertrag für das Zielbild |
| `proposed_shape` | Vorschlag, noch nicht als Vertrag entschieden |
| `llm_visible_contract` | Daten, die ein Modell wirklich im Prompt sehen soll |
| `runtime_only_context` | Daten, die nur Runtime/Orchestrierung nutzt |
| `downstream_decision` | Entscheidung, die eine spätere Stage/Komponente trifft |
| `example_only` | erklärendes Beispiel, keine beobachtete Wahrheit |
| `n8n_prior_art` | alter Workflow-Vorläufer oder daraus abgeleitete Vorarbeit (nur wenn relevant) |

## Kanonische Entscheidungs-Marker

Offene und angenommene Punkte verwenden ausschließlich diese Marker, damit das
CEO-Decision-Gate von `$openspec-propose` sie mechanisch findet:

| Marker | Bedeutung |
|---|---|
| `clarify_first` | Simon muss vor dem Proposal entscheiden |
| `map_first` | erst Source-/Target-Inventur nötig |
| `cto_first` | erst CTO-Review nötig |
| `BD-*` | nummerierte Blocking Decision |
| `assumed_default` | Korb-2-Annahme aus dem Grilling-Protokoll: als gegeben angenommen, mit Ein-Satz-Begründung, vetofähig |

## Aufbau: Erzählbogen statt Formular

Die Reihenfolge ist Absicht: **erst verstehen, dann die Substanz, dann die
Entscheidungslage, dann Belege und Verwaltung.** Buchhaltung (Quellen,
Lebenszyklus, Handoff, Rückkanal) gehört ans Ende, nie vor die Geschichte —
ein Leser, der nach drei Sektionen noch nicht weiß, was gebaut werden soll,
liest ein Formular, kein Zielbild.

**Block 1 — Verstehen (immer Pflicht):**

1. **Frontmatter + Statuszeile** — wie oben; unter dem H1 die Zeile
   `> Status: Zielbild, nicht aktuelle Runtime-Wahrheit.`
2. **In einem Satz** — Vorher/Nachher: Was weiß das System vorher, was nachher?
3. **Ausführliche Beschreibung** — in Simons Sprache; W-Fragen beantworten
   (was wird verwandelt, warum, wer nutzt den Output, welche Entscheidung
   fällt hier, welche ausdrücklich nicht).
4. **Scope, Nicht-Scope und Wirkung** — "Was dieses Vorhaben ausdrücklich
   nicht macht" ist Pflicht. Wenn das Vorhaben einem größeren Produkt/Ziel
   dient, zusätzlich die Wirkungstabelle (Vorbild "Beitrag zum
   GTM-Audit-Report" in Datei 9): Frage des Gesamtprodukts | Beitrag dieses
   Vorhabens | Muss als Fakt überleben? — sie begründet später die
   Must-Survive-Facts und entlarvt Scope-Schleichwege.
5. **Heutiges Äquivalent / Prior Art** — was existiert, was ist gut, was ist
   überholt, was ist wiederverwendbar (Urteils-Spalte Pflicht).

**Block 2 — Substanz (Module, semantisch getriggert):**

6. **Modul LLM/Prompt** und/oder **Modul Runtime-Stage** — siehe unten. Hier
   lebt das eigentliche Zielbild: Zuschnitt, Datenmodell, Prompts, Handoff,
   Fehlerfälle.

**Block 3 — Entscheidungslage:**

7. **Als gegeben angenommene Punkte** — Korb-2-Liste aus dem
   Grilling-Protokoll, jede Annahme mit `assumed_default` + Ein-Satz-Begründung.
8. **Geklärte und offene Entscheidungen** — geklärte Festlegungen als Liste
   (Vorbild: "Geklärte First-Build-Entscheidungen" in Datei 9); offene Punkte
   mit kanonischen Markern.

**Block 4 — Belege und Verwaltung:**

9. **Quellen mit Provenienzklassen** — Tabelle: Quelle, Klasse, was sie belegt.
10. **Lebenszyklus dieses Briefs** — die Bindungsregeln aus dem Abschnitt oben,
    im Brief wiederholt.
11. **Map-/Propose-Handoff** — im bestehenden Skillketten-Vokabular: zu
    lesende Quellen, target path families, `quality_gates.status`,
    `builder_plan_status`, erwartete OpenSpec-Artefakte, nächster Skill;
    optional **Builder-Hinweise** (was der Builder nicht anfassen oder umbauen
    darf, bevor X steht; bekannte Verwechslungsgefahren — Vorbild "Prompting-
    und Builder-Hinweise" in Datei 9).
12. **OpenSpec-Rückkanal** — datierte Status-Einträge, nur anhängen, nie
    umschreiben: Brief erstellt, Final-Lücken-Pass, Proposal erzeugt
    (`$openspec-propose` setzt zusätzlich `resulting_openspec_change`),
    Verify abgeschlossen, archiviert. Wenn Simon einen resultierenden Change
    bewusst verwirft, abbricht oder durch einen anderen Change ersetzt, bekommt
    der Brief ebenfalls einen datierten Eintrag mit Grund und neuer Quelle der
    Wahrheit. Kein Live-Status-Feld — datierte Schnappschüsse können nicht
    lügen; lebende Wahrheit bleibt `openspec list`.

## Modul LLM/Prompt (Pflicht, sobald Prompt-Wahrheit betroffen ist)

- Prompt Contracts nach `services/gtm-agents/prompts/PROMPT-FILE-CONVENTION.md`:
  System Prompt und User Prompt Template als eine semantische Einheit,
  Output-JSON **inline im User Prompt**, Frontmatter mit `operation_id`,
  `llm_route`, `llm_provider`, `llm_model`, `llm_model_source`,
  `runtime_validation_strictness`, `prompt_language: en` und
  `binding_status: proposed`.
- **Kanonische Block-Form pro Operation** (exakt die Form, die `$openspec-map`
  4.4 als Prompt-Contract extrahiert und `validate_prompt_fidelity.py` später
  gegen den Build prüft — wer hier frei formatiert, verliert die mechanische
  Prüfkette):

  ````markdown
  ### Prompt <stage-op>: <sprechender Name> (`NNN-<operation>.md`)

  ```yaml
  operation_id: <stage>/<op-slug>
  llm_route: ...
  input_context_blocks: [...]
  ```

  # System Prompt

  [vollständiger Wortlaut]

  # User Prompt

  [vollständiger Wortlaut, $variablen aus input_context_blocks,
   Output-JSON inline am Ende]
  ````
- Beispielwerte in Prompts sind `example_only`.
- Modellroute und Sprache begründen, wenn sie vom Standard abweichen.
- **Validator-Regel (Prompt-Vollständigkeit):** Jede deklarierte Operation
  braucht den vollständigen System- und User-Prompt-Wortlaut inklusive
  Output-JSON inline. Fehlender Wortlaut ist ein Validator-Error — außer der
  Block trägt explizit `clarify_first` oder einen `BD-*`-Marker, dann nur
  Warning. `$variablen` im User Prompt müssen die `input_context_blocks`
  abdecken.
- **Prompt-Request-Paritäts-Hinweis (Pflichttext im Modul):** Der Brief-Prompt
  ist Zielvertrag; erfüllt ist er erst, wenn die Runtime den gerenderten
  System- und User-Prompt nachweisbar in den effektiven Provider-Request
  transportiert (`effective_provider_request`, siehe Section 95 und
  `../references/openspec-prompt-request-parity.md`).

## Modul Runtime-Stage (Pflicht, sobald Runtime-Wahrheit betroffen ist)

Sobald Input, Output, Handoff, Validation, Trace oder Replay einer
Runtime-Stage betroffen sind, ist dieses Modul **nicht optional**:

- **Drei-Wahrheiten-Zuordnung** — jede Aussage eindeutig Prompt-, Runtime-
  oder Architektur-Wahrheit zuordnen (`gtm-stage-authoring.md`).
- **Operation-/Substage-Zuschnitt** — Tabelle: Substage, Aufgabe, LLM oder
  deterministisch, Modell/Provider, Begründung; bei Stages zusätzlich
  Trace-/Display-Namensvertrag mit Kanon-Klausel (Pflichtsatz): Der
  Namensvertrag dieses Briefs ist der Slug-Kanon; abweichende IDs in
  Prompt-Contracts, Runtime- oder Architektur-Pfaden sind Drift-Funde, keine
  Wahlfreiheit.
- **Ziel-Datenmodell, kommentiert** — das Herzstück für JSON-Vertragstreue
  (Vorbild "Ziel-Datenmodell" in Datei 9): `jsonc`-Block, jedes Feld mit
  Kommentar zu Quelle (welche Substage/Komponente liefert es), Zweck und
  Verboten ("darf von X nicht ausgetauscht werden"); Werte als `example_only`.
  Dazu **Bewusste Nicht-Felder**: was absichtlich NICHT im Modell ist und
  warum — sonst füllt ein Builder die Lücke mit eigener Fantasie.
- **Runtime-Contract-Zielbild als Rollen** — Contract-, Gates-, Replay-,
  Trace- und Test-Rollen müssen adressiert sein. `contract.ts` ist der
  bevorzugte Zielname; bewusste Bündelung ist erlaubt, muss aber benannt und
  begründet werden (exakt die Section-95-Formel: auffindbar, getestet,
  dokumentiert).
- **Must-Survive-Facts** — welche Fakten dürfen nicht verloren gehen (wenn die
  Wirkungstabelle aus Sektion 4 existiert, speist ihre "Muss als Fakt
  überleben?"-Spalte diese Liste).
- **Handoff und Downstream-Leser** — wer liest was, in welcher Form.
- **Trace, Evidence, Persistence, Replay** — welche Artefakte den Lauf
  beweisen, von wo Replay starten darf.
- **Fehlerfälle und Stop-Regeln** — Tabelle: was kann schiefgehen, woran merkt
  man es, Stop/Warnung/Review.
- **Deprecation, Limits und Cleanup** — welche aktiven Pfade (Architektur,
  Prompts, Runtime) das Zielbild ersetzt und datiert nach
  `_deprecated/YYYY_MM_DD__<relativer_pfad>` archiviert; jede zurückgeholte
  Alt-Logik braucht eine Begründung, warum sie in den neuen Schnitt passt.
  Dazu System- und Budget-Limits als explizite Vertragswerte (Vorbild
  `stage00PdfCaptureLimit = 10` in Datei 9), nie als stilles
  Implementierungsdetail.
- **Wer entscheidet dieses Feld wirklich?** — Feld, Eigentümer,
  Provenienzklasse, Quelle. Kein Feld ohne Erzeuger: Jedes Feld des
  Ziel-Datenmodells und des Handoffs muss hier mit einer produzierenden
  Substage/Komponente auftauchen; ein Feld, das niemand erzeugt, ist ein
  Drift-Fund, kein Gestaltungsspielraum. Jedes Enum wird genau einmal
  definiert und anderswo nur referenziert — kein zweites Vokabular für
  dasselbe semantische Urteil (Lektion aus dem `url_evidence_map`-Doppler,
  CEO-Entscheidung 2026-06-10).

## Projekt-Erweiterungen

Diese generische Vorlage ist der Sicherheitsvertrag (Lebenszyklus,
Eigentümer-Tabellen, Prompt-Vollständigkeit, Validator). Was ein Brief
**fachlich** enthalten muss, definiert pro Projekt eine
Erweiterungs-Vorlage. Für Erweiterungen gilt dieser Vertrag:

- Erweiterungen **ergänzen** fachliche Pflichtquellen, Pflichtsektionen und
  Skeleton-Bausteine; sie **überschreiben nie** Lebenszyklus,
  Sicherheitsregeln oder Validator-Pflichten dieser generischen Vorlage.
- Erweiterungen leben **im Repo** (z. B. unter
  `docs/architecture/**/templates/`), nie im Shared-Skill-Ordner —
  Projektwissen gehört ins Projekt, Skill-Mechanik in den Skill.
- Auffindbarkeit ist Pflicht des Projekts: Die Erweiterung wird aus den
  Sitzungs-Instruktionen (`AGENTS.md`, von `CLAUDE.md` importiert) und aus den
  Architektur-Entrypoints des Repos referenziert, nicht nur aus
  Konversations-Gedächtnis.
- Briefe deklarieren genutzte Erweiterungen im Frontmatter unter `extends:`.
  Eine deklarierte oder vom Projekt vorgeschriebene Erweiterung ist
  verbindlich: Der Brief-Autor liest sie vor dem Schreiben und erfüllt ihre
  Pflichtquellen und Pflichtsektionen. Der Validator prüft nur die
  generischen Regeln — fachliche Dünne fängt nur die Erweiterung.

Referenzbeispiel: Für GTM-Stage-Zielbilder (Sanctum-OS) gilt die promotete
Vorlage `docs/architecture/stages/templates/gtm-stage-zielbild-brief-template.md`
(Report-Rückwärts-Linse, N8N-Pflichtauswertung, Beispielreport-Abgleich;
historische Herleitung im Tagesraum-Artefakt `005` vom 2026-06-04). Die
generische Wirkungstabelle in Sektion 4 ist nur ihr schlanker Kern.

## Skeleton

````markdown
---
date: "YYYY-MM-DD"
kind: "artifact"
topic: "<slug>-zielbild"
status: "zielbild_draft"
provenance_class: "target_contract"
binding_status: "pre_spec_zielbild"
depends_on:
  - "<quelle>"
target_next_skills:
  - "openspec-map"
resulting_openspec_change: "none_yet"
---

# Zielbild: <sprechender Name>

> Datei: `<pfad>`
> Status: Zielbild, nicht aktuelle Runtime-Wahrheit.

## In einem Satz

<Vorhaben> macht aus [Input-Welt] [Output-Welt].

Vorher weiß das System: "[konkreter Vorher-Satz]"

Nachher weiß das System: "[konkreter Nachher-Satz]"

## Ausführliche Beschreibung

[Einfache Sprache. W-Fragen beantworten.]

## Scope, Nicht-Scope und Wirkung

[Was gehört dazu. Was dieses Vorhaben ausdrücklich nicht macht.]

[Optional, wenn Teil eines größeren Produkts/Ziels:]

| Frage des Gesamtprodukts | Beitrag dieses Vorhabens | Muss als Fakt überleben? |
|---|---|---|
| [TBD] | [TBD] | ja/teilweise/nein |

## Heutiges Äquivalent und Prior Art

| Heutige Quelle | Was daran gut ist | Was überholt ist | Wiederverwendbar? |
|---|---|---|---|
| [pfad] | [TBD] | [TBD] | ja/nein/teilweise |

## Modul LLM/Prompt (nur wenn Prompt-Wahrheit betroffen)

Quelle: `target_contract`.

[Pro Operation ein Block in kanonischer Form: ### Prompt-Überschrift mit
Ziel-Dateiname, Frontmatter-Ziel als yaml, # System Prompt, # User Prompt mit
$variablen und Output-JSON inline. Beispiele als example_only.
Prompt-Request-Paritäts-Hinweis nicht vergessen.]

## Modul Runtime-Stage (nur wenn Runtime-Wahrheit betroffen)

Quelle: `target_contract`.

[Drei-Wahrheiten-Zuordnung.]

### Substage-Zuschnitt und Tool-Wahl

Quelle: `target_contract`.

| Substage | Aufgabe | LLM oder deterministisch? | Modell/Provider | Begründung |
|---|---|---|---|---|
| `op-slug` | [TBD] | [TBD] | [TBD oder n/a] | [warum diese Kombination] |

[Bei Stages zusätzlich der Trace-/Display-Namensvertrag. Kanon-Klausel: Dieser
Namensvertrag ist der Slug-Kanon; abweichende IDs in Prompt-Contracts,
Runtime- oder Architektur-Pfaden sind Drift-Funde, keine Wahlfreiheit.]

### Ziel-Datenmodell

Quelle: `proposed_shape`.

```jsonc
{
  "feld": "example_only"
  // Quelle: [wer liefert es]. Zweck: [wozu]. Verbot: [wer darf es nicht ändern].
}
```

Bewusste Nicht-Felder:

- [Feld, das absichtlich fehlt] — [warum]

### Wer entscheidet dieses Feld wirklich?

Kein Feld ohne Erzeuger; Enums genau einmal definiert, sonst nur referenziert.

| Feld | Eigentümer (Substage/Komponente) | Provenienzklasse | Quelle |
|---|---|---|---|
| [feld] | [TBD] | [TBD] | [TBD] |

### Deprecation, Limits und Cleanup

Quelle: `target_contract`.

- Deprecated Pfade:
  - [aktiver Alt-Pfad] -> `_deprecated/YYYY_MM_DD__<relativer_pfad>` — [Grund]
- Zurückgeholte Alt-Logik:
  - [Logik] — [warum sie in den neuen Schnitt passt]
- System- und Budget-Limits:
  - [Limit-Name] = [fester Wert] — [was bei Überschreitung sichtbar passiert]

### Contract-Rollen, Must-Survive, Handoff, Fehlerfälle

[Contract-/Gates-/Replay-/Trace-/Test-Rollen, Must-Survive-Facts, Handoff und
Downstream-Leser, Fehlerfälle-und-Stop-Regeln-Tabelle.]

## Als gegeben angenommene Punkte

- `assumed_default`: [Annahme] — [Ein-Satz-Begründung]

## Geklärte und offene Entscheidungen

Geklärt:

- [Festlegung mit Datum]

Offen:

- `clarify_first`: [Punkt, den Simon entscheiden muss]

## Quellen

| Quelle | Klasse | Was sie belegt |
|---|---|---|
| [pfad] | current_runtime_evidence | [TBD] |
| [pfad] | target_contract | [TBD] |

## Lebenszyklus dieses Briefs

Dieser Brief ist autoritativ nur bis `$openspec-propose` die Change-Artefakte
erzeugt hat. Danach sind die OpenSpec-Artefakte die Bauwahrheit; dieser Brief
wird Provenienz. Bei Widerspruch gewinnen die OpenSpec-Artefakte; der
Widerspruch ist ein Drift-Fund. Wiederholte kanonische Regeln sind in der
Quellen-Tabelle belegt.

## Map-/Propose-Handoff

- Zu lesende Quellen: [liste]
- Target path families: [liste]
- `quality_gates.status`: none | candidates | clarify_first | map_first
- `builder_plan_status`: not_required | recommended | required
- Erwartete OpenSpec-Artefakte: [proposal/design/specs/tasks/prompt-contracts/quality-gates/builder-plan]
- Builder-Hinweise: [optional — was nicht angefasst werden darf, Verwechslungsgefahren]
- Nächster Skill: `$openspec-map <pfad zu diesem Brief>`

## OpenSpec-Rückkanal

- Stand YYYY-MM-DD: Brief erstellt (Grilling: X Annahmen, Y geklärte Fragen).
````

## Qualitätsregeln

- Erst Quellen lesen und das Grilling-Protokoll durchlaufen, dann schreiben.
- Erzählbogen einhalten: Verwaltungssektionen (Quellen, Lebenszyklus, Handoff,
  Rückkanal) nie vor die Substanz ziehen.
- Module sind semantisch getriggert (welche Wahrheitsebene wird verändert?),
  nicht über Keyword-Listen.
- LLM-visible, runtime-only, trace-only und downstream-only strikt trennen.
- Keine synthetischen JSON-Beispiele als beobachtete Wahrheit ausgeben.
- Jede Contract-Sektion beginnt mit `Quelle: <klasse>`.
- **Tabellen entscheiden, sie listen nicht nur auf:** jede Tabelle braucht
  eine Urteils-Spalte (`Muss als Fakt überleben?`, `Stop/Warnung/Review?`,
  `Wiederverwendbar?`, `Darf nicht ersetzt werden durch`) und einen Satz
  davor, der sagt, was sie entscheidet.
- **Kein Feld ohne Erzeuger, kein Doppel-Vokabular:** jedes Feld in
  Ziel-Datenmodell und Handoff hat eine Zeile in der Feld-Eigentümer-Tabelle;
  Enums werden genau einmal definiert und sonst nur referenziert — ein zweites
  Vokabular für dasselbe semantische Urteil ist ein Drift-Fund.
- Vor dem Handoff den Validator laufen lassen:
  `python3 ~/.codex/skills/shared/scripts/validate_foundation_brief.py <brief-pfad>`
