# implement — 盲审匿名化检查与盲审版tex生成

> 前置：07-08-spec-final-check 已完成（yanshan.md 已重写、SKILL.md 已有 spec-check 行）。
> 已读 testing-and-tooling.md（importlib 加载、tests.support.paths、evals.json Bash 写入、
> SKILL.md 表格 hook 陷阱）。

## 步骤

1. **fixture 扩充**：`evals/fixtures/thesis-project/` 加 `chapters/acknowledgement.tex`、
   `chapters/achievements.tex`（design §5 埋点 + `% seed:` 注释），main.tex 加
   `\author{测试作者}` 与 `\input` 两行 → verify:
   `uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/ -q`（存量 + spec-check
   测试不受级联影响；wordcount 类阈值断言若受影响，修 fixture 埋点而不是放松断言）。
2. **新增 `scripts/blind_review.py`**（FIELD_PATTERNS 按模板分表、check findings、
   generate 副本流水线、--dry-run/--force、原文件哈希确认行）→ verify:
   对 fixture 跑 `--check`（检出全部埋点）、`--generate`（副本生成 + 原文件
   `git status` 无改动）、`--dry-run`（`git status` 全程干净）。
3. **新增 `references/modules/blind-review.md`**（R1/R2 逐字规则 + R3 标注 + 工作流 +
   R2 改写前后示例 + 输出契约）。
4. **`templates/yanshan.md`**：填充 `## 盲审` 节（R1/R2 原文、示例
   `[1]第一作者，机械工程学报，2024`、指向模块文档）→ verify:
   `tests/contracts/test_spec_checklists.py` 仍绿（清单段未被破坏）。
5. **SKILL.md**：router 行 + 路由规则 + Example + Safety Boundaries 补句 +
   `last_updated` → verify: `uv run --extra dev python -m pytest tests/contracts/test_skill_contracts.py -q`。
6. **trigger evals**：Bash python 追加正例（"帮我生成盲审版论文，隐去我和导师的名字" 等）
   → verify: `tests/contracts/test_trigger_evals.py`。
7. **新增 `tests/skills/latex_thesis_zh/test_blind_review.py`**（design §5 全部用例，
   含加载守卫）→ verify: 该文件 pytest 全绿。
8. **全量回归** → verify: `just ci` 全绿。

## 回滚点

- fixture 扩充（步骤 1）与脚本（步骤 2）可独立回退；若 fixture 级联破坏存量断言且当轮修不完，
  回退步骤 1 改用独立最小 fixture 目录（`evals/fixtures/blind-review-project/`）再继续。

## 审查门

- R1/R2 文本与用户提供原文逐字一致（不"润色"校方通知）。
- 副本中 `\cite`/`\ref`/`\label`/math 与原文逐字 diff 为空（测试断言）。
- 所有输出行带 `[Script]`/`[LLM]` 与 severity。
