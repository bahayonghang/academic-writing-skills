#!/usr/bin/env python3
"""
Claim-forward check for English LaTeX papers.

Detects self-weakening and claim-postponing prose (disclaimers before the first
claim, limitation sentences ahead of the claim they qualify, self-weakening
collocations, stacked hedges on a claim sentence, and closing paragraphs that
end on a negative judgment without a direction). Every finding is a
``[Script]`` candidate with ``Meaning-Check: NEEDS-LLM``; the script never
rewrites the source and never removes a limitation or an unfavorable result.

Codes: CF-DISCLAIM, CF-SELFWEAK, CF-CAVEAT-POS, CF-HEDGE-STACK, CF-CLOSE-NEG.
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    from parsers import get_parser, resolve_section_keys
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import get_parser, resolve_section_keys

try:
    from tex_loader import assemble, read_text_robust
except ImportError:
    assemble = None
    read_text_robust = None


CODES: tuple[str, ...] = (
    "CF-DISCLAIM",
    "CF-SELFWEAK",
    "CF-CAVEAT-POS",
    "CF-HEDGE-STACK",
    "CF-CLOSE-NEG",
)

TERMS_FILENAME = "claim-forward-terms.yaml"
HEDGE_STACK_THRESHOLD = 3

# Sections where a disclaimer or a leading limitation costs the most.
HIGH_IMPACT_SECTIONS = ("abstract", "introduction", "contribution", "conclusion")
CLOSING_SECTIONS = ("conclusion", "summary")

# Built-in fallback; kept byte-equivalent in meaning to claim-forward-terms.yaml.
_DEFAULT_TERMS: dict[str, Any] = {
    "self_weakening": [
        {"match": "regrettably", "prefer": ""},
        {"match": "unfortunately", "prefer": ""},
        {"match": "still lags far behind", "prefer": "trails {baseline} by {gap}"},
        {"match": "lags far behind", "prefer": "trails {baseline} by {gap}"},
        {"match": "falls short of", "prefer": "reaches {ratio} of"},
        {"match": "of limited effect", "prefer": "improves {metric} by {value} on {scope}"},
        {"match": "only marginally", "prefer": "by {value}"},
        {"match": "merely", "prefer": ""},
        {"match": "suffers from serious", "prefer": "is bounded by {cause} in"},
        {"match": "we were unable to", "prefer": "this work does not cover"},
        {"match": "we failed to", "prefer": "this work does not"},
        {"match": "remains far from", "prefer": "reaches {ratio} of"},
    ],
    "hedges": [
        "may",
        "might",
        "could",
        "possibly",
        "potentially",
        "perhaps",
        "to some extent",
        "to a certain degree",
        "in some cases",
        "under certain conditions",
        "somewhat",
        "relatively",
        "arguably",
        "it seems",
        "appears to",
    ],
    "disclaim_openers": [
        "we do not claim",
        "we do not argue",
        "we do not attempt",
        "we make no claim",
        "this paper does not",
        "this work does not",
        "it is not our goal",
        "it is not our intention",
        "rather than",
    ],
    "direction_markers": [
        "future work",
        "we plan",
        "next step",
        "opens",
        "promising",
        "will extend",
        "will explore",
        "will investigate",
        "remains to be",
        "direction",
    ],
    "process_openers": [
        "we first tried",
        "we initially",
        "after several attempts",
        "our initial approach",
    ],
}

_LIST_KEYS = ("hedges", "disclaim_openers", "direction_markers", "process_openers")

CLAIM_RE = re.compile(
    r"\b(?:we|our (?:method|approach|model|framework|system|results?|analysis)|"
    r"this (?:paper|work|study|article)|the proposed (?:method|approach|model|framework))\b"
    r"[^.]{0,80}?\b(?:propose|proposes|show|shows|demonstrate|demonstrates|achieve|achieves|"
    r"introduce|introduces|present|presents|outperform|outperforms|improve|improves|"
    r"reduce|reduces|enable|enables|establish|establishes|contribute|contributes|"
    r"provide|provides|report|reports|reach|reaches)\b",
    re.IGNORECASE,
)
NUMERIC_CLAIM_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:%|percent|points?|\\%|x\b|times)\b[^.]{0,40}?"
    r"\b(?:higher|lower|faster|better|fewer|more|less|improvement|gain|reduction)\b|"
    r"\b(?:higher|lower|faster|better|fewer|improvement|gain|reduction)\b[^.]{0,40}?"
    r"\d+(?:\.\d+)?\s*(?:%|percent|points?|\\%)",
    re.IGNORECASE,
)
LIMITATION_OPENER_RE = re.compile(
    r"^(?:however|although|while|despite|note that|admittedly|nevertheless)\b", re.IGNORECASE
)
LIMITATION_BODY_RE = re.compile(
    r"\b(?:limitation|limited to|does not|do not|cannot|fails? to|is not able to|"
    r"are not able to|remains? (?:an )?open|not (?:yet )?(?:address|cover|handle)|"
    r"lags? behind|falls? short|only)\b",
    re.IGNORECASE,
)
CITE_RE = re.compile(
    r"\\(?:cite[pt]?|citep|citet|citealp|citeauthor|citeyear)\*?\s*(?:\[[^\]]*\])*\{"
)
PRIOR_WORK_SUBJECT_RE = re.compile(
    r"^(?:they|these|those|such|prior|previous|existing|earlier|their|the authors|"
    r"this (?:line|body) of work|conventional|traditional)\b",
    re.IGNORECASE,
)
HEADING_RE = re.compile(
    r"\\(?:chapter|section|subsection|subsubsection|paragraph)\*?\s*(?:\[[^\]]*\])?\{([^}]*)\}"
)
SKIP_LINE_RE = re.compile(
    r"^\\(?:begin|end|label|caption|includegraphics|centering|vspace|hspace|noindent|"
    r"newpage|clearpage|bibliography|bibliographystyle|maketitle|input|include|"
    r"usepackage|documentclass|author|title|date|footnote|item|hline|toprule|midrule|"
    r"bottomrule|setlength|renewcommand|newcommand|def)\b"
)
ABBREVIATIONS = (
    "e.g.",
    "i.e.",
    "et al.",
    "etc.",
    "cf.",
    "vs.",
    "Fig.",
    "Figs.",
    "Eq.",
    "Eqs.",
    "Sec.",
    "Tab.",
    "No.",
    "approx.",
    "resp.",
    "Dr.",
    "Prof.",
)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\\(\[])")


@dataclass
class Finding:
    code: str
    line: int
    location: str
    severity: str
    priority: str
    section: str
    original: str
    candidate: str
    note: str


@dataclass
class Sentence:
    raw: str
    visible: str
    line: int
    kinds: set[str]
    cite_exempt: bool


def _load_terms(script_dir: Path) -> tuple[dict[str, Any], str]:
    """Return (terms, source) with per-field fallback to the built-in table."""
    terms: dict[str, Any] = {
        "self_weakening": [dict(item) for item in _DEFAULT_TERMS["self_weakening"]],
        **{key: list(_DEFAULT_TERMS[key]) for key in _LIST_KEYS},
    }
    yaml_path = script_dir.parent / "references" / "writing" / TERMS_FILENAME
    if not yaml_path.exists():
        return terms, "builtin"
    try:
        import yaml
    except ImportError:
        return terms, "builtin"
    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeError, yaml.YAMLError):
        return terms, "builtin"
    if not isinstance(data, dict):
        return terms, "builtin"
    for key in _LIST_KEYS:
        configured = data.get(key)
        if (
            isinstance(configured, list)
            and configured
            and all(isinstance(v, str) and v.strip() for v in configured)
        ):
            terms[key] = [v.strip() for v in configured]
    configured_sw = data.get("self_weakening")
    if isinstance(configured_sw, list) and configured_sw:
        cleaned: list[dict[str, str]] = []
        for item in configured_sw:
            if not isinstance(item, dict):
                continue
            match = item.get("match")
            prefer = item.get("prefer", "")
            if isinstance(match, str) and match.strip() and isinstance(prefer, str):
                cleaned.append({"match": match.strip(), "prefer": prefer.strip()})
        if cleaned:
            terms["self_weakening"] = cleaned
    return terms, "yaml"


def _phrase_re(phrase: str) -> re.Pattern[str]:
    return re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)


def _split_sentences(text: str) -> list[tuple[int, str]]:
    """Return (offset, sentence) pairs; offsets index into ``text``."""
    protected = text
    for abbr in ABBREVIATIONS:
        protected = protected.replace(abbr, abbr.replace(".", "\x00"))
    out: list[tuple[int, str]] = []
    pos = 0
    for piece in SENTENCE_SPLIT_RE.split(protected):
        if not piece.strip():
            pos += len(piece) + 1
            continue
        start = protected.find(piece, pos)
        if start < 0:
            start = pos
        out.append((start, piece.replace("\x00", ".").strip()))
        pos = start + len(piece)
    return out


def _classify(visible: str, terms: dict[str, Any]) -> set[str]:
    kinds: set[str] = set()
    lowered = visible.strip().lower()
    for opener in terms["disclaim_openers"]:
        if lowered.startswith(opener):
            kinds.add("disclaim")
            break
    if CLAIM_RE.search(visible) or NUMERIC_CLAIM_RE.search(visible):
        kinds.add("claim")
    if LIMITATION_OPENER_RE.search(visible) or LIMITATION_BODY_RE.search(visible):
        kinds.add("limitation")
    for opener in terms["process_openers"]:
        if lowered.startswith(opener):
            kinds.add("process")
            break
    # A disclaimer is a scope statement, not a claim about the contribution.
    if "disclaim" in kinds:
        kinds.discard("claim")
    return kinds


def _paragraphs(
    lines: list[str], start: int, end: int, comment_prefix: str
) -> list[tuple[list[tuple[int, str]], bool]]:
    """Group prose lines into paragraphs; the flag marks a Limitations context."""
    paragraphs: list[tuple[list[tuple[int, str]], bool]] = []
    current: list[tuple[int, str]] = []
    in_limitations = False
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        heading = HEADING_RE.match(raw)
        if heading:
            if current:
                paragraphs.append((current, in_limitations))
                current = []
            in_limitations = "limitation" in heading.group(1).lower()
            continue
        if not raw or raw == r"\par":
            if current:
                paragraphs.append((current, in_limitations))
                current = []
            continue
        if raw.startswith(comment_prefix) or SKIP_LINE_RE.match(raw):
            continue
        current.append((line_no, raw))
    if current:
        paragraphs.append((current, in_limitations))
    return paragraphs


def _sentences(
    paragraph: list[tuple[int, str]], parser: Any, terms: dict[str, Any]
) -> list[Sentence]:
    offsets: list[int] = []
    line_nos: list[int] = []
    joined_parts: list[str] = []
    cursor = 0
    for line_no, raw in paragraph:
        offsets.append(cursor)
        line_nos.append(line_no)
        joined_parts.append(raw)
        cursor += len(raw) + 1
    joined = " ".join(joined_parts)
    sentences: list[Sentence] = []
    previous_cited = False
    for offset, raw_sentence in _split_sentences(joined):
        visible = re.sub(r"\s+", " ", parser.extract_visible_text(raw_sentence)).strip()
        if not visible:
            continue
        idx = max(0, bisect.bisect_right(offsets, offset) - 1)
        cited = bool(CITE_RE.search(raw_sentence))
        exempt = cited or (previous_cited and bool(PRIOR_WORK_SUBJECT_RE.match(visible)))
        sentences.append(
            Sentence(
                raw=raw_sentence,
                visible=visible,
                line=line_nos[idx],
                kinds=_classify(visible, terms),
                cite_exempt=exempt,
            )
        )
        previous_cited = cited
    return sentences


def _first_index(sentences: list[Sentence], kind: str) -> int | None:
    for i, s in enumerate(sentences):
        if kind in s.kinds:
            return i
    return None


def _base_key(section_key: str) -> str:
    return section_key.split("_", 1)[0]


def _hedge_candidate(visible: str, hedges: list[str]) -> tuple[str, int]:
    hits: list[tuple[int, int]] = []
    for hedge in hedges:
        for m in _phrase_re(hedge).finditer(visible):
            hits.append((m.start(), m.end()))
    hits.sort()
    if len(hits) < HEDGE_STACK_THRESHOLD:
        return visible, len(hits)
    # Keep the first hedge; drop the rest without touching anything else.
    pieces: list[str] = []
    last = 0
    for start, end in hits[1:]:
        pieces.append(visible[last:start])
        last = end
    pieces.append(visible[last:])
    candidate = re.sub(r"\s{2,}", " ", "".join(pieces))
    candidate = re.sub(r"\s+([.,;:])", r"\1", candidate).strip()
    return candidate, len(hits)


def _selfweak_candidate(visible: str, hits: list[dict[str, str]]) -> str:
    """Apply every matched collocation's `prefer` template to one sentence."""
    text = visible
    for item in hits:
        text = _phrase_re(item["match"]).sub(item["prefer"], text, count=1)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+([.,;:])", r"\1", text).strip()
    text = re.sub(r"^,\s*", "", text)
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def analyze_document(
    lines: list[str],
    sections: dict[str, tuple[int, int]],
    parser: Any,
    terms: dict[str, Any],
    section_filter: str | None,
    lineref: Any = None,
) -> tuple[list[Finding], list[str]]:
    """Run the five CF-* rules; returns (findings, error_lines)."""
    if section_filter:
        matched, available = resolve_section_keys(section_filter, sections)
        if not matched:
            avail = ", ".join(available) if available else "(none detected)"
            return [], [f"Section not found: {section_filter}; available: {avail}"]
        targets = [(key, sections[key]) for key in matched]
    else:
        targets = list(sections.items()) if sections else [("document", (1, len(lines)))]

    cp = parser.get_comment_prefix()
    findings: list[Finding] = []
    for key, (start, end) in targets:
        base = _base_key(key)
        high_impact = base in HIGH_IMPACT_SECTIONS
        paragraphs = _paragraphs(lines, start, end, cp)
        for p_index, (paragraph, in_limitations) in enumerate(paragraphs):
            sentences = _sentences(paragraph, parser, terms)
            if not sentences:
                continue
            first_claim = _first_index(sentences, "claim")
            first_disclaim = _first_index(sentences, "disclaim")
            first_limitation = _first_index(sentences, "limitation")

            def emit(
                code: str,
                s: Sentence,
                severity: str,
                priority: str,
                cand: str,
                note: str,
                _key: str = key,
            ) -> None:
                loc = lineref(s.line) if lineref is not None else f"Line {s.line}"
                findings.append(
                    Finding(code, s.line, loc, severity, priority, _key, s.visible, cand, note)
                )

            # CF-DISCLAIM: scope denial before the first claim.
            if (
                first_disclaim is not None
                and base != "related"
                and not in_limitations
                and (first_claim is None or first_disclaim < first_claim)
                and not sentences[first_disclaim].cite_exempt
            ):
                s = sentences[first_disclaim]
                if first_claim is not None:
                    cand = f"{sentences[first_claim].visible} {s.visible}"
                    note = "disclaimer precedes the first claim; lead with the claim, keep the scope sentence after it"
                else:
                    cand = s.visible
                    note = "paragraph opens by stating what this work does not do; state the contribution first"
                sev, pri = ("Minor", "P2") if high_impact else ("Info", "P3")
                emit("CF-DISCLAIM", s, sev, pri, cand, note)

            # CF-CAVEAT-POS: limitation sentence ahead of the claim it qualifies.
            if (
                first_claim is not None
                and first_limitation is not None
                and first_limitation < first_claim
                and not in_limitations
                and "disclaim" not in sentences[first_limitation].kinds
                and not sentences[first_limitation].cite_exempt
            ):
                s = sentences[first_limitation]
                cand = f"{sentences[first_claim].visible} {s.visible}"
                emit(
                    "CF-CAVEAT-POS",
                    s,
                    "Info",
                    "P3",
                    cand,
                    "limitation stated before the claim; swap order, do not delete the limitation",
                )

            # CF-SELFWEAK / CF-HEDGE-STACK: sentence-level.
            for s in sentences:
                if s.cite_exempt:
                    continue
                sw_hits = [
                    item
                    for item in terms["self_weakening"]
                    if _phrase_re(item["match"]).search(s.visible)
                ]
                # Drop collocations nested inside a longer matched one.
                sw_hits = [
                    item
                    for item in sw_hits
                    if not any(
                        other is not item and item["match"].lower() in other["match"].lower()
                        for other in sw_hits
                    )
                ]
                if sw_hits:
                    matched = ", ".join(f"'{item['match']}'" for item in sw_hits)
                    emit(
                        "CF-SELFWEAK",
                        s,
                        "Minor",
                        "P2",
                        _selfweak_candidate(s.visible, sw_hits),
                        f"self-weakening collocation {matched}; state the measured value or "
                        "scope instead (fill {placeholders} from evidence only)",
                    )
                if "claim" in s.kinds:
                    cand, count = _hedge_candidate(s.visible, terms["hedges"])
                    if count >= HEDGE_STACK_THRESHOLD:
                        emit(
                            "CF-HEDGE-STACK",
                            s,
                            "Info",
                            "P3",
                            cand,
                            f"{count} hedges on one claim; keep the one the evidence earns "
                            "(check the over-claim ladder before strengthening)",
                        )

            # CF-CLOSE-NEG: closing paragraph ends on a negative judgment with no direction.
            if base in CLOSING_SECTIONS and p_index == len(paragraphs) - 1 and not in_limitations:
                negative_idx: int | None = None
                for i, s in enumerate(sentences):
                    if s.cite_exempt:
                        continue
                    is_selfweak = any(
                        _phrase_re(item["match"]).search(s.visible)
                        for item in terms["self_weakening"]
                    )
                    if "limitation" in s.kinds or is_selfweak:
                        negative_idx = i
                if negative_idx is not None:
                    tail = " ".join(s.visible for s in sentences[negative_idx:]).lower()
                    has_direction = any(
                        _phrase_re(marker).search(tail) for marker in terms["direction_markers"]
                    )
                    if not has_direction:
                        s = sentences[negative_idx]
                        emit(
                            "CF-CLOSE-NEG",
                            s,
                            "Minor",
                            "P2",
                            f"{s.visible} [LLM: add the direction this limitation points to]",
                            "closing paragraph ends on a negative judgment without a direction; "
                            "keep the judgment, add where it leads",
                        )
    return findings, []


