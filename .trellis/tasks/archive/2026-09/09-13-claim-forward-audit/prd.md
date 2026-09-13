# paper-audit 自我削弱审稿信号 (C3)

父任务：`.trellis/tasks/09-13-claim-forward-integration/`。前置：C1、C2 已归档。

## Goal

让 paper-audit 的审稿 lane 能识别作者自我削弱 / 主张后置（claim-forward 问题）并作为 presentation / claim_accuracy 类观察报告，同时明确"不得因此建议删除不利结果"的边界。仅改文档与 agent 提示；不加脚本、不改评分、不改 lane 数。

## Requirements

### R1 观察码集合（固定 5 个）

`CF-DISCLAIM`、`CF-SELFWEAK`、`CF-CAVEAT-POS`、`CF-CLOSE-NEG`、`CF-HEDGE-STACK`。

- 与 EN/ZH 脚本同名同义（定义引用 `claim-forward-contract.md`）。
- `CF-HEDGE-STACK` 在 audit 侧只作 `[LLM]` 观察（不计数），保留同名以便交叉引用。
- 集合由 `tests/contracts/test_claim_forward_contract.py` 锁定：任一 paper-audit 文档出现 `CF-` 码必须属于该集合。

### R2 参考文档

- `references/OVER_CLAIM_GUARD.md` 新增 "Under-claim / upward calibration" 节：阶梯是上限；hedge 降到证据已支撑档；**禁止**因"显得果断"建议删除 caveat 或不利结果；与 cherry-picking 的边界（顺序 / 措辞可改，内容不得删）。
- `references/CLAIM_EVIDENCE_CONTRACT.md` 加一句：`allowed_wording` 在证据已支撑时可比原文更强（under-claim 是 claim-evidence 不匹配的另一方向）。
- `references/SUBAGENT_TEMPLATES.md`：`section_intro_related` 与 `claims_vs_evidence` 的 DO/DON'T 各加 claim-forward 条目；新增 `section_discussion_conclusion` focus block（现无），含 `CF-CLOSE-NEG` DO 与 "DON'T 建议删除负面结果" 。
- `references/REVIEW_LANE_GUIDE.md`：相关 lane 各加一条 bullet。
- `references/REVIEWER_PSYCHOLOGY.md`：新增"作者递刀子"启发（自我削弱句被审稿人直接引用为拒稿理由）；标注 UNVERIFIED（无实证来源，仅经验规则）。
- `references/ZH_THESIS_REVIEW_CRITERIA.md` 不改行数（15 行固定）；在现有"结论"行的说明中加 `CF-CLOSE-NEG` 指路（若该文件被字符串锁锁定行内容，则改为在 `zh_thesis_reviewer_agent.md` 加 DO 行）。

### R3 agents

- `claims_evidence_reviewer_agent.md`：DO 加 "flag under-claim when evidence supports a stronger wording; report as claim_accuracy"。
- `section_reviewer_agent.md`：DO 加 `CF-DISCLAIM` / `CF-CAVEAT-POS` 观察（presentation）。
- `critical_reviewer_agent.md`：边界句：cherry-picking 检测与 claim-forward 不冲突，后者只改顺序与措辞。
- `editor_in_chief_agent.md`：weak pitch 信号加一条：摘要 / 引言首段以免责或限制开头。
- `zh_thesis_reviewer_agent.md`：DO 加一行（结论章末段负面判定无展望）。

### R4 评估

- `evals/evals.json` 追加 id 26（紧凑格式文本拼接）；fixture `evals/fixtures/claim_forward_cases.tex`（5 case：4 正例对应 CF-DISCLAIM / CF-SELFWEAK / CF-CAVEAT-POS / CF-CLOSE-NEG + 1 边界反例：Limitations 段合法限制 + 不利结果如实陈述，期望不建议删除）。
- `evals/trigger_eval.json` 追加 ≥1 positive。
- `comment_type` 只用 `presentation`（CF-DISCLAIM / CF-CAVEAT-POS / CF-CLOSE-NEG）与 `claim_accuracy`（CF-SELFWEAK / CF-HEDGE-STACK）。

### R5 spec 与测试

- `claim-forward-contract.md` 填 "paper-audit 观察码集合" 节（C1 留的占位）与 "禁改清单"（`audit.py`、`scholar_eval.py`、`quality_rubrics.md` 权重、`ISSUE_SCHEMA.md`、lane 数、`ZH_THESIS_REVIEW_CRITERIA.md` 行数）。
- `test_claim_forward_contract.py` 增 audit 用例：5 码集合闭合；OVER_CLAIM_GUARD 含 under-claim 节标题与 "do not delete" 句；SUBAGENT_TEMPLATES 含 `section_discussion_conclusion` block；`audit.py` / `scholar_eval.py` / `quality_rubrics.md` 哈希不变；`ZH_THESIS_REVIEW_CRITERIA.md` 仍 15 行。
- `tests/skills/paper_audit/test_paper_audit_topology_docs.py` 若锁 SUBAGENT_TEMPLATES 的 block 名集合，更新期望。

### R6 docs

- `docs/` 与 `docs/zh/` paper-audit 页加一段；manifest 重生成。SKILL.md description 加 "under-claim / self-weakening"（≤400），`last_updated` 更新。

## Acceptance Criteria

- [ ] paper-audit 内所有 `CF-` 出现均属 5 码集合（契约测试）。
- [ ] `audit.py`、`scholar_eval.py`、`zh_check_adapters.py`、`quality_rubrics.md`、`ISSUE_SCHEMA.md` 字节不变。
- [ ] `ZH_THESIS_REVIEW_CRITERIA.md` 15 行不变；lane 数不变。
- [ ] eval 26 与 fixture 存在；fixture 边界 case 的 expected_output 明确写 "do not recommend deleting the unfavorable result"。
- [ ] `test_claim_forward_contract.py`、`test_paper_audit_topology_docs.py`、`test_skill_contracts.py`、`test_trigger_evals.py`、`test_docs_bilingual_resources.py` 绿；`just ci`、`check_resource_sync.py`、`just doc-build` 绿。

## Constraints

- 不加脚本、不改 `LANG_SCRIPT_OVERRIDES` / `_SCRIPT_MAP`、不改 MODULE_DIMENSION_MAP、不改评分权重。
- `claims_vs_evidence` 上限 8 不变；claim-forward 观察不设独立配额。
- 沿用 paragraph-arc-audit-contract 先例（文档 + lane + agent + psychology）。

## 依赖

- 依赖 C1（契约 + 测试骨架）与 C2（ZH 码定义，供 `zh_thesis_reviewer_agent.md` 引用）。
