# 来源与先例研究（2026-09-20）

本文按 qiaomu-meta-skill 的先例发现流程记录：需求来源、网络来源、技能目录先例、keep / adapt / reject / invent 综合，以及证据标签。指南正文只引用本文"可引用来源"节中带 URL 的条目。

## 1. 需求来源

用户于 2026-09-20 提供一张表格（截图，标题"2. 各级段落分别承担什么任务"），三列：位置 / 合适职责 / 不必反复做的事，六行：

| 位置 | 合适职责 | 不必反复做的事 |
| --- | --- | --- |
| 章引言 | 本章问题、与前章接口、本章关键方案 | 重新介绍整个行业背景；详列每个小节顺序 |
| 含子节的总节导语 | 界定本节对象或给简短阅读地图 | 重复整章问题和全方法链 |
| 具体方法小节首段 | 直接说明本模块输入、作用或未解决的接口 | 再一次列所有研究挑战 |
| 公式后段落 | 解释符号、关键机制、边界条件 | 按公式顺序把每个乘加操作再译成一遍文字 |
| 实验结果段 | 数值差异、图示现象、适度解释 | 把所有表格单元逐项抄读，再为每个基线推测失败机理 |
| 本章小结 | 新方法、最重要结果、必要接口 | 新增论证；再次列完整训练／部署流程 |

用户只提供了其总结的第 2 节。第 1 节与后续节内容未知，本任务不推断、不补写。用户声明目的："主要是防止结构重复与写作冗余"。

## 2. 可引用来源（带 URL，指南可引用）

| # | 来源 | 采纳要点 | 证据标签 |
| --- | --- | --- | --- |
| W1 | 知学术《论文跨章节重复表述？去冗余的 4 步清单》2026-09-09，https://www.openxueshu.com/archives/fourstep-checklist-for-eliminating-redundant-expressions-across-chapters-in-a-thesis | 四类重复打标（同义复述 / 结论重述 / 材料复用 / 概念重复定义）；"信息增量"两问（是否提供前文没有的新信息；删掉是否断论证）；完整定义只在首次登场处，其余改为指代式衔接（"具体口径见第 X 节"）；章节小结的总结性回顾属结构功能，压缩保留而非删除 | 设计依据（商业博客，含产品推广；只取方法论） |
| W2 | 维普论文知识《论文各部分功能与避免重复》，https://www.vpcs.info/knowledge/id/72 | 各章"只写……不写……"功能定位；雷区表（绪论 vs 综述、结果 vs 讨论、讨论 vs 结论）；"功能定位法：两段作用相同就合并或删除一段"；口诀"结果只报是什么，讨论再讲为什么" | 设计依据 |
| W3 | 维普论文知识《结构清晰与叙事逻辑》，https://www.vpcs.info/knowledge/id/73 | 章节开头路标句与结尾回顾句示例；引言结尾路线图；每段首句为中心句 | 设计依据 |
| W4 | 万维书刊《学位论文开头/结尾的八种写法》（转述 Desmond Thomas《博士生写作手册》），http://eshukan.com/academic/show.aspx?id=151354 | 章引言四种起法（开门见山 / 引语 / 回顾前文 / 轶事）；章结尾：只对特别复杂的章复述要点，其他章无必要；"以上说明了什么"；预告下一章须兑现 | 设计依据 |
| W5 | Perry, *A Structured Approach to Presenting PhD Theses*（NUS 镜像 https://www.ece.nus.edu.sg/stfpage/eleamk/phd/phdth1.html ；PDF https://www.aral.com.au/resources/cperry.pdf ） | "Each chapter should also have a concluding summary section which outlines major themes established in the chapter, without introducing new material"；每章末段总结本章关键成果 | 设计依据（本章小结"不新增论证"的外部出处） |
| W6 | ICMJE Recommendations, Manuscript Preparation, https://icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html | Results: "Do not repeat all the data in the tables or figures in the text; emphasize or summarize only the most important observations"；Discussion: "Do not repeat in detail data or other information given in other parts of the manuscript" | 设计依据（实验结果段"不逐单元抄读"的外部出处） |
| W7 | Ghaffari 等, *The Principles of Biomedical Scientific Writing: Results*, PMC6635678, https://pmc.ncbi.nlm.nih.gov/articles/PMC6635678/ | 不复述表中全部数字；可重复一两个关键值以强调；不用表题/图题作主题句；重要结果放段首 | 设计依据 |
| W8 | Editage《How to Write the Results Section》2026-06-22，https://www.editage.com/blog/results-section-research-paper/ | 常见错误："Repeating in prose every number already in a table, instead of highlighting key values" | 佐证 |
| W9 | CASRAI《Writing the Results Section》，https://casrai.org/guides/writing-the-results-section-of-a-research-paper | "Don't restate a table in sentences… point to the pattern the reader should notice" | 佐证 |
| W10 | Houston《How to Write Mathematics》（Oxford 数学系镜像），https://www.maths.ox.ac.uk/system/files/attachments/How%20to%20write%20mathematics.pdf | 给出 running commentary，但"avoid going to the extreme of explaining every last detail"；符号是速记，用词语解释关系 | 设计依据（公式后段落"不逐算子翻译"的外部出处） |
| W11 | Hewitt & Lee《A Guide to Writing Mathematics》，https://homepages.uc.edu/~herronda/Advanced_Calculus/writing/Guide2WritingMaths.pdf | 每个字母都要定义；变量描述过于繁琐时改用文字表述；只在读者可能跟不上的步骤加文字说明；不用"两栏法"逐步解释 | 设计依据 |
| W12 | Knuth, Larrabee, Roberts《Mathematical Writing》，https://www.idc-online.com/technical_references/pdfs/information_technology/Mathematical_writing.pdf | "Don't use the style of homework papers, in which a sequence of formulas is merely listed. Tie the concepts together with a running commentary"；变量首次出现时定义；读者初读会跳过公式，句子须自成流 | 设计依据 |
| W13 | HKU《Guide to Writing Mathematics》，https://hkumath.hku.hk/web/teaching/guide_to_writing_mathematics.pdf | 数学写作以文字为主、公式为辅；不写孤立公式；但警告符号过度使用 | 佐证 |
| W14 | Jenni《减少学术写作冗余的建议》2025-10-13，https://jenni.ai/zh/blog/reduce-redundancy-in-academic-writing | 自查问句"这个句子是否添加了新的信息" | 佐证 |

