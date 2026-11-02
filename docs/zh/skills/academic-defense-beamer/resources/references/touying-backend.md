# Typst Touying 后端

本文件说明 Touying 后端的安装、版式映射、演讲备注、保真限制、退出码与定稿后的手工维护方法。Touying 后端从同一份论文清单与规划生成 Typst 答辩稿 `defense.typ`，使用 Typst 主题包 simply-ysu-touying。规划字段见 [清单与规划字段](plan-schema.md)，Beamer 版式见 [版式目录](slide-layouts.md)，检查见 [质量门](quality-gate.md)，放映见 [放映与演讲备注](presenting.md)。

## 适用范围

- 输入仍是中文学位论文的 LaTeX 仓库；Typst 只用于答辩稿。用 Typst 写的论文不适用本技能，论文排版用 `typst-paper`。
- 只支持 `yanshan` 主题。主题包自带配色、版位与校标，本技能不定义 Touying 的颜色，也不复制主题源码或校标位图。
- 后端的唯一来源是规划的 `deck.backend`。生成规划时用 `plan_deck.py --backend touying` 写入；`build_deck.py` 没有后端参数。

```bash
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory inventory.json --out slide_plan.yaml --backend touying [--minutes 40] [--stage predefense|defense]
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan slide_plan.yaml --inventory inventory.json --out DIR [--force] [--compile] [--no-notes-pdf] [--typst-package SPEC] [--typst-package-path DIR] [--font-path DIR]
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck DIR/defense.typ --inventory inventory.json [--plan slide_plan.yaml] [--json]
```

## 安装

### Typst 与包版本

| 依赖               | 版本或规格                               | 说明                                                       |
| ------------------ | ---------------------------------------- | ---------------------------------------------------------- |
| Typst              | 0.15.1 或更高                            | `typst --version` 低于 0.15.1 时，`build_deck.py --compile` 退出 5 |
| 主题包             | `@preview/simply-ysu-touying:0.2.0`      | 默认值；`--typst-package` 可改为其他规格，例如 `@local/simply-ysu-touying:0.2.0` |
| Touying            | `@preview/touying:0.8.0`                 | 主题包的依赖，版本固定                                     |
| mitex              | `@preview/mitex:0.2.6`                   | 渲染论文中的 LaTeX 公式，版本固定                          |

`build_deck.py` 不下载 Typst 包。`--compile` 先在本机查找以上三个包，任一缺失时列出缺失的包并退出 6，不调用 `typst compile`。

### 默认方法：从 Typst Universe 缓存

simply-ysu-touying 0.2.0 已在 Typst Universe 上架。在有网络的环境中，于流水线之外让 typst 下载一次。例如在任意空目录新建 `probe.typ`：

```typst
#import "@preview/simply-ysu-touying:0.2.0": *
#import "@preview/mitex:0.2.6": mitex
```

然后运行 `typst compile probe.typ`。typst 把主题包、它依赖的 `touying:0.8.0` 与 `mitex` 一起下载到包缓存目录。之后 `build_deck.py --compile` 可以离线运行。也可以用 `typst init @preview/simply-ysu-touying:0.2.0` 等方式触发下载，但 `mitex` 仍需单独导入一次。

### 备选方法：`@local` 安装

离线环境，或使用修改过的主题时，把主题包目录（含 `typst.toml`，版本为 0.2.0）复制到 Typst 本地包目录：

```text
<data>/typst/packages/local/simply-ysu-touying/0.2.0/typst.toml
```

然后在构建时指定：

```bash
uv run python -B $SKILL_DIR/scripts/build_deck.py … --compile --typst-package @local/simply-ysu-touying:0.2.0
```

主题包内部导入 `@preview/touying:0.8.0`，所以 `touying` 与 `mitex` 仍须在本机：放在包缓存目录，或放在本地包目录的 `preview/<name>/<version>/` 下。

### 包的查找顺序

构建脚本与 typst 使用相同的目录，查找 `<namespace>/<name>/<version>/typst.toml`：

