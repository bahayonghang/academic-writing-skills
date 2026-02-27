# Paper Audit (paper-audit)

Automated multi-mode paper auditing for LaTeX, Typst, and PDF documents.

## Overview

The `paper-audit` skill provides comprehensive automated auditing for academic papers in multiple formats (`.tex`, `.typ`, `.pdf`). It orchestrates multiple specialized checkers and generates structured reports with severity-rated issues and quality scores.

### Key Features

- **Multi-format Support**: LaTeX (`.tex`), Typst (`.typ`), and PDF (`.pdf`) inputs
- **Three Audit Modes**: self-check (comprehensive), review (peer-review focused), gate (submission readiness)
- **PDF Visual Layout Check**: Detects margin overflow, block overlaps, font inconsistency, low-resolution images, blank pages
- **Reference Integrity Check**: Undefined references, unreferenced labels, missing captions, forward references, numbering gaps
- **ScholarEval Assessment**: 8-dimension quality scoring (1–10 scale) with publication readiness label
- **Online Bibliography Verification**: CrossRef + Semantic Scholar API validation (no API key required)
- **NeurIPS-aligned Scoring**: Quality/Clarity/Significance/Originality dimensions (1–6 scale)

## Audit Modes

| Mode | Description | Checks Included |
|------|-------------|-----------------|
| `self-check` | Comprehensive pre-revision audit | All modules |
| `review` | Peer-review simulation | grammar, logic, figures, references, visual |
| `gate` | Submission readiness gate | format, bib, references, visual |

## Using the Skill in Claude Code

Simply mention relevant trigger words in your conversation:

```
Run a full audit on my paper before submission
```

```
Check paper quality with ScholarEval assessment
```

```
Audit my PDF for layout issues
```

### Argument Conventions

- **File path** (required): `.tex`, `.typ`, or `.pdf`
- **Mode** (optional): `self-check` (default), `review`, `gate`
- **Flags** (optional): `--online` for bibliography verification, `--scholar-eval` for ScholarEval

### Script CLI

```bash
# Basic audit (auto-detects mode)
python scripts/audit.py paper.tex --mode self-check

# With online bibliography verification
python scripts/audit.py paper.tex --mode review --online

# With ScholarEval 8-dimension assessment
python scripts/audit.py paper.tex --mode self-check --scholar-eval

# PDF audit (visual + extracted text checks)
python scripts/audit.py paper.pdf --mode gate

# Full audit with all options
python scripts/audit.py paper.tex --mode self-check --online --scholar-eval --email you@example.com
```

## Check Modules

| Module | Trigger | Formats | Description |
|--------|---------|---------|-------------|
| `grammar` | grammar, proofread | tex, typ, pdf | Grammar analysis |
| `sentences` | long sentence | tex, typ, pdf | Long sentence detection |
| `logic` | logic, coherence | tex, typ, pdf | Paragraph coherence (AXES model) |
| `format` | format, lint | tex, typ | Format checking |
| `figures` | figures, images | tex, typ | Figure quality check |
| `references` | ref, label | tex, typ | Reference integrity 🆕 |
| `visual` | visual, layout | **pdf only** | PDF visual layout 🆕 |
| `bib` | bib, bibliography | tex, typ | Bibliography verification |
| `deai` | deai, humanize | tex, typ, pdf | De-AI trace detection |

## Reference Integrity Module

Checks figure and table references for completeness.

### Checks Performed

| Check | Description | Severity |
|-------|-------------|----------|
| Undefined references | `\ref{fig:x}` with no `\label{fig:x}` | Critical |
| Unreferenced labels | `\label{fig:x}` never cited | Minor |
| Missing captions | Figure/table environment without `\caption` | Major |
| Forward references | First `\ref` appears before `\label` | Minor |
| Numbering gaps | `fig:1`, `fig:3` without `fig:2` | Minor |

### Script CLI

```bash
# LaTeX files
python scripts/check_references.py main.tex

# Typst files
python scripts/check_references.py main.typ

# JSON output
python scripts/check_references.py main.tex --json
```

## PDF Visual Layout Module

Analyzes camera-ready PDF for typesetting issues.

### Checks Performed

| Check | Method | Severity |
|-------|--------|----------|
| Margin overflow | Text bbox vs page margin (default 72pt) | Major |
| Block overlaps | Bounding box intersection area > 100 sq pt | Critical |
| Font inconsistency | >2 distinct body fonts (9–13pt) | Minor |
| Low-resolution images | Effective DPI < 150 | Major |
| Blank pages | Pages with no text or images | Minor |

