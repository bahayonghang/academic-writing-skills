# 清单与规划字段

本文件规定提取清单 `inventory.json` 与答辩稿规划 `slide_plan.yaml` 的字段、类型与取值，以及构建脚本的校验、转义与源文本变换规则。版式见 [版式目录](slide-layouts.md)，文字写法见 [内容规范](content-rules.md)，页数与秒数见 [时长预算](time-budget.md)。

## 流水线

```bash
uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis <THESIS_REPO> --out inventory.json [--main FILE] [--json]
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory inventory.json --out slide_plan.yaml [--minutes 40] [--stage predefense|defense] [--theme yanshan|generic]
uv run python -B $SKILL_DIR/scripts/plan_deck.py --plan slide_plan.yaml --outline
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan slide_plan.yaml --inventory inventory.json --out DIR [--logo PATH] [--force] [--compile]
```

1. `extract_thesis.py` 只读论文仓库，写出清单。
2. `plan_deck.py` 由清单生成规划骨架，待填字段写占位符。
3. LLM 按 [内容规范](content-rules.md) 填写占位符。`--outline` 按页序输出帧标题与结论句，交用户确认。
4. `build_deck.py` 校验规划，写出答辩稿、讲稿与主题文件。加 `--compile` 时用 latexmk 编译。

| 脚本                | 退出码                                                                                                  |
| ------------------- | ------------------------------------------------------------------------------------------------------- |
| `extract_thesis.py` | 0：成功，有告警时也为 0；2：论文目录不存在、主文件缺失，或有多个主文件候选且未指定                      |
| `plan_deck.py`      | 0：成功；2：参数错误、输入文件无法读取，或分钟数与章角色不在 [时长预算](time-budget.md) 的适用范围内    |
| `build_deck.py`     | 0：成功；2：输入错误或校验未通过；4：输出目录已有自有文件且未加 `--force`；5：未找到 latexmk 或编译失败 |

## 清单

清单为 UTF-8 JSON。清单含论文根目录的绝对路径，保存在用户工作目录，不提交到公开仓库。

源位置字段 `source` 写作「相对论文根的文件路径:行号」，例如 `chapters/chapter3.tex:20`。

本文件中的「纯文本」指以下处理的结果：删除 `\label`、引用类命令与 `\footnote`；`\\` 与 `~` 换为空格；格式命令（例如 `\textbf`）只保留参数文字；删除其余命令名与花括号。

### 顶层字段

| 字段           | 类型          | 说明                                            |
| -------------- | ------------- | ----------------------------------------------- |
| `thesis_root`  | 字符串        | 论文根目录的绝对路径，`/` 分隔                  |
| `main_tex`     | 字符串        | 主文件，相对论文根                              |
| `degree`       | 字符串        | `doctor`、`master` 或 `unknown`，取自文档类选项 |
| `meta`         | 映射          | 封面字段                                        |
| `logo`         | 字符串或 null | 校徽文件，相对论文根                            |
| `graphicspath` | 字符串列表    | 主文件 `\graphicspath` 的各项，相对主文件目录   |
| `chapters`     | 列表          | 章节树                                          |
| `figures`      | 列表          | 图                                              |
| `tables`       | 列表          | 表                                              |
| `equations`    | 列表          | 带标签的编号公式                                |
| `algorithms`   | 列表          | 算法                                            |
| `publications` | 列表          | 攻读学位期间取得的成果                          |
| `conclusion`   | 映射          | 结论章的贡献与展望条目                          |
| `macros`       | 列表          | 导言区宏定义                                    |
| `warnings`     | 列表          | 提取告警                                        |

主文件选择：`--main` 优先。否则候选为论文根目录下同时含 `\documentclass` 与 `\begin{document}` 的 `.tex` 文件。有多个候选时，去掉文件名含 `blind`、`anon`、`review`（不区分大小写）或「盲审」的候选；剩一个时选用该文件并写告警 `W-MAIN`，否则退出 2。

主文件中的 `\input`、`\include` 与 `\subfile` 按文档顺序展开。解析前删除注释。

