# Logging Guidelines

PaperSpine uses plain CLI output instead of a logging framework.

Local output patterns:

- Scripts print status lines to stdout and return JSON or Markdown when asked.
- Errors go to stderr when the script is already treating them as failures.
- The wizard prints final `Wrote ...` lines for the generated config files.
- The updater prints the current and target versions, then the preserved config
  path.
- Validation tools produce markdown reports that are readable as standalone
  artifacts.

Reference files:

- `ref/PaperSpine/src/scripts/intake_wizard.py`
- `ref/PaperSpine/src/scripts/paperspine_update.py`
- `ref/PaperSpine/src/scripts/artifact_check.py`
- `ref/PaperSpine/src/scripts/citation_bank_check.py`

Avoid:

- Adding a logging dependency for script output that is already expressed as a
  small CLI status line.
- Mixing debug noise into report-generating scripts.
- Printing raw escape codes in the keyboard preview or terminal UI paths.
