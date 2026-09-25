# C2 执行计划

## Entry

前置：C1 已通过质量门并有 `research/c1-evidence.md`；用户明确授权 C2；本子任务已 `task.py start`。
读取顺序：`implement.jsonl` → 本 `prd.md` → `design.md` → 父 `design.md` §3–§5、§7 → C1 `references/slide-layouts.md`、
`references/time-budget.md` 与 `templates/beamer/defense-layouts.sty` 的宏签名。
文件边界：只新增或修改 design §1 所列文件。需要改 C1 文件时停下上报。

## Steps

1. 复制 `academic-writing-skills/latex-thesis-zh/scripts/tex_loader.py` 到本技能 `scripts/`，只改模块 docstring 中的技能名；
   用 `diff` 确认其余行一致。
2. 写 `defense_budget.py` 与 `test_defense_budget.py`；先让 C1 time-budget 三档与两种结构的参数化用例通过。
3. 写 fixture `evals/fixtures/mini-thesis/`（design §7）；在 scratchpad 人工检查 fixture 无真实论文内容。
4. 写 `extract_thesis.py` 与 `test_defense_extract.py`（C2 AC1、AC2、文件哈希不变、`W-FIG-FILE`）。
5. 写 `plan_deck.py` 与 `test_defense_plan.py`（区间、研究章下限、帧 id 唯一、`--outline`）。
6. 写 Jinja2 模板与 `build_deck.py`、`test_defense_build.py`（帧标记序列、转义、公式与表体还原、路径、退出码、`--force`、编译）。
7. 写 `references/plan-schema.md`：清单与规划全部字段、占位符、转义规则、公式与表体变换规则、`extra_packages`、已知限制；
   再写 zh/en 资源页并重建 manifest（父 design §7）。
8. 端到端手工运行（scratchpad）：fixture → extract → plan → 用脚本把占位符替换为合成文本 → build --compile → 目视 PDF；
   把命令、退出码、帧数与 PDF 页数写入本任务 `research/c2-evidence.md`。
9. 执行质量门命令；全部通过后停止，等待 C3 授权。

## Commands

```bash
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
DEFENSE_ZH_COMPILE=1 rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
rtk proxy uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
rtk proxy uv run python docs/scripts/check_resource_sync.py --skill latex-defense-zh
rtk proxy just ci
rtk proxy just doc-build
```

端到端（`$SKILL_DIR` = 本技能目录，`$WORK` = scratchpad 下的工作目录）：

```bash
uv run python -B $SKILL_DIR/scripts/extract_thesis.py --thesis $WORK/mini-thesis --out $WORK/inventory.json --json
uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory $WORK/inventory.json --out $WORK/slide_plan.yaml
uv run python -B $SKILL_DIR/scripts/plan_deck.py --plan $WORK/slide_plan.yaml --outline
uv run python -B $SKILL_DIR/scripts/build_deck.py --plan $WORK/slide_plan.yaml --inventory $WORK/inventory.json --out $WORK/deck --compile
```

## Review gate

- `tex_loader.py` 与 latex-thesis-zh 副本只差 docstring 技能名。
- 测试不依赖本机字体以外的私有资源；编译用例在无 xelatex 或未设 `DEFENSE_ZH_COMPILE=1` 时 skip。
- `git status --porcelain` 只列出 design §1 文件与 `research/c2-evidence.md`；论文仓库类路径不出现在任何新文件中。
- 模板只调用父 design §5 的宏；grep 核对 `templates/jinja/` 中无 `\newcommand`、`\def` 定义。

## Rollback

删除 design §1 的新增文件（含两份 plan-schema 资源页），再运行 `--write-manifest --inventory-only` 重建 manifest，即回到 C1 完成状态。
不用 `git checkout` 还原 manifest：C1 改动未提交时该命令会一并撤销 C1 的登记。
本计划不授权 commit、archive 或 push。