### 封面字段 meta

| 字段                                  | 取值规则                                                                                           |
| ------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `title_zh`、`title_en`                | `\title{中文题目}{英文题目}` 的两个参数；只有一个参数时只取 `title_zh`                             |
| `author`、`school`、`subject`、`date` | 同名命令的第一个参数                                                                               |
| `supervisor`、`supervisor_title`      | `\supervisor` 的前两个参数：姓名与职称                                                             |
| `title_lines`                         | 导言区中名字以 `titlelines` 结尾的宏，其定义体按 `\\` 切分的各行；无此宏时为只含 `title_zh` 的列表 |

字段值为纯文本。`title_zh`、`author`、`supervisor`、`school`、`subject`、`date` 缺失时为空串，并写告警 `W-META`。其他文档类的键值式设置（例如 `\thusetup{…}`）不解析，缺失字段在规划的 `meta` 中补全。

### 章节树 chapters

| 字段              | 类型          | 说明                                                                                    |
| ----------------- | ------------- | --------------------------------------------------------------------------------------- |
| `number`          | 整数          | 章号：正文中非星号 `\chapter` 的出现序号，从 1 起；遇 `\appendix` 或 `\backmatter` 停止 |
| `title`           | 字符串        | 章题（长题）                                                                            |
| `short_title`     | 字符串或 null | `\chapter[短题]{长题}` 中的短题                                                         |
| `source`          | 字符串        | 源位置                                                                                  |
| `role_suggestion` | 字符串        | 建议章角色：`intro`、`foundation`、`research`、`application` 或 `conclusion`            |
| `role_evidence`   | 字符串        | 建议依据                                                                                |
| `role`            | 字符串，可选  | 用户指定的章角色；存在时 `plan_deck.py` 用该值代替 `role_suggestion`                    |
| `sections`        | 列表          | 节：`number`（`k.m`）、`title`、`short_title`、`source`、`kind`、`subsections`          |

章角色的识别提示见 [答辩稿框架](defense-framework.md)。建议有误时，在该章条目中加 `role` 字段，再运行 `plan_deck.py`。

节型 `kind` 按节题判定：含「引言」或「概述」为 `intro`；含「问题描述」「问题定义」或「问题建模」为 `problem`；含「实验」「仿真」「案例」或「结果」为 `experiment`；含「小结」为 `summary`；其余为 `method`。`subsections` 的每项含 `number`（`k.m.p`）、`title`、`short_title` 与 `source`。

### 图 figures

| 字段                    | 类型          | 说明                                                         |
| ----------------------- | ------------- | ------------------------------------------------------------ |
| `label`                 | 字符串        | 环境顶层第一个 `\label`；无标签时为 `auto:fig:<章号>-<序号>` |
| `number`                | 字符串        | 论文图号，例如 `3-2`                                         |
| `number_source`         | 字符串        | `aux` 或 `computed`                                          |
| `caption`               | 字符串        | 题注源文本                                                   |
| `chapter`               | 整数          | 所在章号                                                     |
| `section`、`subsection` | 字符串或 null | 所在节号与小节号，例如 `3.3`、`3.3.2`                        |
| `files`                 | 列表          | 每个 `\includegraphics` 一项：`path`、`resolved`、`exists`   |
| `subfigures`            | 列表          | 子图：`letter`、`caption`、`file`、`label`、`number`         |
| `source`                | 字符串        | 源位置                                                       |

