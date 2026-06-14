# Implementation Plan: latex-thesis-zh Heading Structure Optimization

Do not start implementation until the user approves this plan and `task.py start` has run.

## Phase 0: Baseline Snapshot

- [x] Confirm working tree status and preserve unrelated dirty files.
- [x] Snapshot old skill for skill-creator comparison:
  - `academic-writing-skills/latex-thesis-zh-workspace/skill-snapshot/`
- [x] Record current relevant command output:
  - `uv run pytest tests/test_latex_thesis_zh_scripts.py tests/test_latex_thesis_zh_coverage.py tests/test_skill_contracts.py tests/test_trigger_evals.py`
  - Baseline: 158 passed on 2026-06-14.

## Phase 1: Red Tests And Eval Fixtures

- [x] Add pytest coverage for heading architecture:
  - body chapter with 6+ direct `\section` headings should be flagged.
  - body chapter title missing object/problem/method should be flagged.
  - child section titles disconnected from the parent chapter should be flagged.
  - conventional chapters such as 绪论, 相关工作, 结论 should not require object-problem-method.
- [x] Add or update `latex-thesis-zh` eval fixture content if a persistent fixture is more useful than temporary test files.
- [x] Extend `academic-writing-skills/latex-thesis-zh/evals/evals.json` with a user-realistic prompt:
  - Include wording close to: "大章节的小标题数目太多，最多 5 节；大标题要体现对象、问题、方法；小标题要扣合大标题。"
  - Add objective assertions for route/module, max-5 finding, object-problem-method finding, and child-title anchoring.
- [x] Extend `academic-writing-skills/latex-thesis-zh/evals/trigger_eval.json` with:
  - Positive: Chinese LaTeX thesis chapter/section title architecture request.
  - Near negative: generic title polishing or English paper heading request that should route elsewhere.

## Phase 2: Implement Minimal Skill Changes

- [x] Update `scripts/optimize_title.py` or a clearly justified existing script path to support heading architecture diagnostics.
  - Preferred: add `--headings` without changing existing `--check` default behavior.
  - Reuse `tex_loader.assemble` and parser heading extraction.
  - Return source-aware diagnostics when possible.
- [x] Update `SKILL.md`:
  - Route 大标题/小标题/章标题/小节标题 to title/structure, and logic only when the user asks about lead-ins/mainline.
  - Add example request for this exact issue class.
- [x] Update internal references:
  - `references/writing/title-optimization.md`
  - `references/writing/structure-guide.md`
  - `references/writing/thesis-writing-guide.md` if needed.
- [x] Mirror reference changes into docs:
  - `docs/skills/latex-thesis-zh/resources/writing/...`
  - `docs/zh/skills/latex-thesis-zh/resources/writing/...`

## Phase 3: Local Verification

- [x] Run targeted tests:
  - `uv run pytest tests/test_latex_thesis_zh_scripts.py`
  - `uv run pytest tests/test_latex_thesis_zh_coverage.py`
  - `uv run pytest tests/test_skill_contracts.py`
  - `uv run pytest tests/test_trigger_evals.py`
  - Evidence: 160 passed with UTF-8 environment on 2026-06-14.
- [x] Run broader gate if changes touch docs or shared contracts:
  - `just doc-build`
  - `just ci` if feasible.
  - Evidence: `just doc-build` passed; `just ci` passed with 826 passed and 0 pyright errors on 2026-06-14.
- [x] Run skill packaging/validation check if available:
  - `python C:\Users\lyh\.skillsmanage\skills\skill-creator\scripts\quick_validate.py academic-writing-skills\latex-thesis-zh`
  - Evidence: `Skill is valid!`

## Phase 4: Skill-Creator Evaluation Loop

- [x] Create workspace:
  - `academic-writing-skills/latex-thesis-zh-workspace/iteration-1/`
- [x] For each new/changed eval case, save:
  - `eval_metadata.json`
  - with-new-skill output
  - old-skill/baseline output when supported.
- [x] Draft assertions while runs are in progress and save them to eval metadata and `evals/evals.json`.
- [x] Grade outputs:
  - Ensure `grading.json` uses `text`, `passed`, and `evidence`.
- [x] Aggregate benchmark if workspace structure supports it:
  - `python -m scripts.aggregate_benchmark academic-writing-skills/latex-thesis-zh-workspace/iteration-1 --skill-name latex-thesis-zh`
- [x] Generate human review artifact:
  - `python C:\Users\lyh\.skillsmanage\skills\skill-creator\eval-viewer\generate_review.py academic-writing-skills/latex-thesis-zh-workspace/iteration-1 --skill-name latex-thesis-zh --benchmark academic-writing-skills/latex-thesis-zh-workspace/iteration-1/benchmark.json --static academic-writing-skills/latex-thesis-zh-workspace/iteration-1/review.html`
  - Evidence: new skill passed 5/5 assertions; old skill passed 1/5 and failed the new `--headings` contract.
  - Benchmark: `academic-writing-skills/latex-thesis-zh-workspace/iteration-1/benchmark.json`
  - Review artifact: `academic-writing-skills/latex-thesis-zh-workspace/iteration-1/review.html`
- [x] Ask user to review `review.html`.
  - Deferred to final handoff with the static review artifact path.
- [x] Read `feedback.json` if provided and complete one revision loop, or record that no revision was needed.
  - No `feedback.json` was present during this run.

## Phase 5: Final Checks And Handoff

- [x] Re-run targeted pytest after any eval-driven revision.
  - Covered by the final targeted pytest run after the implementation/eval updates.
- [x] Check docs mirror consistency and orphan-reference tests.
  - Covered by `tests/test_latex_thesis_zh_coverage.py`, `tests/test_skill_contracts.py`, and `just doc-build`.
- [x] Confirm `git status --short` and list only files changed for this task.
  - Current task changes are in `academic-writing-skills/latex-thesis-zh/`, mirrored `docs/` pages/dist output, tests, eval fixture/workspace, and this Trellis task directory.
- [x] Prepare implementation summary, verification evidence, and review artifact path.

## Risk Points

- `optimize_title.py` currently uses simple title keyword heuristics; extending it to chapter headings must avoid overfitting to industrial examples only.
- Heading architecture checks may create false positives for conventional academic chapter names; keep exemptions explicit.
- If docs mirrors are missed, `test_no_orphan_reference_files` or docs review can drift.
- If skill-creator workspace outputs are too large or generated, decide before committing whether they belong in repo or should remain local artifacts.
