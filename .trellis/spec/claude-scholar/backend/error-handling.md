# Error Handling

Use failure behavior that matches the local runtime:

- Hooks must return the protocol shape expected by Claude Code. For example,
  `hooks/security-guard.js` writes deny decisions to stderr as JSON and exits
  with `2`; confirmation-required cases return `continue: true` with a
  `systemMessage` and exit `0`.
- Hook utilities prefer safe fallbacks over crashes for optional context. In
  `hooks/hook-common.js`, Git, filesystem, frontmatter, and settings reads catch
  failures and return default objects.
- Install scripts use `set -euo pipefail` and a small `error()` helper that
  prints a clear message before exiting.
- Uninstall must fail closed when ownership metadata is missing. See
  `scripts/uninstall.sh` `require_install_metadata()`.

Reference files:

- `ref/claude-scholar/hooks/security-guard.js`
- `ref/claude-scholar/hooks/hook-common.js`
- `ref/claude-scholar/scripts/setup.sh`
- `ref/claude-scholar/scripts/uninstall.sh`

When adding failures:

- Distinguish "block", "confirm", and "allow" for hook decisions.
- Catch only the local operation that can fail; do not hide unrelated parsing or
  path errors behind a broad success message.
- For destructive operations, require install-state evidence before deletion.

Avoid:

- Bare process exits with no message.
- Emitting malformed JSON from hooks.
- Continuing an uninstall when ownership cannot be proven.
