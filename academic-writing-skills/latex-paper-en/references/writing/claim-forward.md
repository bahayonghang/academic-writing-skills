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

**Supplement: repair order.** The five steps are unchanged. When one paragraph holds both an over-strong claim and a vague concession (see "Over-strong claim with a vague concession" below), repair it in three fixed steps: (1) put the evidence first: the number, table, figure, or material that supports the claim; (2) calibrate the claim on the certainty ladder in `over-claim-guard.md`, down to the rung the evidence supports and no further; (3) replace the vague concession with one concrete boundary that states its reason. Doing step (3) alone removes the concession and leaves the over-strong claim in place; do not edit that way.

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

## Three LLM-only dispositions for necessary caveats

These three are judged by the LLM only. No new observation code and no term list; unfavorable results must not be deleted. The strength ceiling is still the one in "Interaction with the over-claim guard" above. Unverified weaknesses must not be written as design strengths.

### Keep a real evidence boundary

Scope: removing the sentence would make a reader question the method's validity or the level of evidence.
May keep: "We report agreement with expert labels on the held-out clinic only; we do not treat this agreement as evidence of diagnostic benefit."
Must not: delete that sentence and leave only "Our classifier improves diagnosis."

### Turn a negation into a positive statement

Scope: only when the source already supports the positive wording. The distinction must survive.
May keep: "The survey measures self-reported study time. Logged study time is analysed separately in Section 5."
Must not: rewrite "We do not equate self-reported and logged study time" as "Self-reported study time accurately reflects actual effort."

### Write a weakness as a trade-off

Scope: only when the manuscript already presents the weakness as a real design choice.
May keep: "Recall on rare classes is lower than the baseline. Section 3.4 states that the loss weights frequent classes to bound annotation cost, and rare-class recall is not a design target."
Must not: rewrite "rare-class recall is lower" as "the model effectively avoids over-fitting to rare classes". Unverified weaknesses must not be written as design strengths. A false-alarm rate above the baseline must not be deleted, and must not be rewritten as "therefore more conservative".

### Context words are examples, not a word list

"Gatekeeper", "bulletproof", "inherently safe", and "theoretical upper bound" are context examples, not a banned-word regex. If the context already names a check, a block, or a fallback, write that observable mechanism. Do not build a banned-word list from them.

### Suggestion blocks

```latex
% CLAIM-FORWARD (synthetic) [Severity: Minor] [Priority: P2]: [LLM] Keep a real evidence boundary
% Problem: a limitation reads as self-weakening, but the boundary is the evidence level
% Original: We report agreement with expert labels on the held-out clinic only; we do not treat this agreement as evidence of diagnostic benefit.
% Revised: keep the sentence unchanged.
% Rationale: removing the boundary would turn label agreement into a diagnostic-benefit claim. LLM-only judgment.

% CLAIM-FORWARD (synthetic) [Severity: Major] [Priority: P1]: [LLM] Unverified weakness written as a design strength
% Problem: lower rare-class recall became a claimed benefit, and the unfavorable number was dropped
% Original: Rare-class recall is lower than the baseline. The false-alarm rate is higher than the baseline.
% Revised: keep both observations. Add "the loss weights frequent classes to bound annotation cost" only if the manuscript already states that design choice.
% Rationale: unverified weaknesses must not be written as design strengths; unfavorable results must not be deleted.
```

## Four LLM-only dispositions for rebuttal and concession shells

These four are judged by the LLM only, in context. No new observation code and no term list, and no regex: the phrasings below are context examples, and the same words can be legitimate elsewhere. The three dispositions above stay as they are.

Two of the four run in the opposite direction from the rest of this guide. "Concession that dismisses a confound" and "Over-strong claim with a vague concession" deal with wording that is *stronger* than the evidence, which is the over-claim guard's downward calibration. Deleting the concession on the instinct to "remove hedging" leaves a stronger claim behind. All four therefore obey three constraints:

- Never delete the concession when it points to a real difference or confound in the manuscript.
- The revised claim is no stronger than the source. None of the four licenses raising an unsupported claim, and none licenses deleting a limitation, an unfavorable comparison, or a non-mainline result.
- Never invent a control, a stratified analysis, a significance test, a limitation, or a number. When the manuscript has nothing to write, mark `needs evidence`.

### Pre-emptive rebuttal shell

Scope: the sentence answers an objection that neither the manuscript's data nor the cited literature raises, and the answer itself adds no evidence, condition, or scope. Typical shapes: "This does not mean that ...", "One should not simply conclude that ...", "Admittedly, some may argue that ...". If the shell carries a condition, a scope, or evidence, it is a real boundary; handle it under "Keep a real evidence boundary".
Destination: when a real confound or alternative explanation exists, rewrite the shell as one concrete boundary that states its reason; when no real objection exists, delete the shell and keep the claim with its verb unchanged; when it is a definitional distinction, keep it (see "Turn a negation into a positive statement").
May keep: "In this paper, latency is the interval from request submission to the first returned result; queueing time is excluded." (definitional distinction)
Must not: delete the shell and at the same time upgrade "reduces latency" to "substantially improves system performance"; delete "The interviews cannot tell us how often teachers actually use the tool" as a shell. That sentence is an evidence boundary.

### Concession that dismisses a confound

Scope: the concession clause names a real difference or confound in the manuscript (a changed denominator, a shift in sample composition, a change in measurement), and the main clause dismisses its effect without analysis. Typical shape: "Although X changed, this does not affect the conclusion that ...". This is an over-claim, not self-weakening.
Destination: never delete the concession. When the manuscript already has an analysis (stratification, adjustment, a common-sample comparison), bind the conclusion to that analysis and cite where it is; when it has none, pull the conclusion back to what the data support, or mark `needs evidence`. Counts, proportions, and denominator changes go to the `experiment` module and `references/evidence/claim-evidence-contract.md`.
May keep: "Enrolment rose from 200 to 250 and completions from 150 to 175, so the completion rate fell from 75.0% to 70.0%. All 50 new enrollees joined the part-time track; within each track the completion rate did not fall (Table 4)." (the concession is answered by an analysis in the manuscript)
Must not: delete "although enrolment changed" and keep "the redesign improved completion"; add "stratified tests showed no significant difference" when the manuscript reports no such test.

