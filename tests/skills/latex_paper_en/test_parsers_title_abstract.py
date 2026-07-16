"""Regression tests for canonical parsers.py fixes (A-EN-4 / A-EN-10).

- R4: ``LatexParser.split_sections`` did not register a ``\\begin{abstract}``
  environment (only the ``\\section*{Abstract}`` heading form), so
  ``--section abstract`` was unreachable for the common IEEE/ACM environment
  style.
- R10: ``extract_title`` used a non-greedy ``\\{(.+?)\\}`` that truncated
  titles containing nested braces and leaked ``\\thanks``/``\\footnote``
  funding text into the title. Fixed with a balanced-brace extractor plus a
  new shared ``_strip_balanced_commands`` helper (ported from the
  cover-letter fork this task supersedes).
"""

from __future__ import annotations

import importlib

parsers = importlib.import_module("parsers")
LatexParser = parsers.LatexParser
extract_title = parsers.extract_title


# ── R4: \begin{abstract} environment registration ─────────────────────────


class TestAbstractEnvironmentRegistration:
    def test_environment_only_abstract_registers_correct_range(self) -> None:
        content = "\n".join(
            [
                r"\documentclass{IEEEtran}",
                r"\begin{document}",
                r"\begin{abstract}",
                "We study forecasting methods and report results.",
                r"\end{abstract}",
                r"\section{Introduction}",
                "Intro body.",
            ]
        )
        sections = LatexParser().split_sections(content)
        assert "abstract" in sections
        assert sections["abstract"] == (3, 5)

    def test_existing_heading_abstract_is_not_duplicated(self) -> None:
        content = "\n".join(
            [
                r"\section*{Abstract}",
                "We study forecasting methods.",
                r"\section{Introduction}",
                "Intro body.",
            ]
        )
        sections = LatexParser().split_sections(content)
        assert sections["abstract"] == (1, 2)
        assert "abstract_2" not in sections

    def test_commented_out_abstract_environment_not_registered(self) -> None:
        content = "\n".join(
            [
                r"\documentclass{IEEEtran}",
                r"% \begin{abstract}",
                "Stale draft text.",
                r"% \end{abstract}",
                r"\section{Introduction}",
                "Intro body.",
            ]
        )
        sections = LatexParser().split_sections(content)
        assert "abstract" not in sections

    def test_same_line_begin_and_end_registers_single_line_range(self) -> None:
        content = "\n".join(
            [
                r"\documentclass{IEEEtran}",
                r"\begin{abstract}Short abstract text.\end{abstract}",
                r"\section{Introduction}",
                "Intro body.",
            ]
        )
        sections = LatexParser().split_sections(content)
        assert sections["abstract"] == (2, 2)

    def test_deai_check_section_abstract_hits_environment_form(self, tmp_path) -> None:
        import subprocess
        import sys

        from tests.support.paths import SCRIPT_DIR_EN

        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\documentclass{IEEEtran}\n"
            "\\begin{document}\n"
            "\\begin{abstract}\n"
            "This paper presents a significant and comprehensive method.\n"
            "\\end{abstract}\n"
            "\\section{Introduction}\n"
            "Intro body.\n"
            "\\end{document}\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPT_DIR_EN / "deai_check.py"),
                str(tex),
                "--section",
                "abstract",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        assert result.returncode == 0
        assert "Section not found" not in result.stderr
        assert "Section: abstract" in result.stdout


# ── R10: extract_title balanced braces + \thanks/\footnote stripping ──────


class TestExtractTitleBalancedBraces:
    def test_nested_braces_title_extracted_in_full(self) -> None:
        content = r"\title{Learning {Fast} and {Slow} Dynamics}"
        assert extract_title(content) == "Learning Fast and Slow Dynamics"

    def test_thanks_with_nested_braces_is_stripped(self) -> None:
        content = r"\title{FastNet\thanks{Funded by \emph{NSF}.}}"
        title = extract_title(content)
        assert title == "FastNet"
        assert "Funded" not in title
        assert "NSF" not in title

    def test_footnote_with_nested_braces_is_stripped(self) -> None:
        content = r"\title{FastNet\footnote{See \url{https://example.com} for code.}}"
        title = extract_title(content)
        assert title == "FastNet"
        assert "example.com" not in title

    def test_whitespace_between_title_command_and_brace_is_tolerated(self) -> None:
        assert extract_title(r"\title {FastNet}") == "FastNet"

    def test_optional_short_title_argument_is_tolerated(self) -> None:
        assert extract_title(r"\title[Short]{FastNet}") == "FastNet"

    def test_no_title_command_falls_through_to_typst_branch(self) -> None:
        content = '#set document(title: "Typst Paper Title")'
        assert extract_title(content) == "Typst Paper Title"
