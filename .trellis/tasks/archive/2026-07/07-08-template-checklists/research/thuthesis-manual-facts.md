# Research: thuthesis 模板手册事实（v7.7.1）

- **Query**: thuthesis 模板手册事实——图表/公式编号、参考文献样式、摘要关键词命令、目录章节层级等
- **Scope**: external（GitHub tuna/thuthesis 源码与手册源文件 + CTAN + GitHub API）
- **检索日期**: 2026-07-09
- **抓取方式**: MCP exa 工具在本会话不可用，改用 Bash `curl -sL` 抓取（任务允许的兜底方式）。
  手册 PDF 未直接抓取，改抓其唯一源文件 `thuthesis.dtx`（手册 thuthesis.pdf 即由该 dtx 生成，
  文档文本逐字一致），引用处标注 dtx 行号（master 分支 2026-07-09 快照）。
- **来源列表**:
  - https://raw.githubusercontent.com/tuna/thuthesis/master/thuthesis.dtx （手册+实现单一源）
  - https://raw.githubusercontent.com/tuna/thuthesis/master/README.md
  - https://raw.githubusercontent.com/tuna/thuthesis/master/CHANGELOG.md
  - https://raw.githubusercontent.com/tuna/thuthesis/master/thuthesis-example.tex
  - https://ctan.org/pkg/thuthesis （版本核对）
  - https://api.github.com/repos/tuna/thuthesis/releases/latest （版本核对）
- **指令式文本检查**: 抓取内容均为文档/代码，未发现指令式文本。

## Findings

### 版本基线

- GitHub 最新 release：**v7.7.1，发布于 2026-05-26**（GitHub API `tag_name=v7.7.1`,
  `published_at=2026-05-26T12:55:10Z`）。CTAN 页面同为 "Version 7.7.1 2026-05-26"。
- 模板编写依据（dtx 摘要节，行 74–87 原文）：
  > 本模板为作者根据清华大学研究生院颁发的《研究生学位论文写作指南》（更新到 2025 年 3 月版本，限校内网络访问）、英文版 *Guide to Thesis Writing for Graduate Students*、清华大学教务处颁发的《清华大学综合论文训练写作规范（试行）》……编写而成
  - 校内指南 URL（dtx 内嵌链接，校外不可访问）：
    `https://info2021.tsinghua.edu.cn/f/info/xxfb_fg/xnzx/template/detail?xxid=fa880bdf60102a29fbe3c31f36b76c7e`
- CHANGELOG v7.7.1（2026-05-26）：
  > 同步研究生论文《写作指南》2026 年 5 月版本的修改：统一博士、硕士授权页的措辞（#1064）。

  ——即《写作指南》存在 **2026 年 5 月版**，相对 2025-03 版的改动仅授权页措辞（据 CHANGELOG）。
- CHANGELOG v7.6.0（2025-03-28）同步 2025-03 版指南：
  > 非涉密论文的声明页中增加"不包含涉及国家秘密的内容"字样（#1000）；授权页的"《中华人民共和国学位条例暂行实施办法》"更新为"《中华人民共和国学位法》"（#1003）。

### 图表与公式编号（高价值：修正仓库既有快照）

- dtx 手册"图表编号"节（行 744–759）原文：
  > 研究生要求图表和公式的编号使用"."或"-"连接，**模板默认使用句点"."**。用户也可以通过 figure-number-separator、table-number-separator 等选项分别设置……也可以使用 number-separator 同时设置图、表、公式三项的编号连接符，比如 `\thusetup{number-separator = -}`。
- 实现（dtx 行 3665–3682）：`figure-number-separator` / `table-number-separator` /
  `equation-number-separator` / `number-separator` 四个选项，`default = {.}`。
- **含义**：现行 thuthesis 默认输出"图 2.1 / 表 3.1 /（3.1）"（点号），连字符"图 2-1"为可选配置。
  仓库现有 `templates/thuthesis.md` 写"格式：图 3-1（用连字符）"与 v7.7.1 默认不符，
  清单条目应写成"点号或连字符二选一、全篇统一（模板默认点号）"。
