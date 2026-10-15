# 设计：回复能力从 defense 迁入 thesis

## 边界与恢复

采用单任务完成联合验收：移除错误归属与建立正确归属是一次原子迁移。记录三笔功能提交的文件清单后，恢复被修改的 defense 旧文件，迁走新增回复文件。共享 README、usage、manifest 按块改动，不整文件回退；旧任务档案保持原样，CHANGELOG 新增纠错说明。

## 文件映射

以下 defense/thesis 代表 academic-writing-skills 下对应技能目录。

| 来源 | 目标 |
| --- | --- |
| defense/scripts/rebuttal_{common,intake,build,check}.py | thesis/scripts 同名文件 |
| defense/references/rebuttal-{workflow,writing,gate}.md | thesis/references 同名文件 |
| defense/examples/review-response.md | thesis/examples 同名文件 |
| defense/evals/fixtures/rebuttal | thesis/evals/fixtures/rebuttal |
| defense 的回复 eval、trigger、openai.yaml 扩展 | 合入 thesis 对应文件，defense 恢复 |
| tests/skills/latex_defense_zh/test_defense_rebuttal_*.py | tests/skills/latex_thesis_zh/test_thesis_rebuttal_*.py |
| defense conftest 中回复 fixture | thesis 隔离加载 fixture，defense 恢复 |
| 双语 defense 新增回复资源 | 双语 thesis/resources 对应路径 |
| defense-rebuttal-contract.md | thesis-rebuttal-contract.md，更新 index |

## 依赖解耦

- common 所需 cn_to_int、read_group、skip_ws 最小迁入回复 common，保留原行为；不复制整个 extract_thesis。
- check 使用 check_deck 的 normalize_digits、NUMBER_EXCLUDED_RES、NUMBER_RE、load_thesis_numbers。审查最小依赖闭包后迁入回复模块，使用 thesis 自带 tex_loader，不引用 defense 包。
- 不修改公共 parser/loader 或引入跨技能绝对路径；若需要改变公共接口，先报告并更新计划。
- 原回复测试借用了 defense mini-thesis。将必要的合成论文资源放入 thesis 回复 fixture，使测试和 eval 均在本包解析，不靠安装 defense 掩盖依赖。

## 行为与路由

数据流保持：评阅书 → 归一化原文/concerns.yaml → 修改计划 → 经授权完成论文修改 → responses → R-* 核对。

thesis 根入口增加三条路由、简短输入/输出与 reference 指针；详细工作流不重复。修正无 LaTeX 源的排除范围：正文编辑需要源文件，回复 intake 允许只有评阅书；缺失论文证据时必须报告 skipped。回复模块不自行改论文、提交或编译论文。

## Qiaomu 应用

选择现有 Production 包有界迁移，不新建技能、不替换作者或许可。沿用 agents/openai.yaml 和仓库 evals/trigger_eval.json；qiaomu 适配/报告写当前任务 reports，避免第二份运行时事实源。

本轮为归属纠错，不做新技能发现或实质重设计。旧 prior-art 只作为有日期的历史来源，不声称重新验证外部候选；记录本轮实际检查的 thesis/defense/qiaomu 入口与 keep/adapt/reject。生成 skill-ir、trigger/输出/隔离安装证据及 creation-handoff。工具与既有结构不兼容时记录具体限制，不为消除报告扩张范围。

## 风险、兼容与回滚

台账 schema、输出和 R-* 不变；命令安装路径改为 thesis，不保留 defense 转发入口。原台账 owner 已为 latex-thesis-zh。风险为数字提取行为漂移、测试模块缓存串包、双语资源残留，分别由原回归、隔离子进程和资源门验证。

回滚仅处理本任务增量，不 reset 分支、不改写提交。实施期间出现用户改动时逐文件保护。验证失败不放宽 R-* 或忽略资源错误。
