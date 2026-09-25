# C4 执行计划

## Entry

前置：C3 已通过质量门并有 `research/c3-evidence.md`；`09-23-pws-catalog-register` 已完成；用户明确授权 C4；本子任务已 `task.py start`。
读取顺序：`implement.jsonl` → 本 `prd.md` → `design.md` → 父 `design.md` §3、§7 → C1–C3 的 references 与 C2/C3 脚本 `--help`。
文件边界：design §1 新增文件与 §2 登记表所列文件。其他路径的改动先停下上报。

## Steps

1. 对五个脚本运行 `--help`，把输出与父 design §3 对照；Module Router 命令只写 `--help` 中存在的选项。
2. 写 SKILL.md（design §1.1）；本地核对 description 字符数在 120–400。
3. 写 examples 三份、`agents/openai.yaml`、`agents/qa-committee-agent.md`。
4. 用 Bash 下的 Python 脚本写 `evals/evals.json` 与 `evals/trigger_eval.json`（design §1.2）。
5. 写 `test_defense_skill_entry.py`（design §4）。
6. 按 design §2 逐行改登记点；每改一个测试文件就运行该文件。
7. docs：资源页（examples、agents Markdown）→ 重建 manifest → 技能总览页 → 索引页、首页、快速开始、usage、安装页 → config.ts 侧栏与描述 →
   README、README_CN → CHANGELOG。
8. spec：`defense-deck-contract.md`、spec 索引、`docs-bilingual-resources.md` 技能数。
9. 执行全部质量门命令；通过后做 AC5 人工扫描。
10. AC11：询问用户输出目录；按父 implement「AC11 流程」对真实论文仓库执行；三个检查点请用户确认；
    写 `research/acceptance-real-thesis.md`（design §5）。
11. 停止并向用户报告；不 commit、不 archive。

## Commands

```bash
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
rtk proxy uv run --extra dev python -m pytest -q tests/contracts
rtk proxy uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
rtk proxy uv run python docs/scripts/check_resource_sync.py
rtk proxy just skills-install --list
rtk proxy just ci
rtk proxy just doc-build
```

AC11（`$THESIS` 为用户给出的论文仓库，`$OUT` 为用户同意的输出目录或 scratchpad 目录）：

```bash
uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis $THESIS --out $OUT/inventory.json --json
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory $OUT/inventory.json --out $OUT/slide_plan.yaml --minutes 40 --stage predefense --theme yanshan
uv run python -B $SKILL_DIR/scripts/plan_deck.py --plan $OUT/slide_plan.yaml --outline
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan $OUT/slide_plan.yaml --inventory $OUT/inventory.json --out $OUT/deck --compile
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck $OUT/deck/defense.tex --inventory $OUT/inventory.json --plan $OUT/slide_plan.yaml
uv run python -B $SKILL_DIR/scripts/render_preview.py --pdf $OUT/deck/defense.pdf --out $OUT/deck/preview
```

## Review gate

- `git status --porcelain` 只含 design §1、§2 所列文件与本任务 `research/` 下证据文件。
- `git diff` 中 `docs/CHANGELOG.md` 只有新增条目；历史条目、harness 证据表与 `paper-writing-studio/` 无改动。
- AC11 证据不含论文题目、姓名、正文、数字与本机路径。

## Rollback

逐处撤销 design §2 表中的 C4 改动。不用 `git checkout` 整文件还原：`test_docs_bilingual_resources.py` 与两份安装页
同时含 C1 未提交的改动。删除 design §1 新增文件、技能总览页、examples/agents 资源页与 `defense-deck-contract.md`，
再运行 `--write-manifest --inventory-only` 重建 manifest，即回到 C3 完成状态。本计划不授权 commit、archive 或 push。
