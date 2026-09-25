# Three-Line Table Guide (GB/T Chinese Thesis)

This guide describes the common three-line (`booktabs`) convention for Chinese theses. The current
university specification and the actual class remain authoritative for caption language, numbering, typeface,
and exceptional table forms.

## Three-Line Table Standard

A three-line table has exactly three horizontal rules and **no vertical lines**:

1. **Top rule** (`\toprule`): above column headers
2. **Mid rule** (`\midrule`): below column headers, above data rows
3. **Bottom rule** (`\bottomrule`): below the last data row

### Anti-Patterns (must flag)

- Vertical lines (`|` in column spec, `\vline`)
- Internal horizontal lines (`\hline` or `\cline` between data rows)
- Using `\hline` instead of booktabs commands
- Missing `\usepackage{booktabs}` in preamble

### Minimal Correct Example

```latex
\begin{table}[htbp]
  \caption{不同模型的准确率比较（\%）}
  \label{tab:accuracy}
  \centering
  \begin{tabular}{lSSS}
    \toprule
    模型 & {精确率} & {召回率} & {F1值} \\
    \midrule
    基线模型   & 85.3 & 82.1 & 83.7 \\
    本文方法   & \textbf{91.2} & \textbf{89.5} & \textbf{90.3} \\
    \bottomrule
  \end{tabular}
\end{table}
```

## Caption and Numbering (GB/T)

- **Caption position**: above the table
- **Numbering format**: "表 3-1" or "表3.1" (chapter-based), Song typeface 5-point (宋体五号)
- **Label**: immediately after caption (`\label{tab:...}`)
- **Table note**: below the table, starting with "注：" (Chinese) or "Note." (English)

The checkers accept a real `\caption` or `\bicaption`, including whitespace, line breaks, and an optional
short title after the command. A commented caption, `\captionsetup`, or a similarly named custom command does
not satisfy caption presence. This syntactic check does not prove that the caption wording or rendered template
format is correct. Use the caption form required by the actual class; do not replace every school's macro.

## Decimal Alignment

Use the `siunitx` package `S` column type to align numbers by decimal point:

```latex
\usepackage{siunitx}
\sisetup{detect-weight, mode=text}
```

When `siunitx` is unavailable, right-align numeric columns with `r`.

## Statistical Significance Markers

| Symbol | Meaning |
|--------|---------|
| `*`    | p < 0.05 |
| `**`   | p < 0.01 |
| `***`  | p < 0.001 |

Place significance markers immediately after the value: `91.2***`.

## Number Precision Rules

| Data type | Precision | Example |
|-----------|-----------|---------|
| Percentage | 1 decimal place | 85.3% |
| Mean +/- SD | 2 decimal places | 3.14 +/- 0.05 |
| p-value | 3 significant figures | 0.003 |
| Large counts | No decimals | 1,024 |

Precision must be consistent within each column.

## Longtable Spacing

Change long-table spacing only after a compiled page shows that `\LTpost` or related longtable glue is causing
the local blank region. Apply the smallest local setting around the affected `longtable`, for example:

```latex
{
  \setlength{\LTpost}{0pt}
  \begin{longtable}{...}
    ...
  \end{longtable}
}
```

Do not modify the global class or all long tables from one page-level symptom. Recompile and inspect the end of
the table, the following paragraph, page breaks, repeated headers, and the adjacent page. If the blank space has
a different owner, keep `\LTpost` unchanged.

## Avoid Double Table Scaling

When a table already uses fixed-width columns, first check whether `\resizebox`, an additional small-font command,
or another outer scale is shrinking it a second time. Remove only the redundant layer that causes unreadable text;
then check width overflow, column wrapping, rule alignment, and readability on the compiled page. A wide table does
not by itself authorize scaling every table to `\textwidth` or changing the class.

## Bold Best Values

In comparison tables, bold the best value in each column. Add direction indicators when ambiguous:
- `↑` higher is better
- `↓` lower is better

## Word Compatibility Note

When submitting thesis with .docx:
1. Create a standard table in Word
2. Select all -> Borders -> No Border
3. Add top border, header bottom border, and table bottom border
4. Result: three-line table matching booktabs aesthetic

## Rendered Acceptance

Use the existing `compile.py` wrapper with the thesis's real entry file and recipe. A passing script check or a
generated PDF does not establish visual acceptance. Inspect the affected table and adjacent pages after compilation.
If no rendered page was actually viewed, report the visual result as `missing evidence`.

## College source checks (yanshan-ee-2025 only)

These candidates run only with `check_tables.py --school yanshan-ee-2025`. The default and
`--school generic` do not emit them. There is no bare `yanshan` alias. Each finding is `[Script]`,
Info/P3, and `Meaning-Check: NEEDS-LLM`. It names a local cell or caption and does not supply a
replacement sentence.

- `TB-SAMEAS`: `同上` or `同左` in the tabular body. Caption text and table notes are excluded.
- `TB-UNITHEAD`: a simple `tabular` column with at least three numeric rows that share one literal unit, while the header lacks that unit. The script does not convert units. `multicolumn`, `multirow`, or a nested table produces a non-coverage note instead of a merged hit.
- `TB-COVERAGE` only: `longtable`, `sidewaystable`, `tabularx`, and a second `tabular` inside one `table` float get one coverage note per float. They are not scanned for `同上`/`同左`, shared-unit headers, or caption punctuation.
- Blank cells and dashes do not establish that a quantity was not measured or was measured and not found. Keep that reading manual.
- `CAP-PUNCT` in this script covers Chinese terminal punctuation of table floats only. Figure floats belong to `check_references.py`.

The college wording is the 2025 electrical-engineering checklist. It is not written into the frozen `templates/yanshan.md`, `thuthesis.md`, `pkuthss.md`, or `generic.md` files.
