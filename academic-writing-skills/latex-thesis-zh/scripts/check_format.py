#!/usr/bin/env python3
"""
LaTeX Format Checker (Chinese) - chktex wrapper with Chinese support

Usage:
    uv run python check_format.py main.tex
    uv run python check_format.py main.tex --strict
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

try:
    from parsers import get_parser
    from tex_loader import assemble
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import get_parser
    from tex_loader import assemble


class FormatChecker:
    """ChkTeX wrapper with Chinese thesis specific checks."""

    # Chinese-specific checks (in addition to chktex)
    # ``visible_only`` checks run against parser.extract_visible_text() output
    # (math, \cite keys, labels stripped) —— 口语词只在真正的正文中标记。
    CHINESE_CHECKS = {
        "mixed_punctuation": {
            "pattern": r"[一-鿿][,.:;!?]|[,.:;!?][一-鿿]",
            "message": "Mixed Chinese/English punctuation detected",
            "severity": "warning",
            "visible_only": False,
        },
        "missing_space_after_cite": {
            "pattern": r"\\cite\{[^}]+\}[一-鿿]",
            "message": "Missing space after \\cite before Chinese text",
            "severity": "info",
            "visible_only": False,
        },
        # "我们"在 thuthesis 等模板许可的表述里常见，降为 info；
        # 是否改"本文/笔者"取决于院校规范。
        "oral_pronoun": {
            "pattern": r"我们|你们",
            "message": "人称代词（部分院校要求用'本文/笔者'，以本校规范为准）",
            "severity": "info",
            "visible_only": True,
        },
        "oral_vague": {
            "pattern": r"很多|一些|非常|特别",
            "message": "Potential oral expression in academic writing",
            "severity": "warning",
            "visible_only": True,
        },
    }

    _VERBATIM_ENVS = ("verbatim", "lstlisting", "minted")

    def __init__(self, tex_file: str, config: Optional[str] = None):
        self.tex_file = Path(tex_file).resolve()
        self.work_dir = self.tex_file.parent
        self.config = config

    def _check_chktex(self) -> tuple[bool, str]:
        """Check if chktex is available."""
        if shutil.which("chktex"):
            return True, "chktex is available"
        return False, "chktex not found"

    def check(self, strict: bool = False) -> dict:
        """Run format checks including Chinese-specific ones."""
        all_issues = []

        # Run chktex if available (note: chktex only sees the entry file;
        # the Chinese-specific checks below cover the assembled project)
        ok, msg = self._check_chktex()
        if ok:
            chktex_issues = self._run_chktex(strict)
            all_issues.extend(chktex_issues)

        # Run Chinese-specific checks
        chinese_issues, warnings = self._run_chinese_checks()
        all_issues.extend(chinese_issues)

        # info 级提示（如人称代词）不降级状态：仅 warning/error 触发 WARNING
        has_actionable = any(i["severity"] in ("warning", "error") for i in all_issues)
        return {
            "status": "WARNING" if has_actionable else "PASS",
            "chktex_available": ok,
            "issues": all_issues,
            "total": len(all_issues),
            "warnings": warnings,
        }

    def _run_chktex(self, strict: bool) -> list[dict]:
        """Run chktex and parse output."""
        cmd = ["chktex"]
        if strict:
            cmd.extend(["-v3"])
        else:
            cmd.extend(["-v0", "-q"])
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
            return self._parse_chktex_output(result.stdout + result.stderr)
        except Exception:
            return []

    def _parse_chktex_output(self, output: str) -> list[dict]:
        """Parse chktex output."""
        issues = []
        pattern = r"(.+?):(\d+):(\d+):\s*(Warning|Error)\s*(\d+):\s*(.+)"

        for line in output.split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                issues.append(
                    {
                        "source": "chktex",
                        "file": match.group(1),
                        "line": int(match.group(2)),
                        "column": int(match.group(3)),
                        "severity": match.group(4).lower(),
                        "code": int(match.group(5)),
                        "message": match.group(6),
                    }
                )

        return issues

    def _run_chinese_checks(self) -> tuple[list[dict], list[str]]:
        """Run Chinese-specific checks across the assembled project."""
        issues: list[dict] = []

        try:
            doc = assemble(self.tex_file)
        except Exception:
            return issues, []

        lines = doc.lines
        parser = get_parser(self.tex_file)

        # 标记 verbatim/lstlisting/minted 环境内的行（口语检查跳过代码）
        in_verbatim = [False] * len(lines)
        depth = 0
        begin_re = re.compile(r"\\begin\{(?:" + "|".join(self._VERBATIM_ENVS) + r")\*?\}")
        end_re = re.compile(r"\\end\{(?:" + "|".join(self._VERBATIM_ENVS) + r")\*?\}")
        for i, line in enumerate(lines):
            if begin_re.search(line):
                depth += 1
            in_verbatim[i] = depth > 0
            if end_re.search(line) and depth > 0:
                depth -= 1

        for check_name, check_info in self.CHINESE_CHECKS.items():
            pattern = check_info["pattern"]
            visible_only = check_info.get("visible_only", False)

            for i, line in enumerate(lines, 1):
                # Skip comments
                if line.strip().startswith("%"):
                    continue
                if visible_only and in_verbatim[i - 1]:
                    continue

                target = parser.extract_visible_text(line) if visible_only else line
                if not target:
                    continue

                src_file, src_line = doc.origin(i)
                for match in re.finditer(pattern, target):
                    issues.append(
                        {
                            "source": "chinese_check",
                            "file": src_file if doc.multi_file else str(self.tex_file.name),
                            "line": src_line,
                            "column": match.start() + 1,
                            "severity": check_info["severity"],
                            "code": check_name,
                            "message": check_info["message"],
                            "matched": match.group(),
                        }
                    )

        return issues, list(doc.warnings)

    def generate_report(self, result: dict) -> str:
        """Generate human-readable report."""
        lines = []
        lines.append("=" * 60)
        lines.append("LaTeX Format Check Report (Chinese Thesis)")
        lines.append("=" * 60)
        lines.append(f"File: {self.tex_file}")
        lines.append(f"Status: {result['status']}")
        lines.append(f"ChkTeX: {'Available' if result['chktex_available'] else 'Not Available'}")
        lines.append(f"Total Issues: {result['total']}")
        for warn in result.get("warnings", []):
            lines.append(f"WARN: {warn}")

        if result["issues"]:
            lines.append("")
            lines.append("-" * 60)
            lines.append("Issues:")
            lines.append("-" * 60)

            # Group by source
            by_source = {}
            for issue in result["issues"]:
                source = issue["source"]
                if source not in by_source:
                    by_source[source] = []
                by_source[source].append(issue)

            for source, issues in by_source.items():
                lines.append(f"\n[{source.upper()}] ({len(issues)} issues)")
                for issue in issues[:10]:
                    sev = issue["severity"].upper()
                    lines.append(f"  [{sev}] {issue['file']}:{issue['line']}: {issue['message']}")
                if len(issues) > 10:
                    lines.append(f"  ... and {len(issues) - 10} more")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="LaTeX Format Checker (Chinese Thesis)")
    parser.add_argument("tex_file", help=".tex file to check")
    parser.add_argument("--strict", "-s", action="store_true", help="Enable strict checking")
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    if not Path(args.tex_file).exists():
        print(f"[ERROR] File not found: {args.tex_file}")
        sys.exit(1)

    checker = FormatChecker(args.tex_file)
    result = checker.check(strict=args.strict)

    if args.json:
        import json

        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(checker.generate_report(result))

    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
