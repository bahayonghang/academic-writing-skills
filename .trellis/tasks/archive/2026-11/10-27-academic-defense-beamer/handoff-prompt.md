请实施 Trellis 父任务 `.trellis/tasks/10-27-academic-defense-beamer` 及其全部三个子任务。规划已经完成并经我审阅，我在此批准实施：可以按顺序对每个子任务运行 `task.py start`。

## 先读

1. 父任务：`prd.md`、`design.md`、`implement.md`、`research/source-analysis.md`。父任务 `design.md` 是三个子任务共享的接口；子任务与它冲突时以父任务为准。
2. 每个子任务开工前，读它自己的 `prd.md` → `design.md` → `implement.md`，以及 `implement.jsonl` / `check.jsonl` 列出的 spec。
3. 仓库规则：`AGENTS.md`，以及 `.trellis/workflow.md` 的 Phase 2 与 Phase 3。

## 顺序（严格串行，前一个提交并归档后才开始下一个）

1. `.trellis/tasks/10-27-defense-rename`：把 `latex-defense-zh` 更名为 `academic-defense-beamer`，行为不变。
2. `.trellis/tasks/10-27-defense-beamer-notes`：Beamer 稿写入 `\note`，另出 second-screen 备注版 `defense-notes.pdf`；新增 D-NOTES-PDF；新增 `references/presenting.md`，推荐用 FerroStage 放映。
3. `.trellis/tasks/10-27-defense-typst-backend`：新增 `--backend touying`（simply-ysu-touying 1.0.0），讲稿用 `#note`，用 `notes=on` 编译备注版。先做 design.md 第 8 节的 spike S1–S5，结论写回 design.md 再编码。
4. 回到父任务，按其 `implement.md` 的“集成复核”逐条核对父 `prd.md` 的跨子任务验收。

每个子任务都走同一个循环：`task.py start` → 实施（可派 trellis-implement）→ trellis-check → 修复 → 本子任务的验证命令 → 提交 → `task.py archive`。

## 已定决策（我未另行说明时按此执行）

- Q1：Touying 默认包规格为 `@preview/simply-ysu-touying:1.0.0`，构建前预检本机是否已安装；文档同时写 `@local` 过渡安装方法。不联网下载包，也不把主题源码或 `ysu-*` 位图复制进技能。
- Q2：FerroStage 目前没有 GitHub Release，只支持 Windows x64。文档写“源码 `just release` 生成 Setup.exe”，非 Windows 用户推荐 pympress。不写不存在的下载链接。
- 版本保持 6.0.0。CHANGELOG 只改 `[Unreleased]`：已有条目把技能名改成新名称，新增能力写成新条目，不另写改名条目。
- 编译测试开关：`DEFENSE_COMPILE`（XeLaTeX），`DEFENSE_TYPST_COMPILE`（Typst）。

## 只读外部来源（只能读；这些绝对路径不得写进技能、测试或文档）

- Typst 主题与示例：`D:/Documents/Code/Writing/touying-theme-ysu`（`themes/*.typ`、`README.zh.md`、`examples/check-page-labels.py`、`examples/beamer-thesis/`）
- FerroStage：`D:/Documents/Code/Rust/Exp/ferrostage`（`docs/beamer-notes.md`、`README.zh-CN.md`）

## 边界与停止条件

- 每个子任务只改它 design.md / implement.md 列出的文件范围。出现以下情况时停下来问我：需要新接口、要跨入未获批准的目录、学术事实保护规则会变化、spike 结论推翻父 design.md 的接口、或者遇到计划外的失败。
- 学术事实保护（AGENTS.md）不得退化：图、数字、公式、表体只能来自论文。
- 本机执行用 PowerShell 语法，Python 一律走 `uv run`。每个子任务提交前都要跑通 `just ci` 和 `uv run python docs/scripts/check_resource_sync.py`。缺 XeLaTeX、Typst 或 Typst 包导致编译测试 skip 时，如实报告为 UNVERIFIED。
- FerroStage 实机打开备注版 PDF 属于人工证据：能做就截图存到对应任务的 `research/`，做不了就标 UNVERIFIED，不要声称已验证。
- 提交只在本地 `dev` 分支进行，用 Conventional Commit 加中文摘要（各子任务的 implement.md 里写有提交标题）。不要 push，不要开 PR，等我确认。

## 完成时汇报

- 每个子任务的提交哈希。
- `just ci` 的结果。
- fixture 分别用 Beamer 和 Touying 构建时的页数、各 D-* 码计数、两份备注版的 D-NOTES-PDF 结果。
- spike S1–S5 的结论。
- 所有 UNVERIFIED 项和遗留问题。
