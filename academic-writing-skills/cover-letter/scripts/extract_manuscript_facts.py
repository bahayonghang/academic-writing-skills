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
    _extract_balanced_block,
    _strip_latex_markup,
    extract_abstract,
    extract_latex_citation_keys,
)
from tex_loader import assemble

# Author command prefixes across common LaTeX templates. We locate the command,
# then balanced-brace-capture its argument so that nested ``\thanks{...}`` (with
# its own braces) does not truncate the author block (the old ``[^}]+`` regex
# stopped at the first ``}`` inside ``\thanks``, dropping every author).
# IEEE: \IEEEauthorblockN{Name} / \IEEEauthorblockA{Affil}
# ACM acmart: \author{Name} ... \affiliation{...} ...
# NeurIPS: \author{Name1\thanks{...} \\ Affil}
# Article: \author{Name1 \and Name2}
AUTHOR_COMMAND_PREFIXES: tuple[str, ...] = (
    r"\\IEEEauthorblockN",
    r"\\author(?:\[[^\]]*\])?",
    r"\\authorinfo",
)

# Only an explicit corresponding-author command is trusted. The previous
# free-text fallback (``corresponding author: <name>``) reached into
# ``\thanks{Corresponding author: a@u.edu}`` and reported the email local part
# as a fabricated author, so it is intentionally removed; we fall back to the
# first extracted author instead.
CORRESPONDING_AUTHOR_PATTERNS: tuple[str, ...] = (r"\\corresponding(?:author)?\s*\{([^}]+)\}",)

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


def load_manuscript_text(path: str | Path) -> str:
    """Read a manuscript, expanding ``\\input`` / ``\\include`` via tex_loader.

    Real papers often keep ``main.tex`` as an include skeleton; without assembly
    the facts blob comes back empty and align-check mis-reports every supported
    claim. ``assemble`` also applies the robust encoding fallback, so this works
    for single-file manuscripts too.
    """
    return assemble(Path(path)).content


def _clean(text: str) -> str:
    """Light cleanup: strip LaTeX commands but keep references like \\cite intact placeholder."""
    cleaned = re.sub(r"\\textbf\{([^}]*)\}", r"\1", text)
    cleaned = re.sub(r"\\emph\{([^}]*)\}", r"\1", cleaned)
    cleaned = re.sub(r"\\textit\{([^}]*)\}", r"\1", cleaned)
    cleaned = re.sub(r"\\\\", " ", cleaned)
    cleaned = re.sub(r"\\and\b", ",", cleaned)
    cleaned = re.sub(r"\\thanks\{[^}]*\}", "", cleaned)
    cleaned = re.sub(r"\\footnote\{[^}]*\}", "", cleaned)
    cleaned = cleaned.replace("~", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def _strip_balanced_commands(text: str, commands: tuple[str, ...]) -> str:
    """Remove ``\\<command>{...}`` spans with balanced-brace bodies.

    Unlike a ``\\thanks\\{[^}]*\\}`` regex, this also removes footnote/thanks
    blocks whose body contains nested braces (e.g. ``\\thanks{\\emph{x}}``),
    which would otherwise leak affiliation or funding text into the author /
    title fields.
    """
    for command in commands:
        opener = re.compile(r"\\" + command + r"\s*\{")
        while True:
            match = opener.search(text)
            if not match:
                break
            brace_idx = match.end() - 1
            body = _extract_balanced_block(text, brace_idx, "{", "}")
            end = brace_idx + len(body) + 2  # skip the opening '{' and closing '}'
            text = text[: match.start()] + " " + text[end:]
    return text


def _balanced_author_blocks(content: str) -> list[str]:
    """Return the balanced-brace argument of each author command in the source."""
    blocks: list[str] = []
    for prefix in AUTHOR_COMMAND_PREFIXES:
        for match in re.finditer(prefix + r"\s*\{", content):
            brace_idx = match.end() - 1
            block = _extract_balanced_block(content, brace_idx, "{", "}")
            if block:
                blocks.append(block)
    return blocks


def extract_authors(content: str) -> list[str]:
    """Extract author names from a LaTeX manuscript.

    Author blocks are captured with balanced braces, ``\\thanks`` / ``\\footnote``
    are stripped first, then each ``\\and``-separated group contributes the text
    before its first ``\\\\`` line break (the name line; affiliations follow on
    later lines). ``\\IEEEauthorblockN`` lists several comma-separated names on
    one line.
    """
    candidates: list[str] = []
    for block in _balanced_author_blocks(content):
        # IEEE wraps the names in \IEEEauthorblockN sub-blocks (captured by their
        # own prefix); skip the outer \author{...} wrapper so its \IEEEauthorblockA
        # affiliation does not leak in as a fake author.
        if r"\IEEEauthorblockN" in block:
            continue
        block = re.sub(r"(?<!\\)%.*", "", block)  # drop line comments (e.g. \author{%)
        stripped = _strip_balanced_commands(block, ("thanks", "footnote"))
        for group in re.split(r"\\[aA]nd\b", stripped):
            name_line = re.split(r"\\\\", group)[0]
            for raw in re.split(r",", name_line):
                name = _clean(raw)
                if not name or "\\" in name or "{" in name or "}" in name:
                    continue
                if len(name.split()) >= 2 and name not in candidates:
                    candidates.append(name)
    return candidates


def extract_corresponding_author(content: str, authors: list[str]) -> str:
    """Corresponding author from an explicit command; falls back to first author.

    No free-text fallback: scraping ``corresponding author: ...`` reached into
    ``\\thanks`` blocks and reported email local parts as fabricated authors.
    """
    for pattern in CORRESPONDING_AUTHOR_PATTERNS:
        match = re.search(pattern, content, flags=re.IGNORECASE)
        if match:
            name = _clean(match.group(1))
            if name and "@" not in name:
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


def _extract_title_local(content: str) -> str:
    """Extract the LaTeX title with balanced braces, stripping ``\\thanks``.

    ``parsers.extract_title`` still uses a non-greedy ``\\{(.+?)\\}`` that
    truncates nested-brace titles and leaks ``\\thanks`` funding statements into
    the letter opening. The cover-letter facts blob needs an accurate, clean
    title, so it is captured locally (parsers.py is owned by the en-family
    foundation task and is out of scope here).
    """
    match = re.search(r"\\title(?:\[[^\]]*\])?\s*\{", content)
    if not match:
        return ""
    body = _extract_balanced_block(content, match.end() - 1, "{", "}")
    if not body:
        return ""
    body = _strip_balanced_commands(body, ("thanks", "footnote"))
    return _strip_latex_markup(body)


def extract_facts(content: str) -> dict:
    """Build the manuscript facts blob."""
    title = _extract_title_local(content)
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
    parser.add_argument("--output", "-o", help="Optional output JSON path")
    args = parser.parse_args(argv)

    path = Path(args.tex_file).resolve()
    if not path.exists():
        print(f"File not found: {args.tex_file}", file=sys.stderr)
        return 2
    if path.suffix.lower() != ".tex":
        print(f"Unsupported format: {path.suffix}; expected .tex", file=sys.stderr)
        return 2

    content = load_manuscript_text(path)
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
