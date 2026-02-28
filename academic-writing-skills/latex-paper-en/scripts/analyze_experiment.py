#!/usr/bin/env python3
"""
Experiment analysis helper for LaTeX papers.
This script formats the raw experiment data into a structured prompt
for the LLM to generate standard IEEE/ACM compliant paragraphs.
"""

import argparse
import sys
from pathlib import Path


def generate_request(input_data: str) -> str:
    path = Path(input_data)
    if path.exists() and path.is_file():
        content = path.read_text(encoding="utf-8", errors="ignore")
    else:
        content = input_data

    prompt = [
        "### Experiment Analysis Request",
        "Please generate a top-tier academic experiment analysis paragraph based on the following data.",
        "Ensure you follow the constraints in `references/modules/EXPERIMENT.md`.",
        "",
        "#### Requirements Reminder:",
        "- Use `\\paragraph{Title Case Heading}` as the paragraph starter.",
        "- NO `\\textbf{}` or `\\emph{}` in the body text.",
        "- NO list formats (`\\begin{itemize}`). Use a cohesive narrative.",
        "- Include SOTA comparison, ablation insights, and statistical significance if applicable.",
        "- Objective tone, no exaggerated claims.",
        "",
        "#### Raw Data / Draft:",
        content,
        "",
        "#### Output Format:",
        "% EXPERIMENT ANALYSIS DRAFT",
        "% [Insert LaTeX paragraph here]",
    ]
    return "\n".join(prompt)


def main() -> int:
    cli = argparse.ArgumentParser(description="Generate experiment analysis prompt from raw data")
    cli.add_argument("input", help="Raw experiment data or file path")
    args = cli.parse_args()

    print(generate_request(args.input))
    return 0


if __name__ == "__main__":
    sys.exit(main())
