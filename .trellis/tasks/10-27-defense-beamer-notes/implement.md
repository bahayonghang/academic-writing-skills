# 执行计划：Beamer 备注版

前置：`10-27-defense-rename` 已提交。路径均相对 `academic-writing-skills/academic-defense-beamer/`。

## 步骤

1. Spike S1、S2（design.md 第 6 节）：在 scratchpad 用 fixture 手写一份带 `\note` 的最小 `defense.tex` 与包装文件，XeLaTeX 编译，
   用 PyMuPDF 读页尺寸与页标签、目视备注半页；结论写回 design.md 第 6 节后再继续。
2. `templates/beamer/defense-layouts.sty`：加 `\DefenseNote` 与备注页样式；同步 `references/slide-layouts.md` 宏一览。
3. `templates/jinja/frames/_note.tex.j2`、12 个帧模板、`deck.tex.j2` 的 second-screen 开关、`templates/jinja/defense-notes.tex.j2`。
4. `scripts/build_deck.py`：`frame.note` 准备与转义、`OWNED_FILES`、manifest 字段、`compile_deck` 双编译、`--no-notes-pdf`。
5. `scripts/check_deck.py`：D-NOTES 源级计数、D-NOTES-PDF、`--notes-pdf` 参数、码表 22 个。
6. 测试（`tests/skills/academic_defense_beamer/`）：
   - `test_defense_build.py`：每帧一个 `\DefenseNote`、转义、`defense-notes.tex` 内容、manifest 字段、`--no-notes-pdf`、自有文件 8 个、`--force` 保留未变文件 mtime。
   - `test_defense_check.py`：D-NOTES 源级正反例；D-NOTES-PDF 六个用例（用 PyMuPDF 生成合成 PDF，或用 `pytest.importorskip`）。
   - 编译用例（`DEFENSE_COMPILE=1`）：两份 PDF 页数相等、比例在带内。
   - 契约测试中自有文件数、D-* 码数量的断言。
7. 文档：`references/presenting.md`（新）、`speaker-notes.md`、`quality-gate.md`、`plan-schema.md`、`SKILL.md`、`examples/*.md`；
   双语技能页 `docs/skills/academic-defense-beamer/index.md` 与 `docs/zh/...` 加“放映与备注”一节；
   `uv run python docs/scripts/check_resource_sync.py --write-manifest`。
8. spec：`.trellis/spec/academic-writing-skills/defense-deck-contract.md` 第 2–6 节（签名、自有文件、D-* 22 码、错误矩阵、测试清单）。
9. `docs/CHANGELOG.md` `[Unreleased]` 加 Added 条目。
10. 验证：
    ```bash
    just ci
    uv run python docs/scripts/check_resource_sync.py
    ```
    有 XeLaTeX：`DEFENSE_COMPILE=1 uv run pytest tests/skills/academic_defense_beamer -k "compile or notes"`。
11. 人工证据：FerroStage 打开 fixture `defense-notes.pdf` 截图，存到任务 `research/`（不入公开 docs）。
12. trellis-check；提交：`feat(academic-defense-beamer): Beamer 答辩稿输出演讲备注版 PDF 并推荐 FerroStage 放映`。

## 回滚点

- 步骤 2–5 每步后跑对应单测；失败回退该步文件。
- 提交后 `git revert`；子任务 1 不受影响。

## 审查门

- `defense.pdf` 页数与改动前一致（编译用例断言）。
- 帧模板中仍无宏定义、帧标题后仍无花括号组（现有契约测试）。
