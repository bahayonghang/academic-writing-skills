# C1 设计

## 1. Files

技能根 `S = academic-writing-skills/latex-defense-zh`。本子任务只新增以下文件：

- `S/references/defense-framework.md`、`slide-layouts.md`、`content-rules.md`、`visual-spec.md`、`time-budget.md`、
  `speaker-notes.md`、`qa-prep.md`
- `S/templates/beamer/beamerthemeYanshanDefense.sty`、`beamerthemeGenericDefense.sty`、`defense-layouts.sty`、`demo-deck.tex`
- `tests/skills/latex_defense_zh/test_defense_theme_assets.py`（仓库测试目录无 `__init__.py`，pytest 按文件名导入，
  本技能测试文件名统一加 `test_defense_` 前缀以免与其他技能重名）

- docs 资源登记（父 design §7）：`docs/skills/latex-defense-zh/resources/references/<七份>.md`、
  `docs/zh/skills/latex-defense-zh/resources/references/<七份>.md`、`docs/resource-manifest.json`（脚本重建）；
  改 `tests/contracts/test_docs_bilingual_resources.py:38-45` 技能集合一行（行号为 cf62830 基线，pws 登记后后移，以锚点文本定位）、`docs/installation.md:85-90` 与
  `docs/zh/installation.md:68-73` 命令块各加一行、`docs/installation.md:96` 与 `docs/zh/installation.md:79` 的「seven/七条」改为「eight/八条」。

不改其他 `tests/contracts/*`、docs 首页/侧栏/导航/usage、README、AGENTS、CLAUDE（归 C4）。`docs/zh/installation.md:51`
描述 `just skills-install` 的「七个 catalog 技能」在 C4 登记 installer 时再改。

## 2. 参考文档要点

事实来源：父 `research/framework-analysis.md`（页序、页型、测量值）与 `research/reference-skills-analysis.md`（采纳机制）。

链接规则：参考文档之间用相对 `.md` 链接；指向 `templates/beamer/*.sty`、`*.tex`、脚本等非公开资源时写 inline code 路径，
不写 Markdown 链接，以免 docs 镜像出现死链（`just doc-build` 检查）。

### 2.1 defense-framework.md

- 全稿页序：封面 → 总目录 → 第 1 章 → [章前目录 → 第 k 章]×(章数−1) → 致谢页；defense 阶段在结论后加成果页。
- 章角色与识别提示（提示供 extract 使用，最终以规划文件为准）：
  intro（章题含「绪论」「引言」或为第 1 章）；conclusion（章题含「结论」「总结与展望」）；
  application（章题含「系统」「平台」且含「设计」「应用」「实现」之一）；
  foundation（非首末章，章内无实验类节题「实验」「案例」「结果分析」「仿真」）；research（其余）。
- 角色页序列（40 分钟默认页数见 time-budget）：
  intro：background → status → challenges → organization；foundation：foundation×n；
  research：intro → problem → method×n → experiment×n → summary；application：intro → architecture → application×n；
  conclusion：innovation → outlook（defense：→ achievements）。
- 对应链：challenges 页的问题条目数 = research 章数 = innovation 页的创新点数；第 k 个问题、第 k 个研究章引言页的
  「研究内容 k」、第 k 个创新点指向同一章。
- 「论文」框：成果列表中标注对应本章的论文放在该章 summary 页；无对应条目的章不放框，不编造。
- 阶段字样：predefense 封面「博士学位论文预答辩」，defense 封面「博士学位论文答辩」；致谢页主句「敬请各位老师批评和指正！」。

### 2.2 slide-layouts.md

十二个版式，每个给出：规划字段、适用页角色、内容上限、LaTeX 骨架（宏调用序列）。

| 版式             | 适用角色                                                    | 主要字段                                 | 上限                  |
| ---------------- | ----------------------------------------------------------- | ---------------------------------------- | --------------------- |
| cover            | cover                                                       | meta                                     | —                     |
| toc              | toc                                                         | chapter                                  | —                     |
| bullets          | background、status、achievements、problem                   | subsection、bullets、takeaway            | 要点 ≤5               |
| figure           | status、organization、architecture、application、experiment | figures[1]、takeaway                     | 图高 ≤0.62\textheight |
| figure-bullets   | intro、background、problem、method、foundation              | figures[1]、bullets、position(left\|top) | 要点 ≤4               |
| figure-grid      | experiment                                                  | figures[1].subfigures[2..6]、takeaway    | 子图 ≤6               |
| equations-figure | method、foundation                                          | equations[≤4]、figures[≤1]、bullets[≤3]  | 公式 ≤4               |
| table            | experiment、application                                     | table、takeaway                          | 表体逐字              |
| cards            | challenges、innovation                                      | bullets（每条一卡）                      | 卡片 ≤5               |
| paper-summary    | summary                                                     | bullets、paper                           | 要点 ≤4               |
| outlook          | outlook                                                     | bullets                                  | 条目 ≤3               |
| thanks           | thanks                                                      | meta                                     | —                     |

