# 论文实践 spec 迁移分析

## 结论与研究边界

2026-09-05 对指定 thesis/.trellis/spec 的 28 份 Markdown 完成全文覆盖；
两位专长 Agent 分别读 9 份与 7 份 writing 文件，主线程读 backend 9 与 guides 3。
当前仓库基线为 dev / d5e5444，开始时无活动任务且工作树干净。
本轮只新增 planning 工件及研究证据，源论文只读。源内容的叙事实践可研究，
其自称“校规/权威论文/工业实证”的外部事实未经独立核验，不能照单采纳。

细化依据：[写作](writing-evidence.md)、[工程章节](engineering-evidence.md)。
研究 Agent 的建议是候选；最终范围以父/子 PRD 和 design 为准。
特别裁决：不采用工程报告提出的四个新结构字段或 R→RA 17→19 扩号；
这些内容改为既有结果指南中的自然语言核对问题，不新增 schema/检查码。
写作研究中的“网络禁用”只指该只读子任务的边界；主线程已完成公开先例检索。

## 主要发现（按影响）

| 优先级 | 发现 | 当前证据 | 规划 |
| --- | --- | --- | --- |
| P1 | 把“去防御性”解释为删真实限定，可能升级科学结论 | 源 writing/anti-defensive-hedging.md:12-27、writing/conclusion-chapter.md:31-35；目标 over-claim-guard.md:6-42 与 defensive-ai-rhetoric-contract.md:32-50 相反 | 不迁移这些改写；新增保留限定、不给机制造证据的反例 |
| P1 | 双语题注被两个 checker 当成没有题注 | check_references.py:38、check_tables.py:266；下文内存实跑 | 子任务 caption-layout |
| P1 | 工程应用章缺按需叙事指南，章号措辞有误路由风险 | references/modules/routing-rules.md:60；method-chapter-guide-zh.md:22-43 只给放置方式 | 子任务 engineering-chapter，不新增运行时分类器 |
| P1 | 展示通道筛选与统计聚合口径未分开 | 源 writing/result-analysis.md:93-134；目标 results-analysis-guide-zh.md:286-302 未覆盖 | 子任务 evidence-writing，自然语言审阅 |
| P2 | 小结三章型、摘要串/并行、综述综合/归因接口尚不细 | 写作证据 D1-D3 的源/目标锚点 | 子任务 evidence-writing，LLM-only |
| P2 | 图表验收缺少编译页与模板条件；已有文档提供笼统建议 | 源 backend/quality-guidelines.md:54-120；目标 formatting/caption-guide.md:3-18、table-guide.md:1-47 | 子任务 caption-layout 的条件指南 |

表中目标简称均位于 academic-writing-skills/latex-thesis-zh/references 或 scripts；
defensive-ai-rhetoric-contract.md 位于 .trellis/spec/academic-writing-skills。
精确路径及直接实现范围在各子任务 design.md，不以简称作为脚本入口。

## 28 份覆盖清单

源根：D:/Documents/LYH/200-Learning/00博士毕业/毕业论文/thesis/.trellis/spec。

| 源文件 | 处理 |
| --- | --- |
| writing/index.md | 读取索引/项目边界；不迁移本地章号 |
| writing/abstract.md | 补串并行模块叙事；拒绝无校规证据的缩写/字数禁令 |
| writing/anti-defensive-hedging.md | 只保留去元话语方向；拒绝删事实限定和提高确定性 |
| writing/chapter-intro-two-paragraph.md | 通用机制已有；恰好两段等条件化，不重做 |
| writing/chapter-summary.md | 补框架/方法/系统小结差异、联合任务与证据收束 |
| writing/chapter5-experiment-and-summary.md | 已覆盖实验主体；工程过渡并入工程章；私有结果与零限定拒绝 |
| writing/chapter6-platform-and-architecture.md | 抽取约束—目标—机制—证据，不迁移具体架构 |
| writing/chapter6-platform-app-and-summary.md | 抽取操作任务/分级证据，不迁移截图/现场数值 |
| writing/chapter6-service-mechanism.md | 抽取接口语义和失败边界，不造状态机或绝对安全 |
| writing/conclusion-chapter.md | 结构大体已覆盖；拒绝证据升级，不另开结论任务 |
| writing/literature-review.md | 补主题综合—代表归因—簇末比较；固定块数/配图不硬化 |
| writing/method-description.md | M-* 已覆盖；模型/符号/超参留本地 |
| writing/paragraph-transition.md | P-ARC/S-CTX 已覆盖；固定五段留本地 |
| writing/problem-statement-and-chapter-arrangement.md | 主线已有，细句式增量本批暂不扩展 |
| writing/process-and-framework-chapter.md | 过程章已有，固定章节/变量留本地 |
| writing/result-analysis.md | 补展示/统计、冻结/重算、分层缺失；RA家族不增加 |
| backend/bibliography-tooling.md | Zotero 清理 CLI 属源工程，不移植；现有保引文键原则保留 |
| backend/database-guidelines.md | 分析数据/Polars/路径是本地；第6章图不是运行数据库证据的边界可吸收 |
| backend/directory-structure.md | 本地目录与兼容包装器不移植；可编辑源与导出关系作为条件说明 |
| backend/error-handling.md | MinerU/分析 CLI 不移植；保留错误退出和编译失败证据区分 |
| backend/index.md | 读取所有权索引，不当远程后端规范 |
| backend/kiln-overview-serve.md | 本地演示 API、图表字段、阈值全部排除 |
| backend/logging-guidelines.md | 不加日志框架；报告数据范围与不混淆运行等级的原则已有/复用 |
| backend/pdf-compression.md | 压缩命令、档位和新依赖排除；不扩大为交付PDF工具 |
| backend/quality-guidelines.md | 吸收局部排版+编译页验收；项目模板、DPI数值有条件使用 |
| guides/index.md | 通用工程思考索引，不放入写作技能 |
| guides/code-reuse-thinking-guide.md | 查现有实现的研究方法；不迁入TS/事件/兼容规则 |
| guides/cross-layer-thinking-guide.md | 只借助跨资源核对方法，不迁入Trellis运行时/版本流程 |

