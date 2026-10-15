# C1 执行计划

## Entry

前置：用户明确授权实施 C1；本子任务已 `task.py start`。
读取顺序：`implement.jsonl` → 本 `prd.md` → 父 `design.md` §1–§4、§6、§8–§10 → 本 `design.md`。
文件边界：本 `design.md` §1 所列文件。其他路径的改动先停下上报。

## Steps

1. 写合成 fixture `评阅书1.txt`、`评阅书2.txt`（用 Write 落盘，避免 heredoc 反斜杠问题）。
2. 写 `rebuttal_common.py`：`load_aux_labels`、`load_bibcites`、`find_anchors`、台账读写、`emit`、`git_changed_files`。
3. 写 `rebuttal_intake.py`：参数 → 目录校验 → 读取与归一化 → 评分 → 编号切分 → 锚点映射 → 写 reviews、state、台账 → 输出。
4. 改 `conftest.py`（`_SHARED_MODULE_NAMES`、`rebuttal_thesis` fixture）。
5. 写 `test_defense_rebuttal_intake.py`（design §3），逐个运行。
6. 在 scratchpad 目录手工运行一次 intake（fixture 评阅书 + mini-thesis 副本），目视 `reviews/R1.md` 与 `concerns.yaml`。
7. 质量门命令全部通过后停下报告；不 commit、不 archive。

## Commands

```bash
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh/test_defense_rebuttal_intake.py
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
rtk proxy uv run --extra dev python -m pytest -q tests/contracts/test_tex_loader_alignment.py
rtk proxy just lint
rtk proxy just typecheck
uv run python -B academic-writing-skills/latex-defense-zh/scripts/rebuttal_intake.py --help
```

Windows 下把 `--json` 输出重定向到文件时，只对该条命令设置 `PYTHONIOENCODING=utf-8`，不全局 export。

## Review gate

- `git status --short` 只含 design §1 所列文件。
- `tex_loader.py`、`extract_thesis.py`、`mini-thesis/` 无 diff。
- fixture 中无真实姓名、学号、题目与评阅编号。

## Rollback

删除 design §1 新增的五个文件；撤销 `conftest.py` 中 `_SHARED_MODULE_NAMES` 追加项与 `rebuttal_thesis` fixture。本计划不授权 commit、archive 或 push。
