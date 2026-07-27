#!/usr/bin/env python3
"""
Long sentence analyzer (MVP) for LaTeX/Typst papers.
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


CLAUSE_MARKERS = {"which", "that", "because", "although", "while", "whereas", "if", "when"}

GOAL_CHOICES = ("grammar", "clarity", "concision", "coherence")
STRENGTH_CHOICES = ("minimal", "moderate", "restructure")

# Goals this module has no rules for. Routed explicitly instead of returning an
# empty result that reads like "nothing to fix".
UNSUPPORTED_GOALS = {"coherence": "logic"}


def _contract_lines(cp: str, changed: str, protected: str, risk_flags: str) -> list[str]:
    return [
        f"{cp} Changed:       {changed}",
        f"{cp} Protected:     {protected}",
        f"{cp} Meaning-Check: NEEDS-LLM",
        f"{cp} Risk-Flags:    {risk_flags}",
    ]


def _count_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def _count_clauses(text: str) -> int:
    lowered = text.lower()
    marker_hits = sum(1 for marker in CLAUSE_MARKERS if re.search(rf"\b{marker}\b", lowered))
    comma_parts = max(0, text.count(","))
    return marker_hits + comma_parts


def _simplify_sentence(text: str) -> str:
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if len(parts) <= 1:
        return text
    head = parts[0]
    tail = ". ".join(parts[1:])
    return f"{head}. {tail}."


def _iter_paragraphs(parser, lines: list[str], start: int, end: int) -> list[tuple[int, str]]:
    """Group consecutive visible lines into paragraphs (start_line, joined_text).

    Real LaTeX hard-wraps prose at ~80 columns, so a single sentence routinely
    spans several source lines. Joining each paragraph before sentence-splitting
    lets cross-line long sentences be detected (E13).
    """
    paragraphs: list[tuple[int, str]] = []
    buffer: list[str] = []
    buffer_start = 0
    prefix = parser.get_comment_prefix()
    for line_no in range(start, min(end, len(lines)) + 1):
        raw = lines[line_no - 1].strip()
        if not raw or raw.startswith(prefix):
            if buffer:
                paragraphs.append((buffer_start, " ".join(buffer)))
                buffer = []
            continue
        visible = parser.extract_visible_text(raw)
        if not visible:
            if buffer:
                paragraphs.append((buffer_start, " ".join(buffer)))
                buffer = []
            continue
        if not buffer:
            buffer_start = line_no
        buffer.append(visible)
    if buffer:
        paragraphs.append((buffer_start, " ".join(buffer)))
    return paragraphs


def analyze(
    file_path: Path,
    section: str | None,
    max_words: int,
    max_clauses: int,
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
                f"{cp} LONG SENTENCE [Severity: Info] [Priority: P3] [Script]: "
                f"This module has no {goal} rules; run the "
                f"`{UNSUPPORTED_GOALS[goal]}` module instead."
            ]
        )

    # Splitting a sentence is a structural edit, which a `minimal` envelope does
    # not authorize. The proposal is still shown — suppressing it would hide the
    # finding — but it is labelled so nobody applies it outside its envelope.
    envelope_note = (
        " Applying the split needs --strength moderate or higher." if strength == "minimal" else ""
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

    output: list[str] = []
    for start, end in ranges:
        for line_no, paragraph in _iter_paragraphs(parser, lines, start, end):
            for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
                sent = sentence.strip()
                if not sent:
                    continue
                words = _count_words(sent)
                clauses = _count_clauses(sent)
                if words <= max_words and clauses <= max_clauses:
                    continue

                simplified = _simplify_sentence(sent)
                location = doc.lineref(line_no) if doc is not None else f"Line {line_no}"
                output.extend(
                    [
                        f"{cp} LONG SENTENCE ({location}, {words} words, {clauses} clauses) "
                        "[Severity: Minor] [Priority: P2] [Script]",
                        f"{cp} Original: {sent}",
                        f"{cp} Suggested: {simplified}",
                        f"{cp} Rationale: Sentence exceeds complexity threshold, "
                        f"split for readability.{envelope_note}",
                        *_contract_lines(
                            cp,
                            "none (split proposal only; source not rewritten)",
                            "none",
                            "not-assessed",
                        ),
                        "",
                    ]
                )
    if not output:
        output.append(f"{cp} LONG SENTENCE: No sentences exceeded configured thresholds.")
    return warning_lines + header + output


def main() -> int:
    cli = argparse.ArgumentParser(description="Long sentence analysis for LaTeX/Typst files (MVP)")
    cli.add_argument("file", type=Path, help="Target .tex/.typ file")
    cli.add_argument("--section", help="Section name to analyze")
    cli.add_argument("--max-words", type=int, default=50, help="Max words per sentence")
    cli.add_argument("--max-clauses", type=int, default=3, help="Max clauses per sentence")
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

    print(
        "\n".join(
            analyze(
                args.file,
                args.section,
                args.max_words,
                args.max_clauses,
                args.goal,
                args.strength,
            )
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
