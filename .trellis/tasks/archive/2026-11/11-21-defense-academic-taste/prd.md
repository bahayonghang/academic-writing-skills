# 提升 academic-defense-beamer 学术视觉与信息架构品味

## Goal

提炼高水平学术/科技答辩 PPT 的「三段式视觉锚点、二维容器矩阵、双层克制强调、带基准关键指标块与短语化微排版」机制，经 `qiaomu-meta-skill` 泛化门禁过滤后融入 `academic-defense-beamer`，消除 Beamer 后端早期粗放视觉与双后端能力代差，在不突破学位论文事实保护边界的前提下提升成稿品味。

## Background

- 来源案例拆解见 `research/source-article.md`（12 张 16:9 答辩页的版面几何、配色权重与微排版记录，含第 9 页中英夹杂漏译词反例）。
- 先例检索与泛化差距判定见 `research/prior-art-and-gap-matrix.md`（G1–G12，已核验本机 `@preview/simply-ysu-touying:0.2.0` 的 `tokens.typ`、`components.typ`、`ysu-beamer.typ` 公开 API）。
- 跨脚本契约见 `.trellis/spec/academic-writing-skills/defense-deck-contract.md`。
- 既有测试锚点：`tests/skills/academic_defense_beamer/test_defense_theme_assets.py:30-62`（色表与 `LAYOUT_API`）、`test_defense_build.py:82,313`（`**词**` → `\DefenseHighlight`）、`test_defense_typst_backend.py:28-29` 与 `test_defense_build_typst.py:81`（Touying 强调映射）、`scripts/check_deck.py:964,1361` 与 `scripts/check_typst.py:389,451`（卡片计数、可见字面量扫描、表格单元格提取）。

## Requirements

- **R1 学术色阶校准与双层克制强调（G1、G2）**：
  - Beamer 主题新增 `defenseTint`、`defenseLine`、`defenseMuted` 语义色，将 `yanshan` 的 `defenseRed` 从荧光纯红 `#FF0000` 校准为沉稳砖红 `#B42318`（`generic` 对应 `#A93226`），同步更新 `references/visual-spec.md` 与 `test_defense_theme_assets.py`。
  - 对齐双后端双层强调语法：`**关键结论词**` 在双后端统一渲染为砖红粗体（Beamer 沿用 `\DefenseHighlight`，Touying 改映射为 `#key`），新增 `*结构术语*` 渲染为深蓝粗体（Beamer 新增 `\DefenseTerm`，Touying 映射 `#hl`）；演讲备注中二者均转为不着色粗体。
  - `scripts/check_deck.py` 在既有 `D-DENSITY` 码下实装「单帧砖红关键强调超过 3 处报 Minor / P2」，不新增 `D-*` 码。

- **R2 三段式页面视觉锚点与封面/目录层次重塑（G3、G4、G10）**：
  - 升级 Beamer 页眉（章节/小节面包屑 + 主标题 + 底细灰线配左侧短砖红横条），将 `\DefenseTakeaway` 从单薄细红框升级为左深蓝/砖红语义色签 + 浅底收束条（`problem`/`challenges` 页凸显核心问题，其余内容页凸显核心结论），并优化封面、目录与致谢页的留白层次与骑跨胶囊信息排版。

- **R3 二维容器矩阵与「短签｜短句」微排版（G5、G6）**：
  - `cards` 版式支持规划可选字段 `columns: 1 | 2 | 3`（缺省：4 张卡默认 `2` 即 `2×2` 宫格，其余默认 `1`）：Beamer 用多列等宽卡片宏渲染，Touying 在 `columns > 1` 时用 `#grid` + `#title-box`、单列保持 `#side-card`；`check_deck.py` 的 `D-CHAIN` 与 `D-DENSITY` 同时统计 `side-card` 与 `title-box`。
  - `bullets` 条目支持可选 `维度短签｜核心短句` 语法（前缀 2–8 字时拆分为浅蓝/深蓝短签 + 对齐正文，Beamer 保持 `\item` 引导、Touying 保持 `#points` 位置参数并用默认 `#tag("短签")` 避免命名参数字符串进入 `check_typst.visible_lines`）；纯文本条目向后兼容。

- **R4 论文源保真 KPI 指标条与图文面板质感（G7、G8）**：
  - 内容帧支持可选 `metrics: [{label, value, basis, key?}]`（至多 3 项）：Beamer 渲染 `\DefenseKPI`，Touying 调用公开组件 `#kpi`；`label`/`value`/`basis` 纳入可见字符与 `D-NUM-SRC` 核验。
  - Beamer `\DefenseFigure` 增加细灰衬底面板与次级灰题注（图号加粗），`\DefensePaperBox` 升级为左深蓝签 + 浅灰蓝底卡片；`table` 帧支持可选 `highlight_rows: [int, ...]`（Touying 透传整数元组 `mark: (...)`，不产生方括号或字符串字面量，保持 `D-TAB-SRC` 与 `D-NUM-SRC` 零误报；Beamer 保持 `DefenseSource` 原文逐字不变）。

