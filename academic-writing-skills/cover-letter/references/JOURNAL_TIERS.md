# Journal Tier Strategy

Three-tier framing strategy for cover letters. Each template references its tier; the writing rules below apply per tier and override venue-specific style when not contradicted.

## top-journal

Nature family, Science family, Cell Press.

- **Opening**: lead with the scientific advance, not the topic. The first sentence must say what changes in the field because of this work.
- **Novelty framing**: paradigm-shift level. "We resolve the long-standing discrepancy between X and Y" beats "We propose a new method for X."
- **Word budget**: ≤350 words. Editors expect tightness.
- **Significance threshold**: must matter for a broad scientific audience, not a subfield. If it only matters to a subfield, route to a tier-2 sister journal.
- **Quantitative anchor**: required. At least one headline number traceable to the manuscript.
- **Comparison frame**: cite a recent paper from the _same journal_ that this work directly extends or contradicts. Editors notice this and it signals real reading of the venue.
- **Cliché avoidance**: never open with "We are pleased to submit..." — flagged as low-effort.

## mid-journal

IEEE Transactions, ACM journals, Springer LNCS / LNAI, PLOS family, Elsevier specialized journals.

- **Opening**: methodological contribution stated cleanly. "We introduce X, an algorithm that handles Y by Z."
- **Novelty framing**: contribution-led. Enumerate 3-4 specific contributions.
- **Word budget**: 400-500 words. More room for methodological context.
- **Significance threshold**: matters within the venue's specialty area. Broader-impact framing is optional; deep methodological framing is required.
- **Quantitative anchor**: required, with explicit comparator naming (baseline + dataset + protocol).
- **Comparison frame**: cite one or two recent papers from the same journal to position the work.
- **Conference extension**: if extending a prior conference paper, disclose the venue and percentage of new content (IEEE / ACM typical bar: ≥30%).

## conference

NeurIPS, ICML, CVPR, ICCV, ECCV, ACL, EMNLP, AAAI, IJCAI, KDD, WWW.

- **Opening**: technical contribution stated in one sentence.
- **Novelty framing**: contribution-led, concise.
- **Word budget**: ≤400 words. Conference reviewers do not read longer letters carefully.
- **Significance threshold**: contributes to a specific subfield with strong empirical or theoretical evidence.
- **Quantitative anchor**: required, with dataset and split named.
- **No broader-impact rhetoric in the letter itself**: that belongs in the manuscript's dedicated Broader Impact section (many ML venues now require it).
- **Dual-submission disclosure**: conferences are strict; always confirm compliance.
- **Anonymization**: for double-blind venues, the cover letter is typically not anonymized but should not leak identifying information beyond what is already in the submission system.

## When the venue does not match any tier

Fall back to `templates/generic.md`. Manually pick the closest tier for framing guidance. If unsure between tiers, prefer the more conservative (mid-journal) framing — overclaiming is worse than underclaiming for editorial trust.
