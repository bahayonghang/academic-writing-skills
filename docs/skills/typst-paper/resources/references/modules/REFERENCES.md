# Module: References

**Trigger**: reference, cross-reference, 引用, 图表引用, label, 编号, undefined reference, missing caption

## Commands

```bash
uv run python $SKILL_DIR/scripts/check_references.py main.typ
uv run python $SKILL_DIR/scripts/check_references.py main.typ --bib references.bib
uv run python $SKILL_DIR/scripts/check_references.py main.typ --json
```

> Available flags: `--bib` (bibliography file for citation-key resolution),
> `--json`. When `--bib` is omitted the script auto-detects
> `#bibliography("...")` in the source.

## Details

`check_references.py` validates figure/table/equation cross-references in a
Typst paper. In Typst, `@key` is BOTH a citation and a cross-reference, so the
checker reconciles each `@key` against:

- `<key>` label definitions found in the source, and
- the bibliography key set (`--bib` or the auto-detected `#bibliography(..)`),

and only flags a reference as undefined when it is neither a known label nor a
known citation. Colon-style labels (`<fig:arch>`, `@fig:arch`) are parsed as one
token.

Checks:

- Undefined references / citations (Critical, P0)
- Unreferenced `fig`/`tab`/`eq` labels (Minor, P2)
- Missing captions inside `#figure(...)` blocks — both `caption: [..]` and
  `caption: "..."` forms are recognized (Major, P1)
- Reference-before-definition ordering (Minor, P2)
- Numbering gaps in numbered label series (Minor, P2)

Skill-layer response: present findings as `// REFERENCES (Line N) [Severity] [Priority]: ...`.
