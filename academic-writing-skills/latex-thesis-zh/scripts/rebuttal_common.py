#!/usr/bin/env python3
"""
Shared helpers for the latex-thesis-zh rebuttal scripts.

rebuttal_intake.py, rebuttal_build.py, and rebuttal_check.py import this module.
It reads aux labels with page numbers, maps bibliography numbers to keys, finds
anchors (figure, table, equation, chapter, section, reference) in review text,
reads and writes the concern ledger, formats R-* result lines, and lists the
files that changed in the thesis git repository. It never writes into the thesis.

Contract: references/rebuttal-workflow.md and references/rebuttal-gate.md.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import yaml

try:
    import tex_loader
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import tex_loader

CN_DIGITS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def skip_ws(text: str, pos: int) -> int:
    while pos < len(text) and text[pos] in " \t\r\n":
        pos += 1
    return pos


def read_group(text: str, pos: int) -> tuple[str, int]:
    """Read the balanced ``{...}`` group that starts at ``pos``.

    Returns the inner text and the index after the closing brace. Escaped
    braces ``\\{`` and ``\\}`` do not change the depth. Raises ValueError when
    no group starts at ``pos`` or the group is not closed.
    """
    if pos >= len(text) or text[pos] != "{":
        raise ValueError("group expected")
    depth = 0
    index = pos
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[pos + 1 : index], index + 1
        index += 1
    raise ValueError("unclosed group")


def cn_to_int(value: str) -> int | None:
    """Convert 1..99 in Arabic or Chinese numerals (一 to 九十九) to int."""
    value = value.strip()
    if value.isdigit():
        return int(value)
    if value == "十":
        return 10
    if len(value) == 1:
        return CN_DIGITS.get(value)
    if len(value) == 2 and value[0] == "十" and value[1] in CN_DIGITS:
        return 10 + CN_DIGITS[value[1]]
    if len(value) == 2 and value[1] == "十" and value[0] in CN_DIGITS:
        return CN_DIGITS[value[0]] * 10
    if len(value) == 3 and value[1] == "十" and value[0] in CN_DIGITS and value[2] in CN_DIGITS:
        return CN_DIGITS[value[0]] * 10 + CN_DIGITS[value[2]]
    return None


NUMBER_RE = re.compile(r"\d+(?:\.\d+)*")
FULLWIDTH = str.maketrans("０１２３４５６７８９．", "0123456789.")
THOUSANDS_RE = re.compile(r"(?<=\d)(?:,|\{,\})(?=\d{3}(?!\d))")
# Structural numbers that R-NUM-SRC does not compare with the thesis.
NUMBER_EXCLUDED_RES = (
    re.compile(r"[图表式]\s*[（(]?\s*\d+(?:\s*[-－.．]\s*\d+)+"),
    re.compile(r"第\s*\d+\s*章"),
    re.compile(r"研究内容\s*\d+"),
    re.compile(r"\d+(?:\.\d+)*\s*节"),
)


def normalize_digits(text: str) -> str:
    """Full-width digits become ASCII digits; thousands separators between digits go."""
    return THOUSANDS_RE.sub("", text.translate(FULLWIDTH))


def load_thesis_numbers(inventory: dict, root: Path) -> set[str] | None:
    """Numbers of the assembled thesis source; None when the thesis cannot be read."""
    main = root / str(inventory.get("main_tex") or "")
    if not main.is_file():
        return None
    try:
        document = tex_loader.assemble(main)
    except (OSError, ValueError):
        return None
    text = "\n".join(tex_loader.COMMENT_RE.sub("", line) for line in document.lines)
    return set(NUMBER_RE.findall(normalize_digits(text)))


LEDGER_SCHEMA = "rebuttal-ledger/1"
STATE_SCHEMA = "rebuttal-state/1"
PRIORITY = {"Critical": "P0", "Major": "P1", "Minor": "P2", "Info": "P3"}

# hyperref anchor prefix -> anchor kind; label prefix is the fallback without hyperref
ANCHOR_KIND_BY_DEST = (
    ("figure", "figure"),
    ("table", "table"),
    ("equation", "equation"),
    ("algorithm", "algorithm"),
    ("chapter", "chapter"),
    ("section", "section"),
    ("subsection", "section"),
    ("subsubsection", "section"),
)
ANCHOR_KIND_BY_LABEL = (
    ("fig:", "figure"),
    ("tab:", "table"),
    ("eq:", "equation"),
    ("alg:", "algorithm"),
    ("chap:", "chapter"),
    ("ch:", "chapter"),
    ("sec:", "section"),
)

_SEP = r"\s*[-.－—–]\s*"
_FLOAT_NUMBER = rf"(\d+{_SEP}\d+)"
_CN_NUMBER = r"([0-9]+|[一二三四五六七八九十]+)"
ANCHOR_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("figure", re.compile(rf"图\s*{_FLOAT_NUMBER}")),
    ("table", re.compile(rf"表\s*{_FLOAT_NUMBER}")),
    ("equation", re.compile(rf"(?:公式|式)\s*[(（]\s*{_FLOAT_NUMBER}\s*[)）]")),
    ("algorithm", re.compile(rf"算法\s*{_FLOAT_NUMBER}")),
    (
        "chapter_range",
        re.compile(rf"第\s*{_CN_NUMBER}\s*章\s*(?:至|到|~|～|-|—|–)\s*第\s*{_CN_NUMBER}\s*章"),
    ),
    ("chapter", re.compile(rf"第\s*{_CN_NUMBER}\s*章")),
    ("section", re.compile(r"(?<![\d.])(\d+\.\d+(?:\.\d+)?)\s*(?:节|小节)")),
    ("reference", re.compile(r"文献\s*\[\s*([\d\s,，、\-–—]+?)\s*\]")),
)


@dataclass(frozen=True)
class AuxLabel:
    label: str
    number: str
    page: str
    title: str
    kind: str | None
    file: str


@dataclass(frozen=True)
class Anchor:
    text: str
    kind: str
    key: str


def _label_kind(label: str, dest: str) -> str | None:
    for prefix, kind in ANCHOR_KIND_BY_DEST:
        if dest == prefix or dest.startswith(prefix + "."):
            return kind
    for prefix, kind in ANCHOR_KIND_BY_LABEL:
        if label.startswith(prefix):
            return kind
    return None


def _aux_files(root: Path) -> list[Path]:
    """Every ``*.aux`` under ``root``, hidden directories skipped, shallower files first."""
    files = [
        path
        for path in root.rglob("*.aux")
        if not any(part.startswith(".") for part in path.relative_to(root).parts[:-1])
    ]
    files.sort(key=lambda path: (len(path.relative_to(root).parts), path.as_posix()))
    return files


def load_aux_labels(root: Path) -> dict[str, AuxLabel]:
    """``\\newlabel`` entries with number, page, title, and kind from every aux under ``root``.

    Same file rule as ``extract_thesis.load_aux_numbers``: hidden directories are
    skipped, shallower files win, ``sub@`` labels are dropped.
    """
    labels: dict[str, AuxLabel] = {}
    for path in _aux_files(root):
        text = tex_loader.read_text_robust(path)[0]
        rel = path.relative_to(root).as_posix()
        for match in re.finditer(r"\\newlabel\s*(?=\{)", text):
            try:
                label, pos = read_group(text, match.end())
                data, _ = read_group(text, skip_ws(text, pos))
            except ValueError:
                continue
            if label.startswith("sub@") or label in labels:
                continue
            groups: list[str] = []
            inner = skip_ws(data, 0)
            while inner < len(data) and data[inner] == "{" and len(groups) < 4:
                try:
                    group, inner = read_group(data, inner)
                except ValueError:
                    break
                groups.append(group.replace("\\relax", "").strip())
                inner = skip_ws(data, inner)
            if not groups or not groups[0]:
                continue
            groups += [""] * (4 - len(groups))
            number, page, title, dest = groups[:4]
            labels[label] = AuxLabel(label, number, page, title, _label_kind(label, dest), rel)
    return labels


def load_bibcites(root: Path) -> dict[str, str]:
    """Bibliography number -> bib key from ``\\bibcite{key}{{n}...}`` in every aux."""
    cites: dict[str, str] = {}
    for path in _aux_files(root):
        text = tex_loader.read_text_robust(path)[0]
        for match in re.finditer(r"\\bibcite\s*(?=\{)", text):
            try:
                key, pos = read_group(text, match.end())
                data, _ = read_group(text, skip_ws(text, pos))
                start = skip_ws(data, 0)
                number = read_group(data, start)[0] if data[start : start + 1] == "{" else data
            except ValueError:
                continue
            number = number.strip()
            if number.isdigit():
                cites.setdefault(number, key)
    return cites


def _normalize_float_number(raw: str) -> str:
    return "-".join(re.split(_SEP, raw.strip()))


def _reference_numbers(raw: str) -> list[str]:
    numbers: list[str] = []
    for part in re.split(r"[,，、]", raw):
        part = part.strip()
        bounds = re.split(r"\s*[-–—]\s*", part)
        if len(bounds) == 2 and bounds[0].isdigit() and bounds[1].isdigit():
            low, high = int(bounds[0]), int(bounds[1])
            if low <= high and high - low <= 50:
                numbers.extend(str(value) for value in range(low, high + 1))
                continue
        if part.isdigit():
            numbers.append(part)
    return numbers


def find_anchors(text: str) -> list[Anchor]:
    """Anchors in review text, in order of appearance, without duplicates.

    Chapter ranges such as 「第3章至第5章」 expand to one chapter anchor per chapter;
    reference lists such as 「文献[1,2]」 expand to one anchor per number.
    """
    found: list[tuple[int, Anchor]] = []
    covered: list[tuple[int, int]] = []

    def free(start: int, end: int) -> bool:
        return all(end <= low or start >= high for low, high in covered)

    for kind, pattern in ANCHOR_PATTERNS:
        for match in pattern.finditer(text):
            if not free(match.start(), match.end()):
                continue
            anchors: list[Anchor] = []
            if kind in ("figure", "table", "equation", "algorithm"):
                anchors.append(
                    Anchor(match.group(0), kind, _normalize_float_number(match.group(1)))
                )
            elif kind == "chapter_range":
                low, high = cn_to_int(match.group(1)), cn_to_int(match.group(2))
                if low is None or high is None or low > high or high - low > 20:
                    continue
                anchors.extend(
                    Anchor(match.group(0), "chapter", str(value)) for value in range(low, high + 1)
                )
            elif kind == "chapter":
                number = cn_to_int(match.group(1))
                if number is None:
                    continue
                anchors.append(Anchor(match.group(0), "chapter", str(number)))
            elif kind == "section":
                anchors.append(Anchor(match.group(0), "section", match.group(1)))
            elif kind == "reference":
                anchors.extend(
                    Anchor(match.group(0), "reference", number)
                    for number in _reference_numbers(match.group(1))
                )
            if anchors:
                covered.append((match.start(), match.end()))
                found.extend((match.start(), anchor) for anchor in anchors)
    found.sort(key=lambda item: item[0])
    result: list[Anchor] = []
    for _, anchor in found:
        if anchor not in result:
            result.append(anchor)
    return result


def load_ledger(path: Path) -> dict:
    """Read the YAML ledger and check its ``schema`` field (ValueError on mismatch)."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != LEDGER_SCHEMA:
        raise ValueError(f"{path} 不是 {LEDGER_SCHEMA} 台账")
    return data


