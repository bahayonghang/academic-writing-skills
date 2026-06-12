# Type Safety

Type safety here means structured metadata and controlled config values.

Local contracts:

- `intake_wizard.py` uses explicit choice constants such as workflows, scenes,
  tiers, languages, and reference modes.
- `PaperSpineConfig` is a dataclass, and JSON config output comes from
  `asdict(config)`.
- `paperspine_update.py` compares versions through a dedicated parser and key
  function.
- Markdown frontmatter in skills and commands must stay simple and portable.
- Inventory and check scripts should emit stable table columns for downstream
  validation.

Reference files:

- `ref/PaperSpine/src/scripts/intake_wizard.py`
- `ref/PaperSpine/src/scripts/paperspine_update.py`
- `ref/PaperSpine/src/scripts/artifact_check.py`
- `ref/PaperSpine/tests/test_intake_wizard.py`
- `ref/PaperSpine/tests/test_update_script.py`

Avoid:

- Free-form config values where the wizard already offers a closed choice set.
- Frontmatter fields that are not supported by the installed host.
- Renaming JSON/table keys without updating the validator and tests together.
