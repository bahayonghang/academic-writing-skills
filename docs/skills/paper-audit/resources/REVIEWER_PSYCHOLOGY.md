# Reviewer Psychology

How a reviewer actually reads a paper, and **where they stop to doubt**. Use this to
**prioritize audit findings**: an issue that sits where reviewers reliably get
suspicious matters more than one they would never reach. Reading path and the
suspicion ranking below are general across venues (CS / ML / quantitative science);
they are about reviewer behavior, not any single field.

## How reviewers read (not front-to-back)

A reviewer handling 3-5 papers in a cycle, ~3-6 hours each, does not read linearly:

```
Step 1 (3-5 min):   Title -> Abstract -> Figure 1 -> Conclusion
                    => "is this worth reading deeply?"  (>50% of accept/reject leaning forms here)
Step 2 (10-20 min): skim all figures + captions -> skim key Methods parameters
                    => "does the data support the claims / is the method credible?"
Step 3 (1-3 h):     Results + Discussion in detail
                    => hunt for over-claims, logic gaps, missing experiments
Step 4 (~30 min):   Introduction close read + spot-check appendix -> write the review
```

Optimizing for **Step 1** has the highest payoff. The audit should weight problems that
a reviewer hits early (title/abstract/figure-1/conclusion) above problems buried deep.

## The 3-second scan

In the first seconds a reviewer registers the title (right keywords? claim overreaching?),
the author list, and the venue. Within 30 seconds: the **first sentence of the abstract**
(empty throat-clearing or a concrete gap?), the **last sentence of the abstract** (does the
claim overreach?), and **Figure 1** (understandable at a glance?).

## Where reviewers stop to doubt — ranked by how often it happens

Order findings by this list. Higher = a reviewer is more likely to catch it and let it
sink the paper, so it should rank higher in the audit roadmap (within the same severity).

1. **Numbers that do not match the claim.** "significantly higher" with no number; the
   abstract says 184, the body says 178; "2× faster" but the figure shows less.
   → _Auditor_: cross-check every number across abstract / body / figures / tables; flag
   every magnitude word with no number. (lanes: `notation_and_numeric_consistency`, `claims_vs_evidence`)
2. **Missing method parameters.** "We ran PCA / fine-tuned" with no version, no
   hyperparameters, no threshold, no multiple-testing correction.
   → _Auditor_: flag undisclosed parameters that block reproduction. (lane: `evaluation_fairness_and_reproducibility`)
3. **Weak citation support.** A specific claim backed only by reviews; a citation whose
   actual conclusion is the opposite; a whole paragraph with no citation.
   → _Auditor_: flag claims without a primary-source anchor. (lane: `prior_art_and_novelty_grounding`)
4. **Over-claim.** "first to" (when it is not), causal language on correlational evidence,
   "universally" from one setting, undemonstrated downstream applications.
   → _Auditor_: see `OVER_CLAIM_GUARD.md`; flag wording that outruns the evidence. (lane: `claims_vs_evidence`)
5. **Story does not close.** Intro promises A, B, C; Results only deliver A and B. Abstract
   stresses X; the body barely covers X.
   → _Auditor_: check contribution-to-result closure end to end. (lane: `claims_vs_evidence`, section lanes)
6. **Figures disconnected from text.** Text cites "Figure 2A" that does not exist; missing
   axis units / legends / scale bars; color choices hostile to color-blind readers.
   → _Auditor_: cross-check figure references and self-containment. (lanes: section lanes, `notation_and_numeric_consistency`)
7. **Language that blocks understanding.** Long multiply-negated sentences; **tense misuse**
   (Methods/Results not in past tense) that blurs method vs. result vs. inference; undefined
   abbreviations on first use.
   → _Auditor_: flag clarity blockers; tense is covered by the writing skills' de-AI tense
   check and should be noted when it impedes reading. (lane: section lanes)
8. **Results "too clean."** Every p-value < 0.001; every effect in the predicted direction;
   sample size conveniently sufficient in every comparison.
   → _Auditor_: note absence of negative / marginal / inconsistent results and limitations. (lane: `evaluation_fairness_and_reproducibility`)

## Reviewer types on a panel

A paper usually gets 2-3 reviewers of these kinds — write (and audit) for all three:

- **Domain expert** — cares whether your data conflict with published work and whether you
  cite the core literature. Audit: literature grounding, honest positioning.
- **Method expert** — cares whether the method choice is justified and parameters are sound.
  Audit: methods detail, fairness of comparison, ablations.
- **Generalist / editor** — cares about "so what" and whether a non-specialist can follow the
  abstract and introduction. Audit: accessibility of abstract/intro, significance framing.

## Making the paper "reject-proof"

Reviewers often decide first and then look for evidence to justify it. The defensive moves
an audit should check are present:

1. Title + abstract carry no over-claim smell (`OVER_CLAIM_GUARD.md`).
2. Figure 1 is understandable in seconds.
3. Key parameters are fully disclosed (kills "is this reproducible?").
4. Limitations are stated by the authors (kills "they ignored the obvious weakness").
5. Data + code + supplementary are available (kills "can this be trusted?").

When these are present, the only thing left to attack is the core claim itself — which is
exactly the high-level discussion a strong paper wants.

## How this skill uses it

- **Critical reviewer** orders its challenges by the suspicion ranking above (highest first).
- **Synthesis** breaks ties _within_ a severity tier by suspicion rank, so the revision
  roadmap surfaces what a real reviewer hits first.
- This file changes **ordering and emphasis**, not severity definitions — severities still
  follow `REVIEW_CRITERIA.md` / `editorial_decision_standards.md`.
