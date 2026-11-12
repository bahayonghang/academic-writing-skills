# Claim-Forward Writing Guide

How to let the reader meet the claim before the limitation, without deleting a single limitation or unfavorable result. Companion to the `claim-forward` module (`references/modules/claim-forward.md`) and to the "Upward calibration" section of `references/writing/over-claim-guard.md`.

## The one rule

**Claim first, scope second, limitation once.** Every paragraph that carries a contribution opens with the contribution. The scope (what the claim covers) follows in positive form. Each limitation is written once, in the place the reader expects it (design constraints in the method chapter, evidence boundaries in the discussion or the "本文的不足" section), and is not repeated as a hedge in front of every claim.

## What this guide does not permit

These edits are rejected on purpose. They conflict with the over-claim guard ("calibration, not timid prose"; never delete a caveat to sound decisive), with the claim-evidence contract, and with the reviewer-side cherry-picking checks:

- Deleting an unfavorable comparison, a failed setting, or a non-mainline result.
- Rewriting a technical shortcoming as a "scope choice" (writing "本文不针对长序列" when the method breaks on long sequences).
- Choosing baselines or metrics so the thesis "cannot lose".
- Raising a verb past the rung the evidence supports (see the certainty ladder in the over-claim guard).

Claim-forward changes **order and wording** only. Content stays.

## Sentence functions (classify before editing)

| Function   | Test                                                                  | Where it belongs                                                             |
| ---------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Claim      | States what the thesis achieves, with or without a number             | First sentence of the paragraph                                              |
| Evidence   | Points to a table, figure, statistic, or comparison                   | Immediately after the claim                                                  |
| Scope      | Says what the claim covers, in positive terms ("在三个室内基准上")    | Inside or right after the claim                                              |
| Limitation | Says what the claim does not cover or where it fails                  | After the claim; once per limitation; or in the "本文的不足" section         |
| Transition | Links to the next paragraph                                           | Last sentence                                                                |
| Process    | Narrates what the authors tried and when                              | Usually deleted from the results; written in the method chapter if the reader must reproduce it |

## Five-step rewrite

1. **Locate the claim.** Find the sentence that states the contribution. If there is none, the paragraph needs a claim before any other edit (do not invent one; ask the author).
2. **Move the claim first.** Put it before any disclaimer, apology, or limitation in the paragraph.
3. **Turn scope positive.** "本文不处理室外场景" becomes "在三个室内基准上" attached to the claim. Delete the negative sentence only when the positive scope now carries the same information; otherwise keep it after the claim.
4. **Place each limitation once.** If the same caveat appears in the abstract, the introduction, and the results, keep it where the evidence is discussed and where a "本文的不足" section exists. The copies are what to delete, not the limitation itself.
5. **Minimal edit and recheck.** Re-read: is every number, comparison, and caveat still present? Does any verb now sit above its evidence rung? If so, step back down.

**Supplement: repair order.** The five steps stay unchanged. When one paragraph holds both an over-strong claim and a vague concession (see "Over-strong claim with a vague concession" below), repair it in three fixed steps: (1) put the evidence first, writing the numbers, tables, figures, or material that support the claim up front; (2) calibrate the claim on the certainty ladder in `over-claim-guard.md`, only down to the rung the evidence supports; (3) replace the vague concession with one concrete boundary that states its reason. Doing step (3) alone deletes the concession and leaves the over-strong claim; do not edit that way.

## Preferred and discouraged patterns

