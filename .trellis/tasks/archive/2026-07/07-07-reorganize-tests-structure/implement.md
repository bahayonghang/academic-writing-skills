# 整理 tests 测试目录结构 — Implementation Plan

## Preconditions

- Task remains in `planning` until this plan is reviewed.
- Implementation should start only after `python ./.trellis/scripts/task.py start .trellis/tasks/07-07-reorganize-tests-structure`.

## Checklist

1. Reconfirm clean baseline:
   - `git status --short`
   - `uv run --extra dev python -m pytest --collect-only -q`
2. Create package/support directories:
   - `tests/__init__.py`
   - `tests/support/__init__.py`
   - `tests/support/paths.py`
   - target directories under `tests/skills/`, `tests/contracts/`, `tests/shared/`
3. Update `tests/conftest.py` to import path constants from `tests.support.paths` while preserving existing sys.path insertion order and runtime cleanup.
4. Move test files according to `design.md` with `git mv`.
5. Replace fragile path/import patterns:
   - `from conftest import SCRIPT_DIR_*` -> `from tests.support.paths import SCRIPT_DIR_*`
   - `Path(__file__).parent.parent / "academic-writing-skills"` -> `SKILLS_ROOT`
   - `Path(__file__).parent.parent` -> `REPO_ROOT`
   - direct script path construction should use `SKILLS_ROOT` or `SCRIPT_DIR_*`
6. Update hard-coded references:
   - `justfile` `check-versions` path
   - `CLAUDE.md` single-file examples and alignment-test references
   - comments in copied parser files that point to old alignment-test paths
   - fixture README references that point to old test files
7. Run fast discovery and targeted tests:
   - `uv run --extra dev python -m pytest --collect-only -q`
   - `uv run --extra dev python -m pytest tests/contracts/test_skill_versions.py -q`
   - `uv run --extra dev python -m pytest tests/shared/test_parsers.py tests/skills/latex_thesis_zh/test_deai_tense_zh.py tests/skills/typst_paper/test_deai_typst.py tests/skills/cover_letter/test_cover_letter_scripts.py -q`
8. Run full gates:
   - `just test`
   - `just lint`
   - `just typecheck`
   - `git diff --check`
   - If the above are green, `just ci` is optional but preferred as final evidence because it matches repository workflow.

## Review Points

- After file moves, root `tests/` should contain no root-level `test_*.py`.
- Collection count should remain 890.
- No old actionable root test paths should remain in developer instructions:
  - `rg -n "tests/test_|tests\\\\test_" .`
- No moved test should rely on depth-sensitive `parent.parent` for repo root:
  - `rg -n "Path\\(__file__\\).*parent\\.parent|parent\\.parent / \\\"academic-writing-skills\\\"" tests`

## Stop Conditions

- Stop and return to planning if adding `tests/__init__.py` causes unexpected pytest import-mode conflicts.
- Stop and revise design if path support centralization forces large behavior changes outside tests/docs/tooling.
