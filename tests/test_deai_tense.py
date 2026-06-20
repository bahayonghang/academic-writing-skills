"""Tense checker tests for deai_check.py.

Imports the latex-paper-en copy (conftest puts SCRIPT_DIR_EN on sys.path). The
typst copy shares this logic; the zh copy gates to the English-abstract region
instead of method/result sections (see that skill's own behavior).
"""

import importlib
from pathlib import Path

deai_module = importlib.import_module("deai_check")


def _doc(tmp_path: Path, body: str, section: str = "Methods") -> Path:
    tex = tmp_path / "m.tex"
    tex.write_text(
        "\\documentclass{article}\n\\begin{document}\n"
        + f"\\section{{{section}}}\n"
        + body
        + "\n\\end{document}\n",
        encoding="utf-8",
    )
    return tex


def _tense(checker) -> list[dict]:
    return [
        s
        for s in checker.generate_suggestions_json(checker.analyze_document())
        if s["category"] == "tense"
    ]


def test_tense_flags_present_reporting_verbs_in_results(tmp_path: Path) -> None:
    tex = _doc(
        tmp_path,
        "Our method shows strong gains and outperforms the baseline.",
        section="Results",
    )
    checker = deai_module.AITraceChecker(tex)
    traces = _tense(checker)
    assert traces, "present-tense reporting verbs in Results should be flagged"
    assert all(s["suggestion_key"] == "past_in_methods_results" for s in traces)
    # Each resolves to the specific tense instruction, not the generic fallback.
    for s in traces:
        assert s["instruction"] != "Rewrite to be more specific and objective."
        assert "past tense" in s["instruction"]


def test_tense_flags_in_methods_section(tmp_path: Path) -> None:
    tex = _doc(tmp_path, "The procedure demonstrates the effect.", section="Methods")
    assert _tense(deai_module.AITraceChecker(tex))


def test_tense_skips_figure_and_table_subjects(tmp_path: Path) -> None:
    tex = _doc(
        tmp_path,
        "Figure 2 shows the loss curve. Table 1 presents the final scores.",
        section="Results",
    )
    assert _tense(deai_module.AITraceChecker(tex)) == []


def test_tense_gated_to_methods_experiments_results(tmp_path: Path) -> None:
    # Same verb in Introduction must NOT be flagged (section gating).
    tex = _doc(tmp_path, "The model shows promise.", section="Introduction")
    assert _tense(deai_module.AITraceChecker(tex)) == []


def test_tense_silent_on_past_tense(tmp_path: Path) -> None:
    tex = _doc(
        tmp_path,
        "Our method showed strong gains and outperformed the baseline.",
        section="Results",
    )
    assert _tense(deai_module.AITraceChecker(tex)) == []


def test_tense_can_be_disabled(tmp_path: Path) -> None:
    tex = _doc(tmp_path, "Our method shows strong gains.", section="Results")
    checker = deai_module.AITraceChecker(tex)
    checker._tense_enabled = False
    assert _tense(checker) == []


def test_tense_has_default_threshold_fallback(tmp_path: Path) -> None:
    tex = _doc(tmp_path, "x", section="Methods")
    checker = deai_module.AITraceChecker(tex)
    assert checker._tense_enabled is True
    assert any("shows?" in pattern for pattern, _ in checker._tense_signals)
    # DEFAULT_THRESHOLDS guarantees the checker works even if the YAML is absent.
    assert deai_module.DEFAULT_THRESHOLDS["tense"]["present_signals"]
