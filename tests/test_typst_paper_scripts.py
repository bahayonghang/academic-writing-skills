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
    _collision_names = (
        "parsers",
        "compile",
        "verify_bib",
        "optimize_title",
        "check_format",
        "check_pseudocode",
    )
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
check_pseudocode_typst = _load_typst("check_pseudocode")
parsers_typst = _load_typst("parsers")
analyze_logic_typst = _load_typst("analyze_logic")
analyze_literature_typst = _load_typst("analyze_literature")
analyze_experiment_typst = _load_typst("analyze_experiment")
deai_typst = _load_typst("deai_check")


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


def test_typst_pseudocode_accepts_algorithm_figure_defaults(tmp_path: Path) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text(
        """#import "@preview/algorithmic:0.1.0": *
#show: style-algorithm

#algorithm-figure(
  caption: [Adaptive inference procedure],
  line-numbers: true,
)[
  step("Initialize cache")
  comment("Short note")
]
""",
        encoding="utf-8",
    )

    checker = check_pseudocode_typst.PseudocodeChecker(str(typ), venue="ieee")
    issues = checker.check()

    assert issues == []


def test_typst_pseudocode_flags_missing_caption_and_style_hook(tmp_path: Path) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text(
        """#import "@preview/algorithmic:0.1.0": *

#algorithm-figure(
)[
  step("Initialize cache")
]
""",
        encoding="utf-8",
    )

    checker = check_pseudocode_typst.PseudocodeChecker(str(typ), venue="ieee")
    issues = checker.check()
    messages = "\n".join(issue["message"] for issue in issues)

    assert "style-algorithm" in messages
    assert "missing a caption" in messages


def test_typst_pseudocode_flags_lovelace_without_wrapper(tmp_path: Path) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text(
        """#import "@preview/lovelace:0.1.0": *

#lovelace[
  let step = "Initialize cache"
]
""",
        encoding="utf-8",
    )

    checker = check_pseudocode_typst.PseudocodeChecker(str(typ), venue="ieee")
    issues = checker.check()

    assert any(issue["severity"] == "Critical" for issue in issues)
    assert any("figure-like container" in issue["message"] for issue in issues)


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


def test_typst_analyze_literature_marks_borderline_cluster_for_review(tmp_path: Path) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text(
        """= Related Work
Smith et al. @smith2020 proposed a convolutional baseline.
Jones et al. @jones2021 introduced a transformer variant.
Lee et al. @lee2022 designed a hybrid architecture.
Wang et al. @wang2023 expanded the benchmark.
""",
        encoding="utf-8",
    )
    findings = analyze_literature_typst.analyze(typ, "related")
    joined = "\n".join(findings).lower()
    assert "needs review" in joined


def test_typst_analyze_literature_flags_repeated_missing_comparative_synthesis(
    tmp_path: Path,
) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text(
        """= Related Work
Smith et al. @smith2020 proposed a convolutional baseline.
Jones et al. @jones2021 introduced a transformer variant.

Lee et al. @lee2022 designed a hybrid architecture.
Wang et al. @wang2023 expanded the benchmark.
""",
        encoding="utf-8",
    )
    findings = analyze_literature_typst.analyze(typ, "related")
    joined = "\n".join(findings).lower()
    assert "multiple citation-heavy paragraphs" in joined


def test_typst_analyze_logic_flags_intro_funnel_jump(tmp_path: Path) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text(
        """= 绪论
工业预测在制造场景中十分重要。
本文提出一种稀疏注意力模型。
= 结论
未来工作将继续扩展更多数据集。
""",
        encoding="utf-8",
    )
    findings = analyze_logic_typst.analyze(typ)
    joined = "\n".join(findings).lower()
    assert "jump from background directly to contribution" in joined or "漏斗" in joined


def test_typst_analyze_logic_flags_tri_section_misalignment(tmp_path: Path) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text(
        """= 摘要
本文研究工业预测问题，并提出一种稀疏模型。
= 引言
本文提出一种稀疏模型，主要贡献是提升效率与精度。
= 结论
未来工作将考虑更多应用场景。
""",
        encoding="utf-8",
    )
    findings = analyze_logic_typst.analyze(typ, cross_section=True)
    joined = "\n".join(findings).lower()
    assert "misaligned" in joined


def test_typst_analyze_experiment_flags_unlayered_discussion(tmp_path: Path) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text(
        """= 讨论
模型在数据集A上的准确率为95.2%。
模型在数据集B上的准确率为94.8%。
模型在数据集C上的准确率为94.1%。
宏平均F1分别为0.92、0.90和0.89。
整体结果较好。
实验数值如上所示。
""",
        encoding="utf-8",
    )
    findings = analyze_experiment_typst.analyze(typ, "discussion")
    joined = "\n".join(findings).lower()
    assert "layered structure" in joined


def test_typst_deai_detects_low_information_density_in_chinese(tmp_path: Path) -> None:
    typ = tmp_path / "main.typ"
    typ.write_text(
        """= 绪论
近年来，该问题引起了广泛关注。
本文具有重要意义。
本文开展了全面研究。
本文取得了显著提升。
""",
        encoding="utf-8",
    )
    checker = deai_typst.AITraceChecker(typ)
    result = checker.check_section("introduction")
    categories = {trace["category"] for trace in result["traces"]}
    assert "low_information_density" in categories
