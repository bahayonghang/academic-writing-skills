# academic-defense-beamer 答辩稿契约

## 1. Scope / Trigger

修改 `academic-writing-skills/academic-defense-beamer/` 的脚本（extract、plan、build、check、preview）、Jinja2 帧模板、
Beamer 主题与版式宏、Typst Touying 后端（`typst_backend.py`、`check_typst.py`、`templates/typst/`）、D-* 判据、清单或规划字段，以及对应公开资源时适用。
五个脚本通过清单 JSON、规划 YAML、帧标记与结果行串成一条流水线；任一环节改名或改格式，下游会静默失配。
详细字段以技能内 `references/plan-schema.md`、`references/quality-gate.md` 与 `references/touying-backend.md` 为准，本文件只锁跨脚本的接口。
后端只在 build（渲染、编译）与 check（源文件解析、编译日志、溢出、备注版）分叉；extract、plan 的帧序列、讲稿与预算、preview 与后端无关。

## 2. Signatures

```text
extract_thesis.py --thesis DIR [--main FILE] --out inventory.json [--json]
plan_deck.py --inventory inventory.json --out slide_plan.yaml [--minutes 40] [--stage predefense|defense] [--theme yanshan|generic] [--backend beamer|touying]
plan_deck.py --plan slide_plan.yaml --outline
build_deck.py --plan slide_plan.yaml --inventory inventory.json --out DIR [--logo PATH] [--force] [--compile] [--no-notes-pdf]
              [--typst-package SPEC] [--typst-package-path DIR] [--font-path DIR]
check_deck.py --deck DIR/defense.tex|DIR/defense.typ --inventory inventory.json [--plan slide_plan.yaml] [--log DIR/defense.log] [--notes-pdf DIR/defense-notes.pdf] [--minutes 40] [--json]
render_preview.py --pdf DIR/defense.pdf --out DIR/preview [--dpi 110] [--cols 4]
```

所有命令写作 `uv run python -B $SKILL_DIR/scripts/<name>.py …`；stdout/stderr 在 `__main__` 中重设为 UTF-8。

| 脚本 | 退出码 |
| --- | --- |
| extract | 0 成功；2 主文件缺失或多个非盲审候选且无 `--main` |
| plan | 0；2 参数或输入错误（`--minutes` 范围 15–90；`--backend touying` 配 `yanshan` 以外主题） |
| build | 0；2 规划校验失败（含 `longtable`/`xltabular` 表体；Touying：主题非 yanshan、包规格非法、EPS 或不支持格式、图片文件缺失、复杂表、不能翻译的宏）；4 自有文件已存在且无 `--force`；5 投屏版或备注版编译失败或超时，或无 latexmk（Touying：无 typst 或低于 0.15.1）；6 Touying 所需 Typst 包未安装 |
| check | 0 无 Critical/Major；1 有；2 输入错误（含 `--notes-pdf` 文件不存在、`--deck` 后缀非 `.tex`/`.typ`、后缀与 manifest `backend` 不符） |
| preview | 0；2 输入错误；3 缺 PyMuPDF（提示 `uv pip install pymupdf`） |

## 3. Contracts

- 后端：唯一来源是规划 `deck.backend`（`beamer` | `touying`）。`plan_deck.py` 对两个后端都写该键；缺键或空值的旧规划按 Beamer 构建。`build_deck.py` 没有 `--backend`；`check_deck.py` 按 `--deck` 后缀选后端。`--typst-package*`、`--font-path` 只对 Touying 生效，Beamer 收到时提示、不报错。
- 帧标记：`build_deck.py` 在每个 `\begin{frame}` 前一行写
  `% defense-frame: id=<id> role=<role> chapter=<n|-> layout=<layout>`；`\begin{frame}` 计数等于 PDF 页数。
  `check_deck.py` 以标记映射行号、页角色与页序；缺标记时回退帧序号并报 D-MARKER。
- 帧 id：`cover`、`toc`、`c<k>-toc`、`c<k>-<role>[-<i>]`、`thanks`；全稿唯一。
- 页序：封面 → 总目录（`\DefenseTocFrame{0}`）→ 第 1 章 → 第 k 章前目录（k ≥ 2）与各页 → 致谢；备用页在致谢之后，不计页数与预算。
  defense 阶段在展望页后加 `achievements`。
- 文字字段是普通文本，渲染时逐字转义；唯一标记是 `**关键词**`（`\DefenseHighlight`）。
- 公式：清单 `tex` 的 `\label{x}` 变为 `\tag*{(编号)}`，其余字符不变，放在 `DefenseSource` 中；
  D-EQ-SRC 去掉 `\label`/`\tag`/`\notag`/`\nonumber` 与空白后与清单逐字比较。
