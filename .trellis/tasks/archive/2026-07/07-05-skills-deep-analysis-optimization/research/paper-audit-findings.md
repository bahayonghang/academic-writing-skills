# Research: paper-audit Deep Audit Findings

- **Query**: 深入分析 paper-audit skill 现存问题（新增功能正确性、评分模型、agent 契约、SKILL 契约、evals、测试盲区）
- **Scope**: internal
- **Date**: 2026-07-05
- **Auditor**: deep-audit researcher
- **Baseline respected**: 2026-06 五技能优化 / 六技能复审已清零旧问题；parsers.py 副本是有意分歧；deai trace 不流入 audit 评分（有意设计）；commit 8cf4622 的 REVIEWER_PSYCHOLOGY / OVER_CLAIM_GUARD 走 lane/agent 判断力、不改 scholar_eval 权重——本次已独立复核该决策，确认成立，不作为问题。

---

## Findings

### PA-1 — `critical_count` 惩罚项在生产评分路径里是死代码（unit test 造成假阳性信心）

- **Severity**: medium
- **Location**:
  - `scripts/scholar_eval.py:265`（`prediction = scorer.predict(merged)` 未传 `critical_count`）
  - `scripts/audit.py:2545-2548`（`build_scholar_result(script_scores, use_regression=regression)` 也不传 critical 计数）
  - `scripts/scoring_model.py:67-79`（`predict(..., critical_count: int = 0)` 默认 0）
  - `scripts/models/scoring_model.json:15`（`"critical_count": -0.5`）
- **问题描述**: weighted-plus 评分模型定义了 `critical_count` 元特征，系数 -0.5（每个 Critical 扣 0.5 分）。但真实审计流水线里，`scholar_eval.build_result` 调 `scorer.predict(merged)` 时**从不传 `critical_count`**，`audit.py` 也不传。因此该特征在 `--regression` 开启时恒为 0，-0.5 惩罚**永不触发**。overall 分数不会因为 Critical issue 数量而下降。
- **证据**:
  - `scholar_eval.py:265` 只传一个位置参数 `merged`，`critical_count` 走默认 0。
  - `test_literature_search.py:575-578` 有单元测试 `scorer.predict(scores, critical_count=3)` 断言扣分生效——**测试通过给了"惩罚项有效"的假象**，但它直接调 `predict` 传参，绕过了真实的 `build_result` 集成路径，掩盖了流水线断链。
- **建议修复方向**: 在 `scholar_eval.build_result` 里把 Critical issue 数量从审计结果算出并透传给 `scorer.predict(merged, critical_count=n)`；或在 `audit.py:2545` 处统计 `all_issues` 中 severity=="Critical" 的数量并沿调用链传入。补一条端到端集成测试（从 audit issues → scholar_eval → 含 critical 的 overall 变化）。

### PA-2 — 空文献检索结果被当成"文献根基差"，把基础设施失败灌入 12% 权重维度

- **Severity**: medium
- **Location**:
  - `scripts/literature_compare.py:225-268`（`compute_literature_grounding_score`，空输入返回 ~2.0）
  - `scripts/audit.py:2505-2512`（无论 `filtered_results` 是否为空都计算 grounding score）
  - `scripts/audit.py:2541-2544`（把该分数作为 `literature_grounding_partial` 传入 scholar_eval）
- **问题描述**: 当 `--literature-search` 开启但外部 API 全部失败 / 无 key / 网络不可用时，`literature_context.filtered_results` 为空。`compare_with_literature([])` 下 `total_found=0`：coverage_component=0、recency_component=0、missing_component=1.5（"neutral"）、freshness_component=0.5，raw=2.0 → **grounding_score=2.0**。这个"低分"被当作真实维度分（权重 12%）拉低 overall，与"真正文献根基薄弱的论文"无法区分——把一次基础设施失败误判成论文缺陷。
- **证据**: `literature_compare.py:246-262` 的 `total_found>0` / `total_dist>0` 分支在空输入时全部走 else，得到 1.5+0.5=2.0；`audit.py:2492` 会打印 "0 relevant results found" 但仍在 2505 继续算分并在 2511 赋值。
- **建议修复方向**: 在 `audit.py` 里当 `filtered_results` 为空（或搜索抛异常）时，把 `literature_grounding_score` 置 `None` 而非算出 2.0，让 scholar_eval 的加权平均按"缺失维度"重新归一化（`_weighted_average` 已支持跳过 None），并在报告里标注"文献检索无结果，该维度未评分"。或在 `compute_literature_grounding_score` 对 `total_found==0` 直接返回 `None`/哨兵。

### PA-3 — `dims_below_5` 元特征把计算出的 `overall` 也算作一个"低分维度"