- **R5 短语化断言文风与去套话规范（G9）**：
  - `references/content-rules.md` 增补高品味文案细则：结论句须为可核查判断句（禁写“本节介绍了…”目录句）、要点优先采用 `2–4 字维度签｜12–28 字动宾/名词短语`、禁用空洞评价套话及非专业缩写的未译外文残留词，且不为凑字数强行扩写。

- **R6 契约、测试、双语镜像与 Qiaomu 交付证据同步**：
  - 所有新增规划字段均为可选，既有 `slide_plan.yaml` 100% 向后兼容。
  - 同步更新 `demo-deck.tex`、Beamer/Touying 单测、`references/*.md`、`examples/*.md`、`SKILL.md`（`last_updated`）、`README.md`/`README_CN.md`、`docs/` 双语镜像与 `docs/resource-manifest.json`、`.trellis/spec/academic-writing-skills/defense-deck-contract.md`，并在任务 `reports/` 下生成 `creation-handoff.md` 与验证证据清单。

## Constraints

- **学术事实保护**：不编造或换算数字、成果、实验结果；图只引用论文清单原图（`D-FIG-ALLOW`）；公式与 Beamer 表体逐字取自论文源（`D-EQ-SRC`、`D-TAB-SRC`）。
- **接口锁定**：5 个脚本 CLI 与退出码不变；12 个 `layout` 名称闭集不变；22 个 `D-*` 码名称闭集不变；备注版 PDF 的 FerroStage / pympress 兼容契约不变。
- **版权、脱敏与包归属**：不搬用来源微信案例的任何正文文字、机构名或配图；测试 fixture 与演示稿全部自写合成；不含任何维护者本机绝对路径；保留技能名 `academic-defense-beamer`、`PolyForm Noncommercial 1.0.0` 许可证与版本 `6.0.0`。

## Acceptance Criteria

- [x] **AC1（R1）**：Beamer 两主题色值与 `visual-spec.md`、`test_defense_theme_assets.py` 一致，去除 `#FF0000`；双后端对 `**词**`（砖红粗体 `\DefenseHighlight` / `#key`）与 `*词*`（深蓝粗体 `\DefenseTerm` / `#hl`）渲染语义一致；单帧 `**词**` > 3 处时双后端 `check_deck.py` 均报 `D-DENSITY` Minor。
- [x] **AC2（R2、R3）**：`cards` 在 `columns` 为 1、2（含 4 卡默认 2×2）、3 时双后端均正确渲染且 `D-CHAIN` / `D-DENSITY` 计数准确；`短签｜正文` 在双后端正确拆分且通过 `#`、`$`、`"`、`\` 转义安全单测。
- [x] **AC3（R4）**：`metrics` 在双后端分别生成 `\DefenseKPI` 与 `#kpi`，论文外数字准确触发 `D-NUM-SRC`（NEEDS-LLM）；Touying `highlight_rows` 正确输出 `mark:` 且 `D-TAB-SRC` 零误报。
- [x] **AC4（兼容性与实编预览）**：不含任何新字段的既有 fixture 规划在双后端构建与检查零回归；具备本机编译环境时，`DEFENSE_COMPILE=1` 与 `DEFENSE_TYPST_COMPILE=1` 下 `demo-deck.tex` 及合成答辩稿投屏版/备注版编译零 `Overfull \vbox`、`D-NOTES-PDF` 零结果，并通过 `render_preview.py` 生成总览图完成目视核验。
- [x] **AC5（R5、R6）**：`content-rules.md` 含短语化断言与禁套话/禁漏译外文规则；`just ci` 四步、`uv run python docs/scripts/check_resource_sync.py`、`just doc-build`、`git diff --check` 全部通过。
- [x] **AC6（证据口径）**：`reports/creation-handoff.md` 区分 `design advantage` / `validated advantage` / `hypothesis`，未实机人工打开 FerroStage 或未跑外部 provider 的部分明确标 `UNVERIFIED`。

## 已确认决策（2026-11-21 用户确认采用方案 A）

| 编号 | 决策项 | 已确认结论 |
| :--- | :--- | :--- |
| **D1** | 优化深度与范围边界 | 采用**方案 A（双后端协同增强）**：同时升级 Beamer 视觉骨架与色阶、扩展向后兼容的可选规划字段与微排版语法（`columns`、`metrics`、`highlight_rows`、`短签｜正文`），并补齐文案规范与强调上限门禁 |
| **D2** | Beamer 主题演进方式 | 直接升级 `yanshan` 与 `generic` 色阶及版式宏（对齐现代深蓝 `#1F296A` + 砖红 `#B42318` + 浅灰蓝块面 `#F2F4F9` 体系），不新增冗余 `--theme` 枚举 |
| **D3** | 双层强调语法分工 | `**关键结论**` 统一为砖红粗体（Beamer `\DefenseHighlight`、Touying `#key`，单帧上限 3 处）；`*结构术语*` 统一为深蓝粗体（Beamer `\DefenseTerm`、Touying `#hl`） |

## Out of Scope

- `.pptx` / Keynote / HTML 输出，英文答辩、期刊会议报告或科技奖申报书制作。
- 自动重绘论文机理图、引入论文清单外的外部实景图/证书图。
- 承诺规避任何检测器，或修改上游 `simply-ysu-touying` / `FerroStage` 仓库。
