# Optimize latex-thesis-zh formula guidance

## Goal

Improve `academic-writing-skills/latex-thesis-zh` so it gives stable,
publication-aware guidance when users ask whether Chinese thesis formulas should
stay on one display line or be split across lines.

The motivating case is a displayed formula whose equation number is forced onto
the next line because the formula is too wide. The skill should recommend a
controlled multi-line layout for that formula while leaving a second, already
well-fitting formula unchanged.

## Requirements

- Verify formula line-break advice against authoritative LaTeX/typesetting
  sources before editing the skill.
- Add guidance that distinguishes:
  - overflow / equation number collision / margin violation, where line breaking
    is appropriate;
  - derivation chains or relation-heavy formulas, where alignment at relation
    operators is appropriate;
  - systems of equations or multi-case definitions, where grouped environments
    are appropriate;
  - short independent formulas that fit the text width, where forced line
    breaking is unnecessary.
- Avoid overclaiming that only three situations ever justify a multi-line
  formula. Include adjacent legitimate cases such as one numbered display
  containing multiple related definitions or aligned relations.
- Keep the existing `latex-thesis-zh` safety boundary: do not silently rewrite
  math blocks, labels, references, or template macros.
- Prefer minimal changes to the existing skill surface: route formula-layout
  questions through the existing formatting/reference material unless evidence
  shows a separate module is worth the added complexity.
- Add eval coverage so future changes preserve the intended distinction:
  first formula may be split because the number is displaced; second formula
  remains unchanged because it fits.

## Acceptance Criteria

- [x] Research notes cite authoritative sources and separate confirmed facts
      from project-specific interpretation.
- [x] `latex-thesis-zh` documentation explains when to split displayed
      formulas and when not to.
- [x] The guidance explicitly handles equation numbers being pushed to a
      second line as a sign of width/layout failure.
- [x] The guidance says not to split a formula merely for visual symmetry if it
      fits within the text block and has no derivation/grouping reason.
- [x] Evals include at least one prompt matching the screenshot scenario.
- [x] Validation plan includes the existing lightweight skill checks used by
      the prior `latex-thesis-zh` optimization loop.

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md`
  for execution planning before `task.py start`.
