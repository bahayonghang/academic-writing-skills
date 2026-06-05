# Experiments And Discussion Section Writing

## Objective

Convince reviewers that the paper's claims are empirically tested: effectiveness, causal contribution, robustness, and realistic limits should be visible.

## Claim-To-Experiment Plan

Start from the paper's main claims:

| Claim Type | Evidence Needed |
| --- | --- |
| Better performance | strong/recent baselines, same protocol, standard metrics |
| Module contributes | ablation removing/replacing the module |
| Robustness/generalization | harder settings, OOD cases, sensitivity analysis |
| Efficiency | runtime, memory, parameter count, or deployment setting |
| Mechanistic explanation | qualitative results, error analysis, or discussion tied to design |

If a claim has no matching experiment, mark `needs evidence` rather than writing around the gap.

## Section Roles

1. **Setup**: datasets, metrics, baselines, implementation settings, and protocol fairness.
2. **Main comparison**: one message per table/figure; state the comparison target and bounded conclusion.
3. **Ablation**: connect each design choice to a result delta.
4. **Analysis/discussion**: explain why results occur; compare to related work when appropriate.
5. **Limitations**: state scope boundaries or failure cases honestly.

## Table And Figure Communication

- One table, one message.
- Put metric direction in headers when possible, such as `PSNR ↑` or `LPIPS ↓`.
- Keep captions focused on setting/protocol/notation.
- Do not claim significance unless variance, statistical test, or repeated-run evidence is visible.

## Discussion Layering

A strong discussion does not repeat numbers. It should move through:

```text
finding -> mechanism/interpretation -> comparison to prior work -> limitation or implication
```

Do not add prior-work comparisons unless the referenced work is already cited or the user asks for verified literature work.
