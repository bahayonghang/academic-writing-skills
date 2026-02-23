# Paper-Audit Skill Feasibility Analysis Report

## 1. Project Goal

Create a unified **paper-audit** (论文审核) skill that supports:

- **Languages**: Chinese & English
- **Input formats**: PDF, LaTeX (.tex), Typst (.typ)
- **Output**: Structured review report with scoring, issue list, and improvement suggestions

## 2. Current Codebase Assets

The existing codebase provides an extremely strong foundation (~70% reuse).

| Asset | Location | Reuse Value |
|-------|----------|-------------|
| `LatexParser` / `TypstParser` | `scripts/parsers.py` | ✅ Section splitting, text extraction, clean text |
| `check_format.py` | Each skill's `scripts/` | ✅ Format validation |
| `analyze_grammar.py` | Each skill's `scripts/` | ✅ Grammar checking |
| `analyze_logic.py` | Each skill's `scripts/` | ✅ Logic coherence & methodology |
| `analyze_sentences.py` | Each skill's `scripts/` | ✅ Long sentence detection |
| `deai_check.py` | Each skill's `scripts/` | ✅ AI-trace detection |
| `verify_bib.py` | Each skill's `scripts/` | ✅ Bibliography integrity |
| `check_figures.py` | `latex-paper-en/scripts/` | ✅ Figure reference checking |
| `check_consistency.py` | `latex-thesis-zh/scripts/` | ✅ Terminology consistency (Chinese) |
| `REVIEWER_PERSPECTIVE.md` | `references/` | ✅ 4-dimension criteria, 6-point scale, checklists |
| `FORBIDDEN_TERMS.md` | `references/` | ✅ Protected terminology |
| Unified Output Protocol | All `SKILL.md` | ✅ Severity/Priority diff-comment format |

## 3. Gap Analysis

### 3.1 PDF Input Support (Biggest Gap)

Current parsers only handle `.tex` and `.typ`. PDF support requires a new extraction pipeline.

| Approach | Library | Pros | Cons |
|----------|---------|------|------|
| **PyMuPDF (fitz)** | `pymupdf` | Fast, preserves layout, extracts images/tables | Loses LaTeX semantics |
| **pymupdf4llm** | `pymupdf4llm` | Outputs Markdown, LLM-friendly | Newer, less battle-tested |
| **pdfplumber** | `pdfplumber` | Good table extraction | Slower, text-only |
| **Nougat (Meta)** | `nougat-ocr` | Reconstructs LaTeX from PDF | Heavy (neural model), slow |
| **Marker** | `marker-pdf` | High-quality Markdown output | Requires ML models |

**Recommendation**: Use `pymupdf` as the primary extractor (fast, reliable), with `pymupdf4llm` as an optional enhanced mode for LLM-friendly Markdown output. A new `PdfParser` class should implement the same `DocumentParser` interface (`split_sections`, `extract_visible_text`, `clean_text`).

### 3.2 Unified Orchestrator

Currently each module runs independently. Paper-audit needs a single-command orchestrator that:

1. Auto-detects input format (`.tex` / `.typ` / `.pdf`)
2. Auto-detects language (Chinese / English)
3. Runs all relevant checks in the correct order
4. Aggregates results into a structured review report
5. Generates a final score

### 3.3 Scoring & Report Engine

Based on `REVIEWER_PERSPECTIVE.md`, the scoring system maps automated checks to review dimensions:

```
Review Dimensions:
├── Quality      — Technical soundness, claims supported
├── Clarity      — Writing quality, organization, notation
├── Significance — Impact, novelty of contribution
└── Originality  — New insights, not obvious extensions

Automated Check → Dimension Mapping:
├── Format Check       → Clarity
├── Grammar            → Clarity
├── Logic Analysis     → Quality + Significance
├── Sentence Analysis  → Clarity
├── De-AI Check        → Clarity + Originality
├── Bibliography       → Quality
├── Figure Check       → Clarity
├── Consistency        → Clarity
└── Checklist Items    → All dimensions
```

Output: A structured report with per-dimension scores (1–6 scale), issue counts by severity, and an overall assessment.

### 3.4 Chinese-Specific Audit Modules

For Chinese papers/theses, additional checks needed:

- GB/T 7714 bibliography format compliance (exists in `latex-thesis-zh`)
- Chinese punctuation correctness (full-width vs half-width)
- Abstract bilingual consistency (Chinese abstract ↔ English abstract)
- University template compliance (exists in `latex-thesis-zh`)

## 4. Proposed Architecture

