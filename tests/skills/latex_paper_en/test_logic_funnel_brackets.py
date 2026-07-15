"""Regression test for the introduction-funnel bracket false-positive (A-EN-8).

``analyze_logic.py``'s ``_check_introduction_funnel`` used a bare ``"[" in
visible`` check to decide whether the introduction cites prior work. Any
bracket — including a non-citation one like a variable name ``[k]`` or a
math interval — falsely counted as "prior work referenced", suppressing the
"introduction does not derive the problem from prior-work limitations"
finding. Fixed by requiring a digit-only citation-list shape
(``NUMERIC_CITE_RE``): ``[12]``, ``[3, 7]``, ``[1-4]`` still count; a
non-digit bracket like ``[k]`` no longer does.

Note (flagged for the parent task): the literal ``NUMERIC_CITE_RE`` pattern
specified in design.md (``r"\\[\\d+(?:\\s*[,-–]\\s*\\d+)*\\]"``) matches
``[0, 1]`` and ``[3, 7]`` identically (both are "digit, comma, digit"), so it
cannot actually distinguish a math interval like ``[0, 1]`` from a two-entry
citation list as prd.md's AC literally claims. This test exercises the
mechanically achievable distinction (digit-only bracket vs. a bracket
containing a non-digit token) rather than the internally-inconsistent
``[0, 1]`` vs. ``[3, 7]`` example.
"""

from __future__ import annotations

import importlib

logic_module = importlib.import_module("analyze_logic")

_FUNNEL_PREAMBLE = (
    r"\documentclass{article}"
    "\n"
    r"\begin{document}"
    "\n"
    r"\section{Introduction}"
    "\n"
    "This capability is increasingly important for real-world deployment.\n"
    "This remains a significant challenge because deployed systems cannot scale.\n"
)
_FUNNEL_FOOTER = "We propose a new adaptive method to address this.\n" r"\end{document}" "\n"


def _funnel_findings(tmp_path, bracket_line: str) -> str:
    tex = tmp_path / "main.tex"
    tex.write_text(_FUNNEL_PREAMBLE + bracket_line + "\n" + _FUNNEL_FOOTER, encoding="utf-8")
    return "\n".join(logic_module.analyze(tex)).lower()


def test_non_digit_bracket_does_not_count_as_prior_work(tmp_path) -> None:
    """A non-citation bracket like [k] no longer suppresses the finding."""
    joined = _funnel_findings(tmp_path, "We can bound the error within [k] iterations.")
    assert "does not derive it from prior work" in joined


def test_numeric_single_citation_bracket_still_counts_as_prior_work(tmp_path) -> None:
    """[12] (a genuine numeric citation shape) still suppresses the finding."""
    joined = _funnel_findings(
        tmp_path, "Numeric analyses reported bounds within [12] iterations empirically."
    )
    assert "does not derive it from prior work" not in joined


def test_numeric_list_citation_bracket_still_counts_as_prior_work(tmp_path) -> None:
    """[3, 7] (a comma-separated numeric citation list) still counts."""
    joined = _funnel_findings(
        tmp_path, "Numeric analyses reported bounds within [3, 7] iterations empirically."
    )
    assert "does not derive it from prior work" not in joined


def test_cite_command_still_counts_as_prior_work(tmp_path) -> None:
    """The pre-existing \\cite{ raw-line check keeps working unchanged."""
    joined = _funnel_findings(tmp_path, r"Numeric analyses \cite{smith2020} reported bounds.")
    assert "does not derive it from prior work" not in joined
