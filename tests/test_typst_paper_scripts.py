"""Regression tests for typst-paper script behaviors."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

_TYPST_DIR = Path(__file__).parent.parent / "academic-writing-skills" / "typst-paper" / "scripts"


def _load_typst(name: str):
    """Load a module from the Typst scripts directory by file path.

    Uses save/restore to prevent sys.modules pollution across test suites.
    """
    typst_str = str(_TYPST_DIR)
    inserted = False
    if typst_str not in sys.path or sys.path.index(typst_str) != 0:
        sys.path.insert(0, typst_str)
        inserted = True

    # Save and remove collision-prone modules so Typst versions get loaded fresh
    _collision_names = ("parsers", "compile", "verify_bib", "optimize_title", "check_format")
    _saved = {}
    for mod_name in list(sys.modules):
        if mod_name in _collision_names:
            _saved[mod_name] = sys.modules.pop(mod_name)

    spec = importlib.util.spec_from_file_location(f"typst_{name}", _TYPST_DIR / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Restore original modules to prevent cross-suite pollution
    for mod_name in _collision_names:
        if mod_name in sys.modules and mod_name not in _saved:
            del sys.modules[mod_name]
        if mod_name in _saved:
            sys.modules[mod_name] = _saved[mod_name]

    if inserted and typst_str in sys.path:
        sys.path.remove(typst_str)
        sys.path.append(typst_str)

    return module


compile_typst = _load_typst("compile")
verify_bib_typst = _load_typst("verify_bib")
optimize_title_typst = _load_typst("optimize_title")
check_format_typst = _load_typst("check_format")
parsers_typst = _load_typst("parsers")
analyze_logic_typst = _load_typst("analyze_logic")


def test_typst_compile_missing_binary_returns_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text("= Title", encoding="utf-8")

    monkeypatch.setattr(compile_typst.shutil, "which", lambda _tool: None)
    compiler = compile_typst.TypstCompiler(str(typ))
    code = compiler.compile()

    assert code == 1


def test_typst_compile_png_inserts_format_flag(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text("= Title", encoding="utf-8")
    commands: list[list[str]] = []

    def fake_run(cmd, cwd=None, capture_output=False):
        commands.append(cmd)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(compile_typst.shutil, "which", lambda _tool: "/usr/bin/fake")
    monkeypatch.setattr(compile_typst.subprocess, "run", fake_run)

    compiler = compile_typst.TypstCompiler(str(typ))
    code = compiler.compile(format="png", output="paper.png")

    assert code == 0
    assert commands
    assert commands[0][:4] == ["typst", "compile", "--format", "png"]
    assert commands[0][-1] == "paper.png"


def test_typst_format_checker_flags_missing_bibliography(tmp_path: Path) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text("@smith2024\n= Introduction\ncontent", encoding="utf-8")

    checker = check_format_typst.FormatChecker(str(typ), venue="ieee")
    assert checker.load_file() is True
    checker.check_citations()

    assert "Citations found but no bibliography command" in checker.issues


def test_typst_verify_bib_reports_missing_and_unused_citations(tmp_path: Path) -> None:
    bib = tmp_path / "refs.bib"
    typ = tmp_path / "main.typ"
    bib.write_text(
        """@article{key1, title={T1}, author={A}, journal={J}, year={2020}}
@article{key2, title={T2}, author={B}, journal={J}, year={2021}}""",
        encoding="utf-8",
    )
    typ.write_text("= Intro\nSee @key1 and @key3.", encoding="utf-8")

    checker = verify_bib_typst.BibChecker(str(bib), typ_file=str(typ))
    assert checker.load_bibtex() is True
    checker.check_citations()

    assert any("key3" in issue for issue in checker.issues)
    assert any("key2" in warning for warning in checker.warnings)


def test_typst_optimize_title_removes_ineffective_words() -> None:
    optimized = optimize_title_typst.optimize_title("A Study of Transformer Forecasting")
    assert "Study of" not in optimized


def test_typst_score_title_rewards_specific_titles() -> None:
    score = optimize_title_typst.score_title(
        "Transformer-Based Time Series Forecasting for Industrial Control"
    )
    assert score["total"] >= 60


def test_typst_parsers_extract_title_and_abstract() -> None:
    content = """#set document(title: [#emph[Industrial Forecasting with Transformers]])

#abstract[
This paper studies time series forecasting.
]
"""
    assert parsers_typst.extract_title(content) == "Industrial Forecasting with Transformers"
    assert "time series forecasting" in parsers_typst.extract_abstract(content)


# ── analyze_logic.py (WP1: Literature Review Quality for Typst) ──


def test_typst_analyze_logic_detects_author_enumeration(tmp_path: Path) -> None:
    """A1: Flag 3+ consecutive author/year enumeration in Typst."""
    typ = tmp_path / "main.typ"
    typ.write_text(
        """= Related Work
In 2019, Smith et al. proposed a novel attention mechanism.
In 2020, Jones et al. introduced a graph-based approach.
In 2021, Wang et al. presented a hybrid transformer method.
In 2022, Li et al. developed an efficient pruning strategy.
""",
        encoding="utf-8",
    )
    findings = analyze_logic_typst.analyze(typ, "related")
    joined = "\n".join(findings).lower()
    assert "enumeration" in joined


def test_typst_analyze_logic_detects_missing_gap_derivation(tmp_path: Path) -> None:
    """A3: Flag Related Work that lacks gap language in Typst."""
    typ = tmp_path / "main.typ"
    typ.write_text(
        """= Related Work
Various methods have been proposed for this task.
These approaches achieve competitive performance on standard benchmarks.
The field continues to evolve with new architectures.
""",
        encoding="utf-8",
    )
    findings = analyze_logic_typst.analyze(typ, "related")
    joined = "\n".join(findings).lower()
    assert "gap" in joined
