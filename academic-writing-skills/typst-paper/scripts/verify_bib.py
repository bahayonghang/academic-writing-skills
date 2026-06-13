#!/usr/bin/env python3
"""
Bibliography Verification Script for Typst

Usage:
    uv run python verify_bib.py references.bib                    # Check BibTeX file
    uv run python verify_bib.py references.yml                    # Check Hayagriva file
    uv run python verify_bib.py references.bib --typ main.typ     # Check citations
    uv run python verify_bib.py references.bib --style ieee       # Check style

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


class BibChecker:
    """Check bibliography files for Typst documents."""

    # Required fields for common BibTeX entry types
    REQUIRED_FIELDS = {
        "article": ["author", "title", "journal", "year"],
        "book": ["author", "title", "publisher", "year"],
        "inproceedings": ["author", "title", "booktitle", "year"],
        "conference": ["author", "title", "booktitle", "year"],
        "incollection": ["author", "title", "booktitle", "publisher", "year"],
        "phdthesis": ["author", "title", "school", "year"],
        "mastersthesis": ["author", "title", "school", "year"],
        "techreport": ["author", "title", "institution", "year"],
        "misc": ["title"],
    }

    # Required fields for Hayagriva (.yml) entries. Hayagriva models the
    # publication container as a nested ``parent`` entry and uses ``date``
    # rather than ``year``/``journal``; applying the BibTeX table here would
    # flag every well-formed entry, so it gets its own minimal contract.
    HAYAGRIVA_REQUIRED_FIELDS = {
        "article": ["title", "author"],
        "book": ["title", "author"],
        "proceedings": ["title"],
        "thesis": ["title", "author"],
        "report": ["title"],
        "web": ["title"],
        "misc": ["title"],
    }

    # Style-specific author thresholds for et al.
    STYLE_ET_AL_THRESHOLD = {
        "ieee": 6,
        "apa": 20,
        "vancouver": 6,
        "nature": 5,
        "mla": 3,
        "chicago": 10,
    }

    def __init__(
        self,
        bib_file: str,
        typ_file: str = None,
        style: str = None,
        online: bool = False,
        email: str = None,
        online_timeout: float = 10.0,
    ):
        self.bib_file = Path(bib_file)
        self.typ_file = Path(typ_file) if typ_file else None
        self.style = style
        self.entries = {}
        self.issues = []
        self.warnings = []
        self.online = online
        self.email = email
        self.online_timeout = online_timeout
        self.is_hayagriva = False

    @staticmethod
    def _extract_balanced_brace(content: str, start_idx: int) -> str:
        """Extract content within balanced braces starting at start_idx."""
        if start_idx >= len(content) or content[start_idx] != "{":
            return ""
        depth = 0
        for i in range(start_idx, len(content)):
            if content[i] == "{":
                depth += 1
            elif content[i] == "}":
                depth -= 1
                if depth == 0:
                    return content[start_idx + 1 : i]
        return ""

    def load_bibtex(self) -> bool:
        """Load and parse BibTeX file."""
        try:
            content = self.bib_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[ERROR] Failed to read file: {e}")
            return False

        # Find entry starts: @type{key,
        entry_starts = list(re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", content))

        for match in entry_starts:
            entry_type = match.group(1).lower()
            key = match.group(2).strip()

            # Skip @comment, @string, @preamble
            if entry_type in ("comment", "string", "preamble"):
                continue

            # Find the balanced closing brace for this entry
            brace_start = match.start() + content[match.start() :].index("{")
            body = self._extract_balanced_brace(content, brace_start)
            if not body:
                continue

            # Parse fields from body (supports nested braces in values)
            fields = {}
            field_pattern = r'(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|"([^"]*)")'
            for field_match in re.finditer(field_pattern, body, re.DOTALL):
                field_name = field_match.group(1).lower()
                field_value = (field_match.group(2) or field_match.group(3) or "").strip()
                fields[field_name] = field_value

            self.entries[key] = {"type": entry_type, "fields": fields}

        return True

    def load_hayagriva(self) -> bool:
        """Load and parse Hayagriva YAML file."""
        try:
            import yaml
        except ImportError:
            print(
                "[ERROR] PyYAML not installed. Run `uv sync` for project dependencies "
                "or `uv add pyyaml` before checking Hayagriva files."
            )
            return False

        try:
            with open(self.bib_file, encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"[ERROR] Failed to parse YAML: {e}")
            return False

        # Convert Hayagriva format to internal format
        self.is_hayagriva = True
        for key, entry in data.items():
            entry_type = str(entry.get("type", "misc")).lower()
            self.entries[key] = {"type": entry_type, "fields": entry}

        return True

    def check_required_fields(self):
        """Check if all required fields are present."""
        print("\n[CHECK] Required Fields")

        required_table = (
            self.HAYAGRIVA_REQUIRED_FIELDS if self.is_hayagriva else self.REQUIRED_FIELDS
        )
        had_issue = False
        for key, entry in self.entries.items():
            entry_type = entry["type"]
            fields = entry["fields"]

            required = required_table.get(entry_type)
            if required is None and self.is_hayagriva:
                required = ["title"]  # any other Hayagriva type still needs a title
            if required:
                missing = [f for f in required if f not in fields]
                if missing:
                    had_issue = True
                    self.issues.append(
                        f"Entry '{key}' ({entry_type}) missing required fields: "
                        f"{', '.join(missing)}"
                    )

        if not had_issue:
            print(f"  ✓ All {len(self.entries)} entries have required fields")

    def check_duplicates(self):
        """Check for duplicate keys."""
        print("\n[CHECK] Duplicate Keys")

        # BibTeX keys are case-insensitive
        keys_lower = {}
        for key in self.entries:
            key_lower = key.lower()
            if key_lower in keys_lower:
                self.issues.append(
                    f"Duplicate key (case-insensitive): '{keys_lower[key_lower]}' and '{key}'"
                )
            else:
                keys_lower[key_lower] = key

        if not any("Duplicate key" in issue for issue in self.issues):
            print("  ✓ No duplicate keys found")

    def check_citations(self):
        """Check citations in Typst file."""
        if not self.typ_file:
            return

        print("\n[CHECK] Citations")

        try:
            content = self.typ_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[ERROR] Failed to read Typst file: {e}")
            return

        # Find all @key references in the Typst file. Hyphens/colons/dots are
        # valid in keys, so the class must include them (a bare \w would split
        # "harry-potter" into "harry"). A trailing "." is a sentence period, not
        # part of the key.
        all_refs = {r.rstrip(".") for r in re.findall(r"@([A-Za-z][\w:.-]*)", content)}
        # Label definitions <name> are cross-reference targets, not citations.
        label_defs = set(re.findall(r"<([A-Za-z][\w:.-]*)>", content))
        bib_keys = set(self.entries.keys())

        # A reference is a citation when its key exists in the bibliography;
        # this intersection replaces the old, brittle prefix blacklist that
        # silently dropped real keys like @figueroa2021.
        cited = all_refs & bib_keys
        print(f"  ✓ Found {len(cited)} unique citations in Typst file")

        # "Not found" = looks like a citation (no colon, not a defined label)
        # yet absent from the bibliography. Colon-style tokens (@fig:arch) and
        # tokens with a matching <label> are cross-references, not citations.
        missing = {
            r for r in all_refs if r not in bib_keys and r not in label_defs and ":" not in r
        }
        if missing:
            self.issues.append(f"Citations not found in bibliography: {', '.join(sorted(missing))}")
        else:
            print("  ✓ All citations found in bibliography")

        # Check for unused entries
        unused = bib_keys - cited
        if unused:
            self.warnings.append(
                f"{len(unused)} unused entries in bibliography: {', '.join(sorted(list(unused)[:5]))}"
                + (f" and {len(unused) - 5} more" if len(unused) > 5 else "")
            )
        else:
            print("  ✓ All bibliography entries are cited")

    def check_identifiers(self):
        """Check for missing DOI/URL identifiers."""
        missing_id = []
        for key, entry in self.entries.items():
            fields = entry["fields"]
            if "doi" not in fields and "url" not in fields:
                missing_id.append(key)

        if missing_id:
            self.warnings.append(
                f"{len(missing_id)} entries missing DOI/URL: "
                + ", ".join(missing_id[:5])
                + (f" and {len(missing_id) - 5} more" if len(missing_id) > 5 else "")
            )
            self.warnings.append(
                "TIP: AI-generated citations have ~40% error rate. "
                "Verify entries without DOI/URL using Semantic Scholar API. "
                "See references/CITATION_VERIFICATION.md"
            )

    def check_style(self):
        """Check style-specific requirements."""
        if not self.style:
            return

        print(f"\n[CHECK] Style Requirements ({self.style.upper()})")

        for key, entry in self.entries.items():
            fields = entry["fields"]

            # Page format: en dash check (BibTeX convention only; Hayagriva
            # uses structured page-ranges and a different separator policy).
            pages = fields.get("pages", "")
            if not self.is_hayagriva and pages and "-" in pages and "--" not in pages:
                self.warnings.append(
                    f"Entry '{key}': page range uses hyphen '{pages}'. "
                    "Use en dash (--) for page ranges."
                )

            # Author count vs et al. threshold
            author = fields.get("author", "")
            if author:
                author_count = len(re.split(r"\s+and\s+", author))
                threshold = self.STYLE_ET_AL_THRESHOLD.get(self.style, 6)
                if author_count > threshold:
                    self.warnings.append(
                        f"Entry '{key}': {author_count} authors; "
                        f"{self.style.upper()} uses et al. after {threshold}. "
                        "Ensure bibliography style handles truncation."
                    )

            # DOI requirement (IEEE, APA, Nature require it)
            if self.style in ("ieee", "apa"):
                entry_type = entry["type"]
                if "doi" not in fields and entry_type in ("article", "inproceedings"):
                    self.warnings.append(
                        f"Entry '{key}': [{self.style.upper()}] DOI recommended "
                        f"for {entry_type} entries."
                    )

    def check_online(self):
        """Verify entries online via CrossRef/Semantic Scholar."""
        if not self.online:
            return
        try:
            from online_bib_verify import OnlineBibVerifier
        except ImportError:
            print("  [WARNING] online_bib_verify.py not found, skipping online verification")
            return

        print("\n[CHECK] Online Verification")
        verifier = OnlineBibVerifier(
            polite_email=self.email,
            timeout=self.online_timeout,
        )
        verified = 0
        for key, entry in self.entries.items():
            entry_dict = {"key": key, **entry.get("fields", {})}
            result = verifier.verify_entry(entry_dict)
            if result.status == "mismatch":
                for m in result.mismatches:
                    self.issues.append(f"Online mismatch for '{key}': {m}")
            elif result.status == "not_found":
                self.warnings.append(f"Entry '{key}' not found in online databases")
            elif result.status == "verified":
                verified += 1
                if result.suggested_doi:
                    self.warnings.append(
                        f"Entry '{key}': consider adding DOI: {result.suggested_doi}"
                    )
        print(f"  ✓ {verified}/{len(self.entries)} entries verified online")

    def run_checks(self) -> int:
        """Run all checks."""
        print(f"[INFO] Checking bibliography: {self.bib_file}")

        # Load file based on extension
        if self.bib_file.suffix == ".bib":
            if not self.load_bibtex():
                return 1
            print(f"[INFO] Loaded {len(self.entries)} BibTeX entries")
        elif self.bib_file.suffix in [".yml", ".yaml"]:
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
        self.check_identifiers()
        self.check_online()

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
        description="Bibliography Verification Script for Typst",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python verify_bib.py references.bib                    # Check BibTeX file
  uv run python verify_bib.py references.yml                    # Check Hayagriva file
  uv run python verify_bib.py references.bib --typ main.typ     # Check citations
  uv run python verify_bib.py references.bib --style ieee       # Check style

Supported Formats:
  .bib        BibTeX format (traditional)
  .yml/.yaml  Hayagriva format (Typst native)

Supported Styles:
  ieee        IEEE numeric citations
  apa         APA author-year citations
  mla         MLA citations
  chicago     Chicago author-date
  gb-7714-2015-numeric  Chinese national standard (GB/T 7714-2015)
        """,
    )
    parser.add_argument("bib_file", help="Bibliography file to check (.bib or .yml)")
    parser.add_argument("--typ", help="Typst file to check citations against")
    parser.add_argument(
        "--style",
        choices=["ieee", "apa", "mla", "chicago", "gb-7714-2015-numeric"],
        help="Citation style to check",
    )
    parser.add_argument(
        "--online",
        action="store_true",
        help="Enable online verification via CrossRef/Semantic Scholar",
    )
    parser.add_argument("--email", help="Email for CrossRef polite pool (faster rate limits)")
    parser.add_argument(
        "--online-timeout",
        type=float,
        default=10.0,
        help="Timeout per API request in seconds",
    )

    args = parser.parse_args()

    # Validate input file
    bib_path = Path(args.bib_file)
    if not bib_path.exists():
        print(f"[ERROR] File not found: {args.bib_file}")
        sys.exit(1)

    # Run checks
    checker = BibChecker(
        args.bib_file,
        args.typ,
        args.style,
        online=getattr(args, "online", False),
        email=getattr(args, "email", None),
        online_timeout=getattr(args, "online_timeout", 10.0),
    )
    sys.exit(checker.run_checks())


if __name__ == "__main__":
    main()
