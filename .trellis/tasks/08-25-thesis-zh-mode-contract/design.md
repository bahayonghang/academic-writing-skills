# 设计：mode 契约与受控改写账本

## 改造前基线

`academic-writing-skills/latex-thesis-zh/SKILL.md` Rewrite Contract 只覆盖
expression。`references/modules/routing-rules.md` 将其余模块列为纯诊断。
无 `diagnose / plan / revise / re-audit / gate` 正交维度。

## 变更清单

| 文件 | 变更 |
| --- | --- |
| `academic-writing-skills/latex-thesis-zh/references/workflow/mode-contract.md` | 优先级表 + destination 状态表 |
| `academic-writing-skills/latex-thesis-zh/references/workflow/controlled-rewrite.md` | 不变量与 ledger 字段 |
| `academic-writing-skills/latex-thesis-zh/scripts/thesis_workflow.py` | orchestrator |
| `academic-writing-skills/latex-thesis-zh/SKILL.md` | 增加 mode 指针；只改 last_updated + 精简段落 |
| `academic-writing-skills/latex-thesis-zh/references/modules/routing-rules.md` | module × mode 矩阵 |
| `academic-writing-skills/latex-thesis-zh/agents/openai.yaml` | default_prompt 先锁 mode |
| `tests/skills/latex_thesis_zh/test_mode_contract.py` | 六类 fixture |
| docs 镜像 + manifest | 本提交内重建 |

## 输入优先级（TPR-11）

从高到低，后者不得覆盖前者：

1. 显式 `--mode {diagnose,plan,revise,re-audit,gate}`
2. 源写授权：`--apply-source`（默认关）。无此 flag 即无源写授权
3. 报告路径：`--output PATH`。`PATH=-` 表示 stdout 为契约产物
4. 自然语言：`--goal` 或 prompt 含「优化」「润色」
5. 默认 `diagnose`

退出码：`0` 成功（含 diagnose/plan 降级摘要）；`2` 显式 revise 未授权；
`3` 缺必需输入；`1` 其它错误。

## 输出 destination 状态表（TPR-11）

先按输入优先级得到 `requested_mode`，再查本表。同一请求只走一行。

`--output` 三态：`PATH` = 普通路径；`-` = stdout 为契约产物；`none` = 未给
`--output`。`none` 时 stdout 只含短摘要与建议文件名，**不是**合同文件。

| requested_mode | `--apply-source` | `--output` | 生效 mode | 文件产物 | stdout | 退出码 |
| --- | --- | --- | --- | --- | --- | --- |
| diagnose | 忽略 | PATH | diagnose | `final-findings.json` + 人类摘要 | 短摘要（非合同） | 0 |
| diagnose | 忽略 | `-` | diagnose | 无 | 合同 JSON+摘要 | 0 |
| diagnose | 忽略 | none | diagnose | 无 | 摘要 + 建议文件名 | 0 |
| plan | 忽略 | PATH | plan | thesis/section map + blueprint | 短摘要（非合同） | 0 |
| plan | 忽略 | `-` | plan | 无 | 合同 map+blueprint | 0 |
| plan | 忽略 | none | plan | 无 | 摘要 + 建议文件名 | 0 |
| 显式 `--mode revise` | 无 | 任意 | 阻断 | 无 source patch | 未授权说明 | 2 |
| 自然语言「优化/润色」 | 无 | 与 plan 同行 | plan（降级） | 与 plan 同行 | 与 plan 同行 | 0 |
| 自然语言「优化/润色」 | 有 | 与显式 revise 同行 | revise dry-run | 与显式 revise 同行 | 与显式 revise 同行 | 0 |
| 显式 `--mode revise` | 有 | PATH | revise dry-run | unified diff + `revision-ledger.jsonl` | 短摘要（非合同） | 0 |
| 显式 `--mode revise` | 有 | `-` | revise dry-run | 无 | 合同 diff+ledger | 0 |
| 显式 `--mode revise` | 有 | none | revise dry-run | 无 | 摘要 + 建议文件名；不把 ledger/diff 当作合同 stdout | 0 |
| re-audit | 忽略 | PATH | re-audit | `re-audit.json` / `.md` | 短摘要（非合同） | 0 |
| re-audit | 忽略 | `-` | re-audit | 无 | 合同 JSON | 0 |
| re-audit | 忽略 | none | re-audit | 无 | 摘要 + 建议文件名 | 0 |
| gate | 忽略 | PATH | gate | 有界 verdict 文件 | 短摘要（非合同） | 0 |
| gate | 忽略 | `-` | gate | 无 | 合同 verdict | 0 |
| gate | 忽略 | none | gate | 无 | 摘要 + 建议文件名 | 0 |

不得把摘要写入源文件。无报告路径不得扩大源写权限。`--apply-source` 本任务
仍只写到副本/diff，不对真实论文写。

六类 fixture：

1. 显式 `--mode diagnose|plan|revise`
2. 自然语言「优化/润色」且无 `--apply-source` → plan、退出码 0
3. 无 `--output` → 摘要 + 建议文件名，stdout 非合同
4. 无 `--apply-source` 的显式 revise → 退出码 2
5. 自然语言「优化/润色」且有 `--apply-source` → revise dry-run
6. `--output -` → stdout 为契约产物，不写源文件

## Orchestrator 合同

```text
uv run python scripts/thesis_workflow.py ENTRY [--mode MODE]
  [--output PATH] [--apply-source] [--goal TEXT] [--strength S] [--tier T]
  [--module MODULE]
```

旧 analyzer CLI 仍可独立运行（严格不变面）。`--strength` 与 `--tier` 词表不合并。
revise 默认 dry-run；`--apply-source` 本任务仍只写到副本/diff，不对真实论文写。

Ledger 字段按 PRD R5。fidelity gate 在写出 diff 前检查 protected/numeric
multiset、claim strength 非升级、source hash、generated owner。

## 兼容

严格不变面：既有 analyzer 独立 CLI。
已批准差异：新入口 `thesis_workflow.py`；routing-rules 从「纯诊断」改为矩阵。

## 验证边界

自动化：六类 fixture、退出码、零 source patch、ledger 字段、NEEDS-LLM、
openai.yaml 四键、C3。
不自动化：真实论文写入（禁止）；人类对 blueprint 的可用性。

## 回滚

删除新增 workflow 文档与 `thesis_workflow.py`；`git restore` SKILL.md、
routing-rules.md、openai.yaml。不触及 dirt 冻结清单。

## 已考虑不做

- 把 stdout 一律当作合同产物：与「无路径则只返摘要」冲突。
- 显式 `--mode revise` 未授权时静默降级为 plan：权限语义被自然语言路径吞掉。
- 有源写授权且无 `--output` 时把 ledger/diff 整份打到 stdout 当合同：与
  「只有 `--output -` 时 stdout 才是契约产物」冲突。
- 新增 module 代替 mode：与既有三轴词汇冲突。
