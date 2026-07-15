# Formula Typesetting and Line-Breaking Guide

This guide supports displayed-equation layout decisions in Chinese degree theses. Follow the university
template first; when no explicit institutional rule exists, use the standard `amsmath` environment-selection logic.

## Basic Principles

- Keep a short formula on one line when it fits within the text width, remains centered, and keeps its number aligned on the same line at the right.
- Do not split a formula merely to “look neater” or match the line count of adjacent formulas.
- Use controlled multiline layout when a formula exceeds the text width, approaches or crosses the page margin, or pushes its number onto the next line.
- Line breaks should serve mathematical structure: long expressions, derivation chains, grouped definitions, equation systems, or piecewise conditions.
- Give layout advice by default; do not silently rewrite `\label{}`, `\ref{}`, `\eqref{}`, or template macros.

## When to Split

### 1. Width or Numbering Failure

If an equation number that should be at the right on the same line is pushed to the next line, the
formula usually exceeds the available text-block width. Split the formula instead of forcing it onto one line.

Recommendations:

- For one long expression, consider `multline`, or use `equation` with `split` / `aligned`.
- Prefer breakpoints at commas, plus/minus signs, between product terms, or between definition-list items; do not break a semantic unit.
- Retain one equation number after splitting unless every line is an independently referenceable equation.

### 2. Derivation Chain or Relation

Align multistep derivations, equivalent transformations, and upper/lower-bound estimates at relation
symbols such as `=`, `\approx`, `\le`, and `\Rightarrow`.

Recommendation:

```latex
\begin{align}
  A &= B + C \\
    &= D + E .
\end{align}
```

If the group needs only one number, use `equation` + `aligned` or `split`, subject to template requirements.

### 3. Equation Systems, Piecewise Conditions, or Grouped Constraints

Use `aligned`, `cases`, or the university template's recommended environment for multiple conditions,
equation systems, piecewise functions, or several definitions of one object.

Recommendation:

```latex
\begin{equation}
\begin{cases}
  y = f(x), & x \ge 0, \\
  y = g(x), & x < 0 .
\end{cases}
\end{equation}
```

## When Not to Split

- The formula stays within the page margins and its number remains on the same line.
- It is not a derivation chain, equation system, piecewise condition, or grouped definition.
- Breaking it would create meaningless visual symmetry only.
- Only one adjacent formula is too long: fix that formula and keep the formulas that already render correctly.

## Recommended Output Wording

```latex
% FORMAT-FORMULA [Severity: Major] [Priority: P1]: 公式过宽导致编号被挤到下一行
% 建议：将该公式改为受控多行排版；若只是单个长表达式，保留一个编号。
% 边界：相邻短公式若能正常放入版心，不需要同步拆分。
```

## References

- AMS-LaTeX `amsmath` documentation: `equation`, `multline`, `split`, `align`, `aligned`, `cases`.
- IEEE Math Typesetting Guide for LaTeX Users: organize multiline equations by mathematical relations and readability, not mechanical line breaks.
