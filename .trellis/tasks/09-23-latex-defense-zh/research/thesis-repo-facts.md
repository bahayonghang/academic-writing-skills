# 目标论文仓库结构事实（2026-09-23）

来源：用户在会话中给出的本机博士论文仓库（下文记为 `<THESIS_REPO>`；绝对路径不写入仓库文件）。
只读核对，未修改、未编译该仓库。本文件只记录结构与计数，不记录论文正文、结果数字或私有文件名以外的内容。

## 1. 入口与类文件

- 主文件 `document.tex`；另有盲审版 `document_blind.tex`。两者都含 `\documentclass` 和 `\begin{document}`。
- `\documentclass[doctor,academic]{ysuthesis}`，XeLaTeX 编译。
- 元数据命令为双参数（中文、英文）：`\title{中}{英}`、`\author{中}{英}`、`\school{中}{英}`、`\subject{中}{英}`、
  `\date{中}{英}`；`\supervisor{中名}{中职称}{英名}{英职称}`。
- 封面题目换行由导言区 `\newcommand{\ysuctitlelines}{…\\…}` 提供；`\title{}` 内不含 `\\`。
- `\graphicspath{{fig/}}`；图片在 `fig/chapterN/<子目录>/`，文件名含中文；格式为 PNG。
- 校徽文件 `fig/ysu_logo.png`，1351 × 397 像素，RGB。
- 章节用 `\include{chapters/chapterN}`（N = 1..7），每章生成 `chapters/chapterN.aux`；
  aux 中 `\newlabel{fig:…}{{3-2}{36}{中文图题}{figure.caption.21}{}}` 给出论文最终图号与图题。
- 图题：`\bicaption{中文}{英文}`；子图：`\subcaptionbox{子题}[宽]{\includegraphics…}`（类文件注释另提 `\bisubcaptionbox`，
  正文当前未使用）。类文件在第 16 行加载 bicaption、booktabs、makecell、tabularx、xltabular、newtxmath。
- 成果列表写在 `document.tex` 的 `\achievement{…}` 中，`\achievementcategory{1. 发表及录用的学术论文}` 下的 `\item`
  以「（…，对应论文第三章）」形式标注章对应关系；专利与奖励为另两类。

## 2. 章结构与计数

| 章 | 角色 | 节数 | includegraphics | figure 环境 | table | 公式环境 | algorithm |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 绪论 | 4（研究现状含 3 小节） | 1 | 1 | 0 | 0 | 0 |
| 2 | 基础章（分析与框架类章题） | 6 | 7 | 7 | 1 | 12 | 0 |
| 3 | 研究章 | 5 | 29 | 11 | 5 | 42 | 1 |
| 4 | 研究章 | 5 | 16 | 8 | 6 | 32 | 1 |
| 5 | 研究章 | 5 | 35 | 14 | 7 | 54 | 1 |
| 6 | 应用章（章题含「平台」「设计」「应用」） | 5 | 15 | 13 | 10 | 4 | 0 |
| 7 | 结论 | 0（无 \section） | 0 | 0 | 0 | 0 | 0 |

- 第 1 章节序：研究背景与意义 → 国内外研究现状（3 小节）→ 研究问题与关键挑战（enumerate 三项）→ 研究内容与章节安排（1 张组织结构图）。
- 研究章节序统一为：引言 → 问题描述 → 方法（2–3 小节）→ 实验与结果分析（3–4 小节）→ 本章小结。
- 第 7 章无小节，正文用「（1）…（2）…（3）…」列出贡献，另有一段平台工作，再用「（1）（2）」列出展望。
- 研究问题数（3）= 研究章数（3）；第 2 章为基础章，不对应研究问题。

## 3. 对技能设计的约束

1. 章角色不能按章号写死：本仓库第 2 章是基础章，参考 pptx 的第 2 章是研究章。提取脚本给出角色建议，规划文件允许覆盖。
2. 图号以 aux 为准；aux 缺失时按章内顺序计算并标记 `number_source: computed`。
3. 子图通过 `\subcaptionbox` 取子题；同一 figure 环境下的多个 includegraphics 构成一个子图组。
4. 成果—章对应关系可从「对应论文第X章」确定性解析；中文数字章号需转换。
5. 盲审版主文件与正式版共存；主文件选择需要显式参数或确定规则（优先 `document.tex`，存在多个候选时报告并要求 `--main`）。
6. 图片路径含中文和子目录；答辩稿引用原图，不复制，`\graphicspath` 用相对路径指回论文 `fig/`。
