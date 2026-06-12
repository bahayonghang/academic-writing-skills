# Directory Structure

Claude Scholar is a distributable Claude Code support package, not an app
backend. Keep runtime logic in the existing component directories:

- `hooks/`: Node hook entrypoints and shared hook helpers. Use `hook-common.js`
  for Git state, project-memory detection, local command/skill discovery, and
  other shared hook utilities.
- `scripts/`: install, uninstall, sync, and package-manager tools. Shell
  installers live at the top of this directory; reusable Node helpers live in
  `scripts/lib/`.
- `rules/`: Markdown rule files that are installed as agent guidance, not
  executable code.
- `settings.json.template`: install-time source for hooks, MCP entries, and
  enabled plugin defaults.

Reference files:

- `ref/claude-scholar/hooks/security-guard.js`
- `ref/claude-scholar/hooks/hook-common.js`
- `ref/claude-scholar/scripts/setup.sh`
- `ref/claude-scholar/scripts/uninstall.sh`
- `ref/claude-scholar/scripts/lib/utils.js`

Local pattern:

- Keep filesystem and process helpers in `scripts/lib/utils.js`.
- Keep package-manager detection in `scripts/lib/package-manager.js`.
- Keep hook-only shared code in `hooks/hook-common.js`.
- Do not add ad hoc helpers inside individual hook files if the same behavior is
  needed by multiple hooks.

Avoid:

- Hardcoded user paths outside `os.homedir()`, `$HOME`, or install-state files.
- Adding new install targets that are not recorded in the manifest/state flow.
- Mixing Markdown rule content into executable script directories.