def dump_ledger(path: Path, data: dict) -> None:
    text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000)
    path.write_text(text, encoding="utf-8", newline="\n")


def load_state(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != STATE_SCHEMA:
        raise ValueError(f"{path} 不是 {STATE_SCHEMA} 状态文件")
    return data


def dump_state(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


@dataclass
class Finding:
    code: str
    severity: str
    concern: str
    file: str
    line: int | None
    message: str

    @property
    def priority(self) -> str:
        return PRIORITY[self.severity]

    def as_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "severity": self.severity,
            "priority": self.priority,
            "source_kind": "script",
            "concern": self.concern,
            "file": self.file,
            "line": self.line,
            "message": self.message,
        }


def render_findings(findings: list[Finding], skipped: list[str]) -> list[str]:
    """R-* result lines in the D-* format, followed by one summary line."""
    lines = []
    for finding in findings:
        location = f"{finding.file}:{finding.line if finding.line is not None else '-'}"
        lines.append(
            f"% {finding.code} (concern={finding.concern}, {location}) "
            f"[Severity: {finding.severity}] [Priority: {finding.priority}]: "
            f"[Script] {finding.message}"
        )
    summary = {severity: sum(f.severity == severity for f in findings) for severity in PRIORITY}
    counts = "，".join(f"{severity} {summary[severity]}" for severity in PRIORITY)
    lines.append(f"% 汇总：{counts}；skipped：{'、'.join(skipped) or '无'}")
    return lines


def emit(findings: list[Finding], skipped: list[str], as_json: bool) -> dict[str, object]:
    """Print the findings and return the JSON payload."""
    summary = {severity: sum(f.severity == severity for f in findings) for severity in PRIORITY}
    payload: dict[str, object] = {
        "findings": [finding.as_dict() for finding in findings],
        "summary": summary,
        "skipped": skipped,
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for line in render_findings(findings, skipped):
            print(line)
    return payload


def _git(thesis: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            # --no-optional-locks: diff must not refresh the index of the read-only thesis repo
            ["git", "--no-optional-locks", "-C", str(thesis), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError:
        return None


def git_head(thesis: Path) -> str | None:
    """``git rev-parse HEAD`` of the thesis repository, or None outside git."""
    result = _git(thesis, "rev-parse", "HEAD")
    if result is None or result.returncode != 0:
        return None
    return result.stdout.strip() or None


def git_changed_files(thesis: Path, base: str) -> set[str] | None:
    """POSIX paths relative to ``thesis`` changed since ``base``, plus untracked files.

    Committed changes come from ``git diff base HEAD``; uncommitted and untracked
    files come from ``git status``. ``git diff base`` against the work tree is not
    used because it rewrites ``.git/index`` even with ``--no-optional-locks``.
    Both lists are limited to ``thesis`` when it is a subdirectory of the
    repository. Returns None when ``thesis`` is not a git repository or a git
    command fails.
    """
    results = (
        _git(thesis, "diff", "--name-only", "--relative", base, "HEAD"),
        _git(thesis, "status", "--porcelain", "-z", "-uall", "--", "."),
        _git(thesis, "rev-parse", "--show-prefix"),
    )
    if any(result is None or result.returncode != 0 for result in results):
        return None
    diff, status, prefix = (result.stdout for result in results if result is not None)
    prefix = prefix.strip()
    files = {line.strip() for line in diff.splitlines() if line.strip()}
    entries = status.split("\0")
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if len(entry) < 4:
            continue
        if entry[0] in "RC":
            index += 1  # a rename or copy entry is followed by its source path
        path = entry[3:]
        files.add(path[len(prefix) :] if prefix and path.startswith(prefix) else path)
    return {path.replace("\\", "/") for path in files}


# ---------------------------------------------------------------------------
# Shared by rebuttal_build.py and rebuttal_check.py
# ---------------------------------------------------------------------------

ACTIONS = ("revise", "add", "clarify", "partial", "future_work", "decline")
MODIFYING_ACTIONS = ("revise", "add", "partial")
STATUSES = ("open", "planned", "done", "needs_user_input")
OWNERS = ("latex-thesis-zh", "drawio", "manual", "none")
EVIDENCE_KINDS = ("git_diff", "user_confirmed", "none")
CATEGORIES = (
    "writing",
    "figure",
    "table",
    "reference",
    "structure",
    "experiment",
    "generalization",
    "theory",
    "complexity",
    "deployment",
    "application",
    "innovation",
    "other",
)
SEVERITIES = tuple(PRIORITY)
CONCERN_ID_RE = re.compile(r"^(R\d+)-(\d+)([a-z]?)$")
REVIEW_ITEM_RE = re.compile(r"^(\d+)\. (.*)$")
KIND_PREFIX = {"figure": "图", "table": "表", "equation": "式", "algorithm": "算法"}


def anchor_form(kind: str | None, number: str) -> str:
    """Thesis wording of an anchor number: 图2-1, 式(2-1), 第2章, 第2.3节, 参考文献[3]."""
    if kind == "equation":
        return f"式({number})"
    if kind in KIND_PREFIX:
        return f"{KIND_PREFIX[kind]}{number}"
    if kind == "chapter":
        return f"第{number}章"
    if kind == "section":
        return f"第{number}节"
    if kind == "reference":
        return f"参考文献[{number}]"
    return number


def concern_ref(concern_id: str) -> str:
    """Form wording of a concern id: R1-3b -> 评阅人1意见3（2）."""
    match = CONCERN_ID_RE.match(concern_id)
    if not match:
        return concern_id
    text = f"评阅人{match.group(1)[1:]}意见{match.group(2)}"
    if match.group(3):
        text += f"（{ord(match.group(3)) - ord('a') + 1}）"
    return text


def load_review_items(workspace: Path) -> dict[str, list[str]]:
    """Numbered shortcomings of every ``workspace/reviews/R<n>.md``, by reviewer id."""
    items: dict[str, list[str]] = {}
    for path in sorted((workspace / "reviews").glob("R*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        start = next((i for i, line in enumerate(lines) if line == "## 不足之处和建议"), None)
        found: list[str] = []
        for line in lines[start + 1 :] if start is not None else []:
            match = REVIEW_ITEM_RE.match(line)
            if match and int(match.group(1)) == len(found) + 1:
                found.append(match.group(2))
        items[path.stem] = found
    return items


def aux_tex(aux_file: str) -> str:
    """Source file of a chapter aux: chapters/chapter2.aux -> chapters/chapter2.tex."""
    return aux_file[: -len(".aux")] + ".tex" if aux_file.endswith(".aux") else aux_file


def reverse_cites(cites: dict[str, str]) -> dict[str, str]:
    """Bib key -> bibliography number."""
    return {key: number for number, key in cites.items()}
