# Example: Generate Nature Cover Letter

User request:
Generate a Nature submission cover letter from my LaTeX paper `main.tex`.

Recommended module sequence:

1. `generate` (with default align-check + presubmission integration)

Commands:

```bash
uv run python -B $SKILL_DIR/scripts/extract_manuscript_facts.py main.tex --json --output facts.json
uv run python -B $SKILL_DIR/scripts/align_check.py --letter draft.md --manuscript main.tex --json
uv run python -B $SKILL_DIR/scripts/presubmission_check.py draft.md --journal nature --json
```

Expected output:

- `facts.json` with title, abstract, authors, contributions, headline numbers.
- Synthesized cover letter prose using `templates/nature.md` (350-word ceiling, paradigm-shift framing).
- `% ALIGNCHECK` block surfacing any claim in the draft that does not trace to the manuscript.
- `% PRESUBMISSION` block listing missing required declarations (originality, dual-submission, competing interests, data availability).
