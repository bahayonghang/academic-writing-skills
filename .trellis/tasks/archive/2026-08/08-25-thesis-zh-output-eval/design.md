# 设计：output eval 升级与 E1-E9 fixture

## 改造前基线

`evals.json` 31 个 case，键集以 `{id, prompt, expected_output, files}` 为主，
可在 skill 仍错选章节、假阳性时全绿。手册 E1 症状在本仓库不成立。

## 变更清单

| 文件 | 变更 |
| --- | --- |
| `academic-writing-skills/latex-thesis-zh/evals/evals.json` | 加字段；旧 case 标 `legacy-trigger-only`；用 python 写入 |
| `academic-writing-skills/latex-thesis-zh/scripts/run_output_evals.py` | 确定性 runner |
| `academic-writing-skills/latex-thesis-zh/evals/fixtures/quality-regressions/` | E1-E9 |
| `academic-writing-skills/latex-thesis-zh/evals/output-evidence/` | 执行落点（可提交小型 golden） |
| `tests/skills/latex_thesis_zh/test_output_evals.py` | 读落点，禁止纯形状自证 |
| docs 镜像 + manifest | 本提交内重建 |

## Runner 合同（TPR-09）

```text
uv run python scripts/run_output_evals.py --case E1 [--write-evidence]
```

- `command` 必须是 argv 列表，指向本仓库脚本，禁止 shell 字符串。
- 捕获 stdout/stderr/exit_code。
- 写入 `evals/output-evidence/<case-id>/meta.json`：
  `{command, cwd, exit_code, skill_last_updated, ir_version, captured_at,
  stdout_rel, stderr_rel, annotation_version, denominator}`。
- 测试读取 meta.json 与 raw 文件，对照结构/保源/证据强度/假阳性合同。
- 禁止：`assert "baseline_output" in case` 作为 AC4 的充分条件。
- 禁止：把预填 `with_skill_output.text` 当作唯一 oracle。

`recorded_fixture` 证明失败可重放。`deterministic_run` 证明本次捕获满足合同。
`provider_backed` / `human_blind_review` 字段可存在，`evidence_status` 必须是
`missing evidence`。

## E1-E9（TPR-09）

每例由 runner 实际执行 `command` argv，把 raw 输出写入
`evals/output-evidence/<id>/`。测试读取该落点对照下表「确定性断言」。
`human_notes.status` 与 `provider_backed` 必须为 `missing evidence`。
无标注文件时 E1-E3 的 TP/FP/FN 只写分母字段与 `evidence_status=missing evidence`，
不得预填达成值，也不得单靠该字段让 case 通过。

| ID | command 入口 | fixture 要点 | 确定性断言 | 本轮 missing evidence |
| --- | --- | --- | --- | --- |
| E1 | `deai_check.py --analyze` | `\clearpage`、跨行 `equation` 的 `\text{}`、`tabular` 内 7 次「首先」、两个自然段 | 表/公式 span 零 `term_threshold`；自然段可触发；caption 只进 caption 通道 | 手册 E1 原文症状；人工美感 |
| E2 | `analyze_logic.py --process-chapter` | 与子任务 1 B1 同构：符号表→绪论→工艺章→方法章→成果章，无 `\mainmatter` | 两步选择器唯一命中工艺章；去掉双信号后要求 `--section`；符号表/成果章零主线 finding | 把全部 body 当过程章 |
| E3 | `analyze_logic.py --motivation-thread` | 绪论 itemize/表格声明问题与贡献，后文自然段回应 | 承诺数、回应数、source span 与金标一致；control 不计数 | 表头是否误当承诺 |
| E4 | `analyze_literature.py` + `--artifacts thesis` | 脱敏的方法枚举/无叙事主语/段末无台阶结构 | 每段 role 字段存在；citation-key multiset 相等；不得新增文献 | 主题递进 1-5 分 |
| E5 | `--artifacts interface` | 章内 P-* 可通过，下游字段物理语义冲突、一处缺权限证据 | 冲突两条 source anchor；章内静默与接口 gate 分栏；`no_script_finding` ≠ `pass` | 物理语义人工分 |
| E6 | `analyze_experiment.py` + claim-evidence | 保留「消融实验/消融设置」、不等预算点估计 | 术语存在；无单组件净效应与「证明」类因果；数字与 cite/ref/label multiset 不变 | 是否正面回答实验问题 |
| E7 | evidence-intake + `thesis_workflow.py --mode revise` | 正文表、派生 TeX、CSV、generator；旧附录与权威正文冲突 | 派生值有 owner；手改 generated 被阻断；默认 dry-run | 是否需要重跑实验 |
| E8 | source-priority ledger | 报告/图片/作者校正/论文接口对同一概念给不同范围 | claim 粒度 authority；展示路径无写权限；未核实字段 missing evidence | 来源可解释性 |
| E9 | `re_audit.py` | 旧 finding、只换连接词、真正补接口、新增回归 | 覆盖 `unresolved`/`addressed`/`new` 或 `regressed`；quote 变仍匹配；hash mismatch 不写源 | 作者能否决定下一步 |

全部 fixture 脱敏，零项目专有事实。E4-E8 的 map 事实正确率保持
**missing evidence**（子任务 2 AC11）；本子任务只验结构、保源、权限与假阳性合同。

## 兼容

C2：四键保留，case 数不减。trigger_eval.json 39 查询语义不变。
严格不变面：旧 31 case 的 id 与 trigger 断言。

## 验证边界

自动化：runner 执行、落点齐全、E1-E9 合同、四键、python 写入、禁止自证测试
本身（元测试：一个只检查字段存在的假测试不得被算作质量通过）。
不自动化：provider A/B、人工盲评、真实论文 P/R、PDF 视觉。

## 回滚

删除 runner、quality-regressions、output-evidence、test_output_evals.py；
用 python 把 evals.json 恢复为只含旧 31 case 四键（从 git restore）。

## 已考虑不做

- 只加 schema/fixture、不跑 workflow：TPR-09 阻断项。
- 本轮做 provider A/B 或盲评：父任务决策 2。
- 把本任务标成 Library-ready：TPR-13。
