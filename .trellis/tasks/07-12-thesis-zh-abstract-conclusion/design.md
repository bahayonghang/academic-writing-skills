# Design: latex-thesis-zh 摘要与结论章节优化

对应 `prd.md` R1~R6。三个待决策点已定案，均给出理由与替代方案取舍。

## D1 摘要学位论文模式：`--model thesis` 为 zh 副本默认

**决策**：`analyze_abstract.py` 增加 `--model {thesis,five}`，**默认 `thesis`**；`five` 保留原五要素模型作后备。

- 依据：zh 副本已于 2026-06 脱离 en/typst 哈希对齐组（`test_writing_modules_alignment.py` TIER1_HASH_GROUPS 注释，审计 F3），可自由特化，不碰契约。
- 为什么默认 thesis：本技能只服务学位论文；五要素模型对博士摘要会产生系统性误报（如 Results 无数值判 MISSING，而精读显示 3/5 博士摘要合规地不带数值——abstract-patterns C1）。
- 替代方案（被弃）：靠 detect_template.py 自动判别——本技能内所有输入都是学位论文，自动判别无信息量，徒增分支。
- 兼容：既有调用 `analyze_abstract.py main.tex` 行为改变（five→thesis），SKILL.md/modules/abstract.md 同步更新；受影响的既有测试显式传 `--model five` 或更新断言。

### thesis 模型检查项（类 `ThesisAbstractAnalyzer`，与 `AbstractAnalyzer` 并列，不继承）

| 检查 ID | 内容 | 判定 | 级别 | 溯源 |
|---|---|---|---|---|
| T-OPEN | 首句以研究对象为主语定位（"X 是/产生于…"），非方法开头 | [Script] 首句不以"本文/针对/为了/提出"开头 + [LLM] 复核 | Warning | ★A1 5/5 |
| T-PAIN | 存在痛点/挑战句（难以/挑战/尚未/无法/瓶颈） | [Script] 词表 | Warning | ★A2 5/5 |
| T-LEAD | 编号段前有总起句且以"："收束（…如下：/…包括：） | [Script] 正则 | Warning | ★A4 5/5 |
| T-ENUM | 主体为（1）（2）…编号工作段，段数与编号一致 | [Script] | Warning | ★A5 5/5、D4 |
| T-PROB | 各工作段以问题导向短语开头（针对/鉴于/为解决/为了） | [Script] 逐段正则；非每段必中，全篇 <50% 才报 | Info | ★B1 |
| T-VERIFY | 验证方式点名（仿真/实际生产数据/实测/现场应用/实验），空泛"验证了有效性"无载体则报 | [Script] 词表 | Warning | ★C2 5/5 |
| T-VERB | 方法动词属规范集（提出/建立/设计/构建/研究/采用/研发），口语动词（搞/弄/做了）报错 | [Script] 词表 | Info | ★B4 |
| T-ABBR | 缩略语首现即定义（大写字母串首现处前后无中英全称括注） | [Script] 正则启发 + NEEDS-LLM 复核 | Warning | ★E3 5/5 |
| T-NUM-HEDGE | 数值指标带"约/以上/区间"稳健表述 | [Script]；仅当出现数值才查 | Info | C3 2/2 |
| T-KW-FIRST | 首个关键词≈研究对象/过程名（与标题主名词重叠） | [Script] 字符重叠启发 | Info | ★D2 |
| T-INNOV | 出现创新表述（创新/首次提出/新方法/新见解 或 编号工作段本身） | [Script] 词表，缺失报 Warning | Warning | web A3 校规 |
| T-TOC-STYLE | 目录式摘要（"第X章"连续出现≥2）/背景铺陈过长（首个编号段前占比>40%） | [Script] + [LLM] lane | Warning | web A10 软性 |

- 字数：thesis 模式默认阈值改用 check_spec 的燕山常量 `(900, 1200)` 博士 /`(500, 650)` 硕士，新增 `--degree {doctor,master}`（默认 doctor）；`--max-chars` 显式传入时覆盖。**不 import check_spec**（避免耦合其 CLI/模板逻辑），常量在 analyze_abstract 内定义并加注释指向 check_spec 对应值；两处一致性由新增单测锁定（比对两模块常量相等）。
- 第一人称：只查"我/我们/笔者"；**"本文/本论文"合法**（PRD 约束 2）。归入 T-VOICE Info 级。

## D2 结论检查器落点：新建 `analyze_conclusion.py`

**决策**：独立新脚本，不并入 analyze_logic.py。

- 理由：analyze_logic.py 已 82KB 且职责是**跨章**逻辑闭合（三方闭合、绪论贡献回应留在原处不动）；结论内容检查是**章内**检查 + 结论↔摘要两节比对，与 analyze_abstract.py 的"每节一脚本"模式对齐；路由上 modules/conclusion.md 一个命令对应一个脚本。
- 复用：`parsers.split_sections()` 已识别 conclusion（结论/总结与展望）；`tex_loader.assemble` 组装多文件；`extract_abstract` 取中文摘要做比对。**不改 parsers.py**（其在 ALIGNMENTS 哈希锁中，本任务零契约变更）。

### 检查项

| 检查 ID | 内容 | 判定 | 级别 | 溯源 |
|---|---|---|---|---|
| CC-TRIAD | 三段式齐全：总结主体 + 创新表述 + 展望 | [Script] 词表定位三要素区块 | Error（缺展望/总结）/ Warning（缺创新表述） | web C1/C5 校规·HIT；C-LABEL |
| CC-OPEN | 开篇承上式总述（复述问题 + 首先/其次/最后研究链） | [Script] 首段序词≥2 个，否则 Info | Info | C-OPENING 5/5 |
| CC-ENUM | 贡献以（1）（2）…编号列举，条数 3~4 之外仅提示 | [Script] | Info | C-ENUM 5/5 |
| CC-SKELETON | 贡献条含"针对…，提出/建立…，表明/验证…"骨架要素 | [LLM] lane（句式变体多，脚本只做粗筛计数） | Warning | C-SKELETON 5/5 |
| CC-OUTLOOK-EMPTY | 展望空话黑名单（广阔前景/值得进一步研究/有待深入 等，词表文件化，维护节律对齐 deai 词表约定）且无具体技术名词 | [Script] 黑名单 + 未来向措辞存在性 | Warning | C-OUTLOOK-SPEC 5/5；web C6 |
| CC-OUTLOOK-TRANS | 展望前有局限/承接过渡句（仍存在/仍有/不足/悬而未决） | [Script] 词表 | Info | C-OUTLOOK-TRANS 5/5 |
| CC-OUTLOOK-COUNT | 展望条数 2~3 之外提示 | [Script] | Info | C-OUTLOOK-COUNT 5/5 |
| CC-VERBATIM | 结论与摘要逐字重复：逐句 difflib.SequenceMatcher，ratio≥0.85 记命中；命中句占结论句 ≥30% 报 Warning，单句命中列 Info 明细 | [Script] + LLM 复核语义级改写 | Warning | C-NO-VERBATIM-ABS；web C4 HIT |
| CC-QUANT | 结论数值与摘要/正文一致：抽取百分比/数值 token（归一化 ％/%、－/-，剥离约/以上），逐个在正文可见文本中查存在性；缺失→NEEDS-LLM 不硬报 | [Script] | Warning（不一致）/不强制带数值 | C-QUANT-CONSIST 1/1；C-QUANT 仅 1/5 故不反向要求 |
| CC-NO-FIG | 结论章内出现 figure/table 环境 | [Script] | Error | C-NO-FIG 5/5 |
| CC-NEW-CONCEPT | 结论出现正文未见的方法名/概念 | [LLM] lane（文档化提示词，脚本不做） | Warning | C-NO-NEW-CONCEPT 5/5 |
| CC-RATIO | 总结:展望篇幅比在 1.5:1~4:1 外提示 | [Script] 字符数 | Info | C-RATIO 5/5 |
| CC-SUBSEC | 子节号（X.1/X.2）与章编号风格 | 仅 Info："与全文风格保持一致"，不判对错 | Info | C-SUBSEC 4/5 扁平；C-NUM 3/5 |

**边界（与 check_spec 零重复）**：`\cite`、字数 ≤2000、模糊措辞（大概/或许）不在本脚本检查范围；报告尾注一行指路 `spec-check` 模块。overclaim 检查指路既有 `over-claim-guard.md` 流程，不在脚本重复实现。