- 提取范围：`figure` 与 `figure*` 环境中有题注的图。
- 编号：论文根目录下任一 `*.aux` 文件的 `\newlabel` 给出标签的编号时，取该编号，`number_source` 为 `aux`。读取 aux 时跳过以 `.` 开头的目录；同一标签出现在多个文件中时，取目录层级最浅的文件。否则按章内出现顺序计算为「章号 + 分隔符 + 序号」，`number_source` 为 `computed`；分隔符取 aux 编号中的 `-` 或 `.`，没有 aux 文件时为 `-`。
- 题注：`\bicaption` 取中文参数，`\caption` 取长题；删去 `\label`，其余源文本不变。
- 图片文件：`path` 为源文件中的原字符串；`resolved` 为解析到的文件，相对论文根。解析顺序为 `graphicspath` 各项，再主文件目录；原路径无扩展名时依次尝试 `.pdf`、`.png`、`.jpg`、`.jpeg`、`.eps`。文件不存在时 `exists` 为 `false`，并写告警 `W-FIG-FILE`。
- 子图：来自 `\subcaptionbox` 与 `subfigure` 环境。字母按出现顺序为 a、b、c……；`\subcaptionbox*` 的子图没有字母。子图编号优先取 aux，否则为「图号(字母)」。`file` 为子图中第一个 `\includegraphics` 的原字符串。

### 表 tables

表的 `label`（无标签时为 `auto:tab:<章号>-<序号>`）、`number`、`number_source`、`caption`、`chapter`、`section`、`subsection` 与 `source` 的规则同图。另有一个字段：

| 字段             | 类型          | 说明                                                                                                               |
| ---------------- | ------------- | ------------------------------------------------------------------------------------------------------------------ |
| `tabular_source` | 字符串或 null | 环境内第一个 `tabular`、`tabular*`、`tabularx`、`xltabular` 或 `longtable` 环境的原文，从 `\begin` 到配对的 `\end` |

提取范围：`table` 与 `table*` 环境中有题注的表。未找到表体时 `tabular_source` 为 null，并写告警 `W-TABLE-BODY`。

### 公式 equations

提取范围：`equation`、`align`、`gather`、`multline`、`flalign` 与 `eqnarray` 的非星号环境中，至少有一个带编号标签的环境。

| 字段                               | 类型   | 说明                                                |
| ---------------------------------- | ------ | --------------------------------------------------- |
| `label`、`number`、`number_source` | 字符串 | 第一个标签的值                                      |
| `labels`                           | 列表   | 全部标签，每项含 `label`、`number`、`number_source` |
| `env`                              | 字符串 | 环境名                                              |
| `tex`                              | 字符串 | `\begin{…}` 与 `\end{…}` 之间的原文                 |

`chapter`、`section`、`subsection` 与 `source` 同图。

计算编号按章内计数：`equation` 与 `multline` 整体计 1 个编号；其余环境按顶层 `\\` 分行，每个非空行计 1 个编号。含 `\notag` 或 `\nonumber` 的行不计编号，该行的标签只在 aux 中有编号时收录。含 `\tag{x}` 的行编号为 x，不计入章内计数。

### 算法 algorithms

提取范围：`algorithm` 环境中有题注的算法。字段为 `label`（无标签时为 `auto:alg:<章号>-<序号>`）、`number`、`number_source`、`caption`、`chapter`、`section`、`subsection` 与 `source`。清单不记录算法体。本版没有算法版式。

### 成果 publications

| 字段       | 类型     | 说明                                                                  |
| ---------- | -------- | --------------------------------------------------------------------- |
| `id`       | 字符串   | `P1`、`P2`……，按出现顺序                                              |
| `category` | 字符串   | 所属类别：前一个 `\achievementcategory{…}` 或 `\section*{…}` 的纯文本 |
| `text`     | 字符串   | 著录纯文本，已删去章号标注                                            |
| `chapters` | 整数列表 | 章号标注给出的章号，升序；无标注时为空列表                            |

- 成果块按以下顺序查找，取第一个找到的：`\achievement{…}` 的参数；`achievements` 环境；题含「成果」或「发表的学术论文」的 `\chapter` 或 `\chapter*`，到下一个 `\chapter` 为止。块内每个 `\item` 生成一条成果。没有成果时写告警 `W-PUB`。
- 章号标注的写法示例：「对应论文第三、四章」「对应第3-5章」「（对应本文第2章和第4章）」。章号可用阿拉伯数字或中文数字（一至九十九）。「至」「-」「~」「—」「–」表示区间；「、」「，」「和」「及」「与」分隔多个章号。

### 结论 conclusion

