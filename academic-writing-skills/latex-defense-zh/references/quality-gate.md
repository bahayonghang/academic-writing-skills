# 质量门

本文件规定答辩稿质量门 `check_deck.py` 的 D-* 码、判据、阈值、严重度与处置方法，以及预览脚本 `render_preview.py` 的用法与目视清单。页角色见 [答辩稿框架](defense-framework.md)，版式见 [版式目录](slide-layouts.md)，文字写法见 [内容规范](content-rules.md)，页数与秒数见 [时长预算](time-budget.md)，讲稿格式见 [讲稿格式](speaker-notes.md)，规划字段见 [清单与规划字段](plan-schema.md)。

## 用法

```bash
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck DIR/defense.tex --inventory inventory.json [--plan slide_plan.yaml] [--log DIR/defense.log] [--minutes 40] [--json]
uv run python -B $SKILL_DIR/scripts/render_preview.py --pdf DIR/defense.pdf --out DIR/preview [--dpi 110] [--cols 4]
```

- `check_deck.py` 读取答辩稿、同目录的 `notes.md` 与 `defense.log`、清单与论文源文件，不写文件。
- `--log` 缺省时使用答辩稿目录中的 `defense.log`。该文件不存在时，D-COMPILE、D-OVERFLOW-V 与 D-OVERFLOW-H 记入 `skipped`。
- 提供 `--plan` 时，章角色与阶段取自规划。未提供时，章角色按帧标记中的页角色推断。分钟数依次取 `--minutes`、规划 `meta.minutes`、40。
- 论文仓库不可读时，D-NUM-SRC 记入 `skipped`。章角色不能全部确定时，D-BUDGET 的内容帧数检查不执行，D-BUDGET 记入 `skipped`；讲稿秒数合计检查照常执行。

| 脚本                | 退出码                                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `check_deck.py`     | 0：没有 Critical 与 Major 结果；1：至少一条 Critical 或 Major 结果；2：答辩稿不存在，清单或规划无法读取，`--log` 指定的文件不存在，或 `--minutes` 不在 15–90 |
| `render_preview.py` | 0：成功；2：PDF 不存在或无法打开，或 `--dpi`、`--cols` 不是正整数；3：未安装 PyMuPDF                                                                         |

## 输出格式

文本模式每条结果一行，末行为汇总：

```text
% D-NUM-SRC (frame=c3-experiment-2, defense.tex:271) [Severity: Major] [Priority: P1]: [Script] Meaning-Check: NEEDS-LLM：数字 37.25 在论文全文中没有同形数字；回到论文原句核对
% 汇总：Critical 0，Major 1，Minor 0，Info 0；skipped：D-COMPILE、D-OVERFLOW-V、D-OVERFLOW-H
```

- `frame` 为帧标记中的 id。缺少帧标记的帧写 `#` 加帧序号，例如 `#17`。导言区字段、全稿统计与不能映射到帧的日志行写 `-`。
- 位置写「文件:行号」。讲稿中的结果写 `notes.md`，不能映射到答辩稿行的日志结果写 `defense.log`，PDF 缺失或过期写 `defense.pdf`。没有行号时写 `-`。
- 映射到帧的日志结果在消息末尾注明日志行号，例如「（defense.log:1234）」。
- NEEDS-LLM 结果在消息前加 `Meaning-Check: NEEDS-LLM：`。
- 结果按帧序排序，`frame=-` 的结果在最前；同一帧内按码名、文件与行号排序。

`--json` 输出以下结构。每条结果的 `source_kind` 固定为 `script`，`meaning_check` 为 `NEEDS-LLM` 或空字符串。

```json
{
  "deck": "defense.tex",
  "findings": [
    {
      "code": "D-NUM-SRC",
      "severity": "Major",
      "priority": "P1",
      "source_kind": "script",
      "frame": "c3-experiment-2",
      "line": 271,
      "file": "defense.tex",
      "message": "数字 37.25 在论文全文中没有同形数字；回到论文原句核对",
      "meaning_check": "NEEDS-LLM"
    }
  ],
  "summary": { "Critical": 0, "Major": 1, "Minor": 0, "Info": 0 },
  "skipped": ["D-COMPILE", "D-OVERFLOW-V", "D-OVERFLOW-H"]
}
```

## 严重度

| 严重度   | 优先级 | 处置                                             |
| -------- | ------ | ------------------------------------------------ |
| Critical | P0     | 学术事实错误或编译失败。交付前必须修复           |
| Major    | P1     | 交付前修复。确认为误报时，向用户说明理由         |
| Minor    | P2     | 建议修复。修复循环结束后仍存在时，交付时告知用户 |
| Info     | P3     | 提示信息，不需要修改答辩稿                       |

## 码表

