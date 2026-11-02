# 答辩稿技能统一为 academic-defense-beamer（Beamer + Touying + 演讲备注）

父任务。负责需求总集、子任务图、跨子任务验收与最终集成复核，本身不是实施目标。
来源证据见 `research/source-analysis.md`。

## 用户需求（原话归纳）

1. 将 `academic-writing-skills/latex-defense-zh` 更名为 `academic-defense-beamer`：技能不再只做 LaTeX，要把 Typst 内容并入同一个技能。
2. 参考 `D:/Documents/Code/Writing/touying-theme-ysu`（Typst 包 `simply-ysu-touying` 0.2.0，依赖 Touying 0.8.0）及示例 `examples/beamer-thesis`，
   把 Typst 版模板和 Notes（演讲备注）的用法写进技能。
3. 文档推荐用 FerroStage（https://github.com/bahayonghang/ferrostage）放映 PDF 答辩稿，像 PPT 一样在演讲者屏读 Notes。

## 范围

- 输入仍是**中文学位论文的 LaTeX 仓库**（博士、硕士）。输出可选 LaTeX Beamer 或 Typst Touying。
- 讲稿五栏继续写入 `notes.md`；另外把讲稿写进 PDF，产出 FerroStage 可读的备注版 PDF。
- 质量门、预览、提问准备沿用现有流程，在 Touying 后端给出等价检查或明确标记跳过。

## 不做（本父任务及全部子任务）

- 以 Typst 论文仓库为输入（例如 modern-ysu-thesis）：另立任务。
- 英文答辩、期刊或会议报告、`.pptx` 输出。
- 打包或复制 simply-ysu-touying 主题源码与 `ysu-*` 品牌位图；技能只引用已安装的 Typst 包。
- 修改 touying-theme-ysu 或 FerroStage 仓库本身；把 simply-ysu-touying 0.2.0 发布到 Typst Universe。
- 迁入 `examples/beamer-thesis` 的论文图片、口播原文、真实姓名或 `lib/layouts.typ` 的论文专用版式。

## 子任务图

| 顺序 | 子任务 | 交付 | 依赖 |
| --- | --- | --- | --- |
| 1 | `10-27-defense-rename` | 改名与全仓引用迁移，行为不变，`just ci` 通过 | 无 |
| 2 | `10-27-defense-beamer-notes` | Beamer 后端写 `\note{}` 并编译 second-screen 备注版 PDF；D-NOTES 扩展；FerroStage 推荐文档 | 1 |
| 3 | `10-27-defense-typst-backend` | `--backend touying`：`.typ` 渲染、`#note` 讲稿、`notes=on` 备注版、Typst 预检、质量门子集、文档 | 1、2（复用 2 的备注 PDF 校验） |

依赖是顺序约束，不是 Trellis 依赖系统；各子任务的 implement.md 重复写明前置条件。

## 已定决策（实施前可由用户推翻）

- D1 名称为 `academic-defense-beamer`。“Beamer”指 PDF 答辩幻灯片体裁，覆盖 LaTeX Beamer 与 Typst Touying 两个后端。范围仍是中文学位论文。
- D2 技能版本保持 `6.0.0`：该技能尚未发版，`docs/CHANGELOG.md` 的 `[Unreleased]` 段落直接改写为新名称，不另写“改名”条目。
- D3 Touying 后端通过可配置的包规格导入主题，默认 `@preview/simply-ysu-touying:0.2.0`（2026-10-28 用户决定，替代原 1.0.0；主题同步升到 Touying 0.8.0）；构建前预检该包能否在本机解析，
  不能时给出 `@local` 安装说明并退出，不联网下载，不打包主题。理由（原）：0.2.0 当时尚未上架；2026-11-01 已上架 Typst Universe，默认值不变，`@local` 作离线备选。
- D4 Touying 后端 MVP 只支持 `yanshan` 主题；`--theme generic --backend touying` 报参数错误。
- D5 推荐演示器 FerroStage（Windows x64，当前无 GitHub Release，需源码构建安装器）；非 Windows 用户给出 pympress 作替代。
  文档按实际发布状态写安装方式，不写不存在的下载链接。
- D6 投屏版 PDF 不变；备注版是额外产物，文件名带 `-notes`。

## 跨子任务验收

- [x] 仓库中除归档任务与 journal 外，不再出现 `latex-defense-zh`、`latex_defense_zh`、`DEFENSE_ZH_COMPILE`（迁移说明里的旧名提及除外）。
- [x] `just ci` 四步全部通过；`uv run python docs/scripts/check_resource_sync.py` 通过。
- [x] 同一份 fixture 论文分别以 `--backend beamer` 与 `--backend touying` 构建，得到投屏版与备注版各一份 PDF；
      两份备注版都通过同一个备注 PDF 校验（Beamer：页宽高比在 FerroStage 拼合带内；Touying：`N` / `notes:N` 标签序列）。
- [ ] 本机人工核对（记录为证据，不作 CI 要求）：两份备注版在 FerroStage 中打开，演讲者窗口显示备注，观众窗口只显示幻灯片。
      没有执行时在交付说明中标为 UNVERIFIED。
- [x] `SKILL.md`、双语技能页、README 与 `docs/` 的用法一致；SKILL.md 正文仍只放路由与最小流程，细节在 `references/`。
- [x] 学术事实保护不退化：图、数字、公式、表体仍只来自论文；Touying 后端的公式、表格保真规则写入质量门参考。

## 待用户确认的问题

- Q1 simply-ysu-touying 1.0.0 是否计划近期上架 Typst Universe？若是，D3 的默认值不变，只在文档里保留 `@local` 过渡说明；若否，默认值改为 `@local/simply-ysu-touying:1.0.0`。
- Q2 FerroStage 是否会在本任务完成前发布 GitHub Release？决定文档写“下载 Setup.exe”还是“源码 `just release`”。
