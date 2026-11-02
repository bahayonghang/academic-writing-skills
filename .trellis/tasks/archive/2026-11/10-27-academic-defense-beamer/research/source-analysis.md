# 来源分析：latex-defense-zh、simply-ysu-touying、FerroStage

调研日期：2026-10-27。本文件记录规划时读到的事实，子任务的 design.md 引用这里，不再重复取证。

## 1. 现有技能 `academic-writing-skills/latex-defense-zh/`

- 版本 6.0.0，尚未发版（`docs/CHANGELOG.md` 的 `[Unreleased]` 段落记录其登记为第八个 catalog 技能）。改名没有已发布用户需要迁移，
  只有维护者本机的旧安装目录 `~/.claude/skills/latex-defense-zh` 需要手动清理。
- 五模块流水线：`extract_thesis.py`(1215 行) → `plan_deck.py`(552) → `build_deck.py`(833) → `check_deck.py`(1441) → `render_preview.py`(132)，
  另有 `defense_budget.py`、`tex_loader.py`（latex-thesis-zh 的副本，受 `tests/contracts/test_tex_loader_alignment.py` 锁定）。
- 输入只有 LaTeX 论文仓库；输出 `defense.tex`（`ctexbeamer`，`aspectratio=169`）+ 主题 `.sty` + `notes.md` + `build_manifest.json`。
- 12 个版式：`cover`、`toc`、`bullets`、`figure`、`figure-bullets`、`figure-grid`、`equations-figure`、`table`、`cards`、
  `paper-summary`、`outlook`、`thanks`（`references/slide-layouts.md`）。帧模板在 `templates/jinja/frames/*.tex.j2`。
- 讲稿五栏（说什么 / 要点 / 秒数 / 过渡 / 可能提问）只写入 `notes.md`；**`defense.tex` 不含 `\note{}`**，PDF 里没有任何演讲者备注。
  这是“像 PPT 一样读 Notes”的直接缺口。
- 质量门 21 个 D-* 码，LaTeX 专属的有：D-MARKER（`% defense-frame:` 注释）、D-EQ-SRC / D-TAB-SRC（与清单逐字比较 LaTeX 源）、
  D-COMPILE / D-OVERFLOW-V / D-OVERFLOW-H（读 latexmk 日志的 Overfull）。
- 安全边界：论文仓库只读、不打包校徽（校徽只从论文仓库引用）、不联网、公式表体逐字取自论文。

### 改名波及面（`rg latex-defense-zh|latex_defense_zh|DEFENSE_ZH`，排除 archive/workspace）

60 个文件、162 处。分组：

| 组 | 文件 |
| --- | --- |
| 技能本体 | `SKILL.md`、`agents/openai.yaml`、`evals/*.json`、fixture `document*.tex` 注释、`templates/beamer/*.sty`、`templates/jinja/deck.tex.j2`、各脚本 docstring |
| 测试 | `tests/skills/latex_defense_zh/`（9 个文件，含 `conftest.py` 的 `DEFENSE_ZH_COMPILE`）、`tests/shared/test_tex_loader_security.py`、`tests/skills/latex_thesis_zh/test_thesis_rebuttal_installed.py` |
| 契约测试 | `tests/contracts/test_skill_contracts.py`（模块表、`allowed-tools` 断言、router help）、`test_skill_versions.py`、`test_skills_install.py`、`test_trigger_evals.py`、`test_tex_loader_alignment.py`、`test_docs_bilingual_resources.py` |
| 安装器 | `scripts/skills_install.py` |
| 相邻技能 | `latex-thesis-zh/SKILL.md`（路由边界 2 处）、`latex-thesis-zh/evals/trigger_eval.json` |
| 文档 | `README.md`、`README_CN.md`、`docs/{index,installation,quick-start,usage,CHANGELOG}.md` 与 `docs/zh/` 镜像、`docs/skills/latex-defense-zh/`、`docs/zh/skills/latex-defense-zh/`、`docs/skills/index.md`、`docs/.vitepress/config.ts`、`docs/resource-manifest.json`（52 处，含散列） |
| 规格 | `.trellis/spec/academic-writing-skills/defense-deck-contract.md`、`index.md`、`thesis-rebuttal-contract.md`、`include-boundary-contract.md` |
| 仓库指令 | `AGENTS.md`（3 处：技能列表、parser copies 段、测试段） |