### Over-strong claim with a vague concession

Scope: one paragraph holds both a verb above its evidence rung ("conclusively proves", "the decisive factor") and a vague concession ("of course this may not hold everywhere, but overall it plays a key role to some extent").
Destination: follow the repair order after the five-step rewrite: evidence first, calibrate the claim on the certainty ladder, then replace the vague concession with one concrete boundary that states its reason. Report the paragraph as one finding.
May keep: "Nine of the 14 interviewed nurses named missing handover templates as the main obstacle (Table 2). All interviewees work in one hospital, so the result reports what the nurses said, not the measured effect of each obstacle." (claim calibrated, boundary with its reason)
Must not: delete only the vague concession and keep "conclusively proves"; report the claim and the concession as two findings.

### Empty modesty

Scope: a limitation sentence names neither an object nor a condition or magnitude ("there remain certain limitations", "there is still room for improvement", "this work offers some reference value"), and it is not a closing transition that already names the concrete limitation.
Destination: fill in the object and the condition or magnitude from the manuscript; when the manuscript has nothing to write, mark `needs evidence` and do not make up a limitation for the authors; when it repeats an existing limitation, delete the duplicate and keep the copy where the evidence is discussed or in the Limitations section.
May keep: a closing transition that names the limitation before the outlook, such as "Generalisation to multi-site deployments remains limited because all data come from one hospital; Section 6 outlines the multi-site study."
Must not: delete the only limitation; write a limitation the manuscript does not contain (such as "the sample is small"); rewrite "there is still room for improvement" as "the method is optimal".

### Deduplication

- Throat-clearing openers ("It is worth noting that", "It should be emphasized that") stay in `deai`. When one sentence holds both an opener and a pre-emptive rebuttal shell, `deai` reports the opener only and claim-forward handles the shell.
- When the script has already reported `CF-HEDGE-STACK` on a claim sentence that is also a concession shell, merge them into one finding: the shell's disposition leads, and the hedge count is supporting evidence.
- One evidence gap yields one finding. An over-strong claim with a vague concession counts once; do not split it into an over-claim finding and a shell finding.
- Several specific mechanisms followed by a blanket retraction ("it may be A, or B; the current data cannot verify this") still belong to the `deai` defensive-speculation rule; do not report them here again.

Accurate and clear source text stays as it is. Zero findings is a valid result; do not produce findings to reach a count, and do not write what the manuscript leaves unknown as certain.

### Suggestion blocks

```latex
% CLAIM-FORWARD (synthetic) [Severity: Major] [Priority: P1]: [LLM] Over-strong claim with a vague concession
% Problem: an over-strong claim and a vague concession share one paragraph; deleting only the concession would keep "conclusively proves"
% Context: Table 2 already lists the 14 nurse interviews from one hospital and the obstacle each nurse named first.
% Original: The interviews conclusively prove that missing handover templates are the decisive obstacle. Of course, this may not hold in every ward, but overall the templates play a key role to some extent.
% Revised: Nine of the 14 interviewed nurses named missing handover templates as the main obstacle (Table 2). All interviewees work in one hospital, so the result reports what the nurses said, not the measured effect of each obstacle.
% Rationale: evidence first; "conclusively prove ... decisive" pulled back to the count in Table 2; the vague concession replaced by a boundary with its reason. The revised claim is no stronger than the source; numbers and table come from the manuscript.

% CLAIM-FORWARD (synthetic) [Severity: Major] [Priority: P1]: [LLM] Concession that dismisses a confound
% Problem: the concession admits a denominator change, and the main clause dismisses it without analysis
% Original: Although enrolment rose from 200 to 250 and the completion rate fell from 75.0% to 70.0%, this does not affect the conclusion that the redesign improved completion.
% Revised: Enrolment rose from 200 to 250 and the completion rate fell from 75.0% to 70.0%. The manuscript does not compare new and returning enrollees, so the current data cannot show whether the redesign improved completion (needs evidence: completion rates reported separately for new and returning enrollees).
% Rationale: the denominator change is a real confound, so the concession's content stays; with no analysis in the manuscript, the conclusion is pulled back to what the data support. No stratified result was invented. Denominator checks go to the experiment module.

% CLAIM-FORWARD (synthetic) [Severity: Minor] [Priority: P2]: [LLM] Pre-emptive rebuttal shell
% Problem: the sentence answers an objection nobody raised and adds no evidence, condition, or scope
% Original: Our method reduces mean latency from 420 ms to 310 ms. This does not mean that it suits every workload.
% Revised: Our method reduces mean latency from 420 ms to 310 ms.
% Rationale: shell deleted; claim and numbers unchanged. If the manuscript names the evaluated workloads, attach them as positive scope; if it names workloads it did not evaluate, keep that as a real boundary after the claim.

% CLAIM-FORWARD (synthetic) [Severity: Minor] [Priority: P2]: [LLM] Empty modesty
% Context: Section 5.3 already reports a higher mean error at night than in daytime.
% Original: Our method still has certain limitations and room for improvement.
% Revised: Our method has a higher mean error at night than in daytime (Section 5.3).
% Rationale: object and condition come from the result in Section 5.3. When the manuscript has nothing to write, keep the sentence and mark it `needs evidence`; do not invent a limitation and do not delete this one.
```
