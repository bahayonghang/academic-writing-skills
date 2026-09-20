# latex-thesis-zh 正文章引言一段式与两段式写法支持

任务目录：`.trellis/tasks/09-20-thesis-zh-chapter-intro-forms/`。单任务，两个 commit：文档层先行，脚本层其后。

## Goal

让 `latex-thesis-zh` 对第 2 章至结论前各章的章引言同时支持**一段式**与**两段式**两种段式：两段式沿用既有"承上启下两段"模板不变；新增一段式的固定推进序、模板、正反例与段式选型判据；把现有指南、路由、模块文档里"章引言宜写成两段"的措辞改为"一段或两段均合规"；修正 `analyze_logic.py` 默认章引言检查对一段式的两处误伤（章号列举不被识别为承上、建议文案写死两段）；并为 `logic` 模块新增 opt-in `--chapter-intro-style` 段式观察，使诊断能报告每章观察到的段式、字数与要件覆盖。

用户价值：现有指南只给两段模板，检查器建议文案指引作者拆成两段；而 5 篇工业博士范文第 3 章起 20 章中 9 章（45%）为一段式，用户样例（熟料第 4 章）亦为一段式。作者按现有指引会被迫改变合法写法。

## Background

需求来源：用户 2026-09-20 要求"第二章开始的引言部分需要支持 2 种写法：1 段式和 2 段式，2 段式按照之前的，一段式请参考 [截图]，他的也不一定好"。截图为某水泥熟料博士论文 4.1 引言（单段约 556 字）。

语料实测、一段式六步推进序、样例可改进点见 `research/reference-corpus-stats.md`；外部来源与技能目录先例（keep / adapt / reject / invent）见 `research/sources-and-prior-art.md`；既有机制、编辑锚点、误伤实测与联动锁见 `research/existing-machinery.md`。技术设计见 `design.md`，执行顺序见 `implement.md`。

## Confirmed Facts

- 术语分离：仓库既有"两形态"指**位置形态**（编号引言节 / 章后导语，4:1，均合规，`intro_form` = `numbered` / `lead`）。本任务的"一段式 / 两段式"是**段式**（自然段数），与位置形态正交。任务内一律用"位置形态"与"段式"两个词（`research/existing-machinery.md` §1）。
- 语料（5 篇、第 3 章起 20 章）：一段式 9 章、两段式 7 章、三段及以上 6 章（均为文献密集型）；一段式 313~577 字、6~12 句；三篇不相关论文（熟料、粉磨、烧成）的一段式共享同一推进序：对象锚定 → 问题推导 →（必要性句）→（承上接口）→ 方案宣告 → 收束或路线（`research/reference-corpus-stats.md` §2）。
- 用户样例可改进项：单句约 150 字超 `check_style_zh.py` 80 字上限；意义句套话；"fCaO 含量"9 次重复；指标形容词堆叠。这些已有 owner（E-LONGSENT、deai 空泛表达），本任务只指路不重造（同 §3）。
- 既有口径（不得推翻）：位置形态两者均合规；路线预告 / 节号目录两态均合规；并列方法章可不承上（承上强度 ∝ 章间依赖，纯并列降 Info）；第 2 章概述式不查承上；引言含 `\cite` 合法；不重述行业背景；目录与路线不双写；篇幅阈值 40 / 900 / 1600 不动（`research/existing-machinery.md` §6）。
- 现有检查器两处误伤（实测）：`CHAPTER_DEP_REF_RE` 不匹配"第 3、4、5 章 / 第 3～5 章"列举（熟料 6.1 实例），一段式承上句被判缺承上；`bridge_suggest` / `preview_suggest` / 过简 / 过长四处建议文案写死"第一段 / 第二段 / 两段"（同 §4）。
- 检查器约定：新能力默认藏在新 flag 后；默认行为只允许误报 / 假绿修复例外，且须同步存量单测 + commit 正文声明；`[Script]` 恒 `Meaning-Check: NEEDS-LLM`；启发式 Info/P3 并标 UNVERIFIED；私有语料不进公开文件。
- 保真锁核对：`test_thesis_zh_guidance_fidelity.py` 不锁任何章引言句子；`tests/` 无断言"两段式 / 推荐形态"字符串的测试。`baseline-before.txt` 不含章引言 finding（`baseline-sample.tex` 仅 1 个 `\chapter`）。
- 技能目录无任何区分章引言段式或检查要件覆盖的先例；一段式推进序、段式选型判据与 `CI-*` 码为原创（`research/sources-and-prior-art.md` §4-§6）。

