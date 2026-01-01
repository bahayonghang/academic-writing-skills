# Academic Writing Style Guide

Comprehensive style guide for academic writing in computer science and related fields.

## General Principles

### Clarity

**Priority**: Clear communication over elegant prose

```latex
% Clear
The model achieves 95% accuracy on the test set.

% Unclear
The model's performance metrics indicate a high degree of correctness.
```

### Conciseness

**Remove unnecessary words**:

```latex
% Wordy
In order to improve the performance of the system...
Due to the fact that the model is complex...

% Concise
To improve system performance...
Because the model is complex...
```

### Precision

**Use specific terms**:

```latex
% Vague
The model works well.

% Precise
The model achieves 95% accuracy with 0.92 F1 score.
```

## Paper Structure

### Abstract

**Length**: 150-250 words

**Structure**:
1. **Context** (1-2 sentences): What is the problem?
2. **Gap** (1 sentence): What is missing?
3. **Contribution** (2-3 sentences): What did you do?
4. **Results** (1-2 sentences): What did you find?

**Example**:
```
Machine learning models require large labeled datasets, which are
expensive to obtain. Existing semi-supervised methods struggle with
limited labeled data. We propose a novel self-training approach that
leverages unlabeled data more effectively. Our method achieves 92%
accuracy with only 10% labeled data, outperforming baselines by 15%.
```

### Introduction

**Structure**:
1. **Motivation** (1-2 paragraphs): Why is this important?
2. **Problem** (1 paragraph): What is the specific problem?
3. **Existing work** (1 paragraph): What have others done?
4. **Gap** (1 paragraph): What is missing?
5. **Contribution** (1 paragraph): What do you contribute?
6. **Organization** (1 paragraph, optional): Paper structure

**Length**: 2-4 pages

### Related Work

**Organization**:
- Group by theme, not chronologically
- Compare and contrast approaches
- Identify gaps your work addresses

**Example structure**:
```latex
\section{Related Work}

\subsection{Supervised Learning Approaches}
Early work focused on...

\subsection{Semi-Supervised Methods}
Recent approaches have explored...

\subsection{Self-Training Techniques}
Our work builds on...
```

### Methodology

**Clarity requirements**:
- Reproducible: Others can implement your method
- Complete: All details provided
- Justified: Explain design choices

**Structure**:
1. **Overview**: High-level description
2. **Details**: Step-by-step explanation
3. **Justification**: Why these choices?

### Experiments

**Required elements**:
- **Setup**: Datasets, baselines, metrics
- **Implementation**: Hyperparameters, hardware
- **Results**: Tables, figures with analysis
- **Ablation**: Component contributions
- **Discussion**: Insights and limitations

### Conclusion

**Structure**:
1. **Summary** (1 paragraph): What did you do?
2. **Key findings** (1 paragraph): What did you learn?
3. **Limitations** (1 paragraph, optional): What are the constraints?
4. **Future work** (1 paragraph): What's next?

**Length**: 0.5-1 page

## Writing Style

### Active vs. Passive Voice

**Prefer active voice**:

```latex
% Passive (weak)
The experiments were conducted by us.
The model was trained on ImageNet.

% Active (strong)
We conducted the experiments.
We trained the model on ImageNet.
```

**Passive acceptable for**:
- Methods section (focus on method, not author)
- When actor is unknown or unimportant

### First Person

**Modern academic writing**: Use "we"

```latex
% Acceptable
We propose a novel method...
We conduct experiments on...
Our approach achieves...
```

**Avoid**:
- "I" in multi-author papers
- "The authors" (awkward)

### Tense Usage

**Present tense**:
- General truths
- Describing figures/tables
- Stating contributions

```latex
Machine learning is a branch of AI.
Figure 1 shows the architecture.
We propose a novel approach.
```

**Past tense**:
- Describing your experiments
- Reporting results

```latex
We trained the model for 100 epochs.
The experiments showed that...
```

**Present perfect**:
- Recent work with present relevance

```latex
Recent studies have shown that...
Researchers have proposed various methods...
```

## Common Patterns

