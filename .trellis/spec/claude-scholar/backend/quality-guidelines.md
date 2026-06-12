# Quality Guidelines

Backend/runtime code is mostly standard Node CommonJS and POSIX shell. Match the
existing style instead of introducing a framework.

Local patterns:

- Node modules use `require(...)` and `module.exports`, as in
  `scripts/lib/utils.js`, `scripts/lib/package-manager.js`, and
  `hooks/hook-common.js`.
- Path operations use Node `path`/`os` helpers or shell variables based on
  `$HOME`, never string-concatenated platform-specific absolute paths.
- Shell installers start with `#!/usr/bin/env bash` and `set -euo pipefail`.
- Dangerous file operations are ownership-aware. `setup.sh` records managed
  paths; `uninstall.sh` removes only recorded paths.
- Security-sensitive code validates inputs before invoking commands. For
  example, `commandExists()` accepts only simple command names before calling
  `where` or `which`.

Verification:

- For script changes, inspect the relevant installer or Node entrypoint directly
  and run the narrow command if it is safe in a temporary target.
- For hook changes, check JSON output shape and exit code behavior manually.
- For settings changes, verify user-owned fields are preserved by the merge
  logic.

Avoid:

- Adding third-party dependencies for small install or hook behavior.
- Writing shell code that assumes only macOS/Linux if the helper is meant to run
  on Windows through Node.
- Adding broad cleanup commands that bypass manifest ownership.