## Requirements

### R1 `thesis-writing-guide.md`"正文章引言"节改写为双段式规范源

- R1.1 节题改为"正文章引言（一段式 / 两段式，承上启下）"。既有两段模板、两段角色、弹性口径四条、正反例表、绪论边界句全部保留原句；只允许在推荐语处把"两段式为推荐形态"改为"承上句（有依赖时）为推荐要件；一段式与两段式均合规"。
- R1.2 新增"共同要件"小节：四个要件与顺序——① 问题（本章对象的现象 / 数据特性 → 技术问题及后果）、② 承上接口（角色复用句，按依赖强度，并列章可省）、③ 方案宣告（"本章……构建 / 提出<方法名>，用于……"）、④ 收束或路线（价值收束"为……提供……"或方法路线"首先……最后"，二选一或并用，不用节号目录）。要件固定、段数灵活。
- R1.3 新增"一段式"小节：六步推进序表（对象锚定 / 问题推导 / 必要性句 / 承上接口 / 方案宣告 / 收束或路线，各列"要件 / 句数 / 是否必需 / 写法"）；一段式模板（合成文本）；篇幅约 300~600 字、6~12 句；起句三种写法（开门见山 / 提问 / 承上，引 W1）；正反例各一段（合成，反例标注四类缺陷：超长句、意义套话、术语重复、目录与路线双写），反例缺陷指路 `check_style_zh.py` E-LONGSENT 与 `deai` 空泛表达，不新建判据。
- R1.4 新增"段式选型"小节：一段式适用条件（问题单一、承上可压成一句、方案一句可宣告、总字数 ≤ 约 600、并列方法章）；两段式适用条件（承上需说明前章结论及其局限 ≥ 2 句、两层以上问题或方案、文献密集需 `\cite` 小型综述可 ≥ 3 段、总字数 > 600）；同一论文各章可混用（语料 2/5），不强求统一；同一章内不双写目录与路线。
- R1.5 "两段式"小节即既有内容，加一句说明：两段式第①段可为"现象 → 问题"而非纯承上，承上句可落在第①段末或第②段首（语料观察，已由弹性口径覆盖）。
- R1.6 来源节只引用 `research/sources-and-prior-art.md` §2 带 URL 条目（W1、W3、W4、W7 至少四条）；不出现私有语料原句、作者或校名。

### R2 既有指南与模块文档措辞协调（只改指段数的句子）

- R2.1 `method-chapter-guide-zh.md` §三：首条"承上启下两段式为主动推荐形态"改为"承上启下为推荐要件，一段式与两段式均合规（段式选型见 thesis-writing-guide.md）"；列表末尾追加"段式"一条并链接；正反例表追加一段式合规行；§十检查映射追加 `CI-*` 行；§九红线、§四以后、阈值表"1~3 段、300~500 字"不改。
- R2.2 `structure-guide.md` 标题后导语规范：把"章引言宜写成承上启下两段"改为"章引言宜承上启下，一段式或两段式均可"，其余原句与链接保留。
- R2.3 `process-chapter-guide-zh.md` §十："承上启下两段式从第 3 章起适用"改为"承上启下（一段式或两段式）从第 3 章起适用"；两位置形态表不改。
- R2.4 `paragraph-roles-zh.md`"指南分工"第一条改为"章引言一段式 / 两段式与弹性口径见……"，其余不改。
- R2.5 `references/modules/logic.md`"Chapter Intro Specialization"改"承上启下、约两段"为"承上启下、一段或两段"；新增 `## Chapter Intro Style Checks (--chapter-intro-style)` 小节：命令、三码表、豁免、`--method-narrative` 无 `--section` 时不运行的说明、指南与词表链接。
- R2.6 `references/modules/routing-rules.md` 章引言条："两段式为推荐形态"改为"一段式与两段式均合规，按依赖强度与篇幅选型"；追加触发词"引言写成一段行不行 / 要不要分两段 / 一段式 / 两段式 / 引言段式"→ `logic --chapter-intro-style` 并补读 thesis-writing-guide 正文章引言节。
- R2.7 每处改动带 `(thesis-writing-guide.md)` 或等价相对链接；不得改动 `tests/contracts/test_thesis_zh_guidance_fidelity.py` 锁定的任何句子。

