# Paper-Audit Skill Design Document

**Date**: 2026-02-23
**Status**: Approved
**Author**: Feasibility analysis & design by collaborative brainstorming session

---

## 1. Overview

### 1.1 Problem Statement

Academic researchers need a unified, local tool that audits papers across multiple formats (LaTeX, Typst, PDF) and languages (Chinese, English) before submission. Existing solutions are either:

- **Commercial SaaS** (Paperpal, Trinka, Writefull) — cloud-only, no offline, no source-file awareness
- **Anti-plagiarism focused** (PaperPass, PaperFace) — Chinese ecosystem focuses on plagiarism/AI-trace reduction, not quality audit
- **Single-format** (existing Claude Code skills) — English-only or single-format
- **AI/ML-domain only** (PaperReview.ai) — no LaTeX/Typst awareness, no Chinese support

### 1.2 Solution

Create a `paper-audit` skill for Claude Code that provides:

- **3 audit modes**: pre-submission self-check, peer review simulation, quality gate
- **3 input formats**: LaTeX (.tex), Typst (.typ), PDF (.pdf with dual extraction modes)
- **2 languages**: English and Chinese (auto-detected)
- **Structured Markdown report** with 4-dimensional scoring (Quality, Clarity, Significance, Originality)

### 1.3 Design Principles

- **70-80% code reuse** from existing sibling skills (latex-paper-en, latex-thesis-zh, typst-paper)
- **KISS**: Monolithic orchestrator with mode-to-checks dict (no plugin system, no YAML config)
- **YAGNI**: Only build what's needed now; extensibility via simple dict modification
- **DRY**: Import existing check scripts directly, zero duplication

---

## 2. Industry Landscape Research

### 2.1 Commercial Tools

| Tool | Focus | Strengths | Gaps |
|------|-------|-----------|------|
| **Paperpal** | Manuscript check (30+ checks) | Overleaf integration, LaTeX support | Cloud-only, no offline, no Chinese thesis |
| **Trinka** | Grammar + consistency | Privacy-first, LaTeX proofreader | No scoring, no review simulation |
| **Writefull** | Academic language feedback | Trained on journal articles | No PDF structure analysis |
| **QuillBot** | Essay/paper checking | AI detection + plagiarism | Not academic-specific |

### 2.2 Academic/Research Tools

| Tool | Focus | Key Finding |
|------|-------|-------------|
| **PaperReview.ai** (Andrew Ng, Stanford, 2025-11) | Agentic peer reviewer | 0.42 AI-human correlation (matches 0.41 human-human). arXiv-grounded, AI/ML focused only |
| **ReviewRL** (Tsinghua, EMNLP 2025) | RL-based review generation | Uses reinforcement learning for factual accuracy + rating consistency |
| **STOC 2026 Experiment** | Pre-submission LLM feedback | Gemini-based, mathematical rigor focus. First major TCS conference to try |
| **OpenReviewer** (ICLR 2026) | Conference decision prediction | 78.5% accuracy on balanced datasets with continual pre-training |

### 2.3 Chinese Ecosystem

| Tool | Focus | Gap |
|------|-------|-----|
| PaperPass / PaperFace / LunBiGuo | Anti-plagiarism + AIGC reduction | No quality audit, no structure analysis |
| No open-source Chinese paper audit tool exists | — | **Clear market gap** |

### 2.4 Existing Claude Code Skills

| Skill | Focus | Limitation |
|-------|-------|------------|
| `paper-review-helper` (MCPMarket, 26 stars) | PDF-to-LaTeX, SymPy math verification | Requires Mathpix (paid), English only |
| `paper-writer-skill` (GitHub) | 10-phase IMRAD pipeline | Writing-focused, not auditing |
| `peer-review` (SkillMD.ai) | Structured reviewer feedback | No format checking, no scoring |
| `fact-checker` (playbooks.com) | Factual claims verification | Not academic-specific |

### 2.5 Competitive Advantage

**No existing tool provides**: PDF + LaTeX + Typst + Chinese + English + 3-mode audit + local/offline + structured scoring in a single skill.

---

## 3. Architecture

### 3.1 File Structure

