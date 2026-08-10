# Implement — 父任务路线图与集成验收

> 父任务不承担直接实现。实现步骤在两个子任务的 implement.md 中；本文件只保留执行顺序、
> 评审门与父级集成收口。

## 执行顺序

1. **子 1 `08-10-results-guide-zh`**（guide + experiment.md + spec-mapping + 双语文档）。
   - 评审门 G1（子 1 归档前）：`research/spec-mapping.md` 无损核对通过；guide 与
     method-description-guide 四级表映射落位；resource sync + docs build 绿。
2. **子 2 `08-10-results-checker-zh`**（checker + tests + 路由 + evals + 真实语料标定）。
   - 启动条件：子 1 的 guide 判据冻结（归档或用户确认判据不再变更）。
   - 评审门 G2（实现后）：正/反例 + 边界矩阵命中报告；误报未清零不得进路由/evals 步骤。
3. **父级集成收口**（本任务）：
   - [x] guide RA-* 映射表与脚本实际行为回核一致（不一致由子 2 修文档并提交）。
   - [x] SKILL.md / routing-rules.md / experiment.md 三处路由口径一致。
   - [x] `just ci` 全绿；`uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh`
         与 `just doc-build` 通过。
   - [x] R8 标定报告存在且效果声明遵守 UNVERIFIED 口径（父 design §7）。
   - [x] prd 跨子验收标准逐条回填。

## 集成复核记录（2026-08-10）

- 两个归档子任务与父任务的 context manifest 均通过 `task.py validate`；归档子任务
  `task.json` 状态均为 `completed`。
- 运行时 `RA_CHECKERS`、中文 guide、experiment 模块与英文 guide 均为同一八项；公开与
  运行时表面无已裁候选残留。`research/spec-mapping.md` 的 17 项 `R-*` 无缺漏。
- 修复归档后的回归测试路径：标定报告断言改读规范归档路径
  `.trellis/tasks/archive/2026-08/08-10-results-checker-zh/research/calibration-report.md`。
- 父级集成修复提交：`ce980b5`（标定测试归档路径 + checker contract 回归规则）。
- Focused RA + defensive/router/docs contracts：`84 passed`。`just ci`：Ruff 通过，Pyright
  `0 errors`（72 warnings），pytest `1497 passed`。
- 单技能与全量 resource sync 均通过（257 entries）；`just doc-build` 完成（22.43s）。

## 提交与归档策略

- git commit 统一在各子任务 Phase 3.4 执行，按子系统拆分（文档层 / 脚本+测试层 /
  路由+evals 层 / docs 联动层），scope 用 `latex-thesis-zh`；实现期间只做可回滚检查点，
  不逐步提交。
- 归档序：子 1 → 子 2 → 父。父归档前完成 Phase 3.3 spec 更新判定：RA/M 分界与保真度
  门控设计是否沉淀进 `.trellis/spec/academic-writing-skills/`（更新
  defensive-ai-rhetoric-contract.md、method-narrative-contract.md 或新增条目）。

## 回滚点

任一子任务失败按其提交序逆向 revert；两子任务无共享文件（衔接改动归子 2 提交），互不
影响。父任务无代码改动，回滚无父级动作。