- 表体：`tabular_source` 原文放在 `DefenseSource` 与 `\adjustbox` 中；D-TAB-SRC 去掉空白后逐字比较。
- 模板只调用主题宏 API（`\Defense*` 与 `DefenseSource`），`templates/jinja/` 中不定义宏。唯一例外是 `defense-notes.tex.j2`
  的构建开关 `\def\DefenseNotesPDF{}`：它不是版式宏，只让 `deck.tex.j2` 导言区启用 second-screen 备注与页标签语句。
- 演讲备注：每帧在 `\end{frame}` 前恰有一个 `\DefenseNote{要点}{说什么}{过渡}{秒数}`（`frames/_note.tex.j2`），宏定义在
  `defense-layouts.sty`。文字按普通字段转义，`**关键词**` 变为 `\textbf`（不着色）；空栏为空串；可能提问不进入 PDF。
  `\note` 必须在帧内：帧外 `\note` 会生成独立备注页，破坏「帧数 = PDF 页数」。
- 备注版：`defense-notes.tex` 定义 `\DefenseNotesPDF` 后 `\input{defense.tex}`；导言区据此启用
  `show notes on second screen=right`，并以 `\special{pdf:put @catalog <</PageLabels<</Nums[0<</S/D>>]>>>>}` 覆盖页标签。
  不覆盖时 hyperref 为每个逻辑页（幻灯片与备注）各写一条标签，物理页标签变成 `1,1,2,2,…`，FerroStage 会把相邻两帧并成一组；
  `\hypersetup{pdfpagelabels=false}` 不能阻止这些记录。备注版页数 = 投屏版页数，16:9 下 W/H ≈ 3.56。
- 帧模板中，`\begin{frame}{<title>}` 之后不得直接跟花括号组：Beamer 把它当作帧副标题吞掉。分组一律用 `\begingroup … \endgroup`。
- 自有文件八个：`defense.tex`、`defense-notes.tex`、`thesis-macros.tex`、`notes.md`、`build_manifest.json`、两个主题 `.sty` 与
  `defense-layouts.sty`。`build_manifest.json` 含 `backend: "beamer"` 与 `notes_pdf`（`defense-notes.pdf`，`--no-notes-pdf` 时为 `null`）。
  `--force` 只覆盖自有文件；内容未变的自有文件不重写，保留 mtime（latexmk 按内容哈希决定是否重编，
  重写同内容的 `defense.tex` 会让 PDF 早于答辩稿而误报 D-COMPILE）。
- Touying 后端（细节见技能内 `references/touying-backend.md`）：
  - 包：默认 `@preview/simply-ysu-touying:0.2.0`，固定 `@preview/touying:0.8.0`、`@preview/mitex:0.2.6`，Typst ≥ 0.15.1。`--compile` 先按 `--typst-package-path` > `TYPST_PACKAGE_PATH` > `<data>/typst/packages`，`@preview` 再查 `TYPST_PACKAGE_CACHE_PATH` > `<cache>/typst/packages` 找 `typst.toml`；任一缺失退出 6，且不调用 `typst compile`（不触发下载）。
  - 帧标记 `// defense-frame: id=… role=… chapter=… layout=…`，字段同 Beamer；每章一个一级标题 `=`，第 1 章、首帧不是章前目录的章与无帧章写 `<touying:skip>`。
  - 文字字段一律为 Typst 字符串字面量（只转义 `\` 与 `"`，空白合并），`**词**` → `#hl("词")`；规划文本不得进入标记模式。题注与表格单元格由 `latex_inline` 转换：`~` → U+00A0，空白合并只作用于 ASCII 空白（Python `\s` 会吞掉 NBSP）；D-TAB-SRC 两侧都经 `compact` 去空白，NBSP 不造成误报。
  - 论文原文（题注、公式、表格）写在 `// defense-source-begin` 与 `// defense-source-end` 之间；源区外的数学或表格为 Major。公式去 `\label` 后原样交给 `mitex`；宏按用到的数学递归选取并翻译为 `\newcommand`（`\def` 无参、`\DeclareMathOperator(*)`），带参 `\def` 等不能翻译时 plan 提示、build 退出 2。表格只支持简单 `tabular`/`tabular*`/`tabularx`。
  - 自有文件：`defense.typ`、`notes.md`、`build_manifest.json` 与 `img/`（规划引用的论文原图逐字节副本）；manifest 含 `backend: "touying"`、`notes_pdf`、`typst_package`、`typst_version`、`copied_images`。`--force` 只删除上次 `copied_images` 中本次不再引用的图；内容未变的文件不重写。`defense.log` 在每次 `--compile` 开始时清空，再追加两次 stderr。
  - `meta.chapters[].nav_label`：页脚短名，plan 预填（≤ 6 字用章题，否则「第k章」并给 hint），build 缺省时同规则补；Beamer 忽略。
  - 备注：每帧恰一段，内容页 `#note[…]`，封面/总目录/致谢用 `note:` 参数，章扉页写在 `= 章名` 之后。备注版 `--input notes=on`：内容页标签 `N`、备注页 `notes:N`，备注页同宽、高 = 宽 × 13.5/16；投屏版不写 `/PageLabels`。PyMuPDF 2.0 `get_label()` 误读 Typst 标签，Touying 分支自行解析 catalog `/PageLabels` 的 `/Nums`。
  - D-OVERFLOW-V：主题溢出时自动续页。读 `<ysu-note>` 记录（`typst eval 'query(<ysu-note>).map(it => it.value)'`，失败再用已弃用的 `typst query`；只在答辩稿导入的包与 `touying:0.8.0` 都已在本机时运行，避免触发下载），帧页数 = 下一帧 `page` − 本帧 `page`（末帧用投屏版总页数 + 1，需 PyMuPDF）；读不到记录时退化为总页数 > 帧数、不定位；都不可行记 `skipped`。D-OVERFLOW-H 恒记 `skipped`。D-NOTES-PDF：备注页数 = 帧数、末页为备注页、`notes:` 配对、尺寸；总页数 2 × 帧数只在无溢出时成立，差值归 D-OVERFLOW-V。