- 编号按章：v7.7.0 新增选项（CHANGELOG，加粗为默认值）：
  > `figure-numbering`: **`chapter`** / `global`；`table-numbering`: **`chapter`** / `global`；`equation-numbering`: **`chapter`** / `global`；`footnote-numbering`: **`page`** / `chapter` / `global`；`footnote-style`: **`circled`** / `plain`；`style-override`: **`none`** / `schwarzman`
  - 即图/表/公式默认按章编号（章号+分隔符+序号），脚注默认按页编号、带圈数字。
  - 苏世民学院变体（dtx 行 1661）："全文的脚注都连续编号（包括到附录中），不使用带圈数字；全文图、表、公式连续编号。"
- 分图编号（dtx 行 3772–3773）：`\thesubfigure = (\alph{subfigure})`，即 (a)(b)(c)。
- 图表标题（dtx 行 3745–3752 文档）："图表标题字体为 11pt；去掉图表号后面的冒号，图序与图名文字之间空一个汉字符宽度；图：caption 在下……表：caption 在上"。

### 章节层级与目录

- dtx "目录"节（行 4105–4110）原文：
  > 最多 4 层，即: x.x.x.x，对应的命令和层序号分别是：\chapter(0), \section(1), \subsection(2), \subsubsection(3)。

  代码：`\setcounter{secnumdepth}{3}`、`\setcounter{tocdepth}{2}`
  ——编号最深到 `\subsubsection`（如 2.1.2.1），**目录只收录到 `\subsection`（如 2.1.1，共三级条目）**。
- 研究生标题格式（dtx 行 3930–3953，模板对《写作指南》要求的转述）：
  > 各章标题，例如："第 1 章 引言"。章序号与章名之间空一个汉字符。采用黑体三号字，居中书写，单倍行距，段前空 24 磅，段后空 18 磅。
  > 一级节标题，例如："2.1 实验装置与实验方法"。……黑体四号（14pt）字居左书写，行距为固定值 20 磅，段前空 24 磅，段后空 6 磅。
  > 二级节标题，例如："2.1.1 实验装置"。采用黑体 13pt 字居左书写……段前空 12 磅，段后空 6 磅。
  > 三级节标题，例如："2.1.2.1 归纳法"。采用黑体小四号（12pt）字居左书写……
- 章名实现：`name = {第,章}`、`number = \thechapter`（阿拉伯数字）、`aftername = \quad`（dtx 行 3979–3986）。

### 摘要与关键词

- 用法（dtx 行 652–673）：摘要用 `abstract` / `abstract*` 环境（中文/英文）；
  > 关键词需要使用 \thusetup 进行设置。关键词之间以西文逗号隔开，模板会自动调整为要求的格式。关键词的设置只要在摘要环境结束前即可。

  ```latex
  \thusetup{ keywords = {关键词 1, 关键词 2}, keywords* = {keyword 1, keyword 2} }
  ```
- 输出格式（dtx 行 5266–5296）：中文摘要末尾自动输出 `关键词：`，各词间以全角分号"；"分隔
  （`\thu@clist@use{\thu@keywords}{；}`）；文档注释：
  > 中文摘要部分的标题为"摘要"，用黑体三号字。摘要内容用小四号字书写，两端对齐，汉字用宋体，外文字用 Times New Roman 体，标点符号一律用中文输入状态下的标点符号。

### 参考文献

- dtx "参考文献"节（行 955–1013）：
  > 研究生要求的参考文献格式基于《信息与文献 参考文献著录规则》（GB/T 7714—2015）进行了少量改编（如英文姓名不使用全大写），可以选择"顺序编码制"和"著者-出版年制"。
  - BibTeX 路线：`\usepackage[sort]{natbib}` + `\bibliographystyle{thuthesis-numeric}`（顺序编码）
    或 `\bibliographystyle{thuthesis-author-year}`（著者-出版年）；样式"由 gbt7714 的 .bst 进行了少量修改"。
  - biblatex 路线：`\usepackage[style=thuthesis-author-year]{biblatex}`（样式"由 biblatex-gb7714-2015 进行了少量改编"），输出用 `\printbibliography`。
  - 仓库根目录实际分发：`thuthesis-numeric.bst/.bbx/.cbx`、`thuthesis-author-year.bst/.bbx/.cbx`、
    `thuthesis-bachelor.bst/.bbx/.cbx`（本科生用）。
