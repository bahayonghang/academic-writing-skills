# English Papers (latex-paper-en)

Complete toolkit for English academic paper writing with LaTeX.

## Overview

The `latex-paper-en` skill provides comprehensive support for writing English academic papers in LaTeX, with a focus on major publication venues (IEEE, ACM, Springer, NeurIPS, etc.).

### Key Features

- **Multiple compilation recipes** (pdflatex, xelatex, latexmk, with bibliography workflows)
- **ChkTeX integration** for LaTeX linting
- **Format checking** with venue-specific rules (IEEE, ACM, Springer)
- **Bibliography verification** (BibTeX format validation)
- **Prose extraction** for grammar checking
- **Style guide references** (Common Chinglish errors, academic writing best practices)
- **Chinese-to-English academic translation** (Deep Learning, Time Series, Industrial Control domains)
- **De-AI writing analysis** for reducing AI-generated text traces

## Environment Requirements

> **Note**: This skill assumes LaTeX environment is already configured on your system.

**Windows**: MiKTeX or TeX Live installed and added to PATH
**macOS/Linux**: TeX Live installed

Required tools: `pdflatex`, `xelatex`, `latexmk`, `biber`, `chktex`

## Using the Skill in Claude Code

This skill is designed to work with Claude Code and similar AI assistants. Simply mention the relevant trigger words in your conversation, and the assistant will activate the appropriate module.

### Argument Conventions

Provide clear inputs in your request:
- **Main `.tex` path** (required for tool execution)
- **Target scope** (section/chapter or full document)
- **Module choice** (compile / format / grammar / translation / etc.)

If any of these are missing or ambiguous, the assistant will ask for clarification instead of guessing.

### Execution Guardrails

- Tools/scripts run **only** when you explicitly request execution.
- Destructive operations (`--clean`, `--clean-all`) require explicit confirmation.

### Example Usage

**Compile your paper**:
```
Please compile my LaTeX paper main.tex using xelatex with bibtex
```

**Check format**:
```
Can you check the format of my paper for IEEE conference submission?
```

**Translate to English**:
```
Translate this Chinese text to academic English (Deep Learning domain):
本文提出了一种基于Transformer的方法...
```

**De-AI polishing**:
```
Please reduce AI writing traces in my introduction section
```

## Modular Design

The skill uses a modular design where each module can be invoked independently:

| Module | Triggers | Function |
|--------|----------|----------|
| Compile | compile, 编译, build | LaTeX compilation |
| Format Check | format, chktex, lint | Format checking |
| Grammar Analysis | grammar, proofread | Grammar analysis |
| Sentence Decomposition | long sentence, simplify | Long sentence decomposition |
| Expression | academic tone, improve writing | Expression optimization |
| Logic & Methodology | logic, coherence, methodology, argument | Logical coherence & methodological depth |
| Translation | translate, 翻译, 中译英 | Chinese-English translation |
| Bibliography | bib, bibliography | Bibliography checking |
| Reference Integrity | ref, label, reference check | Figure/table reference validation 🆕 |
| De-AI Polishing | deai, 去AI化, humanize | Reduce AI writing traces |
| Title Optimization | title, 标题, title optimization | Generate and optimize titles 🆕 |

## Output Protocol

All suggestions must use a diff-comment style and include fixed fields:
- **Severity**: Critical / Major / Minor
- **Priority**: P0 / P1 / P2

Minimal template:
```latex
% <MODULE> (Line <N>) [Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <Issue>
% Before: ...
% After:  ...
% Rationale: ...
% ⚠️ [PENDING VERIFICATION]: <if evidence/metric is required>
```

If a tool fails (missing script/tool or invalid path), respond with an error comment and a safe next step.

## Compile Module

### Tools (matching VS Code LaTeX Workshop)

| Tool | Command | Args |
|------|---------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| pdflatex | `pdflatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir=%OUTDIR%` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

### Recipes

| Recipe | Steps |
|--------|-------|
| XeLaTeX | xelatex |
| PDFLaTeX | pdflatex |
| LaTeXmk | latexmk |
| xelatex -> bibtex -> xelatex*2 | xelatex → bibtex → xelatex → xelatex |
| xelatex -> biber -> xelatex*2 | xelatex → biber → xelatex → xelatex |
| pdflatex -> bibtex -> pdflatex*2 | pdflatex → bibtex → pdflatex → pdflatex |
| pdflatex -> biber -> pdflatex*2 | pdflatex → biber → pdflatex → pdflatex |

### Usage in Claude Code

