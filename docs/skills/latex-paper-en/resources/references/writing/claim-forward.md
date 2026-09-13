# Claim-Forward Writing Guide

How to state a contribution so the reader meets the claim before the caveat, without removing a single limitation or unfavorable result. Companion to the `claim-forward` module (`references/modules/claim-forward.md`) and to the "Upward calibration" section of `references/evidence/over-claim-guard.md`.

## The one rule

**Claim first, scope second, limitation once.** Every paragraph that carries a contribution opens with the contribution. The scope (what the claim covers) follows it in positive form. Each limitation is written once, in the place the reader expects it (Methods for design constraints, Discussion or a Limitations section for evidence boundaries), and is not repeated as a hedge in front of every claim.

## What this guide does not permit

These edits are rejected on purpose. They conflict with the over-claim guard ("calibration, not timid prose", never delete a caveat to sound decisive), with the claim-evidence contract, and with reviewer cherry-picking checks:

- Deleting an unfavorable comparison, a failed setting, or a non-mainline result.
- Rewriting a technical shortcoming as a "scope choice" ("we do not target long sequences" when the method breaks on them).
- Choosing baselines or metrics so the paper "cannot lose".
- Strengthening a verb past the rung the evidence earns (see the certainty ladder in the over-claim guard).

Claim-forward changes **order and wording**. Content stays.

## Sentence functions (classify before editing)

| Function   | Test                                                                   | Where it belongs                                                                 |
| ---------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Claim      | States what the work achieves, with or without a number                | First sentence of the paragraph                                                  |
| Evidence   | Points to a table, figure, statistic, or comparison                    | Immediately after the claim                                                      |
| Scope      | Says what the claim covers, in positive terms ("on indoor benchmarks") | Inside or right after the claim                                                  |
| Limitation | Says what the claim does not cover or where it fails                   | After the claim; once per limitation; or in Limitations                          |
| Transition | Links to the next paragraph                                            | Last sentence                                                                    |
| Process    | Narrates what the authors tried and when                               | Usually deleted from Results; belongs in Methods if the reader must reproduce it |

## Five-step rewrite

1. **Locate the claim.** Find the sentence that states the contribution. If there is none, the paragraph needs a claim before any other edit (do not invent one; ask the author).
2. **Move the claim first.** Put it before any disclaimer, apology, or limitation in the paragraph.
3. **Turn scope positive.** "We do not handle outdoor scenes" becomes "on three indoor benchmarks" attached to the claim. The negative sentence is removed only if the positive scope now carries the same information; otherwise it stays after the claim.
4. **Place each limitation once.** If the same caveat appears in Abstract, Introduction, and Results, keep it where the evidence is discussed and where a Limitations paragraph exists. The other copies are the ones to remove, not the limitation itself.
5. **Minimal edit and check.** Re-read: is every number, comparison, and caveat still present? Does any verb now sit above its evidence rung? If yes, step back down.

## Preferred and discouraged patterns

| Discouraged                                                                                  | Preferred                                                                                                                                         | Why                                                            |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| "We do not claim generality. Our method improves accuracy by 12%."                           | "Our method improves accuracy by 12% on three indoor benchmarks. We do not evaluate outdoor scenes."                                              | Claim first; scope positive; the boundary stays                |
| "Regrettably, our method still lags far behind the oracle."                                  | "Our method trails the oracle by 4.1 points on the long-tail split."                                                                              | State the gap as a measurement, not an apology                 |
| "Although the evaluation is limited to one dataset, we show a 7% gain."                      | "We show a 7% gain on Dataset X. Evaluation on further datasets is future work."                                                                  | Limitation after the claim, with a direction                   |
| "Our approach may potentially improve robustness to some extent in some cases."              | "Our approach improves robustness under occlusion (Table 3)." or, if the evidence is weak, "Our approach may improve robustness under occlusion." | One hedge, chosen by the evidence                              |
| "It only reaches 91% and merely matches the baseline."                                       | "It reaches 91%, matching the baseline at one third of the cost."                                                                                 | Report the number with the trade-off, not with `only`/`merely` |
| "We first tried a transformer, which failed, then a CNN, which also failed, and finally ..." | "We use a hybrid encoder (Section 3.2); Appendix B reports the alternatives we evaluated."                                                        | Process chronology moves out of Results (`CF-LOSS-FRAME`)      |
| Conclusion ending: "However, the method does not handle variable frame rates."               | "... does not yet handle variable frame rates; extending the buffer to asynchronous input is the next step."                                      | Close on a direction, keep the judgment                        |

## Self-check (four questions, run after the rewrite)

1. Is the first sentence of each contribution paragraph the claim?
2. Does every limitation sit after the claim it qualifies, and appear only once?
3. Is every `regrettably` / `merely` / `only` / `unfortunately` / `falls short` replaced by a measured value or a positive scope?
4. Does the closing paragraph add a direction after its last limitation instead of a new self-negation?

If answering any question required deleting a comparison, a result, or a caveat, undo that edit.

## Codes emitted by the script

| Code             | Layer        | What to do                                                                                         |
| ---------------- | ------------ | -------------------------------------------------------------------------------------------------- |
| `CF-DISCLAIM`    | `[Script]`   | Step 2 (move the claim first)                                                                      |
| `CF-CAVEAT-POS`  | `[Script]`   | Step 2 and step 4                                                                                  |
| `CF-SELFWEAK`    | `[Script]`   | Replace the collocation with a measurement; fill `{placeholders}` from the manuscript only         |
| `CF-HEDGE-STACK` | `[Script]`   | Keep one hedge; check the over-claim ladder first                                                  |
| `CF-CLOSE-NEG`   | `[Script]`   | Add the direction; keep the judgment                                                               |
| `CF-LOSS-FRAME`  | `[LLM]` only | Move process chronology out of Results/Conclusion; keep the alternatives in Methods or an appendix |

## Interaction with the over-claim guard

The over-claim guard corrects downward (evidence weaker than the wording). Claim-forward corrects upward (wording weaker than the evidence). They meet at the same ladder: a claim-forward rewrite may raise a verb only to the rung the evidence already supports, and the guard's reverse-calibration list ("when NOT to hedge") names the cases where strong wording is earned. When unsure, leave the verb and fix only the order.

## Attribution

Adapted, with the rejections noted above, from two MIT-licensed skills:

- Kiterlin, _anti-defensive-writing_ — https://github.com/Kiterlin/anti-defensive-writing (sentence-function classification, five-step rewrite, preferred/discouraged patterns, "write limitations once").
- Adkid-Zephyr, _anti-defensive-writing-Skill_ — https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill (claim-before-limitation ordering, self-weakening word list, "no new self-negation in the conclusion", minimal-edit prompt, self-check questions). Its rules on selective presentation (organize only around strengths, avoid comparisons you cannot win, delete non-mainline results) are not adopted; see "What this guide does not permit".
