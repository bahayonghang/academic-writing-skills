# 设计：Touying 后端

## 1. 模块划分

| 文件 | 职责 |
| --- | --- |
| `scripts/build_deck.py` | 入口不变；按 `deck.backend` 分派。共享：规划校验、讲稿 `notes.md`、manifest、自有文件写入与 `--force`。 |
| `scripts/typst_backend.py`（新） | Typst 字符串转义、`**…**` → `hl`、表格网格解析、图片复制清单、包预检、`typst compile` 调用 |
| `templates/typst/deck.typ.j2`、`templates/typst/frames/<layout>.typ.j2`（新） | Touying 帧模板；只调用 simply-ysu-touying 与 mitex 的公开 API，不定义函数 |
| `scripts/check_typst.py`（新） | 解析 `defense.typ`（标记、`image(...)`、`mitex(...)`、表格单元、备注）供 `check_deck.py` 调用 |
| `scripts/check_deck.py` | 按 `--deck` 后缀选解析器；码实现复用，Typst 专属分支调用 `check_typst.py` |

单入口保持 SKILL.md Module Router 不变，契约测试 `router_help` 继续有效。新模块用相对导入或 `sys.path` 插入方式，与现有脚本一致（实施时照 `build_deck.py` 导入 `defense_budget` 的方式）。

## 2. 版式映射

| 版式 | Touying 输出 |
| --- | --- |
| `cover` | `#title-slide(note: …)`；`config-info` 由规划 `meta` 填写；`stage` / `stage-en` 由阶段映射（预答辩 → 博士 / 硕士学位论文预答辩 · Pre-defense；正式答辩同理） |
| `toc` 总目录 | `#outline-slide(groups: ((from:, to:, tags:),), note: …)`：`research` 章连续段落成一组 |
| `toc` 章前目录 `c<k>-toc` | `= 章名` + `#chapter-opener(question: …, keywords: (…))` + `#note[…]`；question 取帧结论句，keywords 取帧要点（≤ 3 条），细节以 spike S3 结论为准 |
| `bullets` | `== 标题` + `#sub[小节]` + `#takeaway[结论句]` + `#points(…)` |
| `figure` | 同上 + `#figure-box(caption: …)[#image("img/…", width: …)]` |
| `figure-bullets` | `#slide(composer: (1fr, 1fr))[figure-box][points]`（以 Touying 0.8.0 实际 API 为准） |
| `figure-grid` | `#grid(columns: n, ..figure-box)` |
| `equations-figure` | `#eq-block(number: "(3-2)")[#mitex(`…`)]` + figure-box |
| `table` | `#result-table(header: (…), rows: ((…),), mark: …)` |
| `cards` | `#grid` of `#card(…)` / `#title-box(title: …)[…]` |
| `paper-summary` | `#paper-box[…]` |
| `outlook` | `#points(…)` 或 `#card` 列 |
| `thanks` | `#ending-slide(note: …)`；`recap` 取创新点（来自结论章），无则省略 |

- 帧标题 → `== 标题`；小节 → `#sub[]`；结论句 → `#takeaway[]`（Touying 中显示为页眉主标题，Beamer 中在页底，语义相同）。
- 页脚导航：`nav-labels` 必须显式传短名（S1：章全名会让页脚重叠折行）。来源为规划可选字段 `meta.chapters[].nav_label`（Beamer 忽略）；
  plan 阶段默认取 `short_title` / `title`，长度 ≤ 6 字时直接用，否则写 `第k章` 并给 hint 建议改成 ≤ 6 字的短名。
- 备用页：致谢之后，同样带标记与备注。

## 3. 文本安全

- 全部文字字段输出为字符串字面量：`"…"`，只转义 `\` → `\\`、`"` → `\"`；换行折成空格。
- `**关键词**` 拆分为 `[#"前"#hl("关键词")#"后"]`。
- 不允许规划文本进入 Typst 标记模式，因此 `#`、`$`、`*`、`_`、`@`、`<`、`` ` ``、`//`、`=` 均按原文显示；回归测试覆盖。
- mitex 输入用原始块 `` mitex(`…`) ``；源中含反引号时改用更长的反引号围栏，不改公式内容。

## 4. 图、公式、表

