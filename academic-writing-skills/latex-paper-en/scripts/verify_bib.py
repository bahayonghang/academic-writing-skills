#!/usr/bin/env python3
"""
BibTeX Verification Script - Check bibliography integrity and citation consistency.

Usage:
    python verify_bib.py references.bib
    python verify_bib.py references.bib --tex main.tex
    python verify_bib.py references.bib --standard gb7714
    python verify_bib.py references.bib --online-check --output verification_needed.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from parsers import extract_latex_citation_keys
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import extract_latex_citation_keys


class BibTeXVerifier:
    """Verify BibTeX file integrity and citation consistency."""

    REQUIRED_FIELDS = {
        "article": ["author", "title", "journal", "year"],
        "inproceedings": ["author", "title", "booktitle", "year"],
        "book": ["author", "title", "publisher", "year"],
    }

    GB7714_RECOMMENDED = ["doi", "url", "urldate"]

    def __init__(self, bib_file: str, standard: str = "default", tex_file: str | None = None):
        self.bib_file = Path(bib_file).resolve()
        self.standard = standard
        self.tex_file = Path(tex_file).resolve() if tex_file else None
        self.entries: list[dict] = []
        self.parse_issues: list[dict] = []

    def parse(self) -> list[dict]:
        """Parse BibTeX file into entries."""
        try:
            content = self.bib_file.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            self.parse_issues.append(
                {
                    "severity": "error",
                    "type": "file_error",
                    "message": f"Failed to read BibTeX file: {exc}",
                }
            )
            return []

        entries = []
        seen_keys: dict[str, str] = {}

        # Entry-level extraction (best-effort for common BibTeX files)
        entry_pattern = r"@(\w+)\s*{\s*([^,]+)\s*,([^@]*?)(?=\n\s*@|\Z)"
        for match in re.finditer(entry_pattern, content, re.DOTALL):
            entry_type = match.group(1).lower().strip()
            key = match.group(2).strip()
            fields = self._parse_fields(match.group(3))
            entries.append(
                {"type": entry_type, "key": key, "fields": fields, "raw": match.group(0)}
            )

            key_lower = key.lower()
            if key_lower in seen_keys:
                self.parse_issues.append(
                    {
                        "severity": "error",
                        "type": "duplicate_key",
                        "key": key,
                        "message": f"Duplicate key detected: '{seen_keys[key_lower]}' and '{key}'",
                    }
                )
            else:
                seen_keys[key_lower] = key

        self.entries = entries
        return entries

    def _parse_fields(self, fields_str: str) -> dict[str, str]:
        fields: dict[str, str] = {}
        # Parse field = {value} or "value" or number
        field_pattern = r'(\w+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)"|(\d+))'
        for match in re.finditer(field_pattern, fields_str):
            name = match.group(1).lower()
            val = match.group(2) or match.group(3) or match.group(4) or ""
            fields[name] = val.strip()
        return fields

    def verify(self) -> dict:
        """Run full verification and return structured results."""
        if not self.entries:
            self.parse()

        results: dict[str, object] = {
            "total_entries": len(self.entries),
            "valid_entries": 0,
            "issues": list(self.parse_issues),
            "status": "PASS",
            "needs_online_check": [],
            "missing_in_bib": [],
            "unused_in_tex": [],
        }

        for entry in self.entries:
            entry_issues = self._verify_entry(entry)
            if entry_issues:
                results["issues"].extend(entry_issues)
            else:
                results["valid_entries"] += 1

            # Check for missing identifiers (DOI/URL)
            if "doi" not in entry["fields"] and "url" not in entry["fields"]:
                results["needs_online_check"].append(
                    {
                        "key": entry["key"],
                        "title": entry["fields"].get("title", "Unknown Title"),
                        "author": entry["fields"].get("author", "Unknown Author"),
                    }
                )

            if self.standard == "gb7714":
                self._check_gb7714_recommended(entry, results["issues"])

        if self.tex_file:
            missing_in_bib, unused_in_tex, tex_issues = self._check_citation_consistency()
            results["missing_in_bib"] = sorted(missing_in_bib)
            results["unused_in_tex"] = sorted(unused_in_tex)
            results["issues"].extend(tex_issues)

        if results["issues"]:
            has_error = any(item["severity"] == "error" for item in results["issues"])
            results["status"] = "FAIL" if has_error else "WARNING"

        return results

    def _verify_entry(self, entry: dict) -> list[dict]:
        issues: list[dict] = []
        entry_type = entry["type"]
        entry_key = entry["key"]
        fields = entry["fields"]

        required = self.REQUIRED_FIELDS.get(entry_type, [])
        for field in required:
            if field not in fields or not fields[field]:
                if field == "author" and "editor" in fields:
                    continue
                issues.append(
                    {
                        "key": entry_key,
                        "type": "missing_field",
                        "field": field,
                        "severity": "error",
                        "message": f"Missing required field '{field}'",
                    }
                )

        # Title case check (simplified heuristic)
        title = fields.get("title", "")
        if title and re.search(r"\b[A-Z]{2,}\b", title) and "{" not in title:
            issues.append(
                {
                    "key": entry_key,
                    "type": "caps",
                    "severity": "warning",
                    "message": "Unprotected uppercase in title",
                }
            )

        return issues

    def _check_gb7714_recommended(self, entry: dict, issues: list[dict]) -> None:
        fields = entry["fields"]
        entry_key = entry["key"]
        for field in self.GB7714_RECOMMENDED:
            if field not in fields:
                issues.append(
                    {
                        "key": entry_key,
                        "type": "gb7714_recommended",
                        "field": field,
                        "severity": "warning",
                        "message": f"GB7714 recommends field '{field}'",
                    }
                )

    def _check_citation_consistency(self) -> tuple[set[str], set[str], list[dict]]:
        issues: list[dict] = []
        if not self.tex_file or not self.tex_file.exists():
            msg = (
                f"TeX file not found: {self.tex_file}" if self.tex_file else "TeX file not provided"
            )
            issues.append(
                {
                    "severity": "error",
                    "type": "tex_file_error",
                    "message": msg,
                }
            )
            return set(), set(), issues

        try:
            tex_content = self.tex_file.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            issues.append(
                {
                    "severity": "error",
                    "type": "tex_file_error",
                    "message": f"Failed to read TeX file: {exc}",
                }
            )
            return set(), set(), issues

        cited_keys = extract_latex_citation_keys(tex_content)
        bib_keys = {entry["key"] for entry in self.entries}

        missing_in_bib = cited_keys - bib_keys
        unused_in_tex = bib_keys - cited_keys

        if missing_in_bib:
            issues.append(
                {
                    "severity": "error",
                    "type": "missing_in_bib",
                    "message": f"Citations not found in BibTeX: {', '.join(sorted(missing_in_bib))}",
                }
            )
        if unused_in_tex:
            issues.append(
                {
                    "severity": "warning",
                    "type": "unused_in_tex",
                    "message": f"Unused BibTeX entries: {', '.join(sorted(unused_in_tex))}",
                }
            )

        return missing_in_bib, unused_in_tex, issues

    def generate_report(self, result: dict) -> str:
        lines = []
        lines.append(f"BibTeX Check: {self.bib_file}")
        lines.append(f"Status: {result['status']}")
        lines.append(f"Total entries: {result['total_entries']}")
        lines.append(f"Valid entries: {result['valid_entries']}")

        if self.tex_file:
            lines.append(f"TeX file: {self.tex_file}")
            lines.append(f"missing_in_bib: {len(result['missing_in_bib'])}")
            lines.append(f"unused_in_tex: {len(result['unused_in_tex'])}")

        if result["issues"]:
            lines.append("\nIssues:")
            for issue in result["issues"]:
                key_suffix = f" @{issue['key']}" if issue.get("key") else ""
                lines.append(f"  [{issue['severity'].upper()}]{key_suffix}: {issue['message']}")

        if result["needs_online_check"]:
            lines.append(
                f"\n[INFO] {len(result['needs_online_check'])} entries missing DOI/URL "
                "(Use --online-check to export list)"
            )
            lines.append(
                "[TIP] AI-generated citations have ~40% error rate. "
                "Verify entries without DOI/URL using Semantic Scholar API or CrossRef. "
                "See references/CITATION_VERIFICATION.md for verification workflow."
            )

        if result["missing_in_bib"]:
            lines.append(f"[INFO] missing_in_bib keys: {', '.join(result['missing_in_bib'])}")
        if result["unused_in_tex"]:
            lines.append(f"[INFO] unused_in_tex keys: {', '.join(result['unused_in_tex'])}")

        return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="BibTeX Verification")
    parser.add_argument("bib_file", help=".bib file")
    parser.add_argument("--tex", help="Main .tex file for citation consistency checks")
    parser.add_argument("--standard", choices=["default", "gb7714"], default="default")
    parser.add_argument(
        "--online-check", action="store_true", help="Generate list for online verification"
    )
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument("--json", action="store_true", help="Print full JSON result")

    args = parser.parse_args()

    if not Path(args.bib_file).exists():
        print(f"[ERROR] File not found: {args.bib_file}", file=sys.stderr)
        return 1

    verifier = BibTeXVerifier(args.bib_file, args.standard, args.tex)
    result = verifier.verify()

    if args.online_check:
        output_file = args.output or "verification_needed.json"
        with open(output_file, "w", encoding="utf-8") as handle:
            json.dump(result["needs_online_check"], handle, indent=2, ensure_ascii=False)
        print(f"Exported {len(result['needs_online_check'])} entries to {output_file}")
    elif args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2, ensure_ascii=False)
        print(f"Saved verification result to {args.output}")
    else:
        print(verifier.generate_report(result))

    # Exit policy: PASS/WARNING -> 0, FAIL/error -> 1
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
