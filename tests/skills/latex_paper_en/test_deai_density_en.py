"""C3 regression coverage for English density conversion and sequence boundaries."""

from __future__ import annotations

import math
from pathlib import Path

import deai_check as deai
import yaml

from tests.support.paths import SKILLS_ROOT

_SKILL_DIR = SKILLS_ROOT / "latex-paper-en"
_YAML = _SKILL_DIR / "references" / "deai" / "tone-thresholds.yaml"


def _checker(tmp_path: Path) -> deai.AITraceChecker:
    tex = tmp_path / "main.tex"
    tex.write_text("\\section{Introduction}\nVisible prose remains available.\n", encoding="utf-8")
    return deai.AITraceChecker(tex)


def _visible_words(count: int, term: str = "analysis", hits: int = 0) -> list[tuple[int, str, str]]:
    assert 0 <= hits <= count
    text = " ".join([term] * hits + ["analysis"] * (count - hits))
    return [(1, "introduction", text)]


def test_default_and_yaml_density_contracts_match() -> None:
    configured = yaml.safe_load(_YAML.read_text(encoding="utf-8"))
    assert deai.DEFAULT_THRESHOLDS["threshold_unit"] == "per_10k_words"
    for key in (
        "threshold_unit",
        "density_fallback",
        "term_thresholds",
        "section_factors",
        "sequence_terms",
        "throat_clearing",
    ):
        assert configured[key] == deai.DEFAULT_THRESHOLDS[key]
    assert configured["threshold_calibration"]["validation_status"].startswith("UNVERIFIED")


def test_missing_yaml_clean_clone_uses_density_defaults(tmp_path: Path) -> None:
    script_dir = tmp_path / "scripts"
    script_dir.mkdir()
    loaded = deai._load_thresholds(script_dir)
    assert loaded["threshold_unit"] == "per_10k_words"
    assert loaded["term_thresholds"] == deai.DEFAULT_THRESHOLDS["term_thresholds"]
    assert loaded["throat_clearing"]["budget_per_10k"] == 2.0


def test_every_legacy_cap_has_exact_5000_word_equivalence_and_density_scaling(
    tmp_path: Path,
) -> None:
    checker = _checker(tmp_path)
    for term, density in deai.DEFAULT_THRESHOLDS["term_thresholds"].items():
        legacy_cap = int(density / 2)
        assert density == legacy_cap * 2
        for words, expected in (
            (1500, math.ceil(legacy_cap * 0.3)),
            (5000, legacy_cap),
            (10000, legacy_cap * 2),
        ):
            cap, corpus, fallback = checker._density_cap(
                term,
                float(density),
                _visible_words(words),
            )
            assert (cap, corpus) == (expected, words)
            assert fallback is (words < 1500)

        checker.thresholds["term_thresholds"] = {term: density}
        checker._iter_visible_lines = lambda term=term, legacy_cap=legacy_cap: _visible_words(
            5000, term, legacy_cap
        )
        assert checker._check_term_threshold() == []
        checker._iter_visible_lines = lambda term=term, legacy_cap=legacy_cap: _visible_words(
            5000, term, legacy_cap + 1
        )
        traces = checker._check_term_threshold()
        assert len(traces) == 1 and traces[0]["pattern"] == f"term_threshold:{term}"


def test_canonical_visible_word_regex_counts_hyphen_apostrophe_and_abbreviation(
    tmp_path: Path,
) -> None:
    checker = _checker(tmp_path)
    raw = r"state-of-the-art don't U.S. alpha \cite{smith} $x+y$ \label{sec:x}"
    visible = checker.parser.extract_visible_text(raw)
    assert visible == "state-of-the-art don't U.S. alpha"
    assert checker._corpus_size([(1, "introduction", visible)]) == 5


def test_sequence_terms_match_only_lowercase_standalone_words(tmp_path: Path) -> None:
    checker = _checker(tmp_path)
    checker.thresholds["threshold_unit"] = "per_document"
    checker.thresholds["term_thresholds"] = {"first": 0}
    checker.thresholds["sequence_terms"] = ["first"]
    checker._iter_visible_lines = lambda: [
        (1, "introduction", "first first-order FIRST First first–stage"),
    ]
    traces = checker._check_term_threshold()
    assert len(traces) == 1
    assert "used 1 times" in traces[0]["text"]


def test_throat_clearing_uses_5000_word_baseline_budget(tmp_path: Path) -> None:
    checker = _checker(tmp_path)
    cfg = checker.thresholds["throat_clearing"]
    assert cfg["budget_per_10k"] == 2.0
    assert cfg["min_budget"] == 1
    assert math.ceil(cfg["budget_per_10k"] * 5000 / 10000) == 1
    assert math.ceil(cfg["budget_per_10k"] * 10000 / 10000) == 2
