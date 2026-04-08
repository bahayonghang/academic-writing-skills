"""Regression tests for latex-paper-en script behaviors."""

import importlib
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

experiment_module = importlib.import_module("analyze_experiment")
logic_module = importlib.import_module("analyze_logic")
literature_module = importlib.import_module("analyze_literature")
deai_module = importlib.import_module("deai_check")
compile_module = importlib.import_module("compile")
verify_bib_module = importlib.import_module("verify_bib")
check_figures_module = importlib.import_module("check_figures")
check_pseudocode_module = importlib.import_module("check_pseudocode")
optimize_title_module = importlib.import_module("optimize_title")
translate_module = importlib.import_module("translate_academic")


def test_compile_biber_flag_forces_detected_recipe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text("\\documentclass{article}\\begin{document}x\\end{document}", encoding="utf-8")
    tex.with_suffix(".pdf").write_bytes(b"%PDF-1.4\n")

    calls: list[list[str]] = []

    def fake_run(cmd: list[str], cwd=None, capture_output=False):
        calls.append(cmd)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(compile_module.shutil, "which", lambda _tool: "/usr/bin/fake")
    monkeypatch.setattr(compile_module.subprocess, "run", fake_run)

    compiler = compile_module.LaTeXCompiler(str(tex), compiler="xelatex")
    code = compiler.compile(biber=True)

    assert code == 0
    assert compiler.recipe == "xelatex-biber"
    assert any(cmd[0] == "biber" for cmd in calls)


