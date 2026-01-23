# Chinese Thesis (latex-thesis-zh)

LaTeX assistant for Chinese doctoral/master theses.

## Overview

The `latex-thesis-zh` skill provides modular support for Chinese thesis writing. Modules are independently callable, but **structure mapping should run first for full reviews or multi-file theses**.

## Using the Skill in Claude Code

This skill is designed to work with Claude Code and similar AI assistants. Simply mention the relevant trigger words in your conversation, and the assistant will activate the appropriate module.

### Example Usage

**Compile thesis**:
```
Compile thesis.tex using xelatex with biber
```

**Map structure**:
```
Map the structure of my thesis to check completeness
```

**Check GB/T format**:
```
Check thesis.tex for GB/T 7714-2015 compliance
```

**Reduce AI traces**:
```
Reduce AI writing traces in the introduction chapter
```

### Trigger Words

| Module | Triggers |
|--------|----------|
| Compile | `compile`, `编译`, `xelatex` |
| Structure Mapping | `structure`, `结构`, `映射` |
| GB/T Format Check | `format`, `格式`, `国标`, `GB/T` |
| Academic Expression | `expression`, `表达`, `润色` |
| Long Sentence Analysis | `long sentence`, `长句`, `拆解` |
| Bibliography | `bib`, `bibliography`, `参考文献` |
| Template Detection | `template`, `模板`, `thuthesis` |
| De-AI Polishing | `deai`, `去AI化`, `人性化`, `降低AI痕迹` |

## Output Protocol

All suggestions must use a diff-comment style and include fixed fields:
- **Severity**: Critical / Major / Minor
- **Priority**: P0 / P1 / P2

Minimal template:
```latex
% <模块>（第<N>行）[Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <问题概述>
% 原文：...
% 修改后：...
% 理由：...
% ⚠️ 【待补证】：<需要证据/数据时标记>
```

If a tool fails (missing script/tool or invalid path), respond with an error comment and a safe next step.

## Modules

### Compile Module

XeLaTeX-focused compilation for Chinese documents.

**Tools** (aligned with VS Code LaTeX Workshop):

| Tool | Command | Args |
|------|---------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| lualatex | `lualatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -xelatex` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

**Recipes**:

| Recipe | Steps | Use Case |
|--------|-------|----------|
| XeLaTeX | xelatex | Quick Chinese compile (recommended) |
| LuaLaTeX | lualatex | Complex font requirements |
| LaTeXmk | latexmk -xelatex | Auto dependency handling |
| xelatex-bibtex | xelatex → bibtex → xelatex×2 | Chinese + BibTeX |
| xelatex-biber | xelatex → biber → xelatex×2 | Chinese + Biber (recommended) |
| lualatex-bibtex | lualatex → bibtex → lualatex×2 | LuaLaTeX + BibTeX |
| lualatex-biber | lualatex → biber → lualatex×2 | LuaLaTeX + Biber |

**Usage in Claude Code**:

Ask the assistant to compile your thesis:

```
Compile thesis.tex using xelatex
```

```
Compile thesis.tex with xelatex and biber workflow
```

```
Clean auxiliary files for thesis.tex
```

The assistant will execute the appropriate compilation commands.

**Failure handling**:
- Missing LaTeX tools: install TeX Live/MiKTeX and ensure PATH is set
- Missing file/script: verify working directory and `scripts/` path
- Compilation error: summarize the first error and request the relevant log snippet

### Structure Mapping Module

Analyze multi-file thesis structure. **Run this first for full reviews or multi-file theses**.

**Usage in Claude Code**:

```
Map the structure of thesis.tex
```

```
Analyze the structure of my thesis to check for missing sections
```

**Thesis Structure Requirements**:

| Section | Required Content |
|---------|------------------|
| Front Matter | Cover, Declaration, Abstract (CN+EN), TOC, Symbol List |
| Main Body | Introduction, Related Work, Core Chapters, Conclusion |
| Back Matter | References, Acknowledgments, Publication List |

### GB/T Format Check Module

Verify GB/T 7714-2015 compliance.

**Usage in Claude Code**:

```
Check thesis.tex for GB/T format compliance
```

```
Check thesis.tex format with strict mode
```

**Checks**:
- Bibliography format (biblatex-gb7714-2015)
- Figure/table caption format
- Equation numbering
- Section heading styles

### Academic Expression Module

Detect colloquial expressions and suggest academic alternatives.

**Colloquial → Academic Examples**:

| ❌ Colloquial | ✅ Academic |
|--------------|-------------|
| 很多研究表明 | 大量研究表明 |
| 效果很好 | 具有显著优势 |
| 我们使用 | 本文采用 |

### Long Sentence Analysis Module

Trigger: Sentences >60 characters OR >3 clauses

Output: Core extraction, modifier analysis, rewrite suggestions

### Bibliography Module