### 2.3 content-rules.md

- 帧标题：论文节号 + 节题（例「3.2 方法设计」），节号取自清单；小节条：小节号 + 小节题或「研究内容 k：章题」。
- 结论句 takeaway：每个内容页一句，≤40 个汉字，陈述本页结论；串读全部 takeaway 应能复述论文主线。
- 要点：每页 ≤5 条，每条 ≤40 个汉字；正文可见字符 ≤180（D-DENSITY 初始阈值，未标定）。
- 字号：正文默认 \small；密集页可用 \footnotesize；任何文字不低于 \scriptsize（8 pt，约等于 pptx 17 pt）。
- 图表：只用清单中的论文图表；题注沿用论文编号「图3-2」「表4-1」；子图题沿用 (a)(b)。
- 数字：只写论文出现过的数字，带单位与对照基准（「比基线降低 12.3%」须论文同时给出两者）；不做单位换算与重新计算。
- 公式：按标签逐字复制论文数学源码，保留论文编号；不改写符号。
- 强调：`**词**` 渲染为红色粗体，每页 ≤3 处。
- 溢出处置顺序：删减文字 → 拆为两页 → 换版式 → 缩小图宽；字号不低于下限。
- 创新点句式：「针对…问题，提出/构建…，实现…」，内容取自论文结论章对应条目，并标明章号；展望取自结论章展望条目。
- 学术事实保护：不改 `\cite`/`\ref`/`\label`/数学；不编造文献、作者、成果、数字；不生成新图。
- 方法来源署名：claude-skill-academic-ppt（MIT）、thesis-defense-pptx-skill（Apache-2.0），只采纳机制。

### 2.4 visual-spec.md

颜色（yanshan）：defenseNavy #1F296A（封面与致谢题带、双线）、defenseBlue #2F5597（目录椭圆、页码）、
defenseAccent #4472C4（小节条文字与图标）、defenseBoxHead #376092（框标题底色）、defensePaper #002060（论文框）、
defenseRed #FF0000（强调）。generic：navy #1F3A5F、blue #2E5E8C、accent #2E5E8C、boxhead #4A6A8A、paper #1F3A5F、red #C0392B。
版位与字号按父 `research/framework-analysis.md` §4 换算表写入；Beamer 类选项 `aspectratio=169, 11pt`；
帧标题 \Large 粗（14 pt，目标 13.2 pt）；小节条 \normalsize 粗；正文 \small。
字体回退：CJK Microsoft YaHei → Source Han Sans SC → FandolHei；拉丁 Arial → TeX Gyre Heros（`\IfFontExistsTF`）。
校徽：内容页高 0.76 cm、封面高 1.23 cm，宽按原比例；路径为空或文件不存在时显示 `logo-text` 文字标识（yanshan 默认「燕山大学」；generic 为空，不显示）。

### 2.5 time-budget.md（C2 的 `scripts/defense_budget.py` 按本节实现）

40 分钟默认（2400 s）。页角色分两类：固定 1 页角色（challenges、organization、research 的 intro/problem/summary、
application 的 intro、innovation、outlook、achievements）；缩放角色（括号内为 40 分钟基数）：background(2)、status(2)、
foundation(3)、architecture(1)、application(2)。

| 段 | 页角色 × 页数 × 秒/页（40 分钟） | 小计 s |
| --- | --- | --- |
| 固定 | cover 1×30；总目录 1×20；章前目录 (章数−1)×8；thanks 1×10 | 108（7 章，不缩放） |
| intro 章 | background 2×50；status 2×50；challenges 1×50；organization 1×50 | 300 |
| foundation 章 | foundation 3×50 | 150 |
| application 章 | intro 1×40；architecture 1×50；application 2×45 | 180 |
| conclusion 章 | innovation 1×90；outlook 1×45；defense 另加 achievements 1×45 | 135（defense 180） |
| research 章 | 余量 R 平均分给各研究章，见下式 | 1527（3 章） |

