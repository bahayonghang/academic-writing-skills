# Spec-Check Module Reference

Purpose: Perform an **item-by-item final check** against the university rule checklist at finalization.
The checklist comes from the “## 逐项检查清单” section of `templates/<template>.md` (or a custom
`--spec-file`). The script executes automatically decidable items, routes the rest to NEEDS-LLM /
MODULE / MANUAL, and summarizes them as an itemized compliance report.

## Primary Command

```bash
uv run python $SKILL_DIR/scripts/check_spec.py main.tex --template yanshan --degree doctor
```

- `--template <id>`: use the checklist in `templates/<id>.md` (currently yanshan, thuthesis, pkuthss,
  and generic). Without it, infer from documentclass; a template without a checklist causes an error
  listing available checklists.
- `--spec-file <path>`: use any custom rule file following the checklist-table format. This is the
  generic entry point for any university. Items referencing nonexistent checkers degrade to NEEDS-LLM
  without interrupting execution.
- `--degree master|doctor`: degree type, affecting length/reference-count thresholds and item scope.
  If omitted, detect from body text; on failure, use master and note it in the report header.
- `--bib <path>`: specify the .bib. By default, discover it from `\bibliography` / `\addbibresource`,
  or fall back to counting the `thebibliography` environment.
- `--year <yyyy>`: base year for latest-five/latest-two-year decisions (current year by default; fix it for tests or reproduction).
- `--json`: structured output (items + summary + status).

Exit codes: any FAIL -> 1; missing/invalid checklist file -> 2; otherwise 0.

## Workflow (Five Steps)

1. **Confirm checklist**: for a known university/template, use `--template`. Otherwise run the `template` module first. If no checklist remains available, ask for the university name or rules document and convert it into the `--spec-file` format below.
2. **Run script**: execute the Primary Command to obtain itemized results in six statuses (PASS / FAIL / NEEDS-LLM / MODULE / MANUAL / SKIP).
3. **Handle MODULE items**: execute each recommended existing module command (tables / references / bibliography / consistency / format), then attach its findings to the corresponding checklist item.
4. **Judge NEEDS-LLM items one by one**: for each item, open `templates/<template>.md` and follow the key-point section referenced by `规范依据`, such as §1.5.3 conclusion requirements. Compare it with the relevant thesis text and determine compliant / noncompliant / indeterminate, with evidence (source file:line + original excerpt). Mark the judgment `[LLM]` and state it separately from script results (`[Script]`).
5. **Summarize report**: output an itemized conclusion table in checklist order (ID / item / result / evidence / recommendation). Give executable diff/suggestion repairs for FAIL and LLM-noncompliant items. Output MANUAL items unchanged as a **pre-print checklist**; layout/printing items cannot be statically determined, so do not fabricate conclusions.

## Status Semantics

| Status | Meaning | Next Action |
| ----------- | ---------------------------------------------------------- | ------------------- |
| PASS / FAIL | Script-decided, with evidence and rule basis | Give repair suggestion for FAIL |
| NEEDS-LLM | Script cannot decide: semantic, missing input, or unknown custom-checklist checker | Judge item by item in Step 4 |
| MODULE | Covered by an existing module | Execute command in Step 3 |
| MANUAL | Requires compiled PDF / print inspection | Add to pre-print checklist |
| SKIP | Scope does not match current degree | None |

## Custom Checklist Format (--spec-file)

Use the same five-column Markdown table as “## 逐项检查清单” in `templates/yanshan.md`.

```markdown
## 逐项检查清单

| ID    | 检查项               | 规范依据 | 检查方式        | 适用 |
| ----- | -------------------- | -------- | --------------- | ---- |
| XX-01 | 关键词 3～8 个       | §2.1     | script:kw_count | 通用 |
| XX-02 | 摘要含研究目的与结论 | §1.2     | llm             | 通用 |
```

- `ID`: `大写前缀-两到三位序号`, such as `XX-01`, unique within the file.
- `检查方式`: `script:<checker>` (built-in checkers below) / `module:<模块名>` (a module in the SKILL.md routing table) / `llm` / `manual`.
- `适用`: `通用` / `硕士` / `博士`.
- Thresholds for built-in length/count checkers come from `TEMPLATE_THRESHOLDS` by template id. When a custom checklist has no threshold basis, these items report measured values and degrade to NEEDS-LLM instead of borrowing another university's threshold.

## Built-In Checkers (script:)

`title_len` (title <=25/subtitle <=35) · `abstract_no_cite` (no citations/figures/tables/formulas in abstract) ·
`kw_count` (3-8 keywords separated by semicolons) · `kw_zh_en_match` (same Chinese/English keyword count) ·
`abstract_len` · `abstract_order` (Chinese before English) · `wordcount` (body length) ·
`intro_len` (introduction length) · `chapter_summary` (chapter summary in every chapter) ·
`conclusion_no_cite` (conclusion cites no literature and is the last chapter) · `conclusion_len` (conclusion <=2000 Chinese characters) ·
`conclusion_hedge` (vague conclusion wording) · `bib_count` · `bib_recency` (at least 1/3 in latest five years and at least one in latest two) ·
`heading_len` (heading <=15 Chinese characters) · `heading_depth` (depth <=4) ·
`cite_in_heading` (no \cite in headings) · `new_page_chapter` (each chapter starts a new page) ·
`appendix_letter` (appendices lettered)

Range/lower-bound checkers use a +/-10% buffer. Values in the buffer report NEEDS-LLM because rules
often say “generally”; values beyond it report FAIL. Length is the visible-text non-whitespace character
count, an approximation including figure/table text, and the report says so. Parenthetical values above
are defaults. `TEMPLATE_THRESHOLDS[<模板>]` can override length/count/separator thresholds by
university: Tsinghua title 25 with no subtitle extension, Peking title 20 and 3-5 comma-separated
keywords, generic with no separator check. Missing keys retain defaults and never borrow another university's values.

## Output Contract

- FAIL line: `% SPEC-CHECK [High] [P1] [Script]: <ID> <检查项> — <证据>（依据 <§>）`.
- An LLM supplemental judgment uses the same line format with source `[LLM]` and location `源文件:行号`.
- Do not modify source files; leave `\cite{}` / `\ref{}` / `\label{}` / math environments unchanged.
- The report must retain the MANUAL checklist. Silence on whether layout items pass means they cannot be statically determined; do not claim “compliant” for the user.

## Common Follow-Ups

- **“I am at Yanshan University; do my final pre-graduation check”** -> `--template yanshan`, then confirm degree from context.
- **“Our university has no checklist”** -> ask for the original rules/PDF text, organize it first as a `--spec-file` checklist with a source for every item, let the user confirm it, and then run the final check. Never invent items from general practice.
- **Before blind-review submission** -> run the `blind-review` module for personal-information redaction in addition to the final check.
