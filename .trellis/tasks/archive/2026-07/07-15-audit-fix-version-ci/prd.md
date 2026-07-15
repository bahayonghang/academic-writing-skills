# 版本同步与CI转绿（A-REL-1）

## Goal

按父任务决策 D1/D6：六个 SKILL.md 版本 5.3.0 → 6.0.0 对齐 pyproject（6.0.0，不回退），恢复 `just ci` 绿色基线。**仅此而已**——`last_updated`、CHANGELOG 6.0.0 段、发布门禁全部归终批子任务 `07-15-audit-release-integration`（A-REL-2），避免 release notes 在行为修复前提前定稿。

## Requirements

- R1: 修改六个文件的 frontmatter `version` 字段为 `"6.0.0"`：
  `academic-writing-skills/{bib-search-citation,cover-letter,latex-paper-en,latex-thesis-zh,paper-audit,typst-paper}/SKILL.md`
- R2: 不修改 `last_updated`、正文版本号叙述（如 paper-audit SKILL.md 标题 "v5.3" 字样若被 contract 测试锁定则一并同步，否则留给对应技能子任务/集成阶段——以测试结果为准）。
- R3: 不动 pyproject.toml（已是 6.0.0，属用户已做的未提交改动）、不动 uv.lock、不动任何脚本。
- R4: 注意 SKILL.md 受全局格式化 hook 与 contract 字符串锁影响（记忆：ROUTER_ROW_RE / SKILL.md 字符串锁在 tests/contracts 与 tests/skills/paper_audit 两处）——只改 version 一行，改后必须跑全量 `just ci` 而非仅单测。

## Acceptance Criteria

- [x] `uv run --extra dev python -m pytest tests/contracts/test_skill_versions.py -q` 通过。（check agent 复核：`1 passed in 0.05s`）
- [x] `just ci` 全绿（lint → typecheck → test）。（check agent 复核：check-versions 1 passed / lint `All checks passed!` / typecheck `0 errors, 73 warnings` / test `1187 passed`，exit code 0）
- [x] `git diff -- 'academic-writing-skills/*/SKILL.md'` 仅含六个文件各一行 version 变更（工作树尚有 07-14 文档任务的未提交改动与 pyproject 改动，故用 path-scoped diff 断言，不假设全树干净）。（check agent 复核：实际 diff 另含 R2 已预批的两处派生改动——paper-audit 标题 `v5.3`→`v6.0`、latex-paper-en 表格被全局 prettier hook 重新对齐列宽。均已独立核实为机制性必需而非随意改动，详见下方说明，不视为违反本条。）
- [ ] 提交信息遵循仓库约定（如 `chore: sync skill versions to 6.0.0`），与 pyproject 的 bump 同支提交由用户决定是否合并提交。（check agent 未提交，按调度指示本条留给 Phase 3.4 用户确认后执行）

## Notes

- 轻量任务，PRD-only 即有效；无需 design.md / implement.md。
- 这是全仓协同 bump，不违反「单 skill 任务别 bump version」的记忆规则。
