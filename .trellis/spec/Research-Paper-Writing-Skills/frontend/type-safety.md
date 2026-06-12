# Type Safety

Type safety here means metadata, section names, and status labels staying
consistent.

Local contracts:

- `SKILL.md` frontmatter uses `name` and `description` fields that match the
  installed skill name.
- Section references keep stable names such as Introduction, Method, and
  Paper Review.
- Example-bank files keep local cite paths that point to the specific example
  file.
- Review statuses should stay in the small set used by the guides, such as
  `pass`, `needs revision`, and `needs new experiment`.

Reference files:

- `ref/Research-Paper-Writing-Skills/research-paper-writing/SKILL.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/references/examples/index.md`
- `ref/Research-Paper-Writing-Skills/research-paper-writing/references/paper-review.md`

Avoid:

- Renaming section guides without updating the skill entrypoint and the example
  index.
- Inventing new status labels when the guide already defines a small review
  vocabulary.
- Mixing arbitrary file paths into example entries.
