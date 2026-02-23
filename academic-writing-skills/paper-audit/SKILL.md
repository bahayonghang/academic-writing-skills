---
name: paper-audit
version: 1.0.0
category: academic-writing
tags:
  - audit
  - review
  - paper
  - pdf
  - latex
  - typst
  - chinese
  - english
  - scoring
  - checklist
description: |
  Unified paper audit skill supporting Chinese & English academic papers.
  Supports LaTeX (.tex), Typst (.typ), and PDF (.pdf) input formats.
  Three modes: self-check (pre-submission), review (peer review simulation),
  gate (quality gate pass/fail).
  Use when user mentions: audit, review, check paper, paper quality,
  pre-submission check, score paper, or any paper auditing task.
argument-hint: "[paper.tex|paper.typ|paper.pdf] [--mode self-check|review|gate] [--pdf-mode basic|enhanced]"
allowed-tools: Read, Glob, Grep, Bash(python *)
references:
  - resources/references/REVIEW_CRITERIA.md
  - resources/references/CHECKLIST.md
  - resources/references/AUDIT_GUIDE.md
scripts:
  - scripts/audit.py
  - scripts/pdf_parser.py
  - scripts/detect_language.py
  - scripts/report_generator.py
  - scripts/parsers.py
---

# Paper Audit Skill (论文审核)

Unified academic paper auditing across formats and languages.

## Critical Rules

1. NEVER modify `\cite{}`, `\ref{}`, `\label{}`, math environments in LaTeX
2. NEVER modify `@cite`, `#cite()`, `#ref()`, `<label>` in Typst
3. NEVER fabricate bibliography entries — only verify existing `.bib`/`.yml` files
4. NEVER change domain terminology without user confirmation
5. Check `FORBIDDEN_TERMS` lists before suggesting any terminology changes
6. For PDF input, clearly flag sections where extraction quality is uncertain
7. Always distinguish between automated findings and LLM-judgment scores

## Audit Modes

### Mode: `self-check` (Pre-submission Self-Check)

**Trigger keywords**: audit, check, self-check, pre-submission, score, review my paper

**What it does**: Runs all automated checks and generates a structured report with:
- Per-dimension scores (Quality, Clarity, Significance, Originality) on 1-6 scale
- Issue list sorted by severity (Critical > Major > Minor)
- Improvement suggestions per section
- Pre-submission checklist results

**CLI**: `python scripts/audit.py paper.tex --mode self-check`

### Mode: `review` (Peer Review Simulation)

**Trigger keywords**: simulate review, peer review, reviewer perspective, what would reviewers say

**What it does**: Everything in self-check PLUS:
- Paper summary from reviewer perspective
- Strengths analysis
- Weaknesses analysis with severity
- Questions a reviewer would ask
- Accept/reject recommendation with confidence

**CLI**: `python scripts/audit.py paper.tex --mode review`

### Mode: `gate` (Quality Gate)

**Trigger keywords**: quality gate, pass/fail, can I submit, ready to submit, advisor check

**What it does**: Fast mandatory checks only:
- Format validation
- Bibliography integrity
- Figure/table references
- Pre-submission checklist
- Binary PASS/FAIL verdict with blocking issues

**CLI**: `python scripts/audit.py paper.tex --mode gate`

## Supported Formats

| Format | Parser | Notes |
|--------|--------|-------|
| LaTeX (.tex) | `LatexParser` | Full support — all checks available |
| Typst (.typ) | `TypstParser` | Full support — all checks available |
| PDF (.pdf) basic | `PdfParser` (pymupdf) | Text extraction with font-size heading detection |
| PDF (.pdf) enhanced | `PdfParser` (pymupdf4llm) | Structured Markdown with table/header preservation |

**PDF Limitations**: Math formulas may be lost; some checks (format, figures) skip for PDF. Recommend providing source files (.tex/.typ) for maximum accuracy.

## Language Support

| Language | Detection | Extra Checks |
|----------|-----------|-------------|
| English | Auto (default) | Standard suite |
| Chinese | Auto (CJK ratio > 30%) | + consistency check, + GB/T 7714 compliance |

Force with `--lang en` or `--lang zh`.

## Check Modules

| Module | Script Source | Dimensions Affected | Applicable Formats |
|--------|-------------|--------------------|--------------------|
| Format Check | `check_format.py` | Clarity | .tex, .typ |
| Grammar Analysis | `analyze_grammar.py` | Clarity | .tex, .typ, .pdf |
| Logic & Coherence | `analyze_logic.py` | Quality, Significance | .tex, .typ, .pdf |
| Sentence Complexity | `analyze_sentences.py` | Clarity | .tex, .typ, .pdf |
| De-AI Detection | `deai_check.py` | Clarity, Originality | .tex, .typ, .pdf |
| Bibliography | `verify_bib.py` | Quality | .tex, .typ |
| Figure/Table Refs | `check_figures.py` | Clarity | .tex |
| Consistency (ZH) | `check_consistency.py` | Clarity | .tex (Chinese only) |
| GB/T 7714 (ZH) | `verify_bib.py` (GB mode) | Quality | .tex (Chinese only) |
| Pre-submission Checklist | Built-in | All | All formats |

## Scoring System

Based on REVIEWER_PERSPECTIVE.md criteria:

### Four Dimensions
- **Quality** (30%): Technical soundness, well-supported claims
- **Clarity** (30%): Clear writing, reproducible, good organization
- **Significance** (20%): Community impact, advances understanding
- **Originality** (20%): New insights, not obvious extensions

### Six-Point Scale (NeurIPS standard)
| Score | Rating | Meaning |
|-------|--------|---------|
| 5.5-6.0 | Strong Accept | Groundbreaking, technically flawless |
| 4.5-5.4 | Accept | Technically solid, high impact |
| 3.5-4.4 | Borderline Accept | Solid but limited evaluation/novelty |
| 2.5-3.4 | Borderline Reject | Merits but weaknesses outweigh |
| 1.5-2.4 | Reject | Technical flaws, insufficient evaluation |
| 1.0-1.4 | Strong Reject | Fundamental errors or known results |

## Output Protocol

All issues follow the unified format:

```
[MODULE] (Line N) [Severity: Critical|Major|Minor] [Priority: P0|P1|P2]: Issue description
  Original: ...
  Revised:  ...
  Rationale: ...
```

- **Severity**: Critical (must fix), Major (should fix), Minor (nice to fix)
- **Priority**: P0 (blocking), P1 (important), P2 (low priority)

## Workflow

When a user requests a paper audit:

1. **Identify the file** — locate the .tex, .typ, or .pdf file
2. **Determine mode** — self-check (default), review, or gate based on user intent
3. **Run the orchestrator** — `python scripts/audit.py <file> --mode <mode>`
4. **Present the report** — show the Markdown report to the user
5. **Discuss findings** — help the user address Critical and Major issues first
6. **Re-audit if needed** — run again after fixes to verify improvements

For `review` mode, supplement the automated report with LLM analysis of:
- Overall paper strengths (what works well)
- Key weaknesses (what reviewers would criticize)
- Questions a reviewer would ask
- Missing related work or baselines