- 图：按清单解析出的论文绝对路径复制到 `<out>/img/<清单相对路径>`；支持 `.pdf .png .jpg .jpeg .svg`，`.eps` 在 plan 阶段 hint、build 阶段报错（退出 2，列出全部）。
  复制保留字节，不转换。`img/` 属自有目录，`--force` 才覆盖，且只删本次清单外的、由上次构建写入的文件（依据 manifest 的 `copied_images`）。
- 公式：`#import "@preview/mitex:<pinned>": mitex`；版本在实施 spike 中按本机缓存与 Typst 0.15.1 兼容性固定，写入 `references/touying-backend.md`。
  论文宏：spike S2 确认 mitex 对 `\newcommand` 的支持；支持则把清单 `macros` 前置；不支持则 plan hint + build 报错，建议用 Beamer 后端。
  `\label{x}` 去掉，编号由 `eq-block(number:)` 显示，与 Beamer 的 `\tag*` 规则对应。D-EQ-SRC 比较规则不变。
- 表：解析 `tabular_source` 为行列；允许 `\hline`、`\toprule`、`\midrule`、`\bottomrule`、`&`、`\\`、单元格内 `$…$`（交给 mitex 行内）；
  遇 `\multirow`、`\multicolumn`、`\makecell`、嵌套 tabular 即判为复杂表并报错。D-TAB-SRC 在 Typst 下比较单元格纯文本序列。

## 5. 包预检（不联网）

1. `shutil.which("typst")`，读 `typst --version`，低于 0.15.1 → 退出 5 并提示。
2. 对 `simply-ysu-touying`、`touying:0.8.0`、`mitex:<pinned>` 逐个查找 `typst.toml`：
   `--typst-package-path` > Typst 数据目录 `<data>/typst/packages/<ns>/<name>/<ver>/`（Windows `%APPDATA%`，Linux `$XDG_DATA_HOME` 或 `~/.local/share`，macOS `~/Library/Application Support`）
   > `@preview` 时再查缓存目录 `<cache>/typst/packages/preview/<name>/<ver>/`（Windows `%LOCALAPPDATA%`，Linux `$XDG_CACHE_HOME` 或 `~/.cache`，macOS `~/Library/Caches`）。
   同时尊重 `TYPST_PACKAGE_PATH` 与 `TYPST_PACKAGE_CACHE_PATH` 环境变量。
3. 任一缺失 → 退出 6，打印缺失的包与 `references/touying-backend.md` 中的安装步骤，不调用 `typst compile`（避免自动下载）。

## 6. 编译与产物

```text
typst compile --root <out> [--package-path P] [--font-path F] <out>/defense.typ <out>/defense.pdf
typst compile --root <out> [--package-path P] [--font-path F] --input notes=on <out>/defense.typ <out>/defense-notes.pdf
```

- stderr 追加写入 `<out>/defense.log`；失败退出 5 并指出哪一份。
- manifest：`backend: "touying"`、`notes_pdf`、`typst_package`、`typst_version`、`copied_images`。

## 7. 检查映射细节

- 见父 design.md 第 6 节。D-OVERFLOW-V 采用候选 B（S4 结论，第 10 节）：
  `typst query --root <out> defense.typ "<ysu-note>"` 取每帧的 `frame` 与起始 `page`；帧 i 的页数 = 下一帧 `page` − 本帧 `page`（末帧用投屏版总页数 + 1），
  页数 > 1 即报，定位到该帧的 `defense-frame` 标记，消息写出多出的页数。前提：构建不输出 `#pause`，且每帧都有备注（D-NOTES 保证）。
  无 Typst 可执行文件时退化为「`defense.pdf` 物理页数 > 帧数」，只报总数、不定位；两者都做不了时记入 `skipped`。
  候选 A 不可行：投屏版 PDF 不写 `/PageLabels`。
- D-NOTES-PDF（Touying）：备注页数 = 帧数；每个备注页标签 = `notes:` + 紧邻前一内容页的标签；末页是备注页；
  备注页宽 = 内容页宽，高 / 宽 ∈ 13.5/16 ± 1%。总页数 = 2 × 帧数只在无溢出时成立：溢出续页各占一个数字标签、只在最后续页后跟备注页，
  这种页数差归 D-OVERFLOW-V 报告，D-NOTES-PDF 不重复报。标签自行解析 catalog `/PageLabels` 的 `/Nums`（不用 PyMuPDF `get_label()`）。