本节的「可见字符」指帧内去掉注释、`DefenseSource` 环境、帧标题、图文件参数与环境参数，再删去命令名与花括号后剩余的字符，空白不计。「内容帧」指页角色不是 cover、toc、thanks、backup 的帧。

### 结构

| 码            | 含义                     | 判据                                                                                                                                                                                                                                                                           | 严重度     | 处置                                                                 |
| ------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- | -------------------------------------------------------------------- |
| D-MARKER      | 帧标记                   | 帧前一个非空行不是帧标记                                                                                                                                                                                                                                                       | Minor / P2 | 答辩稿由构建脚本生成。重新运行 `build_deck.py`，不手改 `defense.tex` |
| D-MARKER      | 帧标记                   | 标记的 role 不在页角色集合，layout 不在版式集合，chapter 不是整数或 `-`；或 id 与前面的帧重复                                                                                                                                                                                  | Major / P1 | 改规划中该帧的字段后重建                                             |
| D-COVERAGE    | 框架完整                 | 首帧（备用页除外）不是 cover，或末帧不是 thanks；绪论章缺 background、status、challenges、organization 之一；基础章缺 foundation；研究章缺 intro、problem、method、experiment、summary 之一；应用章缺 intro、architecture、application 之一；结论章缺 innovation、outlook 之一 | Major / P1 | 在规划中补齐缺少的页角色                                             |
| D-TOC         | 目录                     | 第二帧不是 `\DefenseTocFrame{0}`；第 2 章起某章缺少章前目录，章前目录的参数不等于章号，或章前目录不紧接在该章首帧之前                                                                                                                                                          | Major / P1 | 在规划中恢复该章的 toc 帧，放在该章首帧之前                          |
| D-CHAIN       | 问题、研究章与创新点对应 | challenges 帧的卡片数或 innovation 帧的卡片数不等于研究章 intro 帧数；研究章 intro 帧的小节条不是「研究内容 i：章题」，i 为该章在研究章中的序号                                                                                                                                | Major / P1 | 使问题卡片、研究章与创新点卡片一一对应；按研究章顺序改小节条         |
| D-PLACEHOLDER | 占位符                   | 答辩稿或讲稿含 `〔待填写〕`、`TODO`、`TBD` 或 `XXX`                                                                                                                                                                                                                            | Major / P1 | 在规划中填写该字段后重建                                             |

### 图

| 码            | 含义         | 判据                                                                                                                                                    | 严重度        | 处置                                                    |
| ------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------- |
| D-FIG-ALLOW   | 只用论文的图 | `\includegraphics` 或 `\DefenseFigure` 的文件不在清单 `figures` 的图片文件中（`files[].path`、`files[].resolved`、`subfigures[].file`），也不是校徽文件 | Critical / P0 | 换为清单中的图。不生成新图，不重绘数据图                |
| D-FIG-MISSING | 图文件存在   | 允许使用的图片按答辩稿目录、`\graphicspath` 与扩展名回退找不到文件                                                                                      | Major / P1    | 核对论文仓库中的图文件；图文件变动后重新提取清单        |
| D-FIG-NUMBER  | 图表编号     | 可见文本或讲稿中的「图 k-m」「表 k-m」不在清单编号中；或题注编号属于清单中的另一幅图                                                                    | Major / P1    | 编号沿用论文。改规划中的题注或讲稿                      |
| D-FIG-ASPECT  | 图的比例     | PNG 或 JPEG 位图的高宽比大于 1.6，且版式为 figure、figure-grid 或 equations-figure；或宽高比大于 3，且图在 figure-bullets 的左栏                        | Minor / P2    | 换用其他版式或图的位置，见 [版式目录](slide-layouts.md) |

### 源文本