仓库已有出处（不重复引用，指南只做交叉引用）：清华《研究生学位论文写作指南》§4.5（章引言不重复绪论综述）、§4.6（结论≠各章小结简单重复）已录入 `method-chapter-guide-zh.md` §三、§六、§十。

## 3. 会话早期检索但未保留 URL 的来源

以下来源在本会话压缩前检索到，摘要中未保留可核对 URL，因此**不进入指南引用**，只作背景：张柯论文指导（章引言两部分、小结半页）、上海交通大学模板（每章须有本章小结）、河北工业大学（单一主题不拼凑）、ANU chapter writing、proofreadingmalaysia signposting、Oxbridge Essays、tesify、gentext、Cornell equations、Berndt、Mermin、bbs.wz132 公式解释三模块。标签：**missing evidence**。实施期如需引用，须重新检索并核对 URL。

## 4. 技能目录先例

### 4.1 查询与运行记录

- `research_prior_art.py`（qiaomu）在 Windows 上因 `subprocess.run(["npx", ...])` 找不到 `npx` 报 `FileNotFoundError`；改用 `--skip-skills-sh` 只跑 SkillsMP，输出 `%TEMP%\prior-art\candidates.json`（3 条查询、25 个候选家族、`missing_evidence: []`）。
- SkillsMP 三条查询："thesis chapter structure redundancy check"、"academic writing paragraph responsibility signposting"、"Chinese thesis chapter introduction summary duplication"。25 个候选**全部不相关**（金融 thesis-tracker、PPT 模板、K12 规划等）。标签：SkillsMP 无匹配先例（**missing evidence**，非"不存在"）。
- `npx skills find "thesis chapter signposting redundancy"` 手动运行成功，得到下表候选。安装量只反映采用度，不是质量评分。

### 4.2 候选与处置（只读源码，未执行任何候选代码）