| Discouraged                                                                 | Preferred                                                                                                  | Why                                                          |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| "本文不试图解决通用场景理解问题。本文方法将准确率提高 12%。"                | "本文方法在三个室内基准上将准确率提高 12%。本文未评估室外场景。"                                           | Claim first; scope positive; the boundary stays              |
| "遗憾的是，本文方法在长尾划分上仍明显落后于理想上界。"                      | "本文方法在长尾划分上落后理想上界 4.1 个百分点。"                                                          | State the gap as a measurement, not an apology               |
| "尽管评估范围限于一个数据集，本文取得 7% 的提升。"                          | "本文在数据集 X 上取得 7% 的提升。更多数据集上的评估是后续工作。"                                          | Limitation after the claim, with a direction                 |
| "本文方法可能在一定程度上或许能够提升鲁棒性。"                              | "本文方法在遮挡条件下提升鲁棒性（表 3）。" or, if the evidence is weak, "本文方法可能在遮挡条件下提升鲁棒性。" | One hedge, chosen by the evidence                            |
| "本文方法仅能达到 91%，仅仅与基线持平。"                                    | "本文方法达到 91%，与基线持平而计算量为其三分之一。"                                                       | Report the number with the trade-off, not with "仅能 / 仅仅" |
| "起初尝试 Transformer 失败，随后改用 CNN 也失败，最终 …"                    | "本文采用混合编码器（3.2 节）；附录 B 报告评估过的备选方案。"                                              | Process chronology moves out of the results (`CF-LOSS-FRAME`) |
| Conclusion ending: "然而，该框架无法处理帧率可变的输入。"                   | "… 尚不支持帧率可变的输入；将缓冲机制扩展到异步输入是下一步工作。"                                         | Close on a direction, keep the judgment                      |

## Self-check (four questions after the rewrite)

1. Is the first sentence of each contribution paragraph the claim?
2. Does every limitation sit after the claim it qualifies, and appear only once?
3. Is every "遗憾的是 / 仅仅 / 仅能 / 未能 / 效果有限 / 存在严重不足" replaced by a measured value or a positive scope?
4. Does the closing paragraph add a direction after its last limitation instead of a new self-negation?

If answering any question required deleting a comparison, a result, or a caveat, undo that edit.

## Codes emitted by the script

| Code             | Layer        | What to do                                                                                         |
| ---------------- | ------------ | -------------------------------------------------------------------------------------------------- |
| `CF-DISCLAIM`    | `[Script]`   | Step 2 (move the claim first)                                                                      |
| `CF-CAVEAT-POS`  | `[Script]`   | Step 2 and step 4                                                                                  |
| `CF-SELFWEAK`    | `[Script]`   | Replace the collocation with a measurement; fill `{占位}` from the manuscript only                 |
| `CF-HEDGE-STACK` | `[Script]`   | Keep one hedge; check the over-claim ladder first                                                  |
| `CF-CLOSE-NEG`   | `[Script]`   | Add the direction; keep the judgment                                                               |
| `CF-LOSS-FRAME`  | `[LLM]` only | Move process chronology out of the results / conclusion; keep the alternatives in the method chapter or an appendix |

## Relation to the conclusion module

The `conclusion` module's `CC-OUTLOOK-TRANS` requires a transition sentence before the outlook ("上述不足有待后续工作 …"), and `CF-CLOSE-NEG` requires a direction after the negative judgment. The pattern that satisfies both: negative judgment → transition sentence → outlook; the outlook-paragraph template in `references/writing/conclusion-guide-zh.md` already conforms. Do not delete the limitation in the closing paragraph to satisfy claim-forward — that would trigger the "missing limitation" rule of the conclusion-chapter guide at the same time.

## Relation to the over-claim guard

The over-claim guard calibrates downward (evidence weaker than the wording). Claim-forward calibrates upward (wording weaker than the evidence). They share one ladder: a claim-forward rewrite may raise a verb only to the rung the evidence already supports, and the guard's "reverse calibration" list names the cases where strong wording is earned. When unsure, leave the verb and fix only the order.

## Attribution

Adapted, with the rejections noted above, from two MIT-licensed skills:

- Kiterlin, _anti-defensive-writing_ — https://github.com/Kiterlin/anti-defensive-writing (sentence-function classification, five-step rewrite, preferred / discouraged patterns, "write limitations once").
- Adkid-Zephyr, _anti-defensive-writing-Skill_ — https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill (claim-before-limitation ordering, self-weakening word list, "no new self-negation in the conclusion", minimal-edit prompt, self-check questions). Its rules on selective presentation (organize only around strengths, avoid comparisons you cannot win, delete non-mainline results) are not adopted; see "What this guide does not permit".

