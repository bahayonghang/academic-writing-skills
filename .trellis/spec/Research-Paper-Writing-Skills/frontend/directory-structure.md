# Directory Structure

The writing skill is organized around section guides and examples:

- `references/introduction.md`, `method.md`, `abstract.md`, `experiments.md`,
  `related-work.md`, `conclusion.md`, and `paper-review.md` are the section
  guides.
- `references/examples/` holds reusable writing patterns.
- `references/examples/index.md` is the example-bank index.
- `SKILL.md` points users to the right section guide instead of duplicating all
  of them.

Local pattern:

- Keep the section-guide list stable and easy to load one file at a time.
- Keep examples grouped by section so users can find a pattern quickly.
- Keep the README focused on installation and package purpose.

Reference files:

- `ref/Research-Paper-Writing-Skills/research-paper-writing/SKILL.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/references/examples/index.md`

Avoid:

- Flattening the example bank into one giant file.
- Duplicating section logic in the skill body when the guide already exists.
- Creating extra runtime directories that are not part of the skill package.
