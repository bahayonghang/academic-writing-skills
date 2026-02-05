---
name: latex-paper-en
version: 1.1.0
category: academic-writing
tags:
  - latex
  - paper
  - english
  - ieee
  - acm
  - springer
  - neurips
  - icml
  - deep-learning
  - compilation
  - grammar
  - bibliography
description: |
  LaTeX academic paper assistant for English papers (IEEE, ACM, Springer, NeurIPS, ICML).
  Domains: Deep Learning, Time Series, Industrial Control.

  Triggers (use ANY module independently):
  - "compile", "编译", "build latex" → Compilation Module
  - "format check", "chktex", "格式检查" → Format Check Module
  - "grammar", "语法", "proofread", "润色" → Grammar Analysis Module
  - "long sentence", "长句", "simplify" → Long Sentence Analysis Module
  - "academic tone", "学术表达", "improve writing" → Expression Module
  - "logic", "coherence", "methodology", "argument structure", "论证" → Logical Coherence & Methodological Depth Module
  - "translate", "翻译", "中译英", "Chinese to English" → Translation Module
  - "bib", "bibliography", "参考文献" → Bibliography Module
  - "deai", "去AI化", "humanize", "reduce AI traces" → De-AI Editing Module
  - "title", "标题", "title optimization", "create title" → Title Optimization Module
argument-hint: "[main.tex] [--section <section>] [--module <module>]"
allowed-tools: Read, Glob, Grep, Bash(python *), Bash(pdflatex *), Bash(xelatex *), Bash(latexmk *), Bash(bibtex *), Bash(biber *), Bash(chktex *)
---

# LaTeX Academic Paper Assistant (English)

## Critical Rules

1. NEVER modify `\cite{}`, `\ref{}`, `\label{}`, math environments
2. NEVER fabricate bibliography entries
3. NEVER change domain terminology without confirmation
4. ALWAYS output suggestions in diff-comment format first

## Argument Conventions ($ARGUMENTS)

- Use `$ARGUMENTS` to capture user-provided inputs (main `.tex` path, target section, module choice).
- If `$ARGUMENTS` is missing or ambiguous, ask for: main `.tex` path, target scope, and desired module.
- Treat file paths as literal; do not guess missing paths.

## Execution Guardrails

- Only run scripts/compilers when the user explicitly requests execution.
- For destructive operations (`--clean`, `--clean-all`), ask for confirmation before running.

## Unified Output Protocol (All Modules)

Each suggestion MUST include fixed fields:
- **Severity**: Critical / Major / Minor
- **Priority**: P0 (blocking) / P1 (important) / P2 (nice-to-have)

**Default comment template** (diff-comment style):
```latex
% <MODULE> (Line <N>) [Severity: <Critical|Major|Minor>] [Priority: <P0|P1|P2>]: <Issue summary>
% Original: ...
% Revised:  ...
% Rationale: ...
% ⚠️ [PENDING VERIFICATION]: <if evidence/metric is required>
```

## Failure Handling (Global)

If a tool/script cannot run, respond with a comment block including the reason and a safe next step:
```latex
% ERROR [Severity: Critical] [Priority: P0]: <short error>
% Cause: <missing file/tool or invalid path>
% Action: <install tool / verify file path / re-run command>
```
Common cases:
- **Script not found**: confirm `scripts/` path and working directory
- **LaTeX tool missing**: suggest installing TeX Live/MiKTeX or adding to PATH
- **File not found**: ask user to provide the correct `.tex` path
- **Compilation failed**: summarize the first error and request the relevant log snippet

## Modules (Independent, Pick Any)

### Module: Compile
**Trigger**: compile, 编译, build, pdflatex, xelatex

**Default Behavior**: Uses `latexmk` which automatically handles all dependencies (bibtex/biber, cross-references, indexes) and determines the optimal number of compilation passes. This is the recommended approach for most use cases.

