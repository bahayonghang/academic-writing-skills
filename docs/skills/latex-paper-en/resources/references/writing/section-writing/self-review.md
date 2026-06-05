# Reviewer-Facing Self-Review

## Objective

Read the section as a skeptical reviewer and surface rejection risks before strengthening prose.

## Five-Dimension Checklist

| Dimension | Questions |
| --- | --- |
| Contribution | What new knowledge does this section make visible? Is the novelty type clear? |
| Writing clarity | Can a knowledgeable reader follow the paragraph roles, terms, and notation? |
| Experimental strength | Are performance or result claims supported by visible metrics and settings? |
| Evaluation completeness | Are baselines, ablations, metrics, and datasets sufficient for the claims? |
| Method soundness | Are assumptions, module motivations, and limitations explicit? |

## Claim-Evidence Map

Use this compact shape in responses:

```text
Claim: exact claim or proposed claim
Evidence: citation / figure / table / metric / method section / missing
Status: supported / needs evidence / unsupported
Safe wording: bounded wording that fits the visible evidence
Missing evidence: concrete experiment, citation verification, comparison, or detail
```

## Revision Decisions

- `supported`: keep the claim, but preserve setting boundaries.
- `needs evidence`: keep only as a weak or conditional claim, or request the missing anchor.
- `unsupported`: remove, soften, or mark as pending evidence.

## Rejection-Risk Signals

- A major Abstract or Introduction claim has no experiment evidence.
- A method module has no motivation or ablation.
- Related Work omits the strongest comparator.
- Discussion repeats results without mechanism or limitation.
- Conclusion claims the problem is solved beyond the evaluated setting.
