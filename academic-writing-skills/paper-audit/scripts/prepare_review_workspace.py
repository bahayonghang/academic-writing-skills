"""Prepare a deep-review workspace from a paper source file."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from build_claim_map import build_claim_map
from checkpoint import init_checkpoint
from detect_language import detect_language
from parsers import extract_title, get_parser
from paths import WorkspaceLayout

# Defensive source reader (utf-8 -> latin-1 -> replace); identical helper lives
# in tex_loader / typ_loader and is format-independent.
try:
    from tex_loader import AssembledDocument, assemble, read_text_robust
except ImportError:  # pragma: no cover - loader always vendored alongside
    try:
        from typ_loader import read_text_robust
    except ImportError:
        read_text_robust = None  # type: ignore[assignment]


SUBSECTION_CONTEXT_MIN_HAN = 20
SUBSECTION_CONTEXT_MIN_HAN_RATIO = 0.30
SUBSECTION_CONTEXT_MIN_VISIBLE = 60

_CONTEXT_EXEMPT_SECTIONS = {
    "abstract",
    "conclusion",
    "acknowledgment",
    "appendix",
    "organization",
    "summary",
}
_CONTEXT_BEGIN_ENV_RE = re.compile(r"\\begin\{([^}]+)\}")
_CONTEXT_END_ENV_RE = re.compile(r"\\end\{([^}]+)\}")
_CONTEXT_PROTECTED_ENVS = {
    "equation",
    "align",
    "alignat",
    "flalign",
    "gather",
    "multline",
    "eqnarray",
    "displaymath",
    "figure",
    "table",
    "tabular",
    "tabularx",
    "longtable",
    "algorithm",
    "algorithmic",
    "itemize",
    "enumerate",
    "description",
    "lstlisting",
    "verbatim",
    "minted",
    "abstract",
    "eabstract",
    "cabstract",
    "acknowledgment",
    "acknowledgement",
    "acknowledgments",
    "acknowledgements",
}


@dataclass(frozen=True)
class SubsectionUnit:
    """A numbered depth-3 unit with assembled and source coordinates."""

    subsection_id: str
    title: str
    depth: int
    parent_id: str
    source_file: str
    source_start: int
    source_end: int
    assembled_start: int
    assembled_end: int
    section_scope: str | None

    def public_payload(self) -> dict[str, object]:
        """Return the source-coordinate-only representation written to JSON."""
        return {
            "subsection_id": self.subsection_id,
            "title": self.title,
            "depth": self.depth,
            "parent_id": self.parent_id,
            "source_file": self.source_file,
            "source_start": self.source_start,
            "source_end": self.source_end,
        }


@dataclass(frozen=True)
class ContextParagraph:
    """Visible prose and structural flags needed to assemble context windows."""

    start: int
    end: int
    visible: str
    section: str | None
    in_item: bool
    ends_with_env: bool


def slugify(value: str) -> str:
    """Convert a filename or title into a filesystem-safe slug."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "paper"


def _section_lines(lines: list[str], start: int, end: int, zero_based: bool) -> str:
    if zero_based:
        return "\n".join(lines[start : end + 1]).strip()
    return "\n".join(lines[max(0, start - 1) : end]).strip()


def _clean_summary_line(text: str) -> str:
    """Normalize extracted summary text for reviewer-facing artifacts."""
    normalized = re.sub(r"^#+\s*", "", text.strip())
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = re.sub(
        r"^(abstract|introduction|conclusion|discussion|method|methods|results)\s+",
        "",
        normalized,
        flags=re.IGNORECASE,
    )
    return normalized.strip(" -")


