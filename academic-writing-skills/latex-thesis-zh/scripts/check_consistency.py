#!/usr/bin/env python3
"""
Terminology Consistency Checker - Check term usage consistency in thesis

Usage:
    uv run python check_consistency.py main.tex
    uv run python check_consistency.py main.tex --terms
    uv run python check_consistency.py main.tex --abbreviations
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

try:
    from tex_loader import AssembledDocument, assemble, iter_files, read_text_robust
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from tex_loader import AssembledDocument, assemble, iter_files, read_text_robust


ABBREV_STOPWORDS = frozenset(
    {
        "PDF",
        "URL",
        "HTTP",
        "HTTPS",
        "API",
        "TODO",
        "FIXME",
        "IEEE",
        "ACM",
        "ISO",
        "IEC",
        "GB",
        "DOI",
        "ISBN",
        "ISSN",
        "GPU",
        "CPU",
        "RAM",
        "USB",
        "FPGA",
        "LED",
        "MCU",
    }
)
ABBREV_MIN_USES = 2


class _Definition(NamedTuple):
    full_name: str
    start: int
    position: int
    bounded: bool


class ConsistencyChecker:
    """Check terminology and abbreviation consistency across thesis files."""

    # Surface-form candidates, not proof that concepts are interchangeable.
    DEFAULT_TERM_GROUPS_ZH = [
        ["深度学习", "深层学习"],
        ["卷积神经网络", "卷积网络", "CNN"],
        ["循环神经网络", "RNN"],
        ["长短期记忆", "LSTM"],
        ["生成对抗网络", "GAN"],
        ["自然语言处理", "NLP"],
        ["计算机视觉", "CV"],
        ["强化学习", "RL"],
    ]

    DEFAULT_TERM_GROUPS_EN = [
        ["machine learning", "ML"],
        ["convolutional neural network", "CNN"],
        ["recurrent neural network", "RNN"],
        ["long short-term memory", "LSTM"],
        ["generative adversarial network", "GAN"],
        ["natural language processing", "NLP"],
    ]

    def __init__(
        self,
        tex_files: list[str],
        custom_terms_file: str | None = None,
        *,
        entry_file: str | None = None,
    ):
        self.tex_files = [Path(f).resolve() for f in tex_files]
        self.entry_file = Path(entry_file).resolve() if entry_file else None
        self.content_cache: dict[Path, str] = {}
        self._documents: list[AssembledDocument] | None = None
        self.coverage_note = (
            "按入口 include 图检查装配全文顺序；覆盖范围受 loader 警告限制。"
            if self.entry_file
            else "文件内顺序已检查，跨文件顺序未验证（无主入口）。"
        )
        self.term_groups_zh = list(self.DEFAULT_TERM_GROUPS_ZH)
        self.term_groups_en = list(self.DEFAULT_TERM_GROUPS_EN)
        if custom_terms_file:
            self._load_custom_terms(custom_terms_file)

    def _load_custom_terms(self, path: str) -> None:
        """Load custom term groups from a JSON file.

        Expected format: {"zh": [["termA", "termB"], ...], "en": [["termC", "termD"], ...]}
        """
        import json

        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            if "zh" in data:
                self.term_groups_zh.extend(data["zh"])
            if "en" in data:
                self.term_groups_en.extend(data["en"])
        except Exception as e:
            print(f"[WARNING] Failed to load custom terms: {e}", file=sys.stderr)

    def _load_content(self, tex_file: Path) -> str:
        """Load and cache file content."""
        if tex_file not in self.content_cache:
            try:
                content, warning = read_text_robust(tex_file)
                if warning:
                    print(f"[WARNING] {warning}", file=sys.stderr)
                self.content_cache[tex_file] = content
            except OSError as exc:
                print(f"[WARNING] Cannot read {tex_file}: {exc}", file=sys.stderr)
                raise
        return self.content_cache[tex_file]

    def _get_documents(self) -> list[AssembledDocument]:
        """One ordered document per trusted entry, otherwise independent files."""
        if self._documents is None:
            if self.entry_file:
                document = assemble(self.entry_file)
                self._documents = [document]
                for warning in document.warning_lines("[WARNING]"):
                    print(warning, file=sys.stderr)
            else:
                documents = []
                for tex_file in self.tex_files:
                    content = self._load_content(tex_file)
                    documents.append(
                        AssembledDocument(
                            entry=tex_file,
                            content=content,
                            origins=[
                                (str(tex_file), line) for line in range(1, content.count("\n") + 2)
                            ],
                        )
                    )
                self._documents = documents
            print(f"[INFO] {self.coverage_note}", file=sys.stderr)
        return self._documents

    @staticmethod
    def _origin(document: AssembledDocument, position: int) -> tuple[str, int]:
        return document.origin(document.content.count("\n", 0, position) + 1)

    # 注释与"伪命中"载体（\cite 键、标签、文件路径参数）在术语统计前抹除。
    _SANITIZE_RES = [
        re.compile(r"(?<!\\)%.*"),  # LaTeX 行内注释
        re.compile(r"\\(?:cite\w*|ref|eqref|autoref|cref|Cref|pageref|label)\*?\{[^}]*\}"),
        re.compile(
            r"\\(?:input|include|subfile|includegraphics|bibliography)\s*(?:\[[^\]]*\])?\{[^}]*\}"
        ),
        re.compile(r"\\(?:url|href)\{[^}]*\}"),
    ]

    @classmethod
    def _sanitize(cls, content: str) -> str:
        """Blank out comments / citation keys / file paths, preserving offsets
        so line numbers computed against the sanitized text stay valid."""
        for pattern in cls._SANITIZE_RES:
            content = pattern.sub(lambda m: re.sub(r"[^\r\n]", " ", m.group()), content)
        return content

    @staticmethod
    def _is_abbrev(term: str) -> bool:
        """全大写 ASCII 词视为缩写（CNN/RNN/NLP...），其余为全称变体。"""
        return bool(re.fullmatch(r"[A-Z][A-Z0-9-]+", term))

    @staticmethod
    def _find_abbrev_definitions(content: str) -> dict[str, list[_Definition]]:
        """Collect bounded, same-line visible name fragments, never semantic names."""
        definitions: dict[str, list[_Definition]] = defaultdict(list)
        for match in re.finditer(r"[（(][ \t]*([A-Z]{2,})[ \t]*[）)]", content):
            line_start = content.rfind("\n", 0, match.start()) + 1
            window_start = max(line_start, match.start() - 120)
            prefix = content[window_start : match.start()]
            # A name fragment cannot consume preceding sentences or LaTeX structure.
            boundaries = list(re.finditer(r"[。.!！?？;；,，:：（）(){}\\\r]", prefix))
            fragment_start = boundaries[-1].end() if boundaries else 0
            fragment = prefix[fragment_start:]
            full_name = fragment.strip()
            start = window_start + fragment_start + len(fragment) - len(fragment.lstrip())
            bounded = bool(full_name) and (window_start == line_start or bool(boundaries))
            definitions[match.group(1)].append(
                _Definition(full_name, start, match.start(1), bounded)
            )
        return definitions

    def check_terms(self) -> dict:
        """Check term consistency across files.

        分组共现只产生待复核候选，频率不决定规范名。正常全称/缩写切换
        最多给可选风格提示；未定义或先用后定义由 check_abbreviations 负责。
        """
        # term -> [(document scope, character offset)]
        term_occurrences: dict[str, list[tuple[int, int]]] = defaultdict(list)
        all_groups = self.term_groups_zh + self.term_groups_en
        all_terms = dict.fromkeys(term for group in all_groups for term in group)
        definitions = []
        for idx, document in enumerate(self._get_documents()):
            content = self._sanitize(document.content)
            definitions.append(self._find_abbrev_definitions(content))
            for term in all_terms:
                pattern = re.escape(term)
                if self._is_abbrev(term):
                    pattern = rf"(?<![A-Za-z0-9_]){pattern}(?![A-Za-z0-9_])"
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    term_occurrences[term].append((idx, match.start()))

        inconsistencies = []
        checked_groups: set[frozenset] = set()

        for group in all_groups:
            group_set = frozenset(group)
            if group_set in checked_groups:
                continue
            checked_groups.add(group_set)

            full_variants = [t for t in group if not self._is_abbrev(t)]
            abbrevs = [t for t in group if self._is_abbrev(t)]

            found_full = {
                term: len(term_occurrences[term])
                for term in full_variants
                if term_occurrences[term]
            }

            # (a) Group membership and counts are observations, not semantic proof.
            if len(found_full) > 1:
                inconsistencies.append(
                    {
                        "type": "variant_mix",
                        "group": list(found_full.keys()),
                        "counts": found_full,
                        "suggestion": "NEEDS-LLM：同组表面形式共现，请核对是否指同一概念；"
                        "仅在语义相同且无切换理由时统一，频次和分组顺序不决定规范名。",
                    }
                )

            # (b) Optional style observation; exclude all expansion/reintroduction spans.
            for abbrev in abbrevs:
                late_uses = []
                for term in found_full:
                    for idx, position in term_occurrences[term]:
                        defs = definitions[idx].get(abbrev, [])
                        if (
                            defs
                            and defs[0].bounded
                            and position > defs[0].position
                            and not any(d.start <= position <= d.position for d in defs)
                        ):
                            late_uses.append((idx, position))
                if len(late_uses) >= 3:
                    inconsistencies.append(
                        {
                            "type": "full_after_abbrev",
                            "group": [*found_full.keys(), abbrev],
                            "counts": {**found_full, abbrev: len(term_occurrences[abbrev])},
                            "suggestion": f"可选风格候选：'{abbrev}' 定义后全称出现 "
                            f"{len(late_uses)} 次；全称与缩写可因语境合法切换，"
                            "NEEDS-LLM：结合可读性判断是否调整，不要求全部改为缩写。",
                        }
                    )

        return {
            "term_occurrences": {k: len(v) for k, v in term_occurrences.items() if v},
            "inconsistencies": inconsistencies,
            "status": "PASS" if not inconsistencies else "WARNING",
        }

    def check_abbreviations(self) -> dict:
        """Check first-use order within each trusted document scope."""
        definitions: dict[str, list[tuple[str, str, int]]] = defaultdict(list)
        usages: dict[str, list[tuple[str, int]]] = defaultdict(list)
        issues = []

        for document in self._get_documents():
            content = self._sanitize(document.content)
            local_definitions = self._find_abbrev_definitions(content)
            definition_positions = {
                d.position for items in local_definitions.values() for d in items
            }
            local_usages: dict[str, list[int]] = defaultdict(list)
            for match in re.finditer(r"(?<![A-Za-z0-9_])([A-Z]{2,})(?![A-Za-z0-9_])", content):
                abbrev = match.group(1)
                if abbrev in ABBREV_STOPWORDS or match.start() in definition_positions:
                    continue
                local_usages[abbrev].append(match.start())
                usages[abbrev].append(self._origin(document, match.start()))

            for abbrev, positions in local_usages.items():
                defs = local_definitions.get(abbrev, [])
                late_definition = bool(defs) and positions[0] < defs[0].position
                if late_definition or (not defs and len(positions) >= ABBREV_MIN_USES):
                    first_usage = self._origin(document, positions[0])
                    reason = "used but not defined in checked scope"
                    if late_definition:
                        source, line = self._origin(document, defs[0].position)
                        reason = f"used before its first definition at {source}:{line}"
                    issues.append(
                        {
                            "type": "undefined",
                            "abbreviation": abbrev,
                            "first_usage": first_usage,
                            "usage_count": len(positions),
                            "message": f"'{abbrev}' {reason} "
                            f"(first at {first_usage[0]}:{first_usage[1]})",
                        }
                    )

            for abbrev, defs in local_definitions.items():
                for definition in defs:
                    source, line = self._origin(document, definition.position)
                    if definition.bounded:
                        definitions[abbrev].append((definition.full_name, source, line))
                    elif abbrev not in ABBREV_STOPWORDS:
                        issues.append(
                            {
                                "type": "undefined",
                                "abbreviation": abbrev,
                                "first_usage": (source, line),
                                "usage_count": len(local_usages[abbrev]),
                                "message": f"NEEDS-LLM：'{abbrev}' 在 {source}:{line} "
                                "的括号前缺少可靠全称边界，请人工核对定义。",
                            }
                        )

        # Literal repeated expansions are legal, including across chapters.
        for abbrev, def_list in definitions.items():
            if len({name for name, _, _ in def_list}) > 1:
                locations = "; ".join(
                    f"{source}:{line} ({name})" for name, source, line in def_list
                )
                issues.append(
                    {
                        "type": "multiple_definitions",
                        "abbreviation": abbrev,
                        "definitions": def_list,
                        "message": f"NEEDS-LLM：'{abbrev}' 的可见全称候选片段不同：{locations}；"
                        "请核对语义是否等价（含中英文释义），不自动认定冲突。",
                    }
                )

        return {
            "definitions": {k: len(v) for k, v in definitions.items()},
            "usages": {k: len(v) for k, v in usages.items()},
            "issues": issues,
            "status": "PASS" if not issues else "WARNING",
        }

    def generate_report(self, terms_result: dict, abbrev_result: dict) -> str:
        """Generate human-readable report."""
        lines = []
        lines.append("=" * 60)
        lines.append("Consistency Check Report / 一致性检查报告")
        lines.append("=" * 60)
        lines.append(self.coverage_note)
        for document in self._get_documents():
            lines.extend(document.warning_lines("[WARNING]"))

        # Term consistency
        lines.append("\n[1] Term Consistency / 术语一致性")
        lines.append("-" * 40)

        if terms_result["inconsistencies"]:
            lines.append(f"Status: ⚠️ {len(terms_result['inconsistencies'])} candidates found")
            for inc in terms_result["inconsistencies"]:
                lines.append(f"\n  Group: {', '.join(inc['group'])}")
                for term, count in inc["counts"].items():
                    lines.append(f"    - '{term}': {count} times")
                lines.append(f"  Suggestion: {inc['suggestion']}")
        else:
            lines.append("Status: ✅ No inconsistencies found")

        # Abbreviation check
        lines.append("\n[2] Abbreviation Check / 缩略语检查")
        lines.append("-" * 40)

        if abbrev_result["issues"]:
            lines.append(f"Status: ⚠️ {len(abbrev_result['issues'])} issues found")
            for issue in abbrev_result["issues"]:
                lines.append(f"\n  [{issue['type']}] {issue['message']}")
        else:
            lines.append("Status: ✅ No abbreviation issues found within checked scope")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


def find_tex_files(main_file: str, all_files: bool = False) -> list[str]:
    """Collect the .tex file set to analyze.

    Default: only files reachable from ``main_file`` via \\input/\\include
    (drafts and backups outside the include graph no longer pollute the
    statistics). ``all_files=True`` keeps the legacy rglob behavior.
    """
    main_path = Path(main_file).resolve()

    if not all_files:
        reachable = [str(node.path) for node in iter_files(main_path) if node.exists]
        if reachable:
            return reachable
        return [str(main_path)]

    root_dir = main_path.parent
    tex_files = sorted(set(root_dir.rglob("*.tex")))
    return [str(f) for f in tex_files]


def main():
    parser = argparse.ArgumentParser(description="Terminology Consistency Checker")
    parser.add_argument("tex_file", help="Main .tex file or directory")
    parser.add_argument("--terms", "-t", action="store_true", help="Check only term consistency")
    parser.add_argument(
        "--abbreviations", "-a", action="store_true", help="Check only abbreviation consistency"
    )
    parser.add_argument("--json", "-j", action="store_true", help="Output in JSON format")
    parser.add_argument("--custom-terms", type=str, help="JSON file with custom term groups")
    parser.add_argument(
        "--all-files",
        action="store_true",
        help="Scan every .tex under the project root (legacy rglob), "
        "instead of only files reachable from the main file's include graph",
    )

    args = parser.parse_args()

    # Find tex files
    if Path(args.tex_file).is_dir():
        tex_files = [str(p) for p in Path(args.tex_file).rglob("*.tex")]
    else:
        if not Path(args.tex_file).exists():
            print(f"[ERROR] File not found: {args.tex_file}", file=sys.stderr)
            sys.exit(1)
        tex_files = find_tex_files(args.tex_file, all_files=args.all_files)

    if not tex_files:
        print("[ERROR] No .tex files found", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Checking {len(tex_files)} files...")

    # Run checks
    checker = ConsistencyChecker(
        tex_files,
        custom_terms_file=args.custom_terms,
        entry_file=(
            args.tex_file if not args.all_files and Path(args.tex_file).is_file() else None
        ),
    )

    if args.terms:
        result = checker.check_terms()
        if args.json:
            import json

            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\nTerm consistency: {result['status']}")
            for inc in result["inconsistencies"]:
                print(f"  - {inc['suggestion']}")
        sys.exit(0)

    if args.abbreviations:
        result = checker.check_abbreviations()
        if args.json:
            import json

            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\nAbbreviation check: {result['status']}")
            for issue in result["issues"]:
                print(f"  - {issue['message']}")
        sys.exit(0)

    # Full check
    terms_result = checker.check_terms()
    abbrev_result = checker.check_abbreviations()

    if args.json:
        import json

        output = {
            "terms": terms_result,
            "abbreviations": abbrev_result,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(checker.generate_report(terms_result, abbrev_result))

    # Exit code
    if terms_result["status"] != "PASS" or abbrev_result["status"] != "PASS":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
