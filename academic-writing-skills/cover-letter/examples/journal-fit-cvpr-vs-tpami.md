# Example: Journal-Fit CVPR Vs TPAMI

User request:
Is my cover letter framed for CVPR, or should I retarget to TPAMI?

Recommended module sequence:

1. `journal-fit` for both venues; compare verdicts.

Commands:

```bash
uv run python -B $SKILL_DIR/scripts/journal_fit_check.py cover_letter.md --venue cvpr --json
uv run python -B $SKILL_DIR/scripts/journal_fit_check.py cover_letter.md --venue ieee-trans --json
```

Expected output:

- Per-axis HIGH/MEDIUM/LOW for each venue across `scope_fit`, `novelty_framing`, `evidence_density`, `format_compliance`.
- Concrete quote-level evidence per axis.
- Per-axis suggestions to push the verdict up a tier.
- Overall verdict per venue + a recommendation on which venue better matches the current letter framing.
