---
name: openspec-skill-backup
version: "1.0.1-sanctum"
bundle: openspec-simon
bundle_version: "2026.06.11.3"
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
   bundle version, next bundle version and concrete changed/missing/stale files.
   If `action_needed=none`, explain that local source, local fork snapshot and
   remote branch are already aligned enough for backup purposes. Do not stage or
   commit during preview.

2. **Apply the snapshot when Simon wants the backup prepared**

   ```bash
   python3 ~/.codex/skills/openspec-skill-backup/scripts/backup_openspec_skill_bundle.py apply
   ```

   Only apply when preview says `action_needed=apply_backup` or Simon explicitly
   wants a new snapshot anyway. This updates `bundle_version` in the source skill
   frontmatter, recalculates checksums, writes
   `~/.codex/skills/shared/openspec-simon-bundle.json`, and refreshes
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

4. **Commit and push only after explicit approval**

   Follow the `smart-commit` safety contract. Do not use broad staging shortcuts
   like `git add .` or `git add -A`.

   Stage exact changed files under `simon-skills/`, then commit:

   ```text
   chore(skills): backup OpenSpec Simon bundle <bundle_version>
   ```

   Push only after Simon explicitly approves push in the current conversation.

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
- Keep individual `version:` fields per skill; do not bump them unless the
  skill itself changed semantically.
