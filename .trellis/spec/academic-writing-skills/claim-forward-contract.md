# Claim-Forward（主张前置 / 自我削弱）契约

## 1. Scope / Trigger

修改 `latex-paper-en/scripts/check_claim_forward.py`、`latex-thesis-zh/scripts/check_claim_forward.py`、
两份 `claim-forward-terms*.yaml`、`references/modules/claim-forward.md`、
`references/writing/claim-forward*.md`、over-claim-guard 的"向上校准"节，或 paper-audit 侧任何出现
`CF-*` 观察码的参考文档 / agent 之前，必须遵守本文。

本契约与 `defensive-ai-rhetoric-contract.md` 是两个概念：那里的 "defensive" 指**防御性推测解释**
（多机制堆叠 + 末尾 caveat）。本契约处理的是作者对**自己贡献**的自我削弱与主张后置。术语固定为
`claim-forward` / 主张前置 / 自我削弱，代码前缀 `CF-`；不得用 `defensive` 命名本契约下的模块、脚本、
代码或文件。

## 2. 来源与取舍

- 来源 A：Kiterlin/anti-defensive-writing（MIT，句子/段落级）——整体采纳。
- 来源 B：Adkid-Zephyr/anti-defensive-writing-Skill（MIT，叙事级）——只采纳"主张先于限制、
  结论不新增自我否定、最小改动、自查四问"。
- **否决**（不得进入任何 skill 的规则或候选）：只围绕优势组织、不设自己赢不了的对比、删除非主线
  结果、把技术缺陷改写为范围局限。依据：`latex-thesis-zh/references/writing/conclusion-guide-zh.md`
  "技术缺陷类不利结果必须如实陈述"，`paper-audit/references/OVER_CLAIM_GUARD.md`
  "calibration, not timid prose"，`critical_reviewer_agent.md` cherry-picking 检测。

## 3. 观察码（EN / ZH 脚本同集合，同语义）

| 码 | 语义 | Severity / Priority | 段落门控 |
|---|---|---|---|
| `CF-DISCLAIM` | 段内首个否定式免责句（"We do not claim / 本文不试图"）位于首个主张句之前 | Minor/P2（abstract, introduction, contribution, conclusion）；Info/P3（其余） | `related` 段与 Limitations 段跳过 |
| `CF-SELFWEAK` | 自我削弱**搭配**命中（regrettably / still lags far behind / 遗憾的是 / 仍明显落后 …） | Minor/P2 | 引用句与紧邻的 prior-work 主语句豁免；裸 `only` / `limited` / `仅` / `尚未` 不入词表 |
| `CF-CAVEAT-POS` | 段内首个限制句索引 < 首个主张句索引 | Info/P3 | Limitations 段跳过 |
| `CF-HEDGE-STACK` | 主张句内 hedge 计数 ≥ 3 | Info/P3 | 只看主张句 |
| `CF-CLOSE-NEG` | conclusion / summary **末段**出现负面判定，其后同段无方向标记 | Minor/P2 | Limitations 段跳过；ZH 展望前承接句合法 |

`CF-LOSS-FRAME`（过程编年 / 输者叙事）只在参考文档中定义，属 `[LLM]` 判断，脚本不发。

## 4. 输出格式

```latex
% CLAIM-FORWARD [Script]: section=<key|all> terms=<yaml|builtin>
% CLAIM-FORWARD (Line N) [Severity: Info|Minor] [Priority: P3|P2]: [Script] CF-<CODE> <note>
% Original: <visible sentence>
% Candidate: <reordered / substituted sentence; {placeholders} left for the LLM>
% Meaning-Check: NEEDS-LLM

% CLAIM-FORWARD: <n> finding(s) (CF-...=k, ...)
```

- 退出码恒 0；`--section` 不存在时打 `% ERROR [Severity: Critical] [Priority: P0]: Section not found`
  并列出可用 key，仍 exit 0。
- `--json` 输出 `{"file","section","terms_source","errors","findings":[{code,line,location,severity,
  priority,section,original,candidate,note}],"summary":{"total","by_code"}}`。
- `Candidate` 是**建议**不是替换文本：位置类码只调换顺序，不生成新句；`CF-SELFWEAK` 用 `prefer`
  模板替换，`{占位}` 由 LLM 从稿件证据填入，不得编造；`CF-CLOSE-NEG` 追加
  `[LLM: add the direction ...]`，不删负面判定。
- `[Script]` 恒 `Meaning-Check: NEEDS-LLM`；不带 Changed / Protected / Risk-Flags 四字段
  （模块在 polish contract 三分列表的 "`[LLM]` layer only" 组）。

## 5. 词表

- EN：`references/writing/claim-forward-terms.yaml`；ZH：`references/writing/claim-forward-terms-zh.yaml`。
- 脚本内 `_DEFAULT_TERMS` 与 YAML 等值；YAML 缺失、解析失败、字段非法时**按字段**回退，静默。
- 顶层键：`self_weakening`（`match` / `prefer` 列表）、`hedges`、`disclaim_openers`、
  `direction_markers`、`process_openers`。ZH 可增 `subject_gate` / `cite_exempt` /
  `limitation_section_titles`。
