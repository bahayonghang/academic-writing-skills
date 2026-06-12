# Design: latex-paper-en research-writing-level corpus expansion

## Scope Boundary

This task stays narrow:

- Expand the evaluation corpora for `latex-paper-en`.
- Tune trigger boundaries where needed.
- Keep the existing module-router architecture unchanged.
- Do not add a shared core with `latex-thesis-zh`.
- Do not add new module names unless a real routing gap is proven.

`research-writing-skill` is the benchmark for writing moves, not a dependency to copy verbatim.

## Benchmark Mapping

Map the source skill's section-writing moves into the paper-en architecture:

- Introduction -> stakes, structural gap, key abstraction, design intuition, contributions, results preview.
- Related Work -> category clustering, structural limitations, positioning sentence.
- Method -> named abstraction, why this design, component decomposition, trade-off knob, robustness.
- Experiments -> setup anchoring, head-to-head comparison, deep dive, takeaway, ablation, robustness.
- Conclusion / self-review -> closure, claim-evidence map, limitation boundary, reviewer-facing phrasing.
- Figures / venue narration -> caption and figure synthesis, venue-aware voice, no source breakage.

## Eval Families

Add or refine prompts so each family tests a distinct writing move:

1. Introduction blueprint with a real funnel, not a generic rewrite.
2. Related-work synthesis and gap derivation, not a paper-by-paper list.
3. Method narrative with motivation -> design -> advantage.
4. Evaluation narrative with takeaways, ablation, and robustness.
5. Conclusion closure plus claim-evidence self-review.
6. Figure / caption / venue narration as a separate writing move, not just figure existence.

The corpus should keep the English-paper boundary obvious:

- preserve citations, labels, math, and LaTeX anchors;
- avoid thesis-style chapter prompts;
- avoid turning `paper-audit` into a substitute for writing guidance;
- avoid generic proofreading prompts that do not require section-level reasoning.

## Trigger Strategy

The trigger set should include:

- positive near-neighbors: section rewrite plans, claim-evidence maps, related-work synthesis, method-outline work, evaluation takeaways, conclusion closure, figure narration;
- negative near-neighbors: paper-audit/gate review, Chinese thesis prompts, Typst prompts, pure citation search, from-scratch paper drafting, translation-only requests, compile-only requests, generic polish requests.

Balance matters more than raw count: the positive prompts should look like real paper-writing work, and the negative prompts should be genuinely adjacent so a naive keyword match would still be tempted.

## Compatibility Notes

- No new shared helper or shared reference core.
- No new module list changes are expected if the task stays within existing routes.
- If a trigger boundary clearly needs a wording fix, prefer a tiny frontmatter tweak over a structural rewrite.

## Validation Shape

The final check should be evidence-based and low-risk:

- shape and uniqueness checks for `evals.json` and `trigger_eval.json`;
- contract tests for skill assets and trigger corpus balance;
- version alignment checks stay unchanged;
- no docs mirror update is expected unless a new reference file is introduced.
