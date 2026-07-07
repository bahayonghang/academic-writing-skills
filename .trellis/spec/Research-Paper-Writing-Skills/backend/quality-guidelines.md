# Quality Guidelines

The repository is a documentation-first skill package, so quality means clear
writing, clean packaging, and portable references.

Local patterns:

- Keep the SKILL entrypoint short and route detail into the section files.
- Keep the README install guidance consistent with the skill contract.
- Keep examples concrete and tied to a section purpose.
- Keep English README and Chinese README aligned at the repository level.
- De-AI checker changes should treat structure-shell findings as advisory
  review signals, not hard rewrite commands. Add false-positive tests for
  evidence-bearing academic contrasts before adding new shell patterns.

Verification:

- Read the SKILL file, one section guide, and one example bank file together
  before making a broad edit.
- Check that the skill still has a single triggerable entrypoint and the section
  guide names still match the README.
- For de-AI scripts, test both sides of the rule: one example that flags the
  shell and one evidence-backed contrast that stays unflagged.

Reference files:

- `ref/Research-Paper-Writing-Skills/README.md`
- `ref/Research-Paper-Writing-Skills/README_zh.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/SKILL.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/references/examples/index.md`

Avoid:

- Expanding the skill body into a dump of every section guide.
- Letting the English and Chinese README diverge.
- Adding examples that do not teach a reusable writing pattern.
