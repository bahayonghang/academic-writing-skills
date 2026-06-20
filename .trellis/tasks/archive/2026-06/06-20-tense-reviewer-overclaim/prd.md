# 借鉴写作判断力 follow-up：⑤ 时态信号词检测 / ⑥ reviewer 怀疑点排序 / ① over-claim 进 paper-audit 维度

## 背景

承接已归档任务 `06-20-borrow-writing-judgment-assets`（从 `ref/scientific-research-skills/scientific-paper-writing`
借鉴 4 项写作判断力资产到 3 个写作技能）。该任务明确留下 3 项 follow-up：

- **⑤** 时态表颗粒度 + 信号词检测（源：`meta/constitution.md` 时态宪法）
- **⑥** reviewer 怀疑点排序（源：`meta/reviewer_psychology.md` 8 类怀疑点按概率降序）
- **①** 把 over-claim guard 进 `paper-audit` 作为审计维度（① 资产已在 3 写作技能脚本化，现要在审计侧落地）

本任务把这 3 项**本地化吸收**进本套件，沿用既有架构（脚本 + 参考文档 + agent），不照搬源技能的领域内容与单技能 meta/tasks 架构。

## 关键架构事实（决定落点）

- `paper-audit/scripts/audit.py` 的 `_resolve_script` **复用兄弟技能脚本**：`deai` 模块指向
  `latex-paper-en|latex-thesis-zh|typst-paper/scripts/deai_check.py`（按 lang/fmt 选）。
  **但**（Phase C 实测）audit 调用时**不传 `--analyze`**，deai 默认只回 "Use --analyze for full analysis"
  一行，故 deai 逐条 trace（overclaim/tense 等）**不进 audit issue**——既有行为，非本任务引入。
  → **⑤ 是写作技能特性；paper-audit 的时态/over-claim 觉察由 ⑥①（文档 + LLM lane）承载**，不改 audit。
- `scholar_eval.py` 把 `DEAI` 模块 issue 映射到 **clarity** 维度。时态属"语言问题"（reviewer 怀疑点 #7）→ clarity 合理，不动映射。
- over-claim 本质是 **soundness / claim_accuracy**，故 ① 要把它显式提升到 `claims_vs_evidence` lane / claims-evidence reviewer，
  **而非**靠 deai→clarity 这条已有暗线（用户已选"文档 + lane/agent 接线"，不重映射 scholar_eval）。

## 目标范围与决策（已与用户确认）

| 项 | 落点 | 形态（用户决策） |
|---|---|---|
| ⑤ 时态信号词检测 | `latex-paper-en` + `typst-paper` + `latex-thesis-zh`(仅英文摘要区域) | 脚本 checker + 三技能时态参考文档 |
| ⑥ reviewer 怀疑点排序 | `paper-audit` only | 参考文档 + critical/synthesis agent 接线（不加脚本排序键） |
| ① over-claim 审计维度 | `paper-audit` only | 参考文档 + `claims_vs_evidence` lane / agent 接线 + CHECKLIST 判据（不重映射 scholar_eval） |

**不在范围**：`bib-search-citation`、`cover-letter`；不新增 ScholarEval 第 10 维度；不动权重表。

## 需求

### ⑤ 时态信号词检测

**脚本（deai_check.py ×3）**——新增 `tense` 检查，与既有 `_check_overclaim` 同构（YAML 驱动 + DEFAULT 回退 + `enabled` 开关 + `[Script]` LOW）：

- **en / typst**：仅在 `method` / `result` 段（含 `_2`/`_3` 变体）检测**现在时报告动词信号词**
  （show/shows、reveal/reveals、demonstrate/demonstrates、indicate/indicates、present/presents、confirm/confirms、
  achieve/achieves、outperform/outperforms 等），命中即提示"Methods/Results 默认过去时"并给保守改写指引。
- **zh**：正文中文无时态，故 checker **仅在英文摘要区域**（`\begin{abstract}`，排除 `\begin{cabstract}`）内运行；
  定位不到英文摘要则整体 no-op。叠加 English-line 门控，避免在中文正文/散落英文术语上误报。
- **高精度优先**：`is`/`are` 因误报率过高**不进正则**（沿用 borrow 任务"判断留文档、正则只收无歧义项"原则），
  仅在参考文档的自查清单里以判断力形式提示。命中须过 figure/table/equation/软件主语的假阳性过滤。

**参考文档（×3）**——时态宪法表本地化：

- en `references/modules/tense-guide.md`、typst `references/TENSE_GUIDE.md`：英文论文逐章节时态表 + 信号词自查清单 + 例外（图表/软件/通论）。
- zh `references/writing/tense-guide-zh.md`：中文学位论文语境，聚焦**英文摘要**时态（Background 现在时 / Methods·Results 过去时 / Conclusion 现在时）。

**测试**：`tests/test_deai_tense.py`——en method/result 命中、干净文本不报、图表/软件假阳性不报、YAML 缺失回退、`enabled:false` 跳过；zh 英文摘要内命中、中文正文不报、无英文摘要 no-op。

### ⑥ reviewer 怀疑点排序（paper-audit）

