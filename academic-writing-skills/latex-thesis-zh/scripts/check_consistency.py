#!/usr/bin/env python3
"""
Terminology Consistency Checker - Check term usage consistency in thesis

Usage:
    uv run python check_consistency.py main.tex
    uv run python check_consistency.py main.tex --terms
    uv run python check_consistency.py main.tex --abbreviations
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, NamedTuple

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

_PROJECT_ABBREV_FORM = "（英文全称，缩写）"
_MACRO_COVERAGE_NOTE = "存在未展开的自定义宏，可见文本覆盖不完整，不能据此认为没有问题。"
_UNCLEAR_NAME_NOTE = "NEEDS-LLM：完整括注前的中文名称边界不明确，未登记合格首现，不报告二次出现。"
_GOVERNANCE_KEYS = frozenset({"zh", "en", "banned", "locked", "exempt"})
_FIXED_SKIP_ENVS = frozenset(
    {
        "verbatim",
        "lstlisting",
        "minted",
        "thebibliography",
        "abbreviation",
        "abbreviations",
        "acronym",
        "equation",
        "equation*",
        "align",
        "align*",
        "alignat",
        "alignat*",
        "gather",
        "gather*",
        "multline",
        "multline*",
        "eqnarray",
        "eqnarray*",
        "flalign",
        "flalign*",
        "displaymath",
        "math",
        "subequations",
    }
)
_ABBR_REGION_TITLES = frozenset({"缩略词表", "缩略词对照表"})
_HEADING_LEVELS = {
    "part": 0,
    "chapter": 1,
    "section": 2,
    "subsection": 3,
    "subsubsection": 4,
    "paragraph": 5,
    "subparagraph": 6,
}
_CUSTOM_MACRO_RE = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand|"
    r"NewDocumentCommand|RenewDocumentCommand|ProvideDocumentCommand|"
    r"DeclareDocumentCommand|newenvironment|renewenvironment|"
    r"NewDocumentEnvironment|DeclareDocumentEnvironment|def|edef|gdef|xdef)(?![A-Za-z])"
)
_ENV_RE = re.compile(r"\\(begin|end)\{([^{}]+)\}")
_HEADING_RE = re.compile(
    r"\\(part|chapter|section|subsection|subsubsection|paragraph|subparagraph)"
    r"\*?(?:\s*\[[^\]]*\])?\s*\{([^{}]*)\}"
)
_LABEL_IN_TITLE_RE = re.compile(r"\\label\{[^{}]*\}")
_CITE_PAYLOAD_RE = re.compile(
    r"\\(?:(?:paren|text|auto|foot|smart)?cite\w*"
    r"|ref|eqref|autoref|cref|Cref|pageref|nameref|label)"
    r"\*?(?:\s*\[[^\]]*\])*\s*\{[^{}]*\}"
)
_PATH_RE = re.compile(
    r"\\(?:input|include|subfile|includegraphics|bibliography|addbibresource|"
    r"lstinputlisting)\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}"
    r"|\\(?:url|href)\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}"
)
_MATH_RES = (
    re.compile(r"\$\$(?:\\.|[^$])*?\$\$", re.DOTALL),
    re.compile(r"\\\[(?:\\.|.)*?\\\]", re.DOTALL),
    re.compile(r"\\\((?:\\.|.)*?\\\)", re.DOTALL),
    re.compile(r"(?<!\\)\$(?!\$)(?:\\.|[^$])*?(?<!\\)\$(?!\$)", re.DOTALL),
)
_FULL_FORM_RE = re.compile(
    r"(?P<prefix>[\u4e00-\u9fff·]{0,80})"
    r"[（(]"
    r"(?P<en>[A-Za-z][A-Za-z0-9-]*(?:[ \t]+[A-Za-z][A-Za-z0-9-]*)*)"
    r"[ \t]*[，,][ \t]*"
    r"(?P<abbr>[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*)"
    r"[ \t]*[）)]"
)
_NAME_GLUE_RE = re.compile(r"采用|使用|通过|称为|叫做|的|了|是")
_CLEAR_NAME_MAX = 20


class GovernanceConfigError(Exception):
    """Invalid --governance input. Callers must exit non-zero without a pass report."""


class GovernanceConfig(NamedTuple):
    banned: dict[str, tuple[tuple[str, str | None], ...]]
    locked: dict[str, tuple[str, ...]]
    exempt_envs: tuple[str, ...]
    raw: dict[str, Any]


class _MaskedText:
    def __init__(self, content: str):
        self.chars = list(content)

    def text(self) -> str:
        return "".join(self.chars)

    def blank(self, start: int, end: int) -> None:
        for index in range(max(0, start), min(end, len(self.chars))):
            if self.chars[index] != "\n":
                self.chars[index] = " "

    def blank_matches(self, pattern: re.Pattern[str], *, limit: int | None = None) -> None:
        for match in pattern.finditer(self.text()):
            if limit is not None and match.end() - match.start() > limit:
                continue
            self.blank(match.start(), match.end())


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def _result_status(findings: list[dict[str, Any]], notes: list[str]) -> str:
    if findings:
        return "CANDIDATES"
    if notes:
        return "INCOMPLETE"
    return "PASS"


def _normalize_heading_title(title: str) -> str:
    return re.sub(r"\s+", "", _LABEL_IN_TITLE_RE.sub("", title))


def _is_han(char: str) -> bool:
    return "\u4e00" <= char <= "\u9fff" or char == "·"


def _term_pattern(term: str) -> re.Pattern[str]:
    if term.isascii() and re.search(r"[A-Za-z0-9]", term):
        return re.compile(rf"(?<![A-Za-z0-9_]){re.escape(term)}(?![A-Za-z0-9_])")
    return re.compile(re.escape(term))


def _require_string_groups(data: dict[str, Any], key: str) -> None:
    if key not in data:
        return
    groups = data[key]
    if not isinstance(groups, list):
        raise GovernanceConfigError(f"{key} must be a list of string groups")
    for group in groups:
        if not isinstance(group, list) or not group:
            raise GovernanceConfigError(f"{key} must be a list of string groups")
        if not all(isinstance(term, str) and term.strip() for term in group):
            raise GovernanceConfigError(f"{key} must be a list of string groups")


def _parse_banned(raw: Any) -> dict[str, tuple[tuple[str, str | None], ...]]:
    if not isinstance(raw, dict):
        raise GovernanceConfigError("banned must be an object")
    parsed: dict[str, tuple[tuple[str, str | None], ...]] = {}
    for term, spec in raw.items():
        if not isinstance(term, str) or not term.strip():
            raise GovernanceConfigError("banned term must be a non-empty string")
        if not isinstance(spec, dict) or set(spec) - {"candidates"}:
            raise GovernanceConfigError(f"banned entry {term!r} must contain candidates")
        candidates = spec.get("candidates")
        if not isinstance(candidates, list) or not candidates:
            raise GovernanceConfigError(f"banned term {term!r} needs at least one candidate")
        parsed_candidates: list[tuple[str, str | None]] = []
        for candidate in candidates:
            if not isinstance(candidate, dict) or set(candidate) - {"text", "slot"}:
                raise GovernanceConfigError(f"banned candidate for {term!r} is invalid")
            text = candidate.get("text")
            if not isinstance(text, str) or not text.strip():
                raise GovernanceConfigError(f"banned term {term!r} needs a non-empty candidate")
            slot = candidate.get("slot") if "slot" in candidate else None
            if slot is not None and not isinstance(slot, str):
                raise GovernanceConfigError(f"banned slot for {term!r} must be a string")
            if isinstance(slot, str) and not slot.strip():
                slot = None
            parsed_candidates.append((text, slot))
        parsed[term] = tuple(parsed_candidates)
    return parsed


def _parse_locked(raw: Any) -> dict[str, tuple[str, ...]]:
    if not isinstance(raw, dict):
        raise GovernanceConfigError("locked must be an object")
    parsed: dict[str, tuple[str, ...]] = {}
    for canonical, variants in raw.items():
        if not isinstance(canonical, str) or not canonical.strip():
            raise GovernanceConfigError("locked canonical name must be a non-empty string")
        if not isinstance(variants, list):
            raise GovernanceConfigError(f"locked variants for {canonical!r} must be a list")
        cleaned: list[str] = []
        for variant in variants:
            if not isinstance(variant, str) or not variant.strip():
                raise GovernanceConfigError(f"locked variant for {canonical!r} must be non-empty")
            cleaned.append(variant)
        parsed[canonical] = tuple(cleaned)
    return parsed


def _parse_exempt(raw: Any) -> tuple[str, ...]:
    if not isinstance(raw, dict) or set(raw) - {"environments"}:
        raise GovernanceConfigError("exempt only accepts environment names")
    environments = raw.get("environments", [])
    if not isinstance(environments, list):
        raise GovernanceConfigError("exempt.environments must be a list")
    names: list[str] = []
    for name in environments:
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z*][A-Za-z0-9*]*", name):
            raise GovernanceConfigError("exempt environment name is invalid")
        names.append(name)
    return tuple(names)


def load_governance_terms(path: str) -> GovernanceConfig:
    """Read and validate governance fields once. Does not scan TeX."""
    file_path = Path(path)
    if not file_path.is_file():
        raise GovernanceConfigError(f"custom terms file not found: {path}")
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        raise GovernanceConfigError(f"custom terms file is not valid UTF-8: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GovernanceConfigError(f"invalid JSON: {exc}") from exc
    except OSError as exc:
        raise GovernanceConfigError(f"custom terms file not found: {path}") from exc
    if not isinstance(data, dict):
        raise GovernanceConfigError("custom terms root must be an object")
    unknown = sorted(set(data) - _GOVERNANCE_KEYS)
    if unknown:
        raise GovernanceConfigError(f"unknown fields: {', '.join(unknown)}")
    _require_string_groups(data, "zh")
    _require_string_groups(data, "en")
    banned = _parse_banned(data["banned"]) if "banned" in data else {}
    locked = _parse_locked(data["locked"]) if "locked" in data else {}
    exempt_envs = _parse_exempt(data["exempt"]) if "exempt" in data else ()
    return GovernanceConfig(banned, locked, exempt_envs, data)


def _mask_environments(masked: _MaskedText, names: set[str]) -> None:
    text = masked.text()
    stack: list[tuple[str, int]] = []
    spans: list[tuple[int, int]] = []
    for match in _ENV_RE.finditer(text):
        kind, name = match.group(1), match.group(2).strip()
        if kind == "begin":
            stack.append((name, match.start()))
            continue
        for index in range(len(stack) - 1, -1, -1):
            if stack[index][0] != name:
                continue
            start = stack[index][1]
            del stack[index:]
            if name in names:
                spans.append((start, match.end()))
            break
    for start, end in spans:
        masked.blank(start, end)


def _mask_abbreviation_regions(masked: _MaskedText) -> None:
    text = masked.text()
    headings: list[tuple[int, int, str]] = []
    for match in _HEADING_RE.finditer(text):
        level = _HEADING_LEVELS[match.group(1)]
        title = _normalize_heading_title(match.group(2))
        headings.append((match.start(), level, title))
    for index, (start, level, title) in enumerate(headings):
        if title not in _ABBR_REGION_TITLES:
            continue
        stop = len(text)
        for next_start, next_level, _title in headings[index + 1 :]:
            if next_level <= level:
                stop = next_start
                break
        masked.blank(start, stop)


def mask_protected(content: str, extra_envs: tuple[str, ...] = ()) -> tuple[str, list[str]]:
    """Blank protected spans without moving the remaining source positions."""
    masked = _MaskedText(content)
    masked.blank_matches(re.compile(r"(?<!\\)%[^\n]*"))
    notes: list[str] = []
    if _CUSTOM_MACRO_RE.search(masked.text()):
        notes.append(_MACRO_COVERAGE_NOTE)
    begin_document = re.search(r"\\begin\{document\}", masked.text())
    if begin_document:
        masked.blank(0, begin_document.end())
    _mask_environments(masked, set(_FIXED_SKIP_ENVS).union(extra_envs))
    _mask_abbreviation_regions(masked)
    for pattern in _MATH_RES:
        masked.blank_matches(pattern, limit=4000)
    masked.blank_matches(_CITE_PAYLOAD_RE)
    masked.blank_matches(_PATH_RE)
    return masked.text(), notes


def _candidate_records(
    candidates: tuple[tuple[str, str | None], ...],
) -> list[dict[str, str | None]]:
    return [{"text": text, "slot": slot} for text, slot in candidates]


def _new_finding(**fields: Any) -> dict[str, Any]:
    finding = {
        "severity": "Info",
        "priority": "P3",
        "source": "[Script]",
        "meaning_check": "NEEDS-LLM",
    }
    finding.update(fields)
    return finding


def _is_title_case(english: str) -> bool:
    words = [word for word in english.split() if word]
    if len(words) < 2:
        return False
    capitalized = 0
    for word in words:
        head = word.split("-", 1)[0]
        if head[:1].isupper():
            capitalized += 1
    return capitalized >= 2


def dedupe_style_findings(
    findings: list[dict[str, Any]],
    abbrev_issues: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Drop same-position same-class duplicates. Do not drop a different class."""
    blocked = set()
    for issue in abbrev_issues or []:
        usage = issue.get("first_usage")
        if isinstance(usage, (tuple, list)) and len(usage) >= 2:
            blocked.add((str(usage[0]), int(usage[1]), str(issue.get("type"))))
    kept: list[dict[str, Any]] = []
    seen = set()
    for finding in findings:
        identity = (
            finding.get("file"),
            finding.get("line"),
            finding.get("kind"),
            finding.get("term"),
            finding.get("abbreviation"),
            finding.get("field"),
            finding.get("offset"),
        )
        class_key = (str(finding.get("file")), int(finding["line"]), str(finding.get("kind")))
        if identity in seen or class_key in blocked:
            continue
        seen.add(identity)
        kept.append(finding)
    return kept


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
        governance: GovernanceConfig | None = None,
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
        self.governance = governance
        if governance is not None:
            self._apply_loaded_groups(governance.raw)
        elif custom_terms_file:
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

    def _apply_loaded_groups(self, data: dict[str, Any]) -> None:
        """Same zh/en extend path as the legacy loader. Governance fields stay elsewhere."""
        if "zh" in data:
            self.term_groups_zh.extend(data["zh"])
        if "en" in data:
            self.term_groups_en.extend(data["en"])

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

    def _scan_documents(self) -> list[tuple[AssembledDocument, str, list[str]]]:
        extra_envs = self.governance.exempt_envs if self.governance is not None else ()
        scanned = []
        for document in self._get_documents():
            masked, notes = mask_protected(document.content, extra_envs)
            scanned.append((document, masked, notes))
        return scanned

    def check_governance(self) -> dict[str, Any]:
        """Report banned hits and locked variants. Does not choose a canonical name."""
        if self.governance is None:
            raise GovernanceConfigError("governance config is not loaded")
        findings: list[dict[str, Any]] = []
        notes: list[str] = []
        for document, masked, doc_notes in self._scan_documents():
            notes.extend(doc_notes)
            for term, candidates in self.governance.banned.items():
                for match in _term_pattern(term).finditer(masked):
                    source, line = self._origin(document, match.start())
                    findings.append(
                        _new_finding(
                            kind="banned",
                            term=term,
                            canonical="",
                            candidates=_candidate_records(candidates),
                            file=source,
                            line=line,
                            offset=match.start(),
                        )
                    )
            for canonical, variants in self.governance.locked.items():
                for variant in variants:
                    for match in _term_pattern(variant).finditer(masked):
                        source, line = self._origin(document, match.start())
                        findings.append(
                            _new_finding(
                                kind="locked",
                                term=variant,
                                canonical=canonical,
                                candidates=[],
                                file=source,
                                line=line,
                                offset=match.start(),
                            )
                        )
        notes = _unique(notes)
        return {
            "findings": findings,
            "coverage_notes": notes,
            "status": _result_status(findings, notes),
        }

    def check_abbreviation_style(self) -> dict[str, Any]:
        """Register a clear full form, then flag later XOR and Title Case candidates."""
        findings: list[dict[str, Any]] = []
        notes: list[str] = []
        unclear = False
        for document, masked, doc_notes in self._scan_documents():
            notes.extend(doc_notes)
            registered: dict[tuple[str, str], int] = {}
            for match in _FULL_FORM_RE.finditer(masked):
                prefix = match.group("prefix")
                if not prefix:
                    continue
                prefix_start = match.start()
                before = masked[prefix_start - 1] if prefix_start else ""
                clear = (
                    (prefix_start == 0 or not _is_han(before))
                    and len(prefix) <= _CLEAR_NAME_MAX
                    and _NAME_GLUE_RE.search(prefix) is None
                )
                if not clear:
                    unclear = True
                    continue
                english = match.group("en")
                abbrev = match.group("abbr")
                registered.setdefault((prefix, abbrev), match.end())
                if _is_title_case(english):
                    source, line = self._origin(document, match.start())
                    findings.append(
                        _new_finding(
                            kind="title_case",
                            term=prefix,
                            abbreviation=abbrev,
                            field=english,
                            detail=(
                                f"Title Case；项目形式为{_PROJECT_ABBREV_FORM}；不改写专名大小写"
                            ),
                            file=source,
                            line=line,
                            offset=match.start(),
                        )
                    )
            for (name, abbrev), end in registered.items():
                short_re = re.compile(
                    rf"(?<![\u4e00-\u9fff·]){re.escape(name)}"
                    rf"[（(][ \t]*{re.escape(abbrev)}[ \t]*[）)]"
                )
                side_re = re.compile(
                    rf"(?<![\u4e00-\u9fff·]){re.escape(name)}[ \t]+"
                    rf"(?<![A-Za-z0-9_]){re.escape(abbrev)}(?![A-Za-z0-9_])"
                )
                for kind, pattern, detail in (
                    ("second_parenthetical", short_re, "二次括注候选"),
                    ("juxtaposition", side_re, "并列候选"),
                ):
                    for match in pattern.finditer(masked):
                        if match.start() < end:
                            continue
                        source, line = self._origin(document, match.start())
                        findings.append(
                            _new_finding(
                                kind=kind,
                                term=name,
                                abbreviation=abbrev,
                                field="",
                                detail=detail,
                                file=source,
                                line=line,
                                offset=match.start(),
                            )
                        )
        if unclear:
            notes.append(_UNCLEAR_NAME_NOTE)
        notes = _unique(notes)
        return {
            "findings": findings,
            "coverage_notes": notes,
            "project_form": _PROJECT_ABBREV_FORM,
            "status": _result_status(findings, notes),
        }

    def generate_report(
        self,
        terms_result: dict,
        abbrev_result: dict,
        governance_result: dict[str, Any] | None = None,
        abbreviation_style_result: dict[str, Any] | None = None,
    ) -> str:
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

        if governance_result is not None:
            lines.extend(_governance_report_lines(governance_result))
        if abbreviation_style_result is not None:
            lines.extend(_abbreviation_style_report_lines(abbreviation_style_result))

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