## D3 中英摘要一致性：并入 analyze_abstract.py，`--bilingual` flag

**决策**：不新建脚本；英文摘要抽取函数放在 analyze_abstract.py 内（`_extract_english_abstract`：eabstract/englishabstract 环境、cabstract 场景下的 abstract 环境、`\chapter{Abstract}`/`\section{Abstract}` 标题式），**不改 parsers.py**。

[Script] 检查项：

| 检查 ID | 内容 | 级别 | 溯源 |
|---|---|---|---|
| B-ORD | 首先/其次/然后/最后 ↔ First/Second/Then/Finally 数量与顺序对齐 | Warning | ★F3 5/5 |
| B-NUM | 中英数值 token 集合一致（归一化后比对） | Error（数值不一致是硬伤） | ★F1；web A9 |
| B-ENUM | 编号工作段条数一致 | Warning | ★F1 |
| B-LEN | 英文摘要缺失/过短（<中文摘要要素承载明显不足，字符比启发） | Warning | web A9 |
| B-SEM | 逐句/逐要素语义对应 | [LLM] lane，报告给出逐段对照提示词 | ★F1 |

**时态/语态（★F2）不在此实现**：deai 模块已有英文摘要区域门控的时态检测（tense-guide-zh.md + deai_check），bilingual 报告尾注指路 deai，避免双实现漂移（PRD R2 边界；deai trace 不流入本模块）。

## D4 文档与路由

- 新建 `references/writing/conclusion-guide-zh.md`：体例对齐 introduction-guide-zh.md（结构模板 + 正反例 + 分级说明 + checker 映射表）。PRD R3 全部条目；正例句式取自 research 摘录（改写，不成段照搬原文）。
- `references/writing/abstract-structure.md`：追加"学位论文摘要骨架"一节（thesis 模型 + 与五要素的关系 + 分级规律表）；原五要素内容保留。
- `references/modules/abstract.md`：更新命令（--model/--degree/--bilingual）与说明。
- 新建 `references/modules/conclusion.md`：Trigger（结论、总结与展望、展望、结论章、conclusion）+ 命令 + LLM lane 提示词要点 + spec-check/deai/over-claim 指路。
- `references/writing/thesis-writing-guide.md` §摘要/创新点/总结：改为指路两份专属指南，保留三方闭合概念句。
- SKILL.md：路由表加 conclusion 模块（触发词见上），串行顺序在 `abstract` 之后；`last_updated` 更新，**version 不动**；表格改动避开格式化 hook 重排风险（ROUTER_ROW_RE）。
- `references/modules/blind-review.md`：加一行"摘要/结论规范问题命中盲审规范性维度"Info 联动（web X2）。

## D5 测试设计

- 新增 `tests/skills/latex_thesis_zh/test_analyze_conclusion.py`：CC-* 各 [Script] 项正反例（inline tex fixture，含多文件 include 场景一例）。
- 新增 `tests/skills/latex_thesis_zh/test_abstract_thesis_mode.py`：T-* 正反例 + 阈值常量与 check_spec 一致性锁 + `--model five` 回退 + `--bilingual` B-* 正反例。
- 更新受 D1 默认值影响的既有测试（test_latex_thesis_zh_scripts.py 中 analyze_abstract 用例）。
- 词表文件若新增（展望空话黑名单），测试锁定文件存在与非空。
- 回归：`just ci` 全绿；不触碰 tests/contracts 下任何哈希锁。

## 风险与回滚

| 风险 | 缓解 |
|---|---|
| D1 默认值切换破坏既有测试/用法 | 实现顺序上先跑全量测试摸底；受影响用例逐个显式改；SKILL.md 命令同步 |
| 燕山常量两处漂移 | 一致性单测锁定（test_abstract_thesis_mode） |
| 展望黑名单误伤合法句（"值得进一步研究"出现在具体方向句尾） | 黑名单命中需同句无具体技术名词（名词性短语启发）才报；正反例测试覆盖 |
| CC-VERBATIM 阈值误报 | 0.85/30% 起步，fixture 用真实五篇的改写特征校准；报告标 [Script] 供人工复核 |
| 回滚 | 全部为新增文件 + analyze_abstract.py 单文件增强；git revert 单提交粒度即可回滚，无数据迁移 |
