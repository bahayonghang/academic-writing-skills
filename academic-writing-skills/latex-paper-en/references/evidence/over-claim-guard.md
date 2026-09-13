# Over-Claim Guard

Conservative-wording reference for English papers. The goal is **not** timid prose —
it is to state evidence strength precisely: strong evidence earns strong wording,
weak evidence gets weak wording.

## Boundary with `claim-evidence-contract.md`

- `claim-evidence-contract.md` decides **whether the visible evidence supports a claim**
  (the strength ladder `unsupported → observed → supported → strong`).
- This file decides **how to word a claim once its strength is known** (the verb/qualifier
  to pick so the sentence does not outrun the evidence).

Use them together: the contract sets the ceiling, this guide picks the wording under it.
Where they appear to conflict, the contract wins (it is about substance, not phrasing).

## Certainty ladder (verbs, strongest → weakest)

```
demonstrate / prove                         ← intervention + controlled experiment
  ↓
reveal / identify / find                    ← strong effect, multi-method or replicated
  ↓
indicate / suggest                          ← significant but single-method
  ↓
support / be consistent with                ← trend, agrees with prior work
  ↓
may indicate / could suggest / appear to    ← marginal or predictive
  ↓
hint at / point toward                      ← very weak signal or hypothesis
```

Pick the rung that matches the evidence. Do not climb a rung the data cannot reach.

## Substitution tables

### 1. Causal (the most common over-claim: correlation stated as causation)

| ❌ over-claim | ✅ conservative |
|---|---|
| caused by | associated with / linked to |
| drives / driving | contributes to / is associated with |
| determines | influences / shapes |
| responsible for | implicated in / associated with |
| results in | is followed by / co-occurs with |
| proves that | indicates / provides evidence that |

Causal wording is allowed only with a controlled intervention (ablation, randomized
assignment, A/B test), an instrumental-variable design, or an already-established
mechanism your data reproduce. Otherwise use association wording.

### 2. Novelty / firstness (reviewers verify these in seconds)

| ❌ over-claim | ✅ conservative |
|---|---|
| the first to | the first, to our knowledge / among the first to |
| novel (self-labeled) | name what is new; drop the label |
| unprecedented | substantial / notable |
| previously unknown | not extensively studied |

### 3. Universality (one setting studied, all settings claimed)

| ❌ over-claim | ✅ conservative |
|---|---|
| always / never | generally / rarely |
| in all cases | in the cases studied |
| universally | across the benchmarks evaluated |
| any dataset | the datasets sampled |

### 4. Effect size (vague magnitude word with no number)

| ❌ over-claim | ✅ conservative |
|---|---|
| strong improvement | reduces error by X% |
| large effect | β = X.XX (95% CI: …) |
| significant gain | improved from X to Y (p = …) |
| highly significant | p < 1 × 10⁻¹⁰ |
| robust | consistent across N runs / stable under [perturbation] |

If the number itself carries the weight, drop the adjective — the number speaks.

### 5. Temporal / inferred order (present data, past mechanism)

| ❌ over-claim | ✅ conservative |
|---|---|
| X drove the change | the change is consistent with X |
| occurred at time T | estimates suggest ~T (CI: …) |
| migrated from A to B | the data are consistent with a path A→B |

### 6. Application / impact (downstream uses not demonstrated here)

| ❌ over-claim | ✅ conservative |
|---|---|
| will revolutionize | has potential implications for |
| will be widely used | may be useful for / could inform |
| solves the problem of X | addresses one aspect of X |
| ready for deployment | provides a candidate approach for [setting] |

### 7. Comparison (disparaging prior work)

| ❌ over-claim | ✅ conservative |
|---|---|
| previous methods failed to | previous methods were limited by |
| outperforms all prior work | compares favorably with [specific methods] |
| resolves the long-standing debate | adds evidence to one side of the debate |

## High-frequency trap phrases

| trap | safe replacement |
|---|---|
| "Our results demonstrate X." (X causal) | "Our results are consistent with X." |
| "This is the first work to …" | "To our knowledge, among the first to …" |
| "X plays a critical role in Y." | "X has been implicated in Y / may contribute to Y." |
| "These findings have important implications for …" | "These findings provide a basis for further study of …" |
| "X is a key driver of Y." | "X is associated with Y." |
| "Strongly supports" | "Is consistent with / provides evidence in line with" |

## Reverse calibration: when NOT to hedge

Hedging weak evidence is right; hedging strong evidence is timid. Use strong wording when:

- a controlled intervention (ablation / RCT / A-B) gives a causal result → `demonstrate`;
- multiple methods / datasets / seeds replicate the result → `robustly`, with the evidence named;
- an established mechanism is reproduced → `confirms` / `validates`;
- a large effect with a strong statistic → strong wording **plus** the number.

## Upward calibration (claim-forward)

The ladder above is a ceiling, not a target. The opposite failure is prose that sits *below* the rung its evidence earns: a disclaimer before the claim, a limitation sentence in front of the result it qualifies, `regrettably` / `merely` / `falls short of` on the authors' own numbers, or a conclusion that ends on a new self-negation. The `claim-forward` module (`references/modules/claim-forward.md`, guide in `references/writing/claim-forward.md`) handles that direction.

Rules that keep the two directions consistent:

- Move wording **up to** the rung the evidence supports, never past it. Use the reverse-calibration list above to decide whether strong wording is earned; if it is not, fix the order of the sentences and leave the verb.
- Never delete a caveat, an unfavorable comparison, or a non-mainline result to sound decisive. Claim-forward changes order and wording; the content of every limitation stays.
- Write each limitation once, where the evidence is discussed. Removing a *duplicate* caveat is calibration; removing the *only* copy is an over-claim.
- Report a gap as a measurement ("trails the oracle by 4.1 points"), not as an apology ("regrettably still lags far behind").

## Self-check (scan after drafting a paragraph)

- [ ] Used `first` / `novel`? Did you actually search the literature, or add "to our knowledge"?
- [ ] Used `cause` / `drive` / `determine`? Is there an intervention? If not → `associated with`.
- [ ] Used `all` / `always` / `universally`? Is the scope bounded to what you studied?
- [ ] Used `significant` / `strong` / `substantial`? Is a number attached?
- [ ] Listed implications you did not demonstrate? Add `may` / `could`.
- [ ] Disparaged prior work? Reframe to "limited by", not "failed".

## Script support

`deai_check.py` flags a focused set of unambiguous over-claim phrases (causal /
firstness / universality / application) as `[Script]` LOW traces and points back to
this guide. The script is a safety net for the obvious cases; the tables above cover
the judgment calls it cannot make.