公式（M 分钟，k = M/40，r(x) = ⌊x + 0.5⌋）：
- 缩放角色页数 = max(1, r(基数·k))；intro、foundation、application、conclusion 各段秒数 = 40 分钟小计 × k；固定段不缩放。
- R = 60M − 固定段 − 上述各段秒数；每研究章 T = R / 研究章数；页数 n = max(6, r(T/53))。
- 研究章内 intro、problem、summary 各 1 页；method = max(2, r((n−3)·3/7))；experiment = max(1, n−3−method)。

参考值（7 章：intro + foundation + 3 research + application + conclusion，predefense；内容页不含 cover、toc、thanks）：

| M | 每研究章 n（method/experiment） | 内容页 N | D-BUDGET 区间 [r(0.85N), r(1.15N)] | 全稿帧数 |
| --- | --- | --- | --- | --- |
| 30 | 7（2/2） | 35 | [30, 40] | 44 |
| 40 | 10（3/4） | 45 | [38, 52] | 54 |
| 60 | 15（5/7） | 66 | [56, 76] | 75 |

另两种结构的 40 分钟值：4 研究章、无基础章 → 每章 8 页、N = 44；defense 阶段 → 每章 9 页、N = 43。

### 2.6 speaker-notes.md 与 qa-prep.md

讲稿五栏：说什么（150–250 字，口语、指图号）、要点（一句）、时长（秒，取规划预算）、过渡（一句）、可能提问（1–2 条）。
提问类别：选题意义与创新性界定、方法选择理由、实验有效性与对比公平性、泛化与适用边界、工程落地与部署、章间逻辑、
成果与章对应、局限与展望；每研究章 3–5 问，答案骨架引用论文节号、图号、表号，并建议备用页（backup 角色）。

## 3. Beamer 实现

- 类：`\documentclass[aspectratio=169,11pt]{ctexbeamer}`；主题 `\usetheme{\DefenseThemeName}`，
  `demo-deck.tex` 以 `\providecommand{\DefenseThemeName}{YanshanDefense}` 给默认值，测试用
  `xelatex -jobname=… "\def\DefenseThemeName{GenericDefense}\input{demo-deck.tex}"` 切换。
- `defense-layouts.sty`：依赖 tikz、graphicx、adjustbox、booktabs、multirow、makecell、expl3（ctex 已带）。
  章表用 expl3 `seq` 保存 `\DefenseAddChapter{n}{title}`；`\DefenseTocFrame{k}` 逐行输出，k 行加粗（generic 另加 defenseBlue 色）。
  元数据宏：`\DefenseSupervisor{}`、`\DefenseSubject{}`、`\DefenseSchool{}`、`\DefenseStage{}`；`\DefenseSetup{logo=…}` 用 l3keys。
  `\DefenseDefineLabel` 用 expl3 prop 保存 label→编号；`DefenseSource` 环境按父 design §5 在组内改绑引用与引文命令。
  demo-deck.tex 至少一帧在 `DefenseSource` 内含 `\ref`、`\eqref`、`\cite` 各一次，测试 5 的编译用例覆盖该帧。
- yanshan 主题：`frametitle` 模板用 tikz overlay 画左校徽、居中标题、两侧双线、右上平行四边形页码；
  封面/致谢为无 headline 的整页 tikz 版面（题带、表格、日期）。generic 主题：同版位，无校徽，线色与题带用 generic 色。
- 两主题只定义颜色、headline/frametitle、封面与致谢外观；版式宏只在 `defense-layouts.sty` 定义。

## 4. Tests（`tests/skills/latex_defense_zh/test_defense_theme_assets.py`）

1. 解析 yanshan .sty 的 `\definecolor{defense…}{HTML}{……}`，与本 design §2.4 的六个 hex 值比较。
2. 两主题都含 `\RequirePackage{defense-layouts}`，且不含父 design §5 列出的任一版式宏的 `\newcommand`/`\NewDocumentCommand` 定义。
3. `slide-layouts.md` 版式表的十二个版式名与 `demo-deck.tex` 中 `% layout: <name>` 注释集合相等。
4. 读取 `time-budget.md` 三档行，核对区间端点与 §2.5 公式一致。
5. 编译用例：`DEFENSE_ZH_COMPILE=1` 且 `shutil.which("xelatex")` 时，在 tmp_path 复制 templates/beamer/ 并用合成 PNG
   作校徽编译两主题；断言 PDF 页数（PyMuPDF 可用时读页数，否则解析 log 的 `Output written on … (N pages`）
   等于 `\begin{frame}` 计数，且 log 无 `Overfull \vbox`。否则 skip。

另有既有契约测试覆盖 docs 登记：`tests/contracts/test_docs_bilingual_resources.py`（manifest 与源一致、安装页命令）；
`check_resource_sync.py --skill latex-defense-zh` 覆盖双语页形状与同语言一致性。
