# Experiment Analysis

The Experiment Analysis module leverages LLM capabilities to generate cohesive, top-tier academic paragraphs from raw data or unstructured text.

## Features

- **Cohesive Narrative**: Wraps insights into paragraph structures starting with `\paragraph{}`.
- **Deep Analysis**: Focuses on SOTA comparison, ablation studies, and efficiency trade-offs rather than mere numerical reporting.
- **Objective Tone**: Ensures descriptions remain scientifically rigorous without exaggerated claims.
- **Formatting Constraints**: Strictly avoids `\textbf{}` or `\begin{itemize}` as per IEEE and ACM guidelines.

## Usage

Provide the raw data or draft to the analyzer script:

```bash
python scripts/analyze_experiment.py "Model A achieved 94.2% while Model B achieved 91%. Model A is faster."
```

## System Constraints (For LLM)

When triggered, the assistant follows these rules:
1. Cannot fabricate data or invent non-existent trends.
2. Must use `\paragraph{Title Case Heading}` for the topic sentence.
3. Must use active, concise phrasing and present tense for conclusions.
4. Outputs raw LaTeX block for drop-in replacement.
