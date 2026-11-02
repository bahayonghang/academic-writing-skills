# 执行计划：Touying 后端

前置：`10-27-defense-rename`、`10-27-defense-beamer-notes` 已提交。路径相对 `academic-writing-skills/academic-defense-beamer/`。
外部只读来源：`D:/Documents/Code/Writing/touying-theme-ysu`（主题 API、`examples/check-page-labels.py`、`examples/beamer-thesis` 的方法）。
**不得**把该仓库路径写进技能、测试或文档（项目规则禁止私有绝对路径）。

## 步骤

1. Spike S1–S5（design.md 第 8 节），在 scratchpad 进行；结论与固定版本写回 design.md。任何结论推翻本设计的接口时停止，回父任务修订。
2. `plan_deck.py`：`--backend`、`deck.backend`、主题兼容检查、Touying hints（EPS、复杂表、不支持的宏）。测试：`test_defense_plan.py`。
3. `scripts/typst_backend.py`：转义、`hl` 拆分、表格解析、图片清单、包预检。单测新文件 `test_defense_typst_backend.py`（不需要 Typst）。
4. `templates/typst/`：`deck.typ.j2` 与 12 个帧模板。`build_deck.py` 分派、`img/` 复制、manifest 字段、退出码 6、编译两份 PDF。
   测试 `test_defense_build_typst.py`：帧标记序列、每帧一段备注、注入用例、图片复制与 `--force`、复杂表与 EPS 报错、包缺失退出 6（隔离数据目录）。
5. `scripts/check_typst.py` 与 `check_deck.py` 分派：D-MARKER、D-FIG-*、D-EQ-SRC、D-TAB-SRC、D-NOTES、D-NOTES-PDF、D-COMPILE、D-OVERFLOW-V（按 S4）、D-OVERFLOW-H skipped。
   测试 `test_defense_check_typst.py`：各码正反例。
6. 编译用例（`DEFENSE_TYPST_COMPILE=1`，缺 Typst 或包时 skip）：fixture 全流程；`defense-notes.pdf` 标签与尺寸。
   `tests/skills/academic_defense_beamer/conftest.py` 加开关读取。
7. 文档：`references/touying-backend.md`（新）、`presenting.md`、`slide-layouts.md`（加 Touying 列）、`plan-schema.md`、`quality-gate.md`、`visual-spec.md`（Touying 主题来自包，颜色不在本技能定义）；
   `SKILL.md`、`agents/openai.yaml`、`examples/` 新增 `touying-defense.md`；`evals/trigger_eval.json`、`evals/evals.json`；`typst-paper/SKILL.md` 边界句。
8. 双语技能页、资源页；`uv run python docs/scripts/check_resource_sync.py --write-manifest`；README / README_CN 技能简介；CHANGELOG `[Unreleased]`。
9. spec：`defense-deck-contract.md` 增加后端维度、签名、退出码 6、Touying 码映射、错误矩阵与测试清单；`AGENTS.md` 测试段加 `DEFENSE_TYPST_COMPILE`。
10. 验证：
    ```bash
    just ci
    uv run python docs/scripts/check_resource_sync.py
    ```
    有 Typst 与包：`DEFENSE_TYPST_COMPILE=1 uv run pytest tests/skills/academic_defense_beamer -k typst`。
    qiaomu-meta-skill 门：在技能目录运行其 `validate_skill.py` 与 `trigger_eval.py`（若本机可用），结果存任务 `research/`。
11. 人工证据：FerroStage 打开 Touying `defense-notes.pdf` 截图，存任务 `research/`。
12. trellis-check；提交：`feat(academic-defense-beamer): 新增 Typst Touying 后端与 notes:N 备注版`。
13. 回到父任务执行集成复核。

## 回滚点

- 步骤 2–5 各自独立可回退；Beamer 路径的测试在每步后都要保持绿色。
- 提交后 `git revert` 只移除 Touying 能力，子任务 1、2 不受影响。

## 审查门

- `git diff` 中不得出现 simply-ysu-touying 源码或 `ysu-*` 位图的副本。
- 生成的 `defense.typ` 中不得出现规划文本直接进入标记模式（注入测试守护）。
- SKILL.md 正文行数增加不超过约 40 行；细节进 `references/`。