Simply ask the assistant to compile your paper with specific requirements:

**Basic compilation**:
```
Compile main.tex using xelatex
```

**With bibliography** (recommended for papers):
```
Compile main.tex with xelatex and bibtex workflow
```

**With custom output directory**:
```
Compile main.tex using latexmk and output to build directory
```

**Clean auxiliary files**:
```
Clean auxiliary files for main.tex
```

The assistant will execute the appropriate compilation commands based on your request.

**Script CLI:**
```bash
python scripts/compile.py main.tex
python scripts/compile.py main.tex --biber
python scripts/compile.py main.tex --outdir build
python scripts/compile.py main.tex --recipe xelatex-biber
```

### Failure Handling

- Missing LaTeX tools: install TeX Live/MiKTeX and ensure PATH is set
- Missing file/script: verify working directory and `scripts/` path
- Compilation error: summarize the first error and request the relevant log snippet

## Format Check Module

### Usage in Claude Code

Ask the assistant to check your paper format:

```
Check the format of main.tex
```

```
Check main.tex format with strict mode for IEEE submission
```

The assistant will analyze your paper and provide format suggestions.

## Grammar Analysis Module

LLM-based grammar checking focusing on:
- Subject-verb agreement
- Article usage (a/an/the)
- Tense consistency
- Chinglish detection

**Script CLI (MVP):**
```bash
python scripts/analyze_grammar.py main.tex
python scripts/analyze_grammar.py main.tex --section introduction
```

### Usage in Claude Code

Ask the assistant to check grammar:

```
Check the grammar in my introduction section
```

```
Proofread the methods section and fix Chinglish errors
```

## Sentence Decomposition Module

Decompose long sentences (>50 words or >3 clauses) to improve readability.

**Script CLI (MVP):**
```bash
python scripts/analyze_sentences.py main.tex
python scripts/analyze_sentences.py main.tex --section methods --max-words 45 --max-clauses 3
```

### Usage in Claude Code

```
Simplify the long sentence in Section 3
```

```
Split sentences longer than 50 words in my introduction
```

## Expression Module

Improve academic tone by replacing weak verbs and colloquial phrasing.

**Script CLI (MVP):**
```bash
python scripts/improve_expression.py main.tex
python scripts/improve_expression.py main.tex --section related
```

### Usage in Claude Code

```
Improve academic tone in the abstract
```

```
Replace weak verbs in the related work section
```

## Logic & Methodology Module

Ensure logical flow between paragraphs and strengthen methodological rigor in academic writing.

### AXES Model for Paragraph Coherence

| Component | Description | Example |
|-----------|-------------|---------|
| **A**ssertion | Clear topic sentence stating the main claim | "Attention mechanisms improve sequence modeling." |
| **X**ample | Concrete evidence or data supporting the claim | "In our experiments, attention achieved 95% accuracy." |
| **E**xplanation | Analysis of why the evidence supports the claim | "This improvement stems from the ability to capture long-range dependencies." |
| **S**ignificance | Connection to broader argument or next paragraph | "This finding motivates our proposed architecture." |

### Transition Signals

| Relationship | Signals |
|--------------|---------|
| Addition | furthermore, moreover, in addition, additionally |
| Contrast | however, nevertheless, in contrast, conversely |
| Cause-Effect | therefore, consequently, as a result, thus |
| Sequence | first, subsequently, finally, meanwhile |
| Example | for instance, specifically, in particular |

### Methodological Depth Checklist

- Each claim is supported by evidence (data, citation, or logical reasoning)
- Method choices are justified (why this approach over alternatives?)
- Limitations are acknowledged explicitly
- Assumptions are stated clearly
- Reproducibility details are sufficient (parameters, datasets, metrics)

### Common Issues

| Issue | Problem | Fix |
|-------|---------|-----|
| Logical gap | Missing connection between paragraphs | Add transition sentence explaining the relationship |
| Unsupported claim | Assertion without evidence | Add citation, data, or reasoning |
| Shallow methodology | "We use X" without justification | Explain why X is appropriate for this problem |
| Hidden assumptions | Implicit prerequisites | State assumptions explicitly |

### Usage in Claude Code

```
Check logical coherence in my introduction section
```

```
Analyze methodological depth in the methods section
```

```
Add transition signals between paragraphs in Section 3
```

**Script CLI (MVP):**
```bash
python scripts/analyze_logic.py main.tex
python scripts/analyze_logic.py main.tex --section methods
```

## Translation Module (Chinese → English)

### Supported Domains