| 候选（仓库:技能） | 安装量 / 仓库 stars / 许可 | 内容 | 处置 |
| --- | --- | --- | --- |
| willoscar/research-units-pipeline-skills:redundancy-pruner | 48 / 510 / 无 LICENSE 文件 | 综述草稿去重：区分"重复样板"与"小节特有内容"；全局免责段只保留一个位置；过渡句改为带具体名词的论证桥接；护栏：不增删引用键、不跨小节移引用 | **adapt**：采纳"一处完整、其余指代"和"过渡句要带本节具体名词"两条判据进指南 §4；护栏与本仓库学术事实保护一致。不采纳其 survey 专用的 H3 模型 |
| willoscar/research-units-pipeline-skills:chapter-lead-writer（含 `references/bad_narration_examples.md`） | 42（writer-context-pack 同仓）/ 510 | H2 导语块"预告本章比较视角、把各 H3 连成一个论证、不添加新事实"；反例五类：目录式叙述、幻灯片导航、规划者口吻、计数开头、标题复述 | **adapt**：五类反例转为总节导语的反例（目录式叙述 / 标题复述 / 计数开头），并明确"不重复整章问题与全方法链"。不采纳其脚本生成导语 |
| willoscar/research-units-pipeline-skills:thesis-chapter-reconstructor | 15 / 510 | 把小论文改成学位论文章：重写章目标、内容边界、前后衔接、小节职责；"任何一章像 paper 复制 / 实验报告 / 技术文档 / 多篇拼接就没写完" | **keep（已有）**：本仓库 P-PAPER 与 `method-chapter-guide-zh.md` §八 已覆盖；指南只引用既有位置 |
| alterlab-ieu/alterlab-fc-skills:alterlab-rma-thesis-architect | 46 / 14 / MIT | 人设式论文导师；"每章末段设置下一章首段"；"讨论章不得复述结果" | **reject**：人设与自主执行模式不适配本仓库诊断型模块；"末段设置下一章"已由 `method-chapter-guide-zh.md` §三"缺陷驱动过渡"覆盖 |
| human-avatar/skills-for-humanity:s4h-information-redundancy | 32 / 227 / MIT | 信息论视角：承重冗余（纠错、强化）vs 浪费冗余；先穷举再分类 | **adapt（概念）**：指南 §4 用"结构功能性重述 vs 同义复述"表述，与 W1 的信息增量判据合并；不引入信息论术语 |
| parcadei/continuous-claude-v3:idempotent-redundancy | 487 / 3943 / MIT | 代码层幂等冗余 | **reject**：与写作无关（关键词命中） |
| reviewstage/stage-cli:stage-chapters | 344 / 271 / MIT | 代码评审分章工具 | **reject**：与写作无关 |
| rhavekost/author-toolkit:story-structure | 216 | 小说结构 | **reject**：非学术写作，未读源码 |
| robertguss/claude-code-toolkit:chapter-architect | 27 / 117 / MIT | 非虚构图书章节架构 | **reject**：非学术写作，未读源码 |

### 4.3 keep / adapt / reject / invent 总表

- **keep**（仓库已有，只交叉引用）：章引言两段式与弹性口径；"禁重复绪论综述"；本章小结五角色与"不复述目录、不新增结果、不新增引用"；结果分析"不写流水账"与四轴解释基线；M-EQUATION 释义入口；P-PAPER 拼接感。
- **adapt**：W1 四类重复 + 信息增量两问 + "一处完整、其余指代"；W2 功能定位法；W4/W5 小结"只对复杂章复述要点、不引入新材料"；W6/W7 结果段"只强调最重要观察、可重复一两个关键值"；W10-W12 公式后"定义符号 + 关键机制、不逐步翻译"；redundancy-pruner 的"过渡句带本节具体名词"；chapter-lead-writer 的导语反例。
- **reject**：人设式导师、脚本生成导语、信息论术语、survey 专用 H3 模型、非学术候选。
- **invent**（本仓库原创）：六位置合并矩阵及其"既有 owner / 检查码"两列；跨层级重复的"完整版只在一处"判据按位置落地（章引言不重述绪论背景、总节导语不重复章引言、小节首段不重复总节导语、小结不重复正文论证）；可选的 `PR-*` 脚本观察码（Info/P3、`NEEDS-LLM`）。

## 5. 证据标签总结

- 设计优势（design advantage）：六位置矩阵把散落在 5 份指南中的规则合并为单一入口；负面清单（"不必反复做"）是既有指南普遍缺失的维度。
- 已验证（validated）：无。本任务未做私有语料标定；`PR-*` 阈值（若实现）标注"未标定 / UNVERIFIED"。
- 假设（hypothesis）：脚本层六个码的误报率可接受；总节导语与章引言 bigram Jaccard 阈值可区分"阅读地图"与"复述"。
- 缺失证据（missing evidence）：SkillsMP 无相关先例；早期检索来源无 URL；无用户论文实测。