def test_compile_outdir_applies_to_default_latexmk(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text("\\documentclass{article}\\begin{document}x\\end{document}", encoding="utf-8")

    commands: list[list[str]] = []

    def fake_run(cmd: list[str], cwd=None, capture_output=False):
        commands.append(cmd)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(compile_module.shutil, "which", lambda _tool: "/usr/bin/fake")
    monkeypatch.setattr(compile_module.subprocess, "run", fake_run)

    compiler = compile_module.LaTeXCompiler(str(tex), compiler="pdflatex")
    code = compiler.compile(outdir="build")

    assert code == 0
    assert commands
    assert "-outdir=build" in commands[0]


def test_compile_biber_fallback_for_unknown_compiler(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text("\\documentclass{article}\\begin{document}x\\end{document}", encoding="utf-8")
    tex.with_suffix(".pdf").write_bytes(b"%PDF-1.4\n")

    def fake_run(cmd: list[str], cwd=None, capture_output=False):
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(compile_module.shutil, "which", lambda _tool: "/usr/bin/fake")
    monkeypatch.setattr(compile_module.subprocess, "run", fake_run)

    compiler = compile_module.LaTeXCompiler(str(tex), compiler="unknown")
    code = compiler.compile(biber=True)
    output = capsys.readouterr().out

    assert code == 0
    assert compiler.recipe == "pdflatex-biber"
    assert "Falling back to pdflatex-biber" in output


def test_verify_bib_reports_missing_and_unused_citations(tmp_path: Path) -> None:
    bib = tmp_path / "refs.bib"
    tex = tmp_path / "main.tex"
    bib.write_text(
        """@article{key1, title={T1}, author={A}, journal={J}, year={2020}}
@article{key2, title={T2}, author={B}, journal={J}, year={2021}}""",
        encoding="utf-8",
    )
    tex.write_text(
        "\\documentclass{article}\\begin{document}\\cite{key1,key3}\\end{document}",
        encoding="utf-8",
    )

    verifier = verify_bib_module.BibTeXVerifier(str(bib), tex_file=str(tex))
    result = verifier.verify()

    assert result["status"] == "FAIL"
    assert "key3" in result["missing_in_bib"]
    assert "key2" in result["unused_in_tex"]


def test_verify_bib_main_warning_exit_code_is_zero(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    bib = tmp_path / "refs.bib"
    tex = tmp_path / "main.tex"
    bib.write_text(
        """@article{key1, title={T1}, author={A}, journal={J}, year={2020}}
@article{key2, title={T2}, author={B}, journal={J}, year={2021}}""",
        encoding="utf-8",
    )
    tex.write_text(
        "\\documentclass{article}\\begin{document}\\cite{key1}\\end{document}", encoding="utf-8"
    )

    argv = [
        "verify_bib.py",
        str(bib),
        "--tex",
        str(tex),
        "--json",
    ]
    monkeypatch.setattr(sys, "argv", argv)
    code = verify_bib_module.main()
    assert code == 0


def test_check_figures_detects_includegraphics_with_optional_args(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    fig_pdf = tmp_path / "fig_a.pdf"
    fig_png = tmp_path / "fig_b.png"
    fig_pdf.write_bytes(b"%PDF-1.4\n")
    fig_png.write_bytes(b"not-a-real-png")
    tex.write_text(
        """\\documentclass{article}
\\begin{document}
\\includegraphics[width=0.5\\textwidth]{fig_a}
\\includegraphics{fig_b.png}
\\end{document}
""",
        encoding="utf-8",
    )

    checker = check_figures_module.FigureChecker(tex)
    figures = checker.find_figures()

    assert len(figures) == 2
    assert figures[0]["rel_path"] == "fig_a"
    assert figures[1]["rel_path"] == "fig_b.png"


def test_check_figures_pillow_missing_degrades_gracefully(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    tex = tmp_path / "main.tex"
    fig_png = tmp_path / "fig_b.png"
    fig_png.write_bytes(b"not-a-real-png")
    tex.write_text("\\includegraphics{fig_b.png}", encoding="utf-8")

    checker = check_figures_module.FigureChecker(tex)
    figure = checker.find_figures()[0]
    monkeypatch.setattr(check_figures_module, "Image", None)
    issues = checker.check_quality(figure)

    assert any("Pillow not installed" in issue for issue in issues)


def test_check_figures_help_does_not_advertise_json() -> None:
    script_path = Path(check_figures_module.__file__)
    result = subprocess.run(
        [sys.executable, "-B", str(script_path), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "--json" not in result.stdout


def test_check_pseudocode_flags_ieee_algorithm_float(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{IEEEtran}
\begin{document}
\begin{algorithm}
\caption{Adaptive inference procedure}
\label{alg:main}
\begin{algorithmic}
\State Update model state
\end{algorithmic}
\end{algorithm}
\end{document}
""",
        encoding="utf-8",
    )

    checker = check_pseudocode_module.PseudocodeChecker(str(tex), venue="ieee")
    issues = checker.check()

    assert any(issue["severity"] == "Critical" for issue in issues)
    assert any("floating algorithm environments" in issue["message"] for issue in issues)


def test_check_pseudocode_accepts_ieee_figure_wrapped_algorithmic(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{IEEEtran}
\usepackage{algorithmicx}
\usepackage{algpseudocodex}
\begin{document}
As shown in Fig.~\ref{alg:main}, the controller updates the state online.
\begin{figure}[t]
\caption{Adaptive inference procedure}
\label{alg:main}
\begin{algorithmic}[1]
\Require Current state $x_t$
\Ensure Updated estimate $\hat{x}_{t+1}$
\State Initialize the cache.
\Comment{Short note}
\end{algorithmic}
\end{figure}
\end{document}
""",
        encoding="utf-8",
    )

    checker = check_pseudocode_module.PseudocodeChecker(str(tex), venue="ieee")
    issues = checker.check()

    assert issues == []


def test_check_pseudocode_flags_article_led_caption_and_long_comment(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{IEEEtran}
\usepackage{algorithmicx}
\begin{document}
See Fig.~\ref{alg:main}.
\begin{figure}[t]
\caption{The proposed adaptive inference procedure}
\label{alg:main}
\begin{algorithmic}[1]
\Require State $x_t$
\Ensure Estimate $\hat{x}_{t+1}$
\State Update the cache.
\Comment{This comment line explains far too much detail for a compact pseudocode note.}
\end{algorithmic}
\end{figure}
\end{document}
""",
        encoding="utf-8",
    )

    checker = check_pseudocode_module.PseudocodeChecker(str(tex), venue="ieee")
    issues = checker.check()
    messages = "\n".join(issue["message"] for issue in issues)

    assert "caption starts with an article" in messages
    assert "unusually long" in messages


def test_analyze_experiment_accepts_plural_section_alias_and_reports_review_findings(
    tmp_path: Path,
) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Experiments}
Our method significantly outperforms prior methods on the benchmark.
\end{document}
""",
        encoding="utf-8",
    )

    findings = experiment_module.analyze(tex, "experiments")
    joined = "\n".join(findings).lower()

    assert "section not found" not in joined
    assert "% experiment" in joined
    assert "baseline" in joined or "comparator" in joined
    assert "ablation" in joined
    assert "statistical" in joined
    assert "efficiency" in joined


def test_translate_academic_preserves_latex_fragments() -> None:
    text = r"本文提出了一种用于时间序列预测的模型，如\cite{wang2024}所示，并最小化$L_{pred}$。"
    result = translate_module.translate(text, "deep-learning")

    assert r"\cite{wang2024}" in result
    assert r"$L_{pred}$" in result
    assert "time series forecasting" in result.lower()


def test_optimize_title_compare_requires_multiple_titles(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = optimize_title_module._run_compare_mode(["Only One"])
    output = capsys.readouterr()

    assert code == 1
    assert "--compare requires at least two title candidates" in output.err


def test_optimize_title_batch_mode_writes_json_report(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    out = tmp_path / "titles.json"
    tex.write_text(
        """\\documentclass{article}
\\title{A Study of New Method for Time Series Forecasting}
\\begin{abstract}
We propose a transformer approach for forecasting.
\\end{abstract}
""",
        encoding="utf-8",
    )

    code = optimize_title_module._run_batch_mode(str(tmp_path / "*.tex"), str(out))
    assert code == 0
    assert out.exists()

    payload = json.loads(out.read_text(encoding="utf-8"))
    assert isinstance(payload, list)
    assert payload
    assert payload[0]["file"].endswith("main.tex")


def test_optimize_title_batch_mode_empty_match_returns_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = optimize_title_module._run_batch_mode(str(tmp_path / "*.tex"), None)
    output = capsys.readouterr()

    assert code == 1
    assert "No files matched for batch mode" in output.err


# ── analyze_logic.py (WP1: Literature Review Quality) ─────────


def test_analyze_logic_detects_author_enumeration(tmp_path: Path) -> None:
    """A1: Flag 3+ consecutive author/year enumeration lines in Related Work."""
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Related Work}
In 2019, Smith et al. proposed a novel attention mechanism for sequence modeling.
In 2020, Jones et al. introduced a graph-based approach for document classification.
In 2021, Wang et al. presented a hybrid method combining transformers and CNNs.
In 2022, Li et al. developed an efficient pruning strategy for large models.
\end{document}
""",
        encoding="utf-8",
    )
    findings = logic_module.analyze(tex, "related")
    joined = "\n".join(findings).lower()
    assert "enumeration" in joined


def test_analyze_logic_detects_missing_gap_derivation(tmp_path: Path) -> None:
    """A3: Flag Related Work that lacks gap language in its final lines."""
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Related Work}
Smith et al. proposed method A for image classification.
Jones et al. introduced method B which achieved good results.
Wang et al. presented method C using transformers.
These methods share similar design principles and achieve competitive performance.
\end{document}
""",
        encoding="utf-8",
    )
    findings = logic_module.analyze(tex, "related")
    joined = "\n".join(findings).lower()
    assert "gap" in joined


def test_analyze_logic_passes_well_structured_related_work(tmp_path: Path) -> None:
    """Well-structured Related Work with gap derivation should pass A3."""
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Related Work}
Attention-based methods have shown promise in sequence modeling.
However, existing approaches have a significant limitation in handling
long-range dependencies efficiently. This gap motivates our approach.
\end{document}
""",
        encoding="utf-8",
    )
    findings = logic_module.analyze(tex, "related")
    joined = "\n".join(findings).lower()
    assert "gap" not in joined or "no rule-based" in joined


def test_analyze_literature_marks_borderline_cluster_for_review(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Related Work}
Smith et al. \cite{smith2020} proposed a convolutional baseline.
Jones et al. \cite{jones2021} introduced a transformer variant.
Lee et al. \cite{lee2022} designed a hybrid architecture for the same task.
Wang et al. \cite{wang2023} extended the benchmark with larger datasets.
\end{document}
""",
        encoding="utf-8",
    )

    findings = literature_module.analyze(tex, "related")
    joined = "\n".join(findings).lower()
    assert "needs review" in joined


def test_analyze_literature_flags_repeated_missing_comparative_synthesis(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Related Work}
Smith et al. \cite{smith2020} proposed a convolutional baseline.
Jones et al. \cite{jones2021} introduced a transformer variant.

Lee et al. \cite{lee2022} designed a hybrid architecture for the same task.
Wang et al. \cite{wang2023} extended the benchmark with larger datasets.
\end{document}
""",
        encoding="utf-8",
    )

    findings = literature_module.analyze(tex, "related")
    joined = "\n".join(findings).lower()
    assert "repeatedly catalog prior work" in joined


def test_analyze_literature_passes_when_comparison_and_gap_are_present(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Related Work}
CNN-based methods are efficient on small datasets, whereas transformer variants model long-range dependencies more effectively.
However, both families remain sensitive to distribution shift and require large labeled corpora.
This shared limitation leaves a gap in robust forecasting under scarce labels, which motivates our method.
\end{document}
""",
        encoding="utf-8",
    )

    findings = literature_module.analyze(tex, "related")
    joined = "\n".join(findings).lower()
    assert "comparative synthesis" not in joined


# ── analyze_logic.py (WP4: Cross-Section Logic Chain) ─────────


def test_analyze_logic_cross_section_incomplete(tmp_path: Path) -> None:
    """C3: Flag when Conclusion has no answer language for Introduction claims."""
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Introduction}
We propose a novel framework for time series forecasting.
Our contribution includes a new attention mechanism.
\section{Related Work}
Prior work has explored various approaches.
\section{Conclusion}
Time series forecasting is an important problem.
Future work will explore additional datasets.
\end{document}
""",
        encoding="utf-8",
    )
    findings = logic_module.analyze(tex, cross_section=True)
    joined = "\n".join(findings).lower()
    assert "logic chain" in joined or "cross-section" in joined


def test_analyze_logic_cross_section_complete(tmp_path: Path) -> None:
    """C3: Pass when Conclusion explicitly addresses Introduction claims."""
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Introduction}
We propose a novel framework for time series forecasting.
\section{Related Work}
Prior work has explored various approaches.
\section{Conclusion}
We have shown that our framework achieves state-of-the-art results.
Results demonstrate the effectiveness of the proposed approach.
\end{document}
""",
        encoding="utf-8",
    )
    findings = logic_module.analyze(tex, cross_section=True)
    joined = "\n".join(findings).lower()
    assert "logic chain" not in joined


def test_analyze_logic_flags_intro_funnel_jump(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Introduction}
Time series forecasting is important in industrial planning.
We propose a new adaptive transformer for this task.
\section{Conclusion}
We have shown strong results on multiple benchmarks.
\end{document}
""",
        encoding="utf-8",
    )
    findings = logic_module.analyze(tex)
    joined = "\n".join(findings).lower()
    assert "jump from background directly to contribution" in joined or "funnel" in joined


def test_analyze_logic_flags_tri_section_misalignment(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\begin{abstract}
We study long-horizon forecasting and propose a sparse transformer.
\end{abstract}
\section{Introduction}
We propose a sparse transformer and our main contributions are improved efficiency and accuracy.
\section{Conclusion}
Future work will explore more datasets.
\end{document}
""",
        encoding="utf-8",
    )
    findings = logic_module.analyze(tex, cross_section=True)
    joined = "\n".join(findings).lower()
    assert "misaligned" in joined


# ── analyze_experiment.py (WP2: Discussion Depth) ─────────────


def test_analyze_experiment_flags_shallow_discussion(tmp_path: Path) -> None:
    """B3: Flag discussion section with low attribution/explanatory ratio."""
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Discussion}
Our method achieves 95.2 percent accuracy.
The F1 score is 0.93.
The precision is 0.94 and recall is 0.92.
Results on dataset A show 96.1 percent.
Results on dataset B show 93.8 percent.
Results on dataset C show 94.5 percent.
The overall performance is satisfactory.
\end{document}
""",
        encoding="utf-8",
    )
    findings = experiment_module.analyze(tex, "discussion")
    joined = "\n".join(findings).lower()
    assert "depth" in joined or "attribution" in joined or "explanatory" in joined


def test_analyze_experiment_flags_no_literature_echo(tmp_path: Path) -> None:
    """B4: Flag when no Related Work citations reappear in Discussion."""
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Related Work}
Smith et al. \cite{smith2020} proposed method A.
Jones et al. \cite{jones2021} introduced method B.
\section{Discussion}
Our method achieves the best performance on all benchmarks.
The improvement is consistent across all datasets.
\end{document}
""",
        encoding="utf-8",
    )
    findings = experiment_module.analyze(tex)
    joined = "\n".join(findings).lower()
    assert "literature echo" in joined or "citations from related work" in joined