1. 本地包目录：`--typst-package-path`；未指定时为环境变量 `TYPST_PACKAGE_PATH`；都没有时为 `<data>/typst/packages`。
2. 仅 `@preview` 包：包缓存目录，即环境变量 `TYPST_PACKAGE_CACHE_PATH`，未设置时为 `<cache>/typst/packages`。

| 系统    | `<data>`                             | `<cache>`                          |
| ------- | ------------------------------------ | ---------------------------------- |
| Windows | `%APPDATA%`                          | `%LOCALAPPDATA%`                   |
| Linux   | `$XDG_DATA_HOME` 或 `~/.local/share` | `$XDG_CACHE_HOME` 或 `~/.cache`    |
| macOS   | `~/Library/Application Support`      | `~/Library/Caches`                 |

`--typst-package-path` 与 `--font-path` 原样传给 `typst compile --package-path` 与 `--font-path`。

### 字体

主题包自带字体回退链：中文为思源黑体（Source Han Sans SC）及其回退，西文为 Arial。本机缺少这些字体时，typst 换用其他字体并给出警告，版面可能变化。字体放在非系统目录时，用 `--font-path DIR` 传入。答辩稿不传 `icon:` 参数，不需要 Font Awesome 等图标字体。

## 产物

| 文件                  | 说明                                                                                     |
| --------------------- | ---------------------------------------------------------------------------------------- |
| `defense.typ`         | 答辩稿；每帧前一行为帧标记，每帧一段备注                                                 |
| `notes.md`            | 讲稿，格式与 Beamer 后端相同，见 [讲稿格式](speaker-notes.md)                            |
| `build_manifest.json` | `backend: "touying"`、`notes_pdf`、`typst_package`、`typst_version`、`copied_images`、文件散列与告警 |
| `img/`                | 规划引用的论文原图副本，保留清单中的相对路径，例如 `img/fig/chapter3/network.png`         |
| `defense.pdf`         | 投屏版，每帧一页（编译后）                                                               |
| `defense-notes.pdf`   | 备注版，每帧之后一页 `notes:N` 备注页（编译后；`--no-notes-pdf` 时不编译）               |
| `defense.log`         | 两次 `typst compile` 的标准错误；每次 `--compile` 开始时清空                             |

- `defense.typ`、`notes.md`、`build_manifest.json` 与 `img/` 是自有文件。任一已存在且未加 `--force` 时退出 4。
- 内容未变的文件与图片不重写，保留修改时间。`--force` 只删除上次构建写入、本次不再引用的图片，依据旧 `build_manifest.json` 的 `copied_images`；`img/` 中的其他文件不动。
- Typst 的 `--root` 是输出目录，答辩稿不能引用目录外的文件，所以图片先复制到 `img/`。复制保留字节，不转换格式，不重绘。
- 校标来自主题包。Touying 后端忽略 `--logo` 并给出提示。

编译命令：

```text
typst compile --root DIR [--package-path P] [--font-path F] DIR/defense.typ DIR/defense.pdf
typst compile --root DIR [--package-path P] [--font-path F] --input notes=on DIR/defense.typ DIR/defense-notes.pdf
```

## 版式映射

每帧前一行写帧标记 `// defense-frame: id=<id> role=<role> chapter=<n|-> layout=<layout>`，字段与 Beamer 后端相同。内容版式的帧头依次为：`== #"帧标题"`、`#note[…]`、`#sub("小节")`（`subsection` 非空时）、`#takeaway("结论句")`（`takeaway` 非空时）。

