#!/usr/bin/env python3
"""
LaTeX Format Checker - chktex wrapper with enhanced reporting

Usage:
    uv run python -B check_format.py main.tex
    uv run python -B check_format.py main.tex --strict
    uv run python -B check_format.py main.tex --config .chktexrc
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


class FormatChecker:
    """ChkTeX wrapper with enhanced error reporting."""

    # Warning levels
    LEVEL_ERROR = "ERROR"
    LEVEL_WARNING = "WARNING"
    LEVEL_INFO = "INFO"

    # chktex warnings grouped by the keyword that appears in their message.
    # The previous integer-range buckets did not match chktex's numbering, so
    # categorize from the message text instead (E26).
    CATEGORY_KEYWORDS = [
        ("spacing", ("space", "spacing", "indent", "tab")),
        ("quotation", ("quote", "``", "''", "quotation")),
        ("parentheses", ("parenthesis", "parentheses", "bracket", "brace")),
        ("punctuation", ("dash", "comma", "period", "punctuation", "hyphen")),
        ("ellipsis", ("ellipsis", "dots", "ldots")),
        ("math", ("math", "equation", "$", "subscript", "superscript")),
    ]

    def __init__(self, tex_file: str, config: Optional[str] = None):
        self.tex_file = Path(tex_file).resolve()
        self.work_dir = self.tex_file.parent
        self.config = config

    def _check_chktex(self) -> tuple[bool, str]:
        """Check if chktex is available."""
        if shutil.which("chktex"):
            return True, "chktex is available"
        return (
            False,
            "chktex not found. Install with: apt-get install chktex (Linux) or via TeX Live/MiKTeX",
        )

    def check(self, strict: bool = False) -> dict:
        """
        Run chktex on the document.

        Args:
            strict: Treat any reported issue as a failure.

        Returns:
            Dict with check results
        """
        ok, msg = self._check_chktex()
        if not ok:
            return {"status": "UNAVAILABLE", "message": msg, "issues": [], "fallback": True}

        # Always use the terse `-v0 -q` format so the output is machine-parseable
        # (`file:line:col:code:message`). `-q` only suppresses the banner; chktex
        # has no "more warnings" verbosity, so strictness is enforced below by
        # failing on any reported issue rather than by changing the format (E1).
        cmd = ["chktex", "-v0", "-q"]

        # Config file
        if self.config:
            cmd.extend(["-l", self.config])

        # Add input file
        cmd.append(str(self.tex_file))

        try:
            result = subprocess.run(
                cmd,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            raw_output = result.stdout + result.stderr
            issues = self._parse_output(raw_output)

            # chktex produced output we could not parse: report an internal error
            # instead of a misleading PASS (E1).
            if raw_output.strip() and not issues:
                return {
                    "status": "ERROR",
                    "message": (
                        "chktex produced output that could not be parsed; "
                        "the format checker may be out of date"
                    ),
                    "issues": [],
                    "fallback": False,
                    "raw_output": raw_output.strip(),
                }

            status = "PASS" if not issues else ("FAIL" if strict else "WARNING")
            return {
                "status": status,
                "message": f"Found {len(issues)} issues",
                "issues": issues,
                "fallback": False,
            }

        except Exception as e:
            return {"status": "ERROR", "message": str(e), "issues": [], "fallback": False}

    def _parse_output(self, output: str) -> list[dict]:
        """Parse chktex ``-v0 -q`` output into structured format.

        The terse format is ``file:line:col:code:message`` with no "Warning"
        keyword. A leading drive letter (``C:/...``) is tolerated because the
        four trailing colon-delimited numeric fields anchor the match (E1).
        """
        issues = []
        pattern = r"^(.+?):(\d+):(\d+):(\d+):\s*(.+)$"

        for line in output.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                code = int(match.group(4))
                issues.append(
                    {
                        "file": match.group(1),
                        "line": int(match.group(2)),
                        "column": int(match.group(3)),
                        "level": self.LEVEL_WARNING,
                        "code": code,
                        "message": match.group(5),
                        "category": self._categorize(match.group(5)),
                    }
                )

        return issues

    def _categorize(self, message: str) -> str:
        """Categorize a warning from keywords in its message (E26)."""
        lowered = message.lower()
        for category, keywords in self.CATEGORY_KEYWORDS:
            if any(keyword in lowered for keyword in keywords):
                return category
        return "other"

    def generate_report(self, result: dict) -> str:
        """Generate human-readable report."""
        lines = []
        lines.append("=" * 60)
        lines.append("LaTeX Format Check Report")
        lines.append("=" * 60)
        lines.append(f"File: {self.tex_file}")
        lines.append(f"Status: {result['status']}")
        lines.append(f"Message: {result['message']}")

        if result.get("fallback"):
            lines.append("")
            lines.append("[FALLBACK MODE] chktex not available")
            lines.append("Install chktex for detailed format checking")
            return "\n".join(lines)

        if result["issues"]:
            lines.append("")
            lines.append("-" * 60)
            lines.append("Issues Found:")
            lines.append("-" * 60)

            # Group by category
            by_category = {}
            for issue in result["issues"]:
                cat = issue["category"]
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(issue)

            for category, issues in sorted(by_category.items()):
                lines.append(f"\n[{category.upper()}] ({len(issues)} issues)")
                for issue in issues[:5]:  # Limit to 5 per category
                    lines.append(f"  Line {issue['line']}: {issue['message']}")
                if len(issues) > 5:
                    lines.append(f"  ... and {len(issues) - 5} more")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="LaTeX Format Checker - chktex wrapper")
    parser.add_argument("tex_file", help=".tex file to check")
    parser.add_argument("--strict", "-s", action="store_true", help="Enable strict checking mode")
    parser.add_argument("--config", "-c", help="Path to .chktexrc config file")
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    # Validate input
    if not Path(args.tex_file).exists():
        print(f"[ERROR] File not found: {args.tex_file}")
        sys.exit(1)

    # Run check
    checker = FormatChecker(args.tex_file, args.config)
    result = checker.check(strict=args.strict)

    # Output
    if args.json:
        import json

        print(json.dumps(result, indent=2))
    else:
        print(checker.generate_report(result))

    # Exit code
    if result["status"] in ("ERROR", "FAIL"):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