```
academic-writing-skills/paper-audit/
├── SKILL.md                              # Skill definition (3 modes, triggers, modules)
├── scripts/
│   ├── audit.py                          # Main orchestrator (entry point)
│   ├── pdf_parser.py                     # PdfParser class (basic + enhanced modes)
│   ├── detect_language.py                # Auto language detection (CJK ratio)
│   ├── report_generator.py              # Markdown report builder with scoring
│   └── parsers.py                        # Re-exports DocumentParser, LatexParser, TypstParser
└── resources/
    └── references/
        ├── REVIEW_CRITERIA.md            # Unified 4-dimensional review criteria
        ├── CHECKLIST.md                  # Consolidated pre-submission checklists
        └── AUDIT_GUIDE.md               # Audit modes & interpretation guide
```

### 3.2 Component Responsibilities

| Component | Responsibility | Est. Lines |
|-----------|---------------|------------|
| `SKILL.md` | Skill triggers, critical rules, 3-mode definitions, output protocol | ~200 |
| `audit.py` | Format detection -> language detection -> check dispatch -> aggregation | ~300 |
| `pdf_parser.py` | `PdfParser(DocumentParser)` with basic/enhanced modes | ~150 |
| `detect_language.py` | CJK character ratio -> `"en"` or `"zh"` | ~40 |
| `report_generator.py` | Issue aggregation, per-dimension scoring, Markdown rendering | ~200 |
| `parsers.py` | Thin re-export layer from sibling skills | ~20 |

### 3.3 Approach Rationale

Three architectures were evaluated:

1. **Monolithic Orchestrator** (CHOSEN) — Single `audit.py` entry point with mode-to-checks dict
2. **Plugin Registry** — Auto-discovered check plugins with `CheckPlugin` interface
3. **Config-Driven Pipeline** — YAML-defined check pipeline

**Why Monolithic**: With ~10 stable check modules, a plugin system is over-engineering (YAGNI). The monolithic orchestrator matches existing codebase patterns, is easy to test, and can be refactored to plugins later if needed.

---

## 4. Three Audit Modes

### 4.1 Mode: `self-check` (Pre-submission Self-Check)

**Target user**: Researcher checking their own paper.

**Checks**:
```python
SELF_CHECK = ["format", "grammar", "logic", "sentences", "deai", "bib", "figures"]
# + "consistency", "gbt7714" if language == "zh"
```

**Output**: Structured Markdown report with executive summary, per-dimension scores (1-6 scale), issue list sorted by severity, improvement suggestions, and pre-submission checklist results.

### 4.2 Mode: `review` (Peer Review Simulation)

**Target user**: Researcher wanting simulated conference-style peer review.

**Checks**: Same as `self-check` + LLM-driven analysis:
```python
REVIEW = SELF_CHECK + ["reviewer_strengths", "reviewer_weaknesses", "reviewer_questions"]
```

**Output**: Conference-style review with summary, strengths, weaknesses, questions for authors, missing references, overall score with confidence, and accept/reject recommendation.

### 4.3 Mode: `gate` (Quality Gate)

**Target user**: Advisor/editor enforcing minimum quality.

**Checks** (fast, mandatory only):
```python
GATE = ["format", "bib", "figures", "checklist"]
```

**Output**: Pass/fail gate report with per-item checkmarks, blocking issues, and binary PASS/FAIL verdict.

### 4.4 CLI Interface

```bash
# Self-check (default mode)
python audit.py paper.tex
python audit.py paper.typ
python audit.py paper.pdf --pdf-mode enhanced

# Specific modes
python audit.py paper.tex --mode review
python audit.py paper.pdf --mode gate --pdf-mode basic

# Venue-specific checklist
python audit.py paper.tex --mode self-check --venue neurips

# Force language
python audit.py paper.tex --lang zh
```

---

## 5. PDF Parser Design

### 5.1 Class Design

```python
class PdfParser(DocumentParser):
    """PDF document parser implementing DocumentParser interface."""

    def __init__(self, mode: str = "basic"):
        """mode: 'basic' (pymupdf) or 'enhanced' (pymupdf4llm)"""
        self.mode = mode

    def split_sections(self, content: str) -> dict[str, tuple[int, int]]:
        """Basic: font-size heuristics. Enhanced: Markdown header detection."""

    def extract_visible_text(self, line: str) -> str:
        """Return text as-is (no markup in PDF-extracted text)."""

    def clean_text(self, content: str, keep_structure: bool = False) -> str:
        """Remove page numbers, headers/footers, ligatures."""

    def get_comment_prefix(self) -> str:
        return ">"  # Markdown blockquote for PDF audit comments
```

### 5.2 Extraction Modes

| Mode | Library | Method | Speed | Quality |
|------|---------|--------|-------|---------|
| **basic** | `pymupdf` | `page.get_text("text")` + font-size heading detection | ~ms/page | Good for text, loses tables |
| **enhanced** | `pymupdf4llm` | `to_markdown(doc)` with header/table/bold detection | ~10ms/page | Structured Markdown, tables preserved |

