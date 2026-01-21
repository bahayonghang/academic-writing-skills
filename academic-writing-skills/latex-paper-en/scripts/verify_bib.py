#!/usr/bin/env python3
"""
BibTeX Verification Script - Check bibliography integrity
Includes static checks and online verification preparation.

Usage:
    python verify_bib.py references.bib
    python verify_bib.py references.bib --standard gb7714
    python verify_bib.py references.bib --online-check
"""

import argparse
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Set


class BibTeXVerifier:
    """Verify BibTeX file integrity and completeness."""

    REQUIRED_FIELDS = {
        'article': ['author', 'title', 'journal', 'year'],
        'inproceedings': ['author', 'title', 'booktitle', 'year'],
        'book': ['author', 'title', 'publisher', 'year'],
    }

    GB7714_RECOMMENDED = ['doi', 'url', 'urldate']

    def __init__(self, bib_file: str, standard: str = 'default'):
        self.bib_file = Path(bib_file).resolve()
        self.standard = standard
        self.entries = []
        self.issues = []

    def parse(self) -> List[Dict]:
        """Parse BibTeX file."""
        try:
            content = self.bib_file.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            self.issues.append({'type': 'file_error', 'message': str(e)})
            return []

        entries = []
        # Robust regex for entries
        entry_pattern = r'@(\w+)\s*{\s*([^,]+)\s*,([^@]*?)(?=\n\s*@|\Z)'

        for match in re.finditer(entry_pattern, content, re.DOTALL):
            entries.append({
                'type': match.group(1).lower(),
                'key': match.group(2).strip(),
                'fields': self._parse_fields(match.group(3)),
                'raw': match.group(0)
            })

        self.entries = entries
        return entries

    def _parse_fields(self, fields_str: str) -> Dict[str, str]:
        fields = {}
        # Parse field = {value} or "value" or number
        field_pattern = r'(\w+)\s*=\s*(?:\{([^^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)"|(\d+))'
        for match in re.finditer(field_pattern, fields_str):
            name = match.group(1).lower()
            val = match.group(2) or match.group(3) or match.group(4) or ''
            fields[name] = val.strip()
        return fields

    def verify(self) -> Dict:
        if not self.entries:
            self.parse()

        results = {
            'total_entries': len(self.entries),
            'valid_entries': 0,
            'issues': [],
            'status': 'PASS',
            'needs_online_check': []
        }

        for entry in self.entries:
            entry_issues = self._verify_entry(entry)
            
            # Check for missing identifiers (DOI/ArXiv)
            if 'doi' not in entry['fields'] and 'url' not in entry['fields']:
                 results['needs_online_check'].append({
                     'key': entry['key'],
                     'title': entry['fields'].get('title', 'Unknown Title'),
                     'author': entry['fields'].get('author', 'Unknown Author')
                 })

            if entry_issues:
                results['issues'].extend(entry_issues)
            else:
                results['valid_entries'] += 1

        if results['issues']:
            has_errors = any(i['severity'] == 'error' for i in results['issues'])
            results['status'] = 'FAIL' if has_errors else 'WARNING'

        return results

    def _verify_entry(self, entry: Dict) -> List[Dict]:
        issues = []
        entry_type = entry['type']
        entry_key = entry['key']
        fields = entry['fields']

        if entry_type in self.REQUIRED_FIELDS:
            for field in self.REQUIRED_FIELDS[entry_type]:
                if field not in fields or not fields[field]:
                    if field == 'author' and 'editor' in fields: continue
                    issues.append({
                        'key': entry_key,
                        'type': 'missing_field',
                        'field': field,
                        'severity': 'error',
                        'message': f"Missing required field '{field}'"
                    })
        
        # Title case check (simplified)
        if 'title' in fields and re.search(r'\b[A-Z]{2,}\b', fields['title']) and '{' not in fields['title']:
             issues.append({
                'key': entry_key,
                'type': 'caps',
                'severity': 'warning',
                'message': 'Unprotected uppercase in title'
            })

        return issues

    def generate_report(self, result: Dict) -> str:
        lines = []
        lines.append(f"BibTeX Check: {self.bib_file}")
        lines.append(f"Status: {result['status']}")
        
        if result['issues']:
            lines.append("\nIssues:")
            for issue in result['issues']:
                lines.append(f"  [{issue['severity'].upper()}] @{issue['key']}: {issue['message']}")
        
        if result['needs_online_check']:
            lines.append(f"\n[INFO] {len(result['needs_online_check'])} entries missing DOI/URL (Use --online-check to export list)")
            
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='BibTeX Verification')
    parser.add_argument('bib_file', help='.bib file')
    parser.add_argument('--standard', choices=['default', 'gb7714'], default='default')
    parser.add_argument('--online-check', action='store_true', help='Generate list for online verification')
    parser.add_argument('--output', help='Output file for online check JSON')

    args = parser.parse_args()

    if not Path(args.bib_file).exists():
        print("File not found.")
        sys.exit(1)

    verifier = BibTeXVerifier(args.bib_file, args.standard)
    result = verifier.verify()

    if args.online_check:
        output_file = args.output or "verification_needed.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result['needs_online_check'], f, indent=2)
        print(f"Exported {len(result['needs_online_check'])} entries to {output_file}")
        print("Agent instructions: Use 'google_web_search' for these titles to find DOIs.")
    else:
        print(verifier.generate_report(result))
    
    if result['status'] == 'FAIL':
        sys.exit(1)