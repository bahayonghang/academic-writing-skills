# Module: Literature Review Synthesis

**Trigger**: related work, literature review, research gap, rewrite related work, comparative synthesis

**Purpose**: Diagnose whether the literature review is doing analytical work rather than listing papers, then provide a safe rewrite blueprint.

```bash
uv run python -B scripts/analyze_literature.py main.tex --section related
```

## What This Module Checks

- **A1: Enumeration** — 3+ consecutive author/year lines suggest paper-by-paper listing.
- **A2: Comparative synthesis** — each theme cluster should contain at least one sentence comparing strengths, weaknesses, trade-offs, or shared limitations.
- **A3: Gap derivation** — the final lines should surface the unresolved limitation or under-explored setting that motivates the paper.

## Rewrite Chain

Use this exact reasoning chain when proposing prose:

1. **Consensus**: what multiple papers agree on
2. **Disagreement**: where methods diverge or trade off
3. **Limitations**: what none of the compared methods handle well
4. **Gap**: the unresolved condition the paper targets
5. **This paper**: how the present work enters that gap

## Claim-Evidence Map

When the literature review contains a gap, novelty, or contribution claim,
summarize it with the claim-evidence contract from
`references/evidence/claim-evidence-contract.md`:

- `claim`: the exact gap or contribution sentence.
- `evidence_anchor`: cited prior work, section quote, or `missing`.
- `claim_strength`: `unsupported`, `observed`, `supported`, or `strong`.
- `missing_evidence`: closest prior work, comparison dimension, or claim-support
  check that is still absent.
- `allowed_wording`: bounded gap wording that does not overstate what the cited
  literature proves.

## Hard Boundaries

- Do not invent citations or add uncited claims.
- Keep `\cite{}`, `\ref{}`, `\label{}`, and math untouched unless the user explicitly asks for source edits.
- If the evidence in the section is too thin, say that the gap is unsupported instead of forcing one.
- A citation key only proves that a source is cited; it does not prove the
  cited source supports the exact manuscript claim until claim support is
  checked.
