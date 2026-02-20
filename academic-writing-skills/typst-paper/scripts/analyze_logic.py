#!/usr/bin/env python3
"""
Logic and methodology analyzer (MVP) for LaTeX/Typst papers.
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


def analyze(file_path: Path, section: str | None = None) -> list[str]:
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

    if not out:
        out.append("% LOGIC/METHODOLOGY: No rule-based coherence issues detected.")
    return out


def main() -> int:
    cli = argparse.ArgumentParser(
        description="Logic and methodology analysis for LaTeX/Typst files"
    )
    cli.add_argument("file", type=Path, help="Target .tex/.typ file")
    cli.add_argument("--section", help="Section name to analyze")
    args = cli.parse_args()

    if not args.file.exists():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        return 1

    print("\n".join(analyze(args.file, args.section)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
