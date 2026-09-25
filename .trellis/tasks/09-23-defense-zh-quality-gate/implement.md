# C3 执行计划

## Entry

前置：C2 已通过质量门并有 `research/c2-evidence.md`；用户明确授权 C3；本子任务已 `task.py start`。
读取顺序：`implement.jsonl` → 本 `prd.md` → `design.md` → 父 `design.md` §3、§4、§7 → C1 `references/slide-layouts.md`、
`references/content-rules.md`、`references/time-budget.md` → C2 `references/plan-schema.md` 与 `tests/skills/latex_defense_zh/conftest.py`。
文件边界：只新增或修改 design §1 所列文件。需要改 C1、C2 文件时停下上报。

## Steps

1. 写 `check_deck.py` 的输入层（参数、帧切分、帧标记解析、可见文本、论文全文组装）与输出层（文本行、`--json`、退出码），
   先用基线稿跑通「零结果」路径。
2. 按 design §3 逐码实现判据，每实现一个码就在 `test_defense_check.py` 加该码的正例与反例；顺序：
   D-MARKER → D-COVERAGE → D-TOC → D-CHAIN → D-PLACEHOLDER → D-FIG-ALLOW → D-FIG-MISSING → D-FIG-NUMBER → D-FIG-ASPECT →
   D-EQ-SRC → D-TAB-SRC → D-NUM-SRC → D-PAPER → D-META → D-STAGE → D-DENSITY → D-BUDGET → D-NOTES → D-COMPILE →
   D-OVERFLOW-V → D-OVERFLOW-H。
3. 加父 AC8 三个 `test_parent_ac8_*` 用例、输出契约用例、只读用例。
4. 写 `render_preview.py` 与 `test_defense_preview.py`。
5. 写 `references/quality-gate.md`（design §6），再写 zh/en 资源页并重建 manifest。
6. 手工运行（scratchpad）：C2 端到端产物 → check（文本与 `--json`）→ preview（本机有 PyMuPDF 时）；
   记录命令、退出码、各严重度计数到本任务 `research/c3-evidence.md`。
7. 执行质量门命令；全部通过后停止，等待 C4 授权。

## Commands

```bash
rtk proxy uv run --extra dev python -m pytest -q tests/skills/latex_defense_zh
rtk proxy uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
rtk proxy uv run python docs/scripts/check_resource_sync.py --skill latex-defense-zh
rtk proxy just ci
rtk proxy just doc-build
```

手工运行（`$SKILL_DIR`、`$WORK` 同 C2 implement）：

```bash
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck $WORK/deck/defense.tex --inventory $WORK/inventory.json --plan $WORK/slide_plan.yaml
uv run python -B $SKILL_DIR/scripts/check_deck.py --deck $WORK/deck/defense.tex --inventory $WORK/inventory.json --json
uv run python -B $SKILL_DIR/scripts/render_preview.py --pdf $WORK/deck/defense.pdf --out $WORK/deck/preview
```

## Review gate

- 21 个码在 design §3、`quality-gate.md` 与测试中一一对应（测试以码名参数化，集合断言相等）。
- check 与 preview 不写 `--out` 以外的路径；基线目录哈希不变。
- 阈值在 `quality-gate.md` 标注「初始值，未标定」；不以私有论文调阈值。
- `git status --porcelain` 只列出 design §1 文件与 `research/c3-evidence.md`。

## Rollback

删除 design §1 的新增文件（含两份 quality-gate 资源页），再运行 `--write-manifest --inventory-only` 重建 manifest，即回到 C2 完成状态。
本计划不授权 commit、archive 或 push。