### R3 `SKILL.md` 与 evals

- R3.1 `when_to_use` 追加"引言一段式/两段式"触发词；`logic` 路由行 Use when 与命令追加 `--chapter-intro-style`；路由规则"常见歧义速判"追加"章引言段式（一段还是两段）走 `logic --chapter-intro-style`"；Reference Map 的 thesis-writing-guide 行把"章引言（承上启下两段式）"改为"章引言（一段式 / 两段式）"；`version` 不动；`last_updated` 改为实施日期；description 长度保持 120~400。
- R3.2 `evals/trigger_eval.json` 追加 ≥ 2 正例（如"第四章引言我写成了一段，要不要拆成两段？""帮我按一段式改写第三章引言"）与 ≥ 1 负例（英文论文 → `latex-paper-en`）；前 49 条哈希不变。
- R3.3 `evals/evals.json` 追加 id 52，绑定 `evals/fixtures/chapter-intro-style/main.tex`；前 47 条哈希不变；两文件 `git diff --stat` 为纯增量。

### R4 docs 双语镜像

- R4.1 两份 `docs/**/latex-thesis-zh/index.md` 的 `logic` 路由行同步 `--chapter-intro-style`；新词表 YAML 各加一行。
- R4.2 R1、R2 改动的每个 references 文件与新 YAML 的 en/zh 镜像同步：zh 源 → zh 页原样、en 页译文、neutral YAML 两页与源相等；`docs/resource-manifest.json` 重生成散列。

### R5 脚本层：默认检查两处误伤修复（默认行为变化例外）

- R5.1 `CHAPTER_DEP_REF_RE` 扩展为识别章号列举（顿号、逗号、波浪号、连字符、"至 / 和 / 与 / 及"连接）；三处调用（承上判定、依赖线索、PR-INTRO-BG 同句承接排除）同时受益；"第 N 章"单章匹配结果不变。
- R5.2 `_check_chapter_intro` 四处建议文案改为段式中立（不含"第一段 / 第二段 / 两段"），observe 行（首行）原字面不变；理由行数字口径不变。
- R5.3 两处修复同 commit 更新存量单测（新增断言，不改既有断言），commit 正文显式声明"默认行为变化：误报修复 + 建议文案中立化"。
- R5.4 `parsers.py`、`deai_check.py` 字节不变；`baseline-before.txt` 逐字节不变。

### R6 脚本层：opt-in `--chapter-intro-style`

- R6.1 新 flag 默认关闭；`analyze()` 末尾新增 `chapter_intro_style: bool = False`；可与 `--section`、`--first-chapter` 组合；`--method-narrative` 无 `--section` 的提前返回路径不变。
- R6.2 三个 `[Script]` 码，全部 Info/P3、`Meaning-Check: NEEDS-LLM`、不复制整句：`CI-STYLE`（逐正文章观察：段式标签 一段式 / 两段式 / 多段式、位置形态、约字数、段数与句数、要件覆盖向量 问题 / 承上 / 方案 / 收束或路线；第 2 章承上标"不适用"）、`CI-MOVES`（要件缺失：问题、方案、收束或路线任一未命中；空引言与默认已报"缺启下"的章不重复报方案缺失）、`CI-LONG`（一段式单段汉字数 > 阈值且 ≤ 默认篇幅上限时建议按方案句拆为两段）。触发条件、豁免与常量见 `design.md` §4。
- R6.3 "对象锚定是否具体""意义句是否落到本章对象""段式是否与依赖强度匹配"不做脚本判定，只进 `[LLM]` 复核清单。
- R6.4 词表 `references/writing/chapter-intro-style-terms.yaml`（`problem_markers` / `solution_markers` / `closing_markers` 三字段），逐字段回退内置默认；路标词复用既有 `CHAPTER_ROADMAP_KEYWORDS_ZH`，不入 YAML。
- R6.5 阈值常量 `CI_ONE_PARA_MAX_HAN = 600` 在指南、spec、YAML 注释三处标"未标定 / UNVERIFIED"；不宣称误报率。
- R6.6 章引言行区间由新 helper `_chapter_intro_span` 单源提供，`_chapter_intro_block` 改为调用它；抽取后默认输出逐字节不变。

