# Example: Bibliography and De-AI Review

User request:
Check the references against GB/T 7714 and see whether the introduction has an obvious AI-generated tone.

Recommended module order:
1. `bibliography`
2. `deai`

Commands:
```bash
uv run python $SKILL_DIR/scripts/verify_bib.py references.bib --standard gb7714
uv run python $SKILL_DIR/scripts/deai_check.py main.tex --section introduction
```

Expected output:
- Reference-format problems, missing fields, or suspicious entries.
- De-AI suggestions limited to visible prose, without changing citations or formulas.
