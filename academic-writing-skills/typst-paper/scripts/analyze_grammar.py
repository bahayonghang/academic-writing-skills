#!/usr/bin/env python3
"""
Grammar Analysis (MVP) for English LaTeX/Typst papers.

Outputs diff-comment style suggestions without modifying source files.
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
UNSUPPORTED_GOALS = {"concision": "sentences", "coherence": "logic"}


def _match_case(source: str, replacement: str) -> str:
    """Carry the source span's leading casing over to the replacement.

    Rules match case-insensitively, so a sentence-initial "We propose method"
    used to come back as "we propose a method" — the fix introduced a new error.
    """
    if not source or not replacement:
        return replacement
    if source[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def _contract_lines(cp: str, changed: str, protected: str, risk_flags: str) -> list[str]:
    return [
        f"{cp} Changed:       {changed}",
        f"{cp} Protected:     {protected}",
        f"{cp} Meaning-Check: NEEDS-LLM",
        f"{cp} Risk-Flags:    {risk_flags}",
    ]


# MVP rule set: 4 high-precision subject-verb / article rules. This is a
# deliberately small, conservative set — not a general grammar engine.
def _apply_rules(text: str) -> list[tuple[str, str, str]]:
    """Return list of (issue, revised, rationale).

    Substitutions run case-insensitively on the original text so unrelated
    casing (e.g. acronyms like BERT) is preserved (E12); the matched span keeps
    its own leading capitalization via ``_match_case``.
    """
    findings: list[tuple[str, str, str]] = []
    rules = [
        (
            r"\bwe propose method\b",
            "we propose a method",
            "Grammar: Article missing before singular count noun.",
        ),
        (
            r"\bthe data shows\b",
            "the data show",
            "Grammar: Subject-verb agreement ('data' is plural in formal academic usage).",
        ),
        (
            r"\bthis approach get\b",
            "this approach gets",
            "Grammar: Third-person singular verb form required.",
        ),
        (
            r"\bthese method\b",
            "these methods",
            "Grammar: Plural demonstrative requires plural noun.",
        ),
    ]

    for pattern, replacement, rationale in rules:
        if re.search(pattern, text, re.IGNORECASE):
            revised = re.sub(
                pattern,
                lambda match, target=replacement: _match_case(match.group(0), target),
                text,
                flags=re.IGNORECASE,
            )
            findings.append((pattern, revised, rationale))
    return findings


def analyze(
    file_path: Path,
    section: str | None = None,
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
                f"{cp} GRAMMAR [Severity: Info] [Priority: P3] [Script]: "
                f"This module has no {goal} rules; run the "
                f"`{UNSUPPORTED_GOALS[goal]}` module instead."
            ]
        )

    selected_ranges: list[tuple[int, int]] = []
    if section:
        matched, available = resolve_section_keys(section, sections)
        if not matched:
            return [
                f"{cp} ERROR [Severity: Critical] [Priority: P0]: Section not found: {section}; "
                f"available: {', '.join(available) if available else '(none detected)'}"
            ]
        selected_ranges.extend(sections[key] for key in matched)
    else:
        if sections:
            selected_ranges.extend(sections.values())
        else:
            selected_ranges.append((1, len(lines)))

    output: list[str] = []
    for start, end in selected_ranges:
        for line_no in range(start, min(end, len(lines)) + 1):
            raw = lines[line_no - 1].strip()
            if not raw or raw.startswith(parser.get_comment_prefix()):
                continue
            visible = parser.extract_visible_text(raw)
            if not visible:
                continue

            findings = _apply_rules(visible)
            for pattern, revised, rationale in findings:
                location = doc.lineref(line_no) if doc is not None else f"Line {line_no}"
                output.extend(
                    [
                        f"{cp} GRAMMAR ({location}) [Severity: Major] [Priority: P1] "
                        f"[Script]: Rule hit: {pattern}",
                        f"{cp} Original: {visible}",
                        f"{cp} Revised:  {revised}",
                        f"{cp} Rationale: {rationale}",
                        *_contract_lines(
                            cp,
                            f"1 rule-based correction ({pattern})",
                            "none",
                            "none",
                        ),
                        "",
                    ]
                )
    if not output:
        output.append(f"{cp} GRAMMAR: No rule-based issues detected in selected scope.")
    return warning_lines + header + output


def main() -> int:
    cli = argparse.ArgumentParser(description="Grammar analysis for LaTeX/Typst files (MVP)")
    cli.add_argument("file", type=Path, help="Target .tex or .typ file")
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
