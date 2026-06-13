#!/usr/bin/env python3
"""
Typst Format Checker - Validate academic paper formatting

Usage:
    uv run python check_format.py main.typ              # Basic check
    uv run python check_format.py main.typ --strict     # Strict mode
    uv run python check_format.py main.typ --venue ieee # Venue-specific check

Checks:
    - Page settings (margins, paper size)
    - Text settings (font, size, language)
    - Heading numbering
    - Figure and table formatting
    - Citation style consistency
    - Math equation formatting
"""

import argparse
import re
import sys
from pathlib import Path

# Universe template imports (e.g. @preview/charged-ieee) and template
# invocations (#show: ieee.with(..)) configure page/columns/font internally, so
# venue layout assertions on the user's own file would be false positives.
TEMPLATE_IMPORT_RE = re.compile(r'#import\s+"@preview/([\w-]+)')
TEMPLATE_SHOW_RE = re.compile(r"#show\s*:\s*[\w.-]+\.with\s*\(")


def _balanced_call_body(content: str, head_re: re.Pattern) -> str:
    """Return the argument body of the first ``call(..)`` whose head matches.

    Used to scope field lookups to the actual ``#set page(..)`` / ``#set
    text(..)`` block instead of a lazy ``[\\s\\S]*?`` that can wander across the
    whole document (T24).
    """
    m = head_re.search(content)
    if not m:
        return ""
    open_idx = content.find("(", m.start())
    if open_idx == -1:
        return ""
    depth = 0
    for i in range(open_idx, len(content)):
        ch = content[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return content[open_idx + 1 : i]
    return content[open_idx + 1 :]


class FormatChecker:
    """Check Typst document formatting for academic papers."""

    def __init__(self, typ_file: str, strict: bool = False, venue: str = None):
        self.typ_file = Path(typ_file)
        self.strict = strict
        self.venue = venue
        self.issues = []
        self.warnings = []
        self.content = ""
        self.uses_template = False

    def load_file(self) -> bool:
        """Load the Typst file."""
        try:
            self.content = self.typ_file.read_text(encoding="utf-8")
            self.uses_template = bool(
                TEMPLATE_IMPORT_RE.search(self.content) or TEMPLATE_SHOW_RE.search(self.content)
            )
            return True
        except Exception as e:
            print(f"[ERROR] Failed to read file: {e}")
            return False

    def check_page_settings(self):
        """Check page configuration."""
        print("\n[CHECK] Page Settings")

        if self.uses_template:
            print("  ℹ Layout (page size / margins / columns) is managed by the template")
            return

        page_body = _balanced_call_body(self.content, re.compile(r"#set\s+page\("))

        # Check paper size
        paper_match = re.search(r'paper:\s*"([^"]+)"', page_body)
        if paper_match:
            paper = paper_match.group(1)
            print(f"  ✓ Paper size: {paper}")
            if self.venue == "ieee" and paper != "us-letter":
                self.warnings.append("IEEE typically uses US Letter paper")
        else:
            self.warnings.append("Paper size not explicitly set")

        # Check margins
        margin_match = re.search(r"margin:\s*([^,)]+)", page_body)
        if margin_match:
            margin = margin_match.group(1)
            print(f"  ✓ Margins: {margin}")
        else:
            self.warnings.append("Margins not explicitly set")

        # Check columns
        columns_match = re.search(r"columns:\s*(\d+)", page_body)
        if columns_match:
            columns = columns_match.group(1)
            print(f"  ✓ Columns: {columns}")
            if self.venue == "ieee" and columns != "2":
                self.issues.append("IEEE requires two-column format")
        else:
            if self.venue in ["ieee", "acm", "cvpr"]:
                self.warnings.append(f"{self.venue.upper()} typically uses two-column format")

    def check_text_settings(self):
        """Check text configuration."""
        print("\n[CHECK] Text Settings")

        if self.uses_template:
            print("  ℹ Text settings (font / size / language) are managed by the template")
            return

        text_body = _balanced_call_body(self.content, re.compile(r"#set\s+text\("))

        # Check font
        font_match = re.search(r'font:\s*"([^"]+)"', text_body)
        if font_match:
            font = font_match.group(1)
            print(f"  ✓ Font: {font}")
            if self.venue == "ieee" and "Times" not in font:
                self.warnings.append("IEEE typically uses Times New Roman")
        else:
            self.warnings.append("Font not explicitly set")

        # Check font size
        size_match = re.search(r"size:\s*(\d+(?:\.\d+)?pt)", text_body)
        if size_match:
            size = size_match.group(1)
            print(f"  ✓ Font size: {size}")
        else:
            self.warnings.append("Font size not explicitly set")

        # Check language
        lang_match = re.search(r'lang:\s*"([^"]+)"', text_body)
        if lang_match:
            lang = lang_match.group(1)
            print(f"  ✓ Language: {lang}")
        else:
            self.warnings.append("Language not explicitly set")

    def check_headings(self):
        """Check heading formatting."""
        print("\n[CHECK] Headings")

        # Check numbering
        numbering_match = re.search(r'#set\s+heading\([\s\S]*?numbering:\s*"([^"]+)"', self.content)
        if numbering_match:
            numbering = numbering_match.group(1)
            print(f"  ✓ Heading numbering: {numbering}")
        else:
            if self.venue not in ["neurips", "icml", "iclr"]:
                self.warnings.append("Heading numbering not set (most venues require it)")

        # Count headings
        headings = re.findall(r"^(=+)\s+(.+)$", self.content, re.MULTILINE)
        if headings:
            print(f"  ✓ Found {len(headings)} headings")
            levels = {len(h[0]) for h in headings}
            print(f"  ✓ Heading levels: {sorted(levels)}")
        else:
            self.warnings.append("No headings found")

    def _figure_blocks(self) -> list[tuple[str, str]]:
        """Return (body, tail) for each ``#figure(..)`` block.

        ``body`` is the balanced argument text (so nested ``image(..)`` parens
        no longer truncate detection); ``tail`` is the text right after the
        closing paren, where Typst attaches the ``<label>`` (T24).
        """
        blocks: list[tuple[str, str]] = []
        for m in re.finditer(r"#figure\(", self.content):
            open_idx = m.end() - 1
            depth = 0
            end_idx = open_idx
            for i in range(open_idx, len(self.content)):
                ch = self.content[i]
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        end_idx = i
                        break
            body = self.content[open_idx + 1 : end_idx]
            tail = self.content[end_idx + 1 : end_idx + 40]
            blocks.append((body, tail))
        return blocks

    def check_figures_tables(self):
        """Check figure and table formatting."""
        print("\n[CHECK] Figures and Tables")

        blocks = self._figure_blocks()
        if blocks:
            print(f"  ✓ Found {len(blocks)} figures/tables")

            # Check for labels (attached after the closing paren).
            labeled = sum(1 for _body, tail in blocks if re.match(r"\s*<[^>]+>", tail))
            print(f"  ✓ Labeled figures/tables: {labeled}")
            if labeled < len(blocks):
                self.warnings.append(f"{len(blocks) - labeled} figures/tables without labels")

            # Check for captions: both content [..] and string ".." forms.
            captioned = sum(
                1 for body, _tail in blocks if re.search(r'caption\s*:\s*(?:\[|")', body)
            )
            print(f"  ✓ Figures/tables with captions: {captioned}")
            if captioned < len(blocks):
                self.warnings.append(f"{len(blocks) - captioned} figures/tables without captions")
        else:
            print("  ℹ No figures or tables found")

    def check_citations(self):
        """Check citation formatting."""
        print("\n[CHECK] Citations")

        # Count citations
        citations = re.findall(r"@\w+", self.content)
        if citations:
            unique_citations = set(citations)
            print(f"  ✓ Found {len(citations)} citations ({len(unique_citations)} unique)")

            # Check for bibliography
            bib_match = re.search(r"#bibliography\(", self.content)
            if bib_match:
                print("  ✓ Bibliography command found")
            else:
                self.issues.append("Citations found but no bibliography command")
        else:
            print("  ℹ No citations found")

    def check_math(self):
        """Check math equation formatting."""
        print("\n[CHECK] Math Equations")

        # Count all math expressions
        all_math = re.findall(r"\$[^$]+\$", self.content)

        # Count display math (has whitespace after opening $ and before closing $)
        display_math = re.findall(r"\$\s+[^$]+\s+\$", self.content)

        # Inline math = total - display
        inline_count = len(all_math) - len(display_math)

        if inline_count > 0:
            print(f"  ✓ Found {inline_count} inline math expressions")

        if display_math:
            print(f"  ✓ Found {len(display_math)} display math expressions")

            # Check for labeled equations
            labeled_equations = re.findall(r"\$\s+[^$]+\s+\$\s*<([^>]+)>", self.content)
            print(f"  ✓ Labeled equations: {len(labeled_equations)}")
            if len(labeled_equations) < len(display_math):
                self.warnings.append(
                    f"{len(display_math) - len(labeled_equations)} display equations without labels"
                )

        if not all_math:
            print("  ℹ No math expressions found")

    def check_venue_specific(self):
        """Check venue-specific requirements."""
        if not self.venue:
            return

        print(f"\n[CHECK] Venue-Specific Requirements ({self.venue.upper()})")

        if self.uses_template:
            print(
                "  ℹ Two-column / paper / numbering requirements are enforced by the "
                f"{self.venue.upper()} template; skipping layout assertions"
            )
            return

        if self.venue == "ieee":
            # IEEE specific checks
            if "columns: 2" not in self.content:
                self.issues.append("IEEE requires two-column format")
            if "us-letter" not in self.content:
                self.warnings.append("IEEE typically uses US Letter paper")

        elif self.venue == "acm":
            # ACM specific checks
            if "columns: 2" not in self.content:
                self.warnings.append("ACM typically uses two-column format")

        elif self.venue in ["neurips", "icml", "iclr"]:
            # ML conference checks
            if "columns: 2" in self.content:
                self.warnings.append(f"{self.venue.upper()} typically uses single-column format")
            if "numbering:" in self.content:
                self.warnings.append(f"{self.venue.upper()} typically doesn't number sections")

    def run_checks(self) -> int:
        """Run all format checks."""
        if not self.load_file():
            return 1

        print(f"[INFO] Checking format for: {self.typ_file}")
        if self.venue:
            print(f"[INFO] Venue: {self.venue.upper()}")
        if self.strict:
            print("[INFO] Strict mode enabled")

        self.check_page_settings()
        self.check_text_settings()
        self.check_headings()
        self.check_figures_tables()
        self.check_citations()
        self.check_math()
        self.check_venue_specific()

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
            return 0 if not self.strict else 1
        else:
            print(f"\n❌ Found {len(self.issues)} critical issues")
            return 1


def main():
    parser = argparse.ArgumentParser(
        description="Typst Format Checker - Validate academic paper formatting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python check_format.py main.typ                # Basic check
  uv run python check_format.py main.typ --strict       # Strict mode (warnings as errors)
  uv run python check_format.py main.typ --venue ieee   # IEEE-specific checks

Supported Venues:
  ieee      IEEE conferences and journals
  acm       ACM conferences and journals
  springer  Springer journals
  neurips   NeurIPS, ICML, ICLR (ML conferences)
  cvpr      CVPR, ICCV, ECCV (CV conferences)
        """,
    )
    parser.add_argument("typ_file", help="Typst file to check")
    parser.add_argument("--strict", "-s", action="store_true", help="Treat warnings as errors")
    parser.add_argument(
        "--venue",
        "-v",
        choices=["ieee", "acm", "springer", "neurips", "cvpr"],
        help="Check venue-specific requirements",
    )

    args = parser.parse_args()

    # Validate input file
    typ_path = Path(args.typ_file)
    if not typ_path.exists():
        print(f"[ERROR] File not found: {args.typ_file}")
        sys.exit(1)

    # Run checks
    checker = FormatChecker(args.typ_file, args.strict, args.venue)
    sys.exit(checker.run_checks())


if __name__ == "__main__":
    main()
