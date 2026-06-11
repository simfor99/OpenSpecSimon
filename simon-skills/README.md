# Simon OpenSpec skill bundle

This directory preserves Simon's Codex-native OpenSpec skill chain.

Canonical local source at snapshot time:

```text
/home/simon/.codex/skills
```

Bundle version:

```text
2026.06.11.1
```

Included skills:

- `openspec-apply-change`
- `openspec-archive-change`
- `openspec-explore`
- `openspec-map`
- `openspec-propose`
- `openspec-review`
- `openspec-verify-change`

The `shared/` directory contains the OpenSpec-specific references, templates
and validators required by the bundle. The checksum manifest lives at:

```text
simon-skills/shared/openspec-simon-bundle.json
```

When updating this snapshot, treat `~/.codex/skills` as the source of truth,
refresh the copied files, update the bundle version, and recalculate the
manifest checksums.
