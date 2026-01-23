"""
Document Parsers for Academic Writing Skills (Typst)
Support for Typst document parsing.
"""

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any


class DocumentParser(ABC):
    """Abstract base class for document parsers."""

    @abstractmethod
    def split_sections(self, content: str) -> Dict[str, Tuple[int, int]]:
        """
        Split document into sections.
        Returns map of {section_name: (start_line, end_line)}.
        """
        pass

    @abstractmethod
    def extract_visible_text(self, line: str) -> str:
        """
        Extract text visible to reader, preserving structure markers.
        Used for line-by-line AI trace checking.
        """
        pass

    @abstractmethod
    def clean_text(self, content: str, keep_structure: bool = False) -> str:
        """
        Extract pure prose text, removing all markup.
        Used for prose extraction and word counting.
        """
        pass

    @abstractmethod
    def get_comment_prefix(self) -> str:
        """Get the comment prefix for the language."""
        pass


class TypstParser(DocumentParser):
    """Parser for Typst documents."""

    # Section patterns (Heading 1-3)
    # Matches: = Introduction or == Related Work
    SECTION_PATTERNS = {
        'introduction': r'^=\s+(?:Introduction|INTRODUCTION)',
        'related': r'^=\s+(?:Related\s+Work|RELATED\s+WORK)',
        'method': r'^=\s+.*(?:Method|Methodology|Approach)',
        'experiment': r'^=\s+.*(?:Experiment|Evaluation|Implementation)',
        'result': r'^=\s+.*(?:Result|Performance)',
        'discussion': r'^=\s+.*(?:Discussion|Analysis)',
        'conclusion': r'^=\s+.*(?:Conclusion|Conclusions)',
        'abstract': r'#abstract\['
    }

    PRESERVE_PATTERNS = [
        r'@[a-zA-Z0-9_-]+',           # Citations @key
        r'#cite\([^)]+\)',            # Function calls #cite()
        r'#figure\([^)]+\)',          # Figures
        r'#table\([^)]+\)',           # Tables
        r'\$[^$]+\$',                 # Math $...$
        r'//.*',                      # Line comments
        r'/\[.*?\]',                 # Block comments
        r'<[a-zA-Z0-9_-]+>',          # Labels <label>
        r'#link\([^)]+\)',            # Links
    ]

    def get_comment_prefix(self) -> str:
        return '//'

    def split_sections(self, content: str) -> Dict[str, Tuple[int, int]]:
        lines = content.split('\n')
        sections = {}
        current_section = 'preamble'
        start_line = 0

        for i, line in enumerate(lines, 1):
            line = line.strip()
            # Ignore comments
            if line.startswith('//'):
                continue

            matched = False
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line, re.IGNORECASE):
                    if current_section != 'preamble':
                        sections[current_section] = (start_line, i - 1)
                    current_section = section_name
                    start_line = i
                    matched = True
                    break

        if current_section != 'preamble':
            sections[current_section] = (start_line, len(lines))

        return sections

    def extract_visible_text(self, line: str) -> str:
        # Same logic as LatexParser but with Typst patterns
        temp_line = line

        # Remove comments first for Typst
        if '//' in temp_line:
            temp_line = temp_line.split('//')[0]

        preserved = []
        for pattern in self.PRESERVE_PATTERNS:
            matches = list(re.finditer(pattern, temp_line, re.DOTALL))
            for match in reversed(matches):
                preserved.append({
                    'start': match.start(),
                    'end': match.end(),
                    'text': match.group()
                })
                placeholder = ' ' * (match.end() - match.start())
                temp_line = temp_line[:match.start()] + placeholder + temp_line[match.end():]

        preserved.sort(key=lambda x: x['start'])

        visible_parts = []
        last_end = 0
        for item in preserved:
            if item['start'] > last_end:
                visible_parts.append(temp_line[last_end:item['start']])
            last_end = item['end']
        if last_end < len(temp_line):
            visible_parts.append(temp_line[last_end:])

        return ' '.join(visible_parts).strip()

    def clean_text(self, content: str, keep_structure: bool = False) -> str:
        # Remove comments
        content = re.sub(r'//.*', '', content)
        content = re.sub(r'/\[.*?\]', '', content, flags=re.DOTALL)

        # Remove math
        content = re.sub(r'\$[^$]+\$', '', content)

        # Handle headers
        if keep_structure:
            content = re.sub(r'^=+\s+(.+)$', r'\n\n## \1\n\n', content, flags=re.MULTILINE)
        else:
            content = re.sub(r'^=+\s+.+$', '', content, flags=re.MULTILINE)

        # Remove function calls #func(...) - basic support
        content = re.sub(r'#[a-zA-Z0-9_]+\([^)]*\)', '', content)
        content = re.sub(r'@[a-zA-Z0-9_-]+', '', content)
        content = re.sub(r'<[a-zA-Z0-9_-]+>', '', content)

        # Cleanup
        content = re.sub(r'\n+', '\n', content)
        content = re.sub(r' +', ' ', content)
        return content.strip()


def get_parser(file_path: Any) -> DocumentParser:
    """Factory method to get appropriate parser for Typst files."""
    return TypstParser()
