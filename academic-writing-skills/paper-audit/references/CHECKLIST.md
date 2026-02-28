# Pre-Submission Checklists

Consolidated checklists for paper audit across venues.

## Universal Checklist (All Venues)

### Compilation & Formatting
- [ ] Paper compiles without errors
- [ ] No overfull/underfull hbox warnings (LaTeX)
- [ ] Page limit respected (excluding references)
- [ ] Correct style file / template used
- [ ] Consistent font sizes and margins

### Content Integrity
- [ ] No placeholder text (TODO, FIXME, XXX)
- [ ] All figures referenced in text
- [ ] All tables referenced in text
- [ ] No orphaned citations (every `\cite` has a bib entry)
- [ ] No unused bibliography entries
- [ ] All equations referenced if numbered
- [ ] Consistent notation throughout

### Writing Quality
- [ ] All acronyms defined on first use
- [ ] No overly long sentences (> 60 words)
- [ ] Abstract is self-contained
- [ ] Contributions clearly stated in introduction
- [ ] Limitations section included
- [ ] Figure/Table captions are concise, without AI-like redundancy, and use consistent casing

### Experiment Analysis
- [ ] Experiment section uses cohesive paragraph narratives, not itemized lists
- [ ] Appropriate, up-to-date SOTA baseline methods are included and justified
- [ ] Ablation studies effectively validate the contribution of core components
- [ ] Statistical significance/confidence intervals are reported where applicable

### Submission Compliance
- [ ] Anonymous submission (no author names in blind review)
- [ ] Supplementary material within size limits
- [ ] Code submission prepared (if applicable)
- [ ] Ethics review flagged if applicable

## NeurIPS Specific

- [ ] Paper checklist completed (Appendix)
- [ ] Broader Impact Statement included
- [ ] Lay summary prepared (for accepted papers)
- [ ] Main paper <= 9 pages (+ unlimited references/appendix)
- [ ] Uses official NeurIPS style file
- [ ] Reproducibility details: random seeds, compute, datasets
- [ ] Error bars included with methodology specified
- [ ] Statistical significance tests where appropriate
- [ ] Dataset licensing and consent documented
- [ ] Potential negative societal impacts discussed
- [ ] Comparison with appropriate baselines
- [ ] Ablation studies for key design choices

## ICLR Specific

- [ ] Uses official ICLR style file
- [ ] Double-blind review compliance
- [ ] Main paper <= 10 pages (+ unlimited appendix)
- [ ] Reproducibility statement included
- [ ] Code submission URL provided (if applicable)

## ICML Specific

- [ ] Uses official ICML style file
- [ ] Main paper <= 8 pages (+ unlimited appendix)
- [ ] Impact statement included
- [ ] Supplementary <= 50MB

## IEEE Specific

- [ ] IEEE style file used (conference or journal)
- [ ] Abstract <= 250 words
- [ ] Keywords provided (3-5 terms)
- [ ] References follow IEEE format
- [ ] Figure captions below figures, table captions above tables
- [ ] All figures are high resolution (>= 300 DPI)

## ACM Specific

- [ ] ACM Computing Classification System (CCS) concepts included
- [ ] ACM Reference Format citation in footer
- [ ] Uses `acmart` document class
- [ ] Rights management information included

## Chinese Thesis Specific (中文学位论文)

- [ ] Bibliography follows GB/T 7714-2015 standard
- [ ] Chinese abstract and English abstract both present
- [ ] Abstract bilingual consistency verified
- [ ] Full-width punctuation used in Chinese text
- [ ] Half-width punctuation used in English text and formulas
- [ ] University template compliance verified
- [ ] Declaration of originality included
- [ ] Acknowledgments section present
- [ ] Keywords in both Chinese and English
