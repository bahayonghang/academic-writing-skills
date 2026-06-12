# Directory Structure

User-facing Claude Scholar content is organized by installable component type:

- `skills/<skill-name>/SKILL.md`: reusable skill packages. Many skills also
  contain `references/`, `examples/`, `scripts/`, or `templates/`.
- `commands/*.md` and `commands/sc/*.md`: slash commands. The `sc` commands are
  namespaced and documented together under `commands/sc/README.md`.
- `agents/*.md`: specialized agent prompts.
- `rules/*.md`: always-available or installable rule documents.
- `CLAUDE.md`, `CLAUDE.zh-CN.md`, `CLAUDE.ja-JP.md`: compact core instruction
  files.
- `README*.md`, `MCP_SETUP*.md`, `OBSIDIAN_SETUP*.md`: localized user docs.

Reference files:

- `ref/claude-scholar/skills/command-development/SKILL.md`
- `ref/claude-scholar/skills/architecture-design/SKILL.md`
- `ref/claude-scholar/commands/sc/sc.md`
- `ref/claude-scholar/README.md`

Local pattern:

- Keep component type directories flat unless the component already owns a
  reference/example subtree.
- Put command-family documentation beside the command family, as in
  `commands/sc/README.md`.
- Keep localized root docs in sibling files with matching names and language
  suffixes.

Avoid:

- Root-level `SKILL.md` files that could be discovered as duplicate skills.
- Burying primary skill instructions in references without a short `SKILL.md`
  entrypoint.
