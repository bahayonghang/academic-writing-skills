# Venue-Specific Guidelines

Formatting guidelines for major academic venues in computer science.

## IEEE (Institute of Electrical and Electronics Engineers)

### Overview

IEEE is one of the largest publishers of technical literature in computer science and engineering.

### Title Format

**Style**: Title Case (Each Major Word Capitalized)

```latex
\title{A Novel Approach to Machine Learning Optimization}
```

### Section Headings

**Style**: Title Case

```latex
\section{Introduction and Background}
\section{Related Work}
\section{Proposed Method}
```

### Figure References

**In text**: "Fig."
```latex
See Fig.~\ref{fig:arch} for details.
As shown in Fig.~1...
```

**In captions**: "Fig." or "Figure"
```latex
\caption{Fig. 1: System architecture.}
% or
\caption{Figure 1: System architecture.}
```

### Table Captions

**Style**: "TABLE" in uppercase

```latex
\caption{TABLE I: Comparison of Methods}
```

### Citations

**Style**: Numerical [1], [2], [3]

```latex
Recent work~\cite{smith2024} has shown...
% Renders as: Recent work [1] has shown...
```

### Page Limits

| Venue | Limit | Notes |
|-------|-------|-------|
| IEEE Transactions | 12-14 pages | Varies by journal |
| IEEE Conference | 6-8 pages | Short papers: 4 pages |
| IEEE Letters | 4 pages | Brief communications |

### Template

```latex
\documentclass[conference]{IEEEtran}
\usepackage{cite}
\usepackage{graphicx}

\begin{document}
\title{Your Title Here}
\author{\IEEEauthorblockN{Author Name}
\IEEEauthorblockA{Affiliation}}
\maketitle

\begin{abstract}
Your abstract here.
\end{abstract}

\section{Introduction}
...

\bibliographystyle{IEEEtran}
\bibliography{references}
\end{document}
```

## ACM (Association for Computing Machinery)

### Overview

ACM publishes research across all areas of computing.

### Title Format

**Style**: Title Case

```latex
\title{A Novel Approach to Machine Learning Optimization}
```

### Section Headings

**Style**: Sentence case (Only first word capitalized)

```latex
\section{Introduction and background}
\section{Related work}
\section{Proposed method}
```

### Figure References

**Style**: "Figure" everywhere

```latex
See Figure~\ref{fig:arch} for details.
\caption{Figure 1: System architecture.}
```

### Table Captions

**Style**: "Table" (normal case)

```latex
\caption{Table 1: Comparison of methods}
```

### Citations

**Style**: Numerical [1] or author-year (varies by venue)

**Numerical**:
```latex
Recent work~\cite{smith2024} has shown...
% Renders as: Recent work [1] has shown...
```

**Author-year**:
```latex
Recent work~\cite{smith2024} has shown...
% Renders as: Recent work (Smith et al. 2024) has shown...
```

### Page Limits

| Venue | Limit | Notes |
|-------|-------|-------|
| ACM SIGCHI | 10 pages | Excluding references |
| ACM SIGMOD | 12 pages | Including references |
| ACM SIGGRAPH | 9 pages | Excluding references |

### Template

```latex
\documentclass[sigconf]{acmart}

\begin{document}
\title{Your Title Here}
\author{Author Name}
\affiliation{Affiliation}
\email{email@example.com}

\begin{abstract}
Your abstract here.
\end{abstract}

\maketitle

\section{Introduction and background}
...

\bibliographystyle{ACM-Reference-Format}
\bibliography{references}
\end{document}
```

## Springer

### Overview

Springer publishes conference proceedings (LNCS) and journals.

### Title Format

**Style**: Title Case or Sentence case (varies by venue)

```latex
% LNCS: Title Case
\title{A Novel Approach to Machine Learning Optimization}

% Some journals: Sentence case
\title{A novel approach to machine learning optimization}
```

### Section Headings

**Style**: Sentence case

```latex
\section{Introduction and background}
\section{Related work}
```

### Figure References

**Style**: "Fig." everywhere

```latex
See Fig.~\ref{fig:arch} for details.
\caption{Fig. 1: System architecture}
```

### Table Captions

**Style**: "Table" (normal case)

```latex
\caption{Table 1. Comparison of methods}
```

### Citations

**Style**: Numerical [1] or author-year (varies)

### Page Limits

| Venue | Limit | Notes |
|-------|-------|-------|
| LNCS | 12-15 pages | Including references |
| Springer Journals | Varies | Check specific journal |

### Template (LNCS)

```latex
\documentclass{llncs}
\usepackage{graphicx}

\begin{document}
\title{Your Title Here}
\author{Author Name}
\institute{Affiliation}

\maketitle

\begin{abstract}
Your abstract here.
\end{abstract}

\section{Introduction and background}
...

\bibliographystyle{splncs04}
\bibliography{references}
\end{document}
```

