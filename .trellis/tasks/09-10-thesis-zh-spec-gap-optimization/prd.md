# 中文论文技能最新 spec 差距分析与优化

## Goal
基于全量 spec 与现行技能证据，修正中文学位论文指南的冲突、术语/缩写误诊和编译
outdir 假失败/假成功；用最小的三个子任务完成可验证优化。

## Background
58份 spec、3,787行已经逐文件核对，详见 research/spec-coverage.md。
research/gap-analysis.md 列出 G1–G6 的现行路径、反证、复现和已覆盖能力。
规划基线 HEAD `dd9f1e2`，分支 `dev`。2026-09-10 用户明确授权实施父任务及关联子任务；
独立规划审阅和本轮递归预检均无阻断，按现有计划开始实施与验证。

## Requirements
- R1：全部 spec 均有适用性记录；参考项目经验不能不加区分地变为中文论文强制规则。
- R2：消除无来源数字、因果/首次资格捷径和体裁冲突；增强已有 logic 示例的可操作性。
- R3：术语共现不等于同义，缩写检查依据全文实际首用顺序并允许合法跨章重引，不产生错误的改名或重复定义建议。
- R4：现有 latexmk 路径统一 outdir 和 PDF 判断，不支持组合明确失败。
- R5：每项改动有正反例、实际需要的执行证据和准确覆盖声明；公开资源保持双语一致。
- R6：保持技能自包含、学术载荷和其他工作；遵循 Qiaomu 泛化门槛，不增加非必要平台、配置或依赖。

## Acceptance Criteria
- [x] AC1（R1）：58份 spec 具备行数/散列/适用性清单，已区分本库16份、通用3份及参考39份。
- [x] AC2（R2）：C1 的 AC1–AC6 全通过，旧指南冲突消除且8类实际响应经独立保真复核。
- [x] AC3（R3）：C2 的 AC1–AC6 全通过，不同概念、定义顺序与逐章重引的正确反例得到保护。
- [x] AC4（R4）：C3 的 AC1–AC6 全通过，目标目录/退出码/支持组合可由真实 wrapper 回归验证。
- [x] AC5（R5）：源/双语/manifest、just ci、完整资源检查及 docs build 通过；TeX/provider/人工/真实论文缺口单独标注。
- [x] AC6（R6）：仅批准文件变化，无新配置/依赖/路由/其他技能实现；原有用户改动保留，成果不夸称五工具或真实论文效果。

## Task Map
| 子任务 | 缺口 | 对应父需求 | 独立产物 |
| --- | --- | --- | --- |
| 09-10-thesis-zh-guidance-fidelity（C1） | G1/G2/G3 | R2/R5/R6 | 指南/示例、双语资源、定向 eval 与响应复核 |
| 09-10-thesis-zh-consistency-semantics（C2） | G4/G5 | R3/R5/R6 | 术语/缩写 checker 误诊修复及回归 |
| 09-10-thesis-zh-compile-outdir（C3） | G6 | R4/R5/R6 | outdir 命令/产物判断和回归 |
父任务拥有 R1 全量分析、共享 manifest/spec 与最终集成验收；具体顺序见 design/implement。

## Constraints and Non-goals
本轮实施范围为已审阅的三个子任务及父任务集成，通过 task.py start 激活后执行。
不修改用户论文；不扩展 M-/RA-/P-ARC/S-CTX、评分、IR、状态机、词典、安装器或五工具配置。
不升级学校规范、改许可/作者/版本、不新增依赖，不执行付费 provider、人类盲评或外部发布。
原有 .gitignore、.trellis/.template-hashes.json、skills-lock.json 保持原样。
提交、归档和发布不属当前请求。
