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

### Trigger Words

| Module | Triggers | Function |
|--------|----------|----------|
| Compile | compile, 编译, typst compile | Typst compilation |
| Format Check | format, lint, style check | Format checking |
| Grammar Analysis | grammar, proofread | Grammar analysis |
| Long Sentence | long sentence, simplify | Sentence decomposition |
| Expression | academic tone, improve writing | Expression optimization |
| Translation | translate, 翻译, 中译英 | Chinese-English translation |
| Bibliography | bib, bibliography, citation | Bibliography checking |
| De-AI Polishing | deai, 去AI化, humanize | Reduce AI writing traces |
| Template | template, IEEE, ACM | Template configuration |

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

### IEEE Template

```typst
#import "@preview/charged-ieee:0.1.0": ieee

#show: ieee.with(
  title: [Your Paper Title],
  authors: (
    (
      name: "Author Name",
      department: [Department],
      organization: [University],
      location: [City, Country],
      email: "author@email.com"
    ),
  ),
  abstract: [
    Your abstract here...
  ],
  index-terms: ("Machine Learning", "Deep Learning"),
  bibliography: bibliography("references.bib"),
)

// Your content here
```

### ACM Template

```typst
// ACM two-column format
#set page(
  paper: "us-letter",
  margin: (x: 0.75in, y: 1in),
  columns: 2,
  column-gutter: 0.33in
)

#set text(font: "Linux Libertine", size: 9pt)
#set par(justify: true)
```

### Generic Academic Paper Template

```typst
#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm)
)

#set text(
  font: "Times New Roman",
  size: 11pt,
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.65em,
  first-line-indent: 1.5em
)

#set heading(numbering: "1.1")

// Title
#align(center)[
  #text(size: 16pt, weight: "bold")[Your Paper Title]
  
  #v(0.5em)
  
  Author Name#super[1], Co-author Name#super[2]
  
  #v(0.3em)
  
  #text(size: 10pt)[
    #super[1]University Name, #super[2]Institution Name
  ]
]

// Abstract
#heading(outlined: false, numbering: none)[Abstract]
Your abstract here...

// Main content
= Introduction
Your content here...
```

### Chinese Paper Template

```typst
#set page(
  paper: "a4",
  margin: (x: 3.17cm, y: 2.54cm)
)

#set text(
  font: ("Source Han Serif", "Noto Serif CJK SC"),
  size: 12pt,
  lang: "zh",
  region: "cn"
)

#set par(
  justify: true,
  leading: 1em,
  first-line-indent: 2em
)

#set heading(numbering: "1.1")

// Title
#align(center)[
  #text(size: 18pt, weight: "bold")[论文标题]
  
  #v(0.5em)
  
  作者姓名#super[1]，合作者姓名#super[2]
  
  #v(0.3em)
  
  #text(size: 10.5pt)[
    #super[1]大学名称，#super[2]机构名称
  ]
]

// Abstract
#heading(outlined: false, numbering: none)[摘要]
摘要内容...

*关键词*：关键词1；关键词2；关键词3

// Main content
= 引言
正文内容...
```

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

## Next Steps

- [Compilation Guide](/guides/compilation)
- [Format Checking Guide](/guides/format-checking)
- [Bibliography Guide](/guides/bibliography)