## NeurIPS (Neural Information Processing Systems)

### Overview

Premier conference for machine learning and AI research.

### Title Format

**Style**: Title Case

```latex
\title{A Novel Approach to Machine Learning Optimization}
```

### Section Headings

**Style**: Title Case

```latex
\section{Introduction and Background}
\section{Related Work}
```

### Figure/Table References

**Style**: "Figure" and "Table"

```latex
See Figure~\ref{fig:arch} for details.
\caption{Figure 1: System architecture.}
```

### Citations

**Style**: Author-year

```latex
Recent work~\cite{smith2024} has shown...
% Renders as: Recent work (Smith et al., 2024) has shown...
```

### Page Limits

- **Main paper**: 9 pages (excluding references)
- **Appendix**: Unlimited (but reviewers not required to read)

### Template

```latex
\documentclass{article}
\usepackage{neurips_2024}

\title{Your Title Here}
\author{Author Name \\ Affiliation}

\begin{document}
\maketitle

\begin{abstract}
Your abstract here.
\end{abstract}

\section{Introduction and Background}
...

\bibliographystyle{plainnat}
\bibliography{references}
\end{document}
```

## ICML (International Conference on Machine Learning)

### Overview

Top-tier machine learning conference.

### Format

Similar to NeurIPS:
- **Title**: Title Case
- **Sections**: Title Case
- **Citations**: Author-year
- **Page limit**: 8 pages (excluding references)

### Template

```latex
\documentclass{article}
\usepackage{icml2024}

\title{Your Title Here}
\author{Author Name \\ Affiliation}

\begin{document}
\maketitle

\begin{abstract}
Your abstract here.
\end{abstract}

\section{Introduction and Background}
...

\bibliographystyle{icml2024}
\bibliography{references}
\end{document}
```

## ICLR (International Conference on Learning Representations)

### Overview

Leading conference for deep learning research.

### Format

Similar to NeurIPS/ICML:
- **Title**: Title Case
- **Sections**: Title Case
- **Citations**: Author-year or numerical (varies by year)
- **Page limit**: Unlimited (but typically 8-10 pages)

## AAAI (Association for the Advancement of Artificial Intelligence)

### Overview

Major AI conference covering broad range of topics.

### Title Format

**Style**: Title Case

### Section Headings

**Style**: Title Case

### Citations

**Style**: Author-year

### Page Limits

- **Main paper**: 7 pages
- **References**: 1 page
- **Total**: 8 pages

### Template

```latex
\documentclass[letterpaper]{article}
\usepackage{aaai24}

\title{Your Title Here}
\author{Author Name \\ Affiliation}

\begin{document}
\maketitle

\begin{abstract}
Your abstract here.
\end{abstract}

\section{Introduction and Background}
...

\bibliographystyle{aaai24}
\bibliography{references}
\end{document}
```

## Quick Reference Table

| Venue | Title | Sections | Figures | Tables | Citations | Pages |
|-------|-------|----------|---------|--------|-----------|-------|
| IEEE | Title Case | Title Case | Fig. | TABLE | [1] | 6-14 |
| ACM | Title Case | Sentence | Figure | Table | [1] or (Author, Year) | 9-12 |
| Springer | Varies | Sentence | Fig. | Table | [1] or (Author, Year) | 12-15 |
| NeurIPS | Title Case | Title Case | Figure | Table | (Author, Year) | 9 |
| ICML | Title Case | Title Case | Figure | Table | (Author, Year) | 8 |
| ICLR | Title Case | Title Case | Figure | Table | Varies | ~8-10 |
| AAAI | Title Case | Title Case | Figure | Table | (Author, Year) | 7+1 |

## Checking Venue Requirements

### Before Submission

1. **Download latest template** from venue website
2. **Check formatting guidelines** (often updated yearly)
3. **Verify page limits** (including/excluding references)
4. **Check citation style** (numerical vs. author-year)
5. **Review anonymization requirements** (for double-blind review)

### Common Mistakes

- Using outdated template
- Exceeding page limits
- Wrong citation style
- Incorrect figure/table format
- Missing required sections (e.g., ethics statement)

## Resources

- **IEEE**: https://www.ieee.org/conferences/publishing/templates.html
- **ACM**: https://www.acm.org/publications/proceedings-template
- **Springer**: https://www.springer.com/gp/authors-editors/conference-proceedings
- **NeurIPS**: https://neurips.cc/Conferences/2024/PaperInformation/StyleFiles
- **ICML**: https://icml.cc/Conferences/2024/StyleAuthorInstructions
- **ICLR**: https://iclr.cc/Conferences/2024/AuthorGuide
- **AAAI**: https://aaai.org/conference/aaai/aaai-24/aaai24call/

## Next Steps

- [Common Errors](/references/common-errors) - Avoid common mistakes
- [Style Guide](/references/style-guide) - Academic writing style
- [Usage Guide](/usage) - Tool usage