| Domain | Keywords |
|--------|----------|
| Deep Learning | neural networks, attention, loss functions |
| Time Series | forecasting, ARIMA, sliding window |
| Industrial Control | PID control, fault detection, SCADA |

### Translation Workflow

1. **Terminology Confirmation** - Identify terms and confirm translations
2. **Structure Analysis** - Analyze paragraph structure, determine tense
3. **Sentence Translation** - Translation with annotations
4. **Chinglish Check** - Detect and fix common errors
5. **Academic Polish** - Final review

**Script CLI (MVP):**
```bash
python scripts/translate_academic.py "本文提出了一种基于Transformer的方法" --domain deep-learning
python scripts/translate_academic.py input_zh.txt --domain industrial-control --output translation_report.md
```

### Usage Examples

**Basic Translation Request**:
```
Translate the following to academic English (Deep Learning domain):
本文提出了一种基于Transformer的时间序列预测方法...
```

**With Venue Specification**:
```
Translate the following for IEEE Transactions format:
实验结果表明，我们的方法在多个数据集上取得了最优性能...
```

## Bibliography Module

### Usage in Claude Code

Ask the assistant to verify your bibliography:

```
Verify references.bib for format errors
```

```
Check references.bib against main.tex for unused entries
```

The assistant will check for:
- Required field completeness
- Duplicate entries
- Unused entries
- Citation format consistency

**Script CLI:**
```bash
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --tex main.tex
python scripts/verify_bib.py references.bib --tex main.tex --json
# With online verification (CrossRef + Semantic Scholar)
python scripts/verify_bib.py references.bib --online
python scripts/verify_bib.py references.bib --online --email you@example.com
```

Result includes `missing_in_bib` and `unused_in_tex` for citation consistency.

## De-AI Polishing Module

Reduce AI-generated writing traces while preserving LaTeX syntax and technical accuracy.

### Features

- **AI trace detection** with pattern matching
- **Section-wise analysis** with density scores
- **Batch processing** for entire chapters
- **Syntax-preserving editing** (LaTeX commands, math, citations)

### Usage in Claude Code

**Interactive analysis** (single section):
```
Analyze AI writing traces in my introduction section
```

**Full document analysis**:
```
Check AI trace density across all sections in paper.tex
```

**Reduce AI traces**:
```
Reduce AI writing traces in the methods section while preserving technical accuracy
```

**Batch processing**:
```
Process all sections in paper.tex to reduce AI traces
```

### Output Example

```
================================================================================
DE-AI WRITING TRACE ANALYSIS REPORT
================================================================================
File: paper.tex
Total lines: 450

--------------------------------------------------------------------------------
SECTION-WISE AI TRACE DENSITY
--------------------------------------------------------------------------------

[HIGH] INTRODUCTION
  AI trace density: 8.5%
  Traces found: 12 / 141 lines

[MEDIUM] METHODS
  AI trace density: 3.2%
  Traces found: 5 / 156 lines
```

### Reference Documentation

See `references/DEAI_GUIDE.md` for:
- Common AI patterns to remove
- Section-specific guidelines
- Output format specifications
- Quick reference replacements



## Reference Files

- `references/TERMINOLOGY.md`: Domain terminology (Deep Learning, Time Series, Industrial Control)
- `references/TRANSLATION_GUIDE.md`: Translation principles, Chinglish corrections
- `references/STYLE_GUIDE.md`: Academic writing rules
- `references/COMMON_ERRORS.md`: Common mistakes
- `references/VENUES.md`: Conference/journal requirements
- `references/DEAI_GUIDE.md`: De-AI writing guide and AI pattern detection
- `references/CITATION_VERIFICATION.md`: Citation verification workflow
- `scripts/check_references.py`: Reference integrity checker (standalone)
- `scripts/online_bib_verify.py`: Online bibliography verifier

## Title Optimization Module

Generate and optimize paper titles following IEEE/ACM/Springer/NeurIPS best practices.

### Key Principles

Based on IEEE Author Center and top-tier venue guidelines:

1. **Conciseness**: Remove "A Study of", "Research on", "Novel", "New", "Improved"
2. **Searchability**: Place key terms (Method + Problem) in first 65 characters
3. **Length**: Optimal 10-15 words; acceptable 8-20 words
4. **Specificity**: Use concrete method/problem names, avoid vague terms
5. **Jargon-Free**: Avoid obscure abbreviations (except AI, LSTM, DNA, etc.)

### Quality Scoring

