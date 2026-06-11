# Target Discovery

Use Smart-Commit-style discovery before expensive review work.

## Input Modes

Argument as path:

- accept absolute paths;
- accept repo-relative paths;
- support `openspec/changes/<change>/`;
- support `openspec/changes/archive/YYYY-MM-DD-<change>/`.

Argument as CTO Review memo:

- if the target is recognizably a CTO Review memo, set mode
  `foundation-cto-review`;
- strong signals are `_cto-review_` in the filename, `type: cto-review` in
  frontmatter, or a clear CTO Review title/path;
- if Simon gives only a filename, find the matching file in the repo and prefer
  `docs/todo/**`;
- ask Simon only when the target file is missing or ambiguous;
- never ask which review mode to use once the target is recognizably a CTO
  Review.

Argument as foundation artifact:

- if the target is recognizably a pre-OpenSpec target-contract artifact, set
  mode `foundation_artifact_review`;
- strong signals are `docs/todo/**/03_artifacts/`, `__artifact__` in the
  filename, `kind: artifact`, or `provenance_class: target_contract` in
  frontmatter;
- read `references/foundation-artifact-review.md` before reviewer judgment;
- route plain research notes, reflections, or weak drafts without
  target-contract polarity to `sherlock-review` instead.

Argument as name:

1. exact active: `openspec/changes/<name>/`;
2. exact archived suffix: `openspec/changes/archive/*-<name>/`;
3. fuzzy active;
4. fuzzy archived.

No argument:

- scan active and archived OpenSpec folders;
- group related candidates;
- show preview;
- ask Simon when more than one plausible target exists.

## Candidate Groups

- `single_change`: one active or archived change.
- `active_archive_pair`: active change plus similar archived predecessor.
- `wave_series`: multiple changes with common stage, wave, date, or source-map pattern.
- `spec_cluster`: multiple changes touching the same `specs/<capability>/spec.md`.
- `dirty_related`: active change plus uncommitted files from `git status --short`.
- `cto_review`: one CTO Review memo detected from the target name, path, or content.
- `foundation_artifact`: one pre-OpenSpec target-contract artifact detected
  from the target path, filename, or frontmatter.

## Preview Contract

Show:

- candidate id;
- kind;
- exact paths;
- artifacts found;
- risk note;
- recommendation;
- whether a Red Review already exists.

For `cto_review` candidates also show, when quickly visible:

- source memo path;
- `spec_mode_status`;
- `target_openspec_change`, if present;
- obvious open `BD-*` or Rückkanal status.

For `foundation_artifact` candidates also show, when quickly visible:

- source artifact path;
- `provenance_class`;
- `status`;
- `carry_forward_from` and `depends_on` count;
- obvious target OpenSpec or stage scope.

Never auto-select when multiple plausible candidates exist.

Discovery is read-only: no git staging, no archive moves, no spec sync, no external writes.
