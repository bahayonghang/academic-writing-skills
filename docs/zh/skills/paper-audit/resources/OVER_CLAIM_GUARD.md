# Over-Claim Guard (Audit Lane Reference)

Reference for the `claims_vs_evidence` lane: how to spot wording that outruns the evidence,
and the conservative wording it should be revised to. The goal is **calibration**, not timid
prose — strong evidence earns strong wording; weak evidence must use weak wording.

## Boundary with `CLAIM_EVIDENCE_CONTRACT.md`

- `CLAIM_EVIDENCE_CONTRACT.md` decides **whether the visible evidence supports a claim**
  (the strength ladder `unsupported → observed → supported → strong`).
- This file decides **how a claim should be worded once its strength is known** (which
  verb / qualifier keeps the sentence inside the evidence).

In a finding, set `claim_strength` from the contract and put the bounded rewrite in
`allowed_wording` / the overreaching phrasing in `forbidden_wording`. Where they conflict,
the contract wins (substance over phrasing). Emit these as `comment_type: claim_accuracy`.

## Certainty ladder (verbs, strongest → weakest)

```
demonstrate / prove                         ← intervention + controlled experiment
reveal / identify / find                    ← strong effect, multi-method or replicated
indicate / suggest                          ← significant but single-method
support / be consistent with                ← trend, agrees with prior work
may indicate / could suggest / appear to    ← marginal or predictive
hint at / point toward                      ← very weak signal or hypothesis
```

Flag any claim whose verb sits above the rung its evidence can reach.

## Substitution tables (flag ❌ → suggest ✅)

### 1. Causal (correlation stated as causation — the most common over-claim)

| ❌ over-claim | ✅ conservative |
|---|---|
| caused by | associated with / linked to |
| drives / determines | contributes to / is associated with |
| responsible for | implicated in / associated with |
| proves that | indicates / provides evidence that |

Causal wording is justified only with a controlled intervention (ablation, randomized
assignment, A/B test), an instrumental-variable design, or a reproduced established mechanism.

### 2. Novelty / firstness (reviewers verify these in seconds)

| ❌ over-claim | ✅ conservative |
|---|---|
| the first to | the first, to our knowledge / among the first to |
| novel (self-labeled) | name what is new; drop the label |
| unprecedented | substantial / notable |

### 3. Universality (one setting studied, all settings claimed)

| ❌ over-claim | ✅ conservative |
|---|---|
| always / never | generally / rarely |
| in all cases / universally | in the cases studied / across the benchmarks evaluated |
| any dataset | the datasets sampled |

### 4. Effect size (vague magnitude word, no number)

| ❌ over-claim | ✅ conservative |
|---|---|
| strong / large improvement | reduces error by X% / β = X.XX (95% CI: …) |
| significant gain | improved from X to Y (p = …) |
| robust | consistent across N runs / stable under [perturbation] |

If the number carries the weight, the adjective should be dropped.

### 5. Temporal / inferred order (present data, past mechanism)

| ❌ over-claim | ✅ conservative |
|---|---|
| X drove the change | the change is consistent with X |
| occurred at time T | estimates suggest ~T (CI: …) |

### 6. Application / impact (downstream uses not demonstrated here)

| ❌ over-claim | ✅ conservative |
|---|---|
| will revolutionize | has potential implications for |
| solves the problem of X | addresses one aspect of X |
| ready for deployment | provides a candidate approach for [setting] |

### 7. Comparison (disparaging prior work)

| ❌ over-claim | ✅ conservative |
|---|---|
| previous methods failed to | previous methods were limited by |
| outperforms all prior work | compares favorably with [specific methods] |

## High-frequency trap phrases

| trap | safe rewrite |
|---|---|
| "Our results demonstrate X." (X causal) | "Our results are consistent with X." |
| "This is the first work to …" | "To our knowledge, among the first to …" |
| "X plays a critical role in Y." | "X has been implicated in Y / may contribute to Y." |
| "These findings have important implications for …" | "These findings provide a basis for further study of …" |
| "Strongly supports" | "Is consistent with / provides evidence in line with" |

## When NOT to flag (reverse calibration)

Do not flag strong wording that the evidence earns:

- a controlled intervention (ablation / RCT / A-B) → `demonstrate` is fine;
- multiple methods / datasets / seeds replicate the result → `robustly` (with evidence named);
- a reproduced established mechanism → `confirms` / `validates`;
- a large effect with a strong statistic stated → strong wording **plus** the number.

Flagging earned strong wording is a false positive — leave it.

## How the lane uses this

The `claims_vs_evidence` lane flags over-claim wording as `claim_accuracy` findings with
`allowed_wording` / `forbidden_wording` filled in. This is the LLM-judgment complement to the
writing skills' `deai_check.py` over-claim script, which only catches a few unambiguous
phrases; the tables above cover the contextual judgment the script cannot make.