## 2. Typst 主题 `D:/Documents/Code/Writing/touying-theme-ysu`（包名 `simply-ysu-touying`）

- `typst.toml`：`version = "1.0.0"`，`compiler = "0.15.1"`，唯一依赖 `@preview/touying:0.6.3`，许可 `MIT AND MIT-0`；
  `themes/assets/ysu-*` 品牌位图**不在** SPDX 许可范围内（`ASSETS.md`）。
- **发布状态**：Typst Universe 索引只有 `simply-ysu-touying 0.1.0`；`1.0.0` 返回 404。1.0.0 才有本技能需要的版式与备注。
  本机 `%LOCALAPPDATA%/typst/packages/preview/simply-ysu-touying/` 也只有 `0.1.0/`。
  结论：技能不能假设 `#import "@preview/simply-ysu-touying:1.0.0"` 可解析，必须有可配置的导入与可执行的预检。
- **2026-10-28 更新**：主题仓库决定把包版本改回 `0.2.0` 并升级到 `@preview/touying:0.8.0`（主题仓库任务 `10-27-touying-0-8-0`，
  当时仍在规划）。本技能目标改为 `@preview/simply-ysu-touying:0.2.0` + `touying:0.8.0`；上文 1.0.0 的描述保留为调研时的事实。
- 本机 Typst 0.15.1；本机包缓存另有 `@preview/mitex`（LaTeX 数学转 Typst 渲染）与 `tablem`。
- API（`themes/ysu-beamer.typ`、`themes/components.typ`）：
  - `ysu-theme.with(aspect-ratio, align, nav-labels, nav-full-labels, font, notes, config-info(title, author, supervisor, subject, school, date, stage, stage-en))`
  - 结构页：`title-slide(research-line:, note:)`、`outline-slide(groups:, note:)`、`= 章` + `chapter-opener(question:, keywords:, icon:, outline:, bridge:)`、
    `== 页` + `sub[...]` + `takeaway[...]`、`slide(composer:)`、`ending-slide(title:, kicker:, recap:, note:)`。
  - 组件：`hl`、`key`、`conclude`、`title-box`、`group-box`、`red-frame`、`card`、`paper-box`、`points`、`kpi`、`figure-box(caption:)`、
    `eq-block(number:, note:)`、`result-table(header:, rows:, mark:)` 等 30 个。
- **备注机制**：
  - `#note[...]` 可写在页内任意位置，同页多次按段落拼接；结构页用 `note:` 参数；章扉页的备注写在 `= 章名` 之后。
  - 备注同时写入 pdfpc（Touying `speaker-note`）。
  - `ysu-theme(notes: sys.inputs.at("notes", default: "off") == "on")` + `typst compile --input notes=on` 时每帧后插一页备注页：
    与幻灯片同宽，高 = 宽 × 13.5/16，深色底 18 pt；页标签内容页 `N`（`#pause` 子页共用 `N`），备注页 `notes:N`，备注页只跟在最后一个子页后。
  - `typst query --root . deck.typ "<ysu-note>" --field value` 导出 JSON 记录（frame、page、kind、title、sub、chapter-no、chapter、纯文本）。
  - `examples/check-page-labels.py --expect-notes`：只用标准库解析 Typst 写出的未压缩 PDF，检查标签序列与页面尺寸。
    **它不能解析 XeLaTeX 输出的压缩对象流**，跨后端复用需改用 PyMuPDF（`page.get_label()`）。
- 示例 `examples/beamer-thesis/`（被 `.gitignore` 忽略、不发布）：88 页博士预答辩复刻，`main.typ` + `chapters/ch*.typ` + `lib/layouts.typ`（2661 行论文专用版式）
  + `lib/icons.typ`（Font Awesome 5，需 `--font-path`，`--input icons=off` 可关）+ `sync-assets.py`（按 `img()` 引用从论文仓库复制图）
  + `export-speech.py`（`typst query` → `speech.md`，把 Typst 数学写回 LaTeX）+ `justfile`。
  - 可迁入技能的**方法**：每页前 `// frame: <id> (PNN)` 注释做帧映射；图片复制到输出目录再引用（Typst `--root` 限制不能引用根外文件）；
    `notes=on` 双产物；`typst query` 导出讲稿；`check-page-labels` 校验。
  - **不可迁入的内容**：论文图片、口播原文、真实姓名与题目、`lib/layouts.typ` 的论文专用版式、示例里的私有绝对路径。