**Tools** (matching VS Code LaTeX Workshop):
| Tool | Command | Args |
|------|---------|------|
| xelatex | `xelatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| pdflatex | `pdflatex` | `-synctex=1 -interaction=nonstopmode -file-line-error` |
| latexmk | `latexmk` | `-synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir=%OUTDIR%` |
| bibtex | `bibtex` | `%DOCFILE%` |
| biber | `biber` | `%DOCFILE%` |

**Recipes**:
| Recipe | Steps | Use Case |
|--------|-------|----------|
| latexmk | latexmk (auto) | **DEFAULT** - Auto-handles all dependencies |
| PDFLaTeX | pdflatex | Quick single-pass build |
| XeLaTeX | xelatex | Quick single-pass build |
| pdflatex -> bibtex -> pdflatex*2 | pdflatex → bibtex → pdflatex → pdflatex | Traditional BibTeX workflow |
| pdflatex -> biber -> pdflatex*2 | pdflatex → biber → pdflatex → pdflatex | Modern biblatex (recommended for new projects) |
| xelatex -> bibtex -> xelatex*2 | xelatex → bibtex → xelatex → xelatex | Chinese/Unicode + BibTeX |
| xelatex -> biber -> xelatex*2 | xelatex → biber → xelatex → xelatex | Chinese/Unicode + biblatex |

**Usage**:
```bash
# Default: latexmk auto-handles all dependencies (recommended)
python scripts/compile.py main.tex                          # Auto-detect compiler + latexmk

# Single-pass compilation (quick builds)
python scripts/compile.py main.tex --recipe pdflatex        # PDFLaTeX only
python scripts/compile.py main.tex --recipe xelatex         # XeLaTeX only

# Explicit bibliography workflows (when you need control)
python scripts/compile.py main.tex --recipe pdflatex-bibtex # Traditional BibTeX
python scripts/compile.py main.tex --recipe pdflatex-biber  # Modern biblatex (recommended)
python scripts/compile.py main.tex --recipe xelatex-bibtex  # XeLaTeX + BibTeX
python scripts/compile.py main.tex --recipe xelatex-biber   # XeLaTeX + biblatex

# With output directory
python scripts/compile.py main.tex --outdir build

# Utilities
python scripts/compile.py main.tex --watch                  # Watch mode
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

**Usage**: User provides paragraph source code, agent analyzes and returns polished version with comparison table.

**Output format** (Markdown comparison table):
```markdown
| Original | Revised | Issue Type | Rationale |
|----------|---------|------------|-----------|
| We propose method for time series forecasting. | We propose a method for time series forecasting. | Grammar: Article missing | Singular count noun requires indefinite article "a" |
| The data shows significant improvement. | The data show significant improvement. | Grammar: Subject-verb agreement | "Data" is plural, requires "show" not "shows" |
| This approach get better results. | This approach achieves superior performance. | Grammar + Expression | Verb agreement error; replace weak verb "get" with academic alternative |
```

**Alternative format** (for inline comments in source):
```latex
% GRAMMAR (Line 23) [Severity: Major] [Priority: P1]: Article missing
% Original: We propose method for...
% Revised: We propose a method for...
% Rationale: Missing indefinite article before singular count noun
```

---

### Module: Long Sentence Analysis
**Trigger**: long sentence, 长句, simplify, decompose, >50 words

Trigger condition: Sentences >50 words OR >3 subordinate clauses

Output format:
```latex
% LONG SENTENCE (Line 45, 67 words) [Severity: Minor] [Priority: P2]
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
% EXPRESSION (Line 23) [Severity: Minor] [Priority: P2]: Improve academic tone
% Original: We use machine learning to get better results.
% Revised: We employ machine learning to achieve superior performance.
% Rationale: Replace weak verbs with academic alternatives
```

Style guide: [STYLE_GUIDE.md](references/STYLE_GUIDE.md)

---

### Module: Logical Coherence & Methodological Depth
**Trigger**: logic, coherence, 逻辑, methodology, argument structure, 论证

**Purpose**: Ensure logical flow between paragraphs and strengthen methodological rigor in academic writing.

**Focus Areas**:

**1. Paragraph-Level Coherence (AXES Model)**:
| Component | Description | Example |
|-----------|-------------|---------|
| **A**ssertion | Clear topic sentence stating the main claim | "Attention mechanisms improve sequence modeling." |
| **X**ample | Concrete evidence or data supporting the claim | "In our experiments, attention achieved 95% accuracy." |
| **E**xplanation | Analysis of why the evidence supports the claim | "This improvement stems from the ability to capture long-range dependencies." |
| **S**ignificance | Connection to broader argument or next paragraph | "This finding motivates our proposed architecture." |

**2. Transition Signals**:
| Relationship | Signals |
|--------------|---------|
| Addition | furthermore, moreover, in addition, additionally |
| Contrast | however, nevertheless, in contrast, conversely |
| Cause-Effect | therefore, consequently, as a result, thus |
| Sequence | first, subsequently, finally, meanwhile |
| Example | for instance, specifically, in particular |

**3. Methodological Depth Checklist**:
- [ ] Each claim is supported by evidence (data, citation, or logical reasoning)
- [ ] Method choices are justified (why this approach over alternatives?)
- [ ] Limitations are acknowledged explicitly
- [ ] Assumptions are stated clearly
- [ ] Reproducibility details are sufficient (parameters, datasets, metrics)

**4. Common Issues**:
| Issue | Problem | Fix |
|-------|---------|-----|
| Logical gap | Missing connection between paragraphs | Add transition sentence explaining the relationship |
| Unsupported claim | Assertion without evidence | Add citation, data, or reasoning |
| Shallow methodology | "We use X" without justification | Explain why X is appropriate for this problem |
| Hidden assumptions | Implicit prerequisites | State assumptions explicitly |

**Output Format**:
```latex
% LOGIC (Line 45) [Severity: Major] [Priority: P1]: Logical gap between paragraphs
% Issue: Paragraph jumps from problem description to solution without transition
% Current: "The data is noisy. We propose a filtering method."
% Suggested: "The data is noisy, which motivates the need for preprocessing. Therefore, we propose a filtering method."
% Rationale: Add causal transition to connect problem and solution

% METHODOLOGY (Line 78) [Severity: Major] [Priority: P1]: Unsupported method choice
% Issue: Method selection lacks justification
% Current: "We use ResNet as the backbone."
% Suggested: "We use ResNet as the backbone due to its proven effectiveness in feature extraction and skip connections that mitigate gradient vanishing."
% Rationale: Justify architectural choice with technical reasoning
```

**Section-Specific Guidelines**:
| Section | Coherence Focus | Methodology Focus |
|---------|-----------------|-------------------|
| Introduction | Problem → Gap → Contribution flow | Justify research significance |
| Related Work | Group by theme, compare explicitly | Position against prior work |
| Methods | Step-by-step logical progression | Justify every design choice |
| Experiments | Setup → Results → Analysis flow | Explain evaluation metrics |
| Discussion | Findings → Implications → Limitations | Acknowledge boundaries |

