#!/usr/bin/env python3
"""
BibTeX Verification Script - Check bibliography integrity
Includes static checks and online verification preparation.

Usage:
    uv run python verify_bib.py references.bib
    uv run python verify_bib.py references.bib --standard gb7714
    uv run python verify_bib.py references.bib --online-check
"""

import argparse
import json
import re
import sys
from pathlib import Path


class BibTeXVerifier:
    """Verify BibTeX file integrity and completeness."""

    REQUIRED_FIELDS = {
        "article": ["author", "title", "journal", "year"],
        "inproceedings": ["author", "title", "booktitle", "year"],
        "book": ["author", "title", "publisher", "year"],
    }

    # GB/T 7714 高频文献类型的必填字段（仅 --standard gb7714 / gb7714-2025 生效；
    # default 模式保持 REQUIRED_FIELDS 现状以向后兼容）
    GB_REQUIRED_FIELDS = {
        "phdthesis": ["author", "title", "school", "year"],  # [D]
        "mastersthesis": ["author", "title", "school", "year"],  # [D]
        "techreport": ["author", "title", "institution", "year"],  # [R]
        "patent": ["title", "number", "year"],  # [P]
        "standard": ["title", "number"],  # [S]
        "online": ["title", "url"],  # [EB/OL]
        "electronic": ["title", "url"],  # [EB/OL]
        "webpage": ["title", "url"],  # [EB/OL]
    }

    GB_STANDARDS = {"gb7714", "gb7714-2025"}
    ELECTRONIC_TYPES = {"online", "electronic", "webpage"}

    _CJK_RE = re.compile(r"[一-鿿]")
    _ET_AL_RE = re.compile(r"\bet\s+al\.?", re.IGNORECASE)

    def __init__(
        self,
        bib_file: str,
        standard: str = "default",
        online: bool = False,
        email: str | None = None,
        online_timeout: float = 10.0,
    ):
        self.bib_file = Path(bib_file).resolve()
        self.standard = standard
        self.entries = []
        self.issues = []
        self.online = online
        self.email = email
        self.online_timeout = online_timeout

    def parse(self) -> list[dict]:
        """Parse BibTeX file."""
        try:
            content = self.bib_file.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            self.issues.append({"type": "file_error", "message": str(e)})
            return []

        entries = []
        # Robust regex for entries
        entry_pattern = r"@(\w+)\s*{\s*([^,]+)\s*,([^@]*?)(?=\n\s*@|\Z)"

        for match in re.finditer(entry_pattern, content, re.DOTALL):
            entries.append(
                {
                    "type": match.group(1).lower(),
                    "key": match.group(2).strip(),
                    "fields": self._parse_fields(match.group(3)),
                    "raw": match.group(0),
                }
            )

        self.entries = entries
        return entries

    def _parse_fields(self, fields_str: str) -> dict[str, str]:
        fields = {}
        # Parse field = {value} or "value" or number
        field_pattern = r'(\w+)\s*=\s*(?:\{([^^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)"|(\d+))'
        for match in re.finditer(field_pattern, fields_str):
            name = match.group(1).lower()
            val = match.group(2) or match.group(3) or match.group(4) or ""
            fields[name] = val.strip()
        return fields

    def verify(self) -> dict:
        if not self.entries:
            self.parse()

        results = {
            "total_entries": len(self.entries),
            "valid_entries": 0,
            "issues": [],
            "status": "PASS",
            "needs_online_check": [],
        }

        for entry in self.entries:
            entry_issues = self._verify_entry(entry)
            if self.standard in self.GB_STANDARDS:
                entry_issues.extend(self._verify_entry_gb(entry))

            # Check for missing identifiers (DOI/URL)
            if "doi" not in entry["fields"] and "url" not in entry["fields"]:
                results["needs_online_check"].append(
                    {
                        "key": entry["key"],
                        "title": entry["fields"].get("title", "Unknown Title"),
                        "author": entry["fields"].get("author", "Unknown Author"),
                    }
                )

            if entry_issues:
                results["issues"].extend(entry_issues)
            else:
                results["valid_entries"] += 1

        if self.standard in self.GB_STANDARDS:
            results["issues"].extend(self._gb_file_level_notes())

        if results["issues"]:
            has_errors = any(i["severity"] == "error" for i in results["issues"])
            has_warnings = any(i["severity"] == "warning" for i in results["issues"])
            if has_errors:
                results["status"] = "FAIL"
            elif has_warnings:
                results["status"] = "WARNING"
            # info-only issues keep PASS

        # Online verification (when --online and online_bib_verify is available)
        if self.online:
            try:
                from online_bib_verify import OnlineBibVerifier

                online_verifier = OnlineBibVerifier(
                    polite_email=self.email,
                    timeout=self.online_timeout,
                )
                for entry_info in results["needs_online_check"]:
                    entry_dict = {
                        "key": entry_info["key"],
                        "title": entry_info.get("title", ""),
                        "author": entry_info.get("author", ""),
                    }
                    for entry in self.entries:
                        if entry["key"] == entry_info["key"]:
                            entry_dict.update(entry["fields"])
                            break
                    result = online_verifier.verify_entry(entry_dict)
                    if result.status == "mismatch":
                        for m in result.mismatches:
                            results["issues"].append(
                                {
                                    "key": result.bib_key,
                                    "type": "metadata_mismatch",
                                    "severity": "error",
                                    "message": f"Online verification mismatch: {m}",
                                }
                            )
                    elif result.status == "not_found":
                        results["issues"].append(
                            {
                                "key": result.bib_key,
                                "type": "not_found_online",
                                "severity": "warning",
                                "message": "Entry not found in online databases",
                            }
                        )
                    elif result.status == "verified" and result.suggested_doi:
                        results["issues"].append(
                            {
                                "key": result.bib_key,
                                "type": "doi_suggestion",
                                "severity": "warning",
                                "message": f"Consider adding DOI: {result.suggested_doi}",
                            }
                        )
            except ImportError:
                print("# Warning: online_bib_verify.py not found, skipping online verification")

        return results

    def _verify_entry(self, entry: dict) -> list[dict]:
        issues = []
        entry_type = entry["type"]
        entry_key = entry["key"]
        fields = entry["fields"]

        required_map = dict(self.REQUIRED_FIELDS)
        if self.standard in self.GB_STANDARDS:
            required_map.update(self.GB_REQUIRED_FIELDS)

        if entry_type in required_map:
            for field in required_map[entry_type]:
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

        # Title case check (simplified)
        if (
            "title" in fields
            and re.search(r"\b[A-Z]{2,}\b", fields["title"])
            and "{" not in fields["title"]
        ):
            issues.append(
                {
                    "key": entry_key,
                    "type": "caps",
                    "severity": "warning",
                    "message": "Unprotected uppercase in title",
                }
            )

        return issues

    # ── GB/T 7714 增量检查（--standard gb7714 / gb7714-2025） ────────

    @staticmethod
    def _author_tokens(author: str) -> list[str]:
        return [a.strip() for a in re.split(r"\s+and\s+", author) if a.strip()]

    def _verify_entry_gb(self, entry: dict) -> list[dict]:
        """国标著录格式的逐条目增量检查。只读建议，不改写条目。"""
        issues: list[dict] = []
        entry_type = entry["type"]
        entry_key = entry["key"]
        fields = entry["fields"]

        # 期刊 [J]：国标著录格式需要 刊名, 年, 卷(期): 页码
        if entry_type == "article":
            for field, label in (("volume", "卷号"), ("pages", "页码")):
                if not fields.get(field):
                    issues.append(
                        {
                            "key": entry_key,
                            "type": "gb_missing_field",
                            "field": field,
                            "severity": "warning",
                            "message": f"GB/T 7714 期刊著录需要 卷(期): 页码，缺少 {label} '{field}'",
                        }
                    )

        # 电子文献 [EB/OL]：联机资源需要引用日期 [引用日期]
        if entry_type in self.ELECTRONIC_TYPES and not fields.get("urldate"):
            issues.append(
                {
                    "key": entry_key,
                    "type": "gb_missing_field",
                    "field": "urldate",
                    "severity": "warning",
                    "message": "GB/T 7714 联机文献需要引用日期，缺少 'urldate'",
                }
            )

        # 2015 版：凡著录了获取路径（url）均建议补引用日期；
        # 2025 版取消了非网络文献的访问日期要求，故仅 2015 模式提示
        if (
            self.standard == "gb7714"
            and entry_type not in self.ELECTRONIC_TYPES
            and fields.get("url")
            and not fields.get("urldate")
        ):
            issues.append(
                {
                    "key": entry_key,
                    "type": "gb_urldate_hint",
                    "severity": "info",
                    "message": "著录了 url 但缺少 urldate（GB/T 7714-2015 建议补引用日期；2025 版不再要求）",
                }
            )

        # 作者截断标记："等"/"et al." 不应手写进 .bib，且语种要匹配
        author = fields.get("author", "")
        if author:
            tokens = self._author_tokens(author)
            has_cjk = bool(self._CJK_RE.search(author))
            uses_et_al = bool(self._ET_AL_RE.search(author)) or "others" in [
                t.lower() for t in tokens
            ]
            uses_deng = any(t == "等" or t.endswith(" 等") for t in tokens)
            if uses_et_al and has_cjk:
                issues.append(
                    {
                        "key": entry_key,
                        "type": "gb_author_truncation",
                        "severity": "warning",
                        "message": "中文条目作者使用了 'et al.'，GB/T 7714 中文条目应使用 '等'"
                        "（建议 .bib 保留全部作者，由样式自动截断）",
                    }
                )
            elif uses_deng and not has_cjk:
                issues.append(
                    {
                        "key": entry_key,
                        "type": "gb_author_truncation",
                        "severity": "warning",
                        "message": "英文条目作者使用了 '等'，GB/T 7714 英文条目应使用 'et al.'"
                        "（建议 .bib 保留全部作者，由样式自动截断）",
                    }
                )
            elif uses_et_al or uses_deng:
                issues.append(
                    {
                        "key": entry_key,
                        "type": "gb_author_truncation",
                        "severity": "info",
                        "message": "author 字段含手写截断标记；biblatex/bst 国标样式会自动按"
                        "'前 3 名 + 等/et al.'显示，建议保留全部作者",
                    }
                )

        return issues

    def _gb_file_level_notes(self) -> list[dict]:
        """文件级提示（每类至多一条，info 级，不影响退出状态）。"""
        notes: list[dict] = []

        many_author_keys = []
        missing_langid_keys = []
        preprint_keys = []
        for entry in self.entries:
            fields = entry["fields"]
            author = fields.get("author", "")
            tokens = self._author_tokens(author)
            has_marker = (
                bool(self._ET_AL_RE.search(author))
                or "others" in [t.lower() for t in tokens]
                or any(t == "等" for t in tokens)
            )
            if len(tokens) >= 4 and not has_marker:
                many_author_keys.append(entry["key"])
            cjk_content = self._CJK_RE.search(author) or self._CJK_RE.search(
                fields.get("title", "")
            )
            if cjk_content and not fields.get("langid"):
                missing_langid_keys.append(entry["key"])
            eprint_blob = " ".join(
                fields.get(f, "") for f in ("eprint", "archiveprefix", "journal", "howpublished")
            )
            if re.search(r"arxiv", eprint_blob, re.IGNORECASE):
                preprint_keys.append(entry["key"])

        if many_author_keys:
            notes.append(
                {
                    "key": ", ".join(many_author_keys[:5]),
                    "type": "gb_author_count",
                    "severity": "info",
                    "message": f"{len(many_author_keys)} 条条目作者 ≥4 名：国标显示为"
                    "'前 3 名 + 等/et al.'，biblatex/bst 样式自动处理；仅手写参考文献列表时需自行截断",
                }
            )
        if missing_langid_keys:
            notes.append(
                {
                    "key": ", ".join(missing_langid_keys[:5]),
                    "type": "gb_langid_hint",
                    "severity": "info",
                    "message": f"{len(missing_langid_keys)} 条中文条目缺少 langid 字段"
                    "（biblatex-gb7714 系列样式按 langid 区分中英文排序与 '等/et al.' 显示）",
                }
            )

        if self.standard == "gb7714":
            notes.append(
                {
                    "key": "-",
                    "type": "gb_standard_transition",
                    "severity": "info",
                    "message": "GB/T 7714-2025 已于 2025-12-02 发布、2026-07-01 实施（代替 2015 版）。"
                    "答辩在 2026-07-01 之后建议与学校确认是否切换新国标，可改用 --standard gb7714-2025",
                }
            )
        elif self.standard == "gb7714-2025":
            notes.append(
                {
                    "key": "-",
                    "type": "gb_standard_transition",
                    "severity": "info",
                    "message": "GB/T 7714-2025 模式：非网络文献不再要求访问日期；新增预印本(preprint)/"
                    "数据集(dataset)著录类型；biblatex 社区已有 gb7714-2025 样式实现",
                }
            )
            if preprint_keys:
                notes.append(
                    {
                        "key": ", ".join(preprint_keys[:5]),
                        "type": "gb_preprint_hint",
                        "severity": "info",
                        "message": f"{len(preprint_keys)} 条疑似 arXiv 预印本条目："
                        "GB/T 7714-2025 新增预印本著录类型，建议按预印本格式著录（含获取路径）",
                    }
                )

        return notes

    def generate_report(self, result: dict) -> str:
        lines = []
        lines.append(f"BibTeX Check: {self.bib_file}")
        lines.append(f"Status: {result['status']}")

        if result["issues"]:
            lines.append("\nIssues:")
            for issue in result["issues"]:
                lines.append(f"  [{issue['severity'].upper()}] @{issue['key']}: {issue['message']}")

        if result["needs_online_check"]:
            lines.append(
                f"\n[INFO] {len(result['needs_online_check'])} entries missing DOI/URL (Use --online-check to export list)"
            )

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="BibTeX Verification")
    parser.add_argument("bib_file", help=".bib file")
    parser.add_argument(
        "--standard",
        choices=["default", "gb7714", "gb7714-2025"],
        default="default",
        help="default 仅基础完整性；gb7714 启用 GB/T 7714-2015 增量检查；"
        "gb7714-2025 按 2025 新国标（2026-07-01 实施）调整差异点",
    )
    parser.add_argument(
        "--online-check", action="store_true", help="Generate list for online verification"
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
    parser.add_argument("--output", help="Output file for online check JSON")

    args = parser.parse_args()

    if not Path(args.bib_file).exists():
        print("File not found.")
        sys.exit(1)

    verifier = BibTeXVerifier(
        args.bib_file,
        args.standard,
        online=getattr(args, "online", False),
        email=getattr(args, "email", None),
        online_timeout=getattr(args, "online_timeout", 10.0),
    )
    result = verifier.verify()

    if args.online_check:
        output_file = args.output or "verification_needed.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result["needs_online_check"], f, indent=2, ensure_ascii=False)
        print(f"Exported {len(result['needs_online_check'])} entries to {output_file}")
        print("Agent instructions: 使用 WebSearch 工具检索这些标题以补全 DOI。")
    else:
        print(verifier.generate_report(result))

    if result["status"] == "FAIL":
        sys.exit(1)


if __name__ == "__main__":
    main()