| 字段            | 类型        | 说明                                           |
| --------------- | ----------- | ---------------------------------------------- |
| `chapter`       | 整数或 null | 结论章章号：建议角色为 `conclusion` 的最后一章 |
| `contributions` | 字符串列表  | 贡献条目                                       |
| `outlook`       | 字符串列表  | 展望条目                                       |

条目来源为顶层列表的 `\item`，以及以「（1）」「(1)」「1.」「1、」等编号开头的段落。第一个含「展望」「未来」「今后」或「下一步」的标题或段落之后的条目归入 `outlook`，之前的条目归入 `contributions`。条目开头的编号已删除。没有结论章时写告警 `W-CONCLUSION`。

### 宏 macros

| 字段         | 类型   | 说明                                                                                                |
| ------------ | ------ | --------------------------------------------------------------------------------------------------- |
| `name`       | 字符串 | 宏名，不含反斜杠                                                                                    |
| `command`    | 字符串 | 定义命令：`newcommand`、`renewcommand`、`providecommand`、`DeclareMathOperator`（可带 `*`）或 `def` |
| `definition` | 字符串 | 定义原文                                                                                            |
| `source`     | 字符串 | 源位置                                                                                              |

收集范围为主文件导言区，含导言区中展开的文件。

### 校徽 logo

在 `graphicspath` 的各目录中查找校徽；没有 `graphicspath` 时在主文件目录中查找。文件名主干含 `logo`、`badge`（不区分大小写）或「校徽」的图片恰有一个时，`logo` 为其路径；否则为 null，并写告警 `W-LOGO`。

### 告警 warnings

每条告警含 `code`、`message` 与 `source`（可为 null）。

| 代码           | 条件                                                  |
| -------------- | ----------------------------------------------------- |
| `W-MAIN`       | 有多个主文件候选，去掉盲审版后剩一个并选用            |
| `W-META`       | 封面字段缺失                                          |
| `W-ENCODING`   | 源文件不是 UTF-8，已按 GB18030 解码，或有字符无法解码 |
| `W-INCLUDE`    | `\input`、`\include` 或 `\subfile` 的目标文件不存在   |
| `W-FIG-FILE`   | 图片文件不存在                                        |
| `W-TABLE-BODY` | 表环境中没有表体环境                                  |
| `W-PUB`        | 未找到成果列表，或列表中没有条目                      |
| `W-CONCLUSION` | 未识别出结论章                                        |
| `W-LOGO`       | 未找到校徽文件，或找到多个候选                        |

## 规划

规划为 UTF-8 YAML，由 `plan_deck.py` 生成骨架。LLM 填写占位符，并按需调整版式、图表选择与 `meta`。

### 占位符

待填字段写占位符 `〔待填写〕`。内容页的待填字段为 `takeaway`、`bullets` 的各条、`notes.say`、`notes.key`、`notes.transition` 与 `notes.questions` 的各条。封面与目录帧的待填字段为 `notes.say` 与 `notes.transition`。致谢帧的 `notes.say` 预填「汇报完毕，请各位老师批评指正。」。

`--outline` 的末行给出帧数、内容页数与占位符数。`build_deck.py` 不检查占位符；残留占位符由质量门报告。

### 规划 meta

| 字段                                                                    | 类型          | 说明                                       |
| ----------------------------------------------------------------------- | ------------- | ------------------------------------------ |
| `stage`                                                                 | 字符串        | `predefense`（预答辩）或 `defense`（答辩） |
| `theme`                                                                 | 字符串        | `yanshan` 或 `generic`                     |
| `minutes`                                                               | 正整数        | 汇报分钟数，默认 40                        |
| `title_lines`                                                           | 字符串列表    | 封面标题的各行                             |
| `author`、`supervisor`、`supervisor_title`、`subject`、`school`、`date` | 字符串        | 封面字段，初值取自清单的 `meta`            |
| `logo`                                                                  | 字符串或 null | 校徽文件，相对论文根                       |
| `inventory_sha256`                                                      | 字符串        | 生成骨架时清单文件的 SHA-256               |
| `extra_packages`                                                        | 字符串列表    | 追加的宏包名                               |
| `chapters`                                                              | 列表          | 每章一项：`number`、`title`、`role`        |

