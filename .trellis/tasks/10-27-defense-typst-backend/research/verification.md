# 验证记录（2026-11-01）

提交：`70118f1 feat(academic-defense-beamer): 新增 Typst Touying 后端与 notes:N 备注版`

- `just ci`：通过（2933 passed, 25 skipped）。
- `uv run python docs/scripts/check_resource_sync.py`：通过（308 项）。
- `DEFENSE_TYPST_COMPILE=1 uv run --with pymupdf pytest tests/skills/academic_defense_beamer`：251 passed, 5 skipped（Beamer XeLaTeX 编译测试需 `DEFENSE_COMPILE=1`，本机无 latexmk/xelatex）。
- 环境：Typst 0.15.1；`@preview/simply-ysu-touying:0.2.0`、`@preview/touying:0.8.0`、`@preview/mitex:0.2.6` 本机已缓存。
- fixture Touying 构建（40 min, predefense, yanshan）：54 帧；`defense.pdf` 54 页；`defense-notes.pdf` 108 页，`N` / `notes:N` 交替；check_deck 全部零结果，D-OVERFLOW-H 在 `skipped`。
- 人为加 30 条要点：D-OVERFLOW-V 在该帧标记行报 Major。
- trellis-check 修复 4 项：Touying 的 D-FIG-MISSING 提示、check 阶段 `typst eval` 前补查 touying 包（防下载）、`deck` 非映射时报错、quality-gate 与 spec 补缺图不对称说明。
- 触发评测：仓库内无运行器；`tests/contracts/test_trigger_evals.py` 通过。qiaomu-meta 的 validate/trigger 输出见同目录，结构不适用本仓库。

## UNVERIFIED

- FerroStage 打开 Touying `defense-notes.pdf`、演讲者窗口显示备注：需人工操作，未执行。
- 仓库 fixture 不含图片文件，直接用它跑 Touying 构建会退出 2（缺图）；测试用自建图片覆盖。