## 8. Spike 清单（实施第一步，结论写回本文件）

- S1 本机按 `@local` 安装 touying-theme-ysu 0.2.0（Touying 0.8.0）并编译一页最小稿，
  另确认 0.8.0 迁移后 `notes: true` 的备注页尺寸与 `N` / `notes:N` 页标签仍成立（否则回父任务改 D-NOTES-PDF 判据），确认导入路径、字体回退与 `--root` 行为。
- S2 mitex：固定版本；测试 fixture 公式与带 `\newcommand` 的公式；记录支持边界。
- S3 `chapter-opener` 与 `outline-slide` 所需字段能否完全由现有规划字段填出；若需新增可选字段（如 `keywords`），更新 `plan-schema.md` 并保持 Beamer 忽略该字段。
- S4 Touying 页面溢出时的表现（自动分页？裁切？），确定 D-OVERFLOW-V 判据。
- S5 PDF 图在 Typst 0.15.1 下的渲染与体积；SVG 中文字体。

## 9. Spike 结论（2026-10-28，部分）

版本决定（用户 2026-10-28）：目标改为 `@preview/simply-ysu-touying:0.2.0` + `@preview/touying:0.8.0`，替代 1.0.0 + 0.6.3。
主题仓库的 0.8.0 迁移任务当时仍在规划，主题代码仍导入 `touying:0.6.3`，本机未装 `@local` 主题。
因此 S1、S3 与 S4 的主题部分**待主题 0.2.0 就绪后再做**；以下结论只用本机缓存的 `touying:0.8.0`（`compiler = "0.15.0"`）与 `mitex` 得到，Typst 0.15.1。

- **S2 mitex：通过，带宏翻译。** 固定 `@preview/mitex:0.2.6`（本机缓存最高版本）。fixture 7 个公式：
  - 不前置宏时 5 个失败（`\vect`、`\Loss`、`\argmin` 未知）。
  - mitex 支持源内 `\newcommand`（含参数），**不支持** `\def` 与 `\DeclareMathOperator(*)`。
  - 把清单宏按一一对应翻译后前置：`\def\X{…}`（无参数）→ `\newcommand{\X}{…}`；`\DeclareMathOperator*{\X}{t}` → `\newcommand{\X}{\operatorname*{t}}`（无星号同理）。
    翻译只改宏定义的写法，不改公式正文。7 个公式全部通过，`align` 原样或包进 `aligned` 都可，目视正确。
  - 源内 `\label`、`\tag`、`\left…\right`、反引号均可编译；实施时仍按第 4 节去掉 `\label`。
  - 带参数的 `\def`（`\def\X#1{…}`）与其他不支持的定义：plan hint + build 退出 2（不翻译）。
  - 原始块写成 ```` ```\n…\n``` ````（围栏后换行），否则 Typst 0.15 把首行当语言标签并告警。
- **S5 图：通过。** PDF 图作为矢量 XObject 嵌入，原字体保留（54 页的 Beamer PDF 只嵌第 1 页，输出 192 KB < 源 318 KB）；
  SVG 中文按 `font-family` 列表回退（本机落到 SimHei）；PNG 正常。EPS 仍不支持（Typst 不读 EPS）。
- **S4（仅 Touying 核心，simple 主题）：** 内容溢出时**自动续页**，不裁切（40 行要点续出 9 页，页脚计数 `4 / 12`）。
  若主题 0.2.0 行为相同，且构建不输出 `#pause`，则 D-OVERFLOW-V 判据可简化为「投屏版物理页数 > 帧数」，用 `defense-frame` 顺序定位溢出帧；
  主题就绪后用 `ysu-theme` 复测再定。
- **页标签读取（影响 D-NOTES-PDF）：** Typst 写出的 `/PageLabels` 数字树合法（每页 `<</Type /PageLabel /S /D /St n>>`），
  但 PyMuPDF 2.0 的 `page.get_label()` / `get_page_labels()` 把 `/Type /PageLabel` 误读成前缀，返回 `ageLabel1`。
  Touying 分支不得用 `get_label()`：在 `check_deck.py` 中自行读 catalog `/PageLabels` 的 `/Nums`（`/P` 前缀、`/S` 样式、`/St` 起始）组装标签。
  Beamer 分支（xdvipdfmx 输出）现有读法保持不变。
- **S3 字段映射：通过（按主题公开 API 读出，主题 0.2.0 任务承诺保持 1.0 API 契约）。** 不需要新增规划字段。
  - `config-info`：`title` ← `meta.title_lines` 拼接，`author`、`supervisor`（+ `supervisor_title`）、`subject`、`school`、`date` 一一对应；
    `stage` / `stage-en` 由 `meta.stage` 映射（第 2 节）。`title-slide(research-line:)` 可选，不传。
  - `outline-slide(groups:)`：每组只需 `from` / `to`（章序号），`tags` / `icons` 可选；`research` 章的连续段成组，不传 `icons`。
  - `chapter-opener`：`question`、`keywords`、`bridge` 全部可选。规划里章前目录帧（`c<k>-toc`）没有结论句与要点，
    因此默认输出无参的 `#chapter-opener()`；帧若有 `takeaway` 则作 `question`、有 `bullets` 则取前 3 条作 `keywords`。第 2 节表格据此放宽。
  - 待 S1 复测：`nav-labels: auto` 用章标题作页脚导航，fixture 章标题最长 24 字，可能挤出页脚；必要时由 `meta.chapters[].title`
    截断生成短名，或新增可选 `short_title`（届时按规则更新 `plan-schema.md`，Beamer 忽略）。

## 10. Spike 结论（2026-11-01，主题 0.2.0 就绪后补测）

环境：`@preview/simply-ysu-touying:0.2.0`（已上架 Typst Universe，导入 `@preview/touying:0.8.0`，`compiler = "0.15.0"`），Typst 0.15.1，PyMuPDF 2.0。
包规格默认 `@preview/simply-ysu-touying:0.2.0`；`@local` 安装法降为备选（离线或改主题时）写进 `references/touying-backend.md`。

- **S1 最小稿：通过。** 8 帧测试稿（封面、目录、2 个章扉页、3 个内容页、致谢）两份都编译成功。
  - 内容页 16 × 9 cm，备注页 16 × 13.5 cm；备注版页标签为 `N` / `notes:N` 交替，主题自带的 `check-page-labels.py --expect-notes` 在无溢出部分通过。
  - **投屏版 `defense.pdf` 不写 `/PageLabels`**，只有备注版有标签。
  - 同页多次 `#note[]` 按段落拼接；章扉页备注写在 `= 章名` 后生效；没写备注的帧也会有空备注页，配对不受影响。
  - `#takeaway("含 # $ ] // \" 的结论句")` 原样显示：字符串字面量方案确认可行。注意：markup 里不能直接写 `"…"`，模板必须写 `#takeaway("…")`、`#sub("…")` 这类函数调用形式。
  - PyMuPDF 2.0 的 `get_label()` 仍把内容页读成 `ageLabel1`（备注页 `notes:1` 读得对），沿用第 9 节自读 `/Nums` 的方案。
  - **页脚导航：** 2 章 × 24 字可以放下；6 章全名（16–24 字）时页脚重叠折行，作者 · 阶段栏被挤掉。6 个 ≤ 5 字的短名排得整齐。
    结论：必须显式传 `nav-labels`，新增可选规划字段 `meta.chapters[].nav_label`（第 2 节）。
- **S3 复测：通过。** `config-info` 新字段、`outline-slide()` 的分组、无参 `chapter-opener()` 及带 `question` / `keywords` 的版本都按第 9 节映射渲染正常。
- **S4 溢出（ysu-theme）：自动续页，不裁切**，与 Touying 核心一致。40 行要点续出 4 页。
  - 备注版里续页各占一个数字标签（`6, 7, 8, 9, notes:9`），备注页只跟在最后一个续页后面。
  - `typst query "<ysu-note>"` 的记录有 `frame`、`page`（帧起始页）、`kind`、`title`、`text`。溢出帧 6 的 `page = 6`，下一帧 `page = 10`，能精确算出多出 3 页。
  - 判据定为候选 B（第 7 节）。另外记一条主题的小问题：续页页脚计数显示 `6/11, 6/11, 7/11, 8/11`，下一帧又跳到 `10/11`。溢出本身已经是缺陷，不影响本任务，可以反馈给主题仓库。
