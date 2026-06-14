# Current latex-thesis-zh Gap Notes

Inspected files:

- `academic-writing-skills/latex-thesis-zh/SKILL.md`
- `academic-writing-skills/latex-thesis-zh/references/writing/structure-guide.md`
- `academic-writing-skills/latex-thesis-zh/references/writing/title-optimization.md`
- `academic-writing-skills/latex-thesis-zh/references/writing/thesis-writing-guide.md`
- `academic-writing-skills/latex-thesis-zh/scripts/optimize_title.py`
- `academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py`
- `academic-writing-skills/latex-thesis-zh/evals/evals.json`
- `academic-writing-skills/latex-thesis-zh/evals/trigger_eval.json`
- `tests/test_latex_thesis_zh_scripts.py`
- `tests/test_latex_thesis_zh_coverage.py`
- `tests/test_skill_contracts.py`
- `tests/test_trigger_evals.py`

## Existing Strengths

- `SKILL.md` already has module routing for `title`, `structure`, and `logic`.
- `structure-guide.md` already says every chapter/section/subsection should have a lead-in paragraph.
- `thesis-writing-guide.md` already defines a thesis mainline:
  - 研究背景 -> 技术瓶颈/研究空白 -> 科学问题 -> 本文方法/章节工作 -> 实验证据 -> 贡献闭合 -> 局限与展望
- `analyze_logic.py` already checks:
  - missing heading lead-ins
  - weak heading lead-ins
  - chapter intro bridging
  - introduction funnel
  - chapter mainline breaks
  - abstract/contribution/conclusion misalignment
- Tests already cover heading parsing, missing lead-ins, weak lead-ins, and chapter-intro checks.

## Gaps For This Task

- `optimize_title.py` currently focuses on the thesis title, not the full chapter/section title architecture.
- `title-optimization.md` describes thesis-title criteria but not body-chapter title criteria.
- `structure-guide.md` does not yet state "direct sections per chapter should default to <= 5".
- No current pytest assertion checks:
  - a body chapter title missing object/problem/method facets
  - more than 5 direct sections under one chapter
  - section titles that do not anchor to the parent chapter title
- `evals/evals.json` lacks a prompt matching the user's current wording:
  - "大章节的小标题数目太多"
  - "大标题没有体现对象问题方法"
  - "小标题要和上面的大标题扣上"
- `trigger_eval.json` lacks a positive trigger for "大标题/小标题/章节标题结构" and a near negative for generic title polishing outside a Chinese LaTeX thesis project.

## Preferred Integration Point

Do not add a separate public module unless implementation shows it is necessary.

Recommended integration:

- Extend `title` module with a chapter-heading architecture option, e.g. `--headings`.
- Keep `structure` responsible for structure maps and section counts.
- Keep `logic` responsible for lead-ins and mainline closure.
- In `SKILL.md`, route "大标题/小标题/章标题/小节标题" to `title` plus `structure`, and optionally `logic` when the user also asks about论证主线/衔接.

This keeps the public module inventory stable and avoids adding another router row that overlaps with existing `title`, `structure`, and `logic`.
