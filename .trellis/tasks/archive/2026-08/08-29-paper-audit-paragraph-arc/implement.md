# 执行计划 (C4)

> 本任务为纯文档改动，无代码设计，故不设 `design.md`。
> 判据形态由 C2/C3 定型，此处只做审稿侧的表述落地与一致性对齐。

## 前置

- [x] P1 C2 与 C3 已合入：C2 `af84e4a` / `401ee53`，C3 `e09675d` / `0bda6a1`。
- [x] P2 抄录四要素术语表到 `research/arc-terms.md`，作为本任务的对齐基准。
- [x] P3 定位现有所有权测试并记录到 `research/contract-owners.md`；字符串锁不只属于
      `test_skill_contracts.py`。

## 步骤

### S1 Clarity 行为指标

- [x] S1.1 `references/quality_rubrics.md` 的 `Clarity`（9 维版，13%）五档
      各补一条段落粒度观察点。措辞要求可复核，例如
      "topic sentence identifiable in nearly all body paragraphs" 而非 "well written"。
- [x] S1.2 确认 `Presentation` 未被触碰。
- [x] S1.3 保持 4 维 NeurIPS `Clarity` 与 9 维 `Presentation` 逐字不变；本任务不把
      9 维新增观察点扩张到另一评分面。
- [x] 验证：针对两个非目标表的精确快照断言通过。

### S2 lane 与 subagent 模板

- [x] S2.1 `references/REVIEW_LANE_GUIDE.md` 的 `section_intro_related` 补观察点。
- [x] S2.2 `references/SUBAGENT_TEMPLATES.md` 对应 focus block 补 DO / DON'T。
      DON'T 必须含"缺过渡词不等于逻辑断裂"。
- [x] S2.3 确认 `pre_submission_readiness` 的窄口径说明未被削弱。
- [x] 验证：两文件的段落弧线表述逐条对照，术语一致。

### S3 agent 提示

- [x] S3.1 `agents/critical_reviewer_agent.md` 补观察点。
- [x] S3.2 `agents/section_reviewer_agent.md` 补观察点。
- [x] S3.3 措辞与 S2 一致，不引入新术语。

### S4 REVIEWER_PSYCHOLOGY

- [x] S4.1 新增一节：扫读依赖段首句建立结构预期，段末句判断结论与去向；
      弧线缺失导致回读，回读转化为负面印象。
- [x] S4.2 注明 C2 为中文学位论文局部复算、C3 为受控英文样本；会议/期刊适用性
      **UNVERIFIED**，不得写成普适审稿规律或英文真实语料实测。

### S5 一致性测试与收尾

- [x] S5.1 新增 contract 测试：`paragraph-arc-zh.md`、`paragraph-arc.md`、
      `REVIEWER_PSYCHOLOGY.md` 三处的四要素名集合相同（AC4）。
- [x] S5.2 在现有所有权处扩展 paper-audit/contract tests，覆盖五档、lane/agent 一致性、
      DON'T、四要素与非目标表快照。
- [x] S5.3 AC2 / AC5：确认 `audit.py`、`scholar_eval.py`、`scoring_model.py`
      与九维权重表 diff 为空 —— `git diff --exit-code -- <这些路径>`。
- [x] S5.4 SKILL.md 若需触碰只改 `last_updated`；本任务无路由变化，保持不动。
- [x] S5.5 docs/ 双语页面同步；manifest 散列更新。
- [x] 验证：`just ci`

## 评审门

- G1：S1 完成后，把五档新增的观察点交作者读一遍。作者已于 2026-08-29 明确认可并
      批准继续；判据由 contract 测试锁定到 9 维 Clarity 块。

## 回滚点

各步骤独立成 commit，任一步 `git revert` 不影响其他步骤。

## 禁止事项

- 不改 ScholarEval 九维权重、`scoring_model.py`、`Presentation` 维度。
- 不新增 agent、不新增 lane。
- 不让 deai trace 流入 audit 评分（既有判定）。
- 不让 `pre_submission_readiness` 吸收段落弧线发现。
- 不把学位论文语料的结论写成普适审稿规律。
- 不改 `justfile`、`pyproject.toml`。