Each title receives a score (0-100) based on:
- Conciseness (25%): No ineffective words
- Searchability (30%): Key terms in first 65 characters
- Length (15%): Within optimal range
- Specificity (20%): Concrete vs vague terms
- Jargon-Free (10%): No obscure abbreviations

### Usage in Claude Code

**Check existing title**:
```
Check the quality of my paper title
```

**Generate title candidates**:
```
Generate title candidates for my paper based on the abstract
```

**Optimize existing title**:
```
Optimize my paper title to follow IEEE best practices
```

The assistant will analyze your title and provide:
- Quality score with breakdown
- Specific issues detected
- Multiple improved candidates (ranked by score)
- Suggested LaTeX code

**Script CLI:**
```bash
python scripts/optimize_title.py main.tex --check
python scripts/optimize_title.py main.tex --generate
python scripts/optimize_title.py main.tex --optimize
python scripts/optimize_title.py main.tex --compare "Title A" "Title B" "Title C"
python scripts/optimize_title.py "papers/*.tex" --batch --output title_report.json
```

### Title Generation Workflow

1. **Content Analysis**: Extract problem, method, domain, key results from abstract/introduction
2. **Keyword Extraction**: Identify 3-5 core keywords (method + problem + domain)
3. **Template Selection**: Choose appropriate pattern (Method for Problem, Problem via Method, etc.)
4. **Candidate Generation**: Create 3-5 variants with different emphasis
5. **Quality Scoring**: Rank candidates by quality score

### Common Title Patterns

| Pattern | Example | Use Case |
|---------|---------|----------|
| Method for Problem | "Transformer for Time Series Forecasting" | General research |
| Method: Problem in Domain | "Graph Neural Networks: Fault Detection in Industrial Systems" | Domain-specific |
| Problem via Method | "Time Series Forecasting via Attention Mechanisms" | Method-focused |
| Method + Feature | "Lightweight Transformer for Real-Time Detection" | Performance-focused |

### Ineffective Words to Remove

| Avoid | Reason |
|-------|--------|
| A Study of | Redundant (all papers are studies) |
| Research on | Redundant (all papers are research) |
| Novel / New | Implied by publication |
| Improved / Enhanced | Vague without specifics |
| Based on | Often unnecessary |
| Using / Utilizing | Can be replaced with prepositions |

### Good vs Bad Examples

```
Good: "Transformer for Time Series Forecasting in Industrial Control"
Bad:  "A Novel Study on Improved Time Series Forecasting Using Transformers"

Good: "Graph Neural Networks for Fault Detection"
Bad:  "Research on Novel Fault Detection Based on GNNs"

Good: "Attention-Based LSTM for Multivariate Time Series Prediction"
Bad:  "An Improved LSTM Model Using Attention Mechanism for Prediction"
```

### Venue-Specific Guidelines

**IEEE Transactions**:
- Avoid formulas with subscripts (except simple ones)
- Use title case (capitalize major words)
- Typical length: 10-15 words

**ACM Conferences**:
- More flexible with creative titles
- Can use colons for subtitles
- Typical length: 8-12 words

**Springer Journals**:
- Prefer descriptive over creative
- Can be slightly longer (up to 20 words)

**NeurIPS/ICML**:
- Concise and impactful (8-12 words)
- Method name often prominent

### Best Practices

1. **Start with keywords**: Put Method + Problem in first 10 words
2. **Be specific**: "Transformer" > "Deep Learning" > "Machine Learning"
3. **Remove fluff**: Delete "Novel", "Study", "Research", "Based on"
4. **Check length**: Aim for 10-15 words (English)
5. **Test searchability**: Would you find this paper with these keywords?
6. **Avoid jargon**: Unless widely recognized (AI, LSTM, CNN)
7. **Match venue style**: IEEE (descriptive), ACM (creative), NeurIPS (concise)

### References

- [IEEE Author Center](https://conferences.ieeeauthorcenter.ieee.org/)
- [Royal Society Blog on Title Optimization](https://royalsociety.org/blog/2025/01/title-abstract-and-keywords-a-practical-guide-to-maximizing-the-visibility-and-impact-of-your-papers/)

## Recommended Workflows

### Fast Pre-Submission Check
1. Format check (strict mode)
2. Grammar analysis (abstract + introduction)
3. Bibliography verification

### Full Quality Pass
1. Format check → fix critical issues
2. Grammar analysis
3. De-AI polishing
4. Sentence decomposition
5. Expression restructuring
6. Bibliography verification

### Translation Pipeline
1. Terminology confirmation
2. Translation with annotations
3. Chinglish check
4. Academic polish