**Usage in Claude Code**:

```
Verify refs.bib for GB7714 standard compliance
```

```
Check refs.bib against thesis.tex for format errors
```

### Template Detection Module

**Usage in Claude Code**:

```
Detect the template used in thesis.tex
```

```
Identify which university template my thesis is using
```

**Supported Templates**:

| Template | University |
|----------|------------|
| thuthesis | Tsinghua University |
| pkuthss | Peking University |
| ustcthesis | USTC |
| fduthesis | Fudan University |
| ctexbook | Generic |

### De-AI Polishing Module

Reduce AI writing traces while preserving LaTeX syntax and technical accuracy.

**Input Requirements**:
1. **Source type** (required): LaTeX / Typst
2. **Section** (required): Abstract / Introduction / Related Work / Methods / Experiments / Results / Discussion / Conclusion / Other
3. **Source snippet** (required): paste directly, keep indentation and line breaks

**Usage in Claude Code**:

**Interactive editing** (single section):
```
Analyze AI writing traces in the introduction section of thesis.tex
```

**Batch processing** (chapter or full document):
```
Process chapter3/introduction.tex to reduce AI traces
```

```
Process all sections in thesis.tex to reduce AI traces
```

**AI trace density check**:
```
Analyze AI trace density across all sections in thesis.tex
```

**Workflow**:
1. **Syntax structure identification** (preserve all LaTeX/Typst constructs):
   - Commands: `\command{...}`, `\command[...]{}`
   - References: `\cite{}`, `\ref{}`, `\label{}`, `\eqref{}`, `\autoref{}`
   - Environments: `\begin{...}...\end{...}`
   - Math: `$...$`, `\[...\]`, equation/align environments
   - Custom macros (unchanged by default)
2. **AI pattern detection**:
   - Empty phrases: "significant", "comprehensive", "effective", "important"
   - Over-confident: "obviously", "necessarily", "completely", "clearly"
   - Mechanical structures: empty three-part parallelisms
   - Template expressions: "in recent years", "more and more"
3. **Text rewriting** (visible text only):
   - Split long sentences (>50 words)
   - Adjust word order for natural flow
   - Replace vague claims with specific statements
   - Delete redundant phrases
   - Add required subjects without introducing new facts
4. **Output generation**:
   - A. Rewritten source code (minimal invasive edits)
   - B. Change summary (3-10 bullets)
   - C. Pending verification marks (claims requiring evidence)

**Hard Constraints**:
- **Never modify**: `\cite{}`, `\ref{}`, `\label{}`, math environments
- **Never add**: new data, metrics, comparisons, contributions, experimental settings, citation numbers, or bib keys
- **Only modify**: visible paragraph text, section titles, caption text

**Output Format**:
```latex
% ============================================================
% DE-AI EDITING (Line 23 - Introduction)
% ============================================================
% Original: This method achieves significant performance improvement.
% Revised: The proposed method improves performance in the experiments.
%
% Changes:
% 1. Removed vague phrase: "significant" → deleted
% 2. Kept the claim without adding new metrics or baselines
%
% ⚠️ [PENDING VERIFICATION]: Add exact metrics/baselines only if supported by data
% ============================================================

\section{Introduction}
The proposed method improves performance in the experiments...
```

**Section-Specific Guidelines**:

| Section | Focus | Constraints |
|---------|-------|-------------|
| Abstract | Purpose/Method/Key Results (with numbers)/Conclusion | No generic claims |
| Introduction | Importance → Gap → Contribution (verifiable) | Restrain claims |
| Related Work | Group by line, specific differences | Concrete comparisons |
| Methods | Reproducibility (process, parameters, metrics) | Implementation details |
| Results | Report facts and numbers only | No interpretation |
| Discussion | Mechanisms, boundaries, failures, limitations | Critical analysis |
| Conclusion | Answer research questions, no new experiments | Actionable future work |

Reference: `references/DEAI_GUIDE.md`

## Workflow Suggestions

### Daily Writing

Ask the assistant:
```
Compile thesis.tex using xelatex
```

### Chapter Completion

Ask the assistant:
```
Compile thesis.tex with xelatex and biber, then verify refs.bib for GB7714 compliance
```

### Final Submission

Ask the assistant to perform a complete review:
```
Please perform a complete thesis review:
1. Map the structure of thesis.tex
2. Compile with xelatex and biber
3. Check refs.bib for GB7714 compliance
4. Check consistency across chapters
5. Clean auxiliary files
```

## Common Issues

### Chinese Font Missing

```latex
\setCJKmainfont{SimSun}  % Windows
\setCJKmainfont{STSong}  % macOS
```

### Bibliography Format Incorrect

```latex
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
```

## Next Steps

- [Compilation Guide](/guides/compilation)
- [Bibliography Guide](/guides/bibliography)
- [GB/T 7714 Reference](/references/gb-standard)
