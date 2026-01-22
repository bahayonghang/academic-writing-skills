#!/usr/bin/env python3
"""
Bibliography Verification Script for Typst

Usage:
    python verify_bib.py references.bib                    # Check BibTeX file
    python verify_bib.py references.yml                    # Check Hayagriva file
    python verify_bib.py references.bib --typ main.typ     # Check citations
    python verify_bib.py references.bib --style ieee       # Check style

Checks:
    - Required fields for each entry type
    - Duplicate keys
    - Unused entries (when --typ is provided)
    - Missing citations (when --typ is provided)
    - Format consistency
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set


class BibChecker:
    """Check bibliography files for Typst documents."""

    # Required fields for common BibTeX entry types
    REQUIRED_FIELDS = {
        'article': ['author', 'title', 'journal', 'year'],
        'book': ['author', 'title', 'publisher', 'year'],
        'inproceedings': ['author', 'title', 'booktitle', 'year'],
        'conference': ['author', 'title', 'booktitle', 'year'],
        'incollection': ['author', 'title', 'booktitle', 'publisher', 'year'],
        'phdthesis': ['author', 'title', 'school', 'year'],
        'mastersthesis': ['author', 'title', 'school', 'year'],
        'techreport': ['author', 'title', 'institution', 'year'],
        'misc': ['title'],
    }

    def __init__(self, bib_file: str, typ_file: str = None, style: str = None):
        self.bib_file = Path(bib_file)
        self.typ_file = Path(typ_file) if typ_file else None
        self.style = style
        self.entries = {}
        self.issues = []
        self.warnings = []

    def load_bibtex(self) -> bool:
        """Load and parse BibTeX file."""
        try:
            content = self.bib_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"[ERROR] Failed to read file: {e}")
            return False

        # Parse BibTeX entries
        entry_pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,([^}]+)\}'
        matches = re.finditer(entry_pattern, content, re.DOTALL)

        for match in matches:
            entry_type = match.group(1).lower()
            key = match.group(2).strip()
            fields_str = match.group(3)

            # Parse fields
            fields = {}
            field_pattern = r'(\w+)\s*=\s*[{"](.*?)[}"]'
            for field_match in re.finditer(field_pattern, fields_str, re.DOTALL):
                field_name = field_match.group(1).lower()
                field_value = field_match.group(2).strip()
                fields[field_name] = field_value

            self.entries[key] = {
                'type': entry_type,
                'fields': fields
            }

        return True

    def load_hayagriva(self) -> bool:
        """Load and parse Hayagriva YAML file."""
        try:
            import yaml
        except ImportError:
            print("[ERROR] PyYAML not installed. Install with: pip install pyyaml")
            return False

        try:
            with open(self.bib_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"[ERROR] Failed to parse YAML: {e}")
            return False

        # Convert Hayagriva format to internal format
        for key, entry in data.items():
            entry_type = entry.get('type', 'misc')
            self.entries[key] = {
                'type': entry_type,
                'fields': entry
            }

        return True

    def check_required_fields(self):
        """Check if all required fields are present."""
        print("\n[CHECK] Required Fields")

        for key, entry in self.entries.items():
            entry_type = entry['type']
            fields = entry['fields']

            if entry_type in self.REQUIRED_FIELDS:
                required = self.REQUIRED_FIELDS[entry_type]
                missing = [f for f in required if f not in fields]

                if missing:
                    self.issues.append(
                        f"Entry '{key}' ({entry_type}) missing required fields: {', '.join(missing)}"
                    )

        if not self.issues:
            print(f"  ✓ All {len(self.entries)} entries have required fields")

    def check_duplicates(self):
        """Check for duplicate keys."""
        print("\n[CHECK] Duplicate Keys")

        # BibTeX keys are case-insensitive
        keys_lower = {}
        for key in self.entries.keys():
            key_lower = key.lower()
            if key_lower in keys_lower:
                self.issues.append(
                    f"Duplicate key (case-insensitive): '{keys_lower[key_lower]}' and '{key}'"
                )
            else:
                keys_lower[key_lower] = key

        if not any('Duplicate key' in issue for issue in self.issues):
            print(f"  ✓ No duplicate keys found")

    def check_citations(self):
        """Check citations in Typst file."""
        if not self.typ_file:
            return

        print("\n[CHECK] Citations")

        try:
            content = self.typ_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"[ERROR] Failed to read Typst file: {e}")
            return

        # Find all citations in Typst file
        citations = set(re.findall(r'@(\w+)', content))

        # Remove special Typst references (figures, tables, etc.)
        citations = {c for c in citations if not c.startswith(('fig:', 'tab:', 'eq:', 'sec:'))}

        print(f"  ✓ Found {len(citations)} unique citations in Typst file")

        # Check for missing entries
        missing = citations - set(self.entries.keys())
        if missing:
            self.issues.append(
                f"Citations not found in bibliography: {', '.join(sorted(missing))}"
            )
        else:
            print(f"  ✓ All citations found in bibliography")

        # Check for unused entries
        unused = set(self.entries.keys()) - citations
        if unused:
            self.warnings.append(
                f"{len(unused)} unused entries in bibliography: {', '.join(sorted(list(unused)[:5]))}"
                + (f" and {len(unused) - 5} more" if len(unused) > 5 else "")
            )
        else:
            print(f"  ✓ All bibliography entries are cited")

    def check_style(self):
        """Check style-specific requirements."""
        if not self.style:
            return

        print(f"\n[CHECK] Style Requirements ({self.style.upper()})")

        if self.style == 'ieee':
            # IEEE typically uses numeric citations
            print("  ℹ IEEE uses numeric citations [1], [2], etc.")

        elif self.style == 'apa':
            # APA uses author-year citations
            print("  ℹ APA uses author-year citations (Smith, 2020)")

        elif self.style == 'gb-7714-2015':
            # Chinese national standard
            print("  ℹ GB/T 7714-2015 is the Chinese national standard")
            # Check for Chinese characters in titles
            chinese_entries = []
            for key, entry in self.entries.items():
                title = entry['fields'].get('title', '')
                if re.search(r'[\u4e00-\u9fff]', title):
                    chinese_entries.append(key)
            if chinese_entries:
                print(f"  ✓ Found {len(chinese_entries)} entries with Chinese titles")

    def run_checks(self) -> int:
        """Run all checks."""
        print(f"[INFO] Checking bibliography: {self.bib_file}")

        # Load file based on extension
        if self.bib_file.suffix == '.bib':
            if not self.load_bibtex():
                return 1
            print(f"[INFO] Loaded {len(self.entries)} BibTeX entries")
        elif self.bib_file.suffix in ['.yml', '.yaml']:
            if not self.load_hayagriva():
                return 1
            print(f"[INFO] Loaded {len(self.entries)} Hayagriva entries")
        else:
            print(f"[ERROR] Unsupported file format: {self.bib_file.suffix}")
            print("[INFO] Supported formats: .bib (BibTeX), .yml/.yaml (Hayagriva)")
            return 1

        # Run checks
        self.check_required_fields()
        self.check_duplicates()
        self.check_citations()
        self.check_style()

        # Print summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)

        if self.issues:
            print(f"\n❌ ISSUES ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  - {issue}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.issues and not self.warnings:
            print("\n✅ All checks passed!")
            return 0
        elif not self.issues:
            print("\n✅ No critical issues found")
            return 0
        else:
            print(f"\n❌ Found {len(self.issues)} critical issues")
            return 1


def main():
    parser = argparse.ArgumentParser(
        description='Bibliography Verification Script for Typst',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python verify_bib.py references.bib                    # Check BibTeX file
  python verify_bib.py references.yml                    # Check Hayagriva file
  python verify_bib.py references.bib --typ main.typ     # Check citations
  python verify_bib.py references.bib --style ieee       # Check style

Supported Formats:
  .bib        BibTeX format (traditional)
  .yml/.yaml  Hayagriva format (Typst native)

Supported Styles:
  ieee        IEEE numeric citations
  apa         APA author-year citations
  mla         MLA citations
  chicago     Chicago author-date
  gb-7714-2015  Chinese national standard
        """
    )
    parser.add_argument('bib_file', help='Bibliography file to check (.bib or .yml)')
    parser.add_argument(
        '--typ',
        help='Typst file to check citations against'
    )
    parser.add_argument(
        '--style',
        choices=['ieee', 'apa', 'mla', 'chicago', 'gb-7714-2015'],
        help='Citation style to check'
    )

    args = parser.parse_args()

    # Validate input file
    bib_path = Path(args.bib_file)
    if not bib_path.exists():
        print(f"[ERROR] File not found: {args.bib_file}")
        sys.exit(1)

    # Run checks
    checker = BibChecker(args.bib_file, args.typ, args.style)
    sys.exit(checker.run_checks())


if __name__ == '__main__':
    main()