def render_text(
    cp: str,
    findings: list[Finding],
    errors: list[str],
    section: str | None,
    terms_source: str,
    warning_lines: list[str],
) -> list[str]:
    out = list(warning_lines)
    out.append(f"{cp} CLAIM-FORWARD [Script]: section={section or 'all'} terms={terms_source}")
    for err in errors:
        out.append(f"{cp} ERROR [Severity: Critical] [Priority: P0]: {err}")
    if errors:
        return out
    if not findings:
        out.append(f"{cp} CLAIM-FORWARD: No claim-forward patterns detected.")
        return out
    for f in findings:
        out.extend(
            [
                f"{cp} CLAIM-FORWARD ({f.location}) [Severity: {f.severity}] "
                f"[Priority: {f.priority}]: [Script] {f.code} {f.note}",
                f"{cp} Original: {f.original}",
                f"{cp} Candidate: {f.candidate}",
                f"{cp} Meaning-Check: NEEDS-LLM",
                "",
            ]
        )
    counts = {code: sum(1 for f in findings if f.code == code) for code in CODES}
    summary = ", ".join(f"{code}={n}" for code, n in counts.items() if n)
    out.append(f"{cp} CLAIM-FORWARD: {len(findings)} finding(s) ({summary})")
    return out


def run(file_path: Path, section: str | None) -> tuple[list[Finding], list[str], dict[str, Any]]:
    parser = get_parser(file_path)
    warning_lines: list[str] = []
    doc = None
    if assemble is not None:
        doc = assemble(file_path)
        content, lines = doc.content, doc.lines
    elif read_text_robust is not None:
        content, _warning = read_text_robust(file_path)
        lines = content.split("\n")
    else:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")
    cp = parser.get_comment_prefix()
    if doc is not None:
        warning_lines = doc.warning_lines(cp)
    sections = parser.split_sections(content)
    terms, terms_source = _load_terms(Path(__file__).resolve().parent)
    lineref = doc.lineref if doc is not None else None
    findings, errors = analyze_document(lines, sections, parser, terms, section, lineref)
    meta = {"cp": cp, "terms_source": terms_source, "warning_lines": warning_lines}
    return findings, errors, meta


def main() -> int:
    cli = argparse.ArgumentParser(
        description=(
            "Claim-forward check: flag self-weakening and claim-postponing prose "
            "(CF-DISCLAIM, CF-SELFWEAK, CF-CAVEAT-POS, CF-HEDGE-STACK, CF-CLOSE-NEG)."
        )
    )
    cli.add_argument("file", type=Path, help="Target .tex file")
    cli.add_argument("--section", help="Section key to analyze (default: all detected sections)")
    cli.add_argument("--json", action="store_true", help="Emit JSON instead of comment lines")
    args = cli.parse_args()

    if not args.file.exists():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        return 1

    findings, errors, meta = run(args.file, args.section)
    if args.json:
        counts = {code: sum(1 for f in findings if f.code == code) for code in CODES}
        payload = {
            "file": str(args.file),
            "section": args.section,
            "terms_source": meta["terms_source"],
            "errors": errors,
            "findings": [asdict(f) for f in findings],
            "summary": {"total": len(findings), "by_code": counts},
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(
        "\n".join(
            render_text(
                meta["cp"],
                findings,
                errors,
                args.section,
                meta["terms_source"],
                meta["warning_lines"],
            )
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
