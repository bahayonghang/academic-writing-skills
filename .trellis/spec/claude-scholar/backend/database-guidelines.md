# Configuration And State

There is no database, ORM, or migration layer. Persistent state is JSON or text
metadata under the user's `.claude` directory and must be treated as user-owned
unless the install manifest proves ownership.

State files and sources of truth:

- `settings.json.template` is the repository source for hook, MCP, and plugin
  defaults.
- `scripts/setup.sh` writes `.claude-scholar-manifest.txt` and
  `.claude-scholar-install-state` so later uninstall operations know exactly
  what the installer owns.
- `scripts/uninstall.sh` refuses to guess ownership when the manifest or state
  file is missing.
- `scripts/lib/package-manager.js` stores package-manager preferences in
  `.claude/package-manager.json` or the global `.claude` config directory.

Local pattern:

- Parse and merge JSON with Node, then write formatted UTF-8 JSON with a final
  newline.
- Preserve existing user `CLAUDE.md`, `CLAUDE.zh-CN.md`, env/model/API key
  settings, and unrelated `settings.json` entries.
- Install repository CLAUDE files as sidecars when a user file already exists.
- Record every managed path that install/uninstall code may later remove.

Avoid:

- Treating `settings.json` as fully owned by this package.
- Removing files that are not listed in the install manifest.
- Writing tokens, API keys, or private paths into tracked templates.
