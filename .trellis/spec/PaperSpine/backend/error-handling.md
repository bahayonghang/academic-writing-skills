# Error Handling

Use explicit failure modes that match the local scripts:

- `paperspine_update.py` raises `UpdateError` for expected updater failures and
  returns exit code `1` from `main()`.
- `paperspine_update.py --check-only` returns `2` when an update is available
  but no install should occur.
- `artifact_check.py` returns a nonzero status when required artifacts are
  missing or content checks fail.
- `intake_wizard.py` should exit cleanly on `KeyboardInterrupt` when the user
  quits interactive input.
- Test helpers and validators should fail with concrete file or row references,
  not vague "something went wrong" messages.

Reference files:

- `ref/PaperSpine/src/scripts/paperspine_update.py`
- `ref/PaperSpine/src/scripts/artifact_check.py`
- `ref/PaperSpine/src/scripts/intake_wizard.py`
- `ref/PaperSpine/tests/test_update_script.py`
- `ref/PaperSpine/tests/test_integrity_audit.py`
- `ref/PaperSpine/tests/test_scripts.py`

When adding failure points:

- Validate the repository/package before replacing install targets.
- Keep archive validation separate from install replacement.
- Leave existing installs untouched when a downloaded archive is incomplete.
- Prefer narrow, expected exceptions over blanket catches.

Avoid:

- Swallowing update or validation errors and still reporting success.
- Replacing installed host copies before the new archive passes validation.
- Turning user quit paths into stack traces.
