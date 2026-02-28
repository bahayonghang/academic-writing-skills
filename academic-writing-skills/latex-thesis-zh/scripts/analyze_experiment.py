#!/usr/bin/env python3
"""
Experiment analysis helper for Chinese LaTeX thesis and journals.
This script formats the raw experiment data into a structured prompt
for the LLM to generate standard, highly formal academic paragraphs.
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
        "### 中文实验分析生成请求 (Experiment Analysis Request)",
        "请根据以下原始数据或草稿，生成符合中文顶刊与学位论文标准的完美实验分析段落。",
        "务必严格遵守 `references/modules/EXPERIMENT.md` 中的所有约束条件。",
        "",
        "#### 规范要点提醒:",
        "- 强制使用 `\\paragraph{核心结论概括}` 引导段落。",
        "- 正文中**禁止**任何 `\\textbf{}` 等显式加粗。",
        "- **禁止**使用列表环境 (`\\begin{itemize}`) 罗列数据，需串联成连贯的论述段落。",
        "- 包含 SOTA 对比、消融结论，并确保具有深度的比较逻辑而不仅是报数字。",
        "- 极致客观、去口语化，严禁出现“碾压、遥遥领先”等夸张词汇及主观代词。",
        "",
        "#### 原始数据 / 打点草稿:",
        content,
        "",
        "#### 输出格式:",
        "% EXPERIMENT ANALYSIS DRAFT",
        "% [Insert LaTeX paragraph here]",
    ]
    return "\n".join(prompt)


def main() -> int:
    cli = argparse.ArgumentParser(
        description="Generate experiment analysis prompt from raw data (Chinese)"
    )
    cli.add_argument("input", help="Raw experiment data or file path")
    args = cli.parse_args()

    print(generate_request(args.input))
    return 0


if __name__ == "__main__":
    sys.exit(main())
