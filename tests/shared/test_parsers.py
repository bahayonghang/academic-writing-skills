"""Tests for parser helpers used by latex-paper-en scripts."""

import pytest
from parsers import (
    LatexParser,
    TypstParser,
    extract_abstract,
    extract_latex_citation_keys,
    extract_title,
)


@pytest.fixture
def latex_parser() -> LatexParser:
    return LatexParser()


@pytest.fixture
def typst_parser() -> TypstParser:
    return TypstParser()


def test_latex_split_sections(latex_parser: LatexParser) -> None:
    content = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
Intro text.
\section{Related Work}
Related text.
\section{Method}
Method text.
\end{document}
"""
    sections = latex_parser.split_sections(content)
    assert "introduction" in sections
    assert "related" in sections
    assert "method" in sections


def test_latex_extract_visible_text_strips_math_and_commands(latex_parser: LatexParser) -> None:
    line = r"This is \textbf{bold} and \cite{ref1} citation."
    visible = latex_parser.extract_visible_text(line)
    assert "citation" in visible

    math_line = r"Result $x=1$ and \includegraphics[width=0.5\\textwidth]{fig1}"
    math_visible = latex_parser.extract_visible_text(math_line)
    assert "Result" in math_visible
    assert "x=1" not in math_visible
    assert "includegraphics" not in math_visible


def test_latex_clean_text(latex_parser: LatexParser) -> None:
    content = r"Hello \textbf{World}. $x=1$. "
    assert latex_parser.clean_text(content) == "Hello World."


def test_typst_split_sections(typst_parser: TypstParser) -> None:
    content = """
= Introduction
Intro text.
= Related Work
Related text.
"""
    sections = typst_parser.split_sections(content)
    assert "introduction" in sections
    assert "related" in sections


def test_typst_clean_text(typst_parser: TypstParser) -> None:
    content = "Hello *World*. $x=1$. // Comment"
    assert typst_parser.clean_text(content) == "Hello *World*."


def test_typst_clean_text_block_comment(typst_parser: TypstParser) -> None:
    content = "Hello /* hidden */ World."
    assert typst_parser.clean_text(content) == "Hello World."


# ── TypstParser URL-aware line-comment stripping (A-TY-1) ─────────


@pytest.mark.parametrize(
    "line",
    [
        "See https://example.com/x for details.",
        "See http://example.com for details.",
    ],
)
def test_typst_extract_visible_text_keeps_inline_url_and_prose(
    typst_parser: TypstParser, line: str
) -> None:
    visible = typst_parser.extract_visible_text(line)
    assert "example.com" in visible
    assert "details" in visible


def test_typst_extract_visible_text_keeps_url_with_double_slash_path(
    typst_parser: TypstParser,
) -> None:
    """Single-ownership lock: a URL token swallows its own ``//`` path segment,
    so the whole line (URL + trailing prose) stays visible."""
    line = "https://example.com//path more prose"
    assert typst_parser.extract_visible_text(line) == line


def test_typst_extract_visible_text_link_call_hides_but_prose_visible(
    typst_parser: TypstParser,
) -> None:
    line = '#link("https://example.com") hosts the code.'
    visible = typst_parser.extract_visible_text(line)
    assert "hosts the code." in visible
    assert "https://example.com" not in visible


def test_typst_extract_visible_text_link_call_with_protocol_relative_url(
    typst_parser: TypstParser,
) -> None:
    line = '#link("//cdn.example.com/l.js") text'
    assert typst_parser.extract_visible_text(line) == "text"


def test_typst_extract_visible_text_whole_line_comment_is_empty(
    typst_parser: TypstParser,
) -> None:
    assert typst_parser.extract_visible_text("// pure comment") == ""


def test_typst_extract_visible_text_trailing_comment_stripped(
    typst_parser: TypstParser,
) -> None:
    assert typst_parser.extract_visible_text("Prose here. // trailing") == "Prose here."


def test_typst_extract_visible_text_colon_space_slash_not_a_url(
    typst_parser: TypstParser,
) -> None:
    assert typst_parser.extract_visible_text("a: // comment") == "a:"


def test_typst_extract_visible_text_bare_protocol_relative_is_comment(
    typst_parser: TypstParser,
) -> None:
    """Decision lock: a bare ``//host`` (no quotes) is Typst comment syntax
    (the compiler only auto-links ``http(s)://``), so it must vanish."""
    assert typst_parser.extract_visible_text("//cdn.example.com") == ""


def test_typst_extract_visible_text_raw_backtick_slashes_preserved(
    typst_parser: TypstParser,
) -> None:
    line = "`code // x` prose"
    assert typst_parser.extract_visible_text(line) == line


def test_typst_extract_visible_text_block_comment_and_line_comment_same_line(
    typst_parser: TypstParser,
) -> None:
    line = "/* hidden */ prose // note"
    assert typst_parser.extract_visible_text(line) == "prose"


def test_typst_clean_text_preserves_url_and_strips_comment_lines(
    typst_parser: TypstParser,
) -> None:
    content = (
        "See https://example.com/x for details.\n"
        "// this whole line is a comment\n"
        "Trailing prose after comment. // note\n"
    )
    cleaned = typst_parser.clean_text(content)
    assert cleaned == "See https://example.com/x for details.\nTrailing prose after comment."


def test_extract_title_and_abstract_for_latex() -> None:
    content = r"""
\documentclass{article}
\title{Transformer for Time Series Forecasting}
\begin{document}
\maketitle
\begin{abstract}
This paper proposes a robust forecasting pipeline.
\end{abstract}
\end{document}
"""
    assert extract_title(content) == "Transformer for Time Series Forecasting"
    assert extract_abstract(content) == "This paper proposes a robust forecasting pipeline."


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            '#set document(title: "Typst Paper Title")',
            "Typst Paper Title",
        ),
        (
            "#set document(title: [Typst #emph[Paper] Title])",
            "Typst Paper Title",
        ),
    ],
)
def test_extract_title_for_typst(content: str, expected: str) -> None:
    assert extract_title(content) == expected


def test_extract_abstract_from_section_block() -> None:
    content = r"""
\section*{Abstract}
We evaluate robustness under noise.
\section{Introduction}
"""
    assert extract_abstract(content) == "We evaluate robustness under noise."


def test_extract_abstract_for_typst_with_markup() -> None:
    content = "#abstract[We present #emph[a robust] pipeline.]"
    assert extract_abstract(content) == "We present a robust pipeline."


def test_extract_abstract_typst_heading_stops_at_any_level_heading() -> None:
    """A-TY-2: a sub-heading like ``== Keywords`` must terminate capture too,
    not just a level-1 heading."""
    content = "= Abstract\nWe present a method.\n== Keywords\nforecasting, transformers\n"
    result = extract_abstract(content)
    assert result == "We present a method."
    assert "Keywords" not in result


def test_extract_abstract_typst_heading_level1_still_stops_capture() -> None:
    content = "= Abstract\nWe present a method.\n= Introduction\nIntro text.\n"
    assert extract_abstract(content) == "We present a method."


def test_extract_latex_citation_keys_with_optional_args() -> None:
    content = r"""
As shown in \cite{key1,key2}, prior work exists.
Extended by \citep[Sec. 2]{key3}.
\nocite{key4}
"""
    assert extract_latex_citation_keys(content) == {"key1", "key2", "key3", "key4"}
