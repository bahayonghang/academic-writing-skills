# cover-letter

`cover-letter` prepares submission cover letters for existing LaTeX manuscripts. It drafts, reviews, and verifies the letter without editing the manuscript.

## When to Use

- Generate a first cover-letter draft from `main.tex`.
- Optimize an existing `cover_letter.md` or `cover_letter.tex`.
- Check whether letter claims overstate manuscript evidence.
- Score whether the pitch fits a bundled venue template.
- Run final declaration, length, cliché, and tone checks.

## Unified CLI

```bash
uv run python -B academic-writing-skills/cover-letter/scripts/cover_letter.py \
  --mode align-check \
  --manuscript main.tex \
  --letter cover_letter.md \
  --journal nature \
  --json
```

Supported modes:

| Mode | Required inputs | Output |
| --- | --- | --- |
| `generate` | `--manuscript main.tex` | Facts blob plus a deterministic draft scaffold |
| `optimize` | `--letter cover_letter.md`; `--manuscript` recommended | Mechanical and claim-evidence findings |
| `align-check` | `--letter cover_letter.md --manuscript main.tex` | Unsupported or over-scoped claim findings |
| `journal-fit` | `--letter cover_letter.md --journal <venue>` | HIGH / MEDIUM / LOW axis verdicts plus findings |
| `presubmission` | `--letter cover_letter.md --journal <venue>` | Declaration, length, cliché, tone, and paragraph findings |

## Output Protocol

JSON findings use:

- `severity`: `major`, `moderate`, or `minor`
- `priority`: `P1`, `P2`, or `P3`
- `source_kind`: usually `script`
- `comment_type`: `claim_accuracy`, `journal_fit`, `declaration_missing`, `presentation`, or `tone`

`journal-fit` keeps its HIGH / MEDIUM / LOW verdict scale and maps LOW to `major` / `P1`, MEDIUM to `moderate` / `P2`, and HIGH to no issue.

## Boundaries

- Only LaTeX manuscripts are supported.
- The skill does not modify `main.tex`.
- It does not write rebuttals or response-to-reviewer letters.
- It does not fetch live journal policies unless explicitly requested; bundled templates are snapshots.
