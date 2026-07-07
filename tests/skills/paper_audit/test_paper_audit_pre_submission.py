"""Tests for paper-audit pre-submission mechanical checks."""

from pathlib import Path

import pytest


def _write_tex(path: Path, body: str) -> Path:
    path.write_text(body.strip() + "\n", encoding="utf-8")
    return path


def test_presubmission_detects_em_dash_and_ai_tone(tmp_path: Path) -> None:
    from pre_submission_check import run_checks

    tex = _write_tex(
        tmp_path / "paper.tex",
        r"""
\documentclass{article}
\begin{document}
\begin{abstract}
Modern systems face a difficult challenge. This paper proposes an innovative method that
improves accuracy by 12.5 percent. The innovative approach uses a compact model, and the
innovative result demonstrates practical value.
\end{abstract}
\section{Introduction}
This contribution is clear—yet it needs final polishing.
\end{document}
""",
    )

    issues = run_checks(tex)
    messages = [issue.message for issue in issues]

    assert any(issue.code == "G1" and issue.severity == "Major" for issue in issues)
    assert any("AI-tone" in message for message in messages)


def test_presubmission_detects_latex_hygiene(tmp_path: Path) -> None:
    from pre_submission_check import run_checks

    tex = _write_tex(
        tmp_path / "paper.tex",
        r"""
\documentclass{article}
\begin{document}
\begin{abstract}
Learning systems face a practical challenge. This paper proposes a method that improves
accuracy by 9.1 percent and demonstrates reliable deployment value.
\end{abstract}
\section{Method}
ResNet \cite{he2016} is the backbone.
\begin{figure}
\caption{Results}
\label{fig-bad label}
\end{figure}
\begin{equation}
\label{eq-bad}
x = y + z
\end{equation}
\end{document}
""",
    )

    issues = run_checks(tex)
    messages = "\n".join(issue.message for issue in issues)

    assert "non-breaking tie" in messages
    assert "contains spaces" in messages
    assert "uses hyphens" in messages
    assert "never referenced" in messages


def test_presubmission_detects_abstract_missing_results(tmp_path: Path) -> None:
    from pre_submission_check import run_checks

    tex = _write_tex(
        tmp_path / "paper.tex",
        r"""
\documentclass{article}
\begin{document}
\begin{abstract}
Scientific workflows face a practical challenge. This paper proposes a method and describes
the model design. The discussion highlights implications for deployment.
\end{abstract}
\section{Introduction}
The main text is short.
\end{document}
""",
    )

    issues = run_checks(tex)

    assert any(
        issue.code == "A1" and issue.severity == "Major" and "results" in issue.message
        for issue in issues
    )


def test_presubmission_pdf_skips_source_limited_checks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import pre_submission_check

    class FakePdfParser:
        def extract_text_from_file(self, _path: str) -> str:
            return (
                "Abstract\n"
                "Learning systems face a challenge. This paper proposes a method that improves "
                "accuracy by 8.0 percent and demonstrates value.\n"
                "Introduction\n"
                r"Raw source-like text \label{fig-bad label} and ResNet \cite{he2016}."
            )

    monkeypatch.setattr(
        pre_submission_check,
        "get_parser",
        lambda *_args, **_kwargs: FakePdfParser(),
    )
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"%PDF-1.7\n")

    issues = pre_submission_check.run_checks(pdf)
    messages = "\n".join(issue.message for issue in issues)

    assert "label" not in messages.lower()
    assert "non-breaking tie" not in messages


def test_presubmission_cli_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    from pre_submission_check import main

    tex = _write_tex(
        tmp_path / "paper.tex",
        r"""
\documentclass{article}
\begin{document}
\begin{abstract}
Learning systems face a challenge. This paper proposes a method that improves accuracy
by 7.0 percent and demonstrates value.
\end{abstract}
\section{Introduction}
This is clean enough for a JSON smoke test.
\end{document}
""",
    )

    assert main([str(tex), "--json"]) == 0
    out = capsys.readouterr().out
    assert out.strip().startswith("[")
