# Review Criteria

Unified review criteria for paper audit, based on major conference standards (NeurIPS, ICLR, ICML, IEEE, ACM).

## Four-Dimensional Review Framework

### 1. Quality (Weight: 30%)

**What reviewers assess**:
- Technical soundness of claims and proofs
- Correctness of mathematical derivations
- Fairness of experimental comparisons
- Adequate baselines and ablation studies
- Reproducibility of results
- **Experiment Narrative**: Results are presented as a cohesive analytical narrative rather than merely listing numbers.

**Common deduction reasons**:
- Flawed proofs or incorrect derivations
- Missing baselines or unfair comparisons
- Insufficient experimental evaluation
- Claims not supported by evidence
- Missing error bars or statistical tests

**Automated checks mapping**: Bibliography verification, Logic & coherence analysis, Experiment narrative checks

### 2. Clarity (Weight: 30%)

**What reviewers assess**:
- Clear and precise writing
- Logical document organization
- Consistent notation throughout
- Reproducible by domain experts
- Appropriate use of figures and tables

**Common deduction reasons**:
- Ambiguous notation or undefined terms
- Poor organization or missing sections
- Long, convoluted sentences
- Missing method details
- Figures without proper captions or references
- Verbose or AI-generated caption text (e.g., "The figure shows") or inconsistent casing

**Automated checks mapping**: Format check, Grammar analysis, Sentence complexity, De-AI detection, Figure/table references, Consistency

### 3. Significance (Weight: 20%)

**What reviewers assess**:
- Impact on the research community
- Advances understanding of the problem
- Practical applicability
- Non-incremental contribution

**Common deduction reasons**:
- Incremental improvement over existing work
- Narrow applicability
- Limited novelty
- No clear advantage over simpler methods

**Automated checks mapping**: Logic & coherence analysis (methodology justification)

### 4. Originality (Weight: 20%)

**What reviewers assess**:
- New insights or perspectives
- Novel methodology or approach
- Creative problem formulation
- Not obvious extension of prior work

**Common deduction reasons**:
- Known results or obvious extensions
- Insufficient differentiation from prior work
- Missing discussion of novelty
- AI-generated content without original thought

**Automated checks mapping**: De-AI detection

## Scoring Algorithm

```
For each dimension D:
    base_score = 6.0
    for each issue mapped to D:
        if severity == "Critical": score -= 1.5
        if severity == "Major":    score -= 0.75
        if severity == "Minor":    score -= 0.25
    dimension_score = max(1.0, score)

overall = quality * 0.30 + clarity * 0.30 + significance * 0.20 + originality * 0.20
```

## Score-to-Label Mapping

| Score Range | Label | Typical Action |
|-------------|-------|----------------|
| 5.5 - 6.0 | Strong Accept | Submit with confidence |
| 4.5 - 5.4 | Accept | Minor revisions recommended |
| 3.5 - 4.4 | Borderline Accept | Address weaknesses before submission |
| 2.5 - 3.4 | Borderline Reject | Significant revisions needed |
| 1.5 - 2.4 | Reject | Major rework required |
| 1.0 - 1.4 | Strong Reject | Fundamental issues — reconsider approach |

## Important Notes

- **Automated scores cover Clarity well** but have limited ability to assess Quality, Significance, and Originality
- **LLM judgment supplements** automated checks for the latter dimensions
- **Scores should be treated as indicators**, not definitive assessments
- **Always prioritize Critical issues** regardless of overall score
