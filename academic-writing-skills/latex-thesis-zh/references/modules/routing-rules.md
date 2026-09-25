# 路由规则详解（latex-thesis-zh）

SKILL.md 的「路由规则」节给出串行顺序与指针；本文件保留完整判据。

## 总则

- 先根据用户问题自动推断模块，不把“你想用哪个模块”当成默认追问。
- 如果一个请求同时包含 2-3 个兼容目标，按固定顺序串行执行，而不是只做第一个：`template` -> `compile` -> `format` -> `structure` / `consistency` -> `bibliography` / `references` -> `logic` / `literature` -> `experiment` / `title` / `expression` / `deai` / `claim-forward` / `polish` / `tables` / `abstract`。
- 对同一段文字做多轮润色时，按“论证/逻辑 -> 句子结构 -> 词汇/排版”由粗到细处理，顺序不可颠倒；详见 `references/writing/writing-philosophy-zh.md`。
- 某个脚本失败时，先返回精确命令、退出码和关键报错，再给出最小下一步，不要静默切换到别的模块掩盖失败。

## 改写契约适用范围

判定标准只有一条：**该模块是否产出可直接替换原文的具体文本？** 若产出的只是"该怎么改"的指令，则改写行为发生在 LLM 侧，只适用 `[LLM]` 层。三组逐项列出——不要因为某模块"看起来像润色"就给它加契约段。

- **纳入契约（`[Script]` + `[LLM]` 两层）**：`expression`。
- **仅 `[LLM]` 层**（无脚本，或脚本只出指令不出替换文本）：`deai`、`claim-forward`、`polish`。`deai` 的 `-> 建议: 长短句交替` 是行为指令；LLM 依此产出的改写带 `[LLM]` 层字段。`claim-forward` 输出 `Candidate:` 提案（调序后的句子或带 `{占位}` 的模板替换），不是替换文本；其 `[Script]` 块只带 `Meaning-Check: NEEDS-LLM`，LLM 改写再补四字段。`polish` 的脚本只列单元与漂移发现，每条核对同样带 `Meaning-Check: NEEDS-LLM`，四字段由 `[LLM]` 改写块补齐。
- **排除——完全不加契约段**：`compile`、`format`、`structure`、`consistency`、`template`、`bibliography`、`references`、`tables`、`title`、`logic`、`literature`、`experiment`、`abstract`、`conclusion`、`spec-check`、`blind-review`。这些是纯诊断模块，加字段只会制造噪音。

### 分层规则

- `[Script]` 层只能置 `Meaning-Check: NEEDS-LLM`，且只能置 `none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized` 四个规则可确定的标记。规则脚本若肯定式声称 `PRESERVED`，等于制造虚假保证，比没有契约更糟。
- `[LLM]` 层可置 `PRESERVED` 与 `Risk-Flags` 闭集内任一取值，但 `PRESERVED` 始终是待作者核对的提案。
- `Risk-Flags` 是闭集：`none`、`not-assessed`、`lexical-substitution`、`whitespace-normalized`、`overstatement`、`ambiguity`、`terminology-drift`、`invented-claim`。不得发明新取值。
- 改写不得升高措辞强度。强度发生变化时置 `Risk-Flags: overstatement`，判据引用 `references/writing/over-claim-guard.md`，不新建替换表。
- 原文含义确实不清时，置 `ambiguity` 并给出保守版本，绝不静默选择更强的那一种读法。
- `NEEDS-LLM` 沿用 `check_spec.py` 既有语义（`PASS | FAIL | NEEDS-LLM | MODULE | MANUAL | SKIP`）：本层无判定能力，需上层 LLM 或人工复核。

### 编辑轴与追问边界

- `--goal grammar|clarity|concision|coherence` 是这次编辑要解决什么；`--strength minimal|moderate|restructure` 是允许改到多深。两轴正交：`--goal concision --strength minimal` 与 `--goal coherence --strength restructure` 都是合法组合，`--goal` 不是严重度阶梯。
- 幅度语义（三方一致）：

| 取值          | 允许动的层级                       | 禁止                     |
| ------------- | ---------------------------------- | ------------------------ |
| `minimal`     | 词汇、标点、明显语法错             | 改句子结构、改段落顺序   |
| `moderate`    | 上加：拆分/合并句子、语序调整      | 改段落顺序、增删论断     |
| `restructure` | 上加：段落顺序、话题句位置         | 增删论断（红线，永远禁） |