def _governance_report_lines(result: dict[str, Any]) -> list[str]:
    lines = ["\n[3] Term Governance / 术语治理", "-" * 40]
    findings = result["findings"]
    notes = result["coverage_notes"]
    if findings:
        lines.append(f"Status: {len(findings)} candidates")
    elif notes:
        lines.append("Status: coverage incomplete")
    else:
        lines.append("Status: no governance candidates in scanned text")
    lines.extend(notes)
    for finding in findings:
        location = f"{finding['file']}:{finding['line']}"
        lines.append(
            "[Script] [Severity: Info] [Priority: P3] Meaning-Check: NEEDS-LLM "
            f"{finding['kind']} {finding['term']} at {location}"
        )
        if finding["kind"] == "banned":
            rendered = []
            for candidate in finding["candidates"]:
                slot = candidate.get("slot")
                rendered.append(
                    f"{candidate['text']} (slot: {slot})" if slot else candidate["text"]
                )
            lines.append("  candidates: " + "; ".join(rendered))
        else:
            lines.append(f"  canonical: {finding['canonical']}")
    return lines


def _abbreviation_style_report_lines(result: dict[str, Any]) -> list[str]:
    lines = [
        "\n[4] Abbreviation Style / 缩写体例",
        "-" * 40,
        f"项目形式: {result['project_form']}",
    ]
    findings = result["findings"]
    notes = result["coverage_notes"]
    if findings:
        lines.append(f"Status: {len(findings)} candidates")
    elif notes:
        lines.append("Status: coverage incomplete")
    else:
        lines.append("Status: no abbreviation-style candidates in scanned text")
    lines.extend(notes)
    for finding in findings:
        location = f"{finding['file']}:{finding['line']}"
        lines.append(
            "[Script] [Severity: Info] [Priority: P3] Meaning-Check: NEEDS-LLM "
            f"{finding['kind']} {finding['term']} {finding['abbreviation']} at {location}"
        )
        if finding.get("field"):
            lines.append(f"  field: {finding['field']}")
        if finding.get("detail"):
            lines.append(f"  detail: {finding['detail']}")
    return lines


