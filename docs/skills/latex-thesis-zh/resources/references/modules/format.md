# Format Module Reference

Purpose: Check thesis page layout, heading format, figure/table/equation numbering, and displayed-formula layout against GB/T 7713.1 and university template rules.

## Chapter Heading and Figure/Table Numbering

These are **university-level typesetting conventions**, set by each institution rather than mandated
by the national standard. See “Common University-Level Typesetting Conventions” in
[`../../templates/generic.md`](../../templates/generic.md). When the template is known, read
`templates/thuthesis.md` for the Figure 3-1 hyphen style or `templates/pkuthss.md` for the
Figure 3.1 dot style; the template handles formatting automatically.

## Displayed Formula Layout

Formula-layout questions such as “the equation number was pushed to the next line,” “should this long formula be split,” or “should adjacent formulas be split consistently” use the `format` route. Read [`../formatting/formula-guide.md`](../formatting/formula-guide.md) first, then judge against the university template.

Core judgments:

- Recommend controlled line breaking when a formula exceeds the text block, approaches the page margin, or pushes its number to the next line.
- Align derivation chains at relation symbols such as `=` / `\approx` / `\le` / `\Rightarrow`.
- Use structures such as `aligned` / `cases` for equation systems, piecewise conditions, or grouped constraints.
- Do not force a split merely for visual uniformity when the formula fits, the number remains on its line, and no derivation/grouping semantics require a split.

## Figure, Caption, and Table Layout

For captions, continued figures, and subcaptions, first read
[`../formatting/caption-guide.md`](../formatting/caption-guide.md). For three-line tables, local
long-table spacing, and double table scaling, read
[`../formatting/table-guide.md`](../formatting/table-guide.md). The correct action depends on the
current university template, packages, and compiled result; do not generalize one template's command.

Estimate effective image ppi from pixel dimensions and final layout width. DPI metadata alone does
not prove visual quality. Prefer editable or vector source, and inspect the source, exported image,
and actual compiled page together. Follow the wrapper boundary in [`compile.md`](compile.md) for
compilation and page acceptance; when no page was actually inspected, report `missing evidence`.

## Source Hygiene (F-MD / F-NOTE)

`check_format.py` emits three built-in source-hygiene checks by default without an extra flag. They only locate and report issues; they do not rewrite:

| Check | Rule | Severity |
|-------|------|----------|
| F-MD | Visible prose contains Markdown bold `**…**` (escaped `\*\*` is excluded). LaTeX renders the asterisks literally; use `\textbf{}` instead | Major/P1 |
| F-NOTE | Visible prose matches the draft-note CORE vocabulary (“此处占位/待补充/待确认/TODO/FIXME”) or unfinished HEDGE vocabulary (“待验证/暂以占位/仍在进行/重跑/复算/不代表…性能”); suspected draft residue must be removed or completed before finalization | Info/P3 |
| F-PLACEHOLDER | A table-body row has all data cells empty and contains at least 2 explicit placeholders (`& --- & --- &`); the placeholder row lacks real data. A single `-` or an N/A row mixed with real data is not reported | Major/P1 |

All three scan visible prose only and exclude math environments, verbatim content, and comments. The F-NOTE vocabulary is intentionally narrow: normal academic concessions such as “仍需实验确认” do not match, and “复算” matches only as a bare negative assertion. Chinese image paths such as `\includegraphics{中文名.png}` are removed by strip_path_args and do not trigger a false Chinese-English punctuation report.

## Key Checks

- Page margins and layout per university template
- Heading numbering consistency, chapter-based or sequential
- Caption placement: figures below, tables above
- Equation numbers right-aligned without displacement to a separate line
- Displayed formulas split only when width, alignment, derivation, grouping, or readability requires it
- Font and size compliance at each heading level, based on the university's latest formatting rules
