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
