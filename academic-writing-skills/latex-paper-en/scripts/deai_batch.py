#!/usr/bin/env python3
"""
De-AI Batch Processor for English Academic Papers

Batch processes entire LaTeX chapters or documents for de-AI polishing.
Compatible with IEEE TOP journal style (Mode I).

Usage:
    python deai_batch.py main.tex --chapter chapter3/introduction.tex
    python deai_batch.py main.tex --all-sections
    python deai_batch.py main.tex --section introduction --output polished/
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class DeAIBatchProcessor:
    """Batch process LaTeX files for de-AI editing."""

    # Section patterns for splitting
    SECTION_PATTERNS = {
        'abstract': r'\\begin\{abstract\}|\\section\{abstract\}?',
        'introduction': r'\\section\{Introduction\}|\\section\{INTRODUCTION\}',
        'related': r'\\section\{Related\s+Work\}|\\section\{RELATED\s+WORK\}',
        'method': r'\\section\{.*(?:Method|Methodology|Approach)\}',
        'experiment': r'\\section\{.*(?:Experiment|Evaluation|Implementation)\}',
        'result': r'\\section\{.*(?:Result|Performance)\}',
        'discussion': r'\\section\{.*(?:Discussion|Analysis)\}',
        'conclusion': r'\\section\{.*(?:Conclusion|Conclusions)\}',
    }

    # LaTeX structure preservation patterns
    PRESERVE_PATTERNS = [
        r'\\cite\{[^}]+\}',           # Citations
        r'\\ref\{[^}]+\}',            # References
        r'\\label\{[^}]+\}',          # Labels
        r'\\eqref\{[^}]+\}',          # Equation references
        r'\\autoref\{[^}]+\}',        # Auto references
        r'\$\$[^$]+\$\$',            # Display math
        r'\$[^$]+\$',                # Inline math
        r'\\begin\{equation\}.*?\\end\{equation\}',  # Equations
        r'\\begin\{align\}.*?\\end\{align\}',        # Align environments
        r'\\begin\{.*?\}.*?\\end\{.*?\}',           # Generic environments
        r'\\includegraphics\[?[^\]]*\]?\{[^}]+\}',  # Images
        r'\\caption\{[^}]+\}',        # Captions
    ]

    def __init__(self, tex_file: Path):
        self.tex_file = tex_file
        self.content = tex_file.read_text(encoding='utf-8', errors='ignore')
        self.lines = self.content.split('\n')
        self.sections = self._split_sections()

    def _split_sections(self) -> Dict[str, Tuple[int, int, List[str]]]:
        """Split document into sections by LaTeX structure."""
        sections = {}
        current_section = 'preamble'
        start_line = 0
        section_content = []

        for i, line in enumerate(self.lines, 1):
            matched = False
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line, re.IGNORECASE):
                    if current_section != 'preamble':
                        sections[current_section] = (start_line, i - 1, section_content)
                    current_section = section_name
                    start_line = i
                    section_content = []
                    matched = True
                    break

            section_content.append(line)

        # Last section
        if section_content:
            sections[current_section] = (start_line, len(self.lines), section_content)

        return sections

    def extract_visible_text(self, line: str) -> str:
        """Extract only visible text, preserving LaTeX structure markers."""
        # Preserve structure markers
        preserved = []
        temp_line = line

        # Find and mark all preserved patterns
        for pattern in self.PRESERVE_PATTERNS:
            matches = list(re.finditer(pattern, temp_line, re.DOTALL))
            for match in reversed(matches):
                preserved.append({
                    'start': match.start(),
                    'end': match.end(),
                    'text': match.group()
                })
                temp_line = temp_line[:match.start()] + ' ' * (match.end() - match.start()) + temp_line[match.end():]

        # Sort preserved items by position
        preserved.sort(key=lambda x: x['start'])

        # Extract visible text (excluding preserved parts)
        visible_parts = []
        last_end = 0

        for item in preserved:
            if item['start'] > last_end:
                visible_parts.append(temp_line[last_end:item['start']])
            last_end = item['end']

        if last_end < len(temp_line):
            visible_parts.append(temp_line[last_end:])

        visible_text = ' '.join(visible_parts).strip()
        return visible_text

    def analyze_section(self, section_name: str) -> Dict:
        """Analyze a section for AI traces."""
        if section_name not in self.sections:
            return {
                'section': section_name,
                'found': False,
                'lines': 0,
                'traces': [],
            }

        start, end, content = self.sections[section_name]
        traces = []
        line_num = start

        for line in content:
            stripped = line.strip()
            if not stripped or stripped.startswith('%'):
                line_num += 1
                continue

            visible = self.extract_visible_text(stripped)

            # Check for AI patterns
            ai_patterns = self._check_ai_patterns(visible)

            if ai_patterns:
                traces.append({
                    'line': line_num,
                    'original': stripped,
                    'visible': visible,
                    'patterns': ai_patterns,
                })

            line_num += 1

        return {
            'section': section_name,
            'found': True,
            'lines': end - start + 1,
            'traces': traces,
        }

    def _check_ai_patterns(self, text: str) -> List[str]:
        """Check text for AI writing patterns."""
        patterns = []

        # Empty phrases
        empty_phrases = [
            r'significant (?:improvement|performance|gain)',
            r'comprehensive (?:analysis|study)',
            r'effective (?:solution|method)',
            r'important (?:contribution|role)',
            r'robust performance',
            r'novel approach',
            r'state-of-the-art',
        ]

        # Over-confident
        over_confident = [
            r'\bobviously\b',
            r'\bclearly\b',
            r'\bcertainly\b',
            r'\bundoubtedly\b',
        ]

        # Vague quantifiers
        vague_quantifiers = [
            r'\bmany studies\b',
            r'\bnumerous experiments\b',
            r'\bvarious methods\b',
            r'\bseveral approaches\b',
        ]

        # Template expressions
        template_exprs = [
            r'\bin recent years\b',
            r'\bmore and more\b',
            r'\bplays? an important role\b',
            r'\bwith the (?:rapid )?development of\b',
        ]

        all_checks = [
            ('empty_phrase', empty_phrases),
            ('over_confident', over_confident),
            ('vague_quantifier', vague_quantifiers),
            ('template_expr', template_exprs),
        ]

        for category, pattern_list in all_checks:
            for pattern in pattern_list:
                if re.search(pattern, text, re.IGNORECASE):
                    patterns.append(f'{category}: {pattern}')

        return patterns

    def generate_batch_report(self, analyses: Dict[str, Dict]) -> str:
        """Generate batch processing report."""
        report = []
        report.append("=" * 70)
        report.append("DE-AI BATCH PROCESSING REPORT")
        report.append("=" * 70)
        report.append(f"Source file: {self.tex_file}")
        report.append("")

        total_traces = 0
        total_lines = 0

        for section_name, analysis in analyses.items():
            if not analysis['found']:
                continue

            trace_count = len(analysis['traces'])
            total_traces += trace_count
            total_lines += analysis['lines']

            density = (trace_count / analysis['lines'] * 100) if analysis['lines'] > 0 else 0

            report.append(f"\n{'─' * 70}")
            report.append(f"SECTION: {section_name.upper()}")
            report.append(f"{'─' * 70}")
            report.append(f"Lines: {analysis['lines']}")
            report.append(f"AI traces detected: {trace_count}")
            report.append(f"Density: {density:.1f}%")

            if trace_count > 0:
                report.append(f"\nTraces (first 5):")
                for i, trace in enumerate(analysis['traces'][:5], 1):
                    report.append(f"\n  [{i}] Line {trace['line']}")
                    report.append(f"      Patterns: {', '.join(trace['patterns'])}")
                    report.append(f"      Visible: {trace['visible'][:100]}")

        report.append("\n" + "=" * 70)
        report.append("SUMMARY")
        report.append("=" * 70)
        report.append(f"Total lines analyzed: {total_lines}")
        report.append(f"Total AI traces: {total_traces}")
        overall_density = (total_traces / total_lines * 100) if total_lines > 0 else 0
        report.append(f"Overall density: {overall_density:.1f}%")

        return "\n".join(report)

    def process_section_file(self, chapter_file: Path, output_dir: Path) -> bool:
        """Process a single chapter file."""
        if not chapter_file.exists():
            print(f"[ERROR] Chapter file not found: {chapter_file}")
            return False

        # Read chapter content
        content = chapter_file.read_text(encoding='utf-8')
        lines = content.split('\n')

        # Process each line
        processed_lines = []
        modifications = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip empty lines and comments
            if not stripped or stripped.startswith('%'):
                processed_lines.append(line)
                continue

            visible = self.extract_visible_text(stripped)
            patterns = self._check_ai_patterns(visible)

            if patterns:
                # Add de-AI editing comment
                comment = f"% DE-AI: Line {i} - {', '.join(patterns)}"
                processed_lines.append(comment)
                processed_lines.append(line)
                modifications.append({
                    'line': i,
                    'patterns': patterns,
                    'original': stripped,
                })
            else:
                processed_lines.append(line)

        # Write output
        output_file = output_dir / chapter_file.name
        output_file.write_text('\n'.join(processed_lines), encoding='utf-8')

        print(f"[SUCCESS] Processed: {chapter_file.name}")
        print(f"         Output: {output_file}")
        print(f"         Modifications: {len(modifications)}")

        return True


def main():
    parser = argparse.ArgumentParser(
        description='Batch process LaTeX documents for de-AI editing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all sections
  python deai_batch.py paper.tex --all-sections

  # Process specific chapter file
  python deai_batch.py main.tex --chapter chapter3/introduction.tex --output polished/

  # Analyze specific section
  python deai_batch.py paper.tex --section introduction
        """
    )

    parser.add_argument('tex_file', type=Path, help='Main LaTeX file')
    parser.add_argument('--chapter', type=Path, help='Process specific chapter file')
    parser.add_argument('--all-sections', action='store_true', help='Analyze all sections')
    parser.add_argument('--section', type=str, help='Analyze specific section')
    parser.add_argument('--output', type=Path, help='Output directory for processed files')
    parser.add_argument('--report', type=Path, help='Save report to file')

    args = parser.parse_args()

    if not args.tex_file.exists():
        print(f"[ERROR] File not found: {args.tex_file}", file=sys.stderr)
        sys.exit(1)

    processor = DeAIBatchProcessor(args.tex_file)

    if args.all_sections:
        # Analyze all sections
        analyses = {}
        for section_name in processor.sections.keys():
            analyses[section_name] = processor.analyze_section(section_name)

        report = processor.generate_batch_report(analyses)

        if args.report:
            args.report.write_text(report, encoding='utf-8')
            print(f"[SUCCESS] Report saved to: {args.report}")
        else:
            print(report)

    elif args.chapter:
        # Process specific chapter file
        if not args.output:
            print("[ERROR] --output required when processing chapter file")
            sys.exit(1)

        args.output.mkdir(parents=True, exist_ok=True)
        success = processor.process_section_file(args.chapter, args.output)

        sys.exit(0 if success else 1)

    elif args.section:
        # Analyze specific section
        analysis = processor.analyze_section(args.section.lower())

        if not analysis['found']:
            print(f"[WARNING] Section not found: {args.section}")
            sys.exit(1)

        print(f"\nSection: {args.section}")
        print(f"Lines: {analysis['lines']}")
        print(f"AI traces: {len(analysis['traces'])}\n")

        for trace in analysis['traces'][:10]:
            print(f"Line {trace['line']}:")
            print(f"  Patterns: {', '.join(trace['patterns'])}")
            print(f"  Text: {trace['visible'][:100]}")
            print()

    else:
        # Default: list available sections
        print(f"[INFO] Available sections in {args.tex_file.name}:")
        for section_name in processor.sections.keys():
            start, end, _ = processor.sections[section_name]
            print(f"  - {section_name}: lines {start}-{end}")


if __name__ == '__main__':
    main()
