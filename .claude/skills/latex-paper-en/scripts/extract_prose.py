#!/usr/bin/env python3
"""
LaTeX Prose Extractor - Extract plain text from LaTeX for analysis

Usage:
    python extract_prose.py main.tex
    python extract_prose.py main.tex --output prose.txt
    python extract_prose.py main.tex --keep-structure
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional


class ProseExtractor:
    """Extract readable prose from LaTeX, skipping math/citations/commands."""

    # Environments to skip entirely
    SKIP_ENVIRONMENTS = [
        'equation', 'equation*', 'align', 'align*', 'gather', 'gather*',
        'multline', 'multline*', 'eqnarray', 'eqnarray*', 'displaymath',
        'figure', 'figure*', 'table', 'table*', 'tabular', 'tabular*',
        'lstlisting', 'verbatim', 'minted', 'algorithm', 'algorithmic',
    ]

    # Commands that should preserve their content
    PRESERVE_COMMANDS = [
        'textbf', 'textit', 'emph', 'underline', 'textsc', 'textrm',
        'textsf', 'texttt', 'textup', 'textsl',
    ]

    def __init__(self, tex_file: str):
        self.tex_file = Path(tex_file).resolve()

    def extract(self, keep_structure: bool = False) -> str:
        """
        Extract prose from LaTeX file.

        Args:
            keep_structure: Preserve paragraph/section structure

        Returns:
            Extracted plain text
        """
        try:
            content = self.tex_file.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            raise RuntimeError(f"Cannot read file: {e}")

        # Process the content
        text = self._process(content, keep_structure)

        return text

    def _process(self, content: str, keep_structure: bool) -> str:
        """Process LaTeX content to extract prose."""

        # Step 1: Remove comments (but not escaped %)
        content = re.sub(r'(?<!\\)%.*', '', content)

        # Step 2: Remove skip environments
        for env in self.SKIP_ENVIRONMENTS:
            pattern = rf'\\begin\{{{env}\}}.*?\\end\{{{env}\}}'
            content = re.sub(pattern, '', content, flags=re.DOTALL)

        # Step 3: Remove inline math
        content = re.sub(r'\$[^$]+\$', '', content)
        content = re.sub(r'\\\[.*?\\\]', '', content, flags=re.DOTALL)
        content = re.sub(r'\\\(.*?\\\)', '', content, flags=re.DOTALL)

        # Step 4: Replace citations with placeholder
        content = re.sub(r'\\(?:cite|citep|citet|parencite|textcite)\*?\{[^}]+\}', '[CITE]', content)

        # Step 5: Replace references with placeholder
        content = re.sub(r'\\(?:ref|eqref|autoref|cref|Cref)\{[^}]+\}', '[REF]', content)

        # Step 6: Remove labels
        content = re.sub(r'\\label\{[^}]+\}', '', content)

        # Step 7: Preserve content from formatting commands
        for cmd in self.PRESERVE_COMMANDS:
            pattern = rf'\\{cmd}\{{([^}}]+)\}}'
            content = re.sub(pattern, r'\1', content)

        # Step 8: Handle section headers
        if keep_structure:
            content = re.sub(r'\\section\*?\{([^}]+)\}', r'\n\n## \1\n\n', content)
            content = re.sub(r'\\subsection\*?\{([^}]+)\}', r'\n\n### \1\n\n', content)
            content = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'\n\n#### \1\n\n', content)
            content = re.sub(r'\\paragraph\*?\{([^}]+)\}', r'\n\n**\1** ', content)
        else:
            content = re.sub(r'\\(?:sub)*section\*?\{[^}]+\}', '', content)
            content = re.sub(r'\\paragraph\*?\{[^}]+\}', '', content)

        # Step 9: Remove remaining commands (but keep their arguments if simple)
        content = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^}]*)\}', r'\1', content)

        # Step 10: Remove standalone commands
        content = re.sub(r'\\[a-zA-Z]+\*?', '', content)

        # Step 11: Remove braces
        content = re.sub(r'[{}]', '', content)

        # Step 12: Clean up whitespace
        if keep_structure:
            content = re.sub(r'\n{3,}', '\n\n', content)
        else:
            content = re.sub(r'\n+', '\n', content)

        content = re.sub(r' +', ' ', content)
        content = re.sub(r'^\s+', '', content, flags=re.MULTILINE)

        return content.strip()

    def extract_sentences(self) -> List[str]:
        """Extract individual sentences from prose."""
        text = self.extract(keep_structure=False)

        # Split on sentence boundaries
        # This is a simplified approach; for better results, use nltk
        sentences = re.split(r'(?<=[.!?])\s+', text)

        # Filter empty sentences and clean
        sentences = [s.strip() for s in sentences if s.strip()]

        return sentences


def main():
    parser = argparse.ArgumentParser(
        description='LaTeX Prose Extractor'
    )
    parser.add_argument('tex_file', help='.tex file to extract from')
    parser.add_argument(
        '--output', '-o',
        help='Output file (default: stdout)'
    )
    parser.add_argument(
        '--keep-structure', '-k',
        action='store_true',
        help='Preserve paragraph and section structure'
    )
    parser.add_argument(
        '--sentences', '-s',
        action='store_true',
        help='Output as list of sentences'
    )

    args = parser.parse_args()

    # Validate input
    if not Path(args.tex_file).exists():
        print(f"[ERROR] File not found: {args.tex_file}", file=sys.stderr)
        sys.exit(1)

    # Extract
    extractor = ProseExtractor(args.tex_file)

    try:
        if args.sentences:
            sentences = extractor.extract_sentences()
            output = '\n'.join(f"{i+1}. {s}" for i, s in enumerate(sentences))
        else:
            output = extractor.extract(keep_structure=args.keep_structure)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"[SUCCESS] Extracted prose written to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
