"""Regression tests for latex-paper-en script behaviors."""

import importlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

compile_module = importlib.import_module("compile")
verify_bib_module = importlib.import_module("verify_bib")
check_figures_module = importlib.import_module("check_figures")
optimize_title_module = importlib.import_module("optimize_title")


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
