# Type Safety

Type safety here means metadata and structured-file correctness.

Local contracts:

- Skill frontmatter uses stable scalar keys such as `name`, `description`, and
  optional `version`.
- Command frontmatter uses supported fields such as `description`,
  `allowed-tools`, `model`, and `argument-hint`.
- JSON files are parsed and written with `JSON.parse` and
  `JSON.stringify(..., null, 2)` patterns in the local scripts.
- YAML-like frontmatter parsing in `hooks/hook-common.js` is intentionally
  simple; do not rely on nested YAML features there.
- Settings paths should be path-joined or plugin-relative, not string-built from
  platform-specific absolute paths.

Reference files:

- `ref/claude-scholar/hooks/hook-common.js`
- `ref/claude-scholar/scripts/lib/utils.js`
- `ref/claude-scholar/skills/command-development/SKILL.md`
- `ref/claude-scholar/settings.json.template`

Avoid:

- Complex YAML in frontmatter that the local lightweight parser cannot read.
- JSON writes without UTF-8 and a final newline.
- Command examples that depend on a personal absolute path.
