# Module: Tables

**Trigger**: table, 表格, 三线表, three-line, booktabs, tabular, data table, generate table, table format

## Commands

```bash
uv run python -B $SKILL_DIR/scripts/check_tables.py main.typ
uv run python -B $SKILL_DIR/scripts/check_tables.py main.typ --fix-suggestions
uv run python -B $SKILL_DIR/scripts/check_tables.py main.typ --json
uv run python -B $SKILL_DIR/scripts/generate_table.py data.csv --style booktabs --bilingual
uv run python -B $SKILL_DIR/scripts/generate_table.py data.json --style plain
```

## Details

**check_tables.py**: Scans `table(...)` calls in the Typst source. Checks:

- Three-line rule compliance (`table.hline` rules, no `table.vline`)
- Vertical-line presence (`table.vline` flagged)
- `stroke: none` on the table with explicit hlines (three-line idiom)
- Number precision consistency within columns

`--fix-suggestions` attaches a concrete fix to each finding; `--json` emits the
raw issue list.

**generate_table.py**: Converts structured data (CSV or JSON) into
publication-ready Typst table code:

1. Markdown preview (stdout)
2. Typst `table(...)` code — `--style booktabs` (three-line, default) or
   `--style plain` (full grid)
3. Bilingual caption suggestion (if `--bilingual`)
4. Statistical-significance note (if `--stats`)
5. Word conversion tip

Skill-layer response: convert script output into `// TABLES (Line N) [Severity] [Priority]: ...` findings.

See also: [TABLE_GUIDE.md](../TABLE_GUIDE.md) for the full three-line table specification.
