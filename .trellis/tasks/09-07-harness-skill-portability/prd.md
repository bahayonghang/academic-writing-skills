# 规范 Skill 跨 Harness 委派与模型分工

优先级：P2。父需求：R4/R5/R6/R7。状态：planning。

## 目标与背景

SKILL 的 allowed-tools 包含 Claude 风格工具字面，paper-audit lane 模板及脚本 fallback 与 harness 实际委派是不同证据。现有 trigger_eval 测试只验证语料，不能证明真实多工具触发/独立 reviewer。

## 范围

- academic-writing-skills/{latex-paper-en,latex-thesis-zh,typst-paper,bib-search-citation,cover-letter,paper-audit}/SKILL.md
- academic-writing-skills/paper-audit/references/workflow-detail.md
- academic-writing-skills/paper-audit/references/SUBAGENT_TEMPLATES.md
- academic-writing-skills/paper-audit/agents/synthesis_agent.md
- academic-writing-skills/paper-audit/references/editorial_decision_standards.md
- 对应 docs/skills 与 docs/zh/skills 入口页和上述资源镜像
- docs/resource-manifest.json

## 前置与授权

C4 完成；用户批准。

当前仅规划，禁止 task.py start/实现/正式规则回写。任务树归属不代替前置条件。不同工作者不得覆盖其他子任务或用户改动。

## 验收条件

以下需求编号继承父任务的同名要求，本子任务负责其中与自身范围有关的交付。

- R4：强模型负责判断与复核，便宜模型执行有明确边界。
- R5：文件范围、前置与检查可实施、可逐项验收。
- R6：五套工具规则/使用说明无冲突，不混同原生与已验证能力。
- R7：批准后将证实经验按适用工具回写，保留规划/实施边界。

- [x] AC1（R6）：六技能在 standalone 包内即可理解如何把读/搜索/执行/委派映射到当前工具；Claude 元数据不被宣称为其他平台强制权限。
- [x] AC2（R6/R7）：paper-audit 多 lane 的输入、文件范围、输出/provenance、顺序执行与真实独立审查区别明确。报告/overall_assessment 必须用正文注明 native delegated 或 sequential single-agent；后者不得称 independent panel，CONSENSUS 标签仅表示跨视角一致，不作为独立审稿人共识证据。
- [x] AC3（R4/R5）：强模型保留根因/学术判断/最终验收，低成本执行包具备限定文件、失败升级条件及必须运行的测试。
- [x] AC4（R5/R7）：不改变审稿评分/gate/语义边界，不伪造模型调用；所有公开资源与两语镜像/manifest 同步。

## 非目标

不新增依赖，不发布，不改全局工具配置，不扩大到整体框架重构。未运行的能力不得写成已验证。
