# 统一架构：academic-defense-beamer

本文件锁定三个子任务共享的接口。子任务的 design.md 只写本子任务的细节，冲突时以本文件为准；需要改这里时回到父任务修订。

## 1. 分层

```text
             共享（与后端无关）                       后端                         演示
extract_thesis.py ─► inventory.json ─► plan_deck.py ─► slide_plan.yaml ─► build_deck.py ─┬─ beamer  → defense.tex  → defense.pdf + defense-notes.pdf ─┐
                                                       (deck.backend)                     └─ touying → defense.typ  → defense.pdf + defense-notes.pdf ─┴─► FerroStage / pympress
                                                                                   check_deck.py（按后端选择检查项）   render_preview.py（只读 defense.pdf）
```

- `extract`、`plan`、讲稿五栏、时长预算、版式角色、内容规范与后端无关，保持一份实现。
- 后端只在 `build`（渲染、编译）与 `check`（源文件解析、编译日志、溢出判断）分叉。
- `render_preview.py` 只读投屏版 PDF，与后端无关，不改。

## 2. CLI 形状（子任务 2、3 实现，子任务 1 不改 CLI）

```text
plan_deck.py  --inventory … --out slide_plan.yaml [--minutes 40] [--stage …] [--theme yanshan|generic] [--backend beamer|touying]
build_deck.py --plan … --inventory … --out DIR [--logo PATH] [--force] [--compile] [--no-notes-pdf]
              [--typst-package SPEC] [--typst-package-path DIR] [--font-path DIR]
check_deck.py --deck DIR/defense.tex|DIR/defense.typ --inventory … [--plan …] [--log …] [--notes-pdf DIR/defense-notes.pdf] [--minutes 40] [--json]
```

- 后端的唯一来源是规划文件 `deck.backend`（默认 `beamer`，旧规划缺该键时按 `beamer` 处理）。`build_deck.py` 不另设 `--backend`，避免规划与构建不一致。
- `check_deck.py` 按 `--deck` 后缀选后端；后缀与清单不符时退出 2。
- `--compile` 默认同时编译投屏版与备注版；`--no-notes-pdf` 只编译投屏版。
- `--typst-package*`、`--font-path` 只在 Touying 后端生效；Beamer 后端收到时写 warning，不报错。

## 3. 产物布局

| 后端 | 自有文件（`--force` 才覆盖） | 编译产物 |
| --- | --- | --- |
| beamer | `defense.tex`、`defense-notes.tex`、`thesis-macros.tex`、`notes.md`、`build_manifest.json`、两个主题 `.sty`、`defense-layouts.sty` | `defense.pdf`、`defense-notes.pdf`、`defense.log`、`defense-notes.log` |
| touying | `defense.typ`、`notes.md`、`build_manifest.json`、`img/`（从论文仓库复制的图） | `defense.pdf`、`defense-notes.pdf`、`defense.log`（Typst stderr） |

- `build_manifest.json` 增加 `backend` 与 `notes_pdf`（文件名或 null）。
- Touying 的 `img/` 只含规划引用的论文原图，复制时保留相对路径；不复制校徽（主题自带品牌资源，来自已安装的包）。

## 4. 讲稿进入 PDF 的统一规则

- 备注内容：`要点`（加粗一行）→ `说什么`（正文）→ `过渡`（一行）→ `秒数`（行尾小字）。`可能提问` 不进备注 PDF，只在 `notes.md` 与提问准备中。
  理由：演讲者屏空间有限，提问是答辩前准备材料，不是台上口播。
- 占位符 `〔待填写〕` 原样进入备注 PDF，D-PLACEHOLDER 照常报告。
- 文字转义沿用各后端的现有转义函数；`**关键词**` 在备注里只加粗，不着色。
- 帧与备注一一对应：每个计入页数的帧恰有一段备注（可为空串）；备用页同样带备注。

## 5. FerroStage 兼容契约（两后端共同验收）

| 后端 | 备注版形态 | 校验 |
| --- | --- | --- |
| beamer | `\setbeameroption{show notes on second screen=right}`，每物理页 = 左幻灯片 + 右备注；16:9 时 W/H ≈ 3.56 | 全部页同尺寸且 W/H ∈ [3.1, 3.6]；页数 = 投屏版页数；相邻帧页标签不同（避免 FerroStage 误并组） |
| touying | `--input notes=on`，每帧后一页备注页 | 内容页标签 `N`、备注页 `notes:N` 且 suffix 与前一内容页标签逐字相等；备注页宽 = 内容页宽、高 = 宽 × 13.5/16 |

- 校验由 `check_deck.py` 的新码 **D-NOTES-PDF** 执行，用 PyMuPDF 读页尺寸与 `page.get_label()`；缺 PyMuPDF 时记入 `skipped`。
  D-* 码集合因此从 21 个变为 22 个（子任务 2 落地，子任务 3 扩展到 Touying）。
- FerroStage 实机打开属人工证据，不进 CI。

## 6. 质量门在 Touying 后端的映射（子任务 3 落地）

| 码 | Touying 处理 |
| --- | --- |
| D-MARKER | 帧前注释 `// defense-frame: id=… role=… chapter=… layout=…`，与 Beamer 同字段 |
| D-FIG-ALLOW / D-FIG-MISSING | 解析 `image("img/…")`，映射回清单原路径 |
| D-EQ-SRC | 公式以 `mitex` 原样包含清单 LaTeX 源，比较规则与 Beamer 相同 |
| D-TAB-SRC | 比较单元格纯文本与清单表体单元格（Typst 下无法逐字保留 `tabular` 源） |
| D-COMPILE | 读 `defense.log`（构建时保存的 Typst stderr）与 PDF 时间戳 |
| D-OVERFLOW-V | 投屏版 PDF 的逻辑页数（按页标签去重）多于帧数时报，定位到首个多出页所属帧；具体判据由子任务 3 的 spike 确认 |
| D-OVERFLOW-H | 记入 `skipped`（Typst 不报告水平溢出） |
| 其余后端无关码 | 直接复用 |

## 7. 兼容与回滚

- 旧规划（无 `deck.backend`）按 Beamer 构建，产物与改名前一致，另多出备注版。
- 每个子任务单独提交；回滚任一子任务只需回退其提交，子任务 1 的改名不依赖 2、3。
