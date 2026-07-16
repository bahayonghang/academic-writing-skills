# Example: Align-Check Only

User request:
I already wrote a cover letter; check whether any claim overshoots my manuscript before I send it.

Recommended module sequence:

1. `align-check`

Commands:

```bash
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode align-check --letter cover_letter.md --manuscript main.tex --json
```

Expected output:

- JSON list of align-check issues (or LaTeX-comment block when `--json` omitted).
- For each unsupported claim: exact letter quote, manuscript section anchor (or `none`), `claim_strength` label, `missing_evidence` array, and an `allowed_wording` rewrite that stays within manuscript scope.
- Exit code 0 (all claims supported), 1 (some `observed`/`unsupported` but no major), or 2 (at least one Major-severity issue).