def _optional_text(
    governance_result: dict[str, Any] | None, style_result: dict[str, Any] | None
) -> str:
    lines: list[str] = []
    if governance_result is not None:
        lines.extend(_governance_report_lines(governance_result))
    if style_result is not None:
        lines.extend(_abbreviation_style_report_lines(style_result))
    return "\n".join(lines)


def _attach_optional_results(
    checker: ConsistencyChecker,
    payload: dict[str, Any],
    *,
    governance: bool,
    abbreviation_style: bool,
    abbrev_issues: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if governance:
        payload["governance"] = checker.check_governance()
    if abbreviation_style:
        style = checker.check_abbreviation_style()
        style["findings"] = dedupe_style_findings(style["findings"], abbrev_issues)
        style["status"] = _result_status(style["findings"], style["coverage_notes"])
        payload["abbreviation_style"] = style
    return payload


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
        "--governance",
        action="store_true",
        help="Check banned terms, locked names, and extra exempt environments; requires --custom-terms",
    )
    parser.add_argument(
        "--abbreviation-style",
        action="store_true",
        help="Check qualified full forms, later XOR candidates, and Title Case in those forms",
    )
    parser.add_argument(
        "--all-files",
        action="store_true",
        help="Scan every .tex under the project root (legacy rglob), "
        "instead of only files reachable from the main file's include graph",
    )

    args = parser.parse_args()

    governance_config = None
    if args.governance:
        if not args.custom_terms:
            print("[ERROR] --governance requires --custom-terms", file=sys.stderr)
            sys.exit(1)
        try:
            governance_config = load_governance_terms(args.custom_terms)
        except GovernanceConfigError as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            sys.exit(1)

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
        custom_terms_file=None if args.governance else args.custom_terms,
        entry_file=(
            args.tex_file if not args.all_files and Path(args.tex_file).is_file() else None
        ),
        governance=governance_config,
    )

    if args.terms:
        result = checker.check_terms()
        if args.governance or args.abbreviation_style:
            result = _attach_optional_results(
                checker,
                result,
                governance=args.governance,
                abbreviation_style=args.abbreviation_style,
            )
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\nTerm consistency: {result['status']}")
            for inc in result["inconsistencies"]:
                print(f"  - {inc['suggestion']}")
            optional = _optional_text(
                result.get("governance") if args.governance else None,
                result.get("abbreviation_style") if args.abbreviation_style else None,
            )
            if optional:
                print(optional)
        sys.exit(0)

    if args.abbreviations:
        result = checker.check_abbreviations()
        if args.governance or args.abbreviation_style:
            result = _attach_optional_results(
                checker,
                result,
                governance=args.governance,
                abbreviation_style=args.abbreviation_style,
                abbrev_issues=result["issues"],
            )
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\nAbbreviation check: {result['status']}")
            for issue in result["issues"]:
                print(f"  - {issue['message']}")
            optional = _optional_text(
                result.get("governance") if args.governance else None,
                result.get("abbreviation_style") if args.abbreviation_style else None,
            )
            if optional:
                print(optional)
        sys.exit(0)

    # Full check
    terms_result = checker.check_terms()
    abbrev_result = checker.check_abbreviations()
    governance_result = checker.check_governance() if args.governance else None
    style_result = None
    if args.abbreviation_style:
        style_result = checker.check_abbreviation_style()
        style_result["findings"] = dedupe_style_findings(
            style_result["findings"], abbrev_result["issues"]
        )
        style_result["status"] = _result_status(
            style_result["findings"], style_result["coverage_notes"]
        )

    if args.json:
        output = {
            "terms": terms_result,
            "abbreviations": abbrev_result,
        }
        if governance_result is not None:
            output["governance"] = governance_result
        if style_result is not None:
            output["abbreviation_style"] = style_result
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(checker.generate_report(terms_result, abbrev_result, governance_result, style_result))

    # Exit code
    if terms_result["status"] != "PASS" or abbrev_result["status"] != "PASS":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
