# 父任务执行计划（集成与验收）

父任务本身不写产品代码。它负责子任务顺序、每个子任务进入前的检查与最终集成复审。

## 顺序

1. C1 `10-15-defense-zh-rebuttal-intake`：用户授权后 `task.py start`，按 C1 `implement.md` 执行，C1 质量门通过后停下报告。
2. C2 `10-15-defense-zh-rebuttal-response`：前置 C1 已通过（`rebuttal_common.py` 与 intake 产物格式已定）。
3. C3 `10-15-defense-zh-rebuttal-docs`：前置 C2 已通过（三个脚本的 `--help` 已定）。

子任务之间不并行：C2 依赖 `rebuttal_common.py` 与台账格式，C3 依赖三个脚本的 CLI。

## 进入每个子任务前

- `git status --short` 只含已完成子任务的改动与本任务树文件。
- 读取顺序：子任务 `implement.jsonl` → 子任务 `prd.md` → 父 `design.md` 对应节 → 子任务 `design.md` → 子任务 `implement.md`。
- 父 `design.md` 的契约需要改动时，停下回到规划阶段，不在子任务中私改。

## 集成复审（C3 完成后）

```bash
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
rtk proxy uv run --extra dev python -m pytest -q tests/contracts
rtk proxy uv run python docs/scripts/check_resource_sync.py
rtk proxy just ci
rtk proxy just doc-build
```

逐条核对父 `prd.md` AC1–AC10；AC9 证据在 C3 `research/acceptance-real-reviews.md`；AC10 用本地未入库的词表运行 `git grep -n -F -f <词表>`，结果为空。

## Review gate

- 改动文件只在三个子任务 design 列出的范围内。
- `academic-writing-skills/latex-defense-zh/evals/fixtures/mini-thesis/` 无改动。
- 五个原有脚本（`extract_thesis.py`、`plan_deck.py`、`build_deck.py`、`check_deck.py`、`render_preview.py`）无改动；
  `tex_loader.py` 无改动（`tests/contracts/test_tex_loader_alignment.py` 锁定）。

## Rollback

按子任务逆序回滚（C3 → C2 → C1），各子任务 `implement.md` 给出具体步骤。本计划不授权 commit、archive 或 push。
