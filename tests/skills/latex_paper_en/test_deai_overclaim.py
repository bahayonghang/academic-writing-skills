"""Over-claim checker tests for deai_check.py.

Imports the latex-paper-en copy (conftest puts SCRIPT_DIR_EN on sys.path). The
zh/typst copies share the same checker logic by design.
"""

import importlib
from pathlib import Path

deai_module = importlib.import_module("deai_check")


def _doc(tmp_path: Path, body: str) -> Path:
    tex = tmp_path / "m.tex"
    tex.write_text(
        "\\documentclass{article}\n\\begin{document}\n\\section{Introduction}\n"
        + body
        + "\n\\end{document}\n",
        encoding="utf-8",
    )
    return tex


def test_overclaim_flags_causal_firstness_universal_application(tmp_path: Path) -> None:
    tex = _doc(
        tmp_path,
        "The gain is caused by the module and proves that it works universally. "
        "For the first time, this will revolutionize the field.",
    )
    checker = deai_module.AITraceChecker(tex)
    suggestions = checker.generate_suggestions_json(checker.analyze_document())
    oc = [s for s in suggestions if s["category"] == "overclaim"]
    keys = {s["suggestion_key"] for s in oc}
    assert {"soften_causal", "qualify_novelty", "bound_universal", "hedge_application"} <= keys
    # Each suggestion resolves to a specific instruction, not the generic fallback.
    for s in oc:
        assert s["instruction"] != "Rewrite to be more specific and objective."


def test_overclaim_silent_on_clean_prose(tmp_path: Path) -> None:
    tex = _doc(
        tmp_path,
        "We trained the model with Adam and report accuracy on three datasets. "
        "The method is associated with lower error in the cases studied.",
    )
    checker = deai_module.AITraceChecker(tex)
    oc = [
        s
        for s in checker.generate_suggestions_json(checker.analyze_document())
        if s["category"] == "overclaim"
    ]
    assert oc == []


def test_overclaim_can_be_disabled(tmp_path: Path) -> None:
    tex = _doc(tmp_path, "The gain is caused by the module.")
    checker = deai_module.AITraceChecker(tex)
    checker._overclaim_enabled = False
    oc = [
        s
        for s in checker.generate_suggestions_json(checker.analyze_document())
        if s["category"] == "overclaim"
    ]
    assert oc == []


def test_overclaim_has_default_threshold_fallback(tmp_path: Path) -> None:
    tex = _doc(tmp_path, "x")
    checker = deai_module.AITraceChecker(tex)
    assert checker._overclaim_enabled is True
    assert any("caused by" in pattern for pattern, _ in checker._overclaim_patterns)
    # DEFAULT_THRESHOLDS guarantees the checker works even if the YAML is absent.
    assert deai_module.DEFAULT_THRESHOLDS["overclaim"]["patterns"]
