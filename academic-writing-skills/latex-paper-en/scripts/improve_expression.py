#!/usr/bin/env python3
"""
Academic expression improver (MVP) for LaTeX/Typst papers.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from parsers import get_parser, resolve_section_keys
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import get_parser, resolve_section_keys

try:
    from tex_loader import assemble, read_text_robust
except ImportError:
    try:
        from typ_loader import assemble, read_text_robust
    except ImportError:
        assemble = None
        read_text_robust = None


GOAL_CHOICES = ("grammar", "clarity", "concision", "coherence")
STRENGTH_CHOICES = ("minimal", "moderate", "restructure")

# Goals this module has no rules for. Routed explicitly instead of returning an
# empty result that reads like "nothing to fix".
UNSUPPORTED_GOALS = {"coherence": "logic"}

# Note: use->employ and show->demonstrate were removed because the deai guide
# lists "we use ..." as correct and "demonstrate the effectiveness" as an AI
# tell — blindly applying them fought the de-AI module's own advice (E15).
WEAK_VERBS = {
    r"\bget\b": "obtain",
}

WEAK_PHRASES = {
    r"\ba lot of\b": "many",
}

# Detectable but context-dependent: a rule cannot tell a weak use from a correct
# one, so these are reported as candidates and never auto-applied. Measured
# breakage when they were auto-applied: "Make sure" -> "develop sure",
# "make use of" -> "develop use of", "very few" -> "highly few"; deleting
# "kind of" changes the meaning of "a kind of transformer".
CANDIDATE_PATTERNS = {
    r"\bmake\b": 'weak verb "make" is context-dependent ("make sure", "make use of")',
    r"\bvery\b": 'intensifier "very" is context-dependent ("very few")',
    r"\bkind of\b": 'deleting "kind of" changes meaning in "a kind of X"',
}

# Plain-text tokens that must survive polishing verbatim: statistics, values
# with units, and identifier-shaped names (models, datasets, genes). These carry
# no LaTeX/Typst markup, so the syntax guards do not cover them.
# Classification and the tokens rules cannot detect: references/writing/protected-tokens.md
PROTECTED_PATTERNS = (
    r"\bp\s*[<>=]{1,2}\s*0?\.\d+",
    r"\b\d+(?:\.\d+)?\s*\\?%",
    r"\b\d+(?:\.\d+)?\s*(?:GB|MB|KB|TB|ms|ns|Hz|kHz|MHz|GHz|kg|mg|km|cm|mm|nm)\b",
    r"\b[A-Za-z]+[-_]?\d+[A-Za-z0-9]*\b",
    r"\b[A-Z][A-Za-z]*-[A-Za-z][A-Za-z0-9]*\b",
    r"\b[A-Z]{2,}\b",
)

_MASK = "\x00P{}\x00"


def _match_case(source: str, replacement: str) -> str:
    """Carry the source token's casing over to the replacement.

    Without this a sentence-initial "Make" became "develop" and an acronym lost
    its shape, so the "fix" produced worse English than the input.
    """
    if not source or not replacement:
        return replacement
    if source.isupper() and len(source) > 1:
        return replacement.upper()
    if source[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def _find_protected(text: str) -> list[str]:
    spans: list[tuple[int, int, str]] = []
    for pattern in PROTECTED_PATTERNS:
        for match in re.finditer(pattern, text):
            spans.append((match.start(), match.end(), match.group(0)))
    spans.sort(key=lambda item: (item[0], -item[1]))

    kept: list[tuple[int, int, str]] = []
    last_end = -1
    for start, end, token in spans:
        if start < last_end:
            continue
        kept.append((start, end, token))
        last_end = end
    return [token for _start, _end, token in kept]


def _mask_protected(text: str, tokens: list[str]) -> str:
    masked = text
    for index, token in enumerate(tokens):
        masked = masked.replace(token, _MASK.format(index), 1)
    return masked


def _unmask_protected(text: str, tokens: list[str]) -> str:
    restored = text
    for index, token in enumerate(tokens):
        restored = restored.replace(_MASK.format(index), token)
    return restored


def _substitute(text: str, pattern: str, replacement: str) -> str:
    return re.sub(
        pattern,
        lambda match: _match_case(match.group(0), replacement),
        text,
        flags=re.IGNORECASE,
    )


def _enhance(text: str) -> tuple[str, list[str], list[str], list[str]]:
    """Return (revised, rationales, applied edits, protected tokens).

    Protected tokens are masked before substitution so a rule can never rewrite
    a statistic, a unit, or a model/dataset name. Whitespace is left exactly as
    the source had it — collapsing it silently reflowed the author's lines.
    """
    protected = _find_protected(text)
    revised = _mask_protected(text, protected)
    rationales: list[str] = []
    applied: list[str] = []

    for label, table in (
        ("Weak verb replaced", WEAK_VERBS),
        ("Weak phrase adjusted", WEAK_PHRASES),
    ):
        for pattern, replacement in table.items():
            match = re.search(pattern, revised, re.IGNORECASE)
            if not match:
                continue
            revised = _substitute(revised, pattern, replacement)
            rationales.append(f"{label}: {pattern} -> {replacement}")
            applied.append(f"{match.group(0)} -> {_match_case(match.group(0), replacement)}")

    return _unmask_protected(revised, protected), rationales, applied, protected


def _find_candidates(text: str) -> list[tuple[str, str]]:
    """Return (matched token, reason) for context-dependent patterns."""
    found: list[tuple[str, str]] = []
    for pattern, reason in CANDIDATE_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            found.append((match.group(0), reason))
    return found


def _contract_lines(cp: str, changed: str, protected: str, risk_flags: str) -> list[str]:
    return [
        f"{cp} Changed:       {changed}",
        f"{cp} Protected:     {protected}",
        f"{cp} Meaning-Check: NEEDS-LLM",
        f"{cp} Risk-Flags:    {risk_flags}",
    ]


def analyze(
    file_path: Path,
    section: str | None,
    goal: str = "grammar",
    strength: str = "minimal",
) -> list[str]:
    parser = get_parser(file_path)
    doc = None
    warning_lines: list[str] = []
    if assemble is not None:
        doc = assemble(file_path)
        content, lines = doc.content, doc.lines
    elif read_text_robust is not None:
        content, _warning = read_text_robust(file_path)
        lines = content.split("\n")
    else:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")
    sections = parser.split_sections(content)
    cp = parser.get_comment_prefix()
    if doc is not None:
        warning_lines = doc.warning_lines(cp)

    header = [f"{cp} CONTRACT [Script]: goal={goal} strength={strength}"]

    if goal in UNSUPPORTED_GOALS:
        return (
            warning_lines
            + header
            + [
                f"{cp} EXPRESSION [Severity: Info] [Priority: P3] [Script]: "
                f"This module has no {goal} rules; run the "
                f"`{UNSUPPORTED_GOALS[goal]}` module instead."
            ]
        )

    if section:
        matched, available = resolve_section_keys(section, sections)
        if not matched:
            return [
                f"{cp} ERROR [Severity: Critical] [Priority: P0]: Section not found: {section}; "
                f"available: {', '.join(available) if available else '(none detected)'}"
            ]
        ranges = [sections[key] for key in matched]
    else:
        ranges = list(sections.values()) if sections else [(1, len(lines))]

    out: list[str] = []
    for start, end in ranges:
        for line_no in range(start, min(end, len(lines)) + 1):
            raw = lines[line_no - 1].strip()
            if not raw or raw.startswith(parser.get_comment_prefix()):
                continue
            visible = parser.extract_visible_text(raw)
            if not visible:
                continue
            location = doc.lineref(line_no) if doc is not None else f"Line {line_no}"

            revised, rationales, applied, protected = _enhance(visible)
            if rationales and revised != visible:
                out.extend(
                    [
                        f"{cp} EXPRESSION ({location}) [Severity: Minor] [Priority: P2] "
                        f"[Script]: Improve academic tone",
                        f"{cp} Original: {visible}",
                        f"{cp} Revised:  {revised}",
                        f"{cp} Rationale: {'; '.join(rationales)}",
                        *_contract_lines(
                            cp,
                            f"{len(applied)} lexical substitution(s): {'; '.join(applied)}",
                            ", ".join(protected) if protected else "none",
                            "lexical-substitution",
                        ),
                        "",
                    ]
                )

            for token, reason in _find_candidates(visible):
                out.extend(
                    [
                        f"{cp} EXPRESSION ({location}) [Severity: Minor] [Priority: P3] "
                        f"[Script]: Weak-expression candidate",
                        f"{cp} Original: {visible}",
                        f"{cp} Candidate: {reason}; not auto-applied",
                        *_contract_lines(
                            cp,
                            f"none (candidate only: {token})",
                            ", ".join(protected) if protected else "none",
                            "not-assessed",
                        ),
                        "",
                    ]
                )
    if not out:
        out.append(f"{cp} EXPRESSION: No weak-expression patterns detected.")
    return warning_lines + header + out


def main() -> int:
    cli = argparse.ArgumentParser(
        description="Academic expression improvement for LaTeX/Typst files"
    )
    cli.add_argument("file", type=Path, help="Target .tex/.typ file")
    cli.add_argument("--section", help="Section name to analyze")
    cli.add_argument(
        "--goal",
        choices=GOAL_CHOICES,
        default="grammar",
        help="Edit goal: what this pass is for (default: grammar)",
    )
    cli.add_argument(
        "--strength",
        choices=STRENGTH_CHOICES,
        default="minimal",
        help="Edit strength: how far the edit may go (default: minimal)",
    )
    args = cli.parse_args()

    if not args.file.exists():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        return 1

    print("\n".join(analyze(args.file, args.section, args.goal, args.strength)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