| 版式               | Touying 输出                                                                                                                                         |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cover`            | `#title-slide(note: […])`；题目、作者、导师、专业、学院、日期与阶段写在导言区的 `config-info`                                                         |
| `toc`（总目录）    | `#outline-slide(groups: ((from: 3, to: 5), ), note: […])`；每段连续的 `research` 章为一组，按章标题序号计；没有研究章时不传 `groups`                   |
| `toc`（章前目录）  | `= #"章题"`、`#note[…]`、`#chapter-opener(…)`；帧有 `takeaway` 时作 `question:`，有 `bullets` 时取前 3 条作 `keywords:`，都没有时不传参数               |
| `bullets`          | 帧头加 `#points(…)`                                                                                                                                  |
| `figure`           | 帧头加 `#figure-box(caption: […])[#image("img/…", height: 4.2cm)]`                                                                                     |
| `figure-bullets`   | `position: left`：`#grid(columns: (1.25fr, 1fr))`，左格为 `figure-box`（高 3.2 cm），右格为 `points`；`position: top`：`figure-box`（高 2.3 cm）在上，`points` 在下 |
| `figure-grid`      | 帧头加 `#grid(columns: n)`（n 为每行子图数），每格一个子图 `figure-box`（高 2.9 cm 或 1.35 cm），其后 `#fig-caption(…)` 为总题注                             |
| `equations-figure` | 每个公式一个 `#eq-block(number: "(3-1)")[#mitex(…)]`，其后为 `points`；有图时外包 `#grid(columns: (1.15fr, 1fr))`，图在右格（高 2.9 cm）               |
| `table`            | 帧头加 `#fig-caption(…)`（表题在表上方），再加 `#result-table(header: (…), rows: (…))`                                                                |
| `cards`            | 每条要点一个 `#side-card(label: "问题一")[…]`；`innovation` 页的标签为「创新点 1」等                                                                  |
| `paper-summary`    | `points` 加 `#paper-box[…]`                                                                                                                          |
| `outlook`          | 每条一个 `#label-row(label: "其一")[…]`                                                                                                              |
| `thanks`           | `#ending-slide(recap: (…), note: […])`；`innovation` 帧有 1–3 条要点时，`recap` 依次为「创新点 k」与该要点，否则不传                                  |

- 规划给出 `width` 时，图写 `width: N%`（N 为 `width` 乘以 100），否则按上表的高度。
- 帧标题对应 Touying 的 `== 页`，小节条对应 `sub`，结论句对应 `takeaway`。Touying 主题把结论句显示在页眉主标题位置，Beamer 主题显示在页底；两者语义相同，字数规则见 [内容规范](content-rules.md)。
- 每章有一个一级标题 `=`，使目录、页脚导航与章扉页编号与论文章号一致。第 2 章起由章前目录帧写出 `= 章题`；第 1 章、首帧不是章前目录的章，以及规划中没有帧的章（在致谢之前补齐）写成 `= #"章题" <touying:skip>`，只登记该章，不生成章扉页。
- 备用页在致谢之后，同样带帧标记与备注。

### 页脚导航 `nav_label`

页脚导航栏用 `ysu-theme.with(nav-labels: (…))` 显式传入每章的短名，来源为规划的 `meta.chapters[].nav_label`。

- 默认规则：`plan_deck.py --backend touying` 为每章写 `nav_label`。章题不超过 6 个字符时用章题，否则写「第k章」，并在该章第一帧的 `hints` 中提示改成不超过 6 字的短名。
- 原因：6 章全名（16–24 字）会让页脚重叠折行，作者与阶段栏被挤出；不超过 5 字的短名排列整齐。
- 规划缺少 `nav_label` 时，`build_deck.py` 按同一规则补上。Beamer 后端忽略该字段。

## 演讲备注

### 写法

- 每帧恰有一段备注，内容与 Beamer 后端相同：要点（加粗）、说什么、过渡，行尾为本页秒数。「可能提问」不进入 PDF，只在 `notes.md` 中。规则见 [放映与演讲备注](presenting.md)。
- 内容页的备注写在 `== 标题` 之后的 `#note[…]`。`#note[…]` 可以写多次，同页的多段按段落拼接；构建脚本每帧只写一段。
- 结构页（封面、总目录、致谢）用函数的 `note:` 参数，例如 `#title-slide(note: […])`。
- 章扉页的备注写在 `= 章名` 之后、`#chapter-opener` 之前，归属于该章扉页。
- 备注文字同样是字符串字面量；`**关键词**` 在备注中只加粗（`#strong`），不着色。占位符「〔待填写〕」原样出现在备注页。