| 码        | 含义         | 判据                                                                                                        | 严重度        | 处置                                                                                     |
| --------- | ------------ | ----------------------------------------------------------------------------------------------------------- | ------------- | ---------------------------------------------------------------------------------------- |
| D-EQ-SRC  | 公式逐字复制 | `DefenseSource` 内的数学环境去掉 `\label`、`\tag`、`\notag`、`\nonumber` 与全部空白后，不等于清单中任一公式 | Critical / P0 | 按清单公式重建。不改写符号，不合并或拆分公式                                             |
| D-EQ-SRC  | 公式逐字复制 | `DefenseSource` 外出现数学环境、`\[`、`\(`、`$$` 或未转义的 `$`                                             | Major / P1    | 规划的文字字段不写数学内容。需要公式时，用 equations-figure 版式引用清单公式             |
| D-TAB-SRC | 表体逐字复制 | `DefenseSource` 内的表格环境去掉全部空白后，不等于清单中任一表体 `tabular_source`                           | Critical / P0 | 按清单表体重建。不改单元格                                                               |
| D-TAB-SRC | 表体逐字复制 | `DefenseSource` 外出现表格环境                                                                              | Major / P1    | 表格只用 table 版式引用清单表                                                            |
| D-NUM-SRC | 数字出自论文 | 可见文本与讲稿「说什么」「要点」「过渡」「可能提问」中的数字在论文全文中没有同形数字；结果标 NEEDS-LLM      | Major / P1    | 按本文「NEEDS-LLM 复核」一节逐个核对                                                     |
| D-PAPER   | 「论文」框   | `\DefensePaperBox` 的文本去掉全部空白后，不等于清单成果列表中任一条目                                       | Critical / P0 | 著录文本逐字取自成果列表。不编造成果                                                     |
| D-PAPER   | 「论文」框   | 该成果在成果列表中对应的章不含本帧所在章                                                                    | Major / P1    | 换为本章对应的成果                                                                       |
| D-PAPER   | 「论文」框   | 研究章在成果列表中有对应成果，但该章小结页没有「论文」框                                                    | Minor / P2    | 在小结页加入对应成果                                                                     |
| D-META    | 封面字段     | 封面字段（题目、作者、导师、学院、学科、日期）为空；或题目、作者与清单 `meta.title_zh`、`meta.author` 不同  | Major / P1    | 改规划 `meta` 的封面字段后重建                                                           |
| D-META    | 封面字段     | 清单 `meta.title_zh` 或 `meta.author` 为空，不能核对                                                        | Info / P3     | 人工核对封面题目与作者                                                                   |
| D-STAGE   | 答辩阶段     | 阶段不是 predefense 或 defense；与规划 `meta.stage` 不同；或 defense 阶段没有 achievements 帧               | Major / P1    | 答辩稿与规划不一致时，用该规划重建；需要改阶段时，用 `plan_deck.py --stage` 重新生成规划 |
| D-STAGE   | 答辩阶段     | predefense 阶段含 achievements 帧                                                                           | Minor / P2    | 删除规划中的 achievements 帧，或改用 defense 阶段                                        |

### 密度、时长与讲稿

| 码        | 含义     | 判据                                                                                          | 严重度     | 处置                                                                                         |
| --------- | -------- | --------------------------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------- |
| D-DENSITY | 页面密度 | 内容帧可见字符超过 260 个                                                                     | Major / P1 | 按 [内容规范](content-rules.md) 的溢出处置顺序处理                                           |
| D-DENSITY | 页面密度 | 内容帧可见字符为 181–260 个；要点、卡片、展望条目、子图或公式数超过版式上限；结论句超过 40 字 | Minor / P2 | 同上。版式上限见 [版式目录](slide-layouts.md)                                                |
| D-BUDGET  | 页数预算 | 内容帧数不在时长预算的页数区间内                                                              | Major / P1 | 按 [时长预算](time-budget.md) 增删内容帧；时长改变时用 `plan_deck.py --minutes` 重新生成规划 |
| D-BUDGET  | 页数预算 | 讲稿各节（备用页除外）「时长」合计与 60 × 分钟数相差超过 10%                                  | Minor / P2 | 调整规划中各帧的 `notes.seconds`                                                             |
| D-NOTES   | 讲稿     | 答辩稿目录中没有 `notes.md`                                                                   | Major / P1 | 重新运行 `build_deck.py`                                                                     |
| D-NOTES   | 讲稿     | 某帧没有讲稿节，或讲稿节缺少五栏之一；内容帧的「说什么」不在 150–250 字                       | Minor / P2 | 补写规划中该帧的 `notes` 字段                                                                |

### 编译

| 码           | 含义     | 判据                                                                                                                                 | 严重度        | 处置                                                                     |
| ------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------- | ------------------------------------------------------------------------ |
| D-COMPILE    | 编译     | 日志含错误行（以 `! ` 开头，或以「文件:行号:」开头）、`Emergency stop` 或 `Fatal error`；或 `defense.pdf` 不存在或早于 `defense.tex` | Critical / P0 | 按日志行定位原因。常见原因见 [清单与规划字段](plan-schema.md) 的已知限制 |
| D-COMPILE    | 编译     | 日志含未定义的交叉引用或文献引用（`Reference … undefined`、`Citation … undefined`）                                                  | Major / P1    | 核对该标签是否在清单中；重建后重新编译                                   |
| D-OVERFLOW-V | 纵向溢出 | 日志含 `Overfull \vbox`                                                                                                              | Major / P1    | 按 [内容规范](content-rules.md) 的溢出处置顺序处理                       |
| D-OVERFLOW-H | 横向溢出 | 日志含 `Overfull \hbox`，超出量大于 20pt                                                                                             | Major / P1    | 同上                                                                     |
| D-OVERFLOW-H | 横向溢出 | 超出量大于 5pt、不大于 20pt。不大于 5pt 时不报告                                                                                     | Minor / P2    | 同上                                                                     |

