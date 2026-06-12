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
4. Baseline: A aus dem Quellblock ausführen oder klar als Fixture vorbereiten.
5. Variant: B mit genau einem Lever bilden.
6. Round Evidence: Requests ohne Secrets, gerenderte Prompts, Raw Response,
   Response Text, Parsed Output und Metrics schreiben.
7. Review-Dimensionen: Standardachsen und rundenbezogene Fokusmetriken im Chat
   vorschlagen. Erst nach Simons Zustimmung als `assistant_review` mit
   Begründung speichern. Feedbackpunkte als `must_survive`, `must_reject`,
   `evaluation_focus` oder `investigation_question` in den Iterationspfad
   übernehmen.
8. Review Surface: `html/assets/data.json` erzeugen und mit der Shared
   Prompt A/B Review Surface rendern.
9. Browser-Handoff: Simon fragen, ob die HTML geöffnet werden soll. Unter WSL2
   an Windows-Firefox immer einen `file://///wsl.localhost/<distro>/...`-URI
   übergeben, nicht den rohen UNC-Pfad.
10. HITL: Simon entscheidet Promote, Iterate, Change Lever, Split, Reject oder
   Inconclusive.
11. Chaining: Downstream nur nach upstream Approval, mit frozen
   `chained_fixture`; final zusätzlich Live-Kettenlauf.
12. Write-back: Approved fenced block deterministisch in die Quelle schreiben.

## HTML in Windows-Firefox öffnen

Wenn Codex in WSL2 läuft und Simon in Windows 11 arbeitet, muss die lokale HTML
als Windows-Datei-URI geöffnet werden:

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

Nach jedem erfolgreichen Render der Review-Oberfläche fragt der Skill Simon:

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
- Must-Survive-Facts verloren gehen.
- Perplexity/Search ohne Raw Response, parsed Output und Validation bewertet
  wird.
- Class-C-Felder geändert werden müssten.
- Der Write-back-Diff außerhalb des Zielblocks Änderungen zeigt.
- Upstream nach Downstream Approval neu geschrieben wurde; downstream ist dann
  `stale`.
