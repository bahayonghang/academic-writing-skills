# Logging Guidelines

Claude Scholar uses two output styles: machine-readable hook responses and
human-readable installer status.

Hook output:

- Emit valid JSON to the stream expected by the hook protocol.
- Use stderr for deny/error decisions that Claude Code should treat as hook
  output, as in `hooks/security-guard.js`.
- Keep hook messages actionable and short. Include the reason and the next
  required action, not a stack trace for expected policy decisions.

Installer output:

- Use the existing `info`, `warn`, and `error` shell helpers from `setup.sh` and
  `uninstall.sh`.
- Summarize counts at the end: updated, skipped, backed up, removed, and the
  backup path when applicable.
- Preserve clear labels for sidecar CLAUDE installs and settings merges.

Reference files:

- `ref/claude-scholar/hooks/security-guard.js`
- `ref/claude-scholar/scripts/setup.sh`
- `ref/claude-scholar/scripts/uninstall.sh`

Avoid:

- Debug prints from hooks that would corrupt JSON output.
- Logging secrets, token-like values, or full user settings.
- Reporting success before settings, manifest, and install-state writes finish.