## Three dispositions for defensive wording (LLM only)

These three dispositions are judged only by the LLM. They add no observation code and no word list, and they do not delete an unfavorable result. The strength ceiling remains the relation to the over-claim guard above. An unverified weakness must not be written as a design advantage.

### Keep a real evidence boundary

Scope: deleting the sentence would leave the method's legitimacy or the evidence level open to question.
Keep: this thesis reports only the error inside the offline replay window and does not write that error as a closed-loop control gain.
Do not rewrite: delete that sentence and leave only “this thesis reduced the control error”.

### Turn a negation into a positive statement

Scope: turn a negation into a positive statement only when the source already supports the positive wording. The distinction must remain.
Keep: the normalized threshold performs the initial screening. The hardware limit is supplied separately by the deployment environment.
Do not rewrite: change “do not equate the normalized threshold with the hardware limit” into “the normalized threshold guarantees hardware safety”.

### Present a weakness as a trade-off

Scope: present a weakness as a trade-off only when the manuscript already states it as a real design choice.
Keep: the peak channel's extreme-value error is larger than the baseline. The manuscript already states that this channel emits the group mean under squared error, and extreme-value fidelity is not the design goal.
Do not rewrite: an underestimated peak is rewritten as “effectively suppresses numerical jitter and keeps monotonicity”. An unverified weakness must not be written as a design advantage. A false-detection rate above the baseline must stay. Do not delete it, and do not rewrite it as “therefore more faithful”.

### Metaphor words are context examples

Words such as gate, fortify, intrinsic safety, and theoretical performance upper bound are not a banned-word regular expression. If the context already states a check, a block, or a fallback, write that observable mechanism. Do not build a banned-word list from these examples.

### Suggestion blocks

```latex
% 主张前置（合成）[Severity: Minor] [Priority: P2]: [LLM] 保留真实证据边界
% 问题：限制句写成了自我削弱，但边界本身是证据层级
% 原文：本文只报告离线回放窗口内的误差，不把该误差写成闭环控制收益。
% 修改后：保留原句。
% 理由：删掉边界会把回放误差写成控制收益。本类只由 LLM 判断。

% 主张前置（合成）[Severity: Minor] [Priority: P2]: [LLM] 否定转正面缺少原文支持
% 问题：否定句被改成了原文没有的保证
% 原文：不将归一化阈值等同于硬件限值。
% 修改后：不得改成“归一化阈值保证硬件安全”。原文支持时才可写成“归一化阈值用于初筛。硬件限值由部署环境单独给定。”
% 理由：正面说法必须仍能区分两类界限。

% 主张前置（合成）[Severity: Major] [Priority: P1]: [LLM] 未验证弱点被写成设计优点
% 问题：欠估被改成已证的抑制能力，不利数字被删掉
% 原文：峰值被低估。误检率高于基线。
% 修改后：保留两句观察。只有稿件已写明设计选择时，才可补充“该通道在均方误差下输出分组均值”。
% 理由：未验证的弱点不得写成设计优点。不得删除不利结果。门禁、筑牢一类词只是语境例子，不是禁词正则。
```

## Four dispositions for pre-emptive rebuttal and concession shells (LLM only)

These four are judged only by the LLM, in context. No new observation code, no term list, and no regular expression; the phrasings below are context examples, and the same wording can be legitimate elsewhere. The three dispositions above stay unchanged.

Two of the four run in the opposite direction from the rest of this guide. "Concession that dismisses a confound" and "Over-strong claim with a vague concession" deal with wording that is **stronger** than the evidence, which is the over-claim guard's downward calibration. Deleting the concession on the instinct to "remove defensive wording" leaves an even stronger claim. All four therefore obey three constraints:

- When the concession points to a real difference or confound in the manuscript, the concession must not be deleted.
- The revised claim is no stronger than the source. None of the four authorizes raising a claim the evidence does not support, or deleting a limitation, an unfavorable comparison, or a non-mainline result.
- Never invent a control, a stratification, a significance test, a limitation, or a number. When the manuscript has nothing to write, mark it 【待补证】.

### Pre-emptive rebuttal shell

Scope: the sentence answers an objection that neither the manuscript's data nor the cited literature raises, and the answer itself adds no evidence, condition, or scope. Typical shapes: "这并不意味着 …", "不能简单地认为 …", "当然，有人可能认为 …". If the shell carries a condition, a scope, or evidence, it is a real boundary; handle it under "Keep a real evidence boundary" above.
Destination: when a real confound or alternative explanation exists, rewrite the shell as one concrete boundary that states its reason; when no real objection exists, delete the shell and keep the claim with its verb unchanged; when it is a definitional distinction, keep it and handle it under "Turn a negation into a positive statement" above.
Keep: in this thesis, "response time" is the interval from submitting a request to returning the first result and excludes queueing time. (definitional distinction)
Do not rewrite: delete the shell and at the same time change "本文方法缩短了响应时间" into "本文方法显著优化了系统性能"; delete "问卷不能说明受访者的实际使用频率" as a shell. That sentence is an evidence boundary.

### Concession that dismisses a confound

Scope: the concession clause points to a real difference or confound in the manuscript (a changed denominator, a shift in sample composition, a change in measurement), and the main clause dismisses its effect without analysis. Typical shape: "虽然 X 有所变化，但这并不影响 … 的判断". This is an over-claim, not self-weakening.
Destination: the concession must not be deleted. When the manuscript already has an analysis (stratification, adjustment, a common-sample comparison), bind the conclusion to that analysis and state where it is; when it has none, pull the conclusion back to what the data support, or mark it 【待补证】. Counts, proportions, and denominator changes go to `experiment --results-analysis` and `results-analysis-guide-zh.md` for checking.
Keep: community follow-up enrolment rose from 160 to 200, completed follow-ups from 128 to 150, and the follow-up completion rate fell from 80.0% to 75.0%. All 40 new enrollees come from two newly added residential compounds; stratified by compound, the completion rate stays at 80.0% (128/160) in the original compounds and is 55.0% (22/40) in the new compounds, so the overall fall comes from the change in enrolment composition (Table 5-3). (the concession is answered by a stratified analysis in the manuscript)
Do not rewrite: delete "虽然登记人数有变化" and keep only "新随访方案提高了随访依从性"; add "经分层检验差异不显著", which the source does not contain.

### Over-strong claim with a vague concession

Scope: one paragraph holds both a verb above its evidence rung ("充分证明", "决定因素") and a vague concession ("当然不能一概而论，但总体而言在一定程度上 …").
Destination: follow the repair order after the five-step rewrite: evidence first, calibrate the claim on the certainty ladder, then replace the vague concession with one concrete boundary that states its reason. The paragraph yields one finding only.
Keep: 9 of 14 interviewed teachers named "lack of demonstration lessons" as the main obstacle (Table 4-1). All interviewees come from one county, so the result reflects what the interviewed teachers report, not the actual effect of each obstacle. (claim calibrated, boundary with its reason)
Do not rewrite: delete only the vague concession and keep "充分证明"; split the claim and the concession into two findings and count them twice.

### Empty modesty

Scope: a limitation sentence names neither an object nor a condition or magnitude ("仍存在一定不足", "仍有提升空间", "具有一定参考价值"), and it is not a conclusion-chapter transition that already names the concrete limitation.
Destination: fill in the object and the condition or magnitude from the manuscript; when the manuscript has nothing to write, mark it 【待补证】 and do not make up a limitation for the author; when it repeats an existing limitation, delete the copy and keep the one where the evidence is discussed or in the "本文的不足" section.
Keep: a transition before the outlook in the conclusion chapter that names a concrete limitation, such as "所提方法在更复杂工况下的泛化能力仍存在一定不足". It satisfies the "limitation → transition → outlook" form that `CC-OUTLOOK-TRANS` requires, so leave it unchanged.
Do not rewrite: delete the only limitation; write a limitation the manuscript does not contain (such as "样本量偏小"); rewrite "仍有提升空间" as "已达到最优".

