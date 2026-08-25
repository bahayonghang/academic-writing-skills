# 设计：语义中间产物与 finding schema

## 改造前基线

当前 analyzer 只打印人类可读 `% MODULE (L##)` 行，没有稳定 finding id、
`root_cause_key` 或 artifact 引用。paper-audit 的
`academic-writing-skills/paper-audit/references/ISSUE_SCHEMA.md` 是投稿审稿
schema，字段集合与本 skill 需求不等（TPR-07）。

## 变更清单

| 文件 | 变更 |
| --- | --- |
| `academic-writing-skills/latex-thesis-zh/references/schemas/artifacts.md` | 新增 canonical schema 与 paper-audit 映射表 |
| `academic-writing-skills/latex-thesis-zh/scripts/artifacts.py` | schema 校验、稳定 ID、合并、JSON/JSONL IO |
| `academic-writing-skills/latex-thesis-zh/references/workflow/evidence-intake.md` | preflight / source-priority / generated_artifacts schema |
| `academic-writing-skills/latex-thesis-zh/scripts/analyze_logic.py` | 机器 JSON 旁路输出 artifact refs；人类可读行不变 |
| `academic-writing-skills/latex-thesis-zh/scripts/analyze_literature.py` | 同上 |
| `academic-writing-skills/latex-thesis-zh/scripts/analyze_experiment.py` | 同上 |
| `academic-writing-skills/latex-thesis-zh/references/modules/{logic,literature,experiment}.md` | 指向 schema |
| `tests/skills/latex_thesis_zh/test_artifacts.py` | 新增 |
| docs 镜像 + manifest | 本提交内重建 |

## Canonical finding（TPR-07）

真源：`references/schemas/artifacts.md`。采用共享核心 + 扩展，测试不断言与
paper-audit 字段集合相等。

共享核心：`id` `title` `module` `severity` `confidence` `source_kind`
`source_span` `quote` `root_cause_key` `missing_evidence` `gate_blocker`。

本 skill 扩展：`artifact_refs` `evidence_status` `allowed_action`。

`source_kind=human` 仅用于作者笔记导入；脚本与默认 LLM 路径不得写出。

### paper-audit 映射

| paper-audit | 本 skill |
| --- | --- |
| title, quote, severity, confidence, source_kind, root_cause_key, missing_evidence, gate_blocker | 共享核心（severity 机器层用 major\|moderate\|minor，人类可读行仍用 Major/Minor/Info） |
| claim_strength, evidence_anchor | 不在 finding 上独立拥有；见下一节 |
| explanation, comment_type, source_section, related_sections, quote_verified | 不采用 |
| allowed_wording, forbidden_wording | 只在 claim-evidence |
| review_lane, round_scores | 禁止 |

### 字段所有权

- `claim-evidence.json` 拥有 `claim_strength`、`evidence_anchor`、
  `allowed_wording`、`forbidden_wording`、`causal_eligibility`。
- finding 通过 `artifact_refs` 指向 claim 节点。只读快照字段名为
  `claim_snapshot`，形状 `{claim_id, claim_strength, evidence_anchor}`。
- 快照强度 ≤ claim-evidence 强度。finding 顶层不得出现可写
  `claim_strength` / `evidence_anchor`。schema 测试断言这两键不在 finding
  顶层 required/optional 列表中。
- 无 claim 节点：`evidence_status=missing evidence`，
  `claim_snapshot={claim_id: null, claim_strength: unsupported, evidence_anchor: []}`。
- `causal_eligibility` 只存在于 claim-evidence，与 strength 分栏。

稳定 `id`：`F-{root_cause_key}-{source_span.file}-{source_span.start}` 的
blake2s 截断，同一输入重复构建结果相同。

根因合并：`root_cause_key + 归一化 source span` 相同则合并，保留全部 span 与
不同 `allowed_action`。

## 四张 map

按请求最小生成。CLI：`--artifacts thesis,claim-evidence` 只建列出的 map。
空目录不创建。每条 edge/claim 必须带 `source_anchor` 与
`status=validated|inferred|missing evidence`。

生成工件声明（YAML 片段，供 IR `generated_from` 消费）由 evidence-intake 定义；
本任务只定 schema，不内置真实项目 adapter。

整文件级「最高权威」在 schema 校验阶段拒绝。

## 兼容

严格不变面：三个 analyzer 无 `--json` 时的人类可读 stdout、CLI 命令与 flag。
已批准差异：新增可选 `--json` / `--artifacts` 开关；默认关闭。

## 验证边界

自动化：schema 字段测试、合并、ledger 拒绝整文件权威、人类可读快照、C1/C7
不在本任务改动面但仍跑 contracts。
不自动化：LLM map 事实正确率（missing evidence）。

## 回滚

删除新增 schema/脚本/测试；`git restore` 三个 analyzer 与三份 module md。
不触及父任务 dirt 冻结清单。

## 已考虑不做

- 严格复用 paper-audit ISSUE_SCHEMA：字段集合不相等，且含投稿评分通道。
- 版本化双向转换器：本轮无跨 skill 读写 paper-audit bundle 的需求。
- 为每张 map 单独脚本：IO 重复，违反 R3。