- `stage` 与 `minutes` 在生成骨架时决定页序与每页秒数。生成后修改这两个字段不增删帧；需要改阶段或时长时，重新运行 `plan_deck.py`。`defense` 阶段在展望页之后加成果页 `achievements`。`stage` 另决定封面的阶段字样。
- `extra_packages` 的每项须匹配 `^[A-Za-z0-9-]+$`，在固定宏包之后逐个 `\usepackage`。固定宏包为 amsmath、amssymb、mathtools、bm、booktabs、multirow、makecell、tabularx、array、threeparttable、siunitx 与 adjustbox。
- `chapters` 的 `title` 优先取短题。构建脚本用 `chapters` 生成目录页的章表。

### 帧序列与 id

帧序列为：封面 `cover`；总目录 `toc`；第 1 章各页；对第 k 章（k ≥ 2），章前目录 `c<k>-toc` 与第 k 章各页；致谢 `thanks`。内容页 id 为 `c<k>-<role>`；同一章同一角色有多页时为 `c<k>-<role>-<i>`，i 从 1 起。

### 帧字段

| 字段         | 类型          | 说明                                                                                               |
| ------------ | ------------- | -------------------------------------------------------------------------------------------------- |
| `id`         | 字符串        | 帧 id，全稿唯一，匹配 `^[A-Za-z0-9][A-Za-z0-9_-]*$`                                                |
| `role`       | 字符串        | 页角色，见 [答辩稿框架](defense-framework.md)                                                      |
| `layout`     | 字符串        | 版式名，见 [版式目录](slide-layouts.md)                                                            |
| `chapter`    | 整数或 null   | 章号；封面与致谢为 null，总目录为 0                                                                |
| `section`    | 字符串        | 帧标题                                                                                             |
| `subsection` | 字符串        | 小节条；空串时不输出                                                                               |
| `position`   | 字符串        | 只用于 `figure-bullets`：`left`（默认）或 `top`                                                    |
| `takeaway`   | 字符串        | 结论句                                                                                             |
| `bullets`    | 字符串列表    | 要点；`cards` 版式每条一张卡片，`outlook` 版式每条一项                                             |
| `figures`    | 映射列表      | 每项含 `label`，可带 `subfigures`（子图字母列表）与 `width`（图宽占行宽的比例，大于 0 且不大于 1） |
| `equations`  | 映射列表      | 每项含 `label`，取公式的任一标签                                                                   |
| `table`      | 字符串或 null | 表标签                                                                                             |
| `paper`      | 字符串或 null | 成果 id，渲染为「论文」框                                                                          |
| `notes`      | 映射          | 讲稿：`say`、`key`、`seconds`（整数）、`transition`、`questions`（字符串列表）                     |
| `source`     | 字符串列表    | 所映射节与所选图表的源位置；只读，不渲染                                                           |
| `hints`      | 字符串列表    | 节题、图表题注、研究内容、结论条目或成果著录；只读，不渲染                                         |

`cover`、`toc` 与 `thanks` 版式的帧只使用 `id`、`role`、`layout`、`chapter` 与 `notes`。`width` 对 `figure-grid` 无效。

### 骨架预填规则

| 字段                            | 预填规则                                                                                                                                                                                                     |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `layout`                        | 按页角色与候选图表选择，见下表                                                                                                                                                                               |
| `section`                       | 所映射第一节的「节号 节题」（短题优先）；没有可映射的节时为章题                                                                                                                                              |
| `subsection`                    | 研究章 `intro` 页为「研究内容 i：章题」；`innovation`、`outlook`、`achievements` 页为「01　主要创新点」「02　未来研究展望」「03　攻读学位期间取得的成果」；只映射到一个小节时为「小节号 小节题」；其余为空串 |
| `figures`、`equations`、`table` | 从所映射节中按出现顺序取前页未用的第一个候选                                                                                                                                                                 |
| `bullets`                       | `figure`、`figure-grid`、`table` 版式为空列表；`challenges` 与 `innovation` 的条数等于研究章数；`outlook` 的条数为结论展望条目数，至多 3 条，没有条目时为 2 条；其余为 1 条                                  |
| `paper`                         | `summary` 页取章号标注含本章的第一条成果；同章的其他成果写入 `hints`                                                                                                                                         |
| `notes.seconds`                 | 时长预算给出的每页秒数                                                                                                                                                                                       |

