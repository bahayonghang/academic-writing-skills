# Module: De-AI Editing (去AI化编辑)

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
# Output: AI trace analysis + rule-based revision suggestions
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

Reference: [DEAI_GUIDE.md](../references/DEAI_GUIDE.md)
