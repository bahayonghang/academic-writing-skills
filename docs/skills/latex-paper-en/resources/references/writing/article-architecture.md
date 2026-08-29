# Journal-Style Article Architecture

> **Attribution and scope:** This reference adapts community-derived, Nature-leaning
> rhetorical heuristics from `ref/claude-scholar/skills/nature-writing`. The source does
> not identify its article corpus, DOI list, or sample-selection method, and it does not
> cite official Nature author guidance. Some abstract, introduction, and method patterns
> share a source lineage with `ref/Research-Paper-Writing-Skills`, which the local
> section-writing bank already adapts. Treat this reference as an LLM writing aid, not as
> official Nature rules or a venue-compliance profile.

Use this reference when a user asks for a full-paper argument, journal narrative,
Nature-style structure, Results narrative, or Discussion structure. Do not load it for
ordinary grammar polishing or a single conference-style section unless the user also asks
for journal-level restructuring.

## Full-Paper Argument Chain

Reduce the paper to this chain before drafting or restructuring:

`field-scale need -> unresolved bottleneck -> proposed move -> decisive evidence -> broader implication -> boundary`

Give the boundary the same status as the contribution and evidence. If a link is absent
from the source, mark it as missing. Do not invent a claim, result, citation, mechanism, or
scope condition to complete the chain.

For paragraph-level navigation inside this chain, `logic --paragraph-arc` can surface missing lead,
close, adjacent-interface, and expansion forms. It does not establish that an argument-chain link
is semantically present or absent. See [`paragraph-arc.md`](paragraph-arc.md); the provisional
English thresholds have synthetic-only evidence and remain **UNVERIFIED** on real papers.

## Journal-Style Abstract Moves

For a journal-style abstract, consider this six-move sequence:

1. Establish the field context or problem.
2. State why current routes do not fully solve it.
3. Name what the paper introduces or demonstrates.
4. Report the strongest supported result, with quantitative or comparative evidence when available.
5. State the supported mechanism, workflow effect, or practical consequence.
6. Close with a bounded implication.

This sequence is an additional mode, not a replacement for the three abstract patterns in
`references/writing/section-writing/abstract.md`. Select the pattern for the paper type,
venue, evidence, and author intent.

## Abstract Diagnostics (LLM)

These are candidate prompts for contextual review, not pass/fail rules:

| Layer | Severity | Priority | Candidate prompt |
| --- | --- | --- | --- |
| `[LLM]` | Info | P3 | If the abstract opens with `Here, we` or `In this paper, we` and has no prior context sentence, it may lack field context. Check the abstract type before suggesting a change. |
| `[LLM]` | Info | P3 | If the final sentence makes a broad promise without a scope limit, it may need a narrower boundary. |
| `[LLM]` | Info | P3 | If the abstract contains no number, comparison, or concrete test, it may feel ungrounded. The existing `Results-VAGUE` script check already covers the related lack-of-specific-results signal; do not add a duplicate script rule. |

## Results Evidence Ladder

Arrange Results so that later claims rest on earlier evidence:

1. System, workflow, or design-space overview.
2. Validation that the platform, assay, or setup is credible.
3. Primary performance or discovery result.
4. Fair comparison with a baseline, standard practice, or prior method.
5. Mechanism, diagnostic analysis, or interpretability evidence.
6. Scale-up, application, generalization, or stress test.

Open a claim-first subsection with this pattern when it matches the evidence:

`To test [question], we [action].`

Then report the result and its evidence. Keep interpretation brief unless the paragraph
explicitly moves into Discussion. For claim-to-experiment planning, see
`references/writing/section-writing/experiments.md`.

## Discussion Widening

Widen from the finding to its supported meaning:

1. State the central advance.
2. Explain why the evidence supports it.
3. Identify the workflow, design rule, or conceptual boundary that changes.
4. Relate that change fairly to previous studies.
5. State remaining limits and dependencies.
6. Name future work that the evidence now makes plausible.

Do not restate every figure. Select only the evidence that changes interpretation. Use the
existing Discussion Layering guidance in
`references/writing/section-writing/experiments.md` for paragraph-level planning.
