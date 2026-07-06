"""Tense checker tests for the latex-thesis-zh copy of deai_check.py.

The zh checker gates tense detection to the *English abstract region* (Chinese
prose has no tense), so it must locate that region across the flagship thesis
templates: generic ``\\begin{abstract}``, thuthesis ``\\begin{abstract*}`` and
pkuthss ``\\begin{eabstract}``, while skipping the Chinese abstract environments.

The zh copy is loaded by file path via importlib — a bare ``import deai_check``
resolves to the latex-paper-en copy on sys.path (see conftest), which gates to
method/result sections instead and would silently test the wrong object.
"""

import importlib.util
import sys
from pathlib import Path

_ZH_DIR = Path(__file__).parent.parent / "academic-writing-skills" / "latex-thesis-zh" / "scripts"

# Shared module names other skills also vendor; evicted around each load so the
# ZH copy wins, then restored so later EN/AUDIT tests are unaffected.
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load_zh(name: str):
    """Load a module from the ZH scripts directory by file path, isolated from
    other skills' cached ``parsers`` / ``tex_loader`` modules.

    Evicts those shared names and puts the ZH dir at ``sys.path[0]`` before
    executing, forcing the ZH copy's ``from parsers import ...`` to resolve to
    the ZH versions; restores both ``sys.path`` and the evicted modules
    afterward so EN/AUDIT tests are unaffected.
    """
    path = _ZH_DIR / f"{name}.py"
    saved_path = list(sys.path)
    saved_modules = {n: sys.modules.pop(n, None) for n in _SHARED_MODULE_NAMES}
    try:
        sys.path.insert(0, str(_ZH_DIR))
        spec = importlib.util.spec_from_file_location(f"zh_{name}", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for n, mod in saved_modules.items():
            if mod is not None:
                sys.modules[n] = mod
            else:
                sys.modules.pop(n, None)


deai_check = _load_zh("deai_check")

_EN_ABSTRACT = "Our method shows strong gains and outperforms the baseline.\n"
_ZH_ABSTRACT = "本文提出一种方法，显著提升了性能。\n"


def _checker(tmp_path: Path, body: str, cls: str = "ctexbook"):
    tex = tmp_path / "t.tex"
    tex.write_text(
        f"\\documentclass{{{cls}}}\n\\begin{{document}}\n{body}\\end{{document}}\n",
        encoding="utf-8",
    )
    return deai_check.ChineseAITraceChecker(tex)


def _tense(checker) -> list[dict]:
    return [
        s
        for s in checker.generate_suggestions_json(checker.analyze_document())
        if s["category"] == "tense"
    ]


def test_loads_the_zh_copy_not_the_en_copy() -> None:
    # Guards the importlib path-load: the EN copy exposes AITraceChecker, the zh
    # copy exposes ChineseAITraceChecker with the English-abstract gate.
    assert hasattr(deai_check, "ChineseAITraceChecker")
    assert hasattr(deai_check.ChineseAITraceChecker, "_english_abstract_range")


def test_generic_plain_abstract_flags_present_tense(tmp_path: Path) -> None:
    checker = _checker(tmp_path, f"\\begin{{abstract}}\n{_EN_ABSTRACT}\\end{{abstract}}\n")
    traces = _tense(checker)
    assert traces, "present-tense reporting verbs in a plain English abstract should be flagged"
    assert all(s["suggestion_key"] == "past_in_methods_results" for s in traces)
    for s in traces:
        assert s["instruction"] != "请改写得更具体、客观。"
        assert "过去时" in s["instruction"]


def test_thuthesis_abstract_star_flags_present_tense(tmp_path: Path) -> None:
    # thuthesis: \begin{abstract} is Chinese, \begin{abstract*} is English.
    body = (
        f"\\begin{{abstract}}\n{_ZH_ABSTRACT}\\end{{abstract}}\n"
        f"\\begin{{abstract*}}\n{_EN_ABSTRACT}\\end{{abstract*}}\n"
    )
    checker = _checker(tmp_path, body, cls="thuthesis")
    traces = _tense(checker)
    assert traces, "the thuthesis abstract* English abstract should be checked for tense"
    assert any("shows?" in s["pattern"] for s in traces)
    assert any("outperforms?" in s["pattern"] for s in traces)


def test_thuthesis_chinese_abstract_produces_no_tense(tmp_path: Path) -> None:
    # thuthesis with only the Chinese \begin{abstract}; an embedded English verb
    # must NOT be flagged because there is no English abstract region.
    body = "\\begin{abstract}\n本文提出一种方法，shows 出色的效果。\n\\end{abstract}\n"
    checker = _checker(tmp_path, body, cls="thuthesis")
    assert checker._en_abstract_range is None
    assert _tense(checker) == []


def test_pkuthss_eabstract_flags_present_tense(tmp_path: Path) -> None:
    # pkuthss: \begin{cabstract} is Chinese, \begin{eabstract} is English.
    body = (
        f"\\begin{{cabstract}}\n{_ZH_ABSTRACT}\\end{{cabstract}}\n"
        f"\\begin{{eabstract}}\n{_EN_ABSTRACT}\\end{{eabstract}}\n"
    )
    checker = _checker(tmp_path, body, cls="pkuthss")
    traces = _tense(checker)
    assert traces, "the pkuthss eabstract English abstract should be checked for tense"
    assert any("shows?" in s["pattern"] for s in traces)


def test_dual_plain_abstract_selects_english_region(tmp_path: Path) -> None:
    # Two plain \begin{abstract} environments, Chinese first then English:
    # the English one (not the first match) must be selected.
    body = (
        f"\\begin{{abstract}}\n{_ZH_ABSTRACT}\\end{{abstract}}\n"
        f"\\begin{{abstract}}\n{_EN_ABSTRACT}\\end{{abstract}}\n"
    )
    checker = _checker(tmp_path, body)
    traces = _tense(checker)
    assert traces, "the English abstract in a dual-abstract layout should be checked"
    assert any("shows?" in s["pattern"] for s in traces)


def test_dual_plain_abstract_english_first_also_selected(tmp_path: Path) -> None:
    # Ordering must not matter: English first, Chinese second still selects English.
    body = (
        f"\\begin{{abstract}}\n{_EN_ABSTRACT}\\end{{abstract}}\n"
        f"\\begin{{abstract}}\n{_ZH_ABSTRACT}\\end{{abstract}}\n"
    )
    checker = _checker(tmp_path, body)
    assert _tense(checker), "an English-first dual-abstract layout should still be checked"


def test_tense_silent_on_past_tense_abstract(tmp_path: Path) -> None:
    body = (
        "\\begin{abstract}\n"
        "Our method showed strong gains and outperformed the baseline.\n"
        "\\end{abstract}\n"
    )
    assert _tense(_checker(tmp_path, body)) == []


def test_present_study_adjective_not_flagged(tmp_path: Path) -> None:
    # SH-1: "the present study" is the adjective, not the reporting verb `presents`.
    # The signal is \bpresents\b (no `?`), so the bare word `present` must not hit.
    body = "\\begin{abstract}\nThe present study focuses on noise robustness.\n\\end{abstract}\n"
    assert _tense(_checker(tmp_path, body)) == []


def test_presents_reporting_verb_still_flagged(tmp_path: Path) -> None:
    # The verb `presents` is still a present-tense reporting signal.
    body = "\\begin{abstract}\nThis paper presents a noise-robust forecasting model.\n\\end{abstract}\n"
    traces = _tense(_checker(tmp_path, body))
    assert traces, "the reporting verb 'presents' should still be flagged"
    assert any("presents" in s["pattern"] for s in traces)
