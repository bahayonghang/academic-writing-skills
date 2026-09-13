# C3 技术设计：paper-audit claim-forward 审稿信号（文档层）

## 边界

- 改动集合：`references/{OVER_CLAIM_GUARD,CLAIM_EVIDENCE_CONTRACT,SUBAGENT_TEMPLATES,REVIEW_LANE_GUIDE,REVIEWER_PSYCHOLOGY}.md`、`agents/{claims_evidence_reviewer,section_reviewer,critical_reviewer,editor_in_chief,zh_thesis_reviewer}_agent.md`、`SKILL.md`（description / last_updated / Reference Map 一行）、`evals/`、docs、spec、契约测试。
- 禁改：`scripts/*`、`quality_rubrics.md` 权重、`ISSUE_SCHEMA.md`、`DEEP_REVIEW_CRITERIA.md` 结构、lane 数、`ZH_THESIS_REVIEW_CRITERIA.md` 行数。

## 信号流（无代码路径）

```
manuscript -> lane 子代理读 SUBAGENT_TEMPLATES focus block
  -> 观察到 CF-* 模式 -> issue(comment_type=presentation|claim_accuracy, note 含 CF-码)
  -> claims_evidence lane：under-claim 走 claim-evidence map 的 allowed_wording（可更强）
  -> critical lane：确认没有把"删除不利结果"作为建议
  -> editor_in_chief：weak pitch 信号汇总
```

paper-audit 不运行 EN/ZH 的 `check_claim_forward.py`（与 "paper-audit 跑 deai 不传 --analyze，trace 不流入 audit" 同一原则）；观察完全靠 lane 文档与 agent 判断。

## 各文档增量

| 文件 | 增量 | 位置 |
|---|---|---|
| `OVER_CLAIM_GUARD.md` | "## Under-claim and upward calibration" 节：阶梯为上限；四条规则（claim first / positive scope / hedge to earned rung / limitations once）；红线句 "Never recommend deleting a caveat, an unfavorable comparison, or a non-mainline result to make prose sound decisive"；与 cherry-picking 的边界 | 现有阶梯表之后 |
| `CLAIM_EVIDENCE_CONTRACT.md` | 一句：`allowed_wording` may be stronger than the manuscript wording when the evidence row already supports it; report as claim_accuracy | `allowed_wording` 字段说明处 |
| `SUBAGENT_TEMPLATES.md` | `section_intro_related` DO：flag disclaimers before the first claim（CF-DISCLAIM）/ limitations before the claim（CF-CAVEAT-POS）；DON'T：do not suggest removing scope statements。`claims_vs_evidence` DO：flag self-weakening wording where evidence supports stronger（CF-SELFWEAK / CF-HEDGE-STACK）。新增 `section_discussion_conclusion` block：DO flag closing paragraph negative judgment without direction（CF-CLOSE-NEG）；DON'T recommend deleting the negative result | 对应 block；新 block 放在 `section_results` 之后 |
| `REVIEW_LANE_GUIDE.md` | 三个 lane 各一 bullet，引用 OVER_CLAIM_GUARD 新节 | lane 条目内 |
| `REVIEWER_PSYCHOLOGY.md` | "Authors handing the reviewer a knife" 启发：自我削弱句常被直接引用为拒稿理由；只改顺序与措辞；标 UNVERIFIED | 现有启发列表末尾 |
| `ZH_THESIS_REVIEW_CRITERIA.md` | 若行内容非锁定：结论行说明加 "CF-CLOSE-NEG"；否则不改 | 结论行 |
| 5 个 agent | 各一行 DO 或边界句（见 prd R3） | DO/DON'T 列表 |
| `SKILL.md` | description 加 "under-claim / self-weakening"；Reference Map 不新增文件（无新参考文件） | frontmatter |

## 码集合锁定方式

`test_claim_forward_contract.py`：

```python
AUDIT_CF_CODES = {"CF-DISCLAIM", "CF-SELFWEAK", "CF-CAVEAT-POS", "CF-CLOSE-NEG", "CF-HEDGE-STACK"}
# 遍历 paper-audit/references/*.md + agents/*.md，正则 CF-[A-Z-]+，断言 ⊆ AUDIT_CF_CODES 且 == AUDIT_CF_CODES
```

同时断言 `audit.py` / `scholar_eval.py` / `zh_check_adapters.py` / `quality_rubrics.md` sha256 与基线一致（基线在 C3 实现时记录）。

## eval 26 与 fixture

- fixture `evals/fixtures/claim_forward_cases.tex`：Case A（引言首段以 "We do not claim…" 开头）、Case B（结果段 "regrettably … still lags far behind"，且表格数据显示差距 2%）、Case C（贡献段限制句在主张前）、Case D（结论末段 "remains far from practical" 后无 future work）、Case E（Limitations 段 + 一处不利对比如实陈述，期望：不建议删除，只建议措辞 / 顺序）。
- eval prompt：审稿 lane 定位；expected_output 列 4 个 CF 码 + Case E 的 "keep the unfavorable comparison" 明示。
- 紧凑 JSON：按现有 `evals.json` 风格，用 python 读取 → append → 与原文本格式一致的拼接写回（见 memory `evals-json-formatter-gotcha`）。

## 兼容与回滚

- 全部增行；`git revert` 单 commit 即回滚。
- `test_paper_audit_topology_docs.py` 若锁 block 名集合需同步更新，回滚时一起回滚。

## 取舍

- 不加 `CF-` 到 `ISSUE_SCHEMA.md`：码是 note 内的观察标签，不是 schema 字段；与 paragraph-arc 先例一致。
- 不给 claim-forward 独立 lane / 配额：观察量小，并入现有 lane 更少噪音；`claims_vs_evidence` 上限 8 不变。
- `CF-HEDGE-STACK` 保留同名而非删去：跨 skill 交叉引用一致；audit 侧不计数由文档写明。