| 页角色                                   | 默认版式                                                                                                     |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `challenges`、`innovation`               | `cards`                                                                                                      |
| `summary`                                | `paper-summary`                                                                                              |
| `outlook`                                | `outlook`                                                                                                    |
| `method`、`foundation`                   | 有公式候选时 `equations-figure`；否则有图候选时 `figure-bullets`；否则 `bullets`                             |
| `experiment`                             | 有图候选时 `figure`，该图至少有 2 个带字母的子图时 `figure-grid`；无图候选有表候选时 `table`；否则 `bullets` |
| `application`                            | 有图候选时 `figure`；无图候选有表候选时 `table`；否则 `bullets`                                              |
| `status`、`organization`、`architecture` | 有图候选时 `figure`；否则 `bullets`                                                                          |
| `background`、`problem`、`intro`         | 有图候选时 `figure-bullets`；否则 `bullets`                                                                  |
| `achievements`                           | `bullets`                                                                                                    |

- 候选条件：图至少有一个 `\includegraphics`；表的 `tabular_source` 非空，且不是 `longtable` 或 `xltabular` 环境。
- `figure-grid` 预选前 6 个子图字母。研究章 `intro` 页的 `figure-bullets` 预填 `position: top`，其余为 `left`。
- 绪论章：`background`、`status`、`challenges`、`organization` 页分别映射到节题含「背景」「意义」，「现状」「综述」「进展」，「问题」「挑战」，「内容」「安排」「组织」的第一节。
- 研究章：`intro`、`problem`、`summary` 页映射到对应节型的第一节；`method` 与 `experiment` 页分配到对应节型的全部节。
- 基础章：`foundation` 页分配到节型不为 `intro` 与 `summary` 的节。
- 应用章：`intro` 页映射到节型为 `intro` 的节，没有时取第一节；`architecture` 页映射到节题含「架构」「总体」「框架」或「结构」的节；`application` 页分配到其余节，节型为 `summary` 的节除外。
- 结论章各页不映射节。
- 分配规则：页数不多于节数时，相邻节合并到同一页，各页节数相差不超过 1，靠前的页多一节。页数多于节数时，每节至少一页；一节有多页时，再把这些页按同一规则分配到该节的小节。

## 构建规则

### 校验

以下任一项不满足时，`build_deck.py` 列出全部错误并退出 2，不写任何文件：

- 规划：`meta` 为映射；`meta.stage` 与 `meta.theme` 取值合法；`meta.minutes` 为正整数；`meta.title_lines` 为列表；`meta.chapters` 的每项为含 `number` 与 `title` 的映射；`meta.extra_packages` 的每项符合宏包名规则；`frames` 为非空列表；帧 id 符合 id 规则且不重复。
- 帧：`role` 与 `layout` 在允许集合内；目录帧的 `chapter` 为 0 或章号；`notes` 为映射，`notes.seconds` 为整数，`notes.questions` 为列表；`bullets` 为列表。
- 引用：`figures` 的每项为含 `label` 的映射，标签在清单中；所选子图字母存在，且该子图有图片文件；`width` 大于 0 且不大于 1；`figure-grid` 以外版式的图至少有一个图片文件；`equations`、`table` 与 `paper` 引用的标签或 id 在清单中。
- 版式：`figure`、`figure-bullets`、`figure-grid` 恰有 1 幅图；`figure-grid` 选 2–6 个子图字母；`equations-figure` 有 1–4 个公式，至多 1 幅图；`table` 版式有 `table` 字段，所引用的表有表体，且表体不是 `longtable` 或 `xltabular` 环境。
- 命令行：`--logo` 文件存在；`--out` 不是已有的普通文件。

