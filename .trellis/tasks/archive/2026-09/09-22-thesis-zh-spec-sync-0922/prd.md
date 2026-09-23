# latex-thesis-zh：论文 spec 增量同步

## Goal

把论文写作规范中可泛化的术语、数字公式、引用、结果核对、学院清单和指南规则补入 latex-thesis-zh。
父任务只拥有来源核对、依赖、共享约束和集成验收；产品交付由六个子任务承担。
本轮只完善规划；全部 task.json 保持 planning。

## Background / Confirmed Facts

- 产品基线：dev / 88bd045；“工作树干净”指创建本任务树之前。当前七个任务目录为未跟踪规划产物，不是产品实现。
- 论文来源有 34 份 Markdown + 1 份 JSON，学院材料 799 行、111 个编号项。源路径和原始差距记录见 research/gap-analysis.md；修订后的事实、来源边界见 research/planning-evidence.md，后者纠正原始分析的推论。
- academic-writing-skills/latex-thesis-zh/scripts/check_consistency.py:106 已接受 zh/en 同义组，不支持禁用词治理；check_style_zh 的“绝对”子串规则见 academic-writing-skills/latex-thesis-zh/scripts/check_style_zh.py:312。
- academic-writing-skills/latex-thesis-zh/scripts/check_spec.py:742 的 module 分支只输出 MODULE 和命令，不执行模块。format 路由存在，缺的是学院公式专项覆盖。
- academic-writing-skills/latex-thesis-zh/references/formatting/formula-guide.md:34 的推导链采用重复关系符；首段已声明校规优先。修订补学校口径，不能将 AMS 推导链一概判错。
- 既往 09-05、09-10、09-13、09-19、09-20 的交付不重做；旧同义漂移、UP-*、PR-*、CI-*、RA-*、CF-* 契约保持。
- 2026-09-22 用户确认保守范围：明确可判项 opt-in；PDF 页底留白 MANUAL；歧义数字 NEEDS-LLM。不增加 PDF 输入、依赖或自动版心判断。

## Requirements

- R1: C1 提供项目自带术语治理、显式缩写体例检查和程度词候选；只报告，不选择或应用替换。豁免保持源位置且不污染旧术语路径。
- R2: C2 提供明确启用的学院源码体例检查；区分学院原文、项目源码约定和启发式。数字、公式、表身、中文题注有支持范围和正反例；旧学校模板不改。
- R3: C3 提供作者引述位置、重引页码候选、文献字段提示和综述递进词提示。保护完整作者数据；不迁移项目图内引用豁免、不编造页码。
- R4: C4 对同章、同指标/对象/评价集/单位的可唯一绑定记录核对表/正文/小结；缺表、缺表面、不同终值分别报告；不以“任意同数”证明一致。无法绑定时 NEEDS-LLM，不推断哪处正确。
- R5: C5 新增 YSE-001..YSE-111 学院模板。完整保留每项子要求和学位适用范围；复合项不冒充全项自动 PASS；页底留白与第111项人工记录栏 MANUAL。
- R6: C6 完成方法表达、三类防御性说明、结构桥接、摘要引号、标题符号五个指南主题及触发路由；本轮全为文档/LLM 层，不增加 CF-METAPHOR 或 T-QUOTE。
- R7: 新行为显式启用，旧调用输出保持；不改真实论文、其他技能、parsers.py、deai_check.py 或 tex_loader.py；公开示例合成，公开学院名称/来源可保留，禁止私有作者/论文原句/实验结果。修改公开能力同步 README 双语、相关 usage/index、资源双语镜像、manifest 与 evals；不添加依赖。

## Task Map

| 顺序 | 子任务 | 父需求 | 依赖与交付 |
| --- | --- | --- | --- |
| C1 | 09-22-thesis-zh-term-governance | R1、R7 | 治理 JSON、--abbreviation-style、--degree-wording |
| C2 | 09-22-thesis-zh-number-equation-table | R2、R7 | C1 完成后接手 check_style_zh；统一 --school yanshan-ee-2025 |
| C3 | 09-22-thesis-zh-citation-literature | R3、R7 | C2 后接手 check_references；独立 opt-in 引用/文献/综述检查 |
| C4 | 09-22-thesis-zh-cross-surface-numbers | R4、R7 | C3 后串行交付；独立 experiment 路径，不依赖 C1 治理配置 |
| C5 | 09-22-thesis-zh-college-checklist-2025 | R5、R7 | C2/C3 CLI 已验证；C4 后接入学院模板与 MODULE 提示 |
| C6 | 09-22-thesis-zh-method-hedging-guides | R6、R7 | C5 后整合指南和最终路由；不再依赖 C1 的 banned 词表 |

串行 C1 → C2 → C3 → C4 → C5 → C6，所有权按时段移交，绝不并发写公共文件。
详细文件边界与验收真源见 design.md；每个子任务需独立质量门禁。

## Acceptance Criteria

- [ ] AC1 (R1): 新开关下，治理候选/锁定变体/豁免、缩写三类问题与反例、程度词及合法搭配均满足 C1 矩阵；旧 JSON 与默认调用保持。
- [ ] AC2 (R2): 学院模式百分号/摄氏度/平面角、数字分组、公式续行和中文题注/表身各有正反例；generic 默认与旧 yanshan.md 不变；指导示例明确学校适用边界。
- [ ] AC3 (R3): 位置候选移动后消失、重引支持/不支持语法分明、缺字段只提示、完整作者不报格式违规；阈值5/7仅新开关下生效并标未标定。
- [ ] AC4 (R4): 唯一绑定三处相等无差异；不同终值和缺表面能检出；其他指标碰巧同数不算匹配；未绑定、单位不明等只报 NEEDS-LLM；不产生修正数字。
- [ ] AC5 (R5): 博士/硕士均恰有111条状态且与来源逐项对应；混合学位行不跳过硕士；复合项不部分 PASS；MODULE 含正确 opt-in 参数；第87/111项 MANUAL。
- [ ] AC6 (R6): 五主题各有合成正反例与人工判读边界；8条方法约束与既有 PR/M/UP 分工一致；路由和两语公开说明完整；CF/T 脚本与码集不变。
- [ ] AC7 (R7): 每子任务目标测试、just ci、完整资源同步与 docs build 通过；默认回归覆盖本次受影响入口；冻结文件与旧模板无差异；公开文件无私有语料，五宿主/真实论文效果继续 UNVERIFIED。

## Key Decisions / Out of Scope

2026-09-22：按用户确认采用保守自动化。保留六子结构；使用既有 loader/parser 和局部函数，
不新建通用规则引擎、IR、评分、schema 版本层或兼容迁移层。
旧调用保持是本任务明确验收约束；新开关不增加旧输出注释。
不修改/编译论文，不联网核验出版事实，不做 PDF 几何自动化、不改旧 YS 编号或文件。
常规判断和既有边界已收敛；进入实施仍需用户针对这版规划明确授权。