def _rewrite_research_focus(text: str) -> str:
    """Rewrite extracted prose into a more question/topic-oriented summary phrase."""
    cleaned = _clean_summary_line(text).rstrip(".")
    lowered = cleaned.lower()
    if lowered.startswith("we achieve state-of-the-art efficiency across "):
        tail = cleaned[39:].strip()
        tail = re.sub(r"^across\s+", "", tail, flags=re.IGNORECASE)
        return "improved efficiency across " + tail
    if lowered.startswith("we achieve "):
        return cleaned[11:].strip()
    if lowered.startswith("we propose "):
        return "a method for " + cleaned[11:].strip()
    if lowered.startswith("this paper proposes "):
        body = cleaned[19:].strip()
        body = re.sub(r"^a\s+", "", body, flags=re.IGNORECASE)
        body = re.sub(r"\s+and\s+claims\s+", " and ", body, flags=re.IGNORECASE)
        return "a proposed method offering " + body
    if lowered.startswith("we demonstrate "):
        return cleaned[15:].strip()
    if lowered.startswith("we show "):
        return cleaned[8:].strip()
    return cleaned


def _first_nonempty_sentence(text: str) -> str:
    """Return the first plausible sentence from a section chunk."""
    cleaned = _clean_summary_line(text)
    if not cleaned:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    return next((part.strip() for part in parts if part.strip()), cleaned)


def _infer_research_question(section_texts: dict[str, str]) -> str:
    """Infer a concise research-question sentence from abstract/introduction."""
    for key in ("abstract", "introduction"):
        chunk = section_texts.get(key, "")
        sentence = _first_nonempty_sentence(chunk)
        if sentence:
            return _rewrite_research_focus(sentence)
    return "Research question could not be inferred automatically from the current source."


def _infer_core_thesis(claim_map: dict, section_texts: dict[str, str]) -> str:
    """Infer the paper's central thesis from claim map or key sections."""
    for claim in claim_map.get("headline_claims", []):
        cleaned = _clean_summary_line(claim)
        if cleaned:
            return cleaned
    for key in ("introduction", "abstract", "method"):
        chunk = section_texts.get(key, "")
        sentence = _first_nonempty_sentence(chunk)
        if sentence:
            return sentence
    return "Core thesis could not be inferred automatically from the current source."


def _section_base(key: str | None) -> str | None:
    return re.sub(r"_\d+$", "", key) if key is not None else None


def _special_ranges(content: str, parser) -> list[tuple[int, int, str]]:
    """Return structural ranges that must never become subsection units."""
    headings = parser.extract_headings(content)
    total = len(content.splitlines())
    ranges: list[tuple[int, int, str]] = []
    for index, heading in enumerate(headings):
        title = str(heading["title"]).strip().lower()
        kind = None
        if "致谢" in title or "acknowledg" in title:
            kind = "acknowledgment"
        elif title.startswith("附录") or title.startswith("appendix"):
            kind = "appendix"
        if kind is None:
            continue
        end = total
        for following in headings[index + 1 :]:
            if int(following["level"]) <= int(heading["level"]):
                end = int(following["line"]) - 1
                break
        ranges.append((int(heading["line"]), end, kind))
    return ranges


def _section_at(
    line_no: int,
    sections: dict[str, tuple[int, int]],
    special_ranges: list[tuple[int, int, str]],
    chapter_ranges: list[dict[str, Any]],
    appendix_start: int | None,
) -> str | None:
    for start, end, kind in special_ranges:
        if start <= line_no <= end:
            return kind
    if appendix_start is not None and line_no >= appendix_start:
        return "appendix"
    for key, (start, end) in sections.items():
        if start <= line_no <= end:
            return _section_base(key)
    for chapter in chapter_ranges:
        if int(chapter["start"]) <= line_no <= int(chapter["end"]):
            key = chapter.get("key")
            return _section_base(key) if isinstance(key, str) else None
    return None


def _heading_is_starred(doc: AssembledDocument, heading: dict[str, Any]) -> bool:
    """Recover the unnumbered marker omitted by parser heading records."""
    line_no = int(heading["line"])
    if not 1 <= line_no <= len(doc.lines):
        return False
    command = re.escape(str(heading["command"]))
    source = re.sub(r"(?<!\\)%.*$", "", doc.lines[line_no - 1])
    return re.search(rf"\\{command}\*", source) is not None


def _source_span(
    doc: AssembledDocument,
    assembled_start: int,
    assembled_end: int,
) -> tuple[str, int, int]:
    """Project an assembled span onto the source file that owns its start."""
    source_file, source_start = doc.origin(assembled_start)
    source_end = source_start
    for line_no in range(assembled_end, assembled_start - 1, -1):
        end_file, end_line = doc.origin(line_no)
        if end_file == source_file:
            source_end = end_line
            break
    return source_file, source_start, source_end


