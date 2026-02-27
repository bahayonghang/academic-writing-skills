# QUICK_REFERENCE.md — Paper Audit Tool

Quick lookup for audit modes, checks, CLI arguments, and format compatibility.

---

## 1. Check Support Matrix

| Check | `.tex` EN | `.tex` ZH | `.typ` | `.pdf` | Script |
|-------|-----------|-----------|--------|--------|--------|
| `format` | ✅ | ✅ | ✅ | ❌ | `check_format.py` |
| `grammar` | ✅ | ✅ | ✅ | ✅ | `analyze_grammar.py` |
| `logic` | ✅ | ✅ | ✅ | ✅ | `analyze_logic.py` |
| `sentences` | ✅ | ✅ | ✅ | ✅ | `analyze_sentences.py` |
| `deai` | ✅ | ✅ | ✅ | ✅ | `deai_check.py` |
| `bib` | ✅ | ✅ | ✅ | ❌ | `verify_bib.py` |
| `figures` | ✅ | ✅ | ❌ | ❌ | `check_figures.py` |
| `references` | ✅ | ✅ | ✅ | ❌ | `check_references.py` |
| `visual` | ❌ | ❌ | ❌ | ✅ | `visual_check.py` |
| `consistency` | ❌ | ✅ | ❌ | ❌ | `check_consistency.py` |
| `gbt7714` | ❌ | ✅ | ❌ | ❌ | (ZH only) |
| `checklist` | ✅ | ✅ | ✅ | ✅ | inline Python |

> **Legend**: ✅ = supported, ❌ = skipped/not applicable

---

## 2. Mode × Check Matrix

| Check | `self-check` | `review` | `gate` | `polish` |
|-------|:------------:|:--------:|:------:|:--------:|
| format | ✅ | ✅ | ✅ | ❌ |
| grammar | ✅ | ✅ | ❌ | ❌ |
| logic | ✅ | ✅ | ❌ | ✅ |
| sentences | ✅ | ✅ | ❌ | ✅ |
| deai | ✅ | ✅ | ❌ | ❌ |
| bib | ✅ | ✅ | ✅ | ❌ |
| figures | ✅ | ✅ | ✅ | ❌ |
| references | ✅ | ✅ | ✅ | ❌ |
| visual | ✅ | ✅ | ✅ | ❌ |
| checklist | ❌ | ❌ | ✅ | ❌ |
| consistency (+ZH) | ✅ | ✅ | ✅ | ❌ |
| gbt7714 (+ZH) | ✅ | ✅ | ✅ | ❌ |

> **Note**: `polish` mode runs `logic` + `sentences` as a fast precheck, then dispatches to Critic agent.

---

## 3. CLI Reference

### Basic Usage
```bash
python audit.py <file> [options]
```

### Positional Arguments
| Argument | Description |
|----------|-------------|
| `file` | Path to document (`.tex`, `.typ`, or `.pdf`) |

### Options
| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--mode` | `self-check`, `review`, `gate`, `polish` | `self-check` | Audit mode |
| `--pdf-mode` | `basic`, `enhanced` | `basic` | PDF extraction engine |
| `--venue` | e.g. `neurips`, `ieee`, `acm` | `` | Target venue for rule selection |
| `--lang` | `en`, `zh` | auto-detect | Force language |
| `--style` | `A`, `B`, `C` | `A` | Polish style (A=plain, B=narrative, C=formal) |
| `--journal` | string | `` | Target journal for polish mode |
| `--skip-logic` | flag | off | Skip logic check in polish mode |
| `--online` | flag | off | Enable CrossRef/Semantic Scholar bib verification |
| `--email` | email | `` | Email for CrossRef polite pool |
| `--scholar-eval` | flag | off | Enable ScholarEval 8-dimension assessment |
| `--format` | `md`, `json` | `md` | Output format (Markdown or JSON) |
| `--output`, `-o` | path | stdout | Save report to file |

### Example Commands
```bash
# Quick self-check (default)
python audit.py paper.tex

# Peer review simulation targeting NeurIPS
python audit.py paper.tex --mode review --venue neurips

# Quality gate for CI/CD pipeline (JSON output)
python audit.py paper.tex --mode gate --format json --output audit.json

# Enhanced PDF audit
python audit.py paper.pdf --pdf-mode enhanced --mode self-check

# Chinese thesis with online bib verification
python audit.py thesis.tex --lang zh --online --email you@university.edu

# Polish mode precheck with style B
python audit.py paper.tex --mode polish --style B --journal "Nature"

# Full self-check with ScholarEval
python audit.py paper.tex --scholar-eval
```

---

## 4. Severity & Priority Reference

| Severity | Priority | Meaning | Impact on Score |
|----------|----------|---------|-----------------|
| `Critical` | `P0` | Blocking issue — must fix | -1.5 per issue |
| `Major` | `P1` | Significant problem | -0.75 per issue |
| `Minor` | `P2` | Style/convention issue | -0.25 per issue |

### Score Scale (NeurIPS-style)
| Score Range | Label |
|-------------|-------|
| ≥ 5.5 | Strong Accept |
| ≥ 4.5 | Accept |
| ≥ 3.5 | Borderline Accept |
| ≥ 2.5 | Borderline Reject |
| ≥ 1.5 | Reject |
| < 1.5 | Strong Reject |

---

## 5. Individual Script Reference

These scripts can be run standalone for targeted checks:

```bash
# Format check (strict mode)
python check_format.py paper.tex --strict

# Reference integrity (JSON output)
python check_references.py paper.tex --json

# Visual layout check
python visual_check.py paper.pdf --margin 72 --min-dpi 150

# Bibliography verification (with online lookup)
python verify_bib.py refs.bib --tex paper.tex --online --email me@uni.edu

# Sentence complexity
python analyze_sentences.py paper.tex --max-words 60 --max-clauses 3
```

---

## 6. PDF Extraction Modes

| Mode | Engine | Speed | Accuracy | Best For |
|------|--------|-------|----------|----------|
| `basic` | PyMuPDF | Fast | Good | Most papers |
| `enhanced` | pymupdf4llm | Slower | Better (tables/headers) | Complex layouts |

---

## 7. Output Format Reference

### Markdown (default)
Human-readable report with sections for scores, issues, and checklist.
Pipe to a Markdown viewer or save with `--output report.md`.

### JSON (`--format json`)
Machine-readable structured output for CI/CD integration:
```json
{
  "file": "paper.tex",
  "language": "en",
  "mode": "gate",
  "generated_at": "2026-02-27T10:00:00",
  "scores": { "quality": 5.5, "clarity": 4.75, "overall": 5.1 },
  "verdict": "Accept",
  "issues": [...],
  "checklist": [...]
}
```

---

*Last updated: 2026-02-27*
