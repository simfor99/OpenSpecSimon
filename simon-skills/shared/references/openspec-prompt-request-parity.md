# OpenSpec Prompt-Request-Parität

## Zweck

Dieses Gate verhindert, dass ein Prompt-Vertrag formal existiert, aber der
produktive Provider-Request einen Teil davon verliert oder Provider-interne
Rohdaten als unsere Prompt-Wahrheit erscheinen.

Dieses Gate prüft den Transport zum Modell oder Provider. Es prüft nicht, ob
die LLM-/Search-LLM-/Perplexity-/Provider-Rückgabe die im User Prompt
geforderte Datenform erfüllt. Für raw response, Provider-Envelope,
Normalisierung, parsed output, Runtime-Validatoren und downstream Handoffs gilt
zusätzlich
`/home/simon/.codex/skills/shared/references/openspec-llm-output-contract-testing.md`.

Die einfache Regel:

```text
Was im Prompt-Vertrag als System Prompt oder User Prompt definiert ist, muss im
effektiven Provider-Request nachweisbar transportiert werden.
```

Der zweite Grundsatz:

```text
Gespeichert und reviewbar sind unser effektiver Provider-Request und die
fachliche Modellantwort. Provider-interne Systeminstruktionen, interne
Modelllabels, Usage-Objekte oder Tool-Interna sind kein Produkt-Trace-Artefakt.
```

## Wann dieses Gate gilt

Aktiviere dieses Gate, wenn ein Change mindestens eine dieser Flächen berührt:

- LLM-, Model-, Agent- oder Provider-Aufrufe;
- Prompt-Dateien, Prompt-Verträge oder Prompt-Operation-Registries;
- GTM Stage Prompt-/Runtime-Handoffs;
- Model-Routing, Provider-Adapter, Tool-Aufrufe oder Trace-Artefakte;
- Review-UI oder Debug-Flächen, die Prompt-, Request- oder Raw-Response-Wahrheit
  anzeigen.

## Pflichtprüfung

Für jede betroffene Prompt-Operation muss Apply oder Verify nachweisen:

- Der Prompt-Vertrag wurde aus der maßgeblichen Quelle gelesen.
- Der gerenderte System Prompt und User Prompt wurden bestimmt.
- Der effektive Provider-Request wurde aus der aktiven Runtime oder einem echten
  Run-Artefakt belegt.
- Wenn der Vertrag einen System Prompt enthält, transportiert der Request ihn
  als Provider-System-/Instructions-Feld oder bewusst eingebettet im Input.
- Wenn der Vertrag einen User Prompt enthält, transportiert der Request ihn als
  User-/Input-Feld.
- Wenn ein Provider kein separates Systemfeld unterstützt, ist die Einbettung
  des System Prompts explizit, getestet und im Trace erkennbar.
- Provider-interne Instruktionen oder interne Modellnamen werden nicht als
  unsere Prompt-Wahrheit dargestellt.
- Provider-interne Instruktionen, interne Modelllabels, Usage-Objekte und
  Tool-Interna werden nicht als produktive Trace- oder Review-Artefakte
  persistiert.

## Evidence

Akzeptierte Evidence-Klassen:

- `runtime_code`: Request-Builder oder Provider-Adapter zeigt das Mapping.
- `rendered_prompt`: gerenderter System-/User-Prompt aus der Prompt-Operation.
- `effective_provider_request`: Request-Artefakt oder Testbeleg des tatsächlich
  gesendeten Provider-Requests.
- `trace_artifact`: Run-Artefakt, das Provider, Route, Prompttransport und
  fachliche Response sichtbar macht, ohne Provider-Rohrauschen zu speichern.
- `test_evidence`: Unit-, Integration- oder Stage-Test, der Prompt-Vertrag und
  effektiven Provider-Request vergleicht.

Nicht ausreichend:

- nur das Promptfile;
- die Raw Provider Response;
- nur ein grüner LLM-Output;
- nur ein Code-Suchtreffer;
- eine UI-Ansicht, die Provider-Rohfelder ungefiltert als Prompt-Wahrheit zeigt.

## Fail-loud-Regel

Ein Change darf nicht als fertig gelten, wenn ein Prompt-Vertrag System/User
definiert, der effektive Provider-Request aber einen Teil davon verliert oder
nicht beweist.

Wenn der Provider absichtlich anders transportiert, muss der Change diese
Transportentscheidung sichtbar machen und testen. Wenn das nicht möglich ist,
bleibt die Arbeit blockiert oder braucht eine Simon-Entscheidung.

## Minimaler Standard für neue GTM-Model-Calls

Jeder neue oder geänderte GTM-Model-Call braucht mindestens:

- ein `effective_provider_request`-Artefakt oder gleichwertige Test-Evidence;
- getrennte Felder für gerenderten System Prompt und User Prompt oder eine
  explizite, getestete Einbettungsstrategie;
- ein bereinigtes Model-Output-Artefakt mit fachlicher Antwort;
- einen Test, der verhindert, dass System Prompt, User Prompt oder
  Prompt-Slots im Request-Builder verloren gehen;
- einen Test oder Check, der verhindert, dass Provider-interne Rohdaten in
  produktive Trace-Artefakte geschrieben werden.
- wenn der User Prompt strukturierte Felder/JSON verlangt: einen separaten
  LLM-Output-Contract-Test, der raw provider response, Provider-Envelope oder
  Normalisierung, parsed output, Runtime-Validator und downstream Handoff gegen
  diesen Rückgabe-Vertrag prüft.