def build_subsection_units(assembled: AssembledDocument, parser) -> list[SubsectionUnit]:
    """Build all numbered depth-3 units from the assembled heading stream."""
    headings = parser.extract_headings(assembled.content)
    if not headings:
        return []

    root_level = min(int(heading["level"]) for heading in headings)
    sections = parser.split_sections(assembled.content)
    special_ranges = _special_ranges(assembled.content, parser)
    chapter_ranges = parser.chapter_ranges(assembled.content)
    appendix_start = next(
        (
            line_no
            for line_no, raw in enumerate(assembled.lines, 1)
            if raw.strip().startswith(r"\appendix")
        ),
        None,
    )
    counters = [0, 0, 0]
    root_numbered = False
    parent_numbered = False
    units: list[SubsectionUnit] = []

    for index, heading in enumerate(headings):
        depth = int(heading["level"]) - root_level + 1
        if depth > 3:
            continue
        if _heading_is_starred(assembled, heading):
            if depth == 1:
                counters[1:] = [0, 0]
                root_numbered = False
                parent_numbered = False
            elif depth == 2:
                counters[2] = 0
                parent_numbered = False
            continue

        counters[depth - 1] += 1
        for deeper in range(depth, 3):
            counters[deeper] = 0
        if depth == 1:
            root_numbered = True
            parent_numbered = False
            continue
        if depth == 2:
            parent_numbered = root_numbered
            continue
        if not root_numbered or not parent_numbered or counters[0] <= 0 or counters[1] <= 0:
            continue

        assembled_start = int(heading["line"])
        assembled_end = len(assembled.lines)
        for following in headings[index + 1 :]:
            following_depth = int(following["level"]) - root_level + 1
            if following_depth <= 3:
                assembled_end = int(following["line"]) - 1
                break
        assembled_end = max(assembled_start, assembled_end)
        section_scope = _section_at(
            assembled_start,
            sections,
            special_ranges,
            chapter_ranges,
            appendix_start,
        )
        if section_scope in _CONTEXT_EXEMPT_SECTIONS:
            continue

        subsection_id = ".".join(str(value) for value in counters)
        source_file, source_start, source_end = _source_span(
            assembled,
            assembled_start,
            assembled_end,
        )
        units.append(
            SubsectionUnit(
                subsection_id=subsection_id,
                title=str(heading["title"]).strip(),
                depth=depth,
                parent_id=".".join(str(value) for value in counters[:2]),
                source_file=source_file,
                source_start=source_start,
                source_end=source_end,
                assembled_start=assembled_start,
                assembled_end=assembled_end,
                section_scope=section_scope,
            )
        )
    return units


def _env_name(value: str) -> str:
    return value.rstrip("*")


