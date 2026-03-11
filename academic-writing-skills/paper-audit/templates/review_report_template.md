# Peer Review Report Template

Output structure for `review` mode with multi-perspective agent assessment.

---

## Template

```markdown
# Peer Review Report

**Paper**: `{file_path}` | **Venue**: {venue or "general"} | **Date**: {timestamp}
**Language**: {language} | **Review Round**: {round, default "1"}

---

## Paper Summary *

{1-paragraph summary of the paper's claims, approach, and key results — 100-200 words}

---

## Strengths *

### S1: {Strength title} *
{Specific description with evidence from the paper — cite section/line numbers}

### S2: {Strength title} *
{Specific description with evidence}

### S3: {Strength title}
{Optional — up to S5}

---

## Weaknesses *

### W1: {Weakness title} *
- **Problem**: {What is wrong — specific, with location in paper}
- **Why it matters**: {Impact on paper quality or reader understanding}
- **Suggestion**: {Concrete improvement direction}
- **Severity**: {Critical | Major | Minor}

### W2: {Weakness title} *
- **Problem**: {description}
- **Why it matters**: {impact}
- **Suggestion**: {how to fix}
- **Severity**: {level}

### W3: {Weakness title}
{Optional — up to W5, same format}

---

## Questions for Authors *

1. {Genuine question about methodology, interpretation, or claims — not rhetorical}
2. {Question}
3. {Optional — up to 4 questions}

---

## Detailed Automated Findings

{Grouped by check module — from Phase 0 script output}

### FORMAT
| Line | Severity | Issue |
|------|----------|-------|
| {line} | {severity} | {message} |

### GRAMMAR
| Line | Severity | Issue |
|------|----------|-------|

### LOGIC
| Line | Severity | Issue |
|------|----------|-------|

{Continue for each module with findings. Omit modules with no issues.}

---

## Dimension Scores

### Script-Based (Automated)

| Dimension | Score | Source |
|-----------|-------|--------|
| Quality | {score}/6.0 | Script |
| Clarity | {score}/6.0 | Script |
| Significance | {score}/6.0 | Script |
| Originality | {score}/6.0 | Script |

### Agent-Based (LLM Judgment)

| Dimension | Score | Reviewer | Evidence |
|-----------|-------|----------|----------|
| Soundness | {score}/10 | Methodology Reviewer | {brief evidence} |
| Reproducibility | {score}/10 | Methodology Reviewer | {brief evidence} |
| Novelty | {score}/10 | Domain Reviewer | {brief evidence} |
| Significance | {score}/10 | Domain Reviewer | {brief evidence} |
| Soundness (independent) | {score}/10 | Critical Reviewer | {brief evidence} |

---

## Consensus Classification

{One of:}
- **[CONSENSUS-ALL]**: All reviewers agree — {summary of consensus}
- **[CONSENSUS-MAJORITY]**: 2/3 reviewers agree — {summary, note dissent}
- **[SPLIT]**: Fundamental disagreement — {describe each position}

{If disagreement exists:}
### Disagreement: {Issue name}
- **Reviewer A view**: {position with evidence}
- **Reviewer B view**: {position with evidence}
- **Resolution**: {how the synthesis agent resolved this}

---

## Overall Assessment

| Dimension | Final Score | Source |
|-----------|------------|--------|
| Quality | {merged}/6.0 | Script + Agent |
| Clarity | {merged}/6.0 | Script |
| Significance | {merged}/6.0 | Script + Agent |
| Originality | {merged}/6.0 | Agent |
| **Overall** | **{overall}/6.0** | |

**Recommendation**: {score_label}

---

## Revision Roadmap

### Priority 1 — Must Address (Blocking)
- [ ] {Action item from Critical issues or W-Critical weaknesses — with source reviewer}
- [ ] {Action item}

### Priority 2 — Strongly Recommended
- [ ] {Action item from Major issues — with source reviewer}
- [ ] {Action item}

### Priority 3 — Optional Improvements
- [ ] {Action item from Minor issues}
- [ ] {Action item}

### Estimated Effort
- Priority 1: ~{X} hours
- Priority 2: ~{Y} hours
- Priority 3: ~{Z} hours
```

---

## Format Guidelines

### Required Fields (marked with *)

All fields marked with `*` must be present in every review report. Optional fields may be omitted if not applicable.

### Strength/Weakness Requirements

- Minimum 2 strengths and 2 weaknesses per report
- Maximum 5 each
- Every strength/weakness must cite a specific location in the paper (section, line, figure)
- Weaknesses MUST use the 4-part format: Problem + Why it matters + Suggestion + Severity

### Constructive Tone

**Good**: "The sampling strategy may not capture the full range of X because... Consider expanding to include..."
**Bad**: "The sampling is flawed and inadequate."

### Evidence Citation

**Good**: "In Section 3.2 (Line 145), the authors claim X but provide no statistical test to support this."
**Bad**: "Some claims are unsupported."
