# Abstract Section Writing

## Objective

Make the abstract readable in one pass: task, challenge, core technical idea, evidence-backed result, and implication must be visible without forcing the reader into the full paper.

## Choose One Logic Pattern

| Pattern | Use When | Paragraph Roles |
| --- | --- | --- |
| Challenge -> Contribution | One main technical contribution solves a clear bottleneck | task, challenge, contribution, benefit, evidence |
| Challenge -> Insight -> Contribution | The key novelty is an insight before an implementation | task, challenge, insight, implementation, evidence |
| Multiple Contributions | The paper has 2-3 separable technical contributions | task, contribution+advantage, contribution+advantage, result |

## Rewrite Workflow

1. Extract visible evidence from the paper first: named method, datasets, metrics, tables/figures, and contribution claims.
2. Decide the abstract pattern above.
3. Keep each sentence to one role; avoid mixing task definition, method mechanics, and result claims in one overloaded sentence.
4. Mention technical names only after they are readable from context.
5. Bound result language to the reported setting.

## Claim-Evidence Guardrails

- A result sentence needs a metric, dataset/setting, and table/figure or section anchor when available.
- A novelty sentence needs a method or contribution anchor in Introduction/Method.
- If the current paper lacks numbers, write `results suggest` or `experiments indicate` only when the local experiment section actually supports it.
- Do not add a new result, dataset, or baseline because an abstract "needs" one.

## Output Pattern

```text
Section objective: ...

Paragraph roles:
1. Task/challenge: ...
2. Insight/contribution: ...
3. Evidence/implication: ...

Proposed abstract:
[Only if requested]

Claim-evidence map:
Claim: ... | Evidence: Table/Figure/Section/... | Status: supported/needs evidence/unsupported
```