def _split_context_paragraphs(content: str, parser) -> list[ContextParagraph]:
    """Split visible prose while preserving heading and environment boundaries."""
    lines = content.split("\n")
    sections = parser.split_sections(content)
    headings = parser.extract_headings(content)
    heading_lines = {int(heading["line"]) for heading in headings}
    special_ranges = _special_ranges(content, parser)
    chapter_ranges = parser.chapter_ranges(content)
    appendix_start = next(
        (line_no for line_no, raw in enumerate(lines, 1) if raw.strip().startswith(r"\appendix")),
        None,
    )
    paragraphs: list[ContextParagraph] = []
    buffer: list[tuple[int, str, str]] = []
    in_protected_env: str | None = None

    def flush(*, ends_with_env: bool = False) -> None:
        nonlocal buffer
        if not buffer:
            return
        meaningful = [row for row in buffer if row[2] or r"\cite" in row[1]]
        if meaningful:
            visible = " ".join(part for _line, _raw, part in meaningful if part).strip()
            if visible:
                start = meaningful[0][0]
                paragraphs.append(
                    ContextParagraph(
                        start=start,
                        end=meaningful[-1][0],
                        visible=visible,
                        section=_section_at(
                            start,
                            sections,
                            special_ranges,
                            chapter_ranges,
                            appendix_start,
                        ),
                        in_item=any(
                            source.lstrip().startswith(r"\item")
                            for _line, source, _visible in buffer
                        ),
                        ends_with_env=ends_with_env,
                    )
                )
        buffer = []

    for line_no, source in enumerate(lines, 1):
        stripped = re.sub(r"(?<!\\)%.*$", "", source).strip()
        if in_protected_env is not None:
            if (
                (in_protected_env == "bracket-math" and r"\]" in stripped)
                or (in_protected_env == "dollar-math" and "$$" in stripped)
                or (
                    in_protected_env not in {"bracket-math", "dollar-math"}
                    and any(
                        _env_name(match.group(1)) == in_protected_env
                        for match in _CONTEXT_END_ENV_RE.finditer(stripped)
                    )
                )
            ):
                in_protected_env = None
            continue

        if line_no in heading_lines or stripped.startswith(r"\appendix"):
            flush()
            continue

        bracket_math = r"\[" in stripped
        dollar_math = "$$" in stripped
        if bracket_math or dollar_math:
            flush(ends_with_env=True)
            if bracket_math and r"\]" not in stripped:
                in_protected_env = "bracket-math"
            elif dollar_math and stripped.count("$$") < 2:
                in_protected_env = "dollar-math"
            continue

        protected_begin = next(
            (
                _env_name(match.group(1))
                for match in _CONTEXT_BEGIN_ENV_RE.finditer(stripped)
                if _env_name(match.group(1)) in _CONTEXT_PROTECTED_ENVS
            ),
            None,
        )
        if protected_begin is not None:
            flush(ends_with_env=True)
            if not any(
                _env_name(match.group(1)) == protected_begin
                for match in _CONTEXT_END_ENV_RE.finditer(stripped)
            ):
                in_protected_env = protected_begin
            continue

        if not stripped or stripped == r"\par" or source.lstrip().startswith("%"):
            flush()
            continue
        if stripped.startswith(r"\item"):
            flush()
            continue

        visible = parser.extract_visible_text(stripped).strip()
        buffer.append((line_no, stripped, visible))
    flush()
    return paragraphs


def _context_is_eligible(
    paragraph: ContextParagraph,
    language: str | None = None,
) -> bool:
    visible = paragraph.visible
    han = len(re.findall(r"[\u4e00-\u9fff]", visible))
    visible_count = len(re.sub(r"\s+", "", visible))
    chinese_length_ok = (
        han >= SUBSECTION_CONTEXT_MIN_HAN
        and han / max(len(visible), 1) >= SUBSECTION_CONTEXT_MIN_HAN_RATIO
    )
    if language == "zh":
        language_length_ok = chinese_length_ok
    elif language == "en":
        language_length_ok = visible_count >= SUBSECTION_CONTEXT_MIN_VISIBLE
    else:
        language_length_ok = chinese_length_ok or visible_count >= SUBSECTION_CONTEXT_MIN_VISIBLE
    return (
        language_length_ok
        and paragraph.section not in _CONTEXT_EXEMPT_SECTIONS
        and not paragraph.in_item
        and not paragraph.ends_with_env
    )


def _eligible_paragraphs(
    paragraphs: list[ContextParagraph],
    start: int,
    end: int,
    language: str | None,
) -> list[ContextParagraph]:
    return [
        paragraph
        for paragraph in paragraphs
        if start <= paragraph.start
        and paragraph.end <= end
        and _context_is_eligible(paragraph, language)
    ]


def _parent_context_for_unit(
    doc: AssembledDocument,
    parser,
    unit: SubsectionUnit,
) -> tuple[int, int] | None:
    """Return the numbered parent title/lead interval in assembled coordinates."""
    headings = parser.extract_headings(doc.content)
    if not headings:
        return None
    root_level = min(int(heading["level"]) for heading in headings)
    for index in range(len(headings) - 1, -1, -1):
        heading = headings[index]
        if int(heading["line"]) >= unit.assembled_start:
            continue
        depth = int(heading["level"]) - root_level + 1
        if depth < 2:
            break
        if depth == 2 and not _heading_is_starred(doc, heading):
            lead_end = unit.assembled_start - 1
            for following in headings[index + 1 :]:
                following_depth = int(following["level"]) - root_level + 1
                if following_depth <= 3:
                    lead_end = int(following["line"]) - 1
                    break
            return int(heading["line"]), lead_end
    return None