- 引用方式（dtx 行 913–941）："顺序编码制"两种模式：上标模式（如 `[1-2]` 右上角）与正文模式
  （"文 [3] 中详细说明了……"，用 `\thusetup{cite-style = inline}` 或 `\inlinecite`）；
  著者-出版年制提供 `\citep` / `\citet`。
- v7.7.0 CHANGELOG："中文著者-出版年制引用标注的括号改为全角（#1054）"。

### 前置/后置部分名称与结构（研究生，dtx 行 2020–2087）

- 研究生（硕/博）各部分标题名：`目　录`（目\quad 录）、`致　谢`、`插图清单`、`附表清单`、
  `插图和附表清单`、`符号和缩略语说明`、`参考文献`、`附录`、`索引`、`个人简历、在学期间完成的相关学术成果`、
  `指导教师评语`、`答辩委员会决议书`、`声　明`（声\hspace{1em}明）。
- thuthesis-example.tex 的骨架顺序（逐字注释）：封面 `\maketitle` → 名单 `data/committee` →
  授权 `\copyrightpage` → `\frontmatter` 摘要 → `\tableofcontents` → `\listoffigures`/`\listoftables` →
  符号 `data/denotation` → `\mainmatter` 各章 → 参考文献 → `\appendix` → `\backmatter` 致谢 →
  `\statement`（声明）→ `data/resume`（个人简历、在学期间完成的相关学术成果）→
  `data/comments`（指导教师/指导小组评语）→ `data/resolution`（答辩委员会决议书）。
- 例：`\documentclass[degree=master]{thuthesis}`；`degree: doctor | master | bachelor | postdoc`；
  `degree-type: academic（默认）| professional`。

### 页面与语言

- dtx "页面设置"节（行 1955–1959）转述《写作指南》：
  > 研究生《写作指南》：页边距：上下左右均为 3.0 厘米，装订线 0 厘米；页眉距边界：2.2 厘米，页脚距边界：2.2 厘米。
- 语言（dtx 行 426–429）：
  > 研究生《写作指南》要求"外国人来华留学生可以用英文撰写学位论文，但须采用中文封面"，"除留学生外，学位论文一律须用汉语书写"。
- 密级（dtx 行 590–591）：定义 `secret-level` 时封面显示密级，"并且从声明页中将移除'不包含涉及国家秘密的内容'字样（2025年3月写作指南更新有此要求）"。
- 编译：thuthesis-example.tex 头部 `% !TEX program = xelatex`；README"推荐下载发布版模板"。

### 与清单落地相关的映射提示

- 编号分隔符条目 → `llm`/`module:format`（默认点号、可选连字符、全篇统一；不能写死连字符）。
- 目录三级、编号四级 → `script:heading_depth`（THU 上限：编号 x.x.x.x，目录收录到三级条目）。
- 关键词分号分隔（输出层面模板自动保证）→ 主要检查 `.tex` 源里 keywords 用西文逗号分隔即可（manual/llm）。
- 参考文献样式条目 → `module:bibliography`（thuthesis-numeric / thuthesis-author-year / biblatex 派生样式）。

## Caveats / Not Found

- 手册 PDF（thuthesis.pdf）本身未抓取（CTAN texdoc PDF 直链未尝试解析），全部引用出自其唯一
  源文件 thuthesis.dtx 的文档注释，行号基于 master 2026-07-09 快照（与 v7.7.1 之间仅有
  Unreleased 小改动：本科生 survey/translation 恢复与封面布局修正，见 CHANGELOG Unreleased 节，
  不影响上述事实）。
- thuthesis 模板/手册**不含**任何字数、文献数量类阈值（题名字数、摘要字数、关键词个数上限等
  属于《写作指南》内容，见 `tsinghua-grad-spec.md`）。
