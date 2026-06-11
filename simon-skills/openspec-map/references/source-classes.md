# Source Classes

Use source classes to prevent mixed-source confusion. Projects may add their
own labels, but these defaults should cover most OpenSpec mapping work.

| Class | Meaning |
|---|---|
| `active` | Current runtime or product code. Highest implementation truth unless superseded by a decision. |
| `architecture` | Architecture documentation, runtime flow docs, or system maps. |
| `decision` | ADR, daily decision file, CTO review decision, or explicit owner call. |
| `skill_control` | Goal Brief, Pre-Proposal Reading Contract, CTO Review backchannel note, Verify Review, CEO Review, or other skill artifact that controls workflow gates. |
| `specification` | Existing OpenSpec spec, external spec, API contract, or formal requirement. |
| `reference` | Helpful implementation reference that is not current runtime truth. |
| `archive` | Historical implementation or prior version. Must not be treated as active without confirmation. |
| `prior_art` | Comparable pattern, earlier artifact, or learning that informs design. |
| `template` | Reusable artifact shape, prompt template, component template, or skill template. |
| `trace` | Runtime output, log, replay, prompt, LLM response, screenshot, or evidence folder. |
| `test` | Existing test, fixture, golden, snapshot, or validator. |
| `research_note` | Investigation note, finding, or exploratory memo. |
| `external_doc` | Third-party documentation, library docs, cloud docs, or upstream reference. |
| `unknown` | Source exists but role is unclear. Use sparingly and explain in notes. |

## Rules

- Do not collapse `active`, `archive`, and `reference` into one bucket.
- If a source has not been opened, mark `read_status: not_read`.
- If a source path is guessed, mark it as an open question, not as evidence.
- If two sources disagree, surface the conflict in the consolidated briefing.
- For production logic, Git and real files outrank summary prose.
- Do not flatten `skill_control` artifacts into normal notes; preserve their
  gate or handoff role.
