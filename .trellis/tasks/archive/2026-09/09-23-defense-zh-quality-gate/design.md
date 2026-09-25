# C3 设计

## 1. Files

技能根 `S = academic-writing-skills/latex-defense-zh`。本子任务新增：

- `S/scripts/check_deck.py`、`S/scripts/render_preview.py`
- `S/references/quality-gate.md`
- `tests/skills/latex_defense_zh/test_defense_check.py`、`test_defense_preview.py`
- docs 资源同步（父 design §7）：`docs/skills/latex-defense-zh/resources/references/quality-gate.md`、
  `docs/zh/skills/latex-defense-zh/resources/references/quality-gate.md`、`docs/resource-manifest.json`（脚本重建）

只读使用 C2 的 `scripts/tex_loader.py`、`scripts/defense_budget.py` 与 `tests/skills/latex_defense_zh/conftest.py`。

## 2. check_deck.py 输入与解析

- 必需：`--deck <DIR>/defense.tex`、`--inventory inventory.json`。可选：`--plan`、`--log`（缺省时若 `<DIR>/defense.log`
  存在则使用）、`--minutes`（缺省取规划 `meta.minutes`，再缺省 40）、`--json`。`<DIR>/notes.md` 存在时读取。
  必需文件缺失或清单 JSON 无法解析 → 退出 2。
- 帧切分：按 `\begin{frame}` 与配对 `\end{frame}` 切分，记录起止行；帧前一行的帧标记给出 id、role、chapter、layout。
- 可见文本：帧内去掉注释行、`DefenseSource` 环境、`\DefenseFigure` 的文件参数与 `\begin{frame}` 标题参数后，
  展开 `\DefenseHighlight{x}` 等宏为参数文本，去掉其余控制序列与花括号，得到可见文本；按字符计数（空白不计）。
- 论文全文：用清单 `thesis_root` 与 `main_tex` 经 `tex_loader.assemble` 组装，去注释；全角数字转半角，去掉数字间的千位逗号。
  论文仓库不可读时，D-NUM-SRC 记入 `skipped`。
- 输出按帧序、再按码名排序。文本模式末行输出各严重度计数与 `skipped` 列表。

## 3. D-* 码表

