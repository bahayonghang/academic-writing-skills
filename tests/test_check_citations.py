"""Tests for check_citations.py — citation stacking detection."""

import subprocess
import sys
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "academic-writing-skills"
    / "paper-audit"
    / "scripts"
    / "check_citations.py"
)


def _run(
    tmp_path: Path, content: str, suffix: str = ".tex", extra_args: list[str] | None = None
) -> subprocess.CompletedProcess:
    f = tmp_path / f"test{suffix}"
    f.write_text(content, encoding="utf-8")
    cmd = [sys.executable, "-B", str(SCRIPT), str(f)]
    if extra_args:
        cmd.extend(extra_args)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(SCRIPT.parent),
    )


# --- LaTeX Tests ---


def test_latex_no_stacking(tmp_path: Path) -> None:
    """2 citations in one sentence — should pass."""
    tex = r"""
\section{Introduction}
Smith et al. \cite{smith2020} proposed X. Jones \cite{jones2021} extended it.
Gradient descent is widely used \cite{a,b}.
"""
    r = _run(tmp_path, tex)
    assert r.returncode == 0
    assert "No citation stacking" in r.stdout


def test_latex_stacking_3(tmp_path: Path) -> None:
    """3 citations in one sentence — Major/P1."""
    tex = r"""
\section{Introduction}
Many methods have been proposed \cite{a,b,c}.
"""
    r = _run(tmp_path, tex)
    assert r.returncode == 1
    assert "[Severity: Major]" in r.stdout
    assert "3 citations" in r.stdout


def test_latex_stacking_5(tmp_path: Path) -> None:
    """5 citations — Critical/P0."""
    tex = r"""
\section{Related Work}
Recent advances include \cite{a}, \cite{b}, \cite{c}, \cite{d}, \cite{e}.
"""
    r = _run(tmp_path, tex)
    assert r.returncode == 1
    assert "[Severity: Critical]" in r.stdout


def test_latex_outside_target_section(tmp_path: Path) -> None:
    """Citations in Methods — should be ignored."""
    tex = r"""
\section{Introduction}
Smith \cite{smith2020} proposed X.
\section{Methods}
We follow \cite{a,b,c,d,e} for preprocessing.
"""
    r = _run(tmp_path, tex)
    assert r.returncode == 0


def test_latex_cite_comma_expansion(tmp_path: Path) -> None:
    r"""Single \cite{a,b,c} counts as 3."""
    tex = r"""
\section{Introduction}
This has been studied \cite{a,b,c}.
"""
    r = _run(tmp_path, tex)
    assert r.returncode == 1
    assert "3 citations" in r.stdout


# --- Typst Tests ---


def test_typst_no_stacking(tmp_path: Path) -> None:
    """2 Typst citations — should pass."""
    typ = """
= Introduction
@smith2020 proposed X. @jones2021 extended it.
"""
    r = _run(tmp_path, typ, suffix=".typ")
    assert r.returncode == 0


def test_typst_stacking(tmp_path: Path) -> None:
    """4 Typst citations in one line — Major/P1."""
    typ = """
= Related Work
Many methods exist @a2020 @b2021 @c2022 @d2023.
"""
    r = _run(tmp_path, typ, suffix=".typ")
    assert r.returncode == 1
    assert "[Severity: Major]" in r.stdout
    assert "4 citations" in r.stdout


# --- Chinese Section Names ---


def test_chinese_section_names(tmp_path: Path) -> None:
    """Chinese content under recognized section name should be detected.

    Note: paper-audit's parser (LatexParser from latex-paper-en) recognizes
    'Introduction' but not Chinese section names like '绪论' directly.
    In real audit flow, Chinese docs use latex-thesis-zh's parser which maps
    '\\section{绪论}' -> 'introduction'. Here we test with the English name.
    """
    tex = r"""
\section{Introduction}
许多学者对此进行了研究 \cite{a,b,c,d}.
"""
    r = _run(tmp_path, tex)
    assert r.returncode == 1


# --- JSON Output ---


def test_json_output(tmp_path: Path) -> None:
    """--json flag produces valid JSON."""
    import json

    tex = r"""
\section{Introduction}
Many methods \cite{a,b,c}.
"""
    r = _run(tmp_path, tex, extra_args=["--json"])
    data = json.loads(r.stdout)
    assert len(data) == 1
    assert data[0]["citation_count"] == 3


# --- Comment Lines ---


def test_latex_comment_skipped(tmp_path: Path) -> None:
    """Commented lines should be ignored."""
    tex = r"""
\section{Introduction}
% Many methods \cite{a,b,c,d,e}.
Real content \cite{x}.
"""
    r = _run(tmp_path, tex)
    assert r.returncode == 0
