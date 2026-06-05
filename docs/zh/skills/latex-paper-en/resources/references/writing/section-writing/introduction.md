# Introduction Section Writing

## Objective

Build a reviewer-facing funnel: meaningful task -> unmet target or failure case -> root technical bottleneck -> proposed solution -> why it works -> evidence and contributions.

## Backward Planning Questions

Answer these before writing:

1. What technical problem is solved, and why is there no established solution?
2. What exactly is new: task, metric, pipeline, module, design choice, finding, or insight?
3. Why should this contribution solve the bottleneck?
4. Which experiments or analyses later support the main promises?

## Forward Section Roles

| Role | Required Content | Failure Signal |
| --- | --- | --- |
| Task/application opening | Define task or application value and target requirement | Opens with generic importance but no task boundary |
| Prior-work limitation | Summarize representative methods by mechanism and limitation | Paper-by-paper list with no technical reason |
| Technical bottleneck | State the unresolved challenge and root cause | Gap is a marketing claim, not a mechanism |
| Proposed solution | Introduce pipeline or key insight with a figure anchor if present | Method appears before the challenge is clear |
| Why it works | Explain technical advantage in bounded terms | Claims novelty without mechanism |
| Evidence/contributions | Preview experiments and enumerate contributions | Contributions do not map to later evidence |

## Introduction Patterns

Use one pattern that matches the paper:

- **Task first**: for niche tasks; define input/output before applications.
- **Application first**: for familiar tasks; open with use cases and target requirements.
- **General-to-specific**: for a new setting inside a familiar area.
- **Open with challenge**: when the unresolved failure case is immediately understandable.

## Anti-Pattern

Do not write the story as "a naive baseline exists, then we patch it." That makes the contribution look obvious. Instead, explain the real technical bottleneck that prior families of methods still cannot resolve.

## Claim-Evidence Closure

Every contribution sentence should map forward:

```text
Intro promise -> Method mechanism -> Experiment evidence -> Conclusion answer
```

If a contribution has no corresponding experiment or analysis, either mark missing evidence or weaken the claim.