def _context_part(
    doc: AssembledDocument,
    part: str,
    subsection_id: str | None,
    assembled_start: int,
    assembled_end: int,
) -> dict[str, object]:
    source_file, source_start, source_end = _source_span(doc, assembled_start, assembled_end)
    return {
        "part": part,
        "subsection_id": subsection_id,
        "source_file": source_file,
        "source_start": source_start,
        "source_end": source_end,
        "status": "ok",
    }


def build_context_window(
    doc: AssembledDocument,
    parser,
    units: list[SubsectionUnit],
    index: int,
    paragraphs: list[ContextParagraph],
    language: str | None = None,
) -> dict[str, object]:
    """Derive one source-coordinate-only window from the ordered cursor."""
    if not 0 <= index < len(units):
        raise IndexError(index)
    current = units[index]
    previous = units[index - 1] if index > 0 else None
    following = units[index + 1] if index + 1 < len(units) else None
    same_prev = previous.parent_id == current.parent_id if previous is not None else None
    same_next = following.parent_id == current.parent_id if following is not None else None
    payload: dict[str, object] = {
        "subsection_id": current.subsection_id,
        "title": current.title,
        "depth": current.depth,
        "parent_id": current.parent_id,
        "source_file": current.source_file,
        "editable": {
            "part": "current",
            "source_start": current.source_start,
            "source_end": current.source_end,
            "status": "ok",
        },
        "read_only": [],
        "same_parent": {"prev": same_prev, "next": same_next},
        "boundary": "first" if previous is None else "last" if following is None else "",
        "prev_id": previous.subsection_id if previous is not None else None,
        "next_id": following.subsection_id if following is not None else None,
    }
    read_only = payload["read_only"]
    assert isinstance(read_only, list)

    current_paragraphs = _eligible_paragraphs(
        paragraphs,
        current.assembled_start,
        current.assembled_end,
        language,
    )
    payload["current_lead_status"] = "ok" if current_paragraphs else "no_eligible_paragraph"

    if previous is None:
        payload["prev_tail_status"] = "absent"
    else:
        previous_paragraphs = _eligible_paragraphs(
            paragraphs,
            previous.assembled_start,
            previous.assembled_end,
            language,
        )
        if previous_paragraphs:
            payload["prev_tail_status"] = "ok"
            tail = previous_paragraphs[-1]
            read_only.append(
                _context_part(
                    doc,
                    "prev.tail",
                    previous.subsection_id,
                    tail.start,
                    tail.end,
                )
            )
        else:
            payload["prev_tail_status"] = "no_eligible_paragraph"

    if previous is not None and same_prev is False:
        parent_context = _parent_context_for_unit(doc, parser, current)
        parent_paragraphs = (
            _eligible_paragraphs(
                paragraphs,
                parent_context[0] + 1,
                parent_context[1],
                language,
            )
            if parent_context is not None
            else []
        )
        if parent_context is not None and parent_paragraphs:
            payload["parent_lead_status"] = "ok"
            read_only.append(
                _context_part(
                    doc,
                    "parent_lead",
                    None,
                    parent_context[0],
                    parent_paragraphs[-1].end,
                )
            )
        else:
            payload["parent_lead_status"] = "no_eligible_paragraph"

    if following is None:
        payload["next_head_status"] = "absent"
    else:
        following_paragraphs = _eligible_paragraphs(
            paragraphs,
            following.assembled_start,
            following.assembled_end,
            language,
        )
        if following_paragraphs:
            payload["next_head_status"] = "ok"
            head = following_paragraphs[0]
            read_only.append(
                _context_part(
                    doc,
                    "next.head",
                    following.subsection_id,
                    head.start,
                    head.end,
                )
            )
        else:
            payload["next_head_status"] = "no_eligible_paragraph"
    return payload


