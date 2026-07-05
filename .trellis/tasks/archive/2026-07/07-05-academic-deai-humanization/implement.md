# Implementation Plan

Do not start implementation until the user approves this planning scope and
`task.py start` is run.

## Checklist

1. Baseline verification
   - Run targeted de-AI tests for current behavior.
   - Verify the working tree only contains this Trellis task before edits.

2. Update thesis de-AI guidance
   - Edit `latex-thesis-zh/references/modules/deai.md`.
   - Edit `latex-thesis-zh/references/deai/guide.md`.
   - Add the academic humanization contract and structure-shell checklist.
   - Keep policy/disclosure and anti-detector-evasion language intact.

3. Add conservative Chinese structure-shell detection
   - Update `latex-thesis-zh/scripts/deai_check.py`.
   - Add categories and suggestion keys with false-positive checks where cheap.
   - Prefer LOW severity/source-preserving suggestions.
   - Do not modify `deai_batch.py` unless it consumes category names directly.

4. Add thesis tests and evals
   - Add unit tests for:
     - binary contrast shell;
     - fake insight marker;
     - lecture colon;
     - vague referent or vague comparative;
     - a legitimate evidence-bearing contrast that should not be treated as a
       hard rewrite command.
   - Add or update `latex-thesis-zh/evals` for prompts asking to reduce AI flavor
     while preserving academic logic and norms.

5. Add Typst parity
   - Edit `typst-paper/references/modules/DEAI.md`.
   - Edit `typst-paper/references/DEAI_GUIDE.md`.
   - Update `typst-paper/scripts/deai_check.py` with bilingual structure-shell
     checks that preserve Typst syntax.
   - Add tests in `tests/test_typst_paper_scripts.py`.
   - Add or update `typst-paper/evals/evals.json` for Chinese/bilingual de-AI
     requests that preserve `@cite`, labels, and math.

6. Add English paper parity
   - Edit `latex-paper-en/references/modules/deai.md`.
   - Edit `latex-paper-en/references/deai/guide.md`.
   - Update `latex-paper-en/scripts/deai_check.py` with English rhetorical
     scaffold checks rather than Chinese phrase hard bans.
   - Add tests in `tests/test_latex_paper_en_scripts.py`.
   - Add or update `latex-paper-en/evals/evals.json` for claim-evidence-first
     de-AI requests.

7. Docs mirror
   - If source reference files are mirrored under `docs/skills` or `docs/zh/skills`,
     update the mirrors consistently.

8. Verification
   - Run focused tests:
     - `uv run pytest tests/test_latex_thesis_zh_scripts.py tests/test_latex_thesis_zh_checker_precision.py`
     - `uv run pytest tests/test_typst_paper_scripts.py tests/test_typst_paper_coverage.py`
     - `uv run pytest tests/test_latex_paper_en_scripts.py tests/test_latex_paper_en_audit.py`
   - Run contract checks:
     - `uv run pytest tests/test_skill_contracts.py`
   - Run broader gate because three skills/docs change:
     - `just ci`

9. Final review
   - Inspect `git diff --check`.
   - Confirm no generated detector-evasion claims or fabricated evidence language.
   - Update this task if scope changes during implementation.

## Rollback Points

- After docs-only edits, before script changes.
- After `latex-thesis-zh` script/tests pass, before Typst alignment.
- After Typst script/tests pass, before English alignment.
- Before docs mirror sync if the mirror scope becomes larger than expected.

## Risky Files

- `academic-writing-skills/latex-thesis-zh/scripts/deai_check.py`
- `academic-writing-skills/typst-paper/scripts/deai_check.py`
- `academic-writing-skills/latex-paper-en/scripts/deai_check.py`
- mirrored docs under `docs/skills/**` and `docs/zh/skills/**`

## Validation Notes

The success condition is not “less AI detector score.” The success condition is:
the skill can identify and explain AI-flavored rhetorical shells while preserving
academic content, source syntax, and evidence boundaries.
