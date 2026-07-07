"""De-AI checker tests for the typst-paper copy of deai_check.py.

The typst copy is loaded by file path via importlib: a bare ``import deai_check``
resolves to the latex-paper-en copy that conftest puts on ``sys.path``, which
gates tense to method/result sections and searches evidence differently. These
typst-specific behaviors — the citation-dense ``low_information_density``
exemption and the ``@fig``-ref tense subject guard — would silently test the
wrong object under a bare import. Same loader rationale as
``test_typst_paper_scripts`` / ``test_deai_tense_zh``.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_TYPST

_TYPST_DIR = SCRIPT_DIR_TYPST


def _load_typst(name: str):
    """Load a module from the Typst scripts directory by file path.

    Puts the Typst dir first on sys.path and evicts collision-prone shared
    modules so the Typst copy's ``from parsers import ...`` resolves to the
    Typst versions; restores both afterwards to avoid leaking into EN/AUDIT
    test suites.
    """
    typst_str = str(_TYPST_DIR)
    inserted = False
    if typst_str not in sys.path or sys.path.index(typst_str) != 0:
        sys.path.insert(0, typst_str)
        inserted = True

    _collision_names = ("parsers",)
    _saved = {}
    for mod_name in list(sys.modules):
        if mod_name in _collision_names:
            _saved[mod_name] = sys.modules.pop(mod_name)

    spec = importlib.util.spec_from_file_location(f"typst_{name}", _TYPST_DIR / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for mod_name in _collision_names:
        if mod_name in sys.modules and mod_name not in _saved:
            del sys.modules[mod_name]
        if mod_name in _saved:
            sys.modules[mod_name] = _saved[mod_name]

    if inserted and typst_str in sys.path:
        sys.path.remove(typst_str)
        sys.path.append(typst_str)

    return module


deai_typst = _load_typst("deai_check")


def _checker(tmp_path: Path, body: str):
    typ = tmp_path / "m.typ"
    typ.write_text(body, encoding="utf-8")
    return deai_typst.AITraceChecker(typ)


def _tense(checker) -> list[dict]:
    return [
        s
        for s in checker.generate_suggestions_json(checker.analyze_document())
        if s["category"] == "tense"
    ]


# --- XA-1: low_information_density citation exemption (EN "E17" fix, ported) ----

# A citation-dense, number-free paragraph: extract_visible_text strips the @keys,
# so evidence must be checked on the raw source or this reads as evidence-free.
_CITED = """= Introduction
This approach has been widely used across many different domains @smith2020 @jones2021.
It is worth noting that various methods play an important role in this area @lee2019.
Furthermore, several comprehensive studies demonstrate the significance here @kim2022.
"""

# Same boilerplate with the citations removed — no evidence marker anywhere.
_UNCITED = """= Introduction
This approach has been widely used across many different domains and settings here.
It is worth noting that various methods play an important role in this area today.
Furthermore, several comprehensive studies demonstrate the significance here now.
"""


def test_low_info_density_exempts_citation_dense_paragraph(tmp_path: Path) -> None:
    checker = _checker(tmp_path, _CITED)
    result = checker.check_section("introduction")
    categories = {trace["category"] for trace in result["traces"]}
    assert "low_information_density" not in categories


def test_low_info_density_flags_same_paragraph_without_citations(tmp_path: Path) -> None:
    # Positive control: identical boilerplate minus the @keys IS flagged, proving
    # the exemption above is citation-driven and the checker is not simply dead.
    checker = _checker(tmp_path, _UNCITED)
    result = checker.check_section("introduction")
    categories = {trace["category"] for trace in result["traces"]}
    assert "low_information_density" in categories


# --- XA-2: tense figure/table false-positive guard sees Typst @fig refs ---------


def test_tense_exempts_typst_fig_ref_subject(tmp_path: Path) -> None:
    checker = _checker(
        tmp_path,
        "= Results\n@fig-loss shows the training curve and the model outperforms the baseline.\n",
    )
    assert _tense(checker) == []


def test_tense_flags_real_subject_in_results(tmp_path: Path) -> None:
    checker = _checker(
        tmp_path,
        "= Results\nThe proposed method shows lower error than the strong baseline overall.\n",
    )
    assert _tense(checker), "a non-figure subject in Results must still be flagged"


def test_tense_trace_reports_visible_text_not_injected_keyword(tmp_path: Path) -> None:
    # The @fig rewrite used by the guard must not leak the literal "figure" into
    # the reported text: a flagged line keeps its real visible text (ref blanked).
    checker = _checker(
        tmp_path,
        "= Results\nThe method shows gains; @fig-loss plots the curve.\n",
    )
    traces = _tense(checker)
    assert traces
    assert all("figure" not in s["issue"].lower() for s in traces)


# --- SH-1: "the present study" adjective vs. the verb "presents" ----------------


def test_tense_present_adjective_exempt_but_verb_flagged(tmp_path: Path) -> None:
    adj = _checker(
        tmp_path,
        "= Results\nThe present study achieves lower error than the strong baseline here.\n",
    )
    adj_patterns = {s["pattern"] for s in _tense(adj)}
    assert not any("present" in p for p in adj_patterns), "'present' adjective must not flag"

    verb = _checker(
        tmp_path,
        "= Results\nThis paper presents the final results across the benchmark suites here.\n",
    )
    verb_patterns = {s["pattern"] for s in _tense(verb)}
    assert any("present" in p for p in verb_patterns), "verb 'presents' must still flag"


# --- TST-1: over-claim checker exists on the Typst copy too ---------------------


def test_overclaim_flags_on_typst_copy(tmp_path: Path) -> None:
    checker = _checker(
        tmp_path,
        "= Introduction\nThe gain is caused by the module and proves that it works universally.\n",
    )
    overclaim = [
        s
        for s in checker.generate_suggestions_json(checker.analyze_document())
        if s["category"] == "overclaim"
    ]
    keys = {s["suggestion_key"] for s in overclaim}
    assert {"soften_causal", "bound_universal"} <= keys