```
paper-audit/
├── SKILL.md                    # Skill definition
├── scripts/
│   ├── audit.py                # Main orchestrator
│   ├── pdf_parser.py           # PdfParser class (DocumentParser interface)
│   ├── report_generator.py     # Scoring & report output
│   ├── detect_language.py      # Auto language detection
│   └── parsers.py              # Import from shared
└── resources/
    ├── references/
    │   ├── REVIEW_CRITERIA.md  # Unified review criteria
    │   └── CHECKLIST.md        # Consolidated checklists
    └── modules/
        └── AUDIT.md            # Orchestration module doc
```

Key design decisions:

- `audit.py` imports and calls existing scripts from sibling skills — no duplication
- `PdfParser` implements the same `DocumentParser` interface, so all downstream modules work transparently
- Language detection drives which check suite to apply (EN vs ZH)

## 5. Module Execution Flow

```
Input File (.tex / .typ / .pdf)
        │
        ▼
┌─ Format Detection ─────────────┐
│  .tex → LatexParser            │
│  .typ → TypstParser            │
│  .pdf → PdfParser (pymupdf)    │
└────────────┬───────────────────┘
             ▼
┌─ Language Detection ───────────┐
│  EN → English check suite      │
│  ZH → Chinese check suite      │
└────────────┬───────────────────┘
             ▼
┌─ Parallel Check Execution ─────┐
│  ├── Format Check              │
│  ├── Grammar Analysis          │
│  ├── Logic & Methodology       │
│  ├── Sentence Complexity       │
│  ├── De-AI Detection           │
│  ├── Bibliography Verification │
│  ├── Figure/Table References   │
│  ├── Consistency (ZH only)     │
│  ├── GB/T 7714 (ZH only)      │
│  └── Pre-submission Checklist  │
└────────────┬───────────────────┘
             ▼
┌─ Report Generation ────────────┐
│  ├── Per-dimension scoring     │
│  ├── Issue aggregation         │
│  ├── Priority-sorted findings  │
│  └── Overall assessment        │
└────────────────────────────────┘
```

## 6. Feasibility Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Technical feasibility | ⭐⭐⭐⭐⭐ | 70% reuse from existing modules, well-defined interfaces |
| PDF support | ⭐⭐⭐⭐ | PyMuPDF is mature; academic PDF layout can be tricky but workable |
| Chinese support | ⭐⭐⭐⭐⭐ | `latex-thesis-zh` already has Chinese-specific modules |
| Scoring accuracy | ⭐⭐⭐ | Automated checks cover Clarity well; Quality/Significance/Originality need LLM judgment |
| Effort estimate | ⭐⭐⭐⭐ | ~4 new files, ~1 new parser, ~1 orchestrator, rest is integration |
| Maintenance cost | ⭐⭐⭐⭐⭐ | Delegates to existing modules; changes propagate automatically |

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| PDF section detection inaccuracy | Medium | Use heuristic heading detection (font size, bold) + fallback to flat text |
| PDF math/formula loss | Medium | Flag as "unable to verify math" rather than guessing; recommend source file |
| Scoring subjectivity (Quality/Originality) | High | Clearly label automated vs LLM-judgment scores; provide evidence for each |
| Cross-module result conflicts | Low | Priority system (P0 > P1 > P2) resolves conflicts; higher severity wins |
| Large PDF processing time | Low | PyMuPDF is fast (~ms); set page limit warning for >100 pages |

## 8. Recommended Implementation Order

1. **SKILL.md** — Define the skill interface, triggers, modules, output protocol
2. **pdf_parser.py** — `PdfParser` implementing `DocumentParser` interface
3. **detect_language.py** — Simple CJK character ratio detection
4. **audit.py** — Orchestrator that calls existing scripts + generates report
5. **report_generator.py** — Scoring engine + structured output
6. **REVIEW_CRITERIA.md** + **CHECKLIST.md** — Reference documents
7. **Tests** — Unit tests for PdfParser + integration tests for orchestrator

## 9. Conclusion

**Feasibility: HIGH** ✅

The `paper-audit` skill is highly feasible because:

- **70% of the core logic already exists** in the three sibling skills
- The **parser abstraction** (`DocumentParser` interface) makes adding PDF support clean
- The **REVIEWER_PERSPECTIVE.md** already defines the scoring framework
- An **empty `paper-audit/` directory** is already prepared in the codebase
- The main new work is the orchestration layer (`audit.py`) and PDF parser (`pdf_parser.py`)

The biggest challenge is PDF quality — academic PDFs vary wildly in structure. But by treating PDF as a "best-effort" input and recommending source files (`.tex`/`.typ`) for full accuracy, this risk is well-contained.
