# 发布集成与文档收尾（A-REL-2 + 父任务集成门禁）

## Goal

本任务树的**终批**子任务：其余七个行为修复子任务全部完成归档后执行。承接原父任务 PRD 中的全部可执行集成工作，使父任务保持纯汇总定位（仅持有需求集、任务地图、跨子验收）。

## 前置条件（全部满足才可 start）

- 07-15 树其余七个子任务（version-ci / latex-paper-en / latex-thesis-zh / paper-audit / typst-paper / bib-search / cover-letter）全部 completed 并归档。
- （已满足）`07-14-refactor-docs-from-latest-skills` 树已全部归档（2026-07-15 复核）。其文档以**当时的** SKILL.md 为事实源——本树行为修复对 SKILL 路由/能力文案的后续改动所产生的概览漂移，由本任务 R4 承接。

## Requirements

- R1（A-REL-2a）：六个 SKILL.md 的 `last_updated` 统一更新为本任务执行日。
- R2（A-REL-2b）：`docs/CHANGELOG.md` 撰写 6.0.0 段——内容以七个子任务实际落地的修复为准（按 A-* finding ID 归纳），不提前定稿、不写未落地项。
- R3：跨子任务集成复查——parsers/deai 对齐锁副本一致（en/audit/cover-letter/typst/zh 按各 design.md 声明的锁行核对）、evals/trigger_eval 仍绿。
- R4：文档同步与一致性（三件）：
  - R4a 资源同步检查器通过（docs 双语契约 `docs-bilingual-resources.md`）；
  - R4b **六技能双语概览/usage 页与最终 SKILL.md 路由的一致性复查并更新**——凡本树子任务改动了 SKILL 路由表/能力文案（至少 PA/ZH 会改），对应 EN + zh 两侧 usage/概览页须同步（契约明文：router 变化必须同步双语 usage.md；资源 checker 捕获不了概览漂移，须逐技能人工对照）；
  - R4c `just doc-build` 通过。
- R5：不修改任何行为代码；若集成复查发现行为缺陷，回开对应子任务而不是在本任务内修。

## Acceptance Criteria

- [x] `git diff -- 'academic-writing-skills/*/SKILL.md'` 仅含六处 `last_updated` 变更。
- [x] CHANGELOG 6.0.0 段的每一条都能对应到已归档子任务的 commit。
- [x] `just ci` 全绿；`just doc-build` 成功。
- [x] 双语资源检查器（docs 契约）通过。
- [x] 六技能 EN/zh 概览与 usage 页与最终 SKILL.md 路由逐一对照无漂移（router 行、模块能力、flag 列表），漂移处已更新并纳入拟提交分组。
- [x] 父任务可据此归档：父 PRD 验收清单逐项勾选。

## 分类说明

轻量-plus 任务：无技术设计决策（不需要 design.md），但有顺序敏感的操作清单 → 附 `implement.md`。
