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


# ── 草稿态词表（模块级，便于按院校规范配置）──────────────────────────
# 出处：fixture ch4/ch5 草稿态样本 + 保守收窄原则（宁漏勿误伤正常学术表述）。

# F-NOTE 核心组：明确的草稿备注词形（占位图注、待办标记）。
DRAFT_NOTE_CORE = [
    r"后续可根据.{0,20}(?:替换|更新|补充)",
    r"此处占位",
    r"待补充",
    r"待确认",
    r"TODO",
    r"FIXME",
]

# F-NOTE 对冲组：作者自认"结果非终稿"的未定稿对冲表述（fixture P2 驱动）。
# "复算"有正常学术用法（"复算结果一致"），加负向断言只命中裸用法。
DRAFT_NOTE_HEDGE = [
    r"待验证(?:设计|表述)?",
    r"暂以占位",
    r"仍在进行",
    r"重跑(?:验证|后补齐)?",
    r"待.{0,6}补齐",
    r"复算(?!结果|表明|验证了)",
    r"不代表.{0,8}性能",
]

# 命令的花括号路径参数（图名/文件名）常含"中文+扩展名点号"，会误触发
# mixed_punctuation；检查前按等长空格剥离，保留其余列号。
# 出处：fixture ch4 L88/111/152/161/187/230 六条中文图名假阳。
_PATH_ARG_RE = re.compile(r"\\(?:includegraphics(?:\[[^\]]*\])?|input|bibliography)\{[^}]*\}")
_KEY_ARG_RE = re.compile(
    r"\\(?:cite[a-zA-Z]*|ref|eqref|autoref|cref|Cref|pageref|label)\*?\{[^}]*\}"
    r"|\\hyperref\[[^\]]*\]"
)

# 单个空占位单元格（表体行去空白后的整格内容）。仅 --/--- / — / \ldots / 待填 命中；
# 单个 - 或任意含数字/文字的真实数据不命中。用于 F-PLACEHOLDER 行级判定。
_PLACEHOLDER_TOKEN_RE = re.compile(r"^(?:---?|—|\\ldots|待填)$")


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
            # 剥离 \includegraphics/\input/\bibliography 的路径参数，避免中文图名假阳（R2b）。
            "strip_path_args": True,
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
            # "特别"带负向断言：书面语"特别说明/特别是/特别地"不报，口语"特别好/特别大"仍报（R2c）。
            "pattern": r"很多|一些|非常|特别(?!说明|地|是)",
            "message": "Potential oral expression in academic writing",
            "severity": "warning",
            "visible_only": True,
        },
        # F-MD：Markdown 加粗残留。XeLaTeX 下 **文本** 按字面星号排版（不会加粗），
        # 应改用 \textbf{}。转义写法 \*\* 因反斜杠隔开而没有连续两颗星，天然不命中；
        # 数学环境 / verbatim / 注释由 visible_only + 既有跳过逻辑排除。
        "F-MD": {
            "pattern": r"\*\*[^*\n]{1,80}\*\*",
            "message": "LaTeX 中 Markdown **加粗** 会按字面星号排版，应改用 \\textbf{}",
            "severity": "warning",
            "visible_only": True,
        },
        # F-NOTE：草稿备注泄漏进正文（占位图注、待办等）。词表刻意收窄，只命中
        # 明确的备注词形；正常学术让步表述（"仍需通过实验确认""有待进一步研究"）
        # 不含触发词形，不误伤。词表见模块级 DRAFT_NOTE_CORE。
        "F-NOTE": {
            "pattern": "|".join(DRAFT_NOTE_CORE),
            "message": "疑似草稿备注泄漏进正文，定稿前应删除或移入注释",
            "severity": "info",
            "visible_only": True,
        },
        # F-NOTE-HEDGE：未定稿对冲表述（作者自认结果非终稿）。与 F-NOTE 同为 info，
        # 但文案区分"草稿备注"与"未定稿对冲"。词表见模块级 DRAFT_NOTE_HEDGE。
        "F-NOTE-HEDGE": {
            "pattern": "|".join(DRAFT_NOTE_HEDGE),
            "message": "疑似未定稿对冲表述（自认结果非终稿），定稿前请核对或补全",
            "severity": "info",
            "visible_only": True,
        },
        # F-PLACEHOLDER：占位符表格行。仅当表体行的**全部数据单元格**都是空占位
        # （--- / -- / — / \ldots / 待填 / 空）且含 ≥2 个显式占位记号时才报——单个 -
        # 单元格是合法负号/缺省，混有真实数字的行（如以 --- 标"不适用"的正常表格）不报。
        # 行级判定见 _placeholder_row_column（正则仅示形）。severity warning（对应 Major）。
        # 出处：fixture ch4 L418/420 全 --- 结果表空行。
        "F-PLACEHOLDER": {
            "pattern": r"(?:&\s*(?:---?|—|\\ldots|待填)\s*){2,}",
            "message": "疑似占位符表格行（多个空数据单元格），定稿前应填入真实数据",
            "severity": "warning",
            "visible_only": False,
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

                # F-PLACEHOLDER 走行级判定（整行数据格全为空占位才报），不做逐字符匹配。
                if check_name == "F-PLACEHOLDER":
                    col = self._placeholder_row_column(line)
                    if col is not None:
                        src_file, src_line = doc.origin(i)
                        issues.append(
                            {
                                "source": "chinese_check",
                                "file": src_file if doc.multi_file else str(self.tex_file.name),
                                "line": src_line,
                                "column": col,
                                "severity": check_info["severity"],
                                "code": check_name,
                                "message": check_info["message"],
                                "matched": line.strip(),
                            }
                        )
                    continue

                target = parser.extract_visible_text(line) if visible_only else line
                if check_info.get("strip_path_args"):
                    target = _PATH_ARG_RE.sub(lambda m: " " * len(m.group()), target)
                    target = _KEY_ARG_RE.sub(lambda m: " " * len(m.group()), target)
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

    @staticmethod
    def _placeholder_row_column(line: str) -> Optional[int]:
        r"""占位符表格行判定。表体行（含 &）去掉行首标题格与行尾 \\ 后，若其余数据格
        全部为空占位（-- / --- / — / \ldots / 待填 / 空）且含 ≥2 个显式占位记号，返回
        首个 & 的 1-based 列号；混有真实数字/文字（如正常表格用 --- 标"不适用"）返回
        None。这样只报 fixture ch4 L418/420 型"整行未填"，不误伤 N/A 与真实数据混排行。"""
        amp = line.find("&")
        if amp < 0:
            return None
        body = re.sub(r"\\\\.*$", "", line)  # 去行尾 \\ 及其后的 \hline/\midrule/注释
        cells = [c.strip() for c in body.split("&")[1:]]  # [1:] 跳过行首标题格
        if len(cells) < 2:
            return None
        explicit = sum(bool(_PLACEHOLDER_TOKEN_RE.match(c)) for c in cells)
        all_filler = all(c == "" or bool(_PLACEHOLDER_TOKEN_RE.match(c)) for c in cells)
        return amp + 1 if explicit >= 2 and all_filler else None

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