def prepare_subsection_artifacts(
    source: Path,
    parser,
    layout: WorkspaceLayout,
) -> dict[str, object]:
    """Write the subsection index/windows and return the polish-state projection."""
    layout.data_dir.mkdir(parents=True, exist_ok=True)
    layout.windows_dir.mkdir(parents=True, exist_ok=True)
    for stale_window in layout.windows_dir.glob("*.json"):
        stale_window.unlink()

    units: list[SubsectionUnit] = []
    windows: list[dict[str, object]] = []
    if source.suffix.lower() != ".tex":
        status = "unsupported_format"
    else:
        try:
            assembled = assemble(source)
        except (OSError, UnicodeError, ValueError):
            status = "unsupported_format"
        else:
            units = build_subsection_units(assembled, parser)
            status = "ok" if units else "no_depth3_headings"
            paragraphs = _split_context_paragraphs(assembled.content, parser)
            language = detect_language(parser.clean_text(assembled.content))
            windows = [
                build_context_window(
                    assembled,
                    parser,
                    units,
                    index,
                    paragraphs,
                    language,
                )
                for index in range(len(units))
            ]

    layout.subsection_index.write_text(
        json.dumps(
            {
                "subsection_index_status": status,
                "units": [unit.public_payload() for unit in units],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    state_units: list[dict[str, object]] = []
    for unit, window in zip(units, windows, strict=True):
        window_path = layout.window_file(unit.subsection_id)
        window_path.write_text(
            json.dumps(window, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        state_units.append(
            {
                "subsection_id": unit.subsection_id,
                "window": layout.relative_to_root(window_path),
                "source_file": unit.source_file,
                "editable": window["editable"],
                "read_only": window["read_only"],
            }
        )
    return {
        "status": status,
        "index": layout.relative_to_root(layout.subsection_index),
        "units": state_units,
    }


def build_section_index(content: str, parser, fmt: str) -> list[dict]:
    """Turn parser section tuples into portable section metadata."""
    sections = parser.split_sections(content)
    lines = content.splitlines()
    zero_based = fmt == ".pdf"
    index: list[dict] = []

    for section_key, (start, end) in sections.items():
        body = _section_lines(lines, start, end, zero_based=zero_based)
        index.append(
            {
                "section_key": section_key,
                "title": section_key.replace("_", " ").title(),
                "start_line": start,
                "end_line": end,
                "line_base": 0 if zero_based else 1,
                "word_count": len(body.split()),
                "char_count": len(body),
                "file_name": f"{section_key}.md",
            }
        )

    return sorted(index, key=lambda item: item["start_line"])


def write_summary_stub(
    layout: WorkspaceLayout,
    title: str,
    claim_map: dict,
    section_index: list[dict],
    section_texts: dict[str, str],
) -> None:
    """Write a structured summary stub the reviewer can refine."""
    research_question = _infer_research_question(section_texts)
    core_thesis = _infer_core_thesis(claim_map, section_texts)
    headline_claims = [_clean_summary_line(claim) for claim in claim_map.get("headline_claims", [])]
    headline_claims = [claim for claim in headline_claims if claim]
    closure_targets = [_clean_summary_line(claim) for claim in claim_map.get("closure_targets", [])]
    closure_targets = [claim for claim in closure_targets if claim]

    lines = [
        f"# Paper Summary: {title}",
        "",
        "## Research Question",
        f"- {research_question}",
        "",
        "## Core Thesis",
        f"- {core_thesis}",
        "",
        "## Headline Claims",
    ]
    if headline_claims:
        lines.extend([f"- {claim}" for claim in headline_claims])
    else:
        lines.append("- No headline claim was extracted automatically.")
    lines.extend(["", "## Section Map"])
    for section in section_index:
        lines.append(
            f"- {section['section_key']} ({section['start_line']}-{section['end_line']}): "
            f"{section['word_count']} words"
        )
    lines.extend(["", "## Closure Targets"])
    if closure_targets:
        lines.extend([f"- {claim}" for claim in closure_targets])
    else:
        lines.append("- No closure target was extracted automatically.")
    layout.paper_summary.write_text("\n".join(lines), encoding="utf-8")


def _copy_workspace_references(layout: WorkspaceLayout) -> None:
    """Copy a small reference set into the workspace for reviewer agents.

    Reviewer lane templates read ``<review_dir>/artifacts/references/...``, so keep
    the workspace self-contained even when the audit is run from other working
    directories.
    """
    skill_root = Path(__file__).resolve().parent.parent
    source_dir = skill_root / "references"
    dest_dir = layout.references_dir
    dest_dir.mkdir(parents=True, exist_ok=True)

    minimal_refs = (
        "DEEP_REVIEW_CRITERIA.md",
        "ISSUE_SCHEMA.md",
        "REVIEW_LANE_GUIDE.md",
        "CONSOLIDATION_RULES.md",
        "CHECKLIST.md",
        "QUALITATIVE_STANDARDS.md",
        "PRE_SUBMISSION_RULES.md",
        "CLAIM_EVIDENCE_CONTRACT.md",
        "DATA_AVAILABILITY_ADVISORY.md",
        "SUBSECTION_CONTEXT_PROTOCOL.md",
    )
    for name in minimal_refs:
        src = source_dir / name
        if not src.exists():
            continue
        shutil.copy2(src, dest_dir / name)


def prepare_workspace(
    input_path: str,
    output_dir: str = "./review_results",
    *,
    overwrite: bool = False,
    overwrite_hint: str = "--overwrite",
) -> Path:
    """Create deep-review workspace files and return the workspace path."""
    source = Path(input_path).resolve()
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    fmt = source.suffix.lower()
    parser = get_parser(str(source))
    if fmt == ".pdf":
        content = parser.extract_text_from_file(str(source))
    elif read_text_robust is not None:
        content, _warning = read_text_robust(source)
        if _warning:
            print(f"[prepare-workspace] {_warning}", file=sys.stderr)
    else:
        content = source.read_text(encoding="utf-8")

    visible_text = parser.clean_text(content, keep_structure=True)
    language = detect_language(parser.clean_text(content))
    title = extract_title(content) if fmt in {".tex", ".typ"} else source.stem
    slug = slugify(title or source.stem)

    workspace = Path(output_dir).resolve() / slug
    if workspace.exists():
        if not overwrite:
            raise FileExistsError(
                f"Review workspace already exists: {workspace}. "
                f"Pass {overwrite_hint} to replace it, or choose a different --output-dir."
            )
        shutil.rmtree(workspace)

    layout = WorkspaceLayout(workspace)
    layout.ensure_dirs()

    prepare_subsection_artifacts(source, parser, layout)
    layout.full_text.write_text(visible_text if visible_text else content, encoding="utf-8")

    section_index = build_section_index(content, parser, fmt)
    lines = content.splitlines()
    section_texts: dict[str, str] = {}
    for section in section_index:
        raw_body = _section_lines(
            lines,
            section["start_line"],
            section["end_line"],
            zero_based=section["line_base"] == 0,
        )
        body = parser.clean_text(raw_body, keep_structure=True) if fmt != ".pdf" else raw_body
        section_texts[section["section_key"]] = body
        layout.section_file(section["file_name"]).write_text(body, encoding="utf-8")

    layout.section_index.write_text(
        json.dumps(section_index, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    claim_map = build_claim_map(
        visible_text if visible_text else content,
        section_index,
        section_texts=section_texts,
    )
    layout.claim_map.write_text(
        json.dumps(claim_map, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    metadata = {
        "slug": slug,
        "title": title or source.stem,
        "source_path": str(source),
        "language": language,
        "format": fmt,
        "generated_at": datetime.now().isoformat(),
    }
    layout.metadata.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_summary_stub(layout, metadata["title"], claim_map, section_index, section_texts)
    _copy_workspace_references(layout)
    init_checkpoint(
        workspace,
        generated_files=layout.initial_generated_files(),
    )
    return workspace


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a deep-review workspace")
    parser.add_argument("input", help="Path to a .tex, .typ, or .pdf file")
    parser.add_argument(
        "--output-dir",
        default="./review_results",
        help="Parent directory for workspace output (default: ./review_results)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing workspace for the same paper slug",
    )
    args = parser.parse_args()

    workspace = prepare_workspace(args.input, output_dir=args.output_dir, overwrite=args.overwrite)
    print(f"WORKSPACE: {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
