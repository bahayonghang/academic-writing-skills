# verification — 08-10-nature-writing-zh

## D-ZH-1：B-NAT 行为

- `analyze_abstract.py --bilingual` 仅在 `english_found=true` 时追加一条 `B-NAT`。
- 输出固定为 `level=Info`、`source=[LLM]`、`flagged=false`、
  `ref=nature-writing N3`；脚本不执行词面匹配，也不作通过/失败判定。
- 正例 CLI：含英文摘要时，JSON 中 `english_found=true`、`B-NAT` 数量为 1，三条“可能”
  候选提示均存在。
- 反例 CLI：无英文摘要时，JSON 中 `english_found=false`、`B-NAT` 数量为 0；原有
  `B-LEN.flagged=true` 保持不变。
- 回归测试：`test_bilingual_nature_prompt_is_llm_lane` 与
  `test_bilingual_nature_prompt_requires_english_abstract`。

## D-ZH-2：结论局限组织

`conclusion-guide-zh.md` 已新增“局限的两类与陈述顺序”：

- 区分范围局限与技术缺陷；
- 局限段优先按数据范围、成立假设和部署场景组织；
- 明确该指导只管理陈述顺序，不是选择性披露规则；
- 明确关键指标落后强基线、安全性或有效性方面不可接受的权衡必须如实陈述；
- 交叉引用 `over-claim-guard.md`，并保留社区归纳来源、来源证据限制和非官方规则声明。

未新增或修改 CC-* 检查项，`analyze_conclusion.py` 未改。

## D-ZH-3：已覆盖，不改正文

`results-analysis-guide-zh.md` 已提供适配学位论文结果章的等价指导，因此本任务不重复加节：

- §二“按两条八步链组织论证”依次覆盖比较协议、主结果、图表定位、机制解释、组件记录与
  后续实验接口；生成或增强场景另有对应八步链。
- §五要求每张图表先确定主要结论，导语优先点出该结论，等价覆盖 claim-first 小节开头。
- §七单独定义五级证据阶梯并限制解释强度；它管理证据强度，不替代 §二、§五的叙事顺序。

## 验证结果

- `uv run --extra dev python -m pytest tests/skills/latex_thesis_zh/test_abstract_thesis_mode.py -q`
  → `47 passed`。
- `uv run --extra dev python -m pytest tests/skills/ tests/contracts/ -q -k "abstract or bilingual or resources"`
  → `115 passed, 1292 deselected`。
- `uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh`
  → `resource contract passed`，manifest 共 258 条。
- `uv run python docs/scripts/check_resource_sync.py`
  → 全量 258 条资源通过。
- `just doc-build` → VitePress 构建成功。
- `just ci` → Ruff 通过；Pyright `0 errors, 72 warnings`；pytest `1499 passed`。
- `git diff --check` → 通过。

`SKILL.md` 的 `last_updated` 已为当前日期 `2026-08-10`，因此未制造无语义改动；`version`
保持 `6.0.0`。

## 证据边界

- 未运行 provider-backed 评估：`UNVERIFIED / missing evidence`。
- 合成正反例只证明门控、字段和提示内容符合契约，不证明真实论文上的查准率或召回率；真实论文
  效果仍为 `UNVERIFIED / missing evidence`。
