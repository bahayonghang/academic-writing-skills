# eval runner 与断言类型核实

对应 `implement.md` 步骤 1。核实日期 2026-09-06。
目的：在写新断言之前确认否定断言是否可用，以及本仓库对 eval 条目的硬性形状约束。

## 结论先行

否定断言可用，类型名是 `not_contains`。因此
`evals.json` 的新用例可以直接断言"输出中不出现模式选择措辞"与"不出现 `review_results`"，
无需退化成"断言正向陈述串"的备选写法（该备选写法在 `design.md` 中已预留，本次未启用）。

## 本仓库不执行断言

仓库内没有任何脚本把 `assertions` 跑在模型输出上。
`evals.json` 是一份**语料**，由外部 skill-creator 侧的评测流程消费；
`trigger_eval.json` 的消费者是 skill-creator 的 `run_loop.py`，
需要 `ANTHROPIC_API_KEY` 且消耗 token，明确不进 `just ci`
（见 `tests/contracts/test_trigger_evals.py` 模块 docstring）。

因此 `just ci` 对新用例的保证只到"形状与内容契约正确"，
**不包括**"断言在真实模型输出上通过"。后者是 missing evidence，已记入交付说明。

## 断言类型分布（实测）

全仓库六个 skill 的 `evals.json` 聚合统计：

| type | 出现次数 |
| --- | --- |
| `regex` | 298 |
| `contains` | 164 |
| `not_contains` | 50 |

统计方式：

```bash
uv run python -c "import json,glob,collections; c=collections.Counter(); [c.update([a['type'] for a in it.get('assertions',[])]) for p in glob.glob('academic-writing-skills/*/evals/evals.json') for it in json.load(open(p,encoding='utf-8'))['evals']]; print(dict(c))"
```

`not_contains` 不只是"恰好有人用过"，而是被契约测试点名要求：
`tests/contracts/test_skill_contracts.py:400` 与 `:407` 分别要求
paper-audit 的 eval 5（gate）与 eval 8（polish）至少含一条 `not_contains`。

## 硬性形状约束（会让 `just ci` 变红）

- 必填键：`{"id", "prompt", "expected_output", "files"}`
  —— `tests/contracts/test_skill_contracts.py:360`。
  注意 `assertions` **不在**这个必填集合里，但本任务 PRD AC2 自行要求了它。
- paper-audit 专属：**每一条** eval 的 `files` 必须非空，且每个路径必须真实存在
  —— `tests/contracts/test_skill_contracts.py:417` 起。
  这是新用例 24/25 复用 `evals/fixtures/quick_audit_fixture.tex` 的原因：
  两条新用例考的是门控与落盘行为，不需要新 fixture，但不能留空 `files`。
- `trigger_eval.json`：≥12 条 query、≥5 正例、≥5 负例、query 全局唯一、
  `category` 为非空字符串 —— `tests/contracts/test_trigger_evals.py:64` 起。
  改后实测 20 条 / 13 正 / 7 负，余量充足。

## 已知写入陷阱（复核确认）

用 Edit/Write 改 `evals.json` 会触发 JSON 格式化把内联数组压平。
本次两条新用例经 Bash 内 python 读—改—写，
`git diff` 显示 `evals.json` 仅 23 行纯新增、既有条目零 diff（AC3 通过）。
