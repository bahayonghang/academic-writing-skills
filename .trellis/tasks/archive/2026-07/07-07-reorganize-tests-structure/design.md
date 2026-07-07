# 整理 tests 测试目录结构 — Design

## Design Summary

采用一层语义分组，而不是按每个脚本模块继续细分。原因是当前问题主要是 41 个根测试文件平铺导致查找困难；过深目录会增加移动成本与路径适配风险，却不能显著提升维护体验。

最终结构：

```text
tests/
  __init__.py
  conftest.py
  fixtures/
  support/
    __init__.py
    paths.py
  skills/
    cover_letter/
    latex_paper_en/
    latex_thesis_zh/
    paper_audit/
    typst_paper/
  contracts/
  shared/
```

## File Move Map

### `tests/skills/latex_paper_en/`

- `test_abstract.py`
- `test_citation_styles.py`
- `test_deai_overclaim.py`
- `test_deai_tense.py`
- `test_latex_paper_en_audit.py`
- `test_latex_paper_en_scripts.py`
- `test_tables.py`

Rationale: these test the `latex-paper-en` script set directly or rely on EN as the canonical script copy.

### `tests/skills/latex_thesis_zh/`

- `test_deai_tense_zh.py`
- `test_latex_thesis_zh_checker_precision.py`
- `test_latex_thesis_zh_coverage.py`
- `test_latex_thesis_zh_gb7714.py`
- `test_latex_thesis_zh_multifile.py`
- `test_latex_thesis_zh_scripts.py`

Rationale: these target the ZH skill and must preserve importlib path-loading guards.

### `tests/skills/typst_paper/`

- `test_deai_typst.py`
- `test_typst_paper_coverage.py`
- `test_typst_paper_scripts.py`

Rationale: these target the Typst skill and must preserve importlib path-loading guards.

### `tests/skills/paper_audit/`

- `test_check_citations.py`
- `test_html_render.py`
- `test_i18n.py`
- `test_literature_search.py`
- `test_paper_audit.py`
- `test_paper_audit_checkpoint.py`
- `test_paper_audit_deep_review.py`
- `test_paper_audit_integration.py`
- `test_paper_audit_pre_submission.py`
- `test_paper_audit_revision_trajectory.py`
- `test_paper_audit_synthesis.py`
- `test_workspace_layout.py`

Rationale: these primarily exercise `paper-audit` scripts, paths, reports, i18n, workspaces, and audit modes.

### `tests/skills/cover_letter/`

- `test_cover_letter_align_check.py`
- `test_cover_letter_presubmission.py`
- `test_cover_letter_scripts.py`

Rationale: these target the cover-letter skill and use temporary importlib module loading to avoid parser shadowing.

### `tests/contracts/`

- `test_claim_evidence_contract.py`
- `test_deai_alignment.py`
- `test_parsers_alignment.py`
- `test_skill_contracts.py`
- `test_skill_versions.py`
- `test_trigger_evals.py`
- `test_venue_templates_layout.py`
- `test_writing_modules_alignment.py`

Rationale: these assert repo-wide packaging, cross-skill alignment, versioning, templates, trigger evals, and copied-module drift contracts.

### `tests/shared/`

- `test_en_family_parsers_multifile.py`
- `test_parsers.py`

Rationale: these cover parser and loader behavior shared by multiple writing skills, even when the canonical import comes from EN.

## Path And Import Strategy

Add `tests/support/paths.py`:

- `TESTS_ROOT`
- `REPO_ROOT`
- `SKILLS_ROOT`
- `SCRIPT_DIR_EN`
- `SCRIPT_DIR_ZH`
- `SCRIPT_DIR_TYPST`
- `SCRIPT_DIR_AUDIT`
- `SCRIPT_DIR_COVER_LETTER`

Then update `tests/conftest.py` to import those constants instead of owning path construction. `conftest.py` remains responsible for:

- disabling bytecode writes;
- mutating `sys.path` in the current established order;
- cleaning runtime artifacts around tests.

Moved tests should import constants from `tests.support.paths`, not `conftest`. This separates stable path data from pytest plugin side effects and keeps pyright imports predictable after files move into subdirectories.

## Compatibility Notes

- Pytest will still recurse because `testpaths = ["tests"]` and `python_files = ["test_*.py"]` already cover nested files.
- `just test` remains valid because it passes the `tests/` directory, not individual root files.
- `just check-versions` must be changed from `tests/test_skill_versions.py` to `tests/contracts/test_skill_versions.py`.
- Comments and docs that point at old single-file paths should be updated where they are actionable developer instructions.
- The zh/typst/cover-letter importlib loaders must not be "simplified"; the project spec records that they protect against testing the wrong script copy.

## Risks

- Moving files with hard-coded `Path(__file__).parent.parent` is the main breakage risk.
- Adding `tests/__init__.py` changes import names during pytest collection, but gives stable `tests.support.paths` imports and avoids collision with unrelated site-packages named `tests`.
- Updating all references mechanically is tempting, but comments sometimes refer to historical tests. Each change should preserve meaning rather than blindly rewriting text.

## Rollback

All moves are structural and should be done with `git mv`. Rollback is a reverse move plus removing `tests/support/` and restoring `justfile` / doc references. No product code should need rollback.
