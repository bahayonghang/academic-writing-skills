# Claim-Evidence Contract

This reference defines the lightweight contract used when a writing or audit flow needs to judge whether manuscript claims are supported by visible evidence. It is an advisory contract, not permission to invent missing evidence.

## Claim Candidate Record

Use this shape when emitting a claim-evidence map:

```json
{
  "claim": "exact manuscript claim or proposed claim",
  "section_key": "abstract|introduction|results|discussion|conclusion|...",
  "evidence_anchor": [
    {"type": "citation|figure_or_table|metric|section|analysis_artifact|missing", "text": "visible anchor"}
  ],
  "claim_strength": "unsupported|observed|supported|strong",
  "missing_evidence": ["specific missing support or verification action"],
  "allowed_wording": "bounded wording that does not outrun the evidence",
  "forbidden_wording": ["wording family that requires stronger evidence"]
}
```

## Strength Ladder

| Strength | Meaning | Safe action |
|---|---|---|
| `unsupported` | No visible citation, metric, figure/table, section, or artifact anchor supports the claim. | Soften, mark missing evidence, or remove. |
| `observed` | A local observation or metric is visible, but cross-checking or comparison support is incomplete. | Keep bounded to the observed setting. |
| `supported` | At least one visible anchor exists, but the source still needs claim-level verification. | Keep the claim only within the anchor's scope. |
| `strong` | Metric plus figure/table/artifact support is visible and the boundary is explicit. | Keep, while preserving dataset/method/setting limits. |

## Evidence Anchor Rules

- A citation key proves only that a reference is cited. It does not prove the cited paper supports the manuscript sentence until claim support is checked.
- A figure supports patterns and comparisons; a table supports exact values. Do not use a figure-only anchor for an exact numeric claim unless the value is readable or separately tabulated.
- A metric without a dataset, baseline, or unit of analysis should remain `observed`, not `strong`.
- A section or appendix reference is useful only when the target section actually contains the promised method, proof, data, or limitation.

## Output Discipline

- Preserve the author's original claim text when reporting problems.
- Never invent baselines, p-values, ablations, sample sizes, citations, figures, or datasets.
- When evidence is missing, write the missing evidence explicitly instead of filling the gap.
- Prefer bounded wording such as "in the reported setting" or "the presented results suggest" over universal claims.
