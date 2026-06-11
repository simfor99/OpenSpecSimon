---
name: openspec-skill-backup
version: "1.0.2-sanctum"
bundle: openspec-simon
bundle_version: "2026.06.11.6"
description: "WHAT: Backs up Simon's Codex OpenSpec skill bundle to the OpenSpecSimon fork. WHEN: Use when OpenSpec skills changed and Simon wants preview, snapshot, commit, or push protection."
argument-hint: "preview | apply | commit | push | status [optional bundle version]"
disable-model-invocation: false
---

# OpenSpec Skill Backup

Back up Simon's active Codex OpenSpec skill chain from `~/.codex/skills` into
the `OpenSpecSimon` fork under `simon-skills/`.

This skill is self-referential: `openspec-skill-backup` is part of the backed-up
bundle and must travel with the other OpenSpec skills.

## When to Use

Use this skill when Simon says any of:

- "OpenSpec Skills sichern"
- "OpenSpec Backup"
- "Backup Skill laufen lassen"
- "push die OpenSpec Skills"
- "neue OpenSpec Skill-Version sichern"

Also use it after changing any of:

- `~/.codex/skills/openspec-*`
- `~/.codex/skills/openspec-skill-backup`
- OpenSpec-specific files in `~/.codex/skills/shared/`

## Process

1. **Preview first**

   ```bash
   python3 ~/.codex/skills/openspec-skill-backup/scripts/backup_openspec_skill_bundle.py preview
   ```

   Report `remote_status`, `source_vs_snapshot`, `action_needed`, current
   bundle version, next bundle version, concrete changed/missing/stale files,
   and the suggested commit message.

   If `action_needed=none`, explain that local source, local fork snapshot and
   remote branch are already aligned enough for backup purposes. Stop there.

   If `action_needed=apply_backup`, ask exactly one decision question:

   ```text
   Soll ich diesen Snapshot jetzt anwenden, validieren, committen und nach GitHub pushen?
   ```

   A user answer like "ja", "okay", "mach das" or "go" to that question is
   explicit approval for apply, exact-path staging, commit and push. Do not ask
   a second time before commit or push.

2. **After approval, run the complete backup**

   ```bash
   python3 ~/.codex/skills/openspec-skill-backup/scripts/backup_openspec_skill_bundle.py apply
   ```

   Only run this after the one decision question above was approved, or Simon
   explicitly requested a backup-and-push in the same message. This updates
   `bundle_version` in the source skill frontmatter, recalculates checksums,
   writes `~/.codex/skills/shared/openspec-simon-bundle.json`, and refreshes
   `/home/simon/projects/OpenSpecSimon/simon-skills/`.

3. **Validate after apply**

   ```bash
   python3 ~/.codex/skills/openspec-skill-backup/scripts/backup_openspec_skill_bundle.py status
   ```

   Confirm manifest validation and re-check `backup_status`. Also run a secret
   scan against the destination if available:

   ```bash
   gitleaks protect --staged --no-banner
   ```

   If nothing is staged yet, use repository hooks or `rg` fallback before
   committing. Treat false positives explicitly; never ignore real secrets.

4. **Commit and push under the single approval**

   Follow the `smart-commit` safety contract. Do not use broad staging shortcuts
   like `git add .` or `git add -A`.

   Stage exact changed files under `simon-skills/`, then commit with the
   suggested message from preview:

   ```text
   chore(skills): backup OpenSpec Simon bundle <bundle_version>
   ```

   Push in the same flow if the one approval question included "pushen" and
   Simon answered yes/okay/mach das.

## Resources

- Script: `scripts/backup_openspec_skill_bundle.py`
- Source root: `~/.codex/skills`
- Destination repo: `/home/simon/projects/OpenSpecSimon`
- Destination path: `/home/simon/projects/OpenSpecSimon/simon-skills`
- Manifest: `~/.codex/skills/shared/openspec-simon-bundle.json`

## Rules

- Canonical source is Codex: `~/.codex/skills`.
- Back up the seven active OpenSpec skills plus this backup skill.
- Include only the OpenSpec-specific shared files listed by the script.
- Exclude `__pycache__`, `.skill-forger-state`, transient caches and backups.
- Increment `bundle_version` on every applied snapshot.
- Preview must distinguish "next possible version" from "backup required".
- Ask only one approval question for apply+commit+push when backup is needed.
- Keep individual `version:` fields per skill; do not bump them unless the
  skill itself changed semantically.