- 三档都受核心规则约束：任何一档都不得添加原文没有的论断、机制、引用、结果、局限、方法或作者意图。
- 默认值为 `--goal grammar` 与 `--strength minimal`，即能解决问题的最小改动。
- 这不构成固定问卷。既有规则不变：自动推断模块，不默认追问。编辑目标、编辑幅度、作者原意只在答案会改变本次编辑时才追问——例如某句歧义到两种读法会产出不同改写时。
- `--tier` 语义不变：`deai` 的检测灵敏度（light 报得少、heavy 报得多）。它绝不被挪用为编辑幅度控制，两套词汇刻意不重叠。

## 逐类判据

- 涉及“引用了不存在的图表”“图表没被引用”“编号断档”“缺图题表题”时走 `references`（交叉引用完整性，盲审高频扣分点）；参考文献条目本身的问题仍走 `bibliography`。
- 涉及“公式编号挤到下一行”“长公式是否应拆成两行”“公式超出版心/页边距”“相邻公式要不要同步拆行”时走 `format`，并补读 `references/formatting/formula-guide.md`；若问题是 `\label` / `\eqref` / 未定义引用，则走 `references`；若问题是标题后直接进入公式，则走 `logic`。
- 涉及模板不明、编译失败、学校规范不清这三类问题时，优先 `template`，再决定后续是 `compile` 还是 `format`。
- `logic` 默认全文档运行（含导语、主线、章引言、漏斗、三方对齐与 C3 绪论-结论闭合）；`--section` 只聚焦单章（接受英文键或中文名，如 `--section 绪论`），此时仅运行与该章相关的检查（如 related 的 A1/A3、introduction 的漏斗）。`--cross-section` 已并入默认行为，仅作兼容保留。
- 涉及“段落首句没有总领”“段末缺少收束”“相邻段跳跃”“单句成段/段内纯罗列”时，走 `logic --paragraph-arc`，并补读 `references/writing/paragraph-arc-zh.md`。该 flag 默认关闭，只输出含 `Meaning-Check: NEEDS-LLM` 的 `[Script]` 观察；`--section` 可缩小章节作用域，`--first-chapter` 不参与段落弧线定位。`logic` 仍属于纯诊断模块，不增加改写契约。
- 涉及“章引言又讲了一遍背景”“每节开头都重复整章问题”“小节首段又列一遍挑战”“公式后把每步都翻成文字”“小结又加了引用/公式”“各级段落该写什么不该写什么 / 结构重复 / 写作冗余”时，走 `logic --paragraph-roles`，并补读 `references/writing/paragraph-roles-zh.md`。该 flag 默认关闭，只输出含 `Meaning-Check: NEEDS-LLM` 的 `[Script]` 观察；实验结果段的流水账仍走 `experiment --results-analysis`。
- `deai` 全文档分析用 `--analyze`（覆盖所有章节，含未命中关键词的正文章）；`--section` 针对单章快速检查，二者互补，不要只跑 `--section` 就下全文结论。
- `deai` 在英文摘要区域会额外做时态检查：方法/结果句用现在时报告动词（如 `shows`/`presents`）发 `[Script]` LOW 痕迹，中文正文不检查；能识别 generic `\begin{abstract}`、thuthesis `\begin{abstract*}`、pkuthss `\begin{eabstract}`（跳过中文摘要环境）。判断级清单见 `references/writing/tense-guide-zh.md`。
- 涉及“标题后直接接列表/公式”“绪论-结论闭合”“章节主线”“研究空白推导”“四级标题导语”时，默认走 `logic`；明确要重构文献综述写法或核对“主题簇—代表文献归因—簇末综合”接口时切到 `literature`。
- 涉及“大标题/小标题/章标题/小节标题/目录标题不对”“小节数太多”“每章最多 5 节”“标题没有体现对象、问题、方法”“小标题没有扣住上级标题”时，默认串行执行 `structure` -> `title`。`title` 使用 `--headings` 输出章标题对象-问题-方法、直属小节数量和小节扣合诊断；只有用户同时问导语、衔接或主线时才追加 `logic`。
- 涉及“每章引言/章首怎么写”“承上启下”“第三章第四章引言”“章引言太短/没承接上一章/没预告本章安排”“引言写成一段行不行 / 要不要分两段 / 一段式 / 两段式 / 引言段式”时，走 `logic`（需要段式与要件观察时加 `--chapter-intro-style`）：它对正文各章（绪论除外）做承上启下章引言专项检查（一段式与两段式均合规，按依赖强度与篇幅选型；缺承上按依赖线索分级——章内有“第 X 章”复用线索维持 Major，纯并列章降 Info），并补读 `references/writing/thesis-writing-guide.md` 的“正文章引言”一节与 `references/writing/method-chapter-guide-zh.md` 给出改写方案；单章文件运行配 `--first-chapter N` 声明真实章号。
- 涉及“本章小结”“章节小结”“章末小结”“小结写法”“小结写成好几段”时，默认走 `logic` 并补读 `references/writing/thesis-writing-guide.md` 的“正文章末小结”一节：先按框架/过程章、方法章或系统/工程章核对全部独立任务与证据状态，再按“问题/目标 -> 本章工作/方法 -> 关键过程/证据 -> 结果价值 -> 对全篇主线的支撑”收束。一个自然段是默认形态；学校模板、导师或用户明确要求时可多段或列点，且只在真实过程顺序中使用序词。
- 涉及“改写绪论/方法章节/实验讨论/总结与展望”“章节主线怎么写”“摘要、创新点、结论如何闭合”时，仍优先走现有模块，并补读 `references/writing/thesis-writing-guide.md`；不要新增英文会议论文式 `section-writing` 模块。
- 涉及摘要编号工作段内多个组件的依赖或并行关系时，走 `abstract` 并补读 `references/writing/abstract-structure.md` 的“编号工作段中的多组件关系”；模块名称不能作为串行因果、增益或消融证据。
- 涉及“第二章怎么写”“工艺流程分析”“总体框架图/技术路线图”“工艺→难点→框架章式”“过程分析章”时，走 `logic` 加 `--process-chapter`（默认查第 2 章，`--section` 可覆盖），并补读 `references/writing/process-chapter-guide-zh.md`：它对工业/过程背景第二章做 P-FLOW/P-DERIVE/P-FRAME/P-ORDER 主线检查，脚本先做双信号章式预判（须同时命中过程信号与框架信号），非过程分析章只出 Info 不强套。“第二章=方法+实验”流派不走该 flag，按下一条方法章条目处理。
- 涉及“方法章怎么写”“一章一方法+同章实验章式”“方法章骨架/五段结构”“实验部分不充分/像项目汇报（逐方法章）”“论文有小论文拼接感/源论文表述”“方法章草稿态残留/占位表格”时，先按正文确认确属方法章，再走 `experiment` 加 `--per-chapter`（逐方法章查 E-DATA/E-ATTR/E-REF/E-FIG/E-METRIC/E-PARAM/E-ABL/E-ECHO）与 `logic`（默认扫 P-PAPER 拼接表述、单章文件配 `--first-chapter N`）、`format`（F-NOTE/F-PLACEHOLDER），并补读 `references/writing/method-chapter-guide-zh.md`：五段骨架、章引言承上分级（并列方法章可不承上）、实验工业版规范、防误报红线 12 条（无显著性检验/人工经验基线/教科书基础节均合法，不报）。只有章号而没有正文信息时先读取章标题、直属小节和代表段落，不凭“第三/四/五/六章”运行 `--per-chapter`。
- 涉及中文学位论文的“工程应用章/系统实现章/平台应用章”“架构和技术栈像清单”“服务机制怎么写”“界面操作像产品说明”“工程验证层级”时，先确认论文语境，并按正文是否承担“研究工件 → 运行约束 → 系统机制/操作任务 → 分级验证”来判定章型；命中后走既有 `logic` 并补读 `references/writing/engineering-application-chapter-guide-zh.md`。工程章不新增脚本或 flag，也不对整章运行方法章 `--per-chapter`；只有用户明确请求或确有定量结果小节时，才对该小节追加既有 `experiment --results-analysis`。离线回放、影子观察、受控试点、生产/闭环证据不得越级，可靠性、业务收益、执行/跟踪保真度和人工可用性分别取证；无论文语境的 API/部署 README 不触发本技能。
- 涉及“结果分析太浅”“只报数字”“次优比较缺失”“图表描述未定位误差”“完整模型结果被归因到单个组件”“生成样本与筛选后选定集混用”“隐藏/删除展示通道”“冻结聚合是否重算”“缺失率分母/共同样本”时，走 `experiment --results-analysis`，并补读 `references/writing/results-analysis-guide-zh.md`。展示变化不授权统计重算；共同集合或分母未知时保留不可比较状态。RA-* 只定位启发式候选，不能代替 `R-*` 人工与 LLM 清单，也不覆盖新增的自然语言口径核对。歧义速判：结果分析的事实组织和证据深度归本旗标；论断强度与证据阶梯的语义裁决读 `references/writing/over-claim-guard.md`；AI 痕迹与防御性推测解释走 `deai` 及其 `[LLM]` 组合判据。
- 涉及“表、正文和本章小结里的终值是否一致”“评价集名称是否混用”“不同指标是否被写成可互推”时，走 `experiment --cross-surface`，可加 `--section`。`--cross-surface-terms` 只能与该开关同时使用。候选为 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`，只给局部位置，不输出修正数字。不传 `--cross-surface` 时不改变 `--results-analysis`。
- 涉及“全篇动机主线/红线是否贯通”（绪论的每条承诺是否都被验证、被回应）时，用 `logic` 加 `--motivation-thread`：它附加一份只读的承诺映射 + 闭合映射启发式诊断，且不改变 `logic` 的默认输出。
- 需要分级去 AI / AIGC 维度分析时，用 `deai` 加 `--tier light|medium|heavy`：缩放阈值、增加 D1 句长检查、按维度（D1-D5）标注；不传 `--tier` 时保持默认输出。
- 涉及“实验像项目汇报”“讨论太浅”“结论不完整”“缺少限制与未来工作”时，默认走 `experiment`，不要误判成纯语言润色。
- 涉及“先说本文不做什么再说做了什么”“写得太谦虚 / 像在道歉”“遗憾的是 / 仍明显落后 / 效果有限”“一句话堆了三个可能 / 或许 / 在一定程度上”“结论末段以缺陷收尾没有展望”时走 `claim-forward`：`check_claim_forward.py` 发 `CF-DISCLAIM` / `CF-SELFWEAK` / `CF-CAVEAT-POS` / `CF-HEDGE-STACK` / `CF-CLOSE-NEG` 五个 `[Script]` 码，只调顺序和搭配，绝不删除限制、不利对比或非主线结果；加强措辞前先对照 `references/writing/over-claim-guard.md` 的“向上校准”节，只抬到证据已支撑的那一级。三条边界：`不是 X 而是 Y` 壳与“值得注意的是”归 `deai`；摘要痛点词（尚未 / 难以）归 `abstract` 的 T-PAIN，不是自我削弱；结论展望前的承接句（`CC-OUTLOOK-TRANS`）合法，`CF-CLOSE-NEG` 只报负面判定后无方向的末段。引用句、“不足 / 局限 / 研究范围”小节、裸“仅 / 尚未”不报。
- 明确要求“润色这段”“润色这一节”“把第 X 章语言润色一下”时走 `polish`：先 `polish_unit_zh.py --plan`，再按单元读取、改写、`--verify`；整章/全文同样逐单元处理。只要求检查/审校时不改写；原有标题、事实与结论强度保持不变，只读邻域不进入润色稿。单元前诊断由 `expression` / `deai` / `claim-forward` 提供，论证问题先走 `logic`；详见 [polish](polish.md) 与 [单元润色协议](../writing/unit-polish-zh.md)。
- 涉及“这段太口语，改学术一点”“句子太长太绕，帮我理顺”“搭配读着别扭”“中英标点混着用”“冒号/分号太多”“标签式冒号”“分号串整段”“数值和单位怎么写”“概数用不用汉字”时走 `expression`：`check_style_zh.py` 跑九个 E-* 检查器（`E-COLLOQ`/`E-ABSOLUTE`/`E-COLLOC`/`E-INCOMP`/`E-PUNCT`/`E-NUMSPACE`/`E-UNITFONT`/`E-NUMSTYLE`/`E-LONGSENT`），规则真相源是 `references/writing/academic-style-zh.md`，数字与单位另见 `references/formatting/number-unit-guide-zh.md`。其中连续正文的冒号、分号与句间逻辑按规则源 §5.4 由 `[LLM]` 判断，`E-PUNCT` 仍只检查 §5.3 的中英标点混用，不增加规则、阈值或检查码。分档表与逐检查器排除条件见 `references/modules/expression.md`。五条边界（每条都有既有 owner，重造必冲突）：
  - vs `abstract`：**人称（我们/本文）不归 `expression`**。第一人称走 `analyze_abstract.py` 的 T-VOICE，首句是否定位研究对象走 T-OPEN，两者维度不同。`check_style_zh.py` 不实现任何人称检查。
  - vs `over-claim-guard`：`expression` 的 `E-ABSOLUTE` 只做**词汇层**替换建议（显然/必然/最好…）；论断强度分级仍归 `references/writing/over-claim-guard.md`，不重复实现。
  - vs `spec-check` YS-36：`expression` 只做通用可判定的数字项（数值与单位间距、单位正斜体、概数/序数用字）；模板专属的完整数字规范终检归 YS-36（判定方式 `llm`）。定稿前逐项终检走 `spec-check`，两者不重复报告同一问题。
  - vs `deai` D1：`expression` 的 `E-LONGSENT` 量的是**单句可读性长度**；`deai` D1（需 `--tier`）量的是**句长变异系数 CV 过低**＝机械均匀的 AI 痕迹。两者语义不同，不报同一条 finding。
  - vs `logic`：段落顺序、论证结构、章节主线不在 `expression`，仍走 `logic`。
- 涉及“对照学校规范逐项检查”“终检/定稿检查/毕业前格式自查”“规范符合性”时走 `spec-check`：先确认学校与学位（燕山大学用 `--template yanshan`，清华/北大/无专用模板分别用 `--template thuthesis|pkuthss|generic`，四份模板快照均带逐项清单）；模板未识别且无清单时，请用户提供学校名或规范文件（整理成 `--spec-file` 清单）。脚本报告中 NEEDS-LLM 项按 `references/modules/spec-check.md` 第 4 步逐项判读，MODULE 项执行对应模块命令，MANUAL 项以“打印前自查单”原样交付，不要替用户宣称版式已符合。
- 涉及“盲审”“外审”“送审版本”“匿名版/隐名”“隐去姓名/致谢”时走 `blind-review`：`--check` 定位泄露点（能拿到姓名时加 `--author`/`--supervisor` 全文扫描）；生成盲审版先 `--generate --dry-run` 给用户确认计划再生成——只写 `_blind` 副本、原文件字节不变；副本中 `TODO-BLIND(R2)` 成果条目与姓名句由你按 `references/modules/blind-review.md` 给出 `[LLM]` 改写建议、用户确认后落入副本（署名次序是事实，不得推断）。只问格式合规仍走 `spec-check`。

## 可选术语治理、缩写体例与程度词

项目术语治理、缩写体例和程度词只在显式开关下运行。`check_consistency.py` 的 `--governance` 必须配合 `--custom-terms`。`--abbreviation-style` 与治理开关独立。`check_style_zh.py` 的 `--degree-wording` 默认关闭。这三项只给 `[Script]`、Info/P3 和 `Meaning-Check: NEEDS-LLM` 的局部词、字段或位置，不输出整句替换。不传这些开关时原输出保持不变。复制到论文工程后只依赖技能包内资源。

## 可选学院数字、公式、表身和中文题注

`--school yanshan-ee-2025` 可以加在 `check_style_zh.py`、`check_format.py`、`check_tables.py` 和 `check_references.py` 上。默认和 `--school generic` 不增加候选。不接受单独的 `yanshan`。
数字与单位只在 `check_style_zh.py`。公式源码只在 `check_format.py`。表身「同上」「同左」、同单位列表头和表题末标点只在 `check_tables.py`。非表浮动体的中文题注末标点只在 `check_references.py`。
本模式不在 `check_references.py` 增加引文位置、页码或文献著录规则。
候选为 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`，只报告局部位置，不输出整句替换，不改写数学。不传 `--school` 时原输出不变。