以下情况只告警，构建继续：`meta.inventory_sha256` 与当前清单不一致；字段在所选版式中不显示，例如 `figure` 版式的 `bullets`；图含多个图片文件，只显示第一个；校徽文件不存在；论文仓库与输出目录不在同一盘符。告警写到标准输出与 `build_manifest.json`。

### 文本转义

转义用于规划的 `section`、`subsection`、`takeaway`、`bullets`、`meta` 封面字段、`meta.chapters` 的章题与成果著录文本。规则按以下顺序执行：

1. 连续空白（含换行）合并为一个空格。
2. `**词**` 渲染为 `\DefenseHighlight{词}`；未配对的 `**` 按普通字符输出。
3. 其余字符按下表替换。

| 字符                    | 输出                 |
| ----------------------- | -------------------- |
| `\`                     | `\textbackslash{}`   |
| `{`、`}`                | `\{`、`\}`           |
| `$`、`&`、`#`、`%`、`_` | 前加 `\`             |
| `~`                     | `\textasciitilde{}`  |
| `^`                     | `\textasciicircum{}` |

以 `[` 或 `<` 开头的要点前加 `{}`，以免 `\item` 把它读作可选参数或叠层参数。以 `[` 或 `*` 开头的标题行前加 `{}`。文本字段不支持内联数学与 LaTeX 命令；公式用 `equations` 字段。

### 题注

图题注输出为 `图<编号>\quad` 加 `DefenseSource` 环境中的题注源文本；表题注为 `表<编号>\quad` 加题注源文本；子图题注为 `(<字母>)` 加子图题注源文本。题注源文本不转义。在 `DefenseSource` 环境中，`\ref` 与 `\eqref` 输出论文编号，引用命令不输出。

### 公式

- 输出为 `\begin{<env>*}`、变换体与 `\end{<env>*}`，整体放在 `DefenseSource` 环境中。
- 变换体：清单 `tex` 中每个 `\label{x}` 替换为 `\tag*{(<x 的编号>)}`，其余字符不变。
- 以下标签直接删除，不加 `\tag*`：所在行已有 `\tag`；同一行中第一个以外的标签；清单中没有编号的标签；`eqnarray` 的全部标签。`eqnarray*` 不支持 `\tag`，编号在公式下方列出，例如 `(4-1)\quad (4-2)`。
- 行的划分同清单的编号计算：`equation` 与 `multline` 整体为一行，其余环境按顶层 `\\` 分行。
- 没有删除标签时，把变换体中的 `\tag*{(<编号>)}` 换回对应的 `\label{x}`，结果与清单 `tex` 逐字相同。

变换示例（第一段为清单 `tex` 所在的论文环境，第二段为答辩稿输出）：

```latex
\begin{align}
  \vect{h}_{t} &= \sigma\left(W_{x}\vect{x}_{t} + W_{h}\vect{h}_{t-1}\right) \label{eq:c4-hidden}\\
  \vect{z}_{t} &= \operatorname{concat}\left(\vect{h}_{t}, \vect{s}_{t}\right) \nonumber\\
  \hat{\vect{y}}_{t+1} &= W_{o}\vect{z}_{t} + b \label{eq:c4-output}
\end{align}
```

```latex
\begin{DefenseSource}
\begin{align*}
  \vect{h}_{t} &= \sigma\left(W_{x}\vect{x}_{t} + W_{h}\vect{h}_{t-1}\right) \tag*{(4-1)}\\
  \vect{z}_{t} &= \operatorname{concat}\left(\vect{h}_{t}, \vect{s}_{t}\right) \nonumber\\
  \hat{\vect{y}}_{t+1} &= W_{o}\vect{z}_{t} + b \tag*{(4-2)}
\end{align*}
\end{DefenseSource}
```

### 表体

`tabular_source` 的原文不变，放在 `DefenseSource` 环境中，再外包 `\adjustbox{max width=\textwidth,max totalheight=0.62\textheight}`。表题注在表体上方。`longtable` 与 `xltabular` 放在 `\adjustbox` 中时编译失败，因此 `plan_deck.py` 不预选这类表，`build_deck.py` 遇到时退出 2。

