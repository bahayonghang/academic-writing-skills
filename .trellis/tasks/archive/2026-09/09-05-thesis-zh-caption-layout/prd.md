# 双语题注识别与图表版式验收

## Goal

消除技能推荐的双语题注误报，并把实践中的图表版式经验变成有适用条件的验收指引。父需求归属见父 PRD Task Map。

## Background

已在内存合成表格上复现：`academic-writing-skills/latex-thesis-zh/scripts/check_references.py:38` 与 `academic-writing-skills/latex-thesis-zh/scripts/check_tables.py:259` 的题注路径只认识 caption；合法 bicaption 分别产生 Major/P1 与 WARNING/P2。普通 caption 与真正缺失对照均符合现有输出。源质量规范提供多种编译后版式故障，精确源锚点见父任务 research/spec-transfer-analysis.md。

## Requirements

- R1：references 与 tables 均识别合法 caption/bicaption，维持缺题注与题注位置诊断，并保留准确源坐标。
- R2：识别遵循命令边界与注释语义；不将注释或相似名称视为实际题注，不新增任意宏别名配置或通用 TeX 解析器。
- R3：补续图目录、长表局部留白、重复子题注、表格缩放、有效图像清晰度的条件参考；实际模板命令和原图优先。
- R4：编译诊断使用现有 wrapper 与既定 recipe；只影响局部版式，视觉通过须有渲染证据，缺工具明确报告。
- R5：回归覆盖两条路径与多文件源定位；公共资源/双语/eval同步，不改真实论文、class 或其他 skill。

## Acceptance Criteria

- [x] AC1（R1、R2）：普通与双语题注（含合法短标题选项、空白换行）在 figure/table 适用路径不报缺失；真正缺失仍报。
- [x] AC2（R1、R2）：表格题注在表体下方仍报位置错误；注释伪题注和相似自定义命令不消除真正缺失。
- [x] AC3（R1、R5）：多文件输入返回源文件/行号；只修 ZH 副本，未扩大跨技能解析锁定面。
- [x] AC4（R3、R4）：指南给出五类问题的适用条件、局部处理与验收证据；不将 300 DPI 元数据等同有效分辨率，不一律替换学校题注宏。
- [x] AC5（R4）：最小合成用例用 wrapper 编译并检查续图目录/代表页面；实际看过渲染页才记视觉通过，否则保持 missing evidence，不能以单测代替。
- [x] AC6（R5）：新增 targeted 回归、两个 output 场景与一个触发正例；实际响应和逐项裁决已记录，语料契约、资源同步与 docs build 通过；不运行真实论文或新增依赖。

## Out of Scope

用户已于 2026-09-05 明确批准本任务树实施。除设计列明的目标外不清理、不增依赖、不改其他技能/论文，不提交、归档或发布。
