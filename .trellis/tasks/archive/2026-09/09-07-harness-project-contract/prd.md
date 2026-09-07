# 统一项目规则、依赖说明与使用许可

优先级：P1。父需求：R1/R5/R6/R7。状态：planning。

## 目标与背景

CLAUDE.md:7 写 v3.0.0/MIT；pyproject.toml:3 为 6.0.0，:24 为 MIT classifier；README.md:158、README_CN.md:142 为学术非商业。用户于本轮明确保留后者。README.md:106、README_CN.md:92 的 pdfplumber 与 pdf_parser.py:81/:124 的实际依赖不一致。AGENTS.md:15-21 的门禁说明也需对照 justfile。

## 范围

- AGENTS.md
- CLAUDE.md
- README.md
- README_CN.md
- pyproject.toml（仅 description/许可元数据）

## 前置与授权

用户批准最终计划。

当前仅规划，禁止 task.py start/实现/正式规则回写。任务树归属不代替前置条件。不同工作者不得覆盖其他子任务或用户改动。

## 验收条件

以下需求编号继承父任务的同名要求，本子任务负责其中与自身范围有关的交付。

- R1：项目结构、关键入口和共同事实准确。
- R5：文件范围、前置与检查可实施、可逐项验收。
- R6：五套工具规则/使用说明无冲突，不混同原生与已验证能力。
- R7：批准后将证实经验按适用工具回写，保留规划/实施边界。

- [x] AC1（R1/R6）：共同维护规则在 AGENTS.md，Claude 入口可加载它；不再有冲突 v3/MIT/旧 PDF 依赖声明。
- [x] AC2（R7）：保留学术用途、禁止商业使用的原有方向，不自行撰写额外法律条款或擅定许可证 ID。
- [x] AC3（R1/R5）：README 原有模型推荐两行逐字保留；版本/技能列表/门禁与真实项目一致。
- [x] AC4（R6）：适用工具标明 Claude Code/Codex/Grok Build/Kimi Code/OMP；不声称文档即运行验收。

## 非目标

不新增依赖，不发布，不改全局工具配置，不扩大到整体框架重构。未运行的能力不得写成已验证。
