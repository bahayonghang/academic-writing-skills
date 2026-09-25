# C1 实施证据

记录日期：2026-09-24。本文件不记录本机绝对路径。

## 手工编译

工作目录为会话 scratchpad 中 `templates/beamer/` 的副本。校徽为合成 PNG（1350 × 400 像素，纯色）。

| 运行 | 命令 | 退出码 | PDF 页数 | Overfull |
| --- | --- | --- | --- | --- |
| yanshan，带合成校徽 | `latexmk -xelatex -interaction=nonstopmode -halt-on-error demo-deck.tex` | 0 | 15 | 0 |
| generic | `latexmk -xelatex -interaction=nonstopmode -halt-on-error -jobname=demo-generic "-usepretex=\def\DefenseThemeName{GenericDefense}" demo-deck.tex` | 0 | 15 | 0 |
| generic，单次 xelatex | `xelatex -interaction=nonstopmode -halt-on-error -jobname=demo-generic "\def\DefenseThemeName{GenericDefense}\input{demo-deck.tex}"` | 0 | 15 | `Overfull \vbox` 0 |

`demo-deck.tex` 含 15 个 `\begin{frame}`，PDF 页数与帧数相等。单次 xelatex 运行的页数与 latexmk 两遍运行相同。

## 目视检查

逐页检查两主题的 PDF，结果如下：

- 封面：校徽、阶段字样、题带、信息表与日期的位置符合 `references/visual-spec.md`。
- 目录页：目录行整块水平居中；当前章为粗体（yanshan 黑色，generic `defenseBlue`）。
- 内容页帧标题：两侧双线与页码平行四边形位置正确。
- 卡片、「论文」框、结论句框、2 × 2 子图网格与表格均正确显示；表格水平居中，booktabs 横线在 200 dpi 渲染下完整。
- `DefenseSource` 帧：`\eqref` 输出 (3-2)，`\ref` 输出 3-1，`\cite` 不输出。
- generic 主题：不显示校徽，也不显示文字标识。

## 实施中修正的问题

1. 「论文」框出现 0.4 pt 的 `Overfull \hbox`：正文节点宽度改为减去 1.6 pt 边框宽度。
2. TikZ 节点使用 `align=center` 时中文字距被拉伸：封面题带与结论句框改用 `align=flush center`。
3. 目录行宽度测量为 0：`tikzpicture` 内部使用 `\nullfont`。测量移到 `\defense@tocmeasure`，在绘图前调用。
4. 表格未水平居中：`\par` 必须位于 `DefenseSource` 组内（`}\par`）。`references/slide-layouts.md` 的表格骨架已按此写。
5. latexmk 不接受 TeX 代码作为文件参数（报告找不到文件）。generic 手工编译命令改用 `-usepretex=`，本任务 `implement.md` 已同步。直接调用 xelatex 的写法可用，编译测试沿用该写法。

## 设计文档同步

- 父任务 `design.md` §5：补充 `logo-text` 键、`\DefenseFigure` 的可选参数与 `\DefenseCaption{题注}`。
- 本任务 `design.md` §2.4 与 `implement.md` 步骤 2：校徽路径为空或文件不存在时显示 `logo-text` 文字标识（yanshan 默认「燕山大学」，generic 为空）。

## docs 资源登记

- `--write-manifest --inventory-only` 重建清单为 295 条；新增 7 条，`sourceLocale` 均为 `zh`。
- 七份 zh 资源页与源文件逐字节相同（`cmp` 核对）。
- 七份 en 资源页为完整翻译。VitePress 把正文中的 ASCII 尖括号占位符解析为 HTML 标签，因此 en 页正文用 `\<…\>` 转义；代码块与行内代码不受影响。仓库已有同类写法。
- 资源契约测试的技能集合加 `latex-defense-zh`；两份安装页命令块各加一行，命令条数说明改为 eight 与「八条」。

## 质量门

| 命令 | 结果 |
| --- | --- |
| `rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh` | 4 passed，3 skipped |
| `DEFENSE_ZH_COMPILE=1 rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh` | 7 passed（7.39 s） |
| `rtk proxy uv run python docs/scripts/check_resource_sync.py --inventory-only` | passed（295 条） |
| `rtk proxy uv run python docs/scripts/check_resource_sync.py --skill latex-defense-zh` | passed |
| `rtk proxy uv run --extra dev python -m pytest -q tests/contracts/test_docs_bilingual_resources.py` | 10 passed |
| `rtk proxy just ci` | 2366 passed，5 skipped |
| `rtk proxy just doc-build` | build complete |

## Review gate

- AC6：对技能目录、docs 新页面、测试文件与本任务树目录执行 grep，搜索词只在会话中输入。技能目录、docs 新页面与测试文件无命中。Trellis 生成的 `task.json` 的 `creator` 与 `assignee` 字段为开发者 id，与仓库其他任务相同。
- `git status --porcelain`：只列出 design §1 的文件、本文件，以及 pws 登记任务（`09-23-pws-catalog-register`）的未提交文件。
- 测试 2 与测试 3 通过：两主题不定义版式宏；十二个版式名在 `slide-layouts.md` 与 `demo-deck.tex` 中一致。

## 后续

用户授权先登记 paper-writing-studio，再实施本任务树。按父任务 `implement.md`，C1 通过门禁后开始 C2。本任务不 commit、不归档、不 push。
