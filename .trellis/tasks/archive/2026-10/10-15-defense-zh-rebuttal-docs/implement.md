# C3 执行计划

## Entry

前置：C2 质量门通过；用户明确授权实施 C3；本子任务已 `task.py start`。
读取顺序：`implement.jsonl` → 本 `prd.md` → 父 `design.md` §3–§8 → 本 `design.md` → 三个脚本的 `--help` 输出。
文件边界：本 `design.md` §1 与 §2 所列文件。其他路径的改动先停下上报。

## Steps

1. 运行三个脚本 `--help`，把输出与父 design §8 对照。
2. 写三份 references 与 example（用 Write 落盘）。
3. 改 SKILL.md（design §3）；本地计数 description 字符数；运行入口测试与 `test_skill_contracts.py`。
4. 用 Bash 下的 Python 脚本更新 `evals.json` 与 `trigger_eval.json`；运行 `test_trigger_evals.py`。
5. 改 `test_defense_skill_entry.py` 的 `MODULES`。
6. docs：双语资源页 → 重建 manifest → 双语技能页 → README、README_CN → CHANGELOG → `agents/openai.yaml`。
7. spec：新契约文件、索引行、`defense-deck-contract.md` 指引句。
8. 执行全部质量门命令。
9. AC9：询问用户评阅书目录与论文仓库，按 design §5 执行并写证据文件。
10. 停下报告；不 commit、不 archive。

## Commands

```bash
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
rtk proxy uv run --extra dev python -m pytest -q tests/contracts
rtk proxy uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
rtk proxy uv run python docs/scripts/check_resource_sync.py
rtk proxy just ci
rtk proxy just doc-build
```

AC9（`$REVIEWS`、`$THESIS` 由用户给出）：

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_intake.py --reviews $REVIEWS --thesis $THESIS --stage pre-review --json
```

## Review gate

- `git status --short` 只含 C1、C2 与本 design §1、§2 所列文件，以及本任务 `research/` 下证据文件。
- `docs/CHANGELOG.md` 只有新增条目。
- AC9 证据与全部公开文件不含真实姓名、学号、题目、评阅编号与正文。

## Rollback

逐处撤销 design §2 表中的改动（不用 `git checkout` 整文件还原，README 与 docs 页可能含其他改动）；删除 design §1 新增文件；
重新运行 `check_resource_sync.py --write-manifest --inventory-only` 重建 manifest，即回到 C2 完成状态。
AC9 在用户目录生成的 `responses/` 与 `workspace/` 由用户决定是否保留。本计划不授权 commit、archive 或 push。
