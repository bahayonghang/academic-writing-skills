# State Management

State in this user-facing layer is installation state and user configuration,
not React/server state.

Local pattern:

- README install sections must tell users that existing `CLAUDE.md` and
  `CLAUDE.zh-CN.md` files are preserved and repository versions may install as
  sidecars.
- `settings.json` is merged, not overwritten. User env/model/API key fields are
  preserved by `scripts/setup.sh`.
- Uninstall behavior depends on `.claude-scholar-manifest.txt` and
  `.claude-scholar-install-state`.
- Package-manager preference state belongs in `.claude/package-manager.json`
  through `scripts/lib/package-manager.js`.

Reference files:

- `ref/claude-scholar/README.md`
- `ref/claude-scholar/scripts/setup.sh`
- `ref/claude-scholar/scripts/uninstall.sh`
- `ref/claude-scholar/scripts/lib/package-manager.js`

Avoid:

- Telling users that sidecar CLAUDE files are auto-applied.
- Hand-editing documentation for install state without checking the installer
  and uninstaller code.
- Treating generated user config as tracked source.
