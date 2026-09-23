# Example: Structure and Consistency Check

User request:
Map the structure of this Chinese degree thesis, then check whether terminology and abbreviations are inconsistent.

Recommended module order:
1. `structure`
2. `consistency`

Commands:
```bash
uv run python $SKILL_DIR/scripts/map_structure.py main.tex
uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --terms
uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --abbreviations
```

Expected output:
- An overview of the chapter structure.
- Terminology and abbreviation drift, with locations.

## Opt-in governance, abbreviation style, and degree wording

User request:
Check banned terms, locked names, abbreviation style, and degree wording with a synthetic configuration. Do not change the old default checks.

Commands:
```bash
uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --governance --custom-terms terms.json
uv run python $SKILL_DIR/scripts/check_consistency.py main.tex --abbreviation-style
uv run python -B $SKILL_DIR/scripts/check_style_zh.py main.tex --degree-wording
```

Expected output:
- `[Script]`, Info/P3, `Meaning-Check: NEEDS-LLM`.
- Report only the local word, field, and position. Do not give a replacement sentence.
- Without those flags, the previous output stays unchanged.
