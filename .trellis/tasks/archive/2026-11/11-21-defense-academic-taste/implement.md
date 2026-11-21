# 实施计划：提升 academic-defense-beamer 学术视觉与信息架构品味

> **激活门禁**：待用户在下一条消息明确批准最终规划摘要后，先运行 `uv run python ./.trellis/scripts/task.py start 11-21-defense-academic-taste` 将任务置为 `in_progress`，再按下列顺序施工。

---

## 有序执行清单

### Phase P1：Beamer 现代学术色阶与版式宏升级
- [x] 修改 `academic-writing-skills/academic-defense-beamer/templates/beamer/defense-layouts.sty`、`beamerthemeYanshanDefense.sty`、`beamerthemeGenericDefense.sty`（校准 `#B42318` 砖红与 `Tint`/`Line`/`Muted` 块面色阶；升级页眉、封面/目录/致谢、`\DefenseTakeaway`、`\DefenseFigure`、`\DefensePaperBox`；新增 `\DefenseTerm`、`\DefenseLead`、`\DefenseGridCard`、`\DefenseKPI`）。
- [x] 同步更新 `academic-writing-skills/academic-defense-beamer/references/visual-spec.md` 与 `templates/beamer/demo-deck.tex`。
- [x] 更新并运行 `uv run pytest tests/skills/academic_defense_beamer/test_defense_theme_assets.py`；若本机有 `xelatex`，加跑 `$env:DEFENSE_COMPILE='1'; uv run --with pymupdf pytest tests/skills/academic_defense_beamer/test_defense_theme_assets.py`。

### Phase P2：双后端微排版语法与可选规划字段
- [x] 修改 `scripts/typst_backend.py`（`ty_text` 支持 `**词**` → `#key`、`*词*` → `#hl`；新增 `ty_bullet` 处理 `短签｜正文` 与 `ty_metric` 处理 `#kpi`）。
- [x] 修改 `scripts/build_deck.py`（`tex_escape` 补 `*词*` → `\DefenseTerm`；`item_text` 补 `短签｜正文` → `\DefenseLead`；`validate_frame`、`SHOWN_BY`、`frame_context`、`typst_frame_context` 支持可选 `columns`、`metrics`、`highlight_rows`）。
- [x] 更新 `templates/jinja/frames/*.tex.j2` 与 `templates/typst/frames/*.typ.j2`（多列卡片网格、`metrics` 条、Touying `table` 的 `mark:`）。
- [x] 更新并运行 `uv run pytest tests/skills/academic_defense_beamer/test_defense_build.py tests/skills/academic_defense_beamer/test_defense_typst_backend.py tests/skills/academic_defense_beamer/test_defense_build_typst.py`。

### Phase P3：质量门、高品味文案规范、双语文档镜像与最终验收
- [x] 修改 `scripts/check_deck.py`（`COUNT_RES["card"]` 与 Touying `"card"` 支持多列卡片；`D-DENSITY` 增加单帧砖红关键强调 > 3 处报 Minor）并补齐 `test_defense_check.py`、`test_defense_check_typst.py` 正反例测试。
- [x] 更新 `references/{content-rules,slide-layouts,plan-schema,quality-gate,touying-backend}.md`、`examples/*.md`、`SKILL.md`（`last_updated`）。
- [x] 更新 `.trellis/spec/academic-writing-skills/defense-deck-contract.md`、`README.md`、`README_CN.md`、`docs/` 双语镜像并更新 `docs/resource-manifest.json`。
- [x] 运行完整验证门禁并输出 `.trellis/tasks/11-21-defense-academic-taste/reports/creation-handoff.md`：
  - `just ci`（含 `check-versions`、`lint`、`typecheck`、`test` 四步）
  - `uv run python docs/scripts/check_resource_sync.py`
  - `just doc-build`
  - 本机实编与 `render_preview.py` 总览图目视检查（`DEFENSE_COMPILE=1`、`DEFENSE_TYPST_COMPILE=1`）
  - `git diff --check`

---

## 回滚与风险控制

- 分阶段验证，每完成一个 Phase 立即跑对应 pytest 子集，避免跨层故障叠加。
- 若 Beamer 新增宏导致任何既有 fixture 出现 `Overfull \vbox` 或 `Overfull \hbox > 5pt`，优先收紧宏内边距（`inner ysep` / `\vspace`），绝不放宽 `check_deck.py` 阈值。