writing 全文取证与目标对照在两份独立研究；backend/guides 的主要适配证据如下。

## backend/guides 的适配边界

- backend/database-guidelines.md:7-9,47-51：论文数据库图不是已实现 DB。可泛化为
  “论文设计图/README/演示不是部署证据”，工程指南使用该原则，不新增 ORM。
- backend/directory-structure.md:12,48：可编辑图源与导出图不同 owner。
  条件引用该关系，不固定 drawio/fig 路径，不授权自动修改图片。
- backend/logging-guidelines.md:21-36：报告样本/时间/筛选/证据范围，影子观察不能称闭环。
- backend/error-handling.md:24-37：真实编译失败必须报告；其命令是源项目命令，
  目标仍使用自己的 compile.py wrapper，不能直接复制 document.tex 与 just 配方。
- backend/quality-guidelines.md:54-82：像素/DPI/透明底/Windows 输出名与编译页双重验证；
  :84-100 长表留白和续图目录；:102-120 子题注重复和表格二次缩放。
  这些是条件操作指引，不足以要求所有模板替换宏、都设置同一个 LTpost 或硬锁300 DPI。
- backend/bibliography-tooling.md:20-24 的保留字段/原子替换属于原 CLI 合同，
  不为本任务新增 BibTeX 清理工具；其命令未经目标包实现验证，不能放入路由。
- backend/pdf-compression.md:5-8,32-46 的压缩产品是独立能力，排除。
- guides 里的 API/event/template/version 跨层规则不是论文写作内容；不原样入包。

## 已复现缺陷：双语题注

以 Python -B -X utf8 内存加载当前 ZH 两个模块，在相同表格中替换题注：
调用 ReferenceChecker.check_caption_presence(find_labels()) 与
TableChecker._check_caption_position({content, start: 1})，不创建或修改论文。

| 输入 | references | tables |
| --- | --- | --- |
| caption{Test} | 无缺题注 finding | 无题注 finding |
| bicaption{测试}{Test} | Major/P1 Missing caption，label 源行3 | WARNING/P2 No caption，表起始行1 |
| 真正无题注 | Major/P1 Missing caption | WARNING/P2 No caption |

这证明题注识别层误报；不证明真实 ysuthesis 的编译/版式，也未在本轮修复。
未来测试要覆盖完整 checker、多文件、注释/命令边界和位置，而非只复述这两个私有方法。

## 实际 CLI 与历史状态

本轮实跑 --help 确认：
compile.py 支持 --recipe xelatex-bibtex/xelatex-biber、--outdir（仅 latexmk）；
analyze_logic.py 支持 --section/--method-narrative/--paragraph-arc/--subsection-context；
analyze_experiment.py 支持 --section/--per-chapter/--results-analysis。
不杜撰 --engineering-chapter 或旧计划的 workflow CLI。

08-25-thesis-zh-quality-closure 的 task.json 标 completed，但当前 scripts 清单没有
visible_prose.py、artifacts.py、thesis_workflow.py 或 re_audit.py；本轮不研究消失原因，
只据当前文件规划。历史复用仅限避免重造/验收边界，不能把归档 PRD 当实现。

## 验证状态

- 已完成：28 文件全文覆盖、当前入口与相关源码/测试对照、三项 --help、内存题注对照、
  双目录公开先例发现和候选源阅读。
- 已完成：任务递归预检、context 验证、独立规划审阅；见 [审阅与验证记录](planning-review.md)。
- 未运行：技能实施、产品测试全量 CI、真实论文编译、模型 A/B、独立人工盲评、图表视觉、
  跨平台安装。全部保持 missing evidence，不能从本报告推定结果。
