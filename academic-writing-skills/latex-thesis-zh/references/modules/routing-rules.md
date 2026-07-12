# 路由规则详解（latex-thesis-zh）

SKILL.md 的「路由规则」节给出串行顺序与指针；本文件保留完整判据。

## 总则

- 先根据用户问题自动推断模块，不把“你想用哪个模块”当成默认追问。
- 如果一个请求同时包含 2-3 个兼容目标，按固定顺序串行执行，而不是只做第一个：`template` -> `compile` -> `format` -> `structure` / `consistency` -> `bibliography` / `references` -> `logic` / `literature` -> `experiment` / `title` / `deai` / `tables` / `abstract`。
- 对同一段文字做多轮润色时，按“论证/逻辑 -> 句子结构 -> 词汇/排版”由粗到细处理，顺序不可颠倒；详见 `references/writing/writing-philosophy-zh.md`。
- 某个脚本失败时，先返回精确命令、退出码和关键报错，再给出最小下一步，不要静默切换到别的模块掩盖失败。

## 逐类判据

- 涉及“引用了不存在的图表”“图表没被引用”“编号断档”“缺图题表题”时走 `references`（交叉引用完整性，盲审高频扣分点）；参考文献条目本身的问题仍走 `bibliography`。
- 涉及“公式编号挤到下一行”“长公式是否应拆成两行”“公式超出版心/页边距”“相邻公式要不要同步拆行”时走 `format`，并补读 `references/formatting/formula-guide.md`；若问题是 `\label` / `\eqref` / 未定义引用，则走 `references`；若问题是标题后直接进入公式，则走 `logic`。
- 涉及模板不明、编译失败、学校规范不清这三类问题时，优先 `template`，再决定后续是 `compile` 还是 `format`。
- `logic` 默认全文档运行（含导语、主线、章引言、漏斗、三方对齐与 C3 绪论-结论闭合）；`--section` 只聚焦单章（接受英文键或中文名，如 `--section 绪论`），此时仅运行与该章相关的检查（如 related 的 A1/A3、introduction 的漏斗）。`--cross-section` 已并入默认行为，仅作兼容保留。
- `deai` 全文档分析用 `--analyze`（覆盖所有章节，含未命中关键词的正文章）；`--section` 针对单章快速检查，二者互补，不要只跑 `--section` 就下全文结论。
- `deai` 在英文摘要区域会额外做时态检查：方法/结果句用现在时报告动词（如 `shows`/`presents`）发 `[Script]` LOW 痕迹，中文正文不检查；能识别 generic `\begin{abstract}`、thuthesis `\begin{abstract*}`、pkuthss `\begin{eabstract}`（跳过中文摘要环境）。判断级清单见 `references/writing/tense-guide-zh.md`。
- 涉及“标题后直接接列表/公式”“绪论-结论闭合”“章节主线”“研究空白推导”“四级标题导语”时，默认走 `logic`；只有明确要重构文献综述写法时才切到 `literature`。
- 涉及“大标题/小标题/章标题/小节标题/目录标题不对”“小节数太多”“每章最多 5 节”“标题没有体现对象、问题、方法”“小标题没有扣住上级标题”时，默认串行执行 `structure` -> `title`。`title` 使用 `--headings` 输出章标题对象-问题-方法、直属小节数量和小节扣合诊断；只有用户同时问导语、衔接或主线时才追加 `logic`。
- 涉及“每章引言/章首怎么写”“承上启下”“第三章第四章引言”“章引言太短/没承接上一章/没预告本章安排”时，默认走 `logic`：它对正文各章（绪论除外）做承上启下章引言专项检查（两段式为推荐形态；缺承上按依赖线索分级——章内有“第 X 章”复用线索维持 Major，纯并列章降 Info），并补读 `references/writing/thesis-writing-guide.md` 的“正文章引言”一节与 `references/writing/method-chapter-guide-zh.md` 给出改写方案；单章文件运行配 `--first-chapter N` 声明真实章号。
- 涉及“本章小结”“章节小结”“章末小结”“小结写法”“小结写成好几段”时，默认走 `logic` 并补读 `references/writing/thesis-writing-guide.md` 的“正文章末小结”一节：章末小结默认写成一个自然段，按“问题/目标 -> 本章工作/方法 -> 关键过程/证据 -> 结果价值 -> 对全篇主线的支撑”收束；除非学校模板或用户明确要求，不拆成多段或列表。
- 涉及“改写绪论/方法章节/实验讨论/总结与展望”“章节主线怎么写”“摘要、创新点、结论如何闭合”时，仍优先走现有模块，并补读 `references/writing/thesis-writing-guide.md`；不要新增英文会议论文式 `section-writing` 模块。
- 涉及“第二章怎么写”“工艺流程分析”“总体框架图/技术路线图”“工艺→难点→框架章式”“过程分析章”时，走 `logic` 加 `--process-chapter`（默认查第 2 章，`--section` 可覆盖），并补读 `references/writing/process-chapter-guide-zh.md`：它对工业/过程背景第二章做 P-FLOW/P-DERIVE/P-FRAME/P-ORDER 主线检查，脚本先做双信号章式预判（须同时命中过程信号与框架信号），非过程分析章只出 Info 不强套。“第二章=方法+实验”流派不走该 flag，按下一条方法章条目处理。
- 涉及“第三/四/五/六章方法章怎么写”“一章一方法+同章实验章式”“方法章骨架/五段结构”“实验部分不充分/像项目汇报（逐方法章）”“论文有小论文拼接感/源论文表述”“方法章草稿态残留/占位表格”时，走 `experiment` 加 `--per-chapter`（逐方法章查 E-DATA/E-ATTR/E-REF/E-FIG/E-METRIC/E-PARAM/E-ABL/E-ECHO）与 `logic`（默认扫 P-PAPER 拼接表述、单章文件配 `--first-chapter N`）、`format`（F-NOTE/F-PLACEHOLDER），并补读 `references/writing/method-chapter-guide-zh.md`：五段骨架、章引言承上分级（并列方法章可不承上）、实验工业版规范、防误报红线 12 条（无显著性检验/人工经验基线/教科书基础节均合法，不报）。
- 涉及“全篇动机主线/红线是否贯通”（绪论的每条承诺是否都被验证、被回应）时，用 `logic` 加 `--motivation-thread`：它附加一份只读的承诺映射 + 闭合映射启发式诊断，且不改变 `logic` 的默认输出。
- 需要分级去 AI / AIGC 维度分析时，用 `deai` 加 `--tier light|medium|heavy`：缩放阈值、增加 D1 句长检查、按维度（D1-D5）标注；不传 `--tier` 时保持默认输出。
- 涉及“实验像项目汇报”“讨论太浅”“结论不完整”“缺少限制与未来工作”时，默认走 `experiment`，不要误判成纯语言润色。
- 涉及“对照学校规范逐项检查”“终检/定稿检查/毕业前格式自查”“规范符合性”时走 `spec-check`：先确认学校与学位（燕山大学用 `--template yanshan`，清华/北大/无专用模板分别用 `--template thuthesis|pkuthss|generic`，四份模板快照均带逐项清单）；模板未识别且无清单时，请用户提供学校名或规范文件（整理成 `--spec-file` 清单）。脚本报告中 NEEDS-LLM 项按 `references/modules/spec-check.md` 第 4 步逐项判读，MODULE 项执行对应模块命令，MANUAL 项以“打印前自查单”原样交付，不要替用户宣称版式已符合。
- 涉及“盲审”“外审”“送审版本”“匿名版/隐名”“隐去姓名/致谢”时走 `blind-review`：`--check` 定位泄露点（能拿到姓名时加 `--author`/`--supervisor` 全文扫描）；生成盲审版先 `--generate --dry-run` 给用户确认计划再生成——只写 `_blind` 副本、原文件字节不变；副本中 `TODO-BLIND(R2)` 成果条目与姓名句由你按 `references/modules/blind-review.md` 给出 `[LLM]` 改写建议、用户确认后落入副本（署名次序是事实，不得推断）。只问格式合规仍走 `spec-check`。
