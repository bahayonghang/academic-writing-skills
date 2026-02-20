# Chinese Thesis (latex-thesis-zh)

LaTeX assistant for Chinese doctoral/master theses.

## Overview

The `latex-thesis-zh` skill provides modular support for Chinese thesis writing. Modules are independently callable, but **structure mapping should run first for full reviews or multi-file theses**.

## Using the Skill in Claude Code

This skill is designed to work with Claude Code and similar AI assistants. Simply mention the relevant trigger words in your conversation, and the assistant will activate the appropriate module.

### Argument Conventions

Provide clear inputs in your request:
- **Main `.tex` path** (required for tool execution)
- **Target scope** (chapter/section or full thesis)
- **Module choice** (structure / compile / GB/T / template / etc.)

If any of these are missing or ambiguous, the assistant will ask for clarification instead of guessing.

### Execution Guardrails

- Tools/scripts run **only** when you explicitly request execution.
- Destructive operations (`--clean`, `--clean-all`) require explicit confirmation.

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
| Logic & Methodology | `logic`, `coherence`, `逻辑`, `衔接`, `methodology`, `方法论` |
| Long Sentence Analysis | `long sentence`, `长句`, `拆解` |
| Bibliography | `bib`, `bibliography`, `参考文献` |
| Template Detection | `template`, `模板`, `thuthesis` |
| De-AI Polishing | `deai`, `去AI化`, `人性化`, `降低AI痕迹` |
| Title Optimization | `title`, `标题`, `标题优化`, `生成标题` 🆕 |

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

**Usage in Claude Code**:
```
Improve academic expression in Chapter 2
```

```
Replace colloquial phrases in my abstract
```

### Logic & Methodology Module

Ensure logical flow between paragraphs and strengthen methodological rigor.

**AXES Model for Paragraph Coherence**:

| Component | Description | Example |
|-----------|-------------|---------|
| **A**ssertion | Clear topic sentence | "注意力机制能够提升序列建模效果。" |
| **X**ample | Concrete evidence | "实验中，注意力机制达到95%准确率。" |
| **E**xplanation | Why evidence supports claim | "这一提升源于其捕获长程依赖的能力。" |
| **S**ignificance | Connection to broader argument | "这一发现为本文架构设计提供了依据。" |

**Transition Signals (Chinese)**:

| Relationship | Chinese Signals | English Equivalent |
|--------------|-----------------|-------------------|
| Addition | 此外、进一步、更重要的是 | furthermore, moreover |
| Contrast | 然而、但是、相反 | however, nevertheless |
| Cause-Effect | 因此、由此可见、故而 | therefore, consequently |
| Sequence | 首先、随后、最后 | first, subsequently, finally |
| Example | 例如、具体而言、特别是 | for instance, specifically |

**Common Issues**:

| Issue | Problem | Fix |
|-------|---------|-----|
| 逻辑断层 | Missing connection between paragraphs | Add transition sentence |
| 无据主张 | Assertion without evidence | Add citation, data, or reasoning |
| 方法论浅薄 | "本文采用X" without justification | Explain why X is appropriate |
| 隐含假设 | Implicit prerequisites | State assumptions explicitly |

**Usage in Claude Code**:
```
Check logical coherence in my introduction chapter
```

```
Analyze methodological depth in the methods chapter
```

### Long Sentence Analysis Module

Trigger: Sentences >60 characters OR >3 clauses

Output: Core extraction, modifier analysis, rewrite suggestions

**Usage in Claude Code**:
```
Split long sentences in the introduction chapter
```

```
Analyze sentences longer than 60 characters in Chapter 3
```

### Bibliography Module

**Usage in Claude Code**:

```
Verify refs.bib for GB7714 standard compliance
```

```
Check refs.bib against thesis.tex for format errors
```

Behind the scenes, the assistant uses:
```
python scripts/verify_bib.py references.bib
python scripts/verify_bib.py references.bib --standard gb7714
```

### Template Detection Module

**Usage in Claude Code**:

```
Detect the template used in thesis.tex
```

```
Identify which university template my thesis is using
```

The detector also returns a **key requirements summary** extracted from `references/UNIVERSITIES/`.

**Supported Templates**:

| Template | University |
|----------|------------|
| thuthesis | Tsinghua University |
| pkuthss | Peking University |
| ustcthesis | USTC |
| fduthesis | Fudan University |
| ctexbook | Generic |

**University Guidelines (References)**:

- Yanshan University (2024 thesis writing guidelines): see `references/UNIVERSITIES/yanshan.md` (reference only; template detection still relies on `\documentclass{...}`).

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

### Title Optimization Module

Generate and optimize thesis titles following GB/T 7713.1-2006 standards and international best practices.

#### Key Principles

Based on GB/T 7713.1-2006 and international academic standards:

1. **简洁性 (Conciseness)**: Remove "关于...的研究", "...的探索", "新型", "改进的"
2. **可搜索性 (Searchability)**: Place key terms (方法+问题) in first 20 characters
3. **长度 (Length)**: Optimal 15-25 characters; acceptable 10-30 characters
4. **具体性 (Specificity)**: Use concrete method/problem names, avoid vague terms
5. **规范性 (Compliance)**: Follow thesis title standards, avoid obscure abbreviations

#### Quality Scoring

Each title receives a score (0-100) based on:
- 简洁性 (25%): No ineffective words
- 可搜索性 (30%): Key terms in first 20 characters
- 长度 (15%): Within optimal range
- 具体性 (20%): Concrete vs vague terms
- 规范性 (10%): No obscure abbreviations

#### Usage in Claude Code

**Check existing title**:
```
检查我的论文标题质量
```

**Generate title candidates**:
```
根据摘要生成论文标题候选方案
```

**Optimize existing title**:
```
优化我的学位论文标题，符合国标规范
```

The assistant will analyze your title and provide:
- Quality score with breakdown (质量评分及细分)
- Specific issues detected (检测到的问题)
- Multiple improved candidates with Chinese-English pairs (中英文对照的改进方案)
- Suggested LaTeX code (建议的 LaTeX 代码)

#### Title Generation Workflow

1. **内容分析 (Content Analysis)**: Extract problem, method, domain from abstract/introduction
2. **关键词提取 (Keyword Extraction)**: Identify 3-5 core keywords
3. **模板选择 (Template Selection)**: Choose appropriate pattern
4. **候选生成 (Candidate Generation)**: Create 3-5 variants
5. **质量评分 (Quality Scoring)**: Rank candidates by score

#### Common Title Patterns

| 模式 | 示例 | 适用场景 |
|------|------|----------|
| 问题的方法研究 | "时间序列预测的Transformer方法研究" | 方法创新型 |
| 领域问题的方法 | "工业系统故障检测的图神经网络方法" | 应用导向型 |
| 方法及应用 | "注意力机制及其在工业控制中的应用" | 理论+应用型 |
| 面向领域的方法 | "面向智能制造的深度学习预测性维护方法" | 领域专项型 |

#### Ineffective Words to Remove

| 避免使用 | 原因 |
|----------|------|
| 关于...的研究 | 冗余（所有论文都是研究） |
| ...的探索 | 冗余且不具体 |
| 新型 / 新颖的 | 发表即意味着新颖 |
| 改进的 / 优化的 | 不具体，需说明如何改进 |
| 基于...的 | 可简化为直接表述 |

#### Good vs Bad Examples

```
好：工业控制系统时间序列预测的Transformer方法
差：关于基于Transformer的工业控制系统时间序列预测的研究

好：图神经网络故障检测方法及其工业应用
差：新型改进的基于图神经网络的故障检测方法研究

好：注意力机制的多变量时间序列预测方法
差：基于注意力机制的改进型多变量时间序列预测模型研究
```

#### University-Specific Requirements

**清华大学 (Tsinghua University)**:
- 中文标题：不超过 36 个汉字
- 避免使用缩写和公式

**北京大学 (Peking University)**:
- 中文标题：简明扼要，一般不超过 25 字
- 可使用副标题（用破折号分隔）

**通用要求 (General Requirements)**:
- 遵循 GB/T 7713.1-2006 规范
- 中文标题：15-25 字为宜
- 英文标题：对应翻译，注意冠词和介词

#### Chinese-English Title Pairs

| 中文标题 | 英文标题 |
|----------|----------|
| 工业系统故障检测的图神经网络方法 | Graph Neural Networks for Fault Detection in Industrial Systems |
| 基于注意力机制的时间序列预测研究 | Attention-Based Time Series Forecasting |
| 深度学习在智能制造中的应用 | Deep Learning Applications in Smart Manufacturing |

#### Best Practices

1. **关键词前置**: 方法+问题放在前 20 字
2. **具体明确**: "Transformer" > "深度学习" > "机器学习"
3. **删除冗余**: 去掉"关于"、"研究"、"新型"、"基于"
4. **控制长度**: 目标 15-25 字（中文）
5. **测试可搜索性**: 用这些关键词能找到你的论文吗？
6. **避免生僻**: 除非是广泛认可的术语（AI、LSTM、CNN）
7. **符合规范**: 遵循学校模板和 GB/T 7713.1-2006 标准

#### References

- GB/T 7713.1-2006: 学位论文编写规则
- `references/GB_STANDARD.md`: 国标格式规范
- `references/UNIVERSITIES/`: 学校模板指南

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

## Recommended Workflows

### Full Thesis Review (Multi-file)
1. Structure mapping (first)
2. GB/T format check
3. Template detection + verify key requirements
4. De-AI polishing (intro + related work)
5. Academic expression cleanup
6. Long sentence analysis
7. Bibliography verification

### Pre-Defense Quick Pass
1. Compile with xelatex + biber
2. Bibliography verification
3. GB/T format check (strict)

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
