"""Extract structured facts from a LaTeX manuscript for cover-letter generation.

Emits a JSON facts blob consumed by ``generate`` mode (via SKILL.md guidance to
Claude) and by ``align_check.py`` (as the manuscript anchor set).

The extractor is deterministic: regex-based, no LLM calls. Best-effort across
common LaTeX templates (article, IEEEtran, ACM acmart, NeurIPS neurips,
Springer LNCS llncs).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from parsers import (
    LatexParser,
    extract_abstract,
    extract_latex_citation_keys,
    extract_title,
)

# Author commands across common LaTeX templates.
# IEEE: \IEEEauthorblockN{Name} / \IEEEauthorblockA{Affil}
# ACM acmart: \author{Name} ... \affiliation{...} ...
# NeurIPS: \author{Name1\thanks{...} \\ Affil}
# Article: \author{Name1 \and Name2}
AUTHOR_COMMAND_PATTERNS: tuple[str, ...] = (
    r"\\IEEEauthorblockN\s*\{([^}]+)\}",
    r"\\author(?:\[[^\]]*\])?\s*\{([^}]+)\}",
    r"\\authorinfo\s*\{([^}]+)\}",
)

CORRESPONDING_AUTHOR_PATTERNS: tuple[str, ...] = (
    r"\\corresponding(?:author)?\s*\{([^}]+)\}",
    r"corresponding author[:\s]*([A-Z][A-Za-z'\.\- ]+)",
)

CONTRIBUTIONS_HEADER_PATTERNS: tuple[str, ...] = (
    r"\\(?:sub)?section\*?\{(?:Our )?Contributions?\}",
    r"\\(?:sub)?section\*?\{Main\s+Contributions?\}",
    r"\\(?:sub)?section\*?\{Summary\s+of\s+Contributions?\}",
    r"\\paragraph\*?\{(?:Our )?Contributions?\}",
)

INLINE_CONTRIBUTIONS_PATTERNS: tuple[str, ...] = (
    r"(?:Our|The)\s+(?:main\s+|primary\s+)?contributions?\s+(?:are|include)\s*[:\.]",
    r"(?:In\s+summary|To\s+summarize),?\s+(?:our|the\s+main)\s+contributions?",
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _clean(text: str) -> str:
    """Light cleanup: strip LaTeX commands but keep references like \\cite intact placeholder."""
    cleaned = re.sub(r"\\textbf\{([^}]*)\}", r"\1", text)
    cleaned = re.sub(r"\\emph\{([^}]*)\}", r"\1", cleaned)
    cleaned = re.sub(r"\\textit\{([^}]*)\}", r"\1", cleaned)
    cleaned = re.sub(r"\\\\", " ", cleaned)
    cleaned = re.sub(r"\\and\b", ",", cleaned)
    cleaned = re.sub(r"\\thanks\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\\footnote\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def extract_authors(content: str) -> list[str]:
    """Extract author names from a LaTeX manuscript."""
    candidates: list[str] = []
    for pattern in AUTHOR_COMMAND_PATTERNS:
        for match in re.finditer(pattern, content):
            raw = _clean(match.group(1))
            parts = re.split(r",|\band\b", raw, flags=re.IGNORECASE)
            for part in parts:
                name = part.strip()
                if not name or "\\" in name or "{" in name or "}" in name:
                    continue
                if name and len(name.split()) >= 2 and name not in candidates:
                    candidates.append(name)
    return candidates


def extract_corresponding_author(content: str, authors: list[str]) -> str:
    """Best-effort corresponding-author detection. Falls back to first author."""
    for pattern in CORRESPONDING_AUTHOR_PATTERNS:
        match = re.search(pattern, content, flags=re.IGNORECASE)
        if match:
            name = _clean(match.group(1))
            if name:
                return name
    return authors[0] if authors else ""


def _extract_itemized(text: str, max_items: int = 5) -> list[str]:
    items: list[str] = []
    # \begin{itemize}\item ...\item ...\end{itemize}
    env = re.search(
        r"\\begin\{(?:itemize|enumerate)\}(.*?)\\end\{(?:itemize|enumerate)\}",
        text,
        flags=re.DOTALL,
    )
    if env:
        for raw in re.findall(r"\\item\s+(.+?)(?=\\item|\\end\{)", env.group(1), flags=re.DOTALL):
            cleaned = _clean(raw)
            if cleaned:
                items.append(cleaned)
            if len(items) >= max_items:
                break
    return items


def extract_contributions(content: str, max_items: int = 5) -> list[str]:
    """Extract contributions list from a LaTeX manuscript.

    Strategy: find a section/paragraph heading that names "Contributions," then
    look for an itemize/enumerate block inside the following ~2000 characters.
    Falls back to inline patterns like ``Our main contributions are: (1) ... (2) ...``.
    """
    items: list[str] = []
    for pattern in CONTRIBUTIONS_HEADER_PATTERNS:
        match = re.search(pattern, content, flags=re.IGNORECASE)
        if not match:
            continue
        window = content[match.end() : match.end() + 2500]
        items.extend(_extract_itemized(window, max_items=max_items))
        if items:
            return items[:max_items]

    # Inline numbered contributions: "Our main contributions are: (1) ...; (2) ...; (3) ..."
    for pattern in INLINE_CONTRIBUTIONS_PATTERNS:
        match = re.search(pattern, content, flags=re.IGNORECASE)
        if not match:
            continue
        window = content[match.end() : match.end() + 1500]
        numbered = re.findall(r"\(\d+\)\s+([^.;]+?[.;])", window)
        for item in numbered:
            cleaned = _clean(item.rstrip(".;"))
            if cleaned and cleaned not in items:
                items.append(cleaned)
            if len(items) >= max_items:
                break
        if items:
            return items[:max_items]

    return items


def extract_section_anchors(content: str) -> dict[str, tuple[int, int]]:
    """Return section names and their line ranges (via LatexParser.split_sections)."""
    parser = LatexParser()
    return parser.split_sections(content)


def extract_facts(content: str) -> dict:
    """Build the manuscript facts blob."""
    title = extract_title(content)
    abstract = extract_abstract(content)
    authors = extract_authors(content)
    corresponding = extract_corresponding_author(content, authors)
    contributions = extract_contributions(content)
    sections = extract_section_anchors(content)
    citations = sorted(extract_latex_citation_keys(content))

    # Headline numeric tokens (for cover-letter quantitative anchor lookup).
    # Accept either bare "47%" or LaTeX-escaped "47\%". No trailing \b because
    # `%` is a non-word character so the boundary would never satisfy.
    number_patterns = (
        r"\b\d+(?:\.\d+)?\s*(?:\\?%|pp|x|×|ms|MB|GB|FLOPs?)",
        r"(?:\$|USD\s*)\s*\d+(?:\.\d+)?\s*(?:[kKmMbB]|million|billion)?\b",
        r"\b\d+(?:\.\d+)?\s+(?:sensor\s+)?modalit(?:y|ies)\b",
    )
    numbers: list[str] = []
    for pattern in number_patterns:
        numbers.extend(re.findall(pattern, content, flags=re.IGNORECASE))
    # Normalize the LaTeX escape so downstream consumers can substring-match.
    unique_numbers = sorted({n.replace("\\", "") for n in numbers})[:20]

    return {
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "corresponding_author": corresponding,
        "contributions": contributions,
        "section_anchors": {
            key: {"start_line": start, "end_line": end} for key, (start, end) in sections.items()
        },
        "citation_keys": citations,
        "headline_numbers": unique_numbers,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract manuscript facts (title, abstract, authors, contributions) from .tex"
    )
    parser.add_argument("tex_file", help=".tex manuscript file")
    parser.add_argument("--json", action="store_true", help="Emit JSON (default behavior)")
    parser.add_argument("--output", "-o", help="Optional output JSON path")
    args = parser.parse_args(argv)

    path = Path(args.tex_file).resolve()
    if not path.exists():
        print(f"File not found: {args.tex_file}", file=sys.stderr)
        return 2
    if path.suffix.lower() != ".tex":
        print(f"Unsupported format: {path.suffix}; expected .tex", file=sys.stderr)
        return 2

    content = _read_text(path)
    facts = extract_facts(content)
    payload = json.dumps(facts, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)

    # Return non-zero when key facts are missing (so calling skill can flag).
    missing_keys = [k for k in ("title", "abstract") if not facts.get(k)]
    return 1 if missing_keys else 0


if __name__ == "__main__":
    raise SystemExit(main())