- **Severity**: low
- **Location**: `scripts/scoring_model.py:159`
- **问题描述**: `_extract_features` 的 `dims_below_5 = sum(1 for v in scores.values() if v is not None and v < 5.0)`。在生产路径中 `scores` 是 `merged`（`scholar_eval.merge_scores` 的输出），**包含已计算的 `overall` 键**。若 overall < 5，会被算进 "dims_below_5"，等于把综合分当成第 9 个维度重复计入惩罚（系数 -0.3），轻微夸大扣分。
- **证据**: `merge_scores` 在 `scholar_eval.py:211` 设置 `final["overall"]`；`build_result:265` 把这个含 overall 的 dict 传给 `predict` → `_extract_features` 遍历 `.values()` 含 overall。
- **建议修复方向**: 在 `_extract_features` 里对 `dims_below_5` 显式排除 `overall`（以及任何 `*_partial` 键），只统计 8 个基础维度。

### PA-4 — SKILL.md 把 scoring model 描述为 "regression-based"，与实现明确矛盾

- **Severity**: low
- **Location**:
  - `SKILL.md:326`（"regression-based overall score with weighted-average fallback"）
  - `SKILL.md:13` argument-hint 里 `--regression` 标志名
  - `scripts/scoring_model.py:1-10, 30-36, 187-198`（docstring 明确声明"NOT a statistically trained regression model"，`train()` 抛 NotImplementedError）
- **问题描述**: 类名 `RegressionScorer`、CLI 标志 `--regression`、SKILL.md 的 "regression-based" 表述，都暗示统计回归 / 训练模型；但实现本身在 docstring 里反复澄清系数是手调的加权平均（`model_type="weighted_plus"`），并无回归。文档与实现自相矛盾，可能误导使用者以为有训练好的模型。
- **建议修复方向**: 统一措辞。最小改动：把 SKILL.md:326 改为"weighted-plus overall score (hand-tuned weights + interaction/penalty terms)"，与脚本 docstring 一致；类名/标志名保留（backward compat，脚本注释已解释）即可，但文档不应再称 "regression-based"。

### PA-5 — SKILL.md 未登记 `--regression` / `--tavily-key` / `--s2-key` 三个真实 CLI 标志

- **Severity**: low
- **Location**: `SKILL.md:13`（argument-hint）对照 `scripts/audit.py:3057-3092`
- **问题描述**: `audit.py` argparse 实际支持 `--scholar-eval`、`--literature-search`、`--tavily-key`、`--s2-key`、`--regression`、`--overwrite-workspace`、`--format` 等。SKILL.md 的 `argument-hint` 只列了 `--literature-search`、`--scholar-eval`、`--overwrite-workspace`、`--format`，**漏掉 `--regression`、`--tavily-key`、`--s2-key`**。`--regression` 在 SKILL.md 正文任何地方都没出现（只出现 "regression" 作为形容词）。属文档完整性缺口，非功能 bug。
- **建议修复方向**: 在 argument-hint 补 `[--regression] [--tavily-key KEY] [--s2-key KEY]`，并在正文（Scripts 或 Critical Rules 的 online 段）说明 `--regression` 切换的是 weighted-plus 模型。

### PA-6 — critical_reviewer_agent 标题写 "8 Challenges" 但实际有 11 个维度

- **Severity**: low
- **Location**: `agents/critical_reviewer_agent.md:45`（"## Review Dimensions (8 Challenges)"）对照 `:47-98`（编号 1-11 的维度）与 `:157`（"challenges you formulated during dimensions 1-11"）
- **问题描述**: 标题声明 8 个挑战，但下面列了 11 个（C3/C4/C5 = dim 9/10/11 是后加的），且 surrender 计数逻辑自身写的是 "dimensions 1-11"。标题与内容不一致，可能让 agent 少跑后 3 个维度或误报 `challenges_made`。SKILL.md:358 也称其 "with C3-C5 checks"，说明 11 维是预期。
- **建议修复方向**: 把标题改为 "Review Dimensions (11 Challenges)"（或 "8 core + 3 cross-section"）。

---

## 未发现问题的维度（明确记录）

