#!/usr/bin/env python3
"""
Table Structure Checker - Validate three-line table compliance in LaTeX documents.

Usage:
    uv run python -B check_tables.py main.tex
    uv run python -B check_tables.py main.tex --fix-suggestions
    uv run python -B check_tables.py main.tex --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from tex_loader import assemble
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from tex_loader import assemble


CAPTION_RE = re.compile(r"\\(?:bi)?caption\b\s*(?:\[[^\]]*\]\s*)?\{")
SCHOOL_CHOICES = ("yanshan-ee-2025", "generic")
_COLLEGE_SCHOOL = "yanshan-ee-2025"
_CJK_END_PUNCT = "。！？；，、："
_UNIT_WORDS = (
    "kg|mg|g|t|km|cm|mm|nm|m|s|ms|ns|h|min|Hz|kHz|MHz|GHz|"
    "Pa|kPa|MPa|GPa|N|J|kJ|W|kW|MW|V|kV|A|mA|K|mol|L|mL|dB|bit|B|KB|MB|GB|TB"
)
_CELL_UNIT_RE = re.compile(
    rf"(-?(?:\d+(?:\.\d+)?))\s*(?:~|\\,)?\s*(\\%|%|℃|(?:{_UNIT_WORDS}))(?![A-Za-z])"
)
_CAPTION_CMD_RE = re.compile(r"\\(caption|bicaption)\b")


class TableChecker:
    """Validate LaTeX tables against the three-line (booktabs) standard."""

    LEVEL_ERROR = "ERROR"
    LEVEL_WARNING = "WARNING"
    LEVEL_INFO = "INFO"

    # Booktabs commands that define valid three-line rules
    VALID_RULES = {r"\toprule", r"\midrule", r"\bottomrule"}

    # Forbidden rule commands inside tabular body
    FORBIDDEN_RULES = {r"\hline", r"\vline", r"\cline"}

    def __init__(self, tex_file: str, school: str = "generic"):
        self.tex_file = Path(tex_file).resolve()
        self.content = ""
        self.lines: list[str] = []
        self.issues: list[dict] = []
        self.doc = None
        self.school = school

    def _load(self) -> bool:
        """Load the .tex file content (assembling \\include'd chapters)."""
        if not self.tex_file.exists():
            self.issues.append(
                {
                    "line": 0,
                    "level": self.LEVEL_ERROR,
                    "priority": "P1",
                    "message": f"File not found: {self.tex_file}",
                    "category": "file",
                }
            )
            return False
        self.doc = assemble(self.tex_file)
        self.content = self.doc.content
        self.lines = self.doc.lines
        return True

    def check(self, fix_suggestions: bool = False) -> dict:
        """Run all table structure checks."""
        if not self._load():
            return self._result()

        self._check_booktabs_loaded()
        tables = self._find_table_environments()

        for table in tables:
            self._check_vertical_lines(table)
            self._check_rule_commands(table)
            self._check_caption_position(table)
            self._check_table_notes(table)
            self._check_number_precision(table)
            if self.school == _COLLEGE_SCHOOL:
                self._check_college_table(table)
        if self.school == _COLLEGE_SCHOOL:
            self._check_college_unscanned_floats()

        if fix_suggestions:
            for issue in self.issues:
                issue["fix"] = self._suggest_fix(issue)

        return self._result()

    def _result(self) -> dict:
        """Build result dictionary."""
        if not self.issues:
            status = "PASS"
        elif any(i["level"] == self.LEVEL_ERROR for i in self.issues):
            status = "FAIL"
        else:
            status = "WARNING"

        # Map assembled line numbers back to 源文件:行号 (idempotent via flag)
        if self.doc is not None and self.doc.multi_file:
            for issue in self.issues:
                if issue.get("line") and not issue.get("file"):
                    src, src_line = self.doc.origin(issue["line"])
                    issue["file"] = src
                    issue["line"] = src_line

        return {
            "status": status,
            "file": str(self.tex_file),
            "table_count": len(self._find_table_environments()),
            "issue_count": len(self.issues),
            "issues": self.issues,
            "warnings": list(self.doc.warnings) if self.doc is not None else [],
        }

    def _check_booktabs_loaded(self) -> None:
        """Check if booktabs package is loaded."""
        has_booktabs = False
        for line in self.lines:
            stripped = line.split("%")[0]  # Ignore comments
            if re.search(r"\\usepackage(\[[^\]]*\])?\{.*booktabs.*\}", stripped):
                has_booktabs = True
                break
        if not has_booktabs and re.search(r"\\begin\{table\*?\}", self.content):
            self.issues.append(
                {
                    "line": 0,
                    "level": self.LEVEL_WARNING,
                    "priority": "P2",
                    "message": "booktabs package not loaded. Add \\usepackage{booktabs} for professional three-line tables.",
                    "category": "package",
                }
            )

    def _find_table_environments(self) -> list[dict]:
        """Find all table/table* environments with their line ranges."""
        tables = []
        pattern = re.compile(r"\\begin\{(table\*?)\}")
        end_pattern = re.compile(r"\\end\{(table\*?)\}")

        stack: list[dict] = []
        for i, line in enumerate(self.lines, 1):
            stripped = line.split("%")[0]
            for m in pattern.finditer(stripped):
                stack.append({"env": m.group(1), "start": i, "start_col": m.start()})
            for _m in end_pattern.finditer(stripped):
                if stack:
                    entry = stack.pop()
                    entry["end"] = i
                    entry["content"] = "\n".join(self.lines[entry["start"] - 1 : i])
                    tables.append(entry)

        return tables

    def _check_vertical_lines(self, table: dict) -> None:
        """Check for vertical lines in column specifications."""
        content = table["content"]
        # Find tabular column spec: \begin{tabular}{|c|c|c|}
        col_specs = re.findall(r"\\begin\{tabular\*?\}(?:\{[^}]*\})?\{([^}]+)\}", content)
        for spec in col_specs:
            if "|" in spec:
                self.issues.append(
                    {
                        "line": table["start"],
                        "level": self.LEVEL_ERROR,
                        "priority": "P1",
                        "message": f"Vertical lines detected in column spec: {{{spec}}}. Three-line tables must not have vertical lines.",
                        "category": "vertical_lines",
                    }
                )

        # Also check for \vline
        for i, line in enumerate(self.lines[table["start"] - 1 : table["end"]], table["start"]):
            stripped = line.split("%")[0]
            if r"\vline" in stripped:
                self.issues.append(
                    {
                        "line": i,
                        "level": self.LEVEL_ERROR,
                        "priority": "P1",
                        "message": "\\vline detected. Three-line tables must not have vertical lines.",
                        "category": "vertical_lines",
                    }
                )

    def _check_rule_commands(self, table: dict) -> None:
        """Check for correct rule commands (booktabs vs hline)."""
        content = table["content"]

        # Find tabular body
        tabular_match = re.search(
            r"\\begin\{tabular\*?\}(?:\{[^}]*\})?\{[^}]+\}(.*?)\\end\{tabular\*?\}",
            content,
            re.DOTALL,
        )
        if not tabular_match:
            return

        tabular_body = tabular_match.group(1)

        # Count booktabs rules
        toprule_count = len(re.findall(r"\\toprule", tabular_body))
        midrule_count = len(re.findall(r"\\midrule", tabular_body))
        bottomrule_count = len(re.findall(r"\\bottomrule", tabular_body))

        # Check for forbidden rules
        for i, line in enumerate(self.lines[table["start"] - 1 : table["end"]], table["start"]):
            stripped = line.split("%")[0]
            if r"\hline" in stripped:
                self.issues.append(
                    {
                        "line": i,
                        "level": self.LEVEL_WARNING,
                        "priority": "P1",
                        "message": "\\hline detected. Use \\toprule, \\midrule, \\bottomrule (booktabs) instead.",
                        "category": "hline",
                    }
                )
            if re.search(r"\\cline\{[^}]+\}", stripped):
                self.issues.append(
                    {
                        "line": i,
                        "level": self.LEVEL_INFO,
                        "priority": "P3",
                        "message": "\\cline detected. Consider \\cmidrule (booktabs) for partial rules under sub-headers.",
                        "category": "hline",
                    }
                )

        # Validate three-line structure
        if toprule_count == 0 and midrule_count == 0 and bottomrule_count == 0:
            # No booktabs at all — check if using hline
            hline_count = len(re.findall(r"\\hline", tabular_body))
            if hline_count > 0:
                self.issues.append(
                    {
                        "line": table["start"],
                        "level": self.LEVEL_WARNING,
                        "priority": "P1",
                        "message": f"Table uses \\hline ({hline_count}x) instead of booktabs commands. Replace with \\toprule/\\midrule/\\bottomrule.",
                        "category": "booktabs_missing",
                    }
                )
        else:
            if toprule_count != 1:
                self.issues.append(
                    {
                        "line": table["start"],
                        "level": self.LEVEL_WARNING,
                        "priority": "P2",
                        "message": f"Expected exactly 1 \\toprule, found {toprule_count}.",
                        "category": "rule_count",
                    }
                )
            if bottomrule_count != 1:
                self.issues.append(
                    {
                        "line": table["start"],
                        "level": self.LEVEL_WARNING,
                        "priority": "P2",
                        "message": f"Expected exactly 1 \\bottomrule, found {bottomrule_count}.",
                        "category": "rule_count",
                    }
                )

    def _check_caption_position(self, table: dict) -> None:
        """Check that caption appears before tabular environment."""
        content = "\n".join(
            re.sub(r"(?<!\\)%.*", "", line) for line in table["content"].splitlines()
        )

        caption_pos = -1
        tabular_pos = -1

        caption_match = CAPTION_RE.search(content)
        tabular_match = re.search(r"\\begin\{tabular\*?\}", content)

        if caption_match:
            caption_pos = caption_match.start()
        if tabular_match:
            tabular_pos = tabular_match.start()

        if caption_pos < 0:
            self.issues.append(
                {
                    "line": table["start"],
                    "level": self.LEVEL_WARNING,
                    "priority": "P2",
                    "message": "No \\caption found in table environment.",
                    "category": "caption",
                }
            )
        elif tabular_pos >= 0 and caption_pos > tabular_pos:
            self.issues.append(
                {
                    "line": table["start"],
                    "level": self.LEVEL_WARNING,
                    "priority": "P2",
                    "message": "Caption should appear above the table (before \\begin{tabular}), not below.",
                    "category": "caption_position",
                }
            )

    def _check_table_notes(self, table: dict) -> None:
        """Check table note format if present."""
        content = table["content"]

        # Look for common note patterns
        has_note = False
        if re.search(r"\\item\s+Note\.", content):
            has_note = True
        if re.search(r"\\item\s+注[：:]", content):
            has_note = True
        if re.search(r"\\footnotesize\s*Note\.", content):
            has_note = True
        if re.search(r"\\footnotesize\s*注[：:]", content):
            has_note = True

        # Check if there are significance markers but no note explaining them
        if (
            re.search(r"\*\*?\*?", content)
            and not has_note
            and re.search(r"\d+\.?\d*\s*\*{1,3}", content)
        ):
            self.issues.append(
                {
                    "line": table["start"],
                    "level": self.LEVEL_INFO,
                    "priority": "P3",
                    "message": "Statistical significance markers (*/**/ ***) detected but no table note defining them. Add a note: 'Note. * p<0.05; ** p<0.01; *** p<0.001.'",
                    "category": "table_note",
                }
            )

    def _check_number_precision(self, table: dict) -> None:
        """Check for inconsistent decimal precision within columns."""
        content = table["content"]

        # Extract data rows (lines between \midrule and \bottomrule)
        data_match = re.search(r"\\midrule(.*?)\\bottomrule", content, re.DOTALL)
        if not data_match:
            return

        data_section = data_match.group(1)
        rows = [r.strip() for r in data_section.split(r"\\") if r.strip()]

        if len(rows) < 2:
            return

        # Parse columns
        parsed_rows = []
        for row in rows:
            # Remove LaTeX commands for analysis
            cleaned = re.sub(r"\\textbf\{([^}]*)\}", r"\1", row)
            cleaned = re.sub(r"\\bfseries\s*", "", cleaned)
            cleaned = re.sub(r"\$[^$]*\$", "", cleaned)
            cells = [c.strip() for c in cleaned.split("&")]
            parsed_rows.append(cells)

        if not parsed_rows:
            return

        # Check each column for precision consistency
        n_cols = max(len(r) for r in parsed_rows)
        for col_idx in range(n_cols):
            decimals_seen: set[int] = set()
            for row in parsed_rows:
                if col_idx < len(row):
                    cell = row[col_idx].strip().rstrip("*")
                    # Extract numbers
                    nums = re.findall(r"\d+\.(\d+)", cell)
                    for n in nums:
                        decimals_seen.add(len(n))

            if len(decimals_seen) > 1:
                self.issues.append(
                    {
                        "line": table["start"],
                        "level": self.LEVEL_WARNING,
                        "priority": "P3",
                        "message": f"Inconsistent decimal precision in column {col_idx + 1}: found {sorted(decimals_seen)} decimal places. Use consistent precision within each column.",
                        "category": "precision",
                    }
                )

    def _suggest_fix(self, issue: dict) -> str:
        """Generate fix suggestion for an issue."""
        cat = issue.get("category", "")
        if cat == "vertical_lines":
            return "Remove all | characters from the column specification."
        if cat == "hline":
            return "Replace \\hline with \\toprule (first), \\midrule (after header), \\bottomrule (last)."
        if cat == "booktabs_missing":
            return "Add \\usepackage{booktabs} and replace \\hline with \\toprule/\\midrule/\\bottomrule."
        if cat == "caption_position":
            return "Move \\caption{...} before \\begin{tabular}."
        if cat == "precision":
            return "Align all values in the column to the same number of decimal places."
        if cat == "package":
            return "Add \\usepackage{booktabs} to the preamble."
        return ""

    def _college_issue(self, line: int, code: str, detail: str) -> None:
        self.issues.append(
            {
                "line": line,
                "level": self.LEVEL_INFO,
                "priority": "P3",
                "message": f"[Script] Meaning-Check: NEEDS-LLM {code}: {detail}",
                "category": code.lower().replace("-", "_"),
                "code": code,
                "meaning_check": "NEEDS-LLM",
                "layer": "[Script]",
            }
        )

    def _college_unscanned(self, line: int, kind: str) -> None:
        self._college_issue(
            line,
            "TB-COVERAGE",
            f"{kind} 浮动体未做同上/同左、同单位表头和题注标点扫描，覆盖不足，不作为通过",
        )

    def _check_college_unscanned_floats(self) -> None:
        pattern = re.compile(r"\\begin\{(longtable|sidewaystable)\*?\}")
        for i, line in enumerate(self.lines, 1):
            stripped = re.sub(r"(?<!\\)%.*", "", line)
            for match in pattern.finditer(stripped):
                self._college_unscanned(i, match.group(1))

    def _check_college_table(self, table: dict) -> None:
        content = "\n".join(
            re.sub(r"(?<!\\)%.*", "", line) for line in table["content"].splitlines()
        )
        if re.search(r"\\begin\{tabularx\*?\}", content):
            self._college_unscanned(table["start"], "tabularx")
            return
        if len(re.findall(r"\\begin\{tabular\*?\}", content)) > 1:
            self._college_unscanned(table["start"], "多个 tabular")
            return
        self._check_caption_punct(content, table["start"])
        body = _tabular_body(content)
        if body is None:
            return
        same = re.search(r"同上|同左", body)
        if same:
            located = content.find(body)
            same_at = located + same.start() if located >= 0 else 0
            self._college_issue(
                table["start"] + content.count("\n", 0, same_at),
                "TB-SAMEAS",
                "表身出现「同上」或「同左」。题注和表注不在此项内，不提供整句替换",
            )
        if re.search(r"\\(?:multicolumn|multirow)\b|\\begin\{tabular", body):
            self._college_issue(
                table["start"],
                "TB-COVERAGE",
                "multicolumn、multirow 或嵌套表导致列归属不明，不合并命中，不作为通过",
            )
            return
        self._check_unit_header(body, table["start"])

    def _check_caption_punct(self, content: str, table_start: int) -> None:
        for match in _CAPTION_CMD_RE.finditer(content):
            status, chinese = _chinese_caption_arg(content, match.start(), match.group(1))
            line = table_start + content.count("\n", 0, match.start())
            if status != "ok":
                self._college_issue(
                    line,
                    "CAP-COVERAGE",
                    "无法确认中文题注主参数，留人工，不作为通过",
                )
                continue
            visible = _caption_visible(chinese or "")
            if visible and visible[-1] in _CJK_END_PUNCT:
                self._college_issue(
                    line,
                    "CAP-PUNCT",
                    "中文题注可见正文以中文标点结束。英文句点、可选短题注和"
                    " \\bicaption 第二参数不计",
                )

    def _check_unit_header(self, body: str, line: int) -> None:
        rows = _table_rows(body)
        if rows is None:
            self._college_issue(
                line,
                "TB-COVERAGE",
                "简单表列数不一致，列归属不明，不作为通过",
            )
            return
        header, data = rows
        if not header or len(data) < 3:
            return
        width = len(header)
        if any(len(row) != width for row in data):
            self._college_issue(line, "TB-COVERAGE", "表列数不一致，列归属不明，不作为通过")
            return
        for col in range(width):
            units = []
            for row in data:
                found = _literal_unit(row[col])
                if found:
                    units.append(found)
            if len(units) < 3 or len(set(units)) != 1:
                continue
            unit = units[0]
            if not _header_has_unit(header[col], unit):
                self._college_issue(
                    line,
                    "TB-UNITHEAD",
                    f"第 {col + 1} 列至少 3 个数值行使用字面单位 {unit}，表头未见该单位。"
                    "不换算单位，不改写单元格",
                )

    def generate_report(self, result: dict) -> str:
        """Generate human-readable report."""
        lines = []
        lines.append("=" * 60)
        lines.append("Table Structure Check Report")
        lines.append("=" * 60)
        lines.append(f"File: {result['file']}")
        lines.append(f"Tables found: {result['table_count']}")
        lines.append(f"Status: {result['status']}")
        lines.append(f"Issues: {result['issue_count']}")
        for warn in result.get("warnings", []):
            lines.append(f"WARN: {warn}")

        if result["issues"]:
            lines.append("")
            lines.append("-" * 60)

            by_category: dict[str, list[dict]] = {}
            for issue in result["issues"]:
                cat = issue.get("category", "other")
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(issue)

            for category, issues in sorted(by_category.items()):
                lines.append(f"\n[{category.upper()}] ({len(issues)} issues)")
                for issue in issues:
                    if issue.get("file"):
                        prefix = f"  {issue['file']}:{issue['line']}"
                    elif issue["line"]:
                        prefix = f"  Line {issue['line']}"
                    else:
                        prefix = "  Global"
                    lines.append(f"{prefix}: [{issue['level']}] {issue['message']}")
                    if issue.get("fix"):
                        lines.append(f"    Fix: {issue['fix']}")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Table Structure Checker - three-line table compliance"
    )
    parser.add_argument("tex_file", help=".tex file to check")
    parser.add_argument(
        "--fix-suggestions", "-f", action="store_true", help="Include fix suggestions"
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")
    parser.add_argument(
        "--school",
        choices=SCHOOL_CHOICES,
        default="generic",
        help="学院源码体例。仅 yanshan-ee-2025 启用表身/题注候选；默认 generic",
    )

    args = parser.parse_args()

    if not Path(args.tex_file).exists():
        print(f"[ERROR] File not found: {args.tex_file}")
        sys.exit(1)

    checker = TableChecker(args.tex_file, school=args.school)
    result = checker.check(fix_suggestions=args.fix_suggestions)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(checker.generate_report(result))

    sys.exit(1 if result["status"] == "FAIL" else 0)


def _tabular_body(content: str) -> str | None:
    match = re.search(r"\\begin\{tabular\*?\}", content)
    if not match:
        return None
    index = _skip_ws(content, match.end())
    if index < len(content) and content[index] == "[":
        group = _read_group(content, index, "[", "]")
        if group is None:
            return None
        _, index = group
    seen = 0
    while seen < 2:
        index = _skip_ws(content, index)
        if index >= len(content) or content[index] != "{":
            break
        group = _read_group(content, index, "{", "}")
        if group is None:
            return None
        _, index = group
        seen += 1
    end = re.search(r"\\end\{tabular\*?\}", content[index:])
    if not end:
        return None
    return content[index : index + end.start()]


def _table_rows(body: str) -> tuple[list[str], list[list[str]]] | None:
    if "\\midrule" in body:
        header_text, _, data_text = body.partition("\\midrule")
        data_text = data_text.split("\\bottomrule")[0]
    else:
        parts = _split_rows(body)
        if len(parts) < 2:
            return [], []
        header_text, data_text = parts[0], "\\\\".join(parts[1:])
    header = _split_rows(header_text)
    header_cells = _cells(header[-1]) if header else []
    data_rows = [_cells(row) for row in _split_rows(data_text)]
    return header_cells, data_rows


def _split_rows(text: str) -> list[str]:
    rows = []
    for row in re.split(r"\\\\", text):
        cleaned = re.sub(r"\\(?:toprule|midrule|bottomrule|hline|cmidrule\{[^{}]*\})", "", row)
        if cleaned.strip():
            rows.append(cleaned)
    return rows


def _cells(row: str) -> list[str]:
    return [cell.strip() for cell in row.split("&")]


def _literal_unit(cell: str) -> str:
    cleaned = re.sub(r"\\(?:textbf|mathrm|text)\{([^{}]*)\}", r"\1", cell)
    if cleaned.strip() in {"", "-", "--", "---", "—", "–"}:
        return ""
    match = _CELL_UNIT_RE.search(cleaned)
    return match.group(2) if match else ""


def _header_has_unit(header: str, unit: str) -> bool:
    if unit in {"%", "\\%", "℃"}:
        return unit in header
    return re.search(rf"(?<![A-Za-z0-9]){re.escape(unit)}(?![A-Za-z0-9])", header) is not None


def _chinese_caption_arg(text: str, start: int, command: str) -> tuple[str, str | None]:
    index = start + len(command) + 1
    index = _skip_ws(text, index)
    if index < len(text) and text[index] == "*":
        index = _skip_ws(text, index + 1)
    limit = 2 if command == "bicaption" else 1
    for _ in range(limit):
        if index < len(text) and text[index] == "[":
            group = _read_group(text, index, "[", "]")
            if group is None:
                return "manual", None
            _, index = group
            index = _skip_ws(text, index)
        else:
            break
    if index >= len(text) or text[index] != "{":
        return "manual", None
    group = _read_group(text, index, "{", "}")
    if group is None:
        return "manual", None
    return "ok", group[0]


def _skip_ws(text: str, index: int) -> int:
    while index < len(text) and text[index] in " \t\r\n":
        index += 1
    return index


def _read_group(text: str, index: int, open_ch: str, close_ch: str) -> tuple[str, int] | None:
    if index >= len(text) or text[index] != open_ch:
        return None
    depth = 1
    cursor = index + 1
    while cursor < len(text):
        if text[cursor] == "\\" and cursor + 1 < len(text):
            cursor += 2
            continue
        if text[cursor] == open_ch:
            depth += 1
        elif text[cursor] == close_ch:
            depth -= 1
            if depth == 0:
                return text[index + 1 : cursor], cursor + 1
        cursor += 1
    return None


def _caption_visible(body: str) -> str:
    body = re.sub(r"(?<!\\)%.*", "", body)
    body = re.sub(r"(?<!\\)\$(?:\\.|[^$])*\$", " ", body)
    body = re.sub(
        r"\\(?:cite[a-zA-Z]*|ref|eqref|autoref|cref|Cref|pageref|label)\*?\{[^{}]*\}",
        " ",
        body,
    )
    body = re.sub(r"\\[A-Za-z]+\*?", "", body)
    body = body.replace("{", "").replace("}", "")
    return body.strip()


if __name__ == "__main__":
    main()
