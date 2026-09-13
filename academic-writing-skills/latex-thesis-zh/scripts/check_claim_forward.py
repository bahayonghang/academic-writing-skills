#!/usr/bin/env python3
"""
主张前置检查器（claim-forward）— 中文学位论文版本

检出把论文自身主张后置或削弱的表述：段首否定式免责句、写在主张前面的限制句、
自我削弱搭配、主张句上的 hedge 堆叠、以负面判定收尾且无展望方向的结论末段。
每条发现都是 ``[Script]`` 候选（``Meaning-Check: NEEDS-LLM``）；脚本不改源文件，
也绝不删除任何限制、不利对比或非主线结果——只调整顺序与措辞。

观察码：CF-DISCLAIM、CF-SELFWEAK、CF-CAVEAT-POS、CF-HEDGE-STACK、CF-CLOSE-NEG。
与 EN 副本同码同格式，实现独立（中文断句、主语门控、引用命令集合不同）。

Usage:
    uv run python check_claim_forward.py main.tex
    uv run python check_claim_forward.py main.tex --section conclusion --json
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

TERMS_FILENAME = "claim-forward-terms-zh.yaml"
HEDGE_STACK_THRESHOLD = 3

HIGH_IMPACT_SECTIONS = ("abstract", "introduction", "contribution", "conclusion")
# CF-CAVEAT-POS 只看关于自身工作的限制句；“然而……难以……因此本文提出”是问题陈述，
# 是中文学位论文段落的正常动机形态，不报。
OWN_WORK_SUBJECTS = (
    "本文",
    "本章",
    "本研究",
    "本节",
    "所提",
    "提出的",
    "本方法",
    "该方法",
    "我们",
    "本实验",
    "本模型",
    "本系统",
)
CLOSING_SECTIONS = ("conclusion", "summary")
# “有望”在结论/总结章的展望语境合法，不计入 hedge 堆叠。
OUTLOOK_HEDGES = ("有望",)

# 内置回退表；语义与 claim-forward-terms-zh.yaml 等值。
_DEFAULT_TERMS: dict[str, Any] = {
    "self_weakening": [
        {"match": "遗憾的是", "prefer": ""},
        {"match": "令人遗憾", "prefer": ""},
        {"match": "仍明显落后于", "prefer": "落后{gap}于"},
        {"match": "仍明显落后", "prefer": "落后{gap}"},
        {"match": "明显落后于", "prefer": "落后{gap}于"},
        {
            "match": "效果有限",
            "prefer": "在{scope}上提升{value}",
            "subject_gate": ["本文", "本章", "本研究", "所提", "本方法", "提出的"],
        },
        {
            "match": "存在严重不足",
            "prefer": "在{aspect}上受限于{cause}",
            "subject_gate": ["本文", "本章", "本研究", "所提", "本方法", "提出的"],
        },
        {
            "match": "存在较大差距",
            "prefer": "相差{gap}",
            "subject_gate": ["本文", "本章", "本研究", "所提", "本方法", "提出的"],
        },
        {
            "match": "并不理想",
            "prefer": "为{value}",
            "subject_gate": ["本文", "本章", "本研究", "所提", "本方法", "提出的"],
        },
        {
            "match": "差强人意",
            "prefer": "为{value}",
            "subject_gate": ["本文", "本章", "本研究", "所提", "本方法", "提出的"],
        },
        {
            "match": "略显不足",
            "prefer": "为{value}",
            "subject_gate": ["本文", "本章", "本研究", "所提", "本方法", "提出的"],
        },
        {
            "match": "仅能",
            "prefer": "能够",
            "subject_gate": ["本文", "本章", "本研究", "所提", "本方法", "提出的"],
        },
        {
            "match": "仅仅",
            "prefer": "",
            "subject_gate": ["本文", "本章", "本研究", "所提", "本方法", "提出的"],
        },
        {
            "match": "未能",
            "prefer": "尚未在{scope}上",
            "subject_gate": ["本文", "本章", "本研究", "所提", "本方法", "提出的"],
        },
    ],
    "hedges": [
        "可能",
        "或许",
        "也许",
        "在一定程度上",
        "一定程度",
        "某种程度",
        "大致",
        "基本上",
        "相对而言",
        "似乎",
        "有望",
    ],
    "disclaim_openers": [
        "本文不试图",
        "本文并不主张",
        "本文无意",
        "本研究不涉及",
        "本文并未",
        "本文不讨论",
        "本文不追求",
        "本章不试图",
    ],
    "direction_markers": [
        "展望",
        "未来工作",
        "未来研究",
        "后续工作",
        "后续研究",
        "下一步",
        "有待",
        "进一步研究",
        "进一步探索",
        "可进一步",
        "值得进一步",
        "将在后续",
    ],
    "process_openers": ["起初", "最初尝试", "经过多次尝试", "我们曾", "曾尝试"],
    "limitation_section_titles": ["不足", "局限", "研究范围", "范围界定"],
}

_LIST_KEYS = (
    "hedges",
    "disclaim_openers",
    "direction_markers",
    "process_openers",
    "limitation_section_titles",
)

CLAIM_SUBJECT = r"(?:本文|本章|本研究|本节|所提(?:出的)?|提出的|该方法|我们)"
CLAIM_RE = re.compile(
    CLAIM_SUBJECT
    + r"[^。！？；]{0,40}?(?:提出|实现|构建|设计|建立|达到|验证|表明|证明|优于|提升|提高|"
    r"降低|减少|缩短|改善|取得|获得|解决|突破|扩展|给出)"
)
NUMERIC_CLAIM_RE = re.compile(
    r"(?:提升|提高|降低|减少|缩短|改善|优于|高于|低于|快于)[^。！？；]{0,20}?"
    r"\d+(?:\.\d+)?\s*(?:%|％|倍|个百分点|dB|ms|秒)|"
    r"\d+(?:\.\d+)?\s*(?:%|％|倍|个百分点)[^。！？；]{0,12}?(?:提升|提高|降低|减少|改善|优势)"
)
LIMITATION_OPENER_RE = re.compile(r"^(?:然而|但是?|尽管|虽然|需要指出|不过|遗憾的是)")
LIMITATION_BODY_RE = re.compile(
    r"局限|不足|未能|无法|难以|受限于|不适用|尚不能|不能(?:很好地)?|仍(?:然)?存在|"
    r"仍需|还需|有待|落后|差距"
)
CITE_RE = re.compile(
    r"\\(?:cite[pt]?|upcite|citep|citet|citealp|citeauthor|citeyear)\*?\s*(?:\[[^\]]*\])*\{"
)
PRIOR_WORK_SUBJECT_RE = re.compile(
    r"^(?:该(?:方法|模型|类|系统|工作)|上述(?:方法|工作|模型|研究)|这些(?:方法|工作|模型)|"
    r"现有(?:方法|工作|模型|研究)|传统(?:方法|模型)|已有(?:方法|工作|研究)|前人|文献|"
    r"他们|其(?:方法|模型))"
)
HEADING_RE = re.compile(
    r"\\(?:chapter|section|subsection|subsubsection|paragraph)\*?\s*(?:\[[^\]]*\])?\{([^}]*)\}"
)
SKIP_LINE_RE = re.compile(
    r"^\\(?:begin|end|label|caption|bicaption|includegraphics|centering|vspace|hspace|"
    r"noindent|newpage|clearpage|bibliography|bibliographystyle|maketitle|input|include|"
    r"usepackage|documentclass|author|title|date|footnote|item|hline|toprule|midrule|"
    r"bottomrule|setlength|renewcommand|newcommand|def|zihao|songti|heiti)\b"
)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？；])")


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
    """读取公开词表；缺失或字段非法时按字段回退到内置表。"""
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
        cleaned: list[dict[str, Any]] = []
        for item in configured_sw:
            if not isinstance(item, dict):
                continue
            match = item.get("match")
            prefer = item.get("prefer", "")
            if not (isinstance(match, str) and match.strip() and isinstance(prefer, str)):
                continue
            entry: dict[str, Any] = {"match": match.strip(), "prefer": prefer.strip()}
            gate = item.get("subject_gate")
            if isinstance(gate, list) and all(isinstance(g, str) and g for g in gate):
                entry["subject_gate"] = list(gate)
            cleaned.append(entry)
        if cleaned:
            terms["self_weakening"] = cleaned
    return terms, "yaml"


def _split_sentences(text: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    pos = 0
    for piece in SENTENCE_SPLIT_RE.split(text):
        if piece.strip():
            out.append((pos, piece.strip()))
        pos += len(piece)
    return out


def _has_subject(visible: str, gate: list[str]) -> bool:
    return any(token in visible for token in gate)


def _classify(visible: str, terms: dict[str, Any]) -> set[str]:
    kinds: set[str] = set()
    stripped = visible.lstrip("“\"‘' ")
    for opener in terms["disclaim_openers"]:
        if stripped.startswith(opener):
            kinds.add("disclaim")
            break
    if CLAIM_RE.search(visible) or NUMERIC_CLAIM_RE.search(visible):
        kinds.add("claim")
    if LIMITATION_OPENER_RE.search(stripped) or LIMITATION_BODY_RE.search(visible):
        kinds.add("limitation")
    for opener in terms["process_openers"]:
        if stripped.startswith(opener):
            kinds.add("process")
            break
    if "disclaim" in kinds:
        kinds.discard("claim")
    return kinds


def _paragraphs(
    lines: list[str], start: int, end: int, comment_prefix: str, limitation_titles: list[str]
) -> list[tuple[list[tuple[int, str]], bool]]:
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
            title = heading.group(1)
            in_limitations = any(t in title for t in limitation_titles)
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
    parts: list[str] = []
    cursor = 0
    for line_no, raw in paragraph:
        offsets.append(cursor)
        line_nos.append(line_no)
        parts.append(raw)
        cursor += len(raw)
    joined = "".join(parts)
    sentences: list[Sentence] = []
    previous_cited = False
    for offset, raw_sentence in _split_sentences(joined):
        visible = re.sub(r"\s+", "", parser.extract_visible_text(raw_sentence)).strip()
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


def _first_own_limitation(sentences: list[Sentence]) -> int | None:
    for i, s in enumerate(sentences):
        if "limitation" in s.kinds and _has_subject(s.visible, list(OWN_WORK_SUBJECTS)):
            return i
    return None


def _first_index(sentences: list[Sentence], kind: str) -> int | None:
    for i, s in enumerate(sentences):
        if kind in s.kinds:
            return i
    return None


def _base_key(section_key: str) -> str:
    return section_key.split("_", 1)[0]


def _hedge_hits(visible: str, hedges: list[str], closing: bool) -> list[tuple[int, int]]:
    hits: list[tuple[int, int]] = []
    for hedge in hedges:
        if closing and hedge in OUTLOOK_HEDGES:
            continue
        for m in re.finditer(re.escape(hedge), visible):
            hits.append((m.start(), m.end()))
    hits.sort()
    # 去掉被更长命中包含的短命中（如“一定程度”⊂“在一定程度上”）。
    merged: list[tuple[int, int]] = []
    for start, end in hits:
        if merged and start < merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            continue
        merged.append((start, end))
    return merged


def _hedge_candidate(visible: str, hits: list[tuple[int, int]]) -> str:
    pieces: list[str] = []
    last = 0
    for start, end in hits[1:]:
        pieces.append(visible[last:start])
        last = end
    pieces.append(visible[last:])
    return "".join(pieces).replace("，，", "，").strip()


def _selfweak_hits(
    visible: str, terms: dict[str, Any], in_limitations: bool = False
) -> list[dict[str, Any]]:
    """命中的自我削弱搭配；重叠命中只保留最长者。

    不足/局限小节内，带 subject_gate 的弱搭配（未能/仅能/仅仅）是正常的限制表述，不报；
    强搭配（遗憾的是 等）仍报。
    """
    hits: list[tuple[int, int, dict[str, Any]]] = []
    for item in terms["self_weakening"]:
        gate = item.get("subject_gate")
        if gate and (in_limitations or not _has_subject(visible, gate)):
            continue
        start = visible.find(item["match"])
        if start >= 0:
            hits.append((start, start + len(item["match"]), item))
    hits.sort(key=lambda h: (h[0], -(h[1] - h[0])))
    kept: list[tuple[int, int, dict[str, Any]]] = []
    for start, end, item in sorted(hits, key=lambda h: -(h[1] - h[0])):
        if any(start < k_end and end > k_start for k_start, k_end, _ in kept):
            continue
        kept.append((start, end, item))
    kept.sort(key=lambda h: h[0])
    return [item for _, _, item in kept]


def _selfweak_candidate(visible: str, hits: list[dict[str, Any]]) -> str:
    text = visible
    for item in hits:
        text = text.replace(item["match"], item["prefer"], 1)
    text = re.sub(r"^[，、]\s*", "", text)
    return text.replace("，，", "，").strip()


def analyze_document(
    lines: list[str],
    sections: dict[str, tuple[int, int]],
    parser: Any,
    terms: dict[str, Any],
    section_filter: str | None,
    lineref: Any = None,
) -> tuple[list[Finding], list[str]]:
    """运行五项 CF-* 规则；返回 (findings, error_lines)。"""
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
        closing = base in CLOSING_SECTIONS
        paragraphs = _paragraphs(lines, start, end, cp, terms["limitation_section_titles"])
        for p_index, (paragraph, in_limitations) in enumerate(paragraphs):
            sentences = _sentences(paragraph, parser, terms)
            if not sentences:
                continue
            first_claim = _first_index(sentences, "claim")
            first_disclaim = _first_index(sentences, "disclaim")
            first_limitation = _first_own_limitation(sentences)

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

            if (
                first_disclaim is not None
                and base != "related"
                and not in_limitations
                and (first_claim is None or first_disclaim < first_claim)
                and not sentences[first_disclaim].cite_exempt
            ):
                s = sentences[first_disclaim]
                if first_claim is not None:
                    cand = f"{sentences[first_claim].visible}{s.visible}"
                    note = "免责句先于首个主张句；先说贡献，范围说明保留在其后"
                else:
                    cand = s.visible
                    note = "段落以“本文不做什么”开头；先陈述贡献再界定范围"
                sev, pri = ("Minor", "P2") if high_impact else ("Info", "P3")
                emit("CF-DISCLAIM", s, sev, pri, cand, note)

            if (
                first_claim is not None
                and first_limitation is not None
                and first_limitation < first_claim
                and not in_limitations
                and "disclaim" not in sentences[first_limitation].kinds
                and not sentences[first_limitation].cite_exempt
            ):
                s = sentences[first_limitation]
                cand = f"{sentences[first_claim].visible}{s.visible}"
                emit(
                    "CF-CAVEAT-POS",
                    s,
                    "Info",
                    "P3",
                    cand,
                    "限制句先于主张句；交换顺序，限制句不删",
                )

            for s in sentences:
                if s.cite_exempt:
                    continue
                sw_hits = _selfweak_hits(s.visible, terms, in_limitations)
                if sw_hits:
                    matched = "、".join(f"“{item['match']}”" for item in sw_hits)
                    emit(
                        "CF-SELFWEAK",
                        s,
                        "Minor",
                        "P2",
                        _selfweak_candidate(s.visible, sw_hits),
                        f"自我削弱搭配 {matched}；改为测量值或肯定范围（花括号占位只能从稿件证据填入）",
                    )
                if "claim" in s.kinds:
                    hits = _hedge_hits(s.visible, terms["hedges"], closing)
                    if len(hits) >= HEDGE_STACK_THRESHOLD:
                        emit(
                            "CF-HEDGE-STACK",
                            s,
                            "Info",
                            "P3",
                            _hedge_candidate(s.visible, hits),
                            f"一个主张句上叠加 {len(hits)} 个 hedge；只保留证据支撑的一个"
                            "（加强措辞前先对照 over-claim-guard 阶梯）",
                        )

            if closing and p_index == len(paragraphs) - 1 and not in_limitations:
                negative_idx: int | None = None
                for i, s in enumerate(sentences):
                    if s.cite_exempt:
                        continue
                    if "limitation" in s.kinds or _selfweak_hits(s.visible, terms):
                        negative_idx = i
                if negative_idx is not None:
                    tail = "".join(s.visible for s in sentences[negative_idx:])
                    if not any(marker in tail for marker in terms["direction_markers"]):
                        s = sentences[negative_idx]
                        emit(
                            "CF-CLOSE-NEG",
                            s,
                            "Minor",
                            "P2",
                            f"{s.visible}[LLM: 补充该局限指向的后续方向]",
                            "结论末段以负面判定收尾且无展望方向；判定保留，补方向",
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
            "主张前置检查（claim-forward）：检出自我削弱与主张后置表述 "
            "(CF-DISCLAIM, CF-SELFWEAK, CF-CAVEAT-POS, CF-HEDGE-STACK, CF-CLOSE-NEG)。"
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
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