- **对父 design.md 的影响：** 父任务第 6 节 D-OVERFLOW-V 的写法是「逻辑页数（按页标签去重）」，并注明「具体判据由子任务 3 的 spike 确认」。本结论改用 `<ysu-note>` 的页号跳跃，属于该条授权的范围，不改接口。
  D-NOTES-PDF 改成按备注页数和配对检查、不再要求总页数 = 2 × 帧数，只是 Touying 分支的细化，Beamer 分支不变。
  新增的可选规划字段 `meta.chapters[].nav_label` 在第 9 节已经预见到，Beamer 忽略这个字段，需要同步写进 `plan-schema.md`。

## 11. 实施偏差

实施后的代码与本文件前十节的差异如下，均不改父 design.md 的接口；以代码与 `references/touying-backend.md` 为准。

- **讲稿记录的读取命令：** D-OVERFLOW-V 先用 `typst eval 'query(<ysu-note>).map(it => it.value)' --root <out> --in <out>/defense.typ` 取 `<ysu-note>` 记录，失败时再用 `typst query`（Typst 0.15.1 中 `typst query` 已弃用）。两者都只在 typst 存在且答辩稿导入的包均已安装时运行，避免触发下载。
- **源区标记：** 论文原文（题注、公式、表格）写在 `// defense-source-begin` 与 `// defense-source-end` 两行注释之间。D-EQ-SRC、D-TAB-SRC 只比较源区内的 `mitex` 与 `result-table`，源区外的数学与表格报 Major；源区内文字不计可见字符、不参与 D-NUM-SRC。
- **`figure-bullets` 左图：** `position: left` 用 `#grid(columns: (1.25fr, 1fr))`，不用第 2 节的 `slide(composer:)`；`position: top` 为上下排列。`equations-figure` 有图时同样用 `#grid`。
- **其他组件：** `cards` 用 `side-card(label:)`，`outlook` 用 `label-row(label:)`，`thanks` 的 `recap` 只在创新点页有 1–3 条要点时传入；第 2 节的 `card` / `title-box` / `points` 写法未采用。
- **章标题：** 每章一个一级标题，使目录分组、页脚导航与章扉页编号对齐论文章号。第 1 章、首帧不是章前目录的章与规划中没有帧的章（在致谢前补齐）写成 `= … <touying:skip>`，不生成章扉页。
- **末帧溢出定位：** 末帧的页数要用投屏版总页数，读总页数需要 PyMuPDF；缺 PyMuPDF 时只检查末帧以外的帧。读不到记录时的退化判据（总页数 > 帧数）也需要 PyMuPDF，两者都不可行时记入 `skipped`。
- **`defense.log`：** 每次 `--compile` 开始时清空，再依次追加投屏版与备注版两次 `typst compile` 的 stderr（各带 `== typst compile <name> ==` 分隔行），不跨构建累积。
- **`deck.backend` 也写入 Beamer 规划：** `plan_deck.py` 对两个后端都写 `deck: {backend: …}`；缺该键的旧规划仍按 Beamer 构建。Beamer 规划不写 `nav_label`。
- **共享函数位置：** `select_macros` 与 `label_numbers` 移入 `typst_backend.py`，供 plan、build、check 共用；`build_deck.py` 保留同名别名（`select_macros = typst_backend.select_macros` 等），Beamer 路径行为不变。
- **表题位置：** `table` 版式的表题用 `#fig-caption(…)` 放在 `result-table` 之上，与 Beamer 表题在表上方一致。
- **`~` 与不换行空格：** 题注与单元格中的 `~` 转为 U+00A0；空白合并只作用于 ASCII 空白（初版用 `\s` 合并，会把 U+00A0 变回普通空格，已修正并加回归测试）。D-TAB-SRC 两侧都去掉全部空白后比较，NBSP 不产生误报。
- **图片缺失：** 规划引用的图片文件不存在时 build 退出 2（需要复制到 `img/`），而 Beamer 后端此时只由质量门报 D-FIG-MISSING。
