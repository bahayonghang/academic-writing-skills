# 迁移研究（2026-10-15）

## 当前证据

本轮检查了当前 thesis/defense SKILL.md、qiaomu-meta-skill 及 operating-modes/gate-selection/creation-handoff，旧任务 PRD/design/prior-art、三笔功能提交 diff，以及回复脚本导入和测试 fixture 结构。

- defense 恢复基线 53c2ab5；误放提交 791f4fd / b5c47d3 / 340cc70。
- common 依赖 extract_thesis 的 cn_to_int/read_group/skip_ws；check 依赖 check_deck 的数字解析常量与 load_thesis_numbers。
- 测试 conftest 的 rebuttal_thesis 借用 defense mini-thesis；必须迁移必要 fixture。
- thesis 的“无 LaTeX 源不适用”规则须限定为正文模块，避免阻断仅评阅书 intake。

## Qiaomu 决策

- keep：现有回复的原文/覆盖/完成证据三类约束与公开合成 fixture。
- adapt：description-first 路由、根入口渐进披露、跨包独立安装门；沿用仓库适配与 eval 格式。
- reject：只复制目录、导入兄弟 defense 包、复制整套 deck 实现、全局替换历史记录、因 qiaomu 默认命名而重命名既有技能。
- invent：本次增加归属与隔离安装回归；这是迁移防回归措施，不声称新的回复算法或优于外部技能。

本次不是新技能/实质重设计，故新 prior-art discovery 不适用。旧任务 research/prior-art.md 仅作历史溯源：其候选运行未执行，部分候选仅见摘要；本轮未重新浏览候选，不宣称当前外部指标或候选质量。后续 handoff 仅列真正检查的参考材料。

## 规划时证据状态

规划检查完成。实现、迁移后单测、独立安装、文档构建、qiaomu 校验均 NOT_RUN；真实模型触发与五工具运行 UNVERIFIED。旧验证不得作为本任务完成证明。

## 并发工作区观察

规划期间 README.md 与 README_CN.md 出现本会话未写入的模型/平台推荐修改。已检查 diff 并保留；实施时只修改技能能力相关行，不覆盖这些并发编辑。

## 实施后证据

最终本地质量门已通过；详见 ../reports/check-results.md。规划时的 NOT_RUN 只描述当时状态，真实平台、模型与私有材料仍未运行。
