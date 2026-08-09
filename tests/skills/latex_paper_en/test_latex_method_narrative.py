"""Method-section narrative checks for the LaTeX paper skill."""

from pathlib import Path

import analyze_logic


def _run(tmp_path: Path, content: str, section: str | None = "methods") -> str:
    tex = tmp_path / "main.tex"
    tex.write_text(content, encoding="utf-8")
    return "\n".join(analyze_logic.analyze(tex, section))


_METHOD_CASE = r"""\documentclass{article}
\begin{document}
\section{Proposed Method}
\subsection{Encoder}
Next, we introduce the encoder module.
\paragraph{Input stage.} This module is used to normalize the samples.
The samples retain their timestamps during normalization.
\paragraph{Fusion stage.}
The component aims to fuse the aligned features.
\paragraph{Output stage.} The stage emits the fused representation.
\begin{equation}
z = f(x)
\end{equation}
The score is computed from the fused representation.
It is normalized across the feature axis.
The result enters the decoder.
\subsection{Decoder}
Because the fused representation remains ambiguous, the decoder resolves it.
\end{document}
"""


_COMPLIANT_METHOD = r"""\documentclass{article}
\begin{document}
\section{Methods}
\subsection{Encoder}
Because the raw samples remain noisy, the encoder first aligns their timestamps.
\paragraph{Input representation.} The upstream samples retain their measured units.
\paragraph{Alignment operator.} A masked projection aligns valid observations.
\paragraph{Output contract.} The encoder emits an aligned feature tensor.
\begin{equation}
z = f(x)
\end{equation}
where $z$ denotes the aligned representation passed to the decoder.
\subsection{Decoder}
Since the aligned tensor still contains ambiguity, the decoder estimates the target.
\end{document}
"""


def test_method_narrative_reports_three_candidates_and_edge_table(tmp_path: Path) -> None:
    report = _run(tmp_path, _METHOD_CASE)

    assert report.count("M-HEADING") == 1
    assert report.count("M-SEQWORD") == 1
    assert report.count("M-EQUATION") == 1
    assert "M-EDGETABLE" in report
    assert "Encoder -> Decoder" in report
    assert report.count("Meaning-Check: NEEDS-LLM") == 3


def test_method_narrative_accepts_closed_method_section(tmp_path: Path) -> None:
    report = _run(tmp_path, _COMPLIANT_METHOD)

    assert "M-HEADING" not in report
    assert "M-SEQWORD" not in report
    assert "M-EQUATION" not in report
    assert "M-EDGETABLE" in report


def test_method_equations_share_one_following_gloss(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        r"""\documentclass{article}
\begin{document}
\section{Methods}
\subsection{Encoder}
Because the input remains noisy, the encoder aligns it.
\begin{equation}
z_1 = f(x)
\end{equation}
\begin{align}
z_2 &= g(z_1)
\end{align}
where $z_1$ is the aligned feature and $z_2$ enters the decoder.
\subsection{Decoder}
Because ambiguity remains, the decoder estimates the target.
\end{document}
""",
    )

    assert "M-EQUATION" not in report


def test_method_narrative_respects_comments_and_protected_tokens(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        r"""\documentclass{article}
\begin{document}
\section{Methods}
\subsection{Boundary handling}
Next, this section introduces the boundary module. % because a constraint remains
\paragraph{Comment heading.} % This module is used to announce a false hit.
The paragraph only states the input boundary.
\paragraph{Real announcement.}
This module is used to normalize the samples.
\paragraph{Protected announcement.}
See \cite{This module is used to}; the prose does not announce a responsibility.
\begin{equation}
x = 1
% \end{equation}
y = 2
\end{equation}
The output object is defined. % where appears only in a comment
See \ref{where}; the reference key is not a symbol gloss.
$where$ appears only inside protected math.
\end{document}
""",
    )

    assert "M-HEADING" not in report
    assert "M-SEQWORD" in report
    assert "M-EQUATION" in report


def test_method_narrative_is_off_without_section_gate(tmp_path: Path) -> None:
    report = _run(tmp_path, _METHOD_CASE, section=None)

    assert "M-HEADING" not in report
    assert "M-SEQWORD" not in report
    assert "M-EQUATION" not in report
    assert "M-EDGETABLE" not in report


def test_related_work_run_in_groups_do_not_enter_method_scope(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        r"""\documentclass{article}
\begin{document}
\section{Methods}
\subsection{Pipeline}
Because the input remains noisy, the pipeline aligns it before prediction.
\section{Related Work}
\textbf{Transformer-based methods.} This group models global interactions.
\textbf{Convolution-based methods.} This group models local patterns.
\textbf{Hybrid methods.} This group combines the two families.
\end{document}
""",
    )

    assert "M-HEADING" not in report
    assert "M-SEQWORD" not in report
    assert "M-EQUATION" not in report


def test_sequence_transitions_have_one_runtime_source() -> None:
    assert analyze_logic.TRANSITIONS["sequence"] == {
        "next",
        "then",
        "subsequently",
        "after that",
        "after this",
    }