- 只读：extract 与 check 不写论文仓库、答辩稿、清单与规划；preview 只写 `--out` 下的 `page-NNN.png` 与 `contact-sheet.png`。
- D-* 码集合固定为 22 个：D-MARKER、D-COVERAGE、D-TOC、D-CHAIN、D-PLACEHOLDER、D-FIG-ALLOW、D-FIG-MISSING、D-FIG-NUMBER、
  D-FIG-ASPECT、D-EQ-SRC、D-TAB-SRC、D-NUM-SRC、D-PAPER、D-META、D-STAGE、D-DENSITY、D-BUDGET、D-NOTES、D-COMPILE、
  D-OVERFLOW-V、D-OVERFLOW-H、D-NOTES-PDF（最后运行，`skipped` 中排在日志三码之后）。
  `\DefenseNote` 的四个参数是隐藏参数：不计可见字符，不参与答辩稿侧的 D-NUM-SRC / D-FIG-NUMBER（讲稿侧由 `notes.md` 覆盖）；
  D-PLACEHOLDER 的答辩稿扫描跳过 `\DefenseNote` 行。D-NOTES-PDF 用惰性导入的 PyMuPDF 读页尺寸与页标签，
  `page.get_label()` 返回未解码的 `<FEFF…>` 十六进制串，必须按 UTF-16BE 解码后比较。结果行：
  `% D-CODE (frame=<id>, <file>:<行>) [Severity: …] [Priority: …]: [Script] message`；`--json` 含 `findings`、`summary`、`skipped`。

## 4. Validation & Error Matrix

| Condition | Required behavior |
| --- | --- |
| 正式版与盲审版主文件并存 | 选正式版并写 `W-MAIN` |
| 两个非盲审主文件且无 `--main` | extract 退出 2 |
| 规划字段类型错误（例如 `figures` 为字符串列表） | build 列出全部错误并退出 2，不抛异常 |
| 输出目录已有任一自有文件、无 `--force` | build 退出 4，不写任何文件 |
| 只改讲稿后 `--force --compile` | 重写 `defense.tex`（备注在其中）、`notes.md` 与 `build_manifest.json`，两份 PDF 都重编；check 不报 D-COMPILE |
| 不改规划再 `--force` | 不重写任何自有文件，保留 mtime |
| `figure-grid` 帧无小节条 | 子图网格仍显示（不被当作副标题） |
| 无编译日志 | D-COMPILE、D-OVERFLOW-V、D-OVERFLOW-H 记入 `skipped` |
| 未编译（无 `defense.pdf`）、manifest `notes_pdf: null`、缺 PyMuPDF | D-NOTES-PDF 记入 `skipped` |
| 已编译投屏版但缺 `defense-notes.pdf` | D-NOTES-PDF Minor |
| 备注版比例出带、尺寸不一、页数不等、无法读取 | D-NOTES-PDF Major；相邻页标签相同为 Minor，帧数等于页数时定位到后一页的帧 |
| 帧内 `\DefenseNote` 不是恰好 1 次 | D-NOTES Minor |
| 缺 `notes.md` | D-NOTES Major |
| 清单外图片、论文外数字、改写公式 | 分别报 D-FIG-ALLOW、D-NUM-SRC（NEEDS-LLM）、D-EQ-SRC |
| 旧规划无 `deck.backend` | 按 Beamer 构建，产物与 Beamer 规划相同 |
| `deck.backend: touying` 且主题非 yanshan | plan 与 build 均退出 2 |
| Touying：EPS 图、复杂表、带参 `\def` | plan 写 hint；build 列出全部并退出 2 |
| Touying：规划引用的论文图片文件不存在 | build 退出 2（须复制到 `img/`）；Beamer 此时只由 check 报 D-FIG-MISSING。Touying 的 D-FIG-MISSING 只在构建后 `img/` 副本被删改时出现 |
| Touying：Typst 包缺失 | build 已写出自有文件，`--compile` 退出 6，不调用 typst |
| Touying：帧内容溢出续页 | D-OVERFLOW-V Major，定位到帧标记；D-NOTES-PDF 不因总页数重复报 |
| `--deck defense.typ` 但 manifest `backend: beamer`（或反之） | check 退出 2 |
| Touying：题注或单元格含 `~` | `defense.typ` 中为 U+00A0；D-TAB-SRC 无结果 |