日志结果按以下行号映射到帧：错误行的 `l.` 行号或「文件:行号」、`detected at line` 与 `at lines` 后的行号、未定义引用的 `on input line` 行号。行号不在任何帧内时，结果写 `frame=-`。

D-NUM-SRC 的排除项与匹配规则：

- 不比较结构编号：「图、表、式」后的带分隔符编号，「第 k 章」，「研究内容 k」，「k 节」，小节条开头的节号，以及不大于 10 的整数。
- 年份不排除，必须在论文中出现。
- 数字按最长的「数字.数字」串切分，全角数字转为半角，去掉数字间的千位逗号后比较。小数位不同（例如 12.3 与 12.30）按不匹配报告，由复核决定。

## 阈值

| 阈值                     | 值        | 码           |
| ------------------------ | --------- | ------------ |
| 内容帧可见字符（Minor）  | 180       | D-DENSITY    |
| 内容帧可见字符（Major）  | 260       | D-DENSITY    |
| 结论句字数               | 40        | D-DENSITY    |
| 内容帧「说什么」字数     | 150–250   | D-NOTES      |
| 讲稿秒数合计的容差       | ±10%      | D-BUDGET     |
| 横向溢出（Minor、Major） | 5pt、20pt | D-OVERFLOW-H |
| 位图高宽比               | 1.6       | D-FIG-ASPECT |
| 位图宽高比               | 3         | D-FIG-ASPECT |

以上阈值为初始值，未标定。180 字、260 字与 150–250 字的区间没有经过答辩稿语料标定。不按单篇论文调整阈值。版式上限取自 [版式目录](slide-layouts.md)。

## 修复循环

1. 运行 `check_deck.py`。
2. 按码修改 `slide_plan.yaml`，不直接改 `defense.tex`。
3. 用 `build_deck.py --force --compile` 重建答辩稿。
4. 再次运行 `check_deck.py`。

最多 3 轮。第 3 轮后仍有 Critical 或 Major 结果时，列出剩余结果，交用户决定。

- D-DENSITY、D-OVERFLOW-V 与 D-OVERFLOW-H 按 [内容规范](content-rules.md) 的溢出处置顺序处理：删减文字、拆为两页、换用其他版式、缩小图宽。
- D-FIG-ALLOW、D-EQ-SRC、D-TAB-SRC、D-PAPER 与 D-NUM-SRC 只能改为清单与论文原文中的内容。不改写数字、公式、表体或成果条目。

## NEEDS-LLM 复核

D-NUM-SRC 只比较数字的字形，不判断数字的含义。对每条结果执行以下步骤：

1. 在论文中找出该数字所在的原句。
2. 核对数字、单位与对照基准与原句是否一致。
3. 该数字由换算、取整或重新计算得到时，改为论文原文中的数字。
4. 论文用其他写法表示同一数值时（例如 12.30 与 12.3），改为论文原文的写法。
5. 不能判断时，列出该数字与原句，交用户决定。

脚本不报告在论文中出现过的数字。同一数字在论文中表示其他量时，脚本不能发现。交付前，按页序把全部数字与论文原句核对一遍。

## 预览与目视检查

`render_preview.py` 需要 PyMuPDF。未安装时，脚本输出「缺少 PyMuPDF：运行 `uv pip install pymupdf` 后重试」并退出 3。

- 逐页图从 `page-001.png` 开始编号，分辨率由 `--dpi` 指定，默认 110。写入前删除输出目录中旧的 `page-NNN.png`，不删除其他文件。
- 总览图为 `contact-sheet.png`：每页缩略图宽 480 像素，共 `--cols` 列（默认 4），缩略图下方写页码，背景为白色。

逐页核对以下项目：

1. 帧标题与页码的位置与模板一致。
2. 图清晰，没有模糊或拉伸。
3. 每页的强调色（红色粗体）不超过 3 处。
4. 页脚没有遮挡正文或图。
5. 章前目录高亮当前章。

## 已知限制

- 溢出行号按 `defense.tex` 解释。宏包或 `thesis-macros.tex` 中产生的溢出可能映射到错误的帧。
- D-FIG-ASPECT 只读取 PNG 与 JPEG 位图。PDF 与 EPS 图、不可读的图文件不判定。
- `DefenseSource` 内的图片调用不参与 D-FIG-ALLOW。公式与表体由 D-EQ-SRC 与 D-TAB-SRC 与清单逐字比较。
- 帧切分按 `\begin{frame}` 与 `\end{frame}` 所在行进行。一行内有多个帧时不能正确切分。
- 缺少帧标记的帧按帧序号匹配讲稿节。
- 可见字符计数不展开宏定义：删去宏名，保留参数文字。