### R7 测试、spec、fixture

- R7.1 `tests/skills/latex_thesis_zh/test_chapter_intro_style.py`（importlib 按路径加载）：章号列举承上不再误报（三种连接符）；单章"第 N 章"仍匹配；四处建议行不含"第一段 / 第二段 / 两段"；三码各至少一条正例与一条反例；第 2 章 `CI-STYLE` 承上标不适用；`CI-LONG` 与默认过长零重叠；`--section method` 作用域；`--first-chapter` 章号；YAML 逐字段回退与等价；fixture 加 flag 退出码 0；报告不含 fixture 整句；默认输出基线逐字节不变（复用既有基线测试）。
- R7.2 `SMOKE_COMMANDS` 追加 `analyze_logic.py main.tex --chapter-intro-style`；`test_latex_thesis_zh_module_router_commands_match_script_help` 绿；`FROZEN_HASHES["analyze_logic.py"]` 同步。
- R7.3 新建 `.trellis/spec/academic-writing-skills/chapter-intro-style-contract.md` 并在 `index.md` 加行：术语分离、签名、常量、三码契约、豁免、默认行为变化声明、私有标定边界、必需测试。
- R7.4 `evals/fixtures/chapter-intro-style/main.tex`（合成：第 2 章概述式一段编号引言；第 3 章一段式全要件（单章号承上）；第 4 章一段式缺收束/路线；第 5 章一段式超 600 字 + 章号列举承上（复审调整：第 3 章不能列举含自身的章号）；第 6 章两段式合规），不含私有语料。

## Acceptance Criteria

- [x] AC-01 `thesis-writing-guide.md` 正文章引言节含：新节题、既有两段模板原句、"共同要件"四要件、一段式六步表 + 模板 + 正反例、"段式选型"小节、≥ 4 条带 URL 来源；`grep -c "两段式为推荐形态"` 为 0；不含私有语料原句 / 作者 / 校名。
- [x] AC-02 `method-chapter-guide-zh.md`、`structure-guide.md`、`process-chapter-guide-zh.md`、`paragraph-roles-zh.md`、`modules/logic.md`、`modules/routing-rules.md` 六文件中"章引言宜两段 / 两段式为推荐形态 / 承上启下两段式从第 3 章起"措辞为 0 处；各含指路链接；`method-chapter-guide-zh.md` §九与阈值表原句不变；`tests/contracts/test_thesis_zh_guidance_fidelity.py` 绿。
- [x] AC-03 `SKILL.md` `logic` 行命令含 `--chapter-intro-style`；歧义速判含段式指路；Reference Map 措辞已改；`version` 仍 `6.0.0`；`last_updated` = 实施日期；description 120~400；`tests/contracts/test_skill_contracts.py` 绿。
- [x] AC-04 `trigger_eval.json` +≥2 正例 +≥1 负例，前 49 条哈希不变；`evals.json` id 52 存在，前 47 条哈希不变；`git diff --stat` 两文件纯增量；`tests/contracts/test_trigger_evals.py` 绿。
- [x] AC-05 两份 docs index `logic` 行含 `--chapter-intro-style`、写作参考含新 YAML；`uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh` 绿；`just doc-build` 绿；`tests/contracts/test_docs_bilingual_resources.py` 绿。
- [x] AC-06 `CHAPTER_DEP_REF_RE` 对"第 3、4、5 章""第 3～5 章""第3-5章""第三章和第四章"命中，对"第 2 章"命中不变；含章号列举承上句的第 3 章引言不报"缺少承上"（测试断言）。
- [x] AC-07 `_check_chapter_intro` 输出的所有建议行不含"第一段""第二段""两段"；四个 observe 行字面不变；存量章引言测试（`test_chapter_intro_forms.py`、`test_body_chapters.py`、`test_latex_thesis_zh_scripts.py`、`test_process_chapter.py`、`test_paragraph_roles.py`）全绿。
- [x] AC-08 不传 flag 时 `baseline-before.txt` 逐字节不变；`parsers.py`、`deai_check.py` 字节不变；`FROZEN_HASHES["analyze_logic.py"]` 已更新且 `test_polish_unit_zh.py` 绿。
- [x] AC-09 `analyze_logic.py evals/fixtures/chapter-intro-style/main.tex --chapter-intro-style` 退出码 0；输出含 `CI-STYLE`（第 3 章标一段式、第 6 章标两段式）、`CI-MOVES`（第 4 章）、`CI-LONG`（第 5 章）；第 3、6 章不报 `CI-MOVES`；第 2 章 `CI-STYLE` 承上标不适用；每条头含 `[Script] CI-`、`[Severity: Info] [Priority: P3]`，块含 `Meaning-Check: NEEDS-LLM`；不含 fixture 整句。
- [x] AC-10 YAML 三字段与内置默认相等；字段缺失 / 类型错 / 非法值只回退该字段；两份 docs 镜像与源相等（测试断言）。
- [x] AC-11 `SMOKE_COMMANDS` 新行、spec 文件与 index 行存在；`just ci` 绿（check-versions / lint / typecheck / test 四步）。
- [x] AC-12 新增或修改的公开文件、fixture、测试不含私有语料原句、作者信息或本机路径；commit 正文含"默认行为变化"声明（脚本层 commit）。