- **scholar_eval 权重归一化**: 9 维权重 `0.18+0.13+0.08+0.13+0.13+0.08+0.05+0.12+0.10 = 1.00`，**精确 100%**（`scholar_eval.py:37-47`）。commit 8cf4622 的两个新增维度（REVIEWER_PSYCHOLOGY / OVER_CLAIM_GUARD）确实**未新增打分维度、未改权重**——纯 lane/agent 排序与判断力，`_weighted_average` 对缺失维度按可用权重重新归一化，无越界风险。此项 CLEAN，确认既有设计决策成立。
- **REVIEWER_PSYCHOLOGY 排序逻辑一致性**: `REVIEWER_PSYCHOLOGY.md` 的 8 层怀疑序、`critical_reviewer_agent.md:239-247` 的 Finding Prioritization、`synthesis_agent.md:71-74` 的 tie-break 三处措辞一致（numbers↔claim mismatch 最高、"too clean" 最低），引用的 lane 名（`claims_vs_evidence`/`notation_and_numeric_consistency`/`evaluation_fairness_and_reproducibility`/`prior_art_and_novelty_grounding`）与 `REVIEW_LANE_GUIDE.md:20-24` 完全对齐。无漂移。
- **OVER_CLAIM_GUARD 接入对齐**: `OVER_CLAIM_GUARD.md` 与 `claims_evidence_reviewer_agent.md:12-15`、`SUBAGENT_TEMPLATES.md:74-85`、SKILL.md 输出 schema（`comment_type: claim_accuracy` + `allowed_wording`/`forbidden_wording`/`claim_strength`）四侧一致，与 `CLAIM_EVIDENCE_CONTRACT` 的边界（strength ladder vs wording ladder，冲突时 contract 优先）表述清晰。无 bug。
- **评分模型除零 / 越界**: `predict` 与 `_fallback_predict` 都 `max(1.0, min(10.0, ...))` 截断；`_weighted_average` 有 `total_weight==0 → None` 守卫；fallback `total_weight>0 else 5.0`。无除零、无越界。
- **literature_search 失败降级**: 三个 client（S2/arXiv/Tavily）全部 `except → return []`，S2 对 429 有指数退避重试（`literature_search.py:92-98`），Tavily 对 401/403 区分认证失败并打印提示（`:235-244`），`ThreadPoolExecutor` 的 `future.result()` 也包了 try/except。降级路径稳健。（注：空结果向下游的语义问题见 PA-2，属 compare/audit 侧而非 search 侧。）
- **synthesis agent 输出契约**: `synthesis_agent.md` 的 Required Inputs 已含 `REVIEWER_PSYCHOLOGY.md`（8cf4622 加），consensus/arbitration/severity 流程完整，`frame_lock` advisory 由 `consolidate_review_findings.apply_frame_lock_advisory` 处理并有测试覆盖。无契约缺口。

---

## 测试盲区

- **PA-1 的集成缺口未被测试**: `test_literature_search.py:575-578` 只在**单元层**直接 `predict(critical_count=3)`，无端到端测试覆盖 `audit issues → build_result → overall` 的 critical 透传，因此这条断链一直"测试全绿"。建议补集成测试。
- **PA-2 空结果降级无测试**: 无用例覆盖"literature_search 返回空 → grounding_score 行为"。建议补一条断言（空结果不应产出误导性低分）。
- **REVIEWER_PSYCHOLOGY 排序 / OVER_CLAIM_GUARD 无测试**: `grep` 确认 `tests/` 无任何 `REVIEWER_PSYCHOLOGY` / `OVER_CLAIM_GUARD` / suspicion-ordering 引用。属 LLM prompt 级特性，难以单测，但 synthesis 的"同级内按怀疑序 tie-break"这类可判定的排序规则目前完全无回归保护。
- **已有良好覆盖**: `surrender` / `frame_lock` 经 `test_paper_audit_deep_review.py:914-1027` 覆盖（apply_frame_lock_advisory 阈值、边界、渲染）；`scoring_model` 的 fallback / 系数 / load_model / 越界 经 `test_literature_search.py:473-594` 覆盖（除 PA-1 的集成断层外）。

---

## evals 现状

- `evals/evals.json` 与 `evals/trigger_eval.json` **均无** scoring / regression / over-claim / reviewer-psychology / scholar / surrender / frame_lock 相关样例（grep 0 命中）。新增能力（8cf4622 的排序/over-claim 维度，以及 v3.0 的 scoring_model/literature）在 evals 层完全未覆盖。若团队把 evals 作为能力回归基线，这是覆盖缺口（medium-low，取决于 evals 是否被视为契约）。

---

## 严重度汇总表

| 编号 | 严重度 | 文件:行 | 一句话 |
|---|---|---|---|
| PA-1 | medium | scholar_eval.py:265 / audit.py:2545 | `critical_count` 惩罚在生产评分路径恒为 0（死代码），单测掩盖了集成断链 |
| PA-2 | medium | literature_compare.py:225 / audit.py:2505 | 空文献检索结果 → grounding≈2.0，把 API 失败灌入 12% 权重维度 |
| PA-3 | low | scoring_model.py:159 | `dims_below_5` 把 `overall` 也算作低分维度，轻微多扣 |
| PA-4 | low | SKILL.md:326 | 文档称 "regression-based"，与脚本"非回归/手调权重"声明矛盾 |
| PA-5 | low | SKILL.md:13 | argument-hint 漏登记 `--regression`/`--tavily-key`/`--s2-key` |
| PA-6 | low | critical_reviewer_agent.md:45 | 标题 "8 Challenges" 与实际 11 维度不符 |

**无 high 严重度问题。** 新增功能（REVIEWER_PSYCHOLOGY / OVER_CLAIM_GUARD）的正确性、agent 契约一致性、评分权重归一化、除零/越界、外部 API 降级——除上述 6 项外均 CLEAN。
