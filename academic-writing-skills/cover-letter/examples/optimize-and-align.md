# Example: Optimize And Align-Check Cover Letter

User request:
Polish my draft `cover_letter.md` for an IEEE TPAMI submission, and verify it doesn't overclaim relative to `main.tex`.

Recommended module sequence:

1. `optimize` (default integration runs align-check + presubmission)

Commands:

```bash
uv run python -B $SKILL_DIR/scripts/presubmission_check.py cover_letter.md --journal ieee-trans --json
uv run python -B $SKILL_DIR/scripts/align_check.py --letter cover_letter.md --manuscript main.tex --json
```

Expected output:

- `% PRESUBMISSION` findings: missing declarations, length violations, banned phrase hits.
- `% ALIGNCHECK` findings: claim-accuracy issues with `claim_strength`, `allowed_wording` suggestions, and `manuscript_section_anchor` pointers.
- Section-level diff suggestions in LaTeX-comment format: `% OPTIMIZE (Line N) [Severity: Major] [Priority: P1]: ...`
- A re-run of `align_check.py` on the proposed rewrites to verify no new unsupported claim was introduced.