### 备注版

`typst compile --input notes=on` 时，主题在每帧之后插入一页备注页：

- 备注页与幻灯片同宽，高为宽的 13.5/16（幻灯片 16 cm × 9 cm，备注页 16 cm × 13.5 cm），深色底。
- 页标签：内容页为 `N`，备注页为 `notes:N`，`N` 与紧邻前一内容页的标签逐字相同。FerroStage 与 pympress 按这一约定配对，不需要选择拼合布局。
- 投屏版 `defense.pdf` 不写页标签。
- `#pause` 产生的子页共用同一个标签 `N`，备注页只跟在最后一个子页之后。构建脚本不输出 `#pause`。
- 没有备注内容的帧也有一页空备注页，配对不受影响。
- 帧内容溢出时，主题自动续页：续页各占一个数字标签，备注页只跟在最后一个续页之后（例如 `6, 7, 8, 9, notes:9`）。这时备注版总页数不等于 2 × 帧数，质量门按 D-OVERFLOW-V 报告。

### 导出讲稿记录

主题把每帧的备注写成 `<ysu-note>` 元数据，字段为 `frame`、`page`（帧起始页）、`kind`、`title`、`sub`、`chapter-no`、`chapter` 与 `text`（纯文本）。Typst 0.15.1 用 `typst eval` 导出：

```bash
typst eval 'query(<ysu-note>).map(it => it.value)' --root DIR --in DIR/defense.typ
```

旧写法 `typst query --root DIR DIR/defense.typ "<ysu-note>" --field value` 在 Typst 0.15 中已弃用，仍可使用。质量门的 D-OVERFLOW-V 先用前者，失败时用后者。

## 文本安全

- 规划中的全部文字字段输出为 Typst 字符串字面量 `"…"`，只把 `\` 转为 `\\`、`"` 转为 `\"`；连续空白合并为一个空格。
- 文字不进入 Typst 标记模式，因此 `#`、`$`、`*`、`_`、`@`、`<`、`` ` ``、`//`、`=` 与 `]` 都按原文显示。文字字段中的 `$…$` 不渲染为数学。
- `**关键词**` 拆分为 `[#"前"#hl("关键词")#"后"]`；未配对的 `**` 按普通字符输出。
- 题注与表格单元格取自论文 LaTeX 源，转换规则：`\ref` 与 `\eqref` 输出论文编号（未知标签为 `??`）；引文命令不输出；`\textbf` 与 `\emph`、`\textit` 保留强调；`$…$` 交给 mitex 行内渲染；`~` 输出为不换行空格（U+00A0）；`--` 与 `---` 输出为短横与长横；不能转换的命令按原文显示，并给出告警。

## 保真限制

### 图

- 支持 PDF、PNG、JPG（JPEG）与 SVG。PDF 图以矢量嵌入并保留原字体；SVG 中的中文按 `font-family` 列表回退。
- 不支持 EPS：Typst 不能读取。`plan_deck.py` 在 `hints` 中提示，`build_deck.py` 列出全部 EPS 图并退出 2。在论文中改用 PDF、PNG、JPG 或 SVG，或改用 Beamer 后端。
- 规划引用的图片文件不存在时，`build_deck.py` 退出 2（Beamer 后端此时只由质量门报告 D-FIG-MISSING）。

### 公式

- 公式源为清单中的 LaTeX 原文，去掉 `\label` 后以原始块交给 `#mitex(…)`，其余字符不变；编号由 `eq-block(number:)` 显示，对应 Beamer 后端的 `\tag*`。
- 论文导言区的宏按用到的公式、题注与表格单元格选取（含递归引用），翻译为 mitex 能读的 `\newcommand` 后，作为 `thesis-macros` 前置。翻译只改定义的写法，不改公式正文：

| 论文定义                                         | 翻译结果                                            |
| ------------------------------------------------ | --------------------------------------------------- |
| `\newcommand`、`\renewcommand`、`\providecommand` | 改为 `\newcommand`，定义体不变                      |
| `\def\X{…}`（无参数）                            | `\newcommand{\X}{…}`                                |
| `\DeclareMathOperator{\X}{t}`                    | `\newcommand{\X}{\operatorname{t}}`                 |
| `\DeclareMathOperator*{\X}{t}`                   | `\newcommand{\X}{\operatorname*{t}}`                |