- Typst `--root` 约束：被引用的图片必须位于 root 之内。论文仓库在输出目录之外时，必须先复制图片到输出目录（与 LaTeX 后端用 `\graphicspath` 指向论文仓库不同）。

## 3. FerroStage `https://github.com/bahayonghang/ferrostage`（本机 `D:/Documents/Code/Rust/Exp/ferrostage`）

- Rust + GPUI 的 PDF / Beamer 双屏演示器，`Cargo.toml` 版本 1.2.1，MIT OR Apache-2.0，离线、无遥测。
- **平台**：仅 x64 Windows 10 1903+ / Windows 11。macOS / Linux 无构建。
- **发布状态**：`gh repo view` 显示 `latestRelease: null`，没有 GitHub Release；安装路径是源码 `just release` 生成 `FerroStage-<ver>-windows-x64-Setup.exe`，
  或 `just build` 后运行 `target\release\ferrostage.exe`（需 Rust 1.99）。文档不能写“下载安装包”，除非届时已有 Release。
- 备注读取契约（`docs/beamer-notes.md`）：
  1. **同页拼合**：整份 PDF 同尺寸且 `W/H ∈ [3.1,3.6] ∪ [2.4,2.7]` 时自动候选 `Right`（左半幻灯片、右半备注）；
     `W/H ∈ [0.85,0.95] ∪ [0.63,0.70]` 时候选 `Bottom`。Beamer `\setbeameroption{show notes on second screen=right}` 在 16:9 下得到 32:9≈3.56，落在带内。
     比例只是候选，可被手动覆盖（`None/Left/Right/Top/Bottom`）。
  2. **独立备注页**：页标签 `notes:<suffix>`，suffix 与紧邻前一内容步的原始标签逐字相等（`notes:01` 不匹配 `1`）。正好是 simply-ysu-touying 1.0 的 `N` / `notes:N` 约定。
  3. 观众窗口不会落到备注页；`\pause` 子页按相同非空页标签分组。
  4. 已知局限：Beamer 3.72 fixture `notes-right.pdf` 中两帧都标 `1,1` 被误并组，需 `physical_pages` 覆盖。
     → Beamer 备注版必须保证每帧页标签互不相同（默认 `\insertframenumber` 标签即可，需实测）。
- 不支持读取 pdfpc 文本备注或外部 Markdown 讲稿（`notes_for` 的 Markdown 字段只是内存模型）。所以 `notes.md` 不能被 FerroStage 直接读取，
  备注必须进 PDF。
- 跨平台替代：pympress（GPL-2.0+，Linux / macOS / Windows）同时支持 Beamer second-screen 与 `notes:N` 约定；pdfpc 读 pdfpc 备注。

## 4. 对统一技能的推论

1. 共享层：`extract`（LaTeX 论文仓库）与 `plan`（`slide_plan.yaml`、讲稿五栏、时长预算）与后端无关，保留一份。
2. 后端层：`build` 增加 `--backend beamer|touying`；Beamer 走现有 Jinja `.tex.j2`，Touying 新增 `.typ.j2` 帧模板，映射到 simply-ysu-touying 组件。
3. 备注层：两个后端都产出“投屏版 PDF + 备注版 PDF”。Beamer 用 `\note{}` + second-screen；Touying 用 `#note[]` + `notes=on`。都以 FerroStage 为推荐演示器。
4. 质量门：后端无关码（D-COVERAGE、D-CHAIN、D-PLACEHOLDER、D-FIG-ALLOW、D-NUM-SRC、D-DENSITY、D-BUDGET、D-NOTES 等）复用；
   LaTeX 专属码需要 Typst 等价物或在 Typst 下记入 `skipped`。
5. 公式：Touying 后端用 `@preview/mitex` 渲染清单中的 LaTeX 源，保持逐字来源；论文自定义宏能否被 mitex 处理需要 spike。
6. 表格：LaTeX `tabular` 源无法逐字进入 Typst；只支持可解析为单元格网格的简单表，复杂表报构建错误并建议改版式或用 Beamer 后端。
7. 主题：Touying 后端 MVP 只有 `yanshan`（simply-ysu-touying）；`generic` 在 Touying 下报参数错误。