### Deduplication

- Throat-clearing openers ("值得注意的是", "需要强调的是") stay in `deai`. When one sentence holds both an opener and a pre-emptive rebuttal shell, `deai` reports the opener only and claim-forward outputs the shell disposition.
- When the script has already reported `CF-HEDGE-STACK` on a claim sentence that is also a concession shell, merge them into one finding: the shell disposition leads, and the hedge count is supporting evidence.
- One evidence gap yields one finding. An over-strong claim with a vague concession counts once; do not split it into an over-claim finding and a shell finding.
- Several specific mechanisms followed by a blanket retraction ("可能是 A，也可能是 B，现有数据无法验证") still belong to `deai` as defensive speculative explanation; do not report them again here.

Accurate and clear source text stays. Zero findings is a valid result; do not output findings to reach a count, and do not write what the manuscript leaves unknown as certain.

### Suggestion blocks

```latex
% 主张前置（合成）[Severity: Major] [Priority: P1]: [LLM] 断言与让步壳共现
% 问题：过强断言与模糊让步同段出现；只删让步会留下"充分证明"
% 上下文：表 4-2 已报告 312 份有效问卷中轮班组与固定班组的离职意向得分，数据为单一时点采集。
% 原文：问卷结果充分证明排班方式是离职意向的决定因素。当然，不能简单地认为所有科室都如此，但总体而言该因素在一定程度上起到了关键作用。
% 修改后：312 份有效问卷中，轮班组的离职意向得分高于固定班组（表 4-2）。问卷为单一时点的横断面数据，现有结果不能区分排班方式与科室工作量各自的影响。
% 理由：先证据前置，再把"充分证明 … 决定因素"收回到表 4-2 支持的组间比较，最后把模糊让步换成带原因的边界。改后断言强度不高于原文；数字与表号来自稿件，未新增结论。

% 主张前置（合成）[Severity: Major] [Priority: P1]: [LLM] 让步后否定
% 问题：让步句承认分母变化，主句不给分析就否定其影响
% 原文：虽然随访登记人数由 160 增至 200，完成率由 80.0% 降至 75.0%，但这并不影响新随访方案提高了随访依从性的判断。
% 修改后：随访登记人数由 160 增至 200，完成率由 80.0% 降至 75.0%。稿件未比较新增登记者与原有登记者的构成，现有数据不足以判断新随访方案是否提高了随访依从性【待补证：按原有与新增登记者分别报告完成率】。
% 理由：分母变化是真实混杂，让步内容保留；稿件没有分析，结论收回到数据支持的范围，未补造分层结果。分母口径交给 experiment --results-analysis 核对。

% 主张前置（合成）[Severity: Minor] [Priority: P2]: [LLM] 预设反驳壳
% 问题：回应了稿件与文献都未提出的异议，回应本身没有证据、条件或范围
% 原文：本文方法将平均响应时间由 420 ms 缩短至 310 ms。这并不意味着本文方法适用于所有场景。
% 修改后：本文方法将平均响应时间由 420 ms 缩短至 310 ms。
% 理由：删去壳，主张与数字不动。稿件写明了评估负载时，把它以肯定式范围附在主张上；稿件另有未评估的场景时，按真实边界写在主张之后。

% 主张前置（合成）[Severity: Minor] [Priority: P2]: [LLM] 空泛谦辞
% 问题：限制句没有对象、条件或量值
% 上下文：5.3 节已报告夜间场景的平均误差高于白天场景。
% 原文：本文方法仍存在一定不足，仍有提升空间。
% 修改后：本文方法在夜间场景下的平均误差高于白天场景（5.3 节）。
% 理由：对象与条件取自 5.3 节已报告的结果。稿件没有可写内容时，保留原句并标【待补证】，不替作者编局限，也不删除这处限制。
```
