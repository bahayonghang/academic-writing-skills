#!/usr/bin/env python3
"""
Logic and methodology analyzer for LaTeX/Typst papers.

Checks: paragraph-level coherence, method justification,
literature review quality (A1/A3), cross-section logic chain (C3).
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from parsers import extract_abstract, get_parser, resolve_section_keys
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import extract_abstract, get_parser, resolve_section_keys

try:
    from tex_loader import AssembledDocument, assemble
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from tex_loader import AssembledDocument, assemble


TRANSITIONS = {
    "addition": {"furthermore", "moreover", "in addition", "additionally"},
    "contrast": {"however", "nevertheless", "in contrast", "conversely"},
    "cause": {"therefore", "consequently", "as a result", "thus"},
    "sequence": {"next", "then", "subsequently", "after that", "after this"},
}


def _has_transition(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for values in TRANSITIONS.values() for token in values)


def _needs_method_justification(text: str) -> bool:
    lowered = text.lower()
    if "we use" not in lowered and "we adopt" not in lowered:
        return False
    return not any(marker in lowered for marker in ["because", "due to", "to ", "for "])


# Method-narrative criteria are locked by
# tests/contracts/test_method_narrative_alignment.py.
MN_HEADING_RUN = 3
MN_HEADING_HITS = 2
MN_EQUATION_LOOKAHEAD = 3
MN_ANNOUNCE_RE = re.compile(
    r"\b(?:This|The)\s+(?:module|component|stage|block)\s+"
    r"(?:is used to|aims to|is responsible for|serves to)\b|"
    r"\bWe\s+(?:now\s+)?(?:introduce|describe|present)\s+the\b.{0,40}"
    r"\b(?:module|component)\b",
    re.IGNORECASE,
)
_MN_SEQUENCE_ALTERNATION = "|".join(
    re.escape(token)
    for token in sorted(TRANSITIONS["sequence"], key=lambda token: (-len(token), token))
)
MN_SEQ_OPEN_RE = re.compile(
    rf"^(?:{_MN_SEQUENCE_ALTERNATION}),?\s+(?:we|this section)\b", re.IGNORECASE
)
MN_CAUSE_EXEMPT_RE = re.compile(
    r"\b(?:therefore|thus|however|to address|due to|because|since|remaining)\b",
    re.IGNORECASE,
)
MN_EQ_GLOSS_RE = re.compile(r"\bwhere\b", re.IGNORECASE)

_MN_NUMBERED_EQUATION_BEGIN_RE = re.compile(r"\\begin\{(?P<env>equation|align|gather)\}")
_MN_ANY_EQUATION_BEGIN_RE = re.compile(r"\\begin\{(?:equation|align|gather)\*?\}")
_MN_HEADING_COMMAND_RE = re.compile(
    r"^\s*\\(?:section|subsection|subsubsection|paragraph)\*?"
    r"(?:\[[^\]]*\])?\{"
)


def _mn_strip_latex_comment(raw: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", raw)


def _mn_visible_text(raw: str, parser) -> str:
    if parser.get_comment_prefix() == "%":
        raw = _mn_strip_latex_comment(raw)
    return parser.extract_visible_text(raw).strip()


def _mn_after_heading(raw: str) -> str:
    match = _MN_HEADING_COMMAND_RE.match(raw)
    if not match:
        return raw
    depth = 1
    for index in range(match.end(), len(raw)):
        if raw[index] == "{":
            depth += 1
        elif raw[index] == "}":
            depth -= 1
            if depth == 0:
                return raw[index + 1 :]
    return ""


def _mn_first_sentence_after_heading(
    lines: list[str], heading: dict, boundary: int, parser
) -> tuple[int, str] | None:
    parts: list[str] = []
    first_line = heading["line"]
    same_line = _mn_visible_text(_mn_after_heading(lines[first_line - 1]), parser)
    if same_line:
        parts.append(same_line)

    for line_no in range(first_line + 1, min(boundary, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(parser.get_comment_prefix()):
            if parts:
                break
            continue
        uncommented = _mn_strip_latex_comment(raw)
        if _MN_HEADING_COMMAND_RE.match(uncommented) or uncommented.startswith("\\begin{"):
            break
        visible = _mn_visible_text(uncommented, parser)
        if not visible:
            continue
        if not parts:
            first_line = line_no
        parts.append(visible)
        if re.search(r"[.!?]", visible):
            break

    if not parts:
        return None
    paragraph = " ".join(parts)
    sentence = re.split(r"(?<=[.!?])(?:\s|$)", paragraph, maxsplit=1)[0].strip()
    return first_line, sentence


def _mn_finding(
    line_no: int,
    severity: str,
    priority: str,
    code: str,
    message: str,
    current: str,
    suggested: str,
    rationale: str,
    doc: AssembledDocument,
) -> list[str]:
    return [
        f"% METHOD-NARRATIVE ({doc.lineref(line_no)}) [Severity: {severity}] "
        f"[Priority: {priority}]: [Script] {code} {message}",
        f"% Current: {current}",
        f"% Suggested: {suggested}",
        f"% Rationale: {rationale}",
        "% Meaning-Check: NEEDS-LLM",
        "",
    ]


def _check_method_heading(
    lines: list[str], headings: list[dict], start: int, end: int, parser, doc: AssembledDocument
) -> list[str]:
    scoped = [heading for heading in headings if start <= heading["line"] <= end]
    run: list[tuple[dict, str, bool]] = []

    def evaluate() -> list[str]:
        hits = [item for item in run if item[2]]
        if len(run) < MN_HEADING_RUN or len(hits) < MN_HEADING_HITS:
            return []
        first_heading, first_sentence, _hit = hits[0]
        titles = ", ".join(item[0]["title"] for item in run)
        return _mn_finding(
            first_heading["line"],
            "Minor",
            "P2",
            "M-HEADING",
            f"{len(hits)} of {len(run)} consecutive run-in headings open with announcements.",
            f"{first_heading['title']}: {first_sentence}",
            "Keep headings for independent technical units; lead with the active constraint "
            "and the upstream/downstream interface.",
            f"The heading run ({titles}) lists responsibilities without establishing the "
            "method interfaces.",
            doc,
        )

    for index, heading in enumerate(scoped):
        if heading["level"] <= 3:
            finding = evaluate()
            if finding:
                return finding
            run = []
            continue
        if heading.get("command") != "paragraph":
            continue
        boundary = scoped[index + 1]["line"] - 1 if index + 1 < len(scoped) else end
        first = _mn_first_sentence_after_heading(lines, heading, boundary, parser)
        sentence = first[1] if first else ""
        run.append((heading, sentence, bool(MN_ANNOUNCE_RE.search(sentence))))

    return evaluate()


def _check_method_sequence(
    lines: list[str], headings: list[dict], start: int, end: int, parser, doc: AssembledDocument
) -> list[str]:
    out: list[str] = []
    scoped = [heading for heading in headings if start <= heading["line"] <= end]
    for index, heading in enumerate(scoped):
        if heading.get("command") not in {"subsection", "subsubsection"}:
            continue
        boundary = scoped[index + 1]["line"] - 1 if index + 1 < len(scoped) else end
        first = _mn_first_sentence_after_heading(lines, heading, boundary, parser)
        if first is None:
            continue
        line_no, sentence = first
        if not MN_SEQ_OPEN_RE.search(sentence) or MN_CAUSE_EXEMPT_RE.search(sentence):
            continue
        out.extend(
            _mn_finding(
                line_no,
                "Info",
                "P3",
                "M-SEQWORD",
                f"Subsection '{heading['title']}' opens with sequence alone, without a "
                "causal or constraint signal.",
                sentence,
                "Open with the upstream output, remaining constraint, or required capability.",
                "Sequence words state document order but do not establish a technical relation.",
                doc,
            )
        )
    return out


def _mn_equation_blocks(lines: list[str], start: int, end: int) -> list[tuple[int, int, str]]:
    blocks: list[tuple[int, int, str]] = []
    line_no = start
    while line_no <= min(end, len(lines)):
        raw = _mn_strip_latex_comment(lines[line_no - 1])
        begin = _MN_NUMBERED_EQUATION_BEGIN_RE.search(raw)
        if begin is None:
            line_no += 1
            continue
        env = begin.group("env")
        block_end = line_no
        end_re = re.compile(rf"\\end\{{{env}\}}")
        while block_end <= min(end, len(lines)) and not end_re.search(
            _mn_strip_latex_comment(lines[block_end - 1])
        ):
            block_end += 1
        block_end = min(block_end, end, len(lines))
        blocks.append((line_no, block_end, env))
        line_no = block_end + 1
    return blocks


def _mn_visible_between(lines: list[str], start: int, end: int, parser) -> bool:
    return any(
        _mn_visible_text(lines[line_no - 1].strip(), parser)
        for line_no in range(start, min(end, len(lines)) + 1)
        if lines[line_no - 1].strip()
        and not lines[line_no - 1].strip().startswith(parser.get_comment_prefix())
    )


def _check_method_equations(
    lines: list[str], start: int, end: int, parser, doc: AssembledDocument
) -> list[str]:
    blocks = _mn_equation_blocks(lines, start, end)
    if not blocks:
        return []

    groups: list[list[tuple[int, int, str]]] = []
    for block in blocks:
        if not groups or _mn_visible_between(lines, groups[-1][-1][1] + 1, block[0] - 1, parser):
            groups.append([block])
        else:
            groups[-1].append(block)

    out: list[str] = []
    for group in groups:
        visible_after: list[str] = []
        for line_no in range(group[-1][1] + 1, min(end, len(lines)) + 1):
            raw = lines[line_no - 1].strip()
            if not raw or raw.startswith(parser.get_comment_prefix()):
                continue
            uncommented = _mn_strip_latex_comment(raw)
            if _MN_ANY_EQUATION_BEGIN_RE.search(uncommented) or _MN_HEADING_COMMAND_RE.match(
                uncommented
            ):
                break
            visible = _mn_visible_text(uncommented, parser)
            if not visible:
                continue
            visible_after.append(visible)
            if len(visible_after) == MN_EQUATION_LOOKAHEAD:
                break
        if any(MN_EQ_GLOSS_RE.search(text) for text in visible_after):
            continue
        first, last = group[0], group[-1]
        envs = ", ".join(block[2] for block in group)
        out.extend(
            _mn_finding(
                first[0],
                "Minor",
                "P2",
                "M-EQUATION",
                f"The numbered equation group ({envs}) has no 'where' gloss within "
                f"{MN_EQUATION_LOOKAHEAD} non-empty visible lines.",
                f"Equation range {doc.lineref(first[0], last[1])}",
                "Explain new symbols and output semantics, then state the downstream use.",
                "An equation needs purpose, symbol meaning, and a downstream interface to "
                "close the argument.",
                doc,
            )
        )
    return out


def _method_edge_table(headings: list[dict], start: int, end: int) -> list[str]:
    titles = [
        heading["title"]
        for heading in headings
        if start <= heading["line"] <= end
        and heading.get("command") in {"subsection", "subsubsection"}
    ]
    title_list = " -> ".join(titles) if titles else "(no subsection/subsubsection detected)"
    out = [
        "% M-EDGETABLE [Script] Method-module interface skeleton (not a finding)",
        f"% Subsection list: {title_list}",
        "% | Upstream subsection | Upstream output | Connection type | "
        "Intermediate transform | Downstream use |",
        "% | --- | --- | --- | --- | --- |",
    ]
    out.extend(f"% | {title.replace('|', '/')} |  |  |  |  |" for title in titles[:-1])
    out.append("% [LLM] 待填写")
    return out


def _check_method_narrative(
    lines: list[str], headings: list[dict], scope: tuple[int, int], parser, doc: AssembledDocument
) -> list[str]:
    start, end = scope
    out: list[str] = []
    out.extend(_check_method_heading(lines, headings, start, end, parser, doc))
    out.extend(_check_method_sequence(lines, headings, start, end, parser, doc))
    out.extend(_check_method_equations(lines, start, end, parser, doc))
    out.extend(_method_edge_table(headings, start, end))
    return out


# ── Literature review quality checks (A1, A3) ──────────────────

AUTHOR_ENUM_EN = re.compile(
    r"^(?:In \d{4}|.*?\(\d{4}\).*?(?:proposed|introduced|presented|developed|designed))",
    re.IGNORECASE,
)

GAP_KEYWORDS_EN = re.compile(
    r"\b(gap|limitation|however.*(?:no|not|few)|remains|lack|overlooked|"
    r"under-explored|open problem|yet to be|inadequate|insufficient)\b",
    re.IGNORECASE,
)


def _check_lit_review_enumeration(
    lines: list[str], start: int, end: int, parser, doc: AssembledDocument
) -> list[str]:
    """A1: Detect 3+ consecutive author/year enumeration patterns."""
    out: list[str] = []
    consecutive = 0
    streak_start = 0
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(parser.get_comment_prefix()):
            continue
        visible = parser.extract_visible_text(raw)
        if not visible:
            continue
        if AUTHOR_ENUM_EN.search(visible):
            if consecutive == 0:
                streak_start = line_no
            consecutive += 1
        else:
            if consecutive >= 3:
                out.extend(
                    [
                        f"% LIT-REVIEW ({doc.lineref(streak_start, line_no - 1)}) "
                        "[Severity: Major] [Priority: P1]: "
                        f"Author/year enumeration detected ({consecutive} consecutive entries)",
                        "% Suggested: Reorganize by theme clusters with critical analysis.",
                        "% Rationale: Chronological/author enumeration weakens literature synthesis.",
                        "",
                    ]
                )
            consecutive = 0
    if consecutive >= 3:
        out.extend(
            [
                f"% LIT-REVIEW ({doc.lineref(streak_start, min(end, len(lines)))}) "
                "[Severity: Major] [Priority: P1]: "
                f"Author/year enumeration detected ({consecutive} consecutive entries)",
                "% Suggested: Reorganize by theme clusters with critical analysis.",
                "% Rationale: Chronological/author enumeration weakens literature synthesis.",
                "",
            ]
        )
    return out


def _check_gap_derivation(
    lines: list[str], start: int, end: int, parser, doc: AssembledDocument
) -> list[str]:
    """A3: Check last 10 lines of Related Work for research gap language."""
    out: list[str] = []
    scan_start = max(start, end - 10)
    found_gap = False
    for line_no in range(scan_start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(parser.get_comment_prefix()):
            continue
        visible = parser.extract_visible_text(raw)
        if visible and GAP_KEYWORDS_EN.search(visible):
            found_gap = True
            break
    if not found_gap:
        out.extend(
            [
                f"% LIT-REVIEW ({doc.lineref(scan_start, end)}) "
                "[Severity: Major] [Priority: P1]: "
                "No research gap derivation found at end of Related Work",
                "% Suggested: Add explicit gap statement connecting literature to your contribution.",
                "% Rationale: Related Work should conclude by identifying gaps that motivate the study.",
                "",
            ]
        )
    return out


# ── Cross-section logic chain closure (C3) ──────────────────────

CONTRIBUTION_KEYWORDS_EN = re.compile(
    r"\b(we propose|we present|we introduce|our contribution|we design|we develop|"
    r"this paper proposes|this work presents|main contributions)\b",
    re.IGNORECASE,
)
ANSWER_KEYWORDS_EN = re.compile(
    r"\b(we have shown|we demonstrated|results show|results demonstrate|"
    r"experiments confirm|we have proposed|this paper has presented|"
    r"our experiments show|findings indicate|we have addressed)\b",
    re.IGNORECASE,
)

INTRO_BACKGROUND_RE = re.compile(
    r"\b(important|growing|widely used|demand|need|application|applications|"
    r"real-world|industry|practical|in recent years|increasingly)\b",
    re.IGNORECASE,
)
INTRO_PROBLEM_RE = re.compile(
    r"\b(problem|challenge|bottleneck|limitation|difficult|difficulty|issue|"
    r"expensive|costly|fails?|cannot|struggle|insufficient|inefficient)\b",
    re.IGNORECASE,
)
INTRO_PRIOR_RE = re.compile(
    r"\b(existing|previous|prior|earlier|current|traditional|state-of-the-art|"
    r"studies|literature|methods|approaches|however|nevertheless|recent work)\b",
    re.IGNORECASE,
)
TRIAD_PROBLEM_RE = re.compile(
    r"\b(problem|challenge|task|goal|objective|bottleneck|limitation|address)\b",
    re.IGNORECASE,
)
TRIAD_METHOD_RE = re.compile(
    r"\b(propose|present|introduce|design|develop|framework|method|approach|"
    r"model|mechanism|pipeline|strategy)\b",
    re.IGNORECASE,
)
TRIAD_RESULT_RE = re.compile(
    r"\b(result|results|improve|improvement|achieve|achieves|outperform|gain|"
    r"accuracy|f1|mae|mse|latency|throughput|benchmark|experiments show)\b",
    re.IGNORECASE,
)
TRIAD_CONTRIBUTION_RE = re.compile(
    r"\b(contribution|contributions|novel|we propose|we present|we introduce|"
    r"main contributions)\b",
    re.IGNORECASE,
)

# Numeric citation-style bracket, e.g. [12] / [3, 7] / [1-4]. A bare "[" also
# matches math intervals and stray optional-argument brackets, which falsely
# counted as "prior work referenced" in the funnel check (A-EN-8).
NUMERIC_CITE_RE = re.compile(r"\[\d+(?:\s*[,-–]\s*\d+)*\]")


def _section_visible_lines(
    lines: list[str], bounds: tuple[int, int], parser
) -> list[tuple[int, str]]:
    visible_lines: list[tuple[int, str]] = []
    comment_prefix = parser.get_comment_prefix()
    start, end = bounds
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(comment_prefix):
            continue
        visible = parser.extract_visible_text(raw)
        if visible:
            visible_lines.append((line_no, visible))
    return visible_lines


def _coverage_map(text: str) -> dict[str, bool]:
    lowered = text.lower()
    return {
        "problem": bool(TRIAD_PROBLEM_RE.search(lowered)),
        "method": bool(TRIAD_METHOD_RE.search(lowered)),
        "result": bool(TRIAD_RESULT_RE.search(lowered) or re.search(r"\d+(?:\.\d+)?%?", lowered)),
        "contribution": bool(TRIAD_CONTRIBUTION_RE.search(lowered)),
    }


def _check_introduction_funnel(
    lines: list[str], sections: dict[str, tuple[int, int]], parser, doc: AssembledDocument
) -> list[str]:
    """Check whether introduction follows background -> problem -> prior work -> contribution."""
    out: list[str] = []
    if "introduction" not in sections:
        return out

    visible_lines = _section_visible_lines(lines, sections["introduction"], parser)
    if len(visible_lines) < 3:
        return out

    first_background = first_problem = first_prior = first_contribution = None
    for line_no, visible in visible_lines:
        lowered = visible.lower()
        if first_background is None and INTRO_BACKGROUND_RE.search(lowered):
            first_background = line_no
        if first_problem is None and INTRO_PROBLEM_RE.search(lowered):
            first_problem = line_no
        if first_prior is None and (
            INTRO_PRIOR_RE.search(lowered)
            or "\\cite{" in lines[line_no - 1]
            or NUMERIC_CITE_RE.search(visible)
        ):
            first_prior = line_no
        if first_contribution is None and CONTRIBUTION_KEYWORDS_EN.search(lowered):
            first_contribution = line_no

    if first_contribution is None:
        return out

    if first_problem is None or first_contribution < first_problem:
        out.extend(
            [
                f"% INTRODUCTION ({doc.lineref(first_contribution)}) [Severity: Major] [Priority: P1]: "
                "Introduction may jump from background directly to contribution.",
                "% Suggested: Insert the unresolved technical bottleneck before presenting the method.",
                "% Rationale: Readers need the problem statement before the solution.",
                "",
            ]
        )

    if first_problem is not None and first_prior is None:
        out.extend(
            [
                f"% INTRODUCTION ({doc.lineref(first_problem)}) [Severity: Major] [Priority: P1]: "
                "Introduction states the problem but does not derive it from prior work limitations.",
                "% Suggested: Add a prior-work paragraph explaining what existing methods still fail to solve.",
                "% Rationale: The contribution should be motivated by concrete insufficiencies in the literature.",
                "",
            ]
        )
    elif (
        first_problem is not None
        and first_prior is not None
        and first_contribution is not None
        and first_prior > first_contribution
    ):
        out.extend(
            [
                f"% INTRODUCTION ({doc.lineref(first_contribution)}) [Severity: Major] [Priority: P1]: "
                "Contribution claim appears before prior-work insufficiencies are established.",
                "% Suggested: Reorder the introduction so literature limitations appear before the paper contribution.",
                "% Rationale: This preserves the background -> bottleneck -> prior effort -> contribution funnel.",
                "",
            ]
        )
    return out


def _check_tri_section_alignment(
    content: str, lines: list[str], sections: dict[str, tuple[int, int]], parser
) -> list[str]:
    """Check alignment among abstract, contribution source, and conclusion."""
    out: list[str] = []
    if "introduction" not in sections or "conclusion" not in sections:
        return out

    abstract_text = extract_abstract(content)
    if not abstract_text:
        return out

    intro_text = " ".join(
        text for _, text in _section_visible_lines(lines, sections["introduction"], parser)
    )
    conclusion_text = " ".join(
        text for _, text in _section_visible_lines(lines, sections["conclusion"], parser)
    )
    if not intro_text or not conclusion_text:
        return out

    coverage = {
        "abstract": _coverage_map(abstract_text),
        "contribution_source": _coverage_map(intro_text),
        "conclusion": _coverage_map(conclusion_text),
    }
    required_facets = {
        facet
        for facet in ("problem", "method", "result", "contribution")
        if sum(1 for sec in coverage.values() if sec[facet]) >= 2
    }

    mismatches: list[str] = []
    for section_name, section_coverage in coverage.items():
        missing = sorted(facet for facet in required_facets if not section_coverage[facet])
        if len(missing) >= 2 or (
            section_name in {"abstract", "conclusion"}
            and ("result" in missing or "contribution" in missing)
        ):
            mismatches.append(f"{section_name} missing {', '.join(missing)}")

    if coverage["contribution_source"]["contribution"]:
        if not coverage["abstract"]["contribution"]:
            mismatches.append("abstract missing contribution claim")
        if not coverage["conclusion"]["contribution"]:
            mismatches.append("conclusion missing contribution response")
    if coverage["abstract"]["method"] and not coverage["conclusion"]["result"]:
        mismatches.append("conclusion missing result evidence")

    if mismatches:
        out.extend(
            [
                "% LOGIC [Severity: Major] [Priority: P1]: "
                "Abstract, contribution claims, and conclusion may be misaligned.",
                f"% Observation: {'; '.join(mismatches)}.",
                "% Suggested: Make sure all three sections consistently state the problem, method, key results, and contribution.",
                "% Rationale: These sections should tell the same core story with different emphasis, not diverge.",
                "",
            ]
        )
    return out


def _check_cross_section_closure(
    lines: list[str], sections: dict[str, tuple[int, int]], parser, doc: AssembledDocument
) -> list[str]:
    """C3: Verify that intro contributions are answered in conclusion."""
    out: list[str] = []
    if "introduction" not in sections or "conclusion" not in sections:
        return out

    intro_start, intro_end = sections["introduction"]
    concl_start, concl_end = sections["conclusion"]

    intro_claims = 0
    for line_no in range(intro_start, min(intro_end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(parser.get_comment_prefix()):
            continue
        visible = parser.extract_visible_text(raw)
        if visible and CONTRIBUTION_KEYWORDS_EN.search(visible):
            intro_claims += 1

    if intro_claims == 0:
        return out

    concl_answers = 0
    for line_no in range(concl_start, min(concl_end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(parser.get_comment_prefix()):
            continue
        visible = parser.extract_visible_text(raw)
        if visible and ANSWER_KEYWORDS_EN.search(visible):
            concl_answers += 1

    if concl_answers == 0:
        out.extend(
            [
                f"% LOGIC ({doc.lineref(concl_start, concl_end)}) "
                "[Severity: Major] [Priority: P1]: "
                "[Script] Cross-section logic chain may be incomplete",
                f"% Observation: {intro_claims} contribution claim(s) in Introduction "
                "but no explicit answer language in Conclusion.",
                "% Suggested: Add statements that explicitly address each contribution.",
                "% Rationale: Conclusion should close the logic chain opened in Introduction.",
                "",
            ]
        )
    return out


# ── Motivation red-thread closure diagnostic (opt-in: --motivation-thread) ──
#
# Read-only diagnostic that maps each Introduction promise/claim to its
# downstream echo. It is intentionally heuristic (keyword + token overlap) and
# every finding is tagged [Script] with a manual-verification note, in the same
# spirit as the cross-section (C3) check above. It never rewrites the source.

_THREAD_STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "for",
    "with",
    "via",
    "that",
    "this",
    "these",
    "those",
    "from",
    "into",
    "onto",
    "our",
    "ours",
    "their",
    "such",
    "more",
    "most",
    "than",
    "then",
    "thus",
    "also",
    "which",
    "while",
    "where",
    "when",
    "paper",
    "work",
    "study",
    "propose",
    "proposed",
    "present",
    "presents",
    "presented",
    "introduce",
    "introduces",
    "method",
    "methods",
    "approach",
    "approaches",
    "model",
    "models",
    "framework",
    "results",
    "result",
    "show",
    "shows",
    "shown",
    "using",
    "used",
    "based",
    "novel",
    "new",
    "main",
    "contribution",
    "contributions",
    "achieve",
    "achieves",
    "improve",
    "improves",
    "improvement",
    "demonstrate",
    "demonstrates",
}


def _thread_tokens(text: str) -> set[str]:
    """Content tokens for overlap matching: English words (>=4 chars, non-stop)
    plus CJK character bigrams so the heuristic also works on mixed-language
    manuscripts."""
    lowered = text.lower()
    tokens: set[str] = set()
    for word in re.findall(r"[a-z][a-z'-]{3,}", lowered):
        if word not in _THREAD_STOPWORDS:
            tokens.add(word)
    for run in re.findall(r"[一-鿿]{2,}", lowered):
        for i in range(len(run) - 1):
            tokens.add(run[i : i + 2])
    return tokens


def _thread_best_match(
    promise_tokens: set[str], candidates: list[tuple[int, str]], min_overlap: int = 2
) -> tuple[int, int] | None:
    """Return (line_no, overlap) of the best-overlapping candidate line, or None."""
    best_line = None
    best_score = 0
    for line_no, text in candidates:
        overlap = len(promise_tokens & _thread_tokens(text))
        if overlap > best_score:
            best_score = overlap
            best_line = line_no
    if best_line is not None and best_score >= min_overlap:
        return best_line, best_score
    return None


_THREAD_INTRO_KW = ("introduction", "绪论", "引言")
_THREAD_RELATED_KW = ("related", "literature review", "文献综述", "相关工作")
_THREAD_CLOSURE_KW = (
    "discussion",
    "analysis",
    "conclusion",
    "讨论",
    "分析",
    "结论",
    "总结",
    "展望",
)
_LATEX_HEADING_RE = re.compile(r"\\(?:chapter|(?:sub)*section|paragraph)\*?\s*\{([^}]*)\}")
_TYPST_HEADING_RE = re.compile(r"^=+\s+(.*)$")


def _thread_headings(lines: list[str], parser) -> list[tuple[int, str]]:
    """Generic heading scan returning (line_no, lowercased title).

    Unlike the parser's known-section table, this treats ANY heading as a
    boundary, so common plural/compound titles ('Experiments', 'Experimental
    Results', 'Results and Discussion') still delimit the evidence body. Used
    only by the opt-in motivation-thread diagnostic; nothing else relies on it.
    """
    is_typst = parser.get_comment_prefix() == "//"
    heads: list[tuple[int, str]] = []
    for i, raw in enumerate(lines, 1):
        stripped = raw.strip()
        match = _TYPST_HEADING_RE.match(stripped) if is_typst else _LATEX_HEADING_RE.match(stripped)
        if match:
            heads.append((i, match.group(1).strip().lower()))
    return heads


def _check_motivation_thread(
    lines: list[str], sections: dict[str, tuple[int, int]], parser
) -> list[str]:
    """Full-paper red-thread diagnostic: Promise Map + Closure Map.

    Promise Map: each Introduction promise ("we propose X") -> a Results/
    Experiment line that plausibly tests it.
    Closure Map: each Introduction claim -> a Discussion/Conclusion line that
    plausibly resolves it.
    """
    p = parser.get_comment_prefix()
    out: list[str] = []
    heads = _thread_headings(lines, parser)
    intro_pos = next(
        (idx for idx, (_, title) in enumerate(heads) if any(k in title for k in _THREAD_INTRO_KW)),
        None,
    )
    if intro_pos is None and "introduction" not in sections:
        return [
            f"{p} MOTIVATION-THREAD [Script]: Introduction not found; red-thread diagnostic skipped."
        ]

    if intro_pos is not None:
        intro_line = heads[intro_pos][0]
        intro_end = heads[intro_pos + 1][0] - 1 if intro_pos + 1 < len(heads) else len(lines)
    else:
        intro_line, intro_end = sections["introduction"]

    closure_line = next(
        (
            ln
            for ln, title in heads
            if ln > intro_end and any(k in title for k in _THREAD_CLOSURE_KW)
        ),
        None,
    )
    related_ranges: list[tuple[int, int]] = []
    for j, (ln, title) in enumerate(heads):
        if any(k in title for k in _THREAD_RELATED_KW):
            end = heads[j + 1][0] - 1 if j + 1 < len(heads) else len(lines)
            related_ranges.append((ln, end))

    promises = [
        (ln, txt)
        for ln, txt in _section_visible_lines(lines, (intro_line, intro_end), parser)
        if CONTRIBUTION_KEYWORDS_EN.search(txt)
    ]
    evidence_end = closure_line - 1 if closure_line else len(lines)
    evidence_lines = [
        (ln, txt)
        for ln, txt in _section_visible_lines(lines, (intro_end + 1, evidence_end), parser)
        if not any(lo <= ln <= hi for lo, hi in related_ranges)
    ]
    closure_lines = (
        _section_visible_lines(lines, (closure_line, len(lines)), parser) if closure_line else []
    )

    out.append(
        f"{p} MOTIVATION-THREAD [Script] (heuristic): full-paper red-thread closure diagnostic."
    )
    out.append(
        f"{p} Note: keyword + token-overlap heuristic; verify manually, false positives possible."
    )
    out.append("")

    # ── Promise Map ──
    out.append(
        f"{p} MOTIVATION-THREAD: Promise Map (Introduction promise -> Results/Experiment evidence)"
    )
    if not promises:
        out.append(
            f"{p} - No explicit 'we propose / contribution' promise detected in Introduction "
            "[Severity: Moderate] [Priority: P2]."
        )
    else:
        for idx, (ln, txt) in enumerate(promises[:10], 1):
            if not evidence_lines:
                out.append(
                    f"{p} - P{idx} (Intro L{ln}) -> [NO EVIDENCE BODY FOUND] "
                    "[Severity: Major] [Priority: P1]: no body text between Introduction and Conclusion"
                )
                continue
            match = _thread_best_match(_thread_tokens(txt), evidence_lines)
            if match:
                out.append(
                    f"{p} - P{idx} (Intro L{ln}) -> Evidence L{match[0]} "
                    f"[matched, overlap={match[1]}]"
                )
            else:
                out.append(
                    f"{p} - P{idx} (Intro L{ln}) -> [NO EVIDENCE FOUND] "
                    "[Severity: Major] [Priority: P1]: promise not tested in the body"
                )
                out.append(f"{p}   Promise: {txt[:100]}")
    out.append("")

    # ── Closure Map ──
    out.append(
        f"{p} MOTIVATION-THREAD: Closure Map (Introduction claim -> Discussion/Conclusion closure)"
    )
    if not promises:
        out.append(f"{p} - No explicit claim to close.")
    elif not closure_lines:
        out.append(
            f"{p} - [NO DISCUSSION/CONCLUSION SECTION] [Severity: Major] [Priority: P1]: "
            "claims cannot be closed."
        )
    else:
        for idx, (ln, txt) in enumerate(promises[:10], 1):
            match = _thread_best_match(_thread_tokens(txt), closure_lines)
            if match:
                out.append(
                    f"{p} - C{idx} (Intro L{ln}) -> Closure L{match[0]} [closed, overlap={match[1]}]"
                )
            else:
                out.append(
                    f"{p} - C{idx} (Intro L{ln}) -> [UNCLOSED] [Severity: Major] [Priority: P1]: "
                    "claim not resolved in Discussion/Conclusion"
                )
    out.append("")

    # ── Evidence-without-promise (lightweight, capped) ──
    if promises and evidence_lines:
        promise_union: set[str] = set()
        for _, txt in promises:
            promise_union |= _thread_tokens(txt)
        orphans = [
            (ln, txt)
            for ln, txt in evidence_lines
            if TRIAD_RESULT_RE.search(txt)
            and re.search(r"\d", txt)
            and not (_thread_tokens(txt) & promise_union)
        ]
        if orphans:
            out.append(
                f"{p} MOTIVATION-THREAD: Evidence-without-promise "
                "(results not traceable to an Introduction promise)"
            )
            for ln, txt in orphans[:5]:
                out.append(f"{p} - Evidence L{ln} [Severity: Moderate] [Priority: P2]: {txt[:90]}")
            out.append("")
    return out


def analyze(
    file_path: Path,
    section: str | None = None,
    cross_section: bool = False,
    motivation_thread: bool = False,
) -> list[str]:
    parser = get_parser(file_path)
    doc = assemble(file_path)
    content = doc.content
    lines = doc.lines
    sections = parser.split_sections(content)

    matched: list[str] = []
    if section:
        matched, available = resolve_section_keys(section, sections)
        if not matched:
            return [
                f"% ERROR [Severity: Critical] [Priority: P0]: Section not found: {section} "
                f"(available: {', '.join(available) if available else '(none detected)'})"
            ]
        ranges = [sections[key] for key in matched]
    else:
        ranges = list(sections.values()) if sections else [(1, len(lines))]

    out: list[str] = []
    previous_visible = ""
    for start, end in ranges:
        for line_no in range(start, min(end, len(lines)) + 1):
            raw = lines[line_no - 1].strip()
            if not raw or raw.startswith(parser.get_comment_prefix()):
                continue

            visible = parser.extract_visible_text(raw)
            if not visible:
                continue

            if _needs_method_justification(visible):
                out.extend(
                    [
                        f"% METHODOLOGY ({doc.lineref(line_no)}) [Severity: Major] [Priority: P1]: "
                        "Method choice lacks explicit justification",
                        f"% Current: {visible}",
                        "% Suggested: Add rationale (e.g., efficiency/accuracy/reproducibility reasons).",
                        "% Rationale: Method statements should explain why the approach is selected.",
                        "",
                    ]
                )

            if (
                previous_visible
                and not _has_transition(visible)
                and re.search(
                    r"\b(problem|challenge|noisy|difficult)\b", previous_visible, re.IGNORECASE
                )
                and re.search(r"\b(we propose|we design|our method)\b", visible, re.IGNORECASE)
            ):
                out.extend(
                    [
                        f"% LOGIC ({doc.lineref(line_no)}) [Severity: Major] [Priority: P1]: "
                        "Potential logical jump between problem and solution",
                        f"% Current: {visible}",
                        "% Suggested: Add explicit transition (e.g., Therefore/Thus/To address this).",
                        "% Rationale: Strengthens paragraph-level coherence.",
                        "",
                    ]
                )

            previous_visible = visible

    # ── Section-level checks ───────────────────────────────────
    if sections:
        if not section and "introduction" in sections:
            out.extend(_check_introduction_funnel(lines, sections, parser, doc))

        related_key = "related"
        if related_key in sections:
            r_start, r_end = sections[related_key]
            if not section or related_key in matched:
                out.extend(_check_lit_review_enumeration(lines, r_start, r_end, parser, doc))
                out.extend(_check_gap_derivation(lines, r_start, r_end, parser, doc))

        if cross_section and not section:
            out.extend(_check_cross_section_closure(lines, sections, parser, doc))
        if not section:
            out.extend(_check_tri_section_alignment(content, lines, sections, parser))
        if motivation_thread and not section:
            out.extend(_check_motivation_thread(lines, sections, parser))

        if section and any(key == "method" or key.startswith("method_") for key in matched):
            headings = parser.extract_headings(content)
            for key in matched:
                if key == "method" or key.startswith("method_"):
                    out.extend(_check_method_narrative(lines, headings, sections[key], parser, doc))

    if not out:
        out.append("% LOGIC/METHODOLOGY: No rule-based coherence issues detected.")

    warning_lines = doc.warning_lines(parser.get_comment_prefix())
    if warning_lines:
        out = warning_lines + out
    return out


def main() -> int:
    cli = argparse.ArgumentParser(
        description="Logic and methodology analysis for LaTeX/Typst files"
    )
    cli.add_argument("file", type=Path, help="Target .tex/.typ file")
    cli.add_argument("--section", help="Section name to analyze")
    cli.add_argument(
        "--cross-section",
        action="store_true",
        help="Enable cross-section logic chain closure check",
    )
    cli.add_argument(
        "--motivation-thread",
        action="store_true",
        help="Run full-paper motivation red-thread diagnostic (promise map + closure map)",
    )
    args = cli.parse_args()

    if not args.file.exists():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        return 1

    print("\n".join(analyze(args.file, args.section, args.cross_section, args.motivation_thread)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