- 词表精度：EN 无私有语料，UNVERIFIED；ZH 基线来自 5 篇私有博士学位论文（只做研究，不进测试）。

### 5.1 ZH 实现差异（latex-thesis-zh）

- 词表文件 `claim-forward-terms-zh.yaml` 增顶层键 `limitation_section_titles`（不足 / 局限 / 研究范围 / 范围界定）；
  `self_weakening` 项可带 `subject_gate`（本文 / 本章 / 本研究 / 所提 / 本方法 / 提出的）：`仅能` / `仅仅` / `未能`
  与评价类搭配（效果有限 / 存在严重不足 / 存在较大差距 / 并不理想 / 差强人意 / 略显不足）只在句中出现自身主语时报，
  且在限制小节内不报；`遗憾的是` / `令人遗憾` / `仍明显落后` 族不门控。
- `CF-CAVEAT-POS` 只看**关于自身工作**的限制句（`OWN_WORK_SUBJECTS`：本文 / 本章 / 本研究 / 本节 / 所提 / 提出的 /
  本方法 / 该方法 / 我们 / 本实验 / 本模型 / 本系统）；“然而 … 难以 … 因此本文提出”问题陈述不报。基线复核：门控前
  5 篇共 51 次位置类命中（抽样近乎全部为问题陈述），门控后 4 次；`CF-SELFWEAK` 4 → 1。设计稿中的 `cite_exempt` 未单列字段——引用句豁免对全部搭配统一生效。
- 引用命令集合含 `\upcite`；引用句之后一句若主语为 `该类方法 / 上述 / 现有 / 传统 / 已有 / 前人 / 文献 / 他们 / 其`
  同样豁免（承接句）。
- 断句按 `。！？；`；主张句主语集 `本文 / 本章 / 本研究 / 本节 / 所提 / 提出的 / 该方法 / 我们`；
  数值主张（提升 12%、降低 40%）不要求主语。
- `有望` 在 `conclusion` / `summary` 章不计入 hedge；其余章计入。
- `CF-CLOSE-NEG` 的方向标记含 `有待 / 后续 / 展望 / 下一步 / 进一步研究`，因此结论章“不足 → 承接句 → 展望”
  （`CC-OUTLOOK-TRANS` 要求的形态）不报。
- 多文件工程经 `tex_loader.assemble` 展开；`--section` 接受英文键与中文章节名。
- 词表基线：5 篇私有博士学位论文只做研究，不进测试；`遗憾的是 / 仍明显落后 / 存在严重不足 / 本文不试图` 基线 0 次，
  `未能` 3 次均指他人工作，裸 `仅` 15–48 次/篇（故只收搭配）。

## 6. 禁改清单

- `deai_check.py` 三副本（含禁止添加 hedge 正则，见 `defensive-ai-rhetoric-contract.md`）。
- TIER1 哈希组：`analyze_abstract.py` / `analyze_grammar.py` / `analyze_sentences.py` / `improve_expression.py`。
- `latex-thesis-zh/scripts/analyze_conclusion.py`（结果经 `zh_check_adapters.py` 流入 paper-audit）、
  `check_style_zh.py`。
- paper-audit：`audit.py`、`scholar_eval.py`、`zh_check_adapters.py`、`quality_rubrics.md` 权重、
  `ISSUE_SCHEMA.md`、lane 数、`ZH_THESIS_REVIEW_CRITERIA.md` 行数。
- `EXPECTED_ABSENCES["check_claim_forward.py"] = ["typst"]`；typst 不在范围。

## 7. paper-audit 观察码集合

paper-audit 只在文档与 agent 层使用 `CF-*`，集合固定为
`{CF-DISCLAIM, CF-SELFWEAK, CF-CAVEAT-POS, CF-HEDGE-STACK, CF-CLOSE-NEG}`；`CF-HEDGE-STACK`
在 audit 侧为 `[LLM]` 观察，不计数。`comment_type` 只用 `presentation`（DISCLAIM / CAVEAT-POS /
CLOSE-NEG）与 `claim_accuracy`（SELFWEAK / HEDGE-STACK）。审稿侧不得建议删除 caveat、不利对比或
非主线结果。（本节由 C3 任务落地；落地前脚本码集合已生效。）

## 8. Tests Required

- `tests/contracts/test_claim_forward_contract.py`：码集合、输出前缀、`--help` flag、SKILL.md 路由行、
  routing-rules 分组、禁改文件哈希不变、paper-audit 码集合闭合。
- `tests/skills/latex_paper_en/test_claim_forward.py`、`tests/skills/latex_thesis_zh/test_claim_forward_zh.py`：
  每码正例 + 反例、引用豁免、Limitations 豁免、YAML 回退。