# ── analyze_experiment.py (WP5: Conclusion Completeness) ──────


def test_analyze_experiment_conclusion_incomplete(tmp_path: Path) -> None:
    """B5: Flag conclusion missing limitations/future work."""
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Conclusion}
We have shown that our method achieves good results.
The approach enables real-time processing of large datasets.
\end{document}
""",
        encoding="utf-8",
    )
    findings = experiment_module.analyze(tex, "conclusion")
    joined = "\n".join(findings).lower()
    assert "limitation" in joined or "future work" in joined


def test_analyze_experiment_conclusion_complete(tmp_path: Path) -> None:
    """B5: Pass when conclusion contains all three elements."""
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Conclusion}
We have shown that our method achieves state-of-the-art results on three benchmarks.
This approach enables efficient processing applicable to real-time systems.
A limitation of this work is the reliance on labeled data.
Future work will explore semi-supervised extensions.
\end{document}
""",
        encoding="utf-8",
    )
    findings = experiment_module.analyze(tex, "conclusion")
    joined = "\n".join(findings).lower()
    has_limitation_issue = "limitation" in joined and "lacks" in joined
    assert not has_limitation_issue


def test_analyze_experiment_flags_unlayered_discussion(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Discussion}
Our method reaches 95.2 accuracy on dataset A.
It reaches 94.8 accuracy on dataset B.
It reaches 93.9 accuracy on dataset C.
The macro-F1 is 0.92 on dataset A.
The macro-F1 is 0.90 on dataset B.
The macro-F1 is 0.89 on dataset C.
Overall, the reported numbers are strong.
\end{document}
""",
        encoding="utf-8",
    )
    findings = experiment_module.analyze(tex, "discussion")
    joined = "\n".join(findings).lower()
    assert "layered structure" in joined


def test_deai_detects_low_information_density(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Introduction}
In recent years, this topic has attracted much attention.
This paper makes an important contribution to the field.
This paper provides a comprehensive analysis of the problem.
This paper offers an effective solution with significant improvement.
\end{document}
""",
        encoding="utf-8",
    )
    checker = deai_module.AITraceChecker(tex)
    result = checker.check_section("introduction")
    categories = {trace["category"] for trace in result["traces"]}
    assert "low_information_density" in categories


def test_deai_avoids_low_information_false_positive_with_evidence(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"""\documentclass{article}
\begin{document}
\section{Introduction}
In recent years, transformer forecasting has attracted much attention \cite{smith2024}.
We propose a sparse transformer that reduces MAE by 12.3\% over PatchTST.
Experiments on three datasets show consistent gains in both MAE and RMSE.
\end{document}
""",
        encoding="utf-8",
    )
    checker = deai_module.AITraceChecker(tex)
    result = checker.check_section("introduction")
    categories = {trace["category"] for trace in result["traces"]}
    assert "low_information_density" not in categories
