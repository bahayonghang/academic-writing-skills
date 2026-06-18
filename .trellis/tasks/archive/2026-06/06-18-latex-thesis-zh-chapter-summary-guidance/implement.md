# Implementation Plan

## Assumptions

- The user wants a planning task first; implementation starts only after an
  explicit "开始实施/continue" style instruction.
- The desired default follows the screenshot: a single compact prose paragraph.
- School-specific rules override the default when the user provides them.

## Steps

1. Update routing in `SKILL.md`.
   - Add "本章小结/章节小结/章末小结/小结写法" to triggering/routing language.
   - Keep routing under existing `logic` + thesis-writing guide.
   - Verify: `tests/test_skill_contracts.py::test_skill_frontmatter_description_stays_within_runtime_limit`.

2. Add source guidance to `references/writing/thesis-writing-guide.md`.
   - Add a "正文章末小结（单段收束式）" section after "正文章引言".
   - Include content order, one-paragraph default, final-conclusion distinction,
     positive/negative examples, and claim-safety rules.
   - Verify by reading the rendered Markdown and checking no unsupported
     citations/data are introduced.

3. Sync structure-guide and docs mirrors.
   - Cross-link from the recommended chapter structure and checklist.
   - Mirror source reference changes into `docs/skills/...` and `docs/zh/...`.
   - Verify: `just doc-build` if docs changes are non-trivial; otherwise
     targeted Markdown/link inspection plus `just doc-build` before completion.

4. Add eval coverage.
   - Add one `evals.json` case that asks for a chapter-summary rewrite/check
     and asserts "logic" route, "本章小结", compact prose/single paragraph
     language, core components, and no fabricated citations.
   - Add trigger eval should-trigger examples for chapter summaries.
   - Preserve near-miss negatives for English papers, Typst, audit, and pure
     bibliography tasks.
   - Verify: `uv run pytest tests/test_trigger_evals.py tests/test_skill_contracts.py`.

5. Run targeted validation.
   - `uv run pytest tests/test_skill_contracts.py tests/test_trigger_evals.py tests/test_latex_thesis_zh_scripts.py`
   - `just doc-build` if docs mirrors changed.
   - If many docs/source files changed, finish with `just ci` if runtime is
     acceptable.

## Rollback Points

- If frontmatter description length fails, move trigger details from
  description to body routing rules.
- If eval assertions are too brittle for paragraph counting, assert explicit
  "单段/一段" guidance rather than measuring model output line breaks.
- If docs build fails for unrelated dirty-tree changes, record the unrelated
  failure and still run targeted tests for touched files.
