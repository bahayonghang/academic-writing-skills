---
name: latex-paper-en
description: |
  LaTeX academic paper assistant for English papers (IEEE, ACM, Springer, NeurIPS, ICML).
  Domains: Deep Learning, Time Series, Industrial Control.

  Triggers (use ANY module independently):
  - "compile", "编译", "build latex" → Compilation Module
  - "format check", "chktex", "格式检查" → Format Check Module
  - "grammar", "语法", "proofread", "润色" → Grammar Analysis Module
  - "long sentence", "长句", "simplify" → Sentence Decomposition Module
  - "academic tone", "学术表达", "improve writing" → Expression Module
  - "translate", "翻译", "中译英", "Chinese to English" → Translation Module
  - "bib", "bibliography", "参考文献" → Bibliography Module
---

# LaTeX Academic Paper Assistant (English)

## Critical Rules

1. NEVER modify `\cite{}`, `\ref{}`, `\label{}`, math environments
2. NEVER fabricate bibliography entries
3. NEVER change domain terminology without confirmation
4. ALWAYS output suggestions in diff-comment format first

## Modules (Independent, Pick Any)

### Module: Compile
**Trigger**: compile, 编译, build, pdflatex, xelatex

**Tools** (matching VS Code LaTeX Workshop):
| Tool | Command | Args |
|------|---------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| pdflatex | `pdflatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir=%OUTDIR%` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

**Recipes**:
| Recipe | Steps |
|--------|-------|
| XeLaTeX | xelatex |
| PDFLaTeX | pdflatex |
| LaTeXmk | latexmk |
| xelatex -> bibtex -> xelatex*2 | xelatex → bibtex → xelatex → xelatex |
| xelatex -> biber -> xelatex*2 | xelatex → biber → xelatex → xelatex |
| pdflatex -> bibtex -> pdflatex*2 | pdflatex → bibtex → pdflatex → pdflatex |
| pdflatex -> biber -> pdflatex*2 | pdflatex → biber → pdflatex → pdflatex |

**Usage**:
```bash
# Single compiler
python scripts/compile.py main.tex                          # Auto-detect
python scripts/compile.py main.tex --recipe xelatex         # XeLaTeX only
python scripts/compile.py main.tex --recipe pdflatex        # PDFLaTeX only

# With bibliography (recommended for papers)
python scripts/compile.py main.tex --recipe xelatex-bibtex  # BibTeX workflow
python scripts/compile.py main.tex --recipe xelatex-biber   # Biber workflow
python scripts/compile.py main.tex --recipe pdflatex-bibtex
python scripts/compile.py main.tex --recipe pdflatex-biber

# With output directory
python scripts/compile.py main.tex --recipe latexmk --outdir build

# Utilities
python scripts/compile.py main.tex --clean                  # Clean aux files
python scripts/compile.py main.tex --clean-all              # Clean all (incl. PDF)
```

**Auto-detection**: Script detects Chinese content (ctex, xeCJK, Chinese chars) and auto-selects xelatex.

---

### Module: Format Check
**Trigger**: format, chktex, lint, 格式检查

```bash
python scripts/check_format.py main.tex
python scripts/check_format.py main.tex --strict
```

Output: PASS / WARN / FAIL with categorized issues.

---

### Module: Grammar Analysis
**Trigger**: grammar, 语法, proofread, 润色, article usage

Focus areas:
- Subject-verb agreement
- Article usage (a/an/the)
- Tense consistency (past for methods, present for results)
- Chinglish detection → See [COMMON_ERRORS.md](references/COMMON_ERRORS.md)

Output format:
```latex
% GRAMMAR (Line 23): Article missing
% Before: We propose method for...
% After: We propose a method for...
```

---

### Module: Sentence Decomposition
**Trigger**: long sentence, 长句, simplify, decompose, >50 words

Trigger condition: Sentences >50 words OR >3 subordinate clauses

Output format:
```latex
% LONG SENTENCE (Line 45, 67 words)
% Core: [subject + verb + object]
% Subordinates:
%   - [Relative] which...
%   - [Purpose] to...
% Suggested: [simplified version]
```

---

### Module: Expression Restructuring
**Trigger**: academic tone, 学术表达, improve writing, weak verbs

Weak verb replacements:
- use → employ, utilize, leverage
- get → obtain, achieve, acquire
- make → construct, develop, generate
- show → demonstrate, illustrate, indicate

Output format:
```latex
% EXPRESSION (Line 23): Improve academic tone
% Before: We use machine learning to get better results.
% After: We employ machine learning to achieve superior performance.
```

Style guide: [STYLE_GUIDE.md](references/STYLE_GUIDE.md)

---

### Module: Translation (Chinese → English)
**Trigger**: translate, 翻译, 中译英, Chinese to English

**Step 1: Domain Selection**
Identify domain for terminology:
- Deep Learning: neural networks, attention, loss functions
- Time Series: forecasting, ARIMA, temporal patterns
- Industrial Control: PID, fault detection, SCADA

**Step 2: Terminology Confirmation**
```markdown
| 中文 | English | Domain |
|------|---------|--------|
| 注意力机制 | attention mechanism | DL |
```
Reference: [TERMINOLOGY.md](references/TERMINOLOGY.md)

**Step 3: Translation with Notes**
```latex
% ORIGINAL: 本文提出了一种基于Transformer的方法
% TRANSLATION: We propose a Transformer-based approach
% NOTES: "本文提出" → "We propose" (standard academic)
```

**Step 4: Chinglish Check**
Reference: [TRANSLATION_GUIDE.md](references/TRANSLATION_GUIDE.md)

Common fixes:
- "more and more" → "increasingly"
- "in recent years" → "recently"
- "play an important role" → "is crucial for"

**Quick Patterns**:
| 中文 | English |
|------|---------|
| 本文提出... | We propose... |
| 实验结果表明... | Experimental results demonstrate that... |
| 与...相比 | Compared with... |

---

### Module: Bibliography
**Trigger**: bib, bibliography, 参考文献, citation

```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex  # Check citations
python scripts/verify_bib.py references.bib --standard gb7714
```

Checks: required fields, duplicate keys, unused entries, missing citations.

---

## Venue-Specific Rules

Load from [VENUES.md](references/VENUES.md):
- **IEEE**: Active voice, past tense for methods
- **ACM**: Present tense for general truths
- **Springer**: Figure captions below, table captions above
- **NeurIPS/ICML**: 8 pages, specific formatting

---

## Full Workflow (Optional)

If user requests complete review, execute in order:
1. Format Check → fix critical issues
2. Grammar Analysis → fix errors
3. Sentence Decomposition → simplify complex sentences
4. Expression Restructuring → improve academic tone

---

## References

- [STYLE_GUIDE.md](references/STYLE_GUIDE.md): Academic writing rules
- [COMMON_ERRORS.md](references/COMMON_ERRORS.md): Chinglish patterns
- [VENUES.md](references/VENUES.md): Conference/journal requirements
- [FORBIDDEN_TERMS.md](references/FORBIDDEN_TERMS.md): Protected terminology
- [TERMINOLOGY.md](references/TERMINOLOGY.md): Domain terminology (DL/TS/IC)
- [TRANSLATION_GUIDE.md](references/TRANSLATION_GUIDE.md): Translation guide