**Best Practices** (Based on [Elsevier](https://elsevier.blog/logical-academic-writing/), [Proof-Reading-Service](https://www.proof-reading-service.com/blogs/academic-publishing/a-guide-to-creating-clear-and-well-structured-scholarly-arguments)):
1. **One idea per paragraph**: Each paragraph should have a single, clear focus
2. **Topic sentences first**: Start each paragraph with its main claim
3. **Evidence chain**: Every claim needs support (data, citation, or logic)
4. **Explicit transitions**: Use signal words to show relationships
5. **Justify, don't just describe**: Explain *why*, not just *what*

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
If a term is ambiguous or domain-specific, pause and ask for confirmation before translating.

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

### Module: De-AI Editing (去AI化编辑)
**Trigger**: deai, 去AI化, humanize, reduce AI traces, natural writing

**Purpose**: Reduce AI writing traces while preserving LaTeX syntax and technical accuracy.

**Input Requirements**:
1. **Source code type** (required): LaTeX
2. **Section** (required): Abstract / Introduction / Related Work / Methods / Experiments / Results / Discussion / Conclusion / Other
3. **Source code snippet** (required): Direct paste (preserve indentation and line breaks)

**Usage Examples**:

**Interactive editing** (recommended for sections):
```python
python scripts/deai_check.py main.tex --section introduction
# Output: Interactive questions + AI trace analysis + Rewritten code
```

**Batch processing** (for entire chapters):
```bash
python scripts/deai_batch.py main.tex --chapter chapter3/introduction.tex
python scripts/deai_batch.py main.tex --all-sections  # Process entire document
```

**Workflow**:
1. **Syntax Structure Identification**: Detect LaTeX commands, preserve all:
   - Commands: `\command{...}`, `\command[...]{}`
   - References: `\cite{}`, `\ref{}`, `\label{}`, `\eqref{}`, `\autoref{}`
   - Environments: `\begin{...}...\end{...}`
   - Math: `$...$`, `\[...\]`, equation/align environments
   - Custom macros (unchanged by default)

2. **AI Pattern Detection**:
   - Empty phrases: "significant", "comprehensive", "effective", "important"
   - Over-confident: "obviously", "necessarily", "completely", "clearly"
   - Mechanical structures: Three-part parallelisms without substance
   - Template expressions: "in recent years", "more and more"

3. **Text Rewriting** (visible text ONLY):
   - Split long sentences (>50 words)
   - Adjust word order for natural flow
   - Replace vague expressions with specific claims
   - Delete redundant phrases
   - Add necessary subjects (without introducing new facts)

4. **Output Generation**:
   - **A. Rewritten source code**: Complete source with minimal invasive edits
   - **B. Change summary**: 3-10 bullet points explaining modifications
   - **C. Pending verification marks**: For claims needing evidence

**Hard Constraints**:
- **NEVER modify**: `\cite{}`, `\ref{}`, `\label{}`, math environments
- **NEVER add**: New data, metrics, comparisons, contributions, experimental settings, citation numbers, or bib keys
- **ONLY modify**: Visible paragraph text, section titles, caption text

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
% 2. Kept the claim but avoided adding new metrics or baselines
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

**AI Trace Density Check**:
```bash
python scripts/deai_check.py main.tex --analyze
# Output: AI trace density score per section + Target sections for improvement
```

Reference: [DEAI_GUIDE.md](references/DEAI_GUIDE.md)

---

### Module: Title Optimization
**Trigger**: title, 标题, title optimization, create title, improve title

**Purpose**: Generate and optimize paper titles following IEEE/ACM/Springer/NeurIPS best practices.

**Usage Examples**:

**Generate title from content**:
```bash
python scripts/optimize_title.py main.tex --generate
# Analyzes abstract/introduction to propose 3-5 title candidates
```

**Optimize existing title**:
```bash
python scripts/optimize_title.py main.tex --optimize
# Analyzes current title and provides improvement suggestions
```

**Check title quality**:
```bash
python scripts/optimize_title.py main.tex --check
# Evaluates title against best practices (score 0-100)
```

**Title Quality Criteria** (Based on IEEE Author Center & Top Venues):

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Conciseness** | 25% | Remove "A Study of", "Research on", "Novel", "New", "Improved" |
| **Searchability** | 30% | Key terms (Method + Problem) in first 65 characters |
| **Length** | 15% | Optimal: 10-15 words; Acceptable: 8-20 words |
| **Specificity** | 20% | Concrete method/problem names, not vague terms |
| **Jargon-Free** | 10% | Avoid obscure abbreviations (except AI, LSTM, DNA, etc.) |

**Title Generation Workflow**:

**Step 1: Content Analysis**
Extract from abstract/introduction:
- **Problem**: What challenge is addressed?
- **Method**: What approach is proposed?
- **Domain**: What application area?
- **Key Result**: What is the main achievement? (optional)

**Step 2: Keyword Extraction**
Identify 3-5 core keywords:
- Method keywords: "Transformer", "Graph Neural Network", "Reinforcement Learning"
- Problem keywords: "Time Series Forecasting", "Fault Detection", "Image Segmentation"
- Domain keywords: "Industrial Control", "Medical Imaging", "Autonomous Driving"

**Step 3: Title Template Selection**
Common patterns for top venues:

| Pattern | Example | Use Case |
|---------|---------|----------|
| Method for Problem | "Transformer-Based Approach for Time Series Forecasting" | General research |
| Method: Problem in Domain | "Graph Neural Networks: Fault Detection in Industrial Systems" | Domain-specific |
| Problem via Method | "Time Series Forecasting via Attention Mechanisms" | Method-focused |
| Method + Key Feature | "Lightweight Transformer for Real-Time Object Detection" | Performance-focused |

**Step 4: Title Candidates Generation**
Generate 3-5 candidates with different emphasis:
1. Method-focused
2. Problem-focused
3. Application-focused
4. Balanced (recommended)
5. Concise variant

**Step 5: Quality Scoring**
Each candidate receives:
- Overall score (0-100)
- Breakdown by criterion
- Specific improvement suggestions

**Title Optimization Rules**:

**❌ Remove Ineffective Words**:
| Avoid | Reason |
|-------|--------|
| A Study of | Redundant (all papers are studies) |
| Research on | Redundant (all papers are research) |
| Novel / New | Implied by publication |
| Improved / Enhanced | Vague without specifics |
| Based on | Often unnecessary |
| Using / Utilizing | Can be replaced with prepositions |

**✅ Preferred Structures**:
```
Good: "Transformer for Time Series Forecasting in Industrial Control"
Bad:  "A Novel Study on Improved Time Series Forecasting Using Transformers"

Good: "Graph Neural Networks for Fault Detection"
Bad:  "Research on Novel Fault Detection Based on GNNs"

Good: "Attention-Based LSTM for Multivariate Time Series Prediction"
Bad:  "An Improved LSTM Model Using Attention Mechanism for Prediction"
```

**Keyword Placement Strategy**:
- **First 65 characters**: Most important keywords (Method + Problem)
- **Avoid starting with**: Articles (A, An, The), prepositions (On, In, For)
- **Prioritize**: Nouns and technical terms over verbs and adjectives

**Abbreviation Guidelines**:
| ✅ Acceptable | ❌ Avoid in Title |
|--------------|------------------|
| AI, ML, DL | Obscure domain-specific acronyms |
| LSTM, GRU, CNN | Chemical formulas (unless very common) |
| IoT, 5G, GPS | Lab-specific abbreviations |
| DNA, RNA, MRI | Non-standard method names |

**Venue-Specific Adjustments**:

**IEEE Transactions**:
- Avoid formulas with subscripts (except simple ones like "Nd–Fe–B")
- Use title case (capitalize major words)
- Typical length: 10-15 words
- Example: "Deep Learning for Predictive Maintenance in Smart Manufacturing"

**ACM Conferences**:
- More flexible with creative titles
- Can use colons for subtitles
- Typical length: 8-12 words
- Example: "AttentionFlow: Visualizing Attention Mechanisms in Neural Networks"

**Springer Journals**:
- Prefer descriptive over creative
- Can be slightly longer (up to 20 words)
- Example: "A Comprehensive Framework for Real-Time Anomaly Detection in Industrial IoT Systems"

**NeurIPS/ICML**:
- Concise and impactful (8-12 words)
- Method name often prominent
- Example: "Transformers Learn In-Context by Gradient Descent"

**Output Format**:

```latex
% ============================================================
% TITLE OPTIMIZATION REPORT
% ============================================================
% Current Title: "A Novel Study on Time Series Forecasting Using Deep Learning"
% Quality Score: 45/100
%
% Issues Detected:
% 1. [Critical] Contains "Novel Study" (remove ineffective words)
% 2. [Major] Vague method description ("Deep Learning" too broad)
% 3. [Minor] Length acceptable (9 words) but could be more specific
%
% Recommended Titles (Ranked):
%
% 1. "Transformer-Based Time Series Forecasting for Industrial Control" [Score: 92/100]
%    - Concise: ✅ (8 words)
%    - Searchable: ✅ (Method + Problem in first 50 chars)
%    - Specific: ✅ (Transformer, not just "Deep Learning")
%    - Domain: ✅ (Industrial Control)
%
% 2. "Attention Mechanisms for Multivariate Time Series Prediction" [Score: 88/100]
%    - Concise: ✅ (7 words)
%    - Searchable: ✅ (Key terms upfront)
%    - Specific: ✅ (Attention, Multivariate)
%    - Note: Consider adding domain if space allows
%
% 3. "Deep Learning Approach to Time Series Forecasting in Smart Manufacturing" [Score: 78/100]
%    - Concise: ⚠️ (10 words, acceptable)
%    - Searchable: ✅
%    - Specific: ⚠️ ("Deep Learning" still broad)
%    - Domain: ✅ (Smart Manufacturing)
%
% Keyword Analysis:
% - Primary: Transformer, Time Series, Forecasting
% - Secondary: Industrial Control, Attention, LSTM
% - Searchability: "Transformer Time Series" appears in 1,234 papers (good balance)
%
% Suggested LaTeX Update:
% \title{Transformer-Based Time Series Forecasting for Industrial Control}
% ============================================================
```

**Interactive Mode** (Recommended):
```bash
python scripts/optimize_title.py main.tex --interactive
# Step-by-step guided title creation with user input
```

**Batch Mode** (For multiple papers):
```bash
python scripts/optimize_title.py papers/*.tex --batch --output title_report.txt
```

**Title A/B Testing** (Optional):
```bash
python scripts/optimize_title.py main.tex --compare "Title A" "Title B" "Title C"
# Compares multiple title candidates with detailed scoring
```

**Best Practices Summary**:
1. **Start with keywords**: Put Method + Problem in first 10 words
2. **Be specific**: "Transformer" > "Deep Learning" > "Machine Learning"
3. **Remove fluff**: Delete "Novel", "Study", "Research", "Based on"
4. **Check length**: Aim for 10-15 words (English)
5. **Test searchability**: Would you find this paper with these keywords?
6. **Avoid jargon**: Unless it's widely recognized (AI, LSTM, CNN)
7. **Match venue style**: IEEE (descriptive), ACM (creative), NeurIPS (concise)

Reference: [IEEE Author Center](https://conferences.ieeeauthorcenter.ieee.org/), [Royal Society Blog](https://royalsociety.org/blog/2025/01/title-abstract-and-keywords-a-practical-guide-to-maximizing-the-visibility-and-impact-of-your-papers/)

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
3. De-AI Editing → reduce AI writing traces
4. Long Sentence Analysis → simplify complex sentences
5. Expression Restructuring → improve academic tone

---

## Best Practices

This skill follows Claude Code Skills best practices:

### Skill Design Principles
1. **Focused Responsibility**: Each module handles one specific task (KISS principle)
2. **Minimal Permissions**: Only request necessary tool access
3. **Clear Triggers**: Use specific keywords to invoke modules
4. **Structured Output**: All suggestions use consistent diff-comment format

### Usage Guidelines
1. **Start with Format Check**: Always verify document compiles before other checks
2. **Iterative Refinement**: Apply one module at a time for better control
3. **Preserve Protected Elements**: Never modify `\cite{}`, `\ref{}`, `\label{}`, math environments
4. **Verify Before Commit**: Review all suggestions before accepting changes

### Integration with Other Tools
- Use with version control (git) to track changes
- Combine with LaTeX Workshop for real-time preview
- Export suggestions to review with collaborators

---

## References

- [STYLE_GUIDE.md](references/STYLE_GUIDE.md): Academic writing rules
- [COMMON_ERRORS.md](references/COMMON_ERRORS.md): Chinglish patterns
- [VENUES.md](references/VENUES.md): Conference/journal requirements
- [FORBIDDEN_TERMS.md](references/FORBIDDEN_TERMS.md): Protected terminology
- [TERMINOLOGY.md](references/TERMINOLOGY.md): Domain terminology (DL/TS/IC)
- [TRANSLATION_GUIDE.md](references/TRANSLATION_GUIDE.md): Translation guide
- [DEAI_GUIDE.md](references/DEAI_GUIDE.md): De-AI writing guide and patterns
