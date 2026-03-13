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
    from parsers import get_parser
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import get_parser


TRANSITIONS = {
    "addition": {"furthermore", "moreover", "in addition", "additionally"},
    "contrast": {"however", "nevertheless", "in contrast", "conversely"},
    "cause": {"therefore", "consequently", "as a result", "thus"},
}


def _has_transition(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for values in TRANSITIONS.values() for token in values)


def _needs_method_justification(text: str) -> bool:
    lowered = text.lower()
    if "we use" not in lowered and "we adopt" not in lowered:
        return False
    return not any(marker in lowered for marker in ["because", "due to", "to ", "for "])


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


def _check_lit_review_enumeration(lines: list[str], start: int, end: int, parser) -> list[str]:
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
                        f"% LIT-REVIEW (Lines {streak_start}-{line_no - 1}) "
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
                f"% LIT-REVIEW (Lines {streak_start}-{min(end, len(lines))}) "
                "[Severity: Major] [Priority: P1]: "
                f"Author/year enumeration detected ({consecutive} consecutive entries)",
                "% Suggested: Reorganize by theme clusters with critical analysis.",
                "% Rationale: Chronological/author enumeration weakens literature synthesis.",
                "",
            ]
        )
    return out


def _check_gap_derivation(lines: list[str], start: int, end: int, parser) -> list[str]:
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
                f"% LIT-REVIEW (Lines {scan_start}-{end}) "
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


def _check_cross_section_closure(
    lines: list[str], sections: dict[str, tuple[int, int]], parser
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
                f"% LOGIC (Lines {concl_start}-{concl_end}) "
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


def analyze(file_path: Path, section: str | None = None, cross_section: bool = False) -> list[str]:
    parser = get_parser(file_path)
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.split("\n")
    sections = parser.split_sections(content)

    if section:
        key = section.lower()
        if key not in sections:
            return [f"% ERROR [Severity: Critical] [Priority: P0]: Section not found: {section}"]
        ranges = [sections[key]]
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
                        f"% METHODOLOGY (Line {line_no}) [Severity: Major] [Priority: P1]: "
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
                        f"% LOGIC (Line {line_no}) [Severity: Major] [Priority: P1]: "
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
        related_key = "related"
        if related_key in sections:
            r_start, r_end = sections[related_key]
            if not section or section.lower() == related_key:
                out.extend(_check_lit_review_enumeration(lines, r_start, r_end, parser))
                out.extend(_check_gap_derivation(lines, r_start, r_end, parser))

        if cross_section and not section:
            out.extend(_check_cross_section_closure(lines, sections, parser))

    if not out:
        out.append("% LOGIC/METHODOLOGY: No rule-based coherence issues detected.")
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
    args = cli.parse_args()

    if not args.file.exists():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        return 1

    print("\n".join(analyze(args.file, args.section, args.cross_section)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
