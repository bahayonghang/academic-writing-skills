# Formula Layout Standards Research

## User Claim Under Review

The user argues:

- In the screenshot, the first displayed formula has already pushed the equation
  number onto a second line, so the formula may be shown as two lines instead of
  being forced into one line.
- The second formula should not be changed.
- In academic publications and theses, formulas are generally split only when:
  1. a formula is too long for the printable width;
  2. the formula is a multi-step derivation, often aligned at `=`;
  3. the formula is an equation system, often grouped with a large brace.

## Confirmed Facts

### Equation numbers belong at the display edge, not on a displaced extra line

Chinese thesis template notes already in this repository state that equation
numbers are normally right-aligned, commonly as `(3.1)` or `(3-1)`. See:

- `academic-writing-skills/latex-thesis-zh/templates/generic.md`
- `academic-writing-skills/latex-thesis-zh/templates/thuthesis.md`

Interpretation for the screenshot: when a display formula is so wide that the
number is visibly pushed to a separate line, the layout is failing the normal
display-equation expectation. The skill should treat that as a valid reason to
recommend a controlled multi-line layout.

### Authoritative LaTeX guidance supports different multi-line environments for different math shapes

The AMS LaTeX documentation for `amsmath` provides distinct display structures
for:

- single-line numbered equations (`equation`);
- long equations split across lines (`multline`);
- aligned multi-line relations (`align`, `aligned`, `split`);
- grouped equations and cases (`gather`, `cases`, and related structures).

This supports a decision tree rather than a blanket instruction to make every
wide display a two-line equation.

Source used:

- AMS/LaTeX `amsmath` user documentation:
  `https://www.latex-project.org/help/documentation/amsldoc.pdf`

### Publishing-style guidance also treats line breaking as semantic and visual

IEEE math typesetting guidance for LaTeX users discusses line breaks and
alignment as part of mathematical readability, not just page fitting. The common
pattern is to align continued relations at relation operators when a displayed
equation spans multiple lines.

Source used:

- IEEE Math Typesetting Guide for LaTeX Users:
  `https://conferences.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/8/IEEE-Math-Typesetting-Guide-for-LaTeX-Users.pdf`

## Assessment of the User Claim

The claim is mostly correct as practical thesis guidance:

- The first screenshot formula should be eligible for splitting because the
  equation number has been displaced, indicating a width problem.
- The second formula should remain unchanged if it fits the text block and does
  not encode a derivation chain or equation system.
- The three categories named by the user are the right core categories for
  conservative guidance.

The only adjustment: do not write the three categories as a closed universal
law. Academic math layout also commonly uses multi-line displays for closely
related definitions, aligned relations, or grouped constraints even when they
do not look like a classic brace-style equation system. The safer wording is:
"usually split only when there is a width, alignment, derivation, grouping, or
readability reason; otherwise keep a fitting formula on one line."

## Recommended Skill Guidance

For `latex-thesis-zh`, the guidance should say:

1. Do not split a displayed formula merely because it looks dense.
2. Split or reformat when the formula exceeds the text block, collides with the
   equation number, or pushes the number to another line.
3. For a long single expression with one number, prefer a controlled `split`,
   `aligned`, or `multline` layout inside the display, depending on the formula
   shape and thesis template.
4. For derivation chains, align at relation operators such as `=`, `\approx`,
   `\le`, or `\Rightarrow`.
5. For equation systems, cases, or grouped constraints, use grouped structures
   such as `aligned`, `cases`, or template-appropriate environments.
6. If a formula fits and has no derivation/grouping reason, leave it unchanged.

## Open Implementation Question

Whether to implement formula guidance as:

- a lightweight addition to the existing `format` module and template docs; or
- a separate `formula` route.

Recommendation: start lightweight. Add `formula` language to `format` routing,
create a small formula layout reference, and add evals. A separate script/module
can wait until users need automated detection from `.tex` sources.