| 码 | 判据 | 严重度 / 优先级 | 需要的输入 |
| --- | --- | --- | --- |
| D-COMPILE | log 含 `! ` 开头的错误行、`Emergency stop` 或 `Fatal error`；或 `defense.pdf` 不存在或早于 `defense.tex` | Critical / P0 | log |
| D-COMPILE | log 含 `Reference … undefined` 或 `Citation … undefined` | Major / P1 | log |
| D-OVERFLOW-V | log `Overfull \vbox`，按 `detected at line N` 映射到帧 | Major / P1 | log |
| D-OVERFLOW-H | log `Overfull \hbox (Xpt too wide)`：X > 20 | Major / P1 | log |
| D-OVERFLOW-H | 5 < X ≤ 20；X ≤ 5 不报 | Minor / P2 | log |
| D-FIG-ALLOW | `\includegraphics` 或 `\DefenseFigure` 的文件参数不在清单 `files[].path` ∪ `subfigures[].file`（校徽参数除外） | Critical / P0 | — |
| D-FIG-MISSING | 允许的文件按答辩稿 `\graphicspath` 与扩展名回退解析不到 | Major / P1 | — |
| D-FIG-NUMBER | 可见文本、题注或讲稿中的「图/表 k-m」不在清单编号内；或题注编号与所用文件所属图的编号不同 | Major / P1 | — |
| D-FIG-ASPECT | 位图高宽比 > 1.6 且版式为 figure、figure-grid、equations-figure；或宽高比 > 3 且为 figure-bullets 左图 | Minor / P2 | 图文件 |
| D-NUM-SRC | 可见文本与讲稿中的阿拉伯数字（含小数、百分数）在论文全文中无同形数字；标 NEEDS-LLM | Major / P1 | 论文仓库 |
| D-EQ-SRC | `DefenseSource` 内的数学环境规范化后不等于任一清单公式 | Critical / P0 | — |
| D-EQ-SRC | `DefenseSource` 外出现行间数学环境、`\[`、`$$` 或未转义的 `$` | Major / P1 | — |
| D-TAB-SRC | `DefenseSource` 内的表格环境规范化后不等于任一清单 `tabular_source` | Critical / P0 | — |
| D-TAB-SRC | `DefenseSource` 外出现表格环境 | Major / P1 | — |
| D-PLACEHOLDER | 答辩稿或讲稿含 `〔待填写〕`、`TODO`、`TBD`、`XXX` | Major / P1 | — |
| D-TOC | 第二帧不是 `\DefenseTocFrame{0}`；k = 2..n 章缺少章前目录、位置不在该章首帧前、或参数不等于 k | Major / P1 | — |
| D-CHAIN | challenges 卡片数、research intro 帧数、innovation 卡片数三者不等；「研究内容 i」不是按章序 1..R | Major / P1 | — |
| D-COVERAGE | 首帧非 cover、末帧非 thanks；intro 章缺 background/status/challenges/organization；研究章缺 intro/problem/method/experiment/summary；应用章缺 intro/architecture/application；结论章缺 innovation/outlook | Major / P1 | — |
| D-DENSITY | 内容帧可见字符 > 260 | Major / P1 | — |
| D-DENSITY | 可见字符 181–260；要点条数超过 C1 版式上限；takeaway 超过 40 字 | Minor / P2 | — |
| D-BUDGET | 内容帧数不在 `defense_budget` 区间 | Major / P1 | — |
| D-BUDGET | 讲稿秒数合计不在 60M 的 ±10% 内 | Minor / P2 | notes |
| D-NOTES | 缺少 `notes.md` | Major / P1 | — |
| D-NOTES | 某帧缺讲稿节或五栏之一；内容帧「说什么」不在 150–250 字 | Minor / P2 | notes |
| D-META | 封面字段（题目、作者、导师、学校、学科、日期）为空；题目或作者与清单不一致 | Major / P1 | — |
| D-META | 清单对应字段为空，无法比较 | Info / P3 | — |
| D-STAGE | `stage` 不是 predefense/defense；与规划 `meta.stage` 不同；defense 缺 achievements 帧 | Major / P1 | 规划（比较时） |
| D-STAGE | predefense 含 achievements 帧 | Minor / P2 | — |
| D-PAPER | `\DefensePaperBox` 文本规范化后不等于任一清单成果 | Critical / P0 | — |
| D-PAPER | 成果对应章不含该帧所在章 | Major / P1 | — |
| D-PAPER | 研究章有对应成果但 summary 帧无论文框 | Minor / P2 | — |
| D-MARKER | 帧标记缺失 | Minor / P2 | — |
| D-MARKER | 帧标记 role 或 layout 不在允许集合；id 重复 | Major / P1 | — |

判据细节：

- 公式规范化：去掉 `\label{…}`、`\tag{…}`、`\tag*{…}`、`\notag`、`\nonumber` 与全部空白。表格规范化：去掉全部空白。
- D-NUM-SRC 排除项：「图/表/式」编号、「第 k 章」、「研究内容 k」、节号前缀、≤ 10 的整数。年份不排除，必须在论文中出现。
  匹配要求前后不接数字或「.数字」。小数位不同（如 12.3 与 12.30）按不匹配报告，由复核决定。
- 全局性结果（D-COMPILE、log 行无法映射到帧的溢出）写 `frame=-`。图文件不可读时该文件的 D-FIG-ASPECT 不判定。
- D-CHAIN 与 D-COVERAGE 的章角色：有 `--plan` 时取规划；否则按帧标记中出现的页角色推断。
- D-BUDGET 的章角色与阶段同上；分钟数按 §2 顺序取值。
- 帧数统计口径与 C1 time-budget 相同：内容帧不含 cover、toc、章前目录、thanks、backup。

