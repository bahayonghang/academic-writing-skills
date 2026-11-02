# Beamer 后端输出演讲备注 PDF 并推荐 FerroStage

父任务：`.trellis/tasks/10-27-academic-defense-beamer`（统一规则见其 design.md 第 3–5 节，FerroStage 事实见 `research/source-analysis.md` 第 3 节）。
前置条件：子任务 `10-27-defense-rename` 已提交，技能目录为 `academic-writing-skills/academic-defense-beamer/`。

## 背景

现在讲稿只写在 `notes.md`，`defense.tex` 里没有 `\note{}`，PDF 中没有演讲者备注。FerroStage 只从 PDF 读备注（同页拼合或 `notes:N` 独立页），
不读 Markdown，所以用户在台上看不到讲稿。

## 需求

1. `build_deck.py` 为每个帧（含备用页）写一段备注，内容与顺序按父 design.md 第 4 节：要点、说什么、过渡、秒数；不含可能提问。
2. 新增自有文件 `defense-notes.tex`：启用 `show notes on second screen=right` 后载入 `defense.tex`。`--compile` 同时编译出 `defense.pdf` 与 `defense-notes.pdf`；
   `--no-notes-pdf` 只编译投屏版。投屏版 `defense.pdf` 的页数与外观不变。
3. 备注宏由主题提供（例如 `\DefenseNote`），帧模板只调用宏，不定义宏（沿用现有契约）。
4. `check_deck.py`：
   - D-NOTES 增加源级检查：`defense.tex` 中计入页数的每个帧恰有一个备注宏调用。
   - 新码 D-NOTES-PDF：备注版每页同尺寸、W/H ∈ [3.1, 3.6]、页数等于投屏版、相邻页标签不同。默认读 `--deck` 同目录的 `defense-notes.pdf`，可用 `--notes-pdf` 指定；
     缺 PyMuPDF 或 manifest 记录 `notes_pdf: null` 时记入 `skipped`；应有却缺文件时报 Minor。
5. 新参考 `references/presenting.md`：投屏版与备注版的区别；FerroStage 推荐用法（打开 `defense-notes.pdf`，自动或手动选 `Right` 拼合，演讲者窗口读备注，观众窗口只显示左半）；
   安装方式按真实发布状态写（当前无 GitHub Release：源码 `just release` 生成 Setup.exe；仅 Windows x64）；非 Windows 用 pympress；备注页内容规则。
6. `SKILL.md`：Output Contract、Module Router（`build` 行、退出码）、Workflow 第 6 步后加“放映”一步，Reference Map 加 `presenting.md`；正文保持精简。
   `references/speaker-notes.md`、`references/quality-gate.md`、`references/plan-schema.md`、示例 `examples/*.md` 同步。
7. 双语技能页、资源页与 `docs/resource-manifest.json` 同步；`.trellis/spec/academic-writing-skills/defense-deck-contract.md` 更新自有文件表与 D-* 码集合（22 个）。

## 不做

- Touying 后端（子任务 3）。
- pdfpc 专用注释、同页上下拼合（`bottom`）、`notes:N` 独立页形式的 Beamer 输出。
- 修改 FerroStage。

## 验收

- [ ] fixture 构建后 `defense.tex` 每个计数帧恰有一个备注宏；`defense-notes.tex` 存在；旧的 7 个自有文件内容除新增备注宏外不变。
- [ ] `DEFENSE_COMPILE=1` 下：`defense-notes.pdf` 页数 = `defense.pdf` 页数，每页 W/H ≈ 3.56；D-NOTES-PDF 零结果。
- [ ] D-NOTES-PDF 正反例单测：宽高比不在带内、页数不符、相邻标签相同、文件缺失、manifest 关闭、缺 PyMuPDF 各一例。
- [ ] 只改讲稿后 `--force --compile`：两份 PDF 都重编，check 不误报 D-COMPILE（沿用“未变文件保留 mtime”规则，`defense.tex` 因备注改变而重写属预期）。
- [ ] `just ci` 与资源同步检查通过。
- [ ] 人工证据：FerroStage 打开 fixture 的 `defense-notes.pdf`，演讲者窗口显示备注、观众窗口只显示幻灯片。未执行标 UNVERIFIED。
