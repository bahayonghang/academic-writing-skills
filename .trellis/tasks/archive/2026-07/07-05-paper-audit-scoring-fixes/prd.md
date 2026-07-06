# paper-audit 评分链修复

## Goal

修复 paper-audit 评分链的两处集成断链与一处计数偏差，并补上新增判断力功能（REVIEWER_PSYCHOLOGY / OVER_CLAIM_GUARD）的测试与 evals 覆盖。

证据详情：`../07-05-skills-deep-analysis-optimization/research/paper-audit-findings.md`

## 问题清单

- **PA-1 [medium]** `critical_count` 惩罚项在生产评分路径是死代码：`scholar_eval.py:265` 的 `scorer.predict(merged)` 不传 critical_count，audit.py 也不传，`--regression` 下 -0.5/critical 惩罚永不触发。`tests/test_literature_search.py:575-578` 的单测直接传参断言生效，掩盖了集成断链。
- **PA-2 [medium]** 空文献检索结果被误判为"文献根基差"：API 全失败/无 key 时 `compute_literature_grounding_score([])` 返回 ~2.0，灌入 12% 权重拉低 overall，与真正文献薄弱的论文不可区分（`literature_compare.py:225` / `audit.py:2505`）。
- **PA-3 [low]** `scoring_model.py:159` `dims_below_5` 把 overall 也当维度计数，轻微多扣。
- **测试/evals 盲区**：PA-1 集成路径、PA-2 空结果降级无测试；REVIEWER_PSYCHOLOGY 排序与 OVER_CLAIM_GUARD 在 tests/ 与 evals/ 中 grep 零命中。

## Requirements

- R1 PA-1：把 critical_count 从 audit 结果贯通到 `scorer.predict` 调用（scholar_eval.build_result 与 audit.py 两侧）；补集成测试断言"含 critical 发现的审计其 regression 分低于同分无 critical 的审计"。
- R2 PA-2：文献检索空结果时 literature_grounding 置 None 并让加权平均按剩余维度重新归一化（或等效方案），输出中明确标注"文献检索不可用"而非低分；补空结果降级测试。
- R3 PA-3：`dims_below_5` 排除 overall。
- R4 为 REVIEWER_PSYCHOLOGY 排序与 OVER_CLAIM_GUARD lane 补最小测试与至少一条 eval 用例。

## Acceptance Criteria

- [ ] critical_count>0 时 `--regression` 总分确实被扣减（集成测试，非直连 scoring_model 的单测）。
- [ ] 无 API key 跑 `--literature-search` 时 overall 不因空结果下降，输出含明确的不可用标注。
- [ ] 9 维权重在 literature_grounding 缺席时重新归一化为 1.00（测试断言）。
- [ ] REVIEWER_PSYCHOLOGY / OVER_CLAIM_GUARD 各有至少一条测试与一条 eval，`just ci` 全绿。

## Notes

- 既有设计不动：REVIEWER_PSYCHOLOGY / OVER_CLAIM_GUARD 不改权重、不加打分维度；paper-audit 跑 deai 不传 --analyze。
- PA-4/PA-5/PA-6（纯文档项）在 `07-05-docs-metadata-consistency` 处理，本任务不碰。