- 带参数或分隔符的 `\def`（例如 `\def\X#1{…}`）、不完整的定义与其他定义命令不翻译：`plan_deck.py` 在 `hints` 中提示，`build_deck.py` 退出 2，建议改用 Beamer 后端。
- mitex 不能渲染的其他命令在编译时报错，由 D-COMPILE 报告。

### 表格

- 只支持简单表：一个 `tabular`、`tabular*` 或 `tabularx` 环境，内容只有 `\hline`、`\toprule`、`\midrule`、`\bottomrule`、`\cline`、`\cmidrule`、`\addlinespace`、`&`、`\\` 与单元格文字；单元格内可有 `$…$`、`\textbf`、`\emph`、`\ref` 与引文命令。
- 含 `\multirow`、`\multicolumn`、`\makecell`、嵌套环境，或单元格中有不能转换的命令时为复杂表；`longtable` 与 `xltabular` 也不支持。`plan_deck.py` 提示，`build_deck.py` 退出 2。复杂表换用论文中展示同一结果的图，或改用 Beamer 后端。
- 第一行作 `result-table` 的 `header`，其余行作 `rows`；列数不足的行在末尾补空单元格。

### 源区

论文原文（题注、公式、表格）放在 `// defense-source-begin` 与 `// defense-source-end` 两行注释之间。质量门只把源区内的公式与表格与清单比较；源区内的文字不计可见字符，也不参与 D-NUM-SRC。

## 退出码

| 脚本            | 退出码                                                                                                                                                                                    |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plan_deck.py`  | 0：成功；2：参数或输入错误，含 `--backend touying` 与 `yanshan` 以外的主题同用                                                                                                             |
| `build_deck.py` | 0：成功；2：规划校验失败、主题不是 `yanshan`、`--typst-package` 不是 `@namespace/name:x.y.z`、EPS 或不支持的图片格式、图片文件不存在、复杂表、不能翻译的宏；4：自有文件已存在且未加 `--force`；5：未找到 typst、typst 低于 0.15.1、任一份编译失败或超时（错误信息指明是哪一份）；6：主题包、`touying` 或 `mitex` 未安装在本机 |
| `check_deck.py` | 0：没有 Critical 与 Major；1：有；2：输入错误，含 `--deck` 后缀不是 `.tex` 或 `.typ`、后缀与 `build_manifest.json` 的 `backend` 不符                                                      |

退出 6 时，按本文「安装」一节安装缺失的包后重新运行 `build_deck.py --compile`；不需要 `--force` 以外的改动。

## 进阶：定稿后手工维护

规划定稿、质量门通过后，可以脱离流水线，直接修改 `defense.typ` 做细节排版。

1. 复制一份输出目录作为手工维护的工作目录，此后不再对它运行 `build_deck.py --force`：重建会覆盖 `defense.typ`、`notes.md` 与 `img/` 中的副本。
2. 保留每帧前的 `// defense-frame:` 标记。新增的帧也写标记，质量门用它映射帧、页角色与页序。
3. 论文原文继续放在 `// defense-source-begin` 与 `// defense-source-end` 之间，不改动公式与表格内容。
4. 自定义版式放在独立文件中，例如 `lib/layouts.typ`，由 `defense.typ` 导入；这些文件只使用主题包的公开组件。
5. 论文的图更新后，重新把图复制到 `img/`（保持清单中的相对路径），不在答辩稿目录中改图。
6. 可以用 `just` 等任务工具记录常用命令，例如编译两份 PDF 与导出讲稿。
7. 质量门仍可运行：`check_deck.py --deck <工作目录>/defense.typ --inventory inventory.json`。讲稿以 `defense.typ` 中的备注为准时，`notes.md` 不再自动同步，D-NOTES 的讲稿结果需要人工判断。