### 5.3 Factory Function Update

```python
def get_parser(file_path: str, pdf_mode: str = "basic") -> DocumentParser:
    ext = Path(file_path).suffix.lower()
    if ext == ".tex":
        return LatexParser()
    elif ext == ".typ":
        return TypstParser()
    elif ext == ".pdf":
        return PdfParser(mode=pdf_mode)
    else:
        raise ValueError(f"Unsupported format: {ext}")
```

### 5.4 Known Limitations

- **Math formulas**: Lost in PDF extraction; audit will flag "unable to verify math" and recommend source file
- **Multi-column layouts**: Basic mode may interleave columns; enhanced mode handles most cases
- **Scanned PDFs**: Not supported (would require OCR); clear error message provided

---

## 6. Scoring & Report Engine

### 6.1 Dimension Mapping

Each automated check maps to one or more review dimensions:

```python
DIMENSION_MAP = {
    "format":      ["clarity"],
    "grammar":     ["clarity"],
    "logic":       ["quality", "significance"],
    "sentences":   ["clarity"],
    "deai":        ["clarity", "originality"],
    "bib":         ["quality"],
    "figures":     ["clarity"],
    "consistency": ["clarity"],
    "gbt7714":     ["quality"],
    "checklist":   ["quality", "clarity", "significance", "originality"],
}
```

### 6.2 Scoring Algorithm

```
For each dimension D in {Quality, Clarity, Significance, Originality}:
    1. Collect all issues mapped to D
    2. Base score = 6.0
    3. Deductions: Critical = -1.5, Major = -0.75, Minor = -0.25
    4. Floor at 1.0
    5. Overall = weighted average:
       Quality: 30%, Clarity: 30%, Significance: 20%, Originality: 20%
    6. Map to NeurIPS scale:
       5.5-6.0 → Strong Accept, 4.5-5.4 → Accept,
       3.5-4.4 → Borderline Accept, 2.5-3.4 → Borderline Reject,
       1.5-2.4 → Reject, 1.0-1.4 → Strong Reject
```

### 6.3 Report Template (Markdown)

```markdown
# Paper Audit Report

**File**: paper.tex | **Language**: English | **Mode**: self-check
**Generated**: 2026-02-23 | **Venue**: NeurIPS

## Executive Summary
[1-2 sentence summary of findings]

## Scores
| Dimension     | Score | Issues (C/M/m) | Key Finding              |
|---------------|-------|-----------------|--------------------------|
| Quality       | 4.5   | 0/2/3           | Missing ablation study   |
| Clarity       | 3.75  | 1/3/5           | Long sentences in Methods|
| Significance  | 5.0   | 0/0/1           | Strong contribution      |
| Originality   | 4.25  | 0/1/2           | Some AI-trace detected   |
| **Overall**   | **4.3**|                 | **Borderline Accept**    |

## Issues (sorted by severity)
### Critical
- [FORMAT] (Line 42) [Severity: Critical] [Priority: P0]: Missing figure reference...

### Major
- [GRAMMAR] (Line 87) [Severity: Major] [Priority: P1]: Subject-verb disagreement...

### Minor
- [SENTENCES] (Line 123) [Severity: Minor] [Priority: P2]: Sentence exceeds 60 words...

## Improvement Suggestions
### Abstract
- [Specific actionable suggestion]

### Introduction
- [Specific actionable suggestion]

## Pre-Submission Checklist
- [x] Paper compiles without errors
- [x] All figures referenced in text
- [ ] TODO placeholder found on line 256
- [ ] Anonymous submission: author name detected
```

---

## 7. Execution Flow

```
Input: paper.{tex,typ,pdf} + --mode + --pdf-mode + --venue + --lang
                |
                v
    +--- Format Detection ---------------+
    |  .tex -> LatexParser               |
    |  .typ -> TypstParser               |
    |  .pdf -> PdfParser(mode)           |
    +----------------+-------------------+
                     v
    +--- Language Detection -------------+
    |  --lang override OR                |
    |  CJK ratio > 0.3 -> "zh"          |
    |  else -> "en"                      |
    +----------------+-------------------+
                     v
    +--- Mode -> Check Selection --------+
    |  MODE_CHECKS[mode]                 |
    |  + language-specific extras        |
    +----------------+-------------------+
                     v
    +--- Sequential Check Execution -----+
    |  For each check in selected:       |
    |    import from sibling skill       |
    |    run(parsed_content, lang)       |
    |    collect CheckResult             |
    +----------------+-------------------+
                     v
    +--- Report Generation --------------+
    |  aggregate issues by dimension     |
    |  calculate scores                  |
    |  render Markdown report            |
    |  output to stdout / save file      |
    +------------------------------------+
```

