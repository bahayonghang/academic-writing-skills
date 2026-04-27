# Audit Guide

How to use the paper-audit skill and interpret its results.

## Quick Start

```bash
# Basic quick audit
python scripts/audit.py paper.tex --mode quick-audit

# Deep review
python scripts/audit.py paper.tex --mode deep-review

# Quality gate (pass/fail)
python scripts/audit.py paper.pdf --mode gate --pdf-mode enhanced

# Chinese thesis
python scripts/audit.py thesis.tex --lang zh --venue thesis-zh
```

## Mode Selection Guide

| Scenario | Recommended Mode | Why |
|----------|-----------------|-----|
| "Is my paper ready to submit?" | `quick-audit` | Fast readiness analysis |
| "I have three days before submission" | `quick-audit` | Final-week mechanical readiness screen |
| "What would reviewers say?" | `deep-review` | Reviewer-style issue bundle and roadmap |
| "Can my student submit this?" | `gate` | Fast pass/fail check |
| "Quick sanity check before deadline" | `gate` | Fastest, checks essentials only |
| "I want detailed feedback" | `deep-review` | Most comprehensive output |

## Understanding the Report

### Quick-Audit Report

The quick-audit report contains:

1. **Executive Summary**: Overall score and issue count at a glance
2. **Scores Table**: Per-dimension scores with issue counts (Critical/Major/Minor)
3. **Issues List**: All findings sorted by severity
4. **Pre-Submission Checklist**: Pass/fail for each checklist item
5. **PRESUBMISSION findings**: deterministic final-week checks for em dashes,
   AI-tone term frequency, abstract result gaps, LaTeX citation/label/equation
   hygiene, paragraph-shape weak signals, and concrete captions

**How to read scores**:
- **5.0+**: Excellent — minor polish only
- **4.0-5.0**: Good — address Major issues
- **3.0-4.0**: Needs work — significant revisions required
- **< 3.0**: Major concerns — consider restructuring

### Deep Review Report

The deep review workflow now produces two complementary reviewer artifacts:
- **`review_report.md`**: the evidence-rich audit bundle with structured major / moderate / minor findings, committee outputs, and roadmap details
- **`peer_review_report.md`**: a polished journal-style reviewer report with **Summary**, **Major Issues**, **Minor Issues**, and **Recommendation**

The deep review report adds:
- **Overall Assessment**: short calibrated reviewer summary
- **Major / Moderate / Minor Issues**: quote-anchored structured findings
- **Revision Roadmap**: prioritized fix list
- **Recommendation**: score summary, if requested
- **Phase 0 Automated Findings**: script context, including `PRESUBMISSION`
  findings. Full/editor focus may promote high-signal mechanical issues into
  the `pre_submission_readiness` lane; methodology/theory/literature/logic
  focus keeps them out of the final focused bundle.

The peer review report adds:
- **Summary**: 1-2 concise paragraphs in academic-review tone
- **Major Issues**: numbered validity-threatening concerns with section or quote anchors
- **Minor Issues**: numbered secondary concerns that still merit revision
- **Recommendation**: `Accept | Minor Revision | Major Revision | Reject`

### Gate Report

Binary verdict:
- **PASS**: All mandatory checks passed, no critical issues
- **FAIL**: Blocking issues found — must fix before submission

`PRESUBMISSION` Major and Minor findings are advisory in `gate`; they do not
fail the gate unless the script reports Critical.

## Severity Mapping

| PRESUBMISSION source taxonomy | quick/gate severity | deep-review bundle severity |
|-------------------------------|---------------------|-----------------------------|
| CRITICAL | Critical / P0 | major + gate blocker |
| MAJOR | Major / P1 | moderate |
| MINOR | Minor / P2 | minor or Phase 0 only |

## PDF Input Considerations

PDF mode has inherent limitations:

| Feature | LaTeX/Typst | PDF Basic | PDF Enhanced |
|---------|-------------|-----------|-------------|
| Section detection | Exact | Heuristic | Good |
| Math verification | Full | Unavailable | Unavailable |
| Format checking | Full | Skipped | Skipped |
| Figure references | Full | Skipped | Skipped |
| Grammar analysis | Full | Good | Good |
| Logic analysis | Full | Good | Good |
| Bibliography | Full | Skipped | Skipped |
| PRESUBMISSION text checks | Full | Text-only | Text-only |
| PRESUBMISSION source hygiene | Full | Skipped | Skipped |

**Recommendation**: Use source files (.tex/.typ) whenever possible for maximum
accuracy. Use PDF mode for quick reviews when source is unavailable; PDF mode
will explicitly skip citation-tie, label, numbered-equation, and source-caption
checks.

## Addressing Issues

### Priority Order
1. **Critical (P0)**: Must fix — these will likely cause rejection
2. **Major (P1)**: Should fix — these weaken the paper significantly
3. **Minor (P2)**: Nice to fix — these improve polish

### Common Critical Issues
- Missing figure/table references
- Compilation errors
- Placeholder text (TODO/FIXME)
- Author names in blind submission

### Common Major Issues
- Long, convoluted sentences
- Logic gaps in methodology
- Missing baselines or ablations
- AI-trace patterns in writing

### Common Minor Issues
- Minor grammar issues
- Inconsistent notation
- Style guide violations

## Re-auditing After Fixes

After addressing issues, re-run the audit to verify improvements:

```bash
# Before fixes
python scripts/audit.py paper.tex -o report_before.md

# After fixes
python scripts/audit.py paper.tex -o report_after.md
```

Compare scores to track improvement.
