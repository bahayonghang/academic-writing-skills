#!/usr/bin/env python3
"""
BibTeX Verification Script - Check bibliography integrity

Usage:
    python verify_bib.py references.bib
    python verify_bib.py references.bib --standard gb7714
    python verify_bib.py references.bib --tex main.tex
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set


class BibTeXVerifier:
    """Verify BibTeX file integrity and completeness."""

    # Required fields by entry type
    REQUIRED_FIELDS = {
        'article': ['author', 'title', 'journal', 'year'],
        'inproceedings': ['author', 'title', 'booktitle', 'year'],
        'incollection': ['author', 'title', 'booktitle', 'year', 'publisher'],
        'book': ['author', 'title', 'publisher', 'year'],
        'phdthesis': ['author', 'title', 'school', 'year'],
        'mastersthesis': ['author', 'title', 'school', 'year'],
        'techreport': ['author', 'title', 'institution', 'year'],
        'misc': ['author', 'title', 'year'],
        'online': ['author', 'title', 'url', 'year'],
    }

    # GB/T 7714 recommended fields
    GB7714_RECOMMENDED = ['doi', 'url', 'urldate']

    def __init__(self, bib_file: str, standard: str = 'default'):
        self.bib_file = Path(bib_file).resolve()
        self.standard = standard
        self.entries = []
        self.issues = []

    def parse(self) -> List[Dict]:
        """Parse BibTeX file into structured entries."""
        try:
            content = self.bib_file.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            self.issues.append({
                'type': 'file_error',
                'message': f'Cannot read file: {e}'
            })
            return []

        entries = []

        # Pattern for BibTeX entries
        # Matches @type{key, ... }
        entry_pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,([^@]*?)(?=\n\s*@|\Z)'

        for match in re.finditer(entry_pattern, content, re.DOTALL):
            entry_type = match.group(1).lower()
            entry_key = match.group(2).strip()
            fields_str = match.group(3)

            if entry_type in ['comment', 'string', 'preamble']:
                continue

            fields = self._parse_fields(fields_str)

            entries.append({
                'type': entry_type,
                'key': entry_key,
                'fields': fields,
                'raw': match.group(0)
            })

        self.entries = entries
        return entries

    def _parse_fields(self, fields_str: str) -> Dict[str, str]:
        """Parse field = value pairs from entry body."""
        fields = {}

        # Pattern for field = {value} or field = "value" or field = number
        field_pattern = r'(\w+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)"|(\d+))'

        for match in re.finditer(field_pattern, fields_str):
            field_name = match.group(1).lower()
            # Get value from whichever group matched
            value = match.group(2) or match.group(3) or match.group(4) or ''
            fields[field_name] = value.strip()

        return fields

    def verify(self) -> Dict:
        """Verify all entries for completeness and correctness."""
        if not self.entries:
            self.parse()

        results = {
            'total_entries': len(self.entries),
            'valid_entries': 0,
            'issues': [],
            'warnings': [],
            'status': 'PASS'
        }

        for entry in self.entries:
            entry_issues = self._verify_entry(entry)
            if entry_issues:
                results['issues'].extend(entry_issues)
            else:
                results['valid_entries'] += 1

        # Overall status
        if results['issues']:
            has_errors = any(i['severity'] == 'error' for i in results['issues'])
            results['status'] = 'FAIL' if has_errors else 'WARNING'

        return results

    def _verify_entry(self, entry: Dict) -> List[Dict]:
        """Verify a single entry."""
        issues = []
        entry_type = entry['type']
        entry_key = entry['key']
        fields = entry['fields']

        # Check required fields
        if entry_type in self.REQUIRED_FIELDS:
            required = self.REQUIRED_FIELDS[entry_type]
            for field in required:
                if field not in fields or not fields[field]:
                    # 'author' can be replaced by 'editor' for some types
                    if field == 'author' and 'editor' in fields:
                        continue
                    issues.append({
                        'key': entry_key,
                        'type': 'missing_field',
                        'field': field,
                        'severity': 'error',
                        'message': f"Missing required field '{field}'"
                    })

        # GB/T 7714 specific checks
        if self.standard == 'gb7714':
            for field in self.GB7714_RECOMMENDED:
                if field not in fields:
                    issues.append({
                        'key': entry_key,
                        'type': 'missing_recommended',
                        'field': field,
                        'severity': 'warning',
                        'message': f"Missing recommended field '{field}' (GB/T 7714)"
                    })

        # Check for common issues
        if 'title' in fields:
            title = fields['title']
            # Check for unprotected capitals
            if re.search(r'\b[A-Z]{2,}\b', title) and not re.search(r'\{[A-Z]+\}', title):
                issues.append({
                    'key': entry_key,
                    'type': 'unprotected_capitals',
                    'severity': 'warning',
                    'message': 'Title contains uppercase that may be lowercased by some styles'
                })

        return issues

    def check_citations(self, tex_file: str) -> Dict:
        """Check if all citations in tex file exist in bib file."""
        if not self.entries:
            self.parse()

        tex_path = Path(tex_file)
        try:
            tex_content = tex_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return {'status': 'ERROR', 'message': str(e)}

        # Find all citations
        cite_pattern = r'\\(?:cite|citep|citet|parencite|textcite)\*?\{([^}]+)\}'
        cited_keys = set()

        for match in re.finditer(cite_pattern, tex_content):
            keys = match.group(1).split(',')
            for key in keys:
                cited_keys.add(key.strip())

        # Check against bib entries
        bib_keys = {e['key'] for e in self.entries}

        missing = cited_keys - bib_keys
        unused = bib_keys - cited_keys

        return {
            'status': 'PASS' if not missing else 'WARNING',
            'cited': len(cited_keys),
            'in_bib': len(bib_keys),
            'missing': list(missing),
            'unused': list(unused)
        }

    def generate_report(self, result: Dict, citation_result: Optional[Dict] = None) -> str:
        """Generate human-readable report."""
        lines = []
        lines.append("=" * 60)
        lines.append("BibTeX Verification Report")
        lines.append("=" * 60)
        lines.append(f"File: {self.bib_file}")
        lines.append(f"Standard: {self.standard}")
        lines.append(f"Status: {result['status']}")
        lines.append(f"Total entries: {result['total_entries']}")
        lines.append(f"Valid entries: {result['valid_entries']}")

        if result['issues']:
            lines.append("")
            lines.append("-" * 60)
            lines.append("Issues:")
            lines.append("-" * 60)

            # Group by key
            by_key = {}
            for issue in result['issues']:
                key = issue['key']
                if key not in by_key:
                    by_key[key] = []
                by_key[key].append(issue)

            for key, issues in sorted(by_key.items()):
                lines.append(f"\n[@{key}]")
                for issue in issues:
                    severity = issue['severity'].upper()
                    lines.append(f"  [{severity}] {issue['message']}")

        if citation_result:
            lines.append("")
            lines.append("-" * 60)
            lines.append("Citation Check:")
            lines.append("-" * 60)
            lines.append(f"Citations in document: {citation_result['cited']}")
            lines.append(f"Entries in bibliography: {citation_result['in_bib']}")

            if citation_result['missing']:
                lines.append(f"\nMissing entries ({len(citation_result['missing'])}):")
                for key in citation_result['missing'][:10]:
                    lines.append(f"  - {key}")
                if len(citation_result['missing']) > 10:
                    lines.append(f"  ... and {len(citation_result['missing']) - 10} more")

            if citation_result['unused']:
                lines.append(f"\nUnused entries ({len(citation_result['unused'])}):")
                for key in citation_result['unused'][:10]:
                    lines.append(f"  - {key}")

        lines.append("")
        lines.append("=" * 60)
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='BibTeX Verification Script'
    )
    parser.add_argument('bib_file', help='.bib file to verify')
    parser.add_argument(
        '--standard', '-s',
        choices=['default', 'gb7714'],
        default='default',
        help='Citation standard to check against'
    )
    parser.add_argument(
        '--tex', '-t',
        help='Check citations against this .tex file'
    )
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='Output in JSON format'
    )

    args = parser.parse_args()

    # Validate input
    if not Path(args.bib_file).exists():
        print(f"[ERROR] File not found: {args.bib_file}")
        sys.exit(1)

    # Run verification
    verifier = BibTeXVerifier(args.bib_file, args.standard)
    result = verifier.verify()

    citation_result = None
    if args.tex:
        if not Path(args.tex).exists():
            print(f"[ERROR] TeX file not found: {args.tex}")
            sys.exit(1)
        citation_result = verifier.check_citations(args.tex)

    # Output
    if args.json:
        import json
        output = {'verification': result}
        if citation_result:
            output['citations'] = citation_result
        print(json.dumps(output, indent=2))
    else:
        print(verifier.generate_report(result, citation_result))

    # Exit code
    if result['status'] == 'FAIL':
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