## 4. 输出

文本行：`% <码> (frame=<id>, defense.tex:<行>) [Severity: <S>] [Priority: <P>]: [Script] <消息>`，
NEEDS-LLM 项在消息前加 `Meaning-Check: NEEDS-LLM：`（与 `latex-thesis-zh/scripts/analyze_experiment.py` 的写法一致）。
讲稿中的问题行写 `notes.md:<行>`。

`--json`：

```json
{
  "deck": "defense.tex",
  "findings": [
    {"code": "D-NUM-SRC", "severity": "Major", "priority": "P1", "source_kind": "script",
     "frame": "c3-experiment-2", "line": 412, "file": "defense.tex",
     "message": "…", "meaning_check": "NEEDS-LLM"}
  ],
  "summary": {"Critical": 0, "Major": 1, "Minor": 0, "Info": 0},
  "skipped": ["D-COMPILE", "D-OVERFLOW-V", "D-OVERFLOW-H"]
}
```

退出码：有 Critical 或 Major → 1；否则 0；输入错误 → 2。

## 5. render_preview.py

- 模块顶层 `try: import pymupdf` 失败时记为不可用（沿用 `paper-audit/scripts/visual_check.py:21` 的写法）；
  不可用 → stderr 输出「缺少 PyMuPDF：运行 `uv pip install pymupdf` 后重试」并退出 3。
- `--pdf` 不存在或不可打开 → 退出 2。`--out` 不存在时创建；先删除 `--out` 中匹配 `page-\d{3}\.png` 的旧文件，
  再按 `--dpi`（默认 110）输出 `page-001.png` 起的逐页图；不删除其他文件。
- 总览图 `contact-sheet.png`：Pillow 拼图，每格缩略图宽 480 像素，`--cols`（默认 4）列，格下写页码；背景白色。
- stdout 输出页数、输出目录与总览图路径。

## 6. references/quality-gate.md

码表（同 §3，面向用户改写为「含义 / 判据 / 严重度 / 处置」四列）；阈值来源说明：180/260 字与 150–250 字讲稿区间
是初始值、未经语料标定；修复循环：每轮只按码改规划（不直接改 `defense.tex`），重建后重跑 check，最多 3 轮，
仍有 Critical/Major 时列出并交用户决定；溢出处置顺序引用 C1 `content-rules.md`；NEEDS-LLM 复核：逐个数字回到论文原句核对；
预览目视清单：标题与页码位置、图是否清晰、强调色数量、页脚遮挡、目录高亮。

## 7. Tests

- 基线：`conftest.py` 的 `built_deck`；log 在 tmp_path 中合成（仓库 `.gitignore` 忽略 `*.log`，不入库）；
  编译用例外不依赖 xelatex。
- 每个码一个正例、一个反例：反例由基线 `defense.tex` 复制后做一处文本替换或删除得到（例如替换一个图文件名、改一个数字、
  改公式中一个符号、改表格一个单元格、删一个章前目录帧、删一张创新点卡片）。断言码、严重度、优先级与帧 id。
- 父 AC8 三个反例单列用例名 `test_parent_ac8_*`。
- 输出契约：文本行正则、`--json` 字段集合、退出码 0/1/2、`skipped` 内容。
- 只读：运行前后基线目录与清单 SHA-256 不变。
- preview：monkeypatch 使 `pymupdf` 不可用 → 退出 3；`pytest.importorskip("pymupdf")` 后用 PyMuPDF 生成三页合成 PDF，
  断言三张 `page-NNN.png`、旧 `page-009.png` 被删除、总览图存在且尺寸符合列数。
- 脚本加载与 CLI 子进程规则同 C2 design §8。