## 可选引文位置、重复页码、著录提示与综述递进

引文位置、重复引用页码、学院著录提示和综述递进密度只在显式开关下运行。
`check_references.py` 的 `--author-cite` 与 `--repeat-cite` 相互独立，也可与 `--school` 组合。
`verify_bib.py` 的 `--college-details` 只能与 `--standard gb7714` 或 `--standard gb7714-2025` 同时使用。
`analyze_literature.py` 的 `--progression-density` 可与 `--section` 组合，且与 `--intro-citations` 互斥。
候选为 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`，只给局部位置、键或字段，不输出替换句，不改写引用键。
不传这些开关时原输出不变。中文姓名不确定时写明作者主语不确定。重复页码不发明页码。递进阈值标为 `UNVERIFIED`。
方向与组织见 [`literature-progression-zh.md`](../writing/literature-progression-zh.md)。

## 可选跨表面数字

`analyze_experiment.py --cross-surface` 核对同章结果表、正文和本章小结中已经唯一绑定的终值。
`--cross-surface-terms FILE` 只能与 `--cross-surface` 同时出现。
JSON 只接受 `metrics` 与 `eval_sets`。给出的字段替换该字段默认词表，缺省字段保留默认，空数组表示该维没有覆盖。
默认指标是 `准确率`、`精确率`、`召回率`、`F1`、`误差`。默认评价集是 `测试集`、`验证集`、`训练集`。
`RA-XS-BODY`、`RA-XS-SUMMARY`、`RA-XS-MISSING`、`RA-XS-EVALSET`、`RA-XS-METRIC` 和 `RA-XS-COVERAGE` 都是 `[Script]`、Info/P3、`Meaning-Check: NEEDS-LLM`。
没有差异时仍报告已比较键数和未覆盖数，并说明不是全文合规证明。
不传 `--cross-surface` 时不增加这些统计。脚本不读外部数据，不复算比例，不输出修正数字。

## 学院 2025 清单路由

研究生院规范终检走 `--template yanshan`。电气工程学院 2025 清单走 `--template yanshan-ee-2025`，读 `yanshan-ee-2025.md`。二者并存，不能用研究生院阈值判定学院条目。

`--degree master` 仍保留 111 行。第 74 与第 90 项为博士，硕士 SKIP。第 10、47、66、92 项为通用，硕士不 SKIP。

静态结果不能代替人工复核。`script:third_person` 只给 NEEDS-LLM 候选。`module:` 提示不执行。局部命中不把复合项标为 PASS。第 87 与第 111 项保持 `manual`。`--author-cite` 不是学院第 42 条原文。不使用 `--pdf`。

## 方法表达、三类处置、删后桥接、摘要引号与标题符号

下列请求不新增模块，也不新增脚本码或阈值。判断只由 `[LLM]` 完成。

- 张量、交换轴或 Concat 走 `logic`，读 [method-description-guide-zh.md](../writing/method-description-guide-zh.md)。
- 正文用词与架构图标注不一致时，仍走 `logic`，按同一指南做方法一致核读。不静默改模型名或受保护术语。
- 弱点写成优点时走 `claim-forward`，读 [claim-forward-zh.md](../writing/claim-forward-zh.md)。未验证的弱点不得写成设计优点，不利结果不得删除。
- 删去预告后“上述”没有先行词时走 `logic`，读 [paragraph-roles-zh.md](../writing/paragraph-roles-zh.md)。补最短桥接，不把删掉的预告贴回去，也不改写合法的“首先/其次”。
- 摘要引号走 `abstract`，读 [abstract-structure.md](../writing/abstract-structure.md)。中文引语用成对 U+201C 与 U+201D，英文摘要用英文标点。引语的措辞、数学和引用键保持不变。
- 标题或章节安排句中的公式符号走 `structure`，读 [structure-guide.md](../writing/structure-guide.md) 与 [introduction-guide-zh.md](../writing/introduction-guide-zh.md)。该检查不改正文数学、受保护术语或模型名。

`M-FORMDUPE` 是语义复述。`PR-EQ-NARR` 只定位逐算子翻译。同一位置去重后由 LLM 裁定，不得把二者报成同一缺陷。`N-ISOLATE` 与 `M-REPRO` 不得删除复现所需信息，先核该信息是否属于另一段。分号判断指向 [academic-style-zh.md](../writing/academic-style-zh.md#punctuation-prose) 已有的 LLM 层。拆句保持数学记号多重集，指路 `polish_unit_zh.py --verify`。`UP-MATH` 只承诺记号不变，不声称散文语义不变，也不改数学。