### Script CLI

```bash
python scripts/visual_check.py paper.pdf
python scripts/visual_check.py paper.pdf --margin 72 --min-dpi 150
python scripts/visual_check.py paper.pdf --json
```

## ScholarEval Assessment Module

8-dimension academic quality scoring based on ScholarEval (arXiv:2510.16234).

### Dimensions

| Dimension | Weight | Source | Description |
|-----------|--------|--------|-------------|
| Soundness | 20% | script | Logical rigor, claim-evidence alignment |
| Clarity | 15% | script | Grammar, sentence quality, formatting |
| Presentation | 10% | script | Figures, visual layout, references |
| Novelty | 15% | llm | Originality and contribution |
| Significance | 15% | llm | Impact on the field |
| Reproducibility | 10% | mixed | Experiment description completeness |
| Ethics | 5% | llm | Ethical considerations |
| Overall | 10% | computed | Weighted aggregate |

### Publication Readiness Labels

| Score | Label |
|-------|-------|
| 9.0+ | Strong Accept — Ready for top venue |
| 8.0+ | Accept — Publication ready |
| 7.0+ | Ready with minor revisions |
| 6.0+ | Major revisions needed |
| 5.0+ | Significant rework required |
| <5.0 | Not ready for submission |

### Script CLI

```bash
# From audit JSON output
python scripts/scholar_eval.py --audit-json audit_result.json

# Merge with LLM evaluation
python scripts/scholar_eval.py --audit-json result.json --llm-json llm_scores.json

# JSON output
python scripts/scholar_eval.py --audit-json result.json --json
```

### LLM Assessment Prompt

After running the script-based audit, provide this prompt to Claude with the full paper text:

```
Please read the paper and provide 1-10 scores for these dimensions in JSON format:

{
  "novelty": {
    "score": <1-10>,
    "evidence": "<specific innovations and differences from prior work>"
  },
  "significance": {
    "score": <1-10>,
    "evidence": "<potential impact on the field>"
  },
  "reproducibility_llm": {
    "score": <1-10>,
    "evidence": "<completeness of experimental description, code/data availability>"
  },
  "ethics": {
    "score": <1-10>,
    "evidence": "<ethical considerations, conflicts of interest, data privacy>"
  }
}
```

## Online Bibliography Verification

Verify citation metadata against CrossRef and Semantic Scholar databases.

### Features

- **DOI Verification**: Validates DOI existence and cross-checks year/journal fields
- **Title Search**: Finds papers by title when no DOI is available
- **DOI Suggestions**: Recommends DOIs for entries missing them
- **Rate Limiting**: Built-in polite rate limiting (0.5s between requests)
- **No API Key Required**: Uses public CrossRef and Semantic Scholar APIs

### Usage

Add `--online` flag to the audit command:

```bash
# With online verification
python scripts/audit.py paper.tex --mode self-check --online

# With polite email for faster CrossRef rate limits
python scripts/audit.py paper.tex --online --email you@example.com
```

Or run standalone:

```bash
# Verify bibliography file
python scripts/verify_bib.py references.bib --online --email you@example.com
```

## Output Protocol

All issues use the standard protocol:

```
% REFERENCES (Line 45) [Severity: Critical] [Priority: P0]: Undefined reference: \ref{fig:arch}
% VISUAL (Page 3) [Severity: Major] [Priority: P1]: Content overflows left margin (x=28.3pt, margin=72pt)
% BIB (Line 12) [Severity: Major] [Priority: P1]: Online mismatch for 'smith2020': year: bib=2019 vs api=2020
```

## Report Format

The audit generates a structured Markdown report with:
- Issue list by severity (Critical → Major → Minor)
- NeurIPS-aligned score (Quality/Clarity/Significance/Originality, 1-6 scale)
- ScholarEval 8-dimension table with readiness label (when `--scholar-eval`)
- Online verification summary (when `--online`)

## Recommended Workflows

### Pre-Submission Check

```bash
python scripts/audit.py paper.tex --mode gate --online --email you@example.com
```

### Comprehensive Self-Review

```bash
python scripts/audit.py paper.tex --mode self-check --scholar-eval
```

### PDF Camera-Ready Check

```bash
python scripts/audit.py paper.pdf --mode gate
```

### Full Quality Assessment

```bash
python scripts/audit.py paper.tex --mode self-check --online --scholar-eval --email you@example.com
```

## Reference Files

- `resources/references/SCHOLAR_EVAL_GUIDE.md`: Detailed ScholarEval scoring rubrics
