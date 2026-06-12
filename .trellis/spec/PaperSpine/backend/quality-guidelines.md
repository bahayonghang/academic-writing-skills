# Quality Guidelines

PaperSpine scripts are standard library only and must stay portable.

Local patterns:

- Use Python 3.10+ syntax that matches the repo's `ruff.toml`.
- Keep `dist` excluded from linting and treat it as generated output.
- Favor `unittest`-style checks for script behavior and layout invariants.
- Keep helper logic in `src/scripts/_paper_spine_utils.py` instead of copying it
  into each tool.
- Keep line length policy aligned with the repo config (`line-length = 120`).

Verification:

- Run `python -m unittest discover -s tests` when changing scripts or dist
  layout assumptions.
- Use the narrow script test or validation command that covers the changed
  behavior.
- Check that dist sync still preserves the expected suite layout.

Reference files:

- `ref/PaperSpine/ruff.toml`
- `ref/PaperSpine/tests/test_scripts.py`
- `ref/PaperSpine/tests/test_skill_structure.py`
- `ref/PaperSpine/src/scripts/_paper_spine_utils.py`

Avoid:

- Adding third-party dependencies to the shared scripts.
- Writing path- or shell-specific logic when a standard-library helper already
  exists.
- Letting `dist/` drift from the canonical source without a sync step.
