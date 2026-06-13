# Example: Optimize And Align-Check Cover Letter

User request:
Polish my draft `cover_letter.md` for an IEEE TPAMI submission, and verify it doesn't overclaim relative to `main.tex`.

Recommended module sequence:

1. `optimize` (default integration runs align-check + presubmission)

Commands:

```bash
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode optimize --letter cover_letter.md --manuscript main.tex --journal ieee-trans --json
```

Expected output:

- `% PRESUBMISSION` findings: missing declarations, length violations, banned phrase hits.
- `% ALIGNCHECK` findings: claim-accuracy issues with `claim_strength`, `allowed_wording` suggestions, and `manuscript_section_anchor` pointers.
- Section-level diff suggestions in LaTeX-comment format: `% OPTIMIZE (Line N) [Severity: Major] [Priority: P1]: ...`
- A re-run of `--mode align-check` on the proposed rewrites to verify no new unsupported claim was introduced.
