# C2 执行计划

## Entry

前置：C1 质量门通过；用户明确授权实施 C2；本子任务已 `task.py start`。
读取顺序：`implement.jsonl` → 本 `prd.md` → 父 `design.md` §3–§8、§10 → 本 `design.md` → C1 的 `rebuttal_common.py` 与 `rebuttal_intake.py --help`。
文件边界：本 `design.md` §1 所列文件。其他路径的改动先停下上报；需要改 `rebuttal_common.py` 时只追加函数，不改已有签名。

## Steps

1. 写 `concerns-done.yaml`（用 Write 落盘）。
2. 扩展 `conftest.py`：`rebuttal_case` fixture。
3. 写 `rebuttal_build.py`：校验 → `--plan-only` 分支 → 位置解析 → 渲染 → 手改保护 → 写文件与 state。
4. 写 `test_defense_rebuttal_build.py` 并通过。
5. 写 `rebuttal_check.py`：上下文装配 → 16 个检查函数 → 排序 → 输出与 `check.json`。
6. 写 `test_defense_rebuttal_check.py` 并通过。
7. 在 scratchpad 目录对 C1 fixture 跑一遍 intake → build `--plan-only` → build → check，目视 `response-all.md`。
8. 质量门命令全部通过后停下报告；不 commit、不 archive。

## Commands

```bash
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh/test_defense_rebuttal_build.py tests/skills/latex_defense_zh/test_defense_rebuttal_check.py
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
rtk proxy just lint
rtk proxy just typecheck
uv run python -B academic-writing-skills/latex-defense-zh/scripts/rebuttal_build.py --help
uv run python -B academic-writing-skills/latex-defense-zh/scripts/rebuttal_check.py --help
```

## Review gate

- `git status --short` 只含 C1 与本 design §1 所列文件。
- `check_deck.py`、`extract_thesis.py`、`tex_loader.py`、`mini-thesis/` 无 diff。
- 16 个 R-* 码在代码、测试与父 design §7 中名称一致（`grep -o "R-[A-Z-]*"` 三处集合相等）。

## Rollback

删除本 design §1 新增的五个文件；撤销 `conftest.py` 中 `rebuttal_case` fixture；撤销 `rebuttal_common.py` 中本子任务追加的函数。
即回到 C1 完成状态。本计划不授权 commit、archive 或 push。
