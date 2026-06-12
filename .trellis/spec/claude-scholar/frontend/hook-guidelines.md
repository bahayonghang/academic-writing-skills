# Hook Guidelines

This package has real Claude Code hooks, but hook configuration is user-facing
because it is installed through `settings.json.template` and documented in the
README/setup surface.

Local pattern:

- Keep hook entrypoints in `hooks/*.js`.
- Keep hook registration in `hooks/hooks.json` and `settings.json.template`
  synchronized.
- Security-sensitive docs must match `hooks/security-guard.js`: catastrophic
  commands are denied; dangerous-but-legitimate operations require explicit
  confirmation.
- Hook docs should mention behavior, not implementation internals, unless the
  user needs a manual setup step.

Reference files:

- `ref/claude-scholar/hooks/security-guard.js`
- `ref/claude-scholar/hooks/hooks.json`
- `ref/claude-scholar/settings.json.template`
- `ref/claude-scholar/README.md`

Avoid:

- Claiming hooks are active after plugin install if the install path does not
  actually update settings.
- Documenting a hook without adding or updating its settings-template entry.
- Hiding destructive-operation confirmation requirements in a reference file
  that users will not see during install.
