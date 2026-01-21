"""
Document Parsers for Chinese Academic Thesis
Support for LaTeX and Typst document parsing.
"""

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

class DocumentParser(ABC):
    """Abstract base class for document parsers."""

    @abstractmethod
    def split_sections(self, content: str) -> Dict[str, Tuple[int, int]]:
        pass

    @abstractmethod
    def extract_visible_text(self, line: str) -> str:
        pass
        
    @abstractmethod
    def get_comment_prefix(self) -> str:
        pass


class LatexParser(DocumentParser):
    """Parser for Chinese LaTeX Thesis."""

    # Chinese Section patterns
    SECTION_PATTERNS = {
        'abstract': r'\\chapter{摘要}|\\section{摘要}',
        'introduction': r'\\chapter{绪论}|\\chapter{引言}|\\section{绪论}|\\section{引言}',
        'related': r'\\chapter{相关工作}|\\section{相关工作}|\\section{文献综述}',
        'method': r'\\chapter{.*?(?:方法|原理|设计)}',
        'experiment': r'\\chapter{.*?(?:实验|实现|测试)}|\\section{.*?(?:实验|实现)}',
        'result': r'\\chapter{.*?(?:结果|性能)}|\\section{.*?(?:结果|性能)}',
        'discussion': r'\\chapter{.*?(?:讨论|分析)}|\\section{.*?(?:讨论|分析)}',
        'conclusion': r'\\chapter{结论}|\\chapter{总结与展望}|\\section{结论}',
    }

    PRESERVE_PATTERNS = [
        r'\\cite{[^}]+}',           # Citations
        r'\\ref{[^}]+}',            # References
        r'\\label{[^}]+}',          # Labels
        r'\\eqref{[^}]+}',          # Equation references
        r'\\autoref{[^}]+}',        # Auto references
        r'\\$\$[^$]+\\$\$',            # Display math
        r'\$[^$]+\$',                # Inline math
        r'\\begin{equation}.*?end{equation}',  # Equations
        r'\\begin{align}.*?end{align}',        # Align environments
        r'\\begin{.*?}.*?end{.*?}',           # Generic environments
        r'\\includegraphics\[?[^]]*\]?{[^}]+}',  # Images
        r'\\caption{[^}]+}',        # Captions
    ]

    def get_comment_prefix(self) -> str:
        return '%'

    def split_sections(self, content: str) -> Dict[str, Tuple[int, int]]:
        lines = content.split('\n')
        sections = {}
        current_section = 'preamble'
        start_line = 0

        for i, line in enumerate(lines, 1):
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line, re.IGNORECASE):
                    if current_section != 'preamble':
                        sections[current_section] = (start_line, i - 1)
                    current_section = section_name
                    start_line = i
                    break
        
        if current_section != 'preamble':
            sections[current_section] = (start_line, len(lines))
            
        return sections

    def extract_visible_text(self, line: str) -> str:
        temp_line = line
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


class TypstParser(DocumentParser):
    """Parser for Chinese Typst Thesis."""

    # Chinese Section patterns for Typst
    # e.g. = 摘要, = 绪论
    SECTION_PATTERNS = {
        'abstract': r'^=\s+摘要',
        'introduction': r'^=\s+(?:绪论|引言)',
        'related': r'^=\s+(?:相关工作|文献综述)',
        'method': r'^=\s+.*(?:方法|原理|设计)',
        'experiment': r'^=\s+.*(?:实验|实现|测试)',
        'result': r'^=\s+.*(?:结果|性能)',
        'discussion': r'^=\s+.*(?:讨论|分析)',
        'conclusion': r'^=\s+.*(?:结论|总结与展望)',
    }

    PRESERVE_PATTERNS = [
        r'@[a-zA-Z0-9_-]+',           # Citations
        r'#cite\([^)]+\)',            
        r'#figure\([^)]+\)',          
        r'#table\([^)]+\)',           
        r'\$[^$]+\$',                 
        r'//.*',                      
        r'/\*.*?\*/',                 
        r'<[a-zA-Z0-9_-]+>',          
        r'#link\([^)]+\)',            
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
            if line.startswith('//'):
                continue
            
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line):
                    if current_section != 'preamble':
                        sections[current_section] = (start_line, i - 1)
                    current_section = section_name
                    start_line = i
                    break
            
        if current_section != 'preamble':
            sections[current_section] = (start_line, len(lines))
            
        return sections

    def extract_visible_text(self, line: str) -> str:
        temp_line = line
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


def get_parser(file_path: Any) -> DocumentParser:
    """Factory method to get appropriate parser."""
    path_str = str(file_path).lower()
    if path_str.endswith('.typ'):
        return TypstParser()
    return LatexParser()
