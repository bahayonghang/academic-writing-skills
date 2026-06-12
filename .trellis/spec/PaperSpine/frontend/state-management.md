# State Management

PaperSpine state is the workflow artifact tree and the preserved install config,
not interactive app state.

Local pattern:

- `paper_rewriting_output/` is the working artifact tree. It should capture
  config, research, citation, rationale, and final-paper outputs.
- `paper_spine_config.json` and `paper_spine_config.md` are the intake outputs.
- `~/.paperspine/config.json` is preserved across updates.
- `~/.paperspine/install_state.json` tracks the installed version and targets.
- The workflow should not collapse to only `final_paper/main.tex`.

Reference files:

- `ref/PaperSpine/README.md`
- `ref/PaperSpine/src/scripts/intake_wizard.py`
- `ref/PaperSpine/src/scripts/paperspine_update.py`
- `ref/PaperSpine/tests/test_intake_wizard.py`
- `ref/PaperSpine/tests/test_update_script.py`

Avoid:

- Promising that the final paper is the only deliverable.
- Overwriting preserved config just because a new version is installed.
- Skipping rationale, citation, or source-index artifacts when the workflow
  calls for them.
