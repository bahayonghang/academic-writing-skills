# Example: Generate Nature Cover Letter

User request:
Generate a Nature submission cover letter from my LaTeX paper `main.tex`.

Recommended module sequence:

1. `generate` (with default align-check + presubmission integration)

Commands:

```bash
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode generate --manuscript main.tex --journal nature --json
# After saving the synthesized prose to draft.md, verify it:
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode align-check --letter draft.md --manuscript main.tex --json
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode presubmission --letter draft.md --journal nature --json
```

Expected output:

- The `generate` payload carries the facts blob (title, abstract, authors, contributions, headline numbers) and a deterministic draft scaffold.
- Synthesized cover letter prose using `templates/nature.md` (350-word ceiling, paradigm-shift framing).
- `% ALIGNCHECK` block surfacing any claim in the draft that does not trace to the manuscript.
- `% PRESUBMISSION` block listing missing required declarations (originality, dual-submission, competing interests, AI-use disclosure; data availability is optional for Nature and routed via the submission system).