## 5. Good / Base / Bad Cases

- Good：修改一个 D-* 判据时，同时改 `check_deck.py`、`references/quality-gate.md`（含双语资源页与 manifest 散列）与该码的正反例测试。
- Base：规划不变时重建，全部自有文件字节与 mtime 不变，latexmk 不重编，check 零结果；只改讲稿时 `defense.tex` 随备注重写，两份 PDF 重编。
- Bad：在帧模板里写 `{\centering …}` 紧跟帧标题；在文字字段里写 `$…$` 期望渲染数学；为消除 D-NUM-SRC 把数字换成另一个自算的数字。

## 6. Tests Required

- `tests/skills/academic_defense_beamer/`：`test_defense_theme_assets.py`（主题常量、宏 API、演示稿编译）、`test_defense_budget.py`、
  `test_defense_extract.py`、`test_defense_plan.py`、`test_defense_build.py`（帧标记序列、转义、公式与表体还原、`--force`、
  帧标题后无花括号组、未变文件保留 mtime、每帧一个 `\DefenseNote`、备注转义、`--no-notes-pdf`）、
  `test_defense_check.py`（22 码正反例与输出契约；D-NOTES-PDF 用 PyMuPDF 合成 PDF 覆盖比例、页数、重复标签、缺文件，
  另有 manifest 关闭与缺 PyMuPDF 两个 skip 用例）、`test_defense_preview.py`。
- 编译用例只在 `DEFENSE_COMPILE=1` 且有 xelatex/latexmk 时运行，并断言备注版 54 页、W/H 3.56、页标签 `1…54`；
  预览与 D-NOTES-PDF 用例在无 PyMuPDF 时 skip（项目依赖不含 PyMuPDF，验证时用 `uv run --with pymupdf pytest …`）。
  `conftest.py` 在收集阶段预导入 PyMuPDF：它在首次导入时绑定 `sys.stdout`，若首次导入发生在 `capsys` 测试内，后续用例会写入已关闭的流。
- Touying：`test_defense_typst_backend.py`（转义、`hl` 拆分、`latex_inline` 含 NBSP、表格网格与复杂表、宏翻译、图片格式、包查找与退出 6，不需要 Typst）、`test_defense_build_typst.py`（帧标记与每帧一段备注、注入用例、图片复制与 `--force`、旧规划按 Beamer、非 yanshan、复杂表/EPS/带参 `\def` 退出 2、缺包退出 6、编译）、`test_defense_check_typst.py`（各码正反例、源区、后缀与 manifest 不符、溢出定位与退化、页标签解析、D-NOTES-PDF、`~` 不误报）、`test_defense_plan.py` 的 `--backend` 与 `nav_label` 用例。Typst 编译用例只在 `DEFENSE_TYPST_COMPILE=1` 且 typst 与三个包已在本机时运行（另需 PyMuPDF：`uv run --with pymupdf pytest …`）。
- 契约测试：`tests/contracts/test_skill_contracts.py`（路由命令参数出现在 `--help`、命令卫生、`allowed-tools`）、
  `test_skill_versions.py`、`test_skills_install.py`、`test_trigger_evals.py`、`test_docs_bilingual_resources.py`。

## 7. Wrong vs Correct

```python
# Wrong: Python's \s also matches U+00A0, so the no-break space from ``~`` turns back into a space.
value = re.sub(r"\s+", " ", value)

# Correct: collapse ASCII whitespace only.
value = re.sub(r"[ \t\n\r\f\v]+", " ", value)
```

```latex
% Wrong: without a subsection bar, Beamer reads this group as the frame subtitle.
\begin{frame}{3.4 实验与结果分析}
{\centering
\begin{minipage}[t]{0.3\linewidth} … \end{minipage}\par}

% Correct
\begin{frame}{3.4 实验与结果分析}
\begingroup\centering
\begin{minipage}[t]{0.3\linewidth} … \end{minipage}\par\endgroup
```
