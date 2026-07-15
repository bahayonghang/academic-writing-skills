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