## Out of Scope

- 绪论（第 1 章）与结论章引言；总节 / 小节导语（S1 与 PR-LEAD-DUP 已有 owner）。
- 一段式句长、意义句套话、术语重复、形容词堆叠的脚本判定（E-LONGSENT、deai、consistency 已有 owner，只指路）。
- 改变篇幅阈值 40 / 900 / 1600，或把"1~3 段、300~500 字"阈值表改数。
- 强制全文段式统一或判定"段式混用"为缺陷（语料 2/5 混用合法）。
- 自动改写章引言；`polish` 模块不新增段式契约。
- `paper-audit`、`latex-paper-en`、`typst-paper` 的镜像或对齐；`version` bump；`justfile` / `pyproject.toml` / `uv.lock`。
- 私有语料标定与误报率声明。

## 已确认决策与假设

- D1（假设，沿用用户在 2026-09-20 段落职责任务中的选择 B）：交付层级为文档层 + 默认误伤修复 + opt-in 观察，单任务两 commit。若用户复审时只要文档层与误伤修复，删去 R6 与 R7 的三码部分即可，R1-R5 不受影响。
- D2 推荐点从"两段式"移到"承上句（有依赖时）"：两段式不再是推荐形态，两种段式并列合规；承上是否必需仍按既有依赖分级。依据：语料一段式 45%；W1 明确"其他各章引言通常也是一个自然段"。
- D3 一段式"必要性句"（"具有实际工程意义和学术价值"）只作可选要件：仅熟料 5/5 使用、粉磨改用"为此，亟需……"、烧成第 5 章不用；`deai` 已把不落地的意义句列为空泛表达。泛化门槛不通过，不升为规则。
- D4 段式判定按 LaTeX 空行 / `\par` / 标题 / 受保护环境切分（复用 `_split_arc_paragraphs`），不按句数或字数猜段。
- D5 两处默认行为变化走 spec "误报 / 假绿修复"例外：R5.1 减少误报、R5.2 只改建议行；observe 行不变以保护存量断言；commit 正文双声明。
- D6 用户样例只作要件抽取依据，不复制进指南或 fixture；其缺陷（超长句、意义套话、术语重复）作为一段式反例的合成改写来源。

D1 为假设，其余由语料与既有口径推出；均在本次规划摘要中呈现，待用户复审。
