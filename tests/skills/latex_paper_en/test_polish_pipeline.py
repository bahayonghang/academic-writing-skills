"""Regression tests for the EN/Typst polish pipeline (task 07-27-polish-en-expression-fix).

Every counter-example here was measured against the pre-fix scripts:
``Make sure`` became ``develop sure``, ``make use of`` became ``develop use of``,
``very few`` became ``highly few``, a sentence-initial grammar hit came back
lowercased, and runs of whitespace were silently collapsed.

Deliberately absent: a ``makes it possible`` case. ``\\bmake\\b`` does not match
``makes`` (the following ``e`` keeps the word boundary from holding), so such a
test would assert nothing.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

from tests.support.paths import SCRIPT_DIR_EN, SCRIPT_DIR_TYPST

sys.path.insert(0, str(SCRIPT_DIR_EN))

expression = importlib.import_module("improve_expression")
grammar = importlib.import_module("analyze_grammar")
sentences = importlib.import_module("analyze_sentences")
translate = importlib.import_module("translate_academic")

CONTRACT_FIELDS = ("Changed:", "Protected:", "Meaning-Check:", "Risk-Flags:")


def _tex(tmp_path: Path, *body: str) -> Path:
    path = tmp_path / "main.tex"
    path.write_text(
        "\\documentclass{article}\n\\begin{document}\n" + "\n".join(body) + "\n\\end{document}\n",
        encoding="utf-8",
    )
    return path


# ── P1-4: context-blind substitutions no longer produce wrong English ─────────


@pytest.mark.parametrize(
    ("source", "forbidden"),
    [
        ("Make sure the model converges.", "develop sure"),
        ("We make use of a pretrained encoder.", "develop use of"),
        ("Only very few samples are available.", "highly few"),
    ],
)
def test_context_dependent_patterns_are_never_auto_applied(source: str, forbidden: str) -> None:
    revised, rationales, applied, _protected = expression._enhance(source)

    assert revised == source, f"{source!r} must come back unchanged"
    assert not rationales and not applied
    assert forbidden not in revised


def test_context_dependent_patterns_are_still_reported_as_candidates() -> None:
    candidates = expression._find_candidates("Make sure the model converges.")

    assert candidates, "the weak verb must still be surfaced, just not applied"
    token, reason = candidates[0]
    assert token == "Make"
    assert "not" in reason or "context-dependent" in reason


def test_candidate_block_has_no_revised_line(tmp_path: Path) -> None:
    tex = _tex(tmp_path, "Make sure the model converges.")
    output = "\n".join(expression.analyze(tex, None))

    assert "Weak-expression candidate" in output
    assert "% Revised:" not in output
    assert "% Risk-Flags:    not-assessed" in output


# ── P1-4: casing survives substitution ───────────────────────────────────────


def test_expression_substitution_preserves_sentence_initial_capital() -> None:
    revised, _rationales, _applied, _protected = expression._enhance("Get better coverage.")

    assert revised.startswith("Obtain"), revised


def test_grammar_rule_preserves_sentence_initial_capital() -> None:
    findings = grammar._apply_rules("We propose method for forecasting.")

    assert findings
    _pattern, revised, _rationale = findings[0]
    assert revised.startswith("We propose a method"), revised


def test_grammar_rule_still_preserves_unrelated_acronyms() -> None:
    findings = grammar._apply_rules("These method use BERT and the data shows gains")

    assert any("BERT" in revised for _pattern, revised, _rationale in findings)


# ── P1-4: whitespace is left exactly as written ──────────────────────────────


def test_expression_does_not_collapse_whitespace() -> None:
    source = "We get  better  coverage in   a table."
    revised, _rationales, _applied, _protected = expression._enhance(source)

    assert revised.startswith("We obtain"), "the substitution itself should have applied"
    assert revised == "We obtain  better  coverage in   a table.", revised


# ── P2-1: plain-text protected tokens ────────────────────────────────────────


def test_protected_tokens_are_listed_and_never_rewritten() -> None:
    source = "We get 92.1% accuracy on CIFAR-100 with ResNet-50 and p < 0.05."
    revised, _rationales, _applied, protected = expression._enhance(source)

    assert revised.startswith("We obtain ")
    assert "92.1%" in revised and "CIFAR-100" in revised and "ResNet-50" in revised
    assert "92.1%" in protected
    assert "CIFAR-100" in protected
    assert "ResNet-50" in protected
    assert "p < 0.05" in protected


def test_protected_tokens_appear_in_the_contract_field(tmp_path: Path) -> None:
    tex = _tex(tmp_path, "We get 92.1\\% accuracy on CIFAR-100.")
    output = "\n".join(expression.analyze(tex, None))

    assert "% Protected:" in output
    protected_line = next(line for line in output.splitlines() if line.startswith("% Protected:"))
    assert "CIFAR-100" in protected_line


# ── C1 contract fields ───────────────────────────────────────────────────────


def test_expression_emits_all_contract_fields(tmp_path: Path) -> None:
    tex = _tex(tmp_path, "We get better coverage.")
    output = "\n".join(expression.analyze(tex, None))

    for field in CONTRACT_FIELDS:
        assert field in output
    assert "% Meaning-Check: NEEDS-LLM" in output
    assert "PRESERVED" not in output


def test_grammar_emits_all_contract_fields(tmp_path: Path) -> None:
    tex = _tex(tmp_path, "We propose method for forecasting.")
    output = "\n".join(grammar.analyze(tex, None))

    for field in CONTRACT_FIELDS:
        assert field in output
    assert "% Meaning-Check: NEEDS-LLM" in output
    assert "PRESERVED" not in output


def test_sentences_emits_all_contract_fields_and_keeps_suggested(tmp_path: Path) -> None:
    long_sentence = (
        "We evaluated our proposed transformer-based architecture across multiple "
        "challenging datasets, including weather forecasting, energy consumption, and "
        "traffic flow, because these tasks required careful hyperparameter tuning, "
        "although the extensive computational resources needed to achieve consistently "
        "strong and reproducible results across all evaluated settings and conditions "
        "when compared against baselines were substantial."
    )
    tex = _tex(tmp_path, long_sentence)
    output = "\n".join(sentences.analyze(tex, None, 50, 3))

    for field in CONTRACT_FIELDS:
        assert field in output
    assert "% Suggested:" in output, "the field name must stay Suggested:"
    assert "% Meaning-Check: NEEDS-LLM" in output
    assert "PRESERVED" not in output


def test_translation_report_carries_the_contract_block() -> None:
    report = translate.translate("本文提出了一种用于时间序列预测的模型。", "deep-learning")

    assert "### Contract" in report
    for field in ("Changed:", "Protected:", "Meaning-Check:", "Risk-Flags:"):
        assert field in report
    assert "Meaning-Check: NEEDS-LLM" in report
    assert "PRESERVED" not in report


# ── Edit axes ────────────────────────────────────────────────────────────────


def test_contract_header_records_the_declared_envelope(tmp_path: Path) -> None:
    tex = _tex(tmp_path, "We get better coverage.")
    output = "\n".join(expression.analyze(tex, None, "clarity", "moderate"))

    assert "% CONTRACT [Script]: goal=clarity strength=moderate" in output


def test_unsupported_goal_routes_instead_of_reporting_nothing(tmp_path: Path) -> None:
    tex = _tex(tmp_path, "We get better coverage.")
    output = "\n".join(expression.analyze(tex, None, "coherence", "minimal"))

    assert "`logic` module instead" in output
    assert "Improve academic tone" not in output


def test_minimal_strength_marks_the_split_as_out_of_envelope(tmp_path: Path) -> None:
    long_sentence = (
        "We evaluated our proposed transformer-based architecture across multiple "
        "challenging datasets, including weather forecasting, energy consumption, and "
        "traffic flow, because these tasks required careful hyperparameter tuning, "
        "although the extensive computational resources needed to achieve consistently "
        "strong and reproducible results across all evaluated settings and conditions "
        "when compared against baselines were substantial."
    )
    tex = _tex(tmp_path, long_sentence)

    minimal = "\n".join(sentences.analyze(tex, None, 50, 3, "grammar", "minimal"))
    moderate = "\n".join(sentences.analyze(tex, None, 50, 3, "grammar", "moderate"))

    assert "--strength moderate or higher" in minimal
    assert "--strength moderate or higher" not in moderate
    assert "% Suggested:" in minimal and "% Suggested:" in moderate


# ── E15 guard: the removed replacements must stay removed ────────────────────


def test_e15_removals_are_not_restored() -> None:
    assert not any("employ" in value for value in expression.WEAK_VERBS.values())
    assert not any("demonstrate" in value for value in expression.WEAK_VERBS.values())


def test_typst_copies_stay_byte_identical() -> None:
    for name in ("improve_expression.py", "analyze_grammar.py", "analyze_sentences.py"):
        en = (SCRIPT_DIR_EN / name).read_bytes().replace(b"\r\n", b"\n")
        typst = (SCRIPT_DIR_TYPST / name).read_bytes().replace(b"\r\n", b"\n")
        assert en == typst, f"{name} drifted between latex-paper-en and typst-paper"