### 图与校徽路径

- `\graphicspath` 的各项为主文件目录下的 `graphicspath` 各项与主文件目录本身，写成相对输出目录的路径，`/` 分隔，以 `/` 结尾。输出目录与论文仓库不在同一盘符时写绝对路径，并告警。
- `\DefenseFigure` 的文件参数写清单 `files` 第一项的 `path` 原字符串；`figure-grid` 版式写所选子图的 `file`。
- 校徽路径的优先顺序为 `--logo`、规划的 `meta.logo`、清单的 `logo`；后两者相对论文根。校徽文件不存在时告警，封面按主题显示文字标识或不显示校徽。

### 宏

`thesis-macros.tex` 收集所选图的题注与子图题注、公式、表题注与表体中用到的论文宏，并递归加入这些宏的定义中用到的宏。宏按导言区顺序输出，每个宏前一行为注释，写源位置：

- `\newcommand`、`\renewcommand` 与 `\providecommand` 的定义改写为 `\providecommand`。
- `\DeclareMathOperator` 与 `\def` 的定义外包 `\ifdefined\<名>\else … \fi`。

### 标签与编号

`defense.tex` 的导言区为清单中每个图、子图、表、算法与公式标签写一行 `\DefenseDefineLabel{<label>}{<编号>}`，以 `auto:` 开头的合成标签除外。在 `DefenseSource` 环境中，`\ref{<label>}` 输出论文编号，`\eqref` 另加圆括号；未登记的标签输出 `??`。

### 输出文件

| 文件                                                                                    | 内容                                                                                        |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `defense.tex`                                                                           | 答辩稿                                                                                      |
| `thesis-macros.tex`                                                                     | 论文宏                                                                                      |
| `notes.md`                                                                              | 讲稿，格式见 [讲稿格式](speaker-notes.md)                                                   |
| `build_manifest.json`                                                                   | 技能版本、主题、阶段、帧数、规划与清单的 SHA-256、其余六个文件的 SHA-256 与告警；不含时间戳 |
| `beamerthemeYanshanDefense.sty`、`beamerthemeGenericDefense.sty`、`defense-layouts.sty` | 主题与版式宏包的副本                                                                        |

这七个文件为构建脚本的自有文件。任一自有文件已存在且未加 `--force` 时，构建脚本退出 4，不写任何文件。`--force` 只覆盖自有文件，不删除输出目录中的其他文件。内容与现有文件相同的自有文件不重写，保留修改时间：latexmk 按内容判定无需重编时，`defense.pdf` 不会早于 `defense.tex`。

`defense.tex` 在每个 `\begin{frame}` 的前一行写帧标记。质量门用帧标记映射行号、页角色与页序：

```latex
% defense-frame: id=<id> role=<role> chapter=<n|-> layout=<layout>
```

`chapter` 为 null 时写 `-`。

加 `--compile` 时，构建脚本在输出目录运行 `latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error defense.tex`，时限 600 秒。编译失败时，构建脚本在标准错误输出 `defense.log` 的末 40 行，并退出 5。

## 已知限制

- 文本字段不支持内联数学与 LaTeX 命令。
- 论文用 `\renewcommand` 改写的标准命令，在答辩稿中保持标准定义，因为 `\providecommand` 不覆盖已有定义。
- 文档类或论文自带宏包中定义的宏不复制。编译报未定义命令时，把所需宏包加入 `meta.extra_packages`，或改选不含该命令的图表。
- `longtable` 与 `xltabular` 表不能用于 `table` 版式。
- 没有 `\includegraphics` 的图（例如用 TikZ 绘制的图）不能用于图版式。
- 结论条目按建议角色提取；用 `role` 字段改章角色后，`conclusion` 不重新提取。
- 其他文档类的键值式封面设置（例如 `\thusetup{…}`）不解析。
- 文件展开只处理 `\input`、`\include` 与 `\subfile`。