- 新增 `paper-audit/references/REVIEWER_PSYCHOLOGY.md`：reviewer 真实阅读路径（Step1-4）、3 秒决策、**8 类怀疑点按发生概率降序**
  （数字↔claim 不匹配 > 方法参数缺失 > 引用支持不足 > over-claim > 故事不闭环 > 图文脱节 > 语言问题 > 结果太干净）、
  "让 reviewer 找不到 reject 理由"策略。本地化为通用学术/CS 语境，不用 popgen 例子。
- 接入 `agents/critical_reviewer_agent.md` 与 `agents/synthesis_agent.md`：合并/呈现 findings 时按"reviewer 在哪儿停下怀疑"的层级排序/加权。
- 在 paper-audit `SKILL.md` / `AUDIT_GUIDE.md` references 清单登记新文档。

### ① over-claim 进 paper-audit 审计维度

- 新增 `paper-audit/references/OVER_CLAIM_GUARD.md`：镜像写作技能 over-claim guard（确定性动词梯子 + 7 类替换表 + 陷阱句式 + 与 claim-evidence-contract 边界），paper-audit 扁平大写命名。
- 接入 `claims_vs_evidence` lane：在 `references/SUBAGENT_TEMPLATES.md` 该 lane 指令 + `agents/claims_evidence_reviewer_agent.md` 中显式要求核查 over-claim 措辞，发 `claim_accuracy` issue。
- `references/CHECKLIST.md`（或 REVIEW_CRITERIA）新增 over-claim 判据条目。
- 在 paper-audit `SKILL.md` references 清单登记新文档。
- **说明**：deai 脚本的 over-claim 信号已自动流入（clarity）；本项不改 scholar_eval 映射，只在 claims-evidence 侧补判断力维度。

## 约束（项目护栏）

1. **三副本镜像（仅 ⑤ 脚本/文档）**：deai_check.py 改动须同时落 en/zh/typst；EN 为基准副本，zh/typst 镜像后逐份核对逻辑一致（仅路径/命名差异）。zh 措辞中文本地化，非直译。
2. **不碰 parsers.py**：⑤ zh 英文摘要区域定位写在 deai_check.py 内（直接正则 `\begin{abstract}`），**不动 parsers**，避免触发 `test_parsers_alignment`。
3. **SKILL.md 版本同步**：改任何 SKILL.md 只更新 `last_updated`，**不 bump `version`**（全仓版本统一）。涉及 en/zh/typst（⑤ 文档登记）+ paper-audit（⑥① 文档登记）。
4. **不新增 ScholarEval 维度 / 不改权重**：① 走 lane/agent，不动 `SCHOLAR_EVAL_DIMENSIONS` 权重表（和=1.00，受测试锁定）。
5. **零捏造**：时态表、替换词典、reviewer 心理学、来源引用均须真实可核，不引虚构数据/引用。
6. **references 落点用既有目录**：⑤ 文档进 en `modules/`、zh `writing/`、typst 扁平；不新建受 `REFERENCE_LAYOUTS` 锁定外的目录。
7. 改完 `just ci`（lint → typecheck → test）必须**全绿**。

## 验收标准

- [ ] ⑤ `deai_check.py` ×3 新增 tense checker：en/typst 门控 method/result；zh 门控英文摘要区域、无则 no-op；`is`/`are` 不进正则；过图表/软件假阳性过滤；YAML 缺失回退、`enabled:false` 跳过
- [ ] ⑤ `tone-thresholds.yaml`(en/zh) + `AI_TONE_THRESHOLDS.yaml`(typst) 新增 `tense` 段
- [ ] ⑤ 时态参考文档 ×3 就位（en modules / zh writing 中文化 / typst 扁平），含章节时态表 + 信号词自查 + 例外
- [ ] ⑤ `tests/test_deai_tense.py` 覆盖正例/反例/回退/zh 英文摘要门控，通过
- [ ] ⑤ 验证（Phase C 实测）：paper-audit quick-audit 跑通、deai 模块不报错——确认 ⑤ **不破坏** audit；
      并记录 deai trace 因 audit 不传 `--analyze` 而**不流入** audit（既有行为，paper-audit 觉察走 ⑥①）
- [ ] ⑥ `paper-audit/references/REVIEWER_PSYCHOLOGY.md` 就位（阅读路径 + 8 层怀疑序 + 找不到 reject 策略），critical/synthesis agent 接线，references 清单登记
- [ ] ① `paper-audit/references/OVER_CLAIM_GUARD.md` 就位（动词梯子 + 7 替换表 + 边界），claims_vs_evidence lane（SUBAGENT_TEMPLATES）+ claims_evidence_reviewer_agent 接线，CHECKLIST 判据，references 清单登记
- [ ] 所有改动的 SKILL.md 仅改 `last_updated`，`version` 不变（grep 比对 pyproject）
- [ ] 范围外技能（bib / cover-letter）未被改动
- [ ] `just ci` 全绿

## Notes

- ⑤ 经 deai 模块自动流入 paper-audit，是本任务唯一的跨技能 ripple；① ⑥ 是 paper-audit 内的判断力/接线补强。
- `is`/`are` 不进正则是刻意的精度取舍（见 design 三）。若后续要更激进检测，另开 follow-up 并配充分 fixture。
