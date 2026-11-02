# 新增 Typst Touying 后端（simply-ysu-touying）与 notes:N 备注版

父任务：`.trellis/tasks/10-27-academic-defense-beamer`（统一接口见其 design.md；Touying 主题与示例的事实见 `research/source-analysis.md` 第 2 节）。
前置条件：`10-27-defense-rename` 与 `10-27-defense-beamer-notes` 已提交（复用后者的备注内容规则、manifest 字段与 D-NOTES-PDF）。

## 目标

用户可在规划时选 `--backend touying`，从同一份 LaTeX 论文清单与规划生成 Typst Touying 答辩稿：投屏版 `defense.pdf` 与 FerroStage 可读的
`notes:N` 备注版 `defense-notes.pdf`，并通过与 Beamer 后端同一套（或明确映射的）质量门。同时把 simply-ysu-touying 的模板与 Notes 用法写成技能参考。

## 需求

1. `plan_deck.py --backend beamer|touying` 写入 `deck.backend`；`touying` 只允许 `--theme yanshan`（D4），否则退出 2。
   规划阶段对 Touying 不支持的输入给出 hints：EPS 图、复杂表（`\multirow`、`\multicolumn`、`\makecell` 等）、公式中 mitex 不支持的宏（以 spike 结论为准）。
2. `build_deck.py` 在 `deck.backend: touying` 时：
   - 渲染 `defense.typ`：`ysu-theme.with(notes: sys.inputs.at("notes", default: "off") == "on", nav-labels…, config-info(…))`，12 个版式映射到 simply-ysu-touying 组件；
     每帧前写 `// defense-frame: id=… role=… chapter=… layout=…`；每帧一段 `#note[...]`（结构页用 `note:` 参数），内容规则同父 design.md 第 4 节。
   - 把规划引用的论文图复制到 `<out>/img/`（保留相对路径），`defense.typ` 只引用 `img/…`；只复制，不转换、不重绘。
   - 文字字段一律以 Typst 字符串字面量输出（只转义 `\` 与 `"`），`**关键词**` 输出为 `#hl("…")`，杜绝 Typst 标记注入。
   - 公式用 `@preview/mitex` 渲染清单中的 LaTeX 源；表格把简单 `tabular` 解析为单元格网格交给 `result-table`。
   - `--compile`：预检 Typst 可执行文件与 `simply-ysu-touying`、`touying`、`mitex` 包均已在本机（不触发下载），再以 `--root <out>` 编译投屏版与 `--input notes=on` 备注版。
     包规格默认 `@preview/simply-ysu-touying:0.2.0`，可用 `--typst-package` 覆盖，`--typst-package-path`、`--font-path` 透传。
   - 退出码：沿用 2 / 4 / 5；新增 **6 = Typst 包未安装**（提示 `@local` 安装步骤，见 `references/touying-backend.md`）。
3. `check_deck.py --deck <out>/defense.typ`：按父 design.md 第 6 节的映射执行；D-NOTES 源级计数 `#note` / `note:`；D-NOTES-PDF 校验 `N` / `notes:N` 标签与 16:13.5 备注页尺寸。
4. 新参考 `references/touying-backend.md`：
   - 安装 simply-ysu-touying 0.2.0（Typst Universe 上架前的 `@local` 方法；上架后的 `@preview` 方法）、Typst ≥ 0.15.1、字体（思源黑体回退链、Arial）。
   - 版式映射表（12 个版式 → 组件），页面标记 `sub` / `takeaway` 与 Beamer 结论句的对应。
   - Notes 用法：`#note[]` 可多次拼接、结构页 `note:`、章扉页备注写在 `= 章名` 之后、`notes=on` 产物、`#pause` 子页与备注页的关系、`typst query "<ysu-note>"` 导出讲稿。
   - 保真限制：图格式（PDF / PNG / JPG / SVG；EPS 不支持）、公式经 mitex、表格只支持简单网格。
   - 进阶：定稿后脱离流水线手工维护 `defense.typ` 的方法（借鉴 `examples/beamer-thesis` 的 `// frame:` 注释、自定义版式放独立 `lib/layouts.typ`、`img/` 同步、`just` 菜谱），
     明确此后不再由 `build_deck.py` 覆盖，质量门仍可运行。
5. `references/presenting.md`（子任务 2 新建）补 Touying 备注版在 FerroStage 中的用法（`notes:N` 独立页，自动配对，无需选拼合布局）。
6. `SKILL.md`：description 与 when_to_use 加入 Typst / Touying 触发与边界（Typst 论文排版仍归 `typst-paper`）；argument-hint 加 `--backend`；Module Router、
   Required Inputs（Typst 依赖）、Output Contract、Reference Map 更新；正文仍只放路由与最小流程。`agents/openai.yaml` 同步。
7. evals：`trigger_eval.json` 增加 Touying 正例与 `typst-paper` 边界负例；`evals.json` 增加一个 Touying 端到端用例。
   `typst-paper/SKILL.md` 的 Do Not Use 若未提答辩幻灯片，补一句指向本技能。
8. 文档、资源页、manifest、CHANGELOG、`.trellis/spec/academic-writing-skills/defense-deck-contract.md`（后端维度、退出码 6、Touying 码映射）同步。

## 不做

- 以 Typst 论文为输入；Touying 下的 `generic` 主题；图标字体（`icon:` 一律不传，不依赖 Font Awesome）。
- 打包或复制 simply-ysu-touying 源码与 `ysu-*` 位图；自动下载 Typst 包。
- 迁入 `examples/beamer-thesis` 的论文专用版式、图片或口播。

## 验收

- [ ] fixture 以 `--backend touying` 走完 extract → plan → build：`defense.typ` 帧数 = 规划计数帧数，每帧一个 `defense-frame` 标记与一段备注；字符串注入用例（文字中含 `#`、`$`、`]`、`//`、`"`）渲染后按原文显示。
- [ ] `DEFENSE_TYPST_COMPILE=1` 且包已安装时：`defense.pdf` 页数 = 帧数；`defense-notes.pdf` 页数 = 2 × 帧数，标签 `N` / `notes:N` 交替，D-NOTES-PDF 零结果。
- [ ] 包缺失时 build 退出 6 且未尝试联网（测试中以空的 `--typst-package-path` 与隔离的数据目录验证）。
- [ ] check 在 Touying 稿上：D-FIG-ALLOW、D-EQ-SRC、D-TAB-SRC、D-NUM-SRC 各有正反例；D-OVERFLOW-H 出现在 `skipped`。
- [ ] Beamer 后端的全部现有测试不变且通过；旧规划（无 `deck.backend`）仍按 Beamer 构建。
- [ ] `just ci`、资源同步检查通过；trigger eval 新增用例通过。
- [ ] 人工证据：FerroStage 打开 Touying `defense-notes.pdf`，演讲者窗口显示备注。未执行标 UNVERIFIED。
