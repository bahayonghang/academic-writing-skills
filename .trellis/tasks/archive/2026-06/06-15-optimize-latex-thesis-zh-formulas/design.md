# Design: Formula Layout Guidance for latex-thesis-zh

## Scope

This task improves guidance and routing, not automated formula rewriting.

In scope:

- Update `SKILL.md` so formula-layout prompts route to formatting guidance.
- Add a concise reference file for displayed formula line breaking in Chinese
  theses.
- Link that reference from the existing `format` module and template guidance.
- Add eval prompts/assertions for the screenshot case.

Out of scope:

- Writing a parser that measures rendered formula width.
- Automatically transforming LaTeX math environments.
- Changing school template behavior or geometry settings.

## Existing Architecture

`latex-thesis-zh` has a table-driven module router in `SKILL.md`. Formatting
queries route to:

- `scripts/check_format.py`
- `references/modules/format.md`
- template snapshots in `templates/`

Formula references currently appear only as:

- numbering style in `templates/generic.md` and `templates/thuthesis.md`;
- safety boundaries that preserve math environments;
- logic checks that flag headings directly followed by formulas.

There is no dedicated formula-layout route today.

## Proposed Shape

Use the existing `format` route as the first implementation boundary.

Add:

- `references/formatting/formula-guide.md`
  - when to keep one line;
  - when to split;
  - environment-choice heuristics: `equation`, `split`, `aligned`,
    `multline`, `cases`;
  - equation-number displacement as a concrete failure sign;
  - thesis-template caveat: follow the school template first.
- `references/modules/format.md`
  - point formula-layout questions to the formula guide.
- `templates/generic.md`
  - expand the formula-numbering note from "right aligned" to include the
    "do not let the number be pushed to an extra line" practical check.
- `SKILL.md`
  - Triggering / Module Router / route rules mention formula line breaking,
    equation-number collision, and "whether this formula should be split".
- `evals/evals.json`
  - add a realistic prompt using the screenshot scenario.

## Trade-Offs

### Lightweight route through `format`

Pros:

- Minimal surface area.
- Matches the existing "template and layout" purpose of the format module.
- Avoids a fake script that cannot actually know rendered width.

Cons:

- Less discoverable than a separate `formula` module.

### Separate `formula` module

Pros:

- More explicit route for formula-heavy thesis editing.

Cons:

- Adds a module without an automated checker.
- Risks overlap with `references` for equation labels and `logic` for
  formula-after-heading structure.

Decision: use the lightweight `format` route now.

## Compatibility

- Do not change `scripts/check_format.py` unless implementation discovers a
  low-risk static check worth adding.
- Preserve existing evals and trigger behavior for title/structure/logic.
- Keep all guidance source-preserving: propose layout changes, do not mutate
  user math unless explicitly asked.
