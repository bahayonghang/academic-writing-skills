# Typst Papers (typst-paper)

Modern academic paper writing assistant with Typst.

## Overview

The `typst-paper` skill provides comprehensive support for academic paper writing using Typst, a modern typesetting system that compiles in milliseconds. Supports both English and Chinese papers for major publication venues.

### Key Features

- **Lightning-fast compilation** (millisecond-level vs LaTeX's seconds)
- **Clean, intuitive syntax** (easier learning curve than LaTeX)
- **Real-time preview** with watch mode
- **Format checking** with venue-specific rules
- **Grammar analysis** for English papers
- **Academic expression optimization** for both languages
- **Chinese-to-English translation** (Deep Learning, Time Series, Industrial Control)
- **De-AI writing analysis** for reducing AI-generated text traces
- **Template support** (IEEE, ACM, Springer, NeurIPS, etc.)

## Environment Requirements

**Installation**:
```bash
# Using Cargo (Rust package manager)
cargo install typst-cli

# Using Homebrew (macOS)
brew install typst

# Using package manager (Linux)
sudo pacman -S typst  # Arch Linux
```

**Verify installation**:
```bash
typst --version
```

## Using the Skill in Claude Code

This skill is designed to work with Claude Code and similar AI assistants. Simply mention the relevant trigger words in your conversation, and the assistant will activate the appropriate module.

### Argument Conventions

Provide clear inputs in your request:
- **Main `.typ` path** (required for tool execution)
- **Target scope** (section/chapter or full document)
- **Module choice** (compile / format / grammar / template / etc.)

If any of these are missing or ambiguous, the assistant will ask for clarification instead of guessing.

### Execution Guardrails

- Tools/scripts run **only** when you explicitly request execution.
- Operations that overwrite outputs require explicit confirmation.

### Trigger Words

| Module | Triggers | Function |
|--------|----------|----------|
| Compile | compile, 编译, typst compile | Typst compilation |
| Format Check | format, lint, style check | Format checking |
| Grammar Analysis | grammar, proofread | Grammar analysis |
| Long Sentence | long sentence, simplify | Sentence decomposition |
| Expression | academic tone, improve writing | Expression optimization |
| Logic & Methodology | logic, coherence, 逻辑, 衔接, methodology | Logical coherence & methodological depth |
| Translation | translate, 翻译, 中译英 | Chinese-English translation |
| Bibliography | bib, bibliography, citation | Bibliography checking |
| Reference Integrity | ref, label, reference check | Figure/table reference validation 🆕 |
| De-AI Polishing | deai, 去AI化, humanize | Reduce AI writing traces |
| Template | template, IEEE, ACM | Template configuration |
| Title Optimization | title, 标题, title optimization 🆕 | Generate and optimize titles |

### Example Usage

**Compile your paper**:
```
Please compile my Typst paper main.typ
```

**Check grammar**:
```
Can you check the grammar in my introduction section?
```

**Translate to English**:
```
Translate this Chinese text to academic English (Deep Learning domain):
本文提出了一种基于Transformer的方法...
```

### Quick Examples by Module

```
Check format compliance for main.typ
```

```
Simplify long sentences in the introduction section
```

```
Improve academic tone in the abstract
```

```
Verify references.bib and check citations in main.typ
```

```
Reduce AI writing traces in the methods section
```

```
Provide an IEEE template setup for Typst
```

## Compilation Module

### Basic Commands

| Command | Purpose | Notes |
|---------|---------|-------|
| `typst compile main.typ` | Single compilation | Generates PDF |
| `typst watch main.typ` | Watch mode | Auto-recompile on changes |
| `typst compile main.typ output.pdf` | Custom output | Specify output filename |
| `typst compile --format png main.typ` | Other formats | PNG, SVG support |
| `typst fonts` | List fonts | Show available system fonts |

### Usage Examples

```bash
# Basic compilation (recommended)
typst compile main.typ

# Watch mode (real-time preview)
typst watch main.typ

# Specify output directory
typst compile main.typ --output build/paper.pdf

# Export as PNG (for preview)
typst compile --format png main.typ

# View available fonts
typst fonts

# Use custom font path
typst compile --font-path ./fonts main.typ
```

### Compilation Speed

- Typst compiles in milliseconds (vs LaTeX's seconds)
- Incremental compilation: only recompiles changed parts
- Perfect for real-time preview and rapid iteration

### Chinese Support

```typst
// Chinese font configuration
#set text(
  font: ("Source Han Serif", "Noto Serif CJK SC"),
  lang: "zh",
  region: "cn"
)
```

## Format Check Module

### Checks

| Category | Items | Standards |
|----------|-------|-----------|
| Margins | Top/bottom/left/right | Usually 1 inch (2.54cm) |
| Line Spacing | Single/double spacing | Per journal requirements |
| Font | Body font and size | Times New Roman 10-12pt |
| Headings | Heading hierarchy | Clear levels, proper numbering |
| Figures/Tables | Caption format | Figures below, tables above |
| Citations | Citation consistency | Numeric/author-year format |

### Typst Format Configuration

```typst
// Page setup
#set page(
  paper: "a4",  // or "us-letter"
  margin: (x: 2.5cm, y: 2.5cm)
)

// Text setup
#set text(
  font: "Times New Roman",
  size: 11pt,
  lang: "en"
)

// Paragraph setup
#set par(
  justify: true,
  leading: 0.65em,
  first-line-indent: 1.5em
)

// Heading setup
#set heading(numbering: "1.1")
```

## Grammar Analysis Module

LLM-based grammar checking focusing on:
- Subject-verb agreement
- Article usage (a/an/the)
- Tense consistency (methods in past tense, results in present)
- Chinglish detection

### Common Grammar Issues

| Error Type | Example | Correction |
|------------|---------|------------|
| Missing article | propose method | propose a method |
| Subject-verb disagreement | The data shows | The data show |
| Tense inconsistency | We proposed... The results shows | We proposed... The results show |
| Chinglish | more and more | increasingly |

## Long Sentence Analysis Module

### Trigger Conditions

- English: Sentences >50 words OR >3 clauses
- Chinese: Sentences >60 characters OR >3 clauses

### Output Format

```typst
// Long sentence detected (Line 45, 67 words) [Severity: Minor] [Priority: P2]
// Main structure: [Subject + Verb + Object]
// Modifiers:
//   - [Relative clause] which...
//   - [Purpose clause] to...
// Suggested rewrite: [Simplified version]
```

## Academic Expression Module

### English Academic Expressions

| ❌ Weak Verbs | ✅ Academic Alternatives |
|--------------|-------------------------|
| use | employ, utilize, leverage |
| get | obtain, achieve, acquire |
| make | construct, develop, generate |
| show | demonstrate, illustrate, indicate |

### Chinese Academic Expressions

| ❌ Colloquial | ✅ Academic |
|--------------|-------------|
| 很多研究表明 | 大量研究表明 |
| 效果很好 | 具有显著优势 |
| 我们使用 | 本文采用 |
| 可以看出 | 由此可见 |

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

| Relationship | English Signals | Chinese Signals |
|--------------|-----------------|-----------------|
| Addition | furthermore, moreover | 此外、进一步 |
| Contrast | however, nevertheless | 然而、但是 |
| Cause-Effect | therefore, consequently | 因此、由此可见 |
| Sequence | first, subsequently, finally | 首先、随后、最后 |
| Example | for instance, specifically | 例如、具体而言 |

### Methodological Depth Checklist

- Each claim is supported by evidence (data, citation, or logical reasoning)
- Method choices are justified (why this approach over alternatives?)
- Limitations are acknowledged explicitly
- Assumptions are stated clearly
- Reproducibility details are sufficient (parameters, datasets, metrics)

### Common Issues

| Issue | Problem | Fix |
|-------|---------|-----|
| Logical gap | Missing connection between paragraphs | Add transition sentence |
| Unsupported claim | Assertion without evidence | Add citation, data, or reasoning |
| Shallow methodology | "We use X" without justification | Explain why X is appropriate |
| Hidden assumptions | Implicit prerequisites | State assumptions explicitly |

### Usage in Claude Code

```
Check logical coherence in my introduction section
```

```
Analyze methodological depth in the methods section
```

```
Add transition signals between paragraphs
```

## Translation Module (Chinese → English)

### Supported Domains

| Domain | Keywords |
|--------|----------|
| Deep Learning | neural networks, attention, loss functions |
| Time Series | forecasting, ARIMA, temporal patterns |
| Industrial Control | PID, fault detection, SCADA |

### Translation Workflow

1. **Domain Identification** - Identify technical terms
2. **Terminology Confirmation** - Confirm translations
3. **Translation with Annotations** - Translate with notes
4. **Chinglish Check** - Detect and fix common errors
5. **Academic Polish** - Final review

### Common Academic Phrases

| Chinese | English |
|---------|---------|
| 本文提出... | We propose... / This paper presents... |
| 实验结果表明... | Experimental results demonstrate that... |
| 与...相比 | Compared with... / In comparison to... |
| 综上所述 | In summary / In conclusion |

## Bibliography Module

### Typst Bibliography Management

**Method 1: Using BibTeX files**
```typst
#bibliography("references.bib", style: "ieee")
```

**Method 2: Using Hayagriva format**
```typst
#bibliography("references.yml", style: "apa")
```

### Supported Citation Styles

- `ieee` - IEEE numeric citations
- `apa` - APA author-year
- `chicago-author-date` - Chicago author-year
- `mla` - MLA humanities
- `gb-7714-2015` - Chinese national standard

### Citation Examples

```typst
// In-text citations
According to @smith2020, the method...
Recent studies @smith2020 @jones2021 show...

// Bibliography list
#bibliography("references.bib", style: "ieee")
```

```bash
# With online verification
python scripts/verify_bib.py references.bib --online
python scripts/verify_bib.py references.bib --online --email you@example.com
```

## De-AI Polishing Module

Reduce AI writing traces while preserving Typst syntax and technical accuracy.

### Input Requirements

1. **Source type** (required): Typst
2. **Section** (required): Abstract / Introduction / Related Work / Methods / Experiments / Results / Discussion / Conclusion
3. **Source snippet** (required): Paste directly with original indentation

### Workflow

**1. Syntax Structure Identification**
Preserve all Typst constructs:
- Functions: `#set`, `#show`, `#let`
- References: `@cite`, `@ref`, `@label`
- Math: `$...$`, `$ ... $` (block-level)
- Markup: `*bold*`, `_italic_`, `` `code` ``
- Custom functions (unchanged by default)

**2. AI Pattern Detection**:

| Type | Examples | Issue |
|------|----------|-------|
| Empty phrases | significant, comprehensive, effective | Lack specificity |
| Over-confident | obviously, necessarily, completely | Too absolute |
| Mechanical structures | Empty three-part parallelisms | Lack depth |
| Template expressions | in recent years, more and more | Clichés |

**3. Text Rewriting** (visible text only):
- Split long sentences (English >50 words, Chinese >50 characters)
- Adjust word order for natural flow
- Replace vague claims with specific statements
- Delete redundant phrases
- Add necessary subjects without introducing new facts

**4. Output Generation**:
```typst
// ============================================================
// DE-AI EDITING (Line 23 - Introduction)
// ============================================================
// Original: This method achieves significant performance improvement.
// Revised: The proposed method improves performance in the experiments.
//
// Changes:
// 1. Removed vague phrase: "significant" → deleted
// 2. Kept the claim without adding new metrics or baselines
//
// ⚠️ [PENDING VERIFICATION]: Add exact metrics/baselines only if supported by data
// ============================================================

= Introduction
The proposed method improves performance in the experiments...
```

### Hard Constraints

- **Never modify**: `@cite`, `@ref`, `@label`, math environments
- **Never add**: new data, metrics, comparisons, contributions, experimental settings, citation numbers
- **Only modify**: visible paragraph text, section titles

### Section-Specific Guidelines

| Section | Focus | Constraints |
|---------|-------|-------------|
| Abstract | Purpose/Method/Key Results (with numbers)/Conclusion | No generic claims |
| Introduction | Importance → Gap → Contribution (verifiable) | Restrain claims |
| Related Work | Group by line, specific differences | Concrete comparisons |
| Methods | Reproducibility (process, parameters, metrics) | Implementation details |
| Results | Report facts and numbers only | No interpretation |
| Discussion | Mechanisms, boundaries, failures, limitations | Critical analysis |
| Conclusion | Answer research questions, no new experiments | Actionable future work |

## Template Configuration Module

Template examples are maintained in:
- `references/TEMPLATES.md`

## Venue-Specific Rules

### IEEE

- Two-column format, 0.33 inch column gap
- Times New Roman 10pt
- Active voice, methods in past tense
- Figure/table numbering: Fig. 1, Table I

### ACM

- Two-column format, A4 or US Letter
- Present tense for general truths
- Citation format: numeric or author-year

### Springer

- Figure captions below, table captions above
- References in alphabetical order

### NeurIPS/ICML

- 8-page limit (excluding references)
- Anonymous submission (double-blind review)
- Specific formatting requirements

## Typst Advantages

### vs LaTeX

| Feature | Typst | LaTeX |
|---------|-------|-------|
| Compilation Speed | Milliseconds | Seconds |
| Syntax | Clean and intuitive | Complex and verbose |
| Error Messages | Clear and friendly | Cryptic and confusing |
| Learning Curve | Gentle | Steep |
| Real-time Preview | Native support | Requires additional tools |

### Use Cases

- ✅ Rapid prototyping and drafts
- ✅ Documents requiring frequent modifications
- ✅ Team collaboration (simple syntax)
- ✅ Small to medium papers (<100 pages)
- ⚠️ Complex mathematical formulas (LaTeX more mature)
- ⚠️ Specific journal templates (may require LaTeX)

## Quick Start

**Install Typst**:
```bash
# Using Cargo (Rust package manager)
cargo install typst-cli

# Using Homebrew (macOS)
brew install typst

# Using package manager (Linux)
sudo pacman -S typst  # Arch Linux
```

**Create your first paper**:
```bash
# Initialize from template
typst init @preview/charged-ieee

# Compile
typst compile main.typ

# Watch mode (recommended)
typst watch main.typ
```

**Common commands**:
```bash
# View help
typst --help

# View available fonts
typst fonts

# Specify output format
typst compile --format png main.typ

# Use custom fonts
typst compile --font-path ./fonts main.typ
```

## Reference Files

- `references/TYPST_SYNTAX.md`: Typst syntax guide
- `references/STYLE_GUIDE.md`: Academic writing rules
- `references/COMMON_ERRORS.md`: Common mistakes
- `references/VENUES.md`: Conference/journal requirements
- `references/DEAI_GUIDE.md`: De-AI writing guide
- `references/TEMPLATES.md`: Typst template examples
- `scripts/check_references.py`: Reference integrity checker (standalone)
- `scripts/online_bib_verify.py`: Online bibliography verifier

## Title Optimization Module

Generate and optimize paper titles for both English and Chinese papers following best practices.

### Key Principles

Based on IEEE/ACM/Springer/NeurIPS guidelines and GB/T 7713.1-2006 (for Chinese):

**English Papers**:
1. **Conciseness**: Remove "A Study of", "Research on", "Novel", "New"
2. **Searchability**: Key terms (Method + Problem) in first 65 characters
3. **Length**: Optimal 10-15 words
4. **Specificity**: Concrete method/problem names
5. **Jargon-Free**: Avoid obscure abbreviations

**Chinese Papers**:
1. **简洁性**: Remove "关于...的研究", "新型", "改进的"
2. **可搜索性**: Key terms in first 20 characters
3. **长度**: Optimal 15-25 characters
4. **具体性**: Concrete terms
5. **规范性**: Follow standards

### Quality Scoring

Each title receives a score (0-100) based on five criteria with language-specific thresholds.

### Usage in Claude Code

**Check existing title**:
```
Check the quality of my paper title
检查我的论文标题质量
```

**Generate title candidates**:
```
Generate title candidates for my paper
根据摘要生成标题候选方案
```

**Optimize existing title**:
```
Optimize my paper title to follow IEEE best practices
优化我的论文标题
```

The assistant will:
- Auto-detect language (English/Chinese)
- Provide quality score with breakdown
- Generate multiple ranked candidates
- Suggest Typst code for the best title

### Title Patterns

**English**:
- Method for Problem: "Transformer for Time Series Forecasting"
- Method: Problem in Domain: "Graph Neural Networks: Fault Detection in Industrial Systems"
- Problem via Method: "Time Series Forecasting via Attention Mechanisms"

**Chinese**:
- 问题的方法: "时间序列预测的Transformer方法"
- 方法及应用: "注意力机制及其在工业控制中的应用"
- 面向领域的方法: "面向智能制造的深度学习方法"

### Good vs Bad Examples

**English**:
```
Good: "Transformer for Time Series Forecasting in Industrial Control"
Bad:  "A Novel Study on Improved Time Series Forecasting Using Transformers"
```

**Chinese**:
```
好：工业控制系统时间序列预测的Transformer方法
差：关于基于Transformer的工业控制系统时间序列预测的研究
```

### Typst Title Configuration

**English Paper**:
```typst
#align(center)[
  #text(size: 18pt, weight: "bold")[
    Transformer-Based Time Series Forecasting for Industrial Control
  ]
]
```

**Chinese Paper**:
```typst
#align(center)[
  #text(size: 18pt, weight: "bold", font: "Source Han Serif")[
    工业控制系统时间序列预测的Transformer方法
  ]
  
  #v(0.5em)
  
  #text(size: 14pt, font: "Times New Roman")[
    Transformer-Based Time Series Forecasting for Industrial Control Systems
  ]
]
```

### Best Practices

**English**:
1. Start with keywords (Method + Problem in first 10 words)
2. Be specific ("Transformer" > "Deep Learning")
3. Remove fluff ("Novel", "Study", "Research")
4. Target 10-15 words
5. Match venue style

**Chinese**:
1. 关键词前置（方法+问题在前20字）
2. 具体明确（"Transformer" > "深度学习"）
3. 删除冗余（"关于"、"研究"、"新型"）
4. 目标 15-25 字
5. 符合规范

### References

- [IEEE Author Center](https://conferences.ieeeauthorcenter.ieee.org/)
- [Royal Society Blog on Title Optimization](https://royalsociety.org/blog/2025/01/title-abstract-and-keywords-a-practical-guide-to-maximizing-the-visibility-and-impact-of-your-papers/)
- GB/T 7713.1-2006 (Chinese thesis standards)

## Recommended Workflows

### Fast Iteration (Drafting)
1. Compile or watch mode
2. Format check (basic)
3. Grammar analysis (abstract + intro)

### Pre-Submission Pass
1. Format check (venue-specific)
2. Expression optimization
3. De-AI polishing
4. Bibliography verification
5. Template check (if required by venue)