---

## 8. Cross-Skill Import Strategy

```python
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(SKILLS_ROOT / "latex-paper-en" / "scripts"))
sys.path.insert(0, str(SKILLS_ROOT / "latex-thesis-zh" / "scripts"))
sys.path.insert(0, str(SKILLS_ROOT / "typst-paper" / "scripts"))

# Import existing check modules
from check_format import check_format
from analyze_grammar import analyze_grammar
from analyze_logic import analyze_logic
from analyze_sentences import analyze_sentences
from deai_check import check_deai
from verify_bib import verify_bib
from check_figures import check_figures
# Chinese-specific
from check_consistency import check_consistency
```

---

## 9. Dependencies

### New Dependencies

```
pymupdf >= 1.24.0        # PDF basic mode extraction
pymupdf4llm >= 0.0.17    # PDF enhanced mode (Markdown output)
```

### Existing Dependencies (no changes)

```
Pillow                    # Image analysis (already in project)
Python >= 3.9             # Already required
```

---

## 10. Testing Strategy

| Test Type | Scope | Files |
|-----------|-------|-------|
| Unit: PdfParser | Basic/enhanced extraction, section splitting | `test_pdf_parser.py` |
| Unit: detect_language | CJK ratio detection, edge cases | `test_detect_language.py` |
| Unit: report_generator | Score calculation, Markdown rendering | `test_report_generator.py` |
| Integration: audit.py | Full pipeline with .tex/.typ/.pdf samples | `test_audit.py` |
| Regression: existing parsers | Ensure LatexParser/TypstParser unchanged | Existing `test_parsers.py` |

---

## 11. Feasibility Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Technical feasibility | 5/5 | 70-80% reuse, well-defined interfaces |
| PDF support | 4/5 | PyMuPDF mature; academic PDF layouts can be tricky |
| Chinese support | 5/5 | latex-thesis-zh has Chinese-specific modules |
| Scoring accuracy | 3/5 | Automated checks cover Clarity well; Quality/Significance/Originality need LLM judgment |
| Implementation effort | 4/5 | ~6 new files, ~900 lines total, rest is integration |
| Maintenance cost | 5/5 | Delegates to existing modules; changes propagate |

### Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| PDF section detection inaccuracy | Medium | Font-size heuristics + Markdown header fallback; recommend source files |
| PDF math/formula loss | Medium | Flag as "unable to verify math" rather than guessing |
| Scoring subjectivity | High | Clearly label automated vs LLM-judgment scores; provide evidence |
| Cross-module import path conflicts | Low | Explicit sys.path manipulation with skill-root anchoring |
| Large PDF processing time | Low | pymupdf is ~ms per page; warn if >100 pages |

---

## 12. Implementation Order

1. **`parsers.py`** — Thin re-export layer (verify imports work)
2. **`detect_language.py`** — Simple CJK ratio detection (~40 lines)
3. **`pdf_parser.py`** — PdfParser implementing DocumentParser interface (~150 lines)
4. **`audit.py`** — Main orchestrator with 3 modes (~300 lines)
5. **`report_generator.py`** — Scoring engine + Markdown rendering (~200 lines)
6. **`SKILL.md`** — Skill definition with triggers, modules, output protocol (~200 lines)
7. **Reference docs** — `REVIEW_CRITERIA.md`, `CHECKLIST.md`, `AUDIT_GUIDE.md`
8. **Tests** — Unit + integration tests for all new components
9. **Documentation** — Update VitePress docs with paper-audit skill page

---

## 13. Conclusion

The `paper-audit` skill is **highly feasible** with a clear competitive advantage:

- **No existing tool** provides PDF + LaTeX + Typst + Chinese + English + 3-mode audit in one skill
- **70-80% of core logic already exists** in well-tested sibling skills
- The **DocumentParser abstraction** makes adding PDF support clean
- The **REVIEWER_PERSPECTIVE.md** already defines the scoring framework
- Main new work: orchestration layer (~300 lines) + PDF parser (~150 lines) + report generator (~200 lines)

The biggest challenge is PDF extraction quality for academic documents, mitigated by dual-mode extraction and recommending source files for full accuracy.
