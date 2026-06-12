# Quality Guidelines

PaperSpine frontend artifacts must stay portable, bilingual where promised, and
free of template drift.

Local checks:

- README.md and README.en.md should stay content-equivalent.
- Dist skill files should exist for all three hosts and all suite skills.
- Skill metadata should avoid BOMs, control characters, and overly long
  descriptions.
- Dist skill files should not contain raw local-private paths.
- Installed docs should not expose relative launcher paths when the host expects
  installed paths.

Reference files:

- `ref/PaperSpine/tests/test_skill_structure.py`
- `ref/PaperSpine/tests/test_cross_platform_and_ui.py`
- `ref/PaperSpine/README.md`
- `ref/PaperSpine/README.en.md`

Avoid:

- Letting one host lag behind the others.
- Introducing control-character corruption in Markdown files.
- Changing the public README promise without updating the installed suite docs.
