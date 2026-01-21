#!/usr/bin/env python3
"""
De-AI Writing Trace Checker for English Academic Papers

Analyzes LaTeX source code for AI writing patterns and generates reports.
Compatible with IEEE TOP journal style (Mode I).

Usage:
    python deai_check.py main.tex --section introduction
    python deai_check.py main.tex --analyze
    python deai_check.py main.tex --score
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class AITraceChecker:
    """Detect AI writing traces in LaTeX documents."""

    # High-priority AI patterns (Category 1: Empty phrases)
    EMPTY_PHRASES = {
        r'\bsignificant\s+(?:improvement|performance|gain|enhancement|advancement)\b',
        r'\bcomprehensive\s+(?:analysis|study|overview|survey|review)\b',
        r'\beffective\s+(?:solution|method|approach|technique)\b',
        r'\bimportant\s+(?:contribution|role|impact|implication)\b',
        r'\brobust\s+(?:performance|method|approach)\b',
        r'\bnovel\s+(?:approach|method|technique|algorithm)\b',
        r'\bstate-of-the-art\s+(?:performance|results|accuracy)\b',
    }

    # High-priority AI patterns (Category 2: Over-confident)
    OVER_CONFIDENT = {
        r'\bobviously\b',
        r'\bclearly\b',
        r'\bcertainly\b',
        r'\bundoubtedly\b',
        r'\bnecessarily\b',
        r'\bcompletely\b',
        r'\balways\b',
        r'\bnever\b',
    }

    # High-priority AI patterns (Category 4: Vague quantification)
    VAGUE_QUANTIFIERS = {
        r'\bmany\s+studies\b',
        r'\bnumerous\s+experiments?\b',
        r'\bvarious\s+methods?\b',
        r'\bseveral\s+approaches?\b',
        r'\bmultiple\s+(?:datasets?|methods?|experiments?)\b',
        r'\ba\s+(?:lot|large\s+number)\s+of\b',
        r'\bthe\s+majority\s+of\b',
        r'\bsubstantial\s+(?:amount|number|gain|improvement)\b',
    }

    # Medium-priority AI patterns (Category 3: Template expressions)
    TEMPLATE_EXPRESSIONS = {
        r'\bin\s+recent\s+years\b',
        r'\bmore\s+and\s+more\b',
        r'\bplays?\s+an?\s+important\s+role\b',
        r'\bwith\s+the\s+(?:rapid\s+)?development\s+of\b',
        r'\bhas\s+(?:been\s+)?widely\s+used\b',
        r'\bhas\s+attracted\s+(?:much\s+)?attention\b',
    }

    # Section detection patterns
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

    def __init__(self, tex_file: Path):
        self.tex_file = tex_file
        self.content = tex_file.read_text(encoding='utf-8', errors='ignore')
        self.lines = self.content.split('\n')
        self.traces = defaultdict(list)
        self.section_ranges = self._detect_sections()

    def _detect_sections(self) -> Dict[str, Tuple[int, int]]:
        """Detect section line ranges."""
        sections = {}
        current_section = 'preamble'
        start_line = 0

        for i, line in enumerate(self.lines, 1):
            matched = False
            for section_name, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, line, re.IGNORECASE):
                    if current_section != 'preamble':
                        sections[current_section] = (start_line, i - 1)
                    current_section = section_name
                    start_line = i
                    matched = True
                    break

        # Last section
        if current_section != 'preamble':
            sections[current_section] = (start_line, len(self.lines))

        return sections

    def _find_pattern_in_section(
        self,
        pattern: str,
        section_name: str,
        category: str
    ) -> List[Dict]:
        """Find pattern occurrences in a specific section."""
        if section_name not in self.section_ranges:
            return []

        start, end = self.section_ranges[section_name]
        matches = []

        for i in range(start - 1, min(end, len(self.lines))):
            line = self.lines[i]
            if re.search(pattern, line, re.IGNORECASE):
                # Skip comments
                stripped = line.strip()
                if stripped.startswith('%'):
                    continue
                matches.append({
                    'line': i + 1,
                    'text': stripped,
                    'pattern': pattern,
                    'category': category,
                    'section': section_name,
                })

        return matches

    def check_section(self, section_name: str) -> Dict:
        """Check a specific section for AI traces."""
        results = {
            'section': section_name,
            'total_lines': 0,
            'trace_count': 0,
            'traces': [],
        }

        if section_name not in self.section_ranges:
            start, end = 1, len(self.lines)
        else:
            start, end = self.section_ranges[section_name]

        results['total_lines'] = end - start + 1

        # Check all pattern categories
        all_patterns = [
            ('empty_phrase', self.EMPTY_PHRASES),
            ('over_confident', self.OVER_CONFIDENT),
            ('vague_quantifier', self.VAGUE_QUANTIFIERS),
            ('template_expr', self.TEMPLATE_EXPRESSIONS),
        ]

        for category, patterns in all_patterns:
            for pattern in patterns:
                matches = self._find_pattern_in_section(pattern, section_name, category)
                results['traces'].extend(matches)

        results['trace_count'] = len(results['traces'])

        return results

    def analyze_document(self) -> Dict:
        """Analyze entire document and generate section-wise scores."""
        analysis = {
            'total_lines': len(self.lines),
            'sections': {},
        }

        for section_name in self.section_ranges.keys():
            section_result = self.check_section(section_name)
            analysis['sections'][section_name] = section_result

        return analysis

    def calculate_density_score(self, result: Dict) -> float:
        """Calculate AI trace density score for a section."""
        if result['total_lines'] == 0:
            return 0.0
        return (result['trace_count'] / result['total_lines']) * 100

    def generate_report(self, analysis: Dict) -> str:
        """Generate human-readable report."""
        report = []
        report.append("=" * 70)
        report.append("DE-AI WRITING TRACE ANALYSIS REPORT")
        report.append("=" * 70)
        report.append(f"File: {self.tex_file}")
        report.append(f"Total lines: {analysis['total_lines']}")
        report.append("")

        # Section-wise summary
        report.append("-" * 70)
        report.append("SECTION-WISE AI TRACE DENSITY")
        report.append("-" * 70)

        section_scores = []
        for section_name, result in analysis['sections'].items():
            score = self.calculate_density_score(result)
            section_scores.append((section_name, score, result))

            # Priority indicator
            if score > 10:
                priority = "CRITICAL"
            elif score > 5:
                priority = "HIGH"
            elif score > 2:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            report.append(f"\n[{priority}] {section_name.upper()}")
            report.append(f"  AI trace density: {score:.1f}%")
            report.append(f"  Traces found: {result['trace_count']} / {result['total_lines']} lines")

        # Priority ranking
        report.append("")
        report.append("-" * 70)
        report.append("PRIORITY RANKING (Sections to rewrite first)")
        report.append("-" * 70)
        section_scores.sort(key=lambda x: x[1], reverse=True)

        for i, (section_name, score, result) in enumerate(section_scores, 1):
            if score > 2:
                report.append(f"{i}. {section_name}: {score:.1f}% ({result['trace_count']} traces)")

        # Detailed trace listing
        report.append("")
        report.append("-" * 70)
        report.append("DETAILED TRACE LISTING")
        report.append("-" * 70)

        for section_name, result in analysis['sections'].items():
            if result['traces']:
                report.append(f"\n{section_name.upper()}:")
                for trace in result['traces'][:10]:  # Limit to first 10
                    report.append(f"  Line {trace['line']} [{trace['category']}]")
                    report.append(f"    {trace['text'][:80]}")

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze LaTeX documents for AI writing traces',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze entire document
  python deai_check.py paper.tex --analyze

  # Check specific section
  python deai_check.py paper.tex --section introduction

  # Generate score report only
  python deai_check.py paper.tex --score
        """
    )

    parser.add_argument('tex_file', type=Path, help='LaTeX file to analyze')
    parser.add_argument('--section', type=str, help='Specific section to check')
    parser.add_argument('--analyze', action='store_true', help='Full document analysis')
    parser.add_argument('--score', action='store_true', help='Output section scores only')
    parser.add_argument('--output', type=Path, help='Save report to file')

    args = parser.parse_args()

    if not args.tex_file.exists():
        print(f"[ERROR] File not found: {args.tex_file}", file=sys.stderr)
        sys.exit(1)

    checker = AITraceChecker(args.tex_file)

    if args.analyze:
        # Full document analysis
        analysis = checker.analyze_document()
        report = checker.generate_report(analysis)

        if args.output:
            args.output.write_text(report, encoding='utf-8')
            print(f"[SUCCESS] Report saved to: {args.output}")
        else:
            print(report)

        # Exit with code based on worst section
        worst_score = max(
            checker.calculate_density_score(result)
            for result in analysis['sections'].values()
        )
        if worst_score > 10:
            sys.exit(2)  # Critical
        elif worst_score > 5:
            sys.exit(1)  # Warning
        else:
            sys.exit(0)

    elif args.section:
        # Check specific section
        result = checker.check_section(args.section.lower())
        score = checker.calculate_density_score(result)

        print(f"\nSection: {args.section}")
        print(f"AI trace density: {score:.1f}%")
        print(f"Traces found: {result['trace_count']}\n")

        for trace in result['traces']:
            print(f"Line {trace['line']} [{trace['category']}]")
            print(f"  {trace['text']}\n")

    elif args.score:
        # Score-only output
        analysis = checker.analyze_document()
        print(f"\n{'Section':<15} {'Density':<10} {'Traces':<10}")
        print("-" * 35)

        for section_name, result in analysis['sections'].items():
            score = checker.calculate_density_score(result)
            print(f"{section_name:<15} {score:>6.1f}%     {result['trace_count']:>3} / {result['total_lines']:>3}")

    else:
        # Default: interactive mode prompt
        print("[INFO] Use --analyze for full document analysis")
        print("[INFO] Use --section <name> to check specific section")
        print("[INFO] Use --score for section-wise density scores")
        print(f"\n[INFO] Detected sections in {args.tex_file.name}:")
        for section_name in checker.section_ranges.keys():
            print(f"  - {section_name}")


if __name__ == '__main__':
    main()
