# OpenSpec Prompt Optimizer Workflow

## Eingang

Der Eingang ist ein Foundation Brief oder Pre-Spec-Zielbild mit kanonischen
fenced Prompt-Contract-Blöcken:

```text
YAML frontmatter with operation_id
# System Prompt
# User Prompt
```

Die Quelle ist `target_contract`, nicht aktuelle Runtime-Wahrheit. Der Skill
optimiert diesen Zielvertrag, bevor OpenSpec daraus Bauwahrheit macht.

## Kampagne

Eine Kampagne liegt im aktiven Tagesraum unter `07_experiments/`:

```text
NNN_openspec-prompt-optimization-<slug>__YYYY_MM_DD__HH-MM/
  campaign-state.json
  00_prompt-optimization-overview.md
  01_prompt-scope-register.md
  02_operation-profiles/
  03_rounds/
  04_hitl-decisions.md
  05_writeback/
  06_open-issues.md
  html/
```

`campaign-state.json` ist der Resume-Spiegel. Markdown bleibt die menschliche
Wahrheit.

## Phasen

1. Intake: Foundation Brief laden und Prompt-Blöcke mechanisch entdecken.
2. Scope Register: Operationen leicht klassifizieren, noch kein Deep Audit.
3. Operation Profile: Für ausgewählte Operationen Inputs, Outputs, Provider,
   Must-Survive-Facts und Risiken erfassen.
4. Preflight: Für gerenderte Baseline- und Kandidatenprompts
   `preflight_prompt_contract.py` ausführen. Provider-Fit, Einfachheit,
   Anti-Overfit-/Hardcoding-Risiken und Generalisierungsevidence werden als
   Review-Evidence gespeichert, nicht als automatische Entscheidung.
5. Baseline: A aus dem Quellblock ausführen oder klar als Fixture vorbereiten.
6. Variant: B mit genau einem Lever bilden.
7. Round Evidence: Requests ohne Secrets, gerenderte Prompts, Raw Response,
   Response Text, Parsed Output und Metrics schreiben.
8. Review-Dimensionen: Standardachsen und rundenbezogene Fokusmetriken im Chat
   vorschlagen. Erst nach Simons Zustimmung als `assistant_review` mit
   Begründung speichern. Feedbackpunkte als `must_survive`, `must_reject`,
   `evaluation_focus` oder `investigation_question` in den Iterationspfad
   übernehmen.
9. Review Surface: `html/assets/data.json` erzeugen. Diese Datei ist der
   gemeinsame Datenvertrag für die kanonische React-Route
   `/app/review/prompt-ab?path=...` und optionale statische Snapshots. Die
   Daten müssen den gemeinsamen
   Review-Contract befüllen, soweit Evidence vorhanden ist:
   `goalProgress`, `overallAnalysis`, `decisionScorecard`,
   `assistant_recommendation`, `metricMatrix`, `decisionMetrics`,
   `interpretationNotes`, `traceIntegrity`, `hitlDecision`, `preflightChecks`,
   `assistantEvaluation`, `iterationPath`, `testIntent` und
   `cases[].testIntent`.
   `decisionMetrics` muss aus `metricMatrix`, Provider-Metriken und
   Trace-Artefakten renderbar sein; rundenlokale Enrichment-Skripte dürfen
   nur optionale bessere Texte nachliefern.
   `goalProgress` formuliert Ziel, Fortschritt, offenen Abstand zum Endziel
   und nächsten Schritt. `interpretationNotes[case-id]` formuliert die
   caseweisen Entscheidungsfragen für die Chat-Auswertung.
   `cases[].testIntent` formuliert vor der Auswertung, was der Case prüfen
   soll, welches Verhalten erwartet wird und woran die Variante scheitern
   würde. Der Gegencheck kommt aus Parsed Output, Metrics und Trace, nicht aus
   frei geschriebener Review-Prosa.
   `assistant_recommendation` ist neutral und kann auch A behalten, alle
   Varianten ablehnen oder `inconclusive` melden; Promotion bleibt HITL.
10. Browser-Handoff: Wenn der Sanctum-Dev-Server verfügbar ist, primär die
   React-Route öffnen:
   `/app/review/prompt-ab?path=<urlencoded relative path to html/assets/data.json>`.
   Eine statische `html/index.html` nur als Export, Archiv oder Fallback
   rendern. Unter WSL2 an Windows-Firefox für statische Snapshots immer einen
   `file://///wsl.localhost/<distro>/...`-URI übergeben, nicht den rohen
   UNC-Pfad.
11. HITL: Simon entscheidet Promote, Iterate, Change Lever, Split, Reject oder
   Inconclusive.
12. Chaining: Downstream nur nach upstream Approval, mit frozen
   `chained_fixture`; final zusätzlich Live-Kettenlauf.
13. Write-back: Approved fenced block deterministisch in die Quelle schreiben.

## Review-Oberfläche öffnen

Der Primärpfad ist die React-Route:

```text
http://localhost:3000/app/review/prompt-ab?path=docs%2Ftodo%2F...%2Fhtml%2Fassets%2Fdata.json
```

Diese Route liest denselben `html/assets/data.json`-Vertrag wie der statische
Export. Dauerhafte Änderungen an Layout, Farben, Navigation, Collapse-Logik,
Metriken oder Interpretation müssen zuerst in dieser React-Oberfläche landen.
Die statische HTML darf danach als Archiv-/Offline-Snapshot nachgezogen werden.

## Statisches HTML in Windows-Firefox öffnen

Wenn Codex in WSL2 läuft und Simon in Windows 11 arbeitet, muss eine lokale
statische HTML als Windows-Datei-URI geöffnet werden:

```text
file://///wsl.localhost/Ubuntu/home/simon/projects/.../html/index.html
```

Dieser Pfad ist absichtlich nicht:

```text
https://wsl.localhost/Ubuntu/...
```

Und er ist auch nicht als rohes Firefox-Argument ausreichend:

```text
\\wsl.localhost\Ubuntu\home\...
```

Nach jedem erfolgreichen Render eines statischen Snapshots fragt der Skill
Simon:

```text
Soll ich die Review-Oberfläche in Windows-Firefox öffnen?
```

Bei Zustimmung:

```bash
python ~/.codex/skills/openspec-prompt-optimizer/scripts/open_review_surface.py \
  <round>/html/index.html \
  --browser firefox
```

## Stop-Regeln

Stoppe oder markiere `hold`, wenn:

- Provider-/Fixture-Evidence fehlt oder falsch gelabelt ist.
- B mehrere Levers zugleich ändert.
- Parsebare Outputs semantisch schlechter sind.
- Die Assistant Recommendation B bevorzugt, obwohl rote Guardrails blockieren.
- Ein roter Preflight-Fund vorliegt und weder behoben noch im Decision-Ledger
  ausdrücklich akzeptiert wurde.
- Eine mehrstufige Kampagne Generalisierung behauptet, aber keinen Eval-Hash,
  keine Train/Test-Trennung oder keine Mutation-History für verworfene
  Varianten ausweist.
- Must-Survive-Facts verloren gehen.
- Perplexity/Search ohne Raw Response, parsed Output und Validation bewertet
  wird.
- Class-C-Felder geändert werden müssten.
- Der Write-back-Diff außerhalb des Zielblocks Änderungen zeigt.
- Upstream nach Downstream Approval neu geschrieben wurde; downstream ist dann
  `stale`.