### Introducing Contributions

```latex
% Good patterns
We propose a novel method for...
This paper presents a new approach to...
We introduce a framework that...
Our main contribution is...
```

### Describing Results

```latex
% Good patterns
The results show that...
Our method achieves...
Table 1 demonstrates that...
As shown in Figure 2...
```

### Comparing Methods

```latex
% Good patterns
Compared to baseline methods...
Our approach outperforms...
Unlike previous work...
In contrast to X, our method...
```

### Stating Limitations

```latex
% Good patterns
One limitation of our approach is...
Our method assumes that...
Future work should address...
```

## Figures and Tables

### Figure Captions

**Structure**: Brief description + key insight

```latex
\caption{Model architecture. The encoder processes input features,
while the decoder generates predictions. Attention mechanisms (shown
in blue) improve performance by 15\%.}
```

### Table Captions

**Structure**: Brief description + column explanation

```latex
\caption{Comparison of methods on three datasets. Bold indicates
best performance. Our method achieves highest accuracy on all datasets.}
```

### Referring to Figures/Tables

```latex
% Correct
Figure~\ref{fig:arch} shows...
As shown in Table~\ref{tab:results}...
See Fig.~\ref{fig:example} for details.
```

**Note**: Use `~` (non-breaking space) before `\ref`

## Mathematical Notation

### Inline vs. Display

**Inline** (within text):
```latex
The loss function $L = \sum_{i=1}^n (y_i - \hat{y}_i)^2$ measures error.
```

**Display** (separate line):
```latex
The loss function is defined as:
\begin{equation}
L = \sum_{i=1}^n (y_i - \hat{y}_i)^2
\end{equation}
```

### Notation Consistency

**Define once, use consistently**:

```latex
% In introduction or methodology
Let $x \in \mathbb{R}^d$ denote the input vector...

% Use same notation throughout
The model processes $x$ to produce output $y$...
```

### Common Symbols

| Symbol | Meaning | LaTeX |
|--------|---------|-------|
| $\mathbb{R}$ | Real numbers | `\mathbb{R}` |
| $\in$ | Element of | `\in` |
| $\subset$ | Subset | `\subset` |
| $\times$ | Cartesian product | `\times` |
| $\approx$ | Approximately | `\approx` |
| $\propto$ | Proportional to | `\propto` |

## Citations

### Citation Placement

**End of sentence**:
```latex
Machine learning has many applications~\cite{smith2024}.
```

**Mid-sentence**:
```latex
Smith et al.~\cite{smith2024} proposed a novel method.
```

**Multiple citations**:
```latex
Several studies~\cite{smith2024,jones2023,wang2022} have shown...
```

### Citation Style

**Numerical** (IEEE, most CS venues):
```latex
Recent work [1, 2, 3] has explored...
```

**Author-year** (some venues):
```latex
Recent work (Smith et al., 2024) has explored...
```

## Common Phrases

### Introducing Topics

- "In recent years..."
- "With the advent of..."
- "The field of X has seen..."

### Describing Methods

- "We propose a novel approach..."
- "Our method consists of..."
- "The key idea is to..."

### Presenting Results

- "The results demonstrate that..."
- "As shown in Table X..."
- "Our method achieves..."

### Discussing Limitations

- "One limitation is..."
- "Future work should address..."
- "Our approach assumes..."

## Checklist

### Before Submission

- [ ] Abstract clearly states contribution
- [ ] Introduction motivates problem
- [ ] Related work comprehensive
- [ ] Method reproducible
- [ ] Experiments thorough
- [ ] Figures/tables clear
- [ ] Citations complete
- [ ] Grammar checked
- [ ] Formatting correct

## Resources

- **Academic Phrasebank**: Common academic phrases
- **Purdue OWL**: Writing resources
- **Strunk & White**: The Elements of Style
- **Chicago Manual of Style**: Comprehensive guide

## Next Steps

- [Common Errors](/references/common-errors) - Avoid common mistakes
- [Venues](/references/venues) - Venue-specific guidelines
- [Usage Guide](/usage) - Tool usage
