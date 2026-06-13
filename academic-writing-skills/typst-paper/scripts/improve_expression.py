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
    from tex_loader import read_text_robust
except ImportError:
    try:
        from typ_loader import read_text_robust
    except ImportError:
        read_text_robust = None


# Note: use->employ and show->demonstrate were removed because the deai guide
# lists "we use ..." as correct and "demonstrate the effectiveness" as an AI
# tell — blindly applying them fought the de-AI module's own advice (E15).
WEAK_VERBS = {
    r"\bget\b": "obtain",
    r"\bmake\b": "develop",
}

WEAK_PHRASES = {
    r"\bvery\b": "highly",
    r"\ba lot of\b": "many",
    r"\bkind of\b": "",
}


def _enhance(text: str) -> tuple[str, list[str]]:
    revised = text
    changes: list[str] = []
    for pattern, replacement in WEAK_VERBS.items():
        if re.search(pattern, revised, re.IGNORECASE):
            revised = re.sub(pattern, replacement, revised, flags=re.IGNORECASE)
            changes.append(f"Weak verb replaced: {pattern} -> {replacement}")
    for pattern, replacement in WEAK_PHRASES.items():
        if re.search(pattern, revised, re.IGNORECASE):
            revised = re.sub(pattern, replacement, revised, flags=re.IGNORECASE)
            changes.append(f"Weak phrase adjusted: {pattern} -> {replacement or '[deleted]'}")
    revised = re.sub(r"\s+", " ", revised).strip()
    return revised, changes


def analyze(file_path: Path, section: str | None) -> list[str]:
    parser = get_parser(file_path)
    if read_text_robust is not None:
        content, _warning = read_text_robust(file_path)
    else:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = content.split("\n")
    sections = parser.split_sections(content)
    cp = parser.get_comment_prefix()

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
            revised, changes = _enhance(visible)
            if revised.lower() == visible.lower() or not changes:
                continue
            out.extend(
                [
                    f"{cp} EXPRESSION (Line {line_no}) [Severity: Minor] [Priority: P2]: "
                    f"Improve academic tone",
                    f"{cp} Original: {visible}",
                    f"{cp} Revised:  {revised}",
                    f"{cp} Rationale: {'; '.join(changes)}",
                    "",
                ]
            )
    if not out:
        out.append(f"{cp} EXPRESSION: No weak-expression patterns detected.")
    return out


def main() -> int:
    cli = argparse.ArgumentParser(
        description="Academic expression improvement for LaTeX/Typst files"
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
