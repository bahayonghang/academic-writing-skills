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


def test_extract_latex_citation_keys_with_optional_args() -> None:
    content = r"""
As shown in \cite{key1,key2}, prior work exists.
Extended by \citep[Sec. 2]{key3}.
\nocite{key4}
"""
    assert extract_latex_citation_keys(content) == {"key1", "key2", "key3", "key4"}
