# Cross-References Module Reference

Purpose: Check the integrity of figure, table, and equation cross-references across a
multi-file thesis project (\input/\include are resolved automatically).

## Checks

| Check                       | Severity      | Description                                           |
| --------------------------- | ------------- | ----------------------------------------------------- |
| Undefined reference         | Critical / P0 | `\ref{x}` has no matching `\label{x}` definition, a frequent blind-review deduction |
| Unreferenced label          | Minor / P2    | A `fig:`/`tab:`/`eq:` label is never referenced in the body |
| Missing caption             | Major / P1    | A figure/table environment has a label but no `\caption` |
| Reference before definition | Minor / P2    | In the same file, `\ref` appears before `\label` |
| Numbering gap               | Minor / P2    | Numeric label suffixes skip a value, such as fig:a1 and fig:a3 without fig:a2 |

## Command

```bash
uv run python $SKILL_DIR/scripts/check_references.py main.tex
uv run python $SKILL_DIR/scripts/check_references.py main.tex --json
```

Supports `\ref` / `\eqref` / `\autoref` / `\cref` / `\Cref` / `\pageref` /
`\hyperref[]{}`. Exit code is 1 when a Critical undefined reference exists, otherwise 0.

## Notes

- Multi-file parsing follows `\input{}` / `\include{}` automatically and safely handles cycles.
- Labels/references on comment lines are ignored.
- Cross-file ordering is not checked because it is not meaningful; reference-before-definition is checked only within one file.
