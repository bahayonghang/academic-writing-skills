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

> **The major ML/vision conferences do not use a cover letter.** NeurIPS, ICML,
> CVPR, ICLR and peers collect submission metadata through structured
> OpenReview / CMT forms (author list, abstract, checklists), not a free-form
> letter. Treat the `neurips` / `icml` / `cvpr` templates as applicable only
> when a workshop, datasets-and-benchmarks track, or special call explicitly
> requests a letter. For the main track, redirect the user to the submission
> form rather than generating a letter.

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

## Editorial practice snapshot (2025-26)

The cover letter is the first step of desk review (high-volume journals desk-reject 50-80%), so these venue-specific realities matter:

- **AI-use disclosure is now a cover-letter requirement at the top tier.** ICMJE (Jan 2026, Section V) requires generative-AI use to be described in the cover letter and the manuscript; Science/AAAS, NEJM, and APS require cover-letter disclosure explicitly. IEEE (Acknowledgments), ACM (within the Work), and Elsevier/Springer (Methods / dedicated statement) place it in the manuscript instead. Undisclosed AI use can be treated as misconduct.
- **Nature-family cover letters are a confidential channel** — not shown to reviewers. Use them for competing interests, related work under consideration, or specific editorial-handling requests; do not restate the abstract. The letter is optional for Nature flagship.
- **IEEE is bimodal**: _Proceedings of the IEEE_ mandates a detailed cover letter (a missing one can be returned); _IEEE TIM_ explicitly says not to submit one unless there is something specific to raise. Always check the target title's author center.
- **Author-suggested reviewers are being curtailed** (Cureus removed the option in 2025; PLOS ONE removed it earlier; Wiley/IOP now require independent verification). Do not generate a suggested-reviewers paragraph by default — include it only when the target venue's submission process asks for it.
- **Rejected-and-resubmitted manuscripts**: some venues (Wiley _Small_, IEEE/ACM ToN) require the cover letter to state the prior submission and summarize the changes.
- **Double-blind venues**: list people who have already seen the manuscript (to protect the blind), and disclose overlap with the authors' own prior work or shared datasets.
- **Springer Nature fixed phrasing**: "We confirm that this manuscript has not been published elsewhere and is not under consideration by another journal. All authors have approved the manuscript and agree with its submission to [journal]."
- **Generic template letters are a negative signal**: editors who screen 50+ letters a week spot mass-mailed wording instantly. Specificity (named scope dimension, a recent same-venue paper, the concrete headline result) is what reads as written-with-attention.
