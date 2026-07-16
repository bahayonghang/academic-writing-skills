"""Tests for cover-letter journal-fit scoring (A-CL-1 / A-CL-5 / A-CL-6 / A-CL-10)."""

from __future__ import annotations

import importlib.util
import sys
from types import ModuleType

from tests.support.paths import SCRIPT_DIR_COVER_LETTER

SKILL_ROOT = SCRIPT_DIR_COVER_LETTER.parent
FIXTURES = SKILL_ROOT / "evals" / "fixtures"

_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load(module_name: str) -> ModuleType:
    path = SCRIPT_DIR_COVER_LETTER / f"{module_name}.py"
    saved_path = list(sys.path)
    saved_modules = {name: sys.modules.pop(name, None) for name in _SHARED_MODULE_NAMES}
    try:
        sys.path.insert(0, str(SCRIPT_DIR_COVER_LETTER))
        spec = importlib.util.spec_from_file_location(f"_cl_jf_{module_name}", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, mod in saved_modules.items():
            if mod is not None:
                sys.modules[name] = mod
            else:
                sys.modules.pop(name, None)


def test_load_guard_journal_fit_check_module() -> None:
    """Loader sanity: must load the cover-letter copy, not some other skill's."""
    jf = _load("journal_fit_check")
    assert hasattr(jf, "TIER_BUDGETS")


# --- A-CL-1: _count_claims reuses build_letter_claim_map.extract_claims -----


def test_evidence_density_calibrated_journal_fit_fixture_nature() -> None:
    """journal_fit_fixture_letter.md has 2 claim-bearing sentences under the
    shared extractor ('We report ALAI...' + the 47%/2.1x sentence), which
    falls inside Nature's top-journal budget [2, 5] -> HIGH (was a false LOW
    under the old first-person-only counter)."""
    jf = _load("journal_fit_check")
    result = jf.run_journal_fit(FIXTURES / "journal_fit_fixture_letter.md", "nature", SKILL_ROOT)
    axes = {axis.axis: axis.verdict for axis in result.axes}
    assert axes["evidence_density"] == "HIGH"


def test_evidence_density_calibrated_align_check_fixture_ieee_trans() -> None:
    """align_check_fixture_letter.md has 5 claim-bearing sentences, inside
    ieee-trans's mid-journal budget [3, 6] -> HIGH."""
    jf = _load("journal_fit_check")
    result = jf.run_journal_fit(
        FIXTURES / "align_check_fixture_letter.md", "ieee-trans", SKILL_ROOT
    )
    axes = {axis.axis: axis.verdict for axis in result.axes}
    assert axes["evidence_density"] == "HIGH"


def test_evidence_density_counts_non_first_person_claim_sentences(tmp_path) -> None:
    """4 claim-bearing sentences that never use the old 'we report/present/...'
    trigger must not undercount to a false LOW."""
    jf = _load("journal_fit_check")
    letter = tmp_path / "varied_claims.md"
    letter.write_text(
        "Dear Editor,\n\n"
        "Our method improves accuracy by 5% on Bench-1. "
        "This work reports a new benchmark suite for streaming detection. "
        "The main contribution is a lightweight gating module for streaming inference. "
        "A 30% reduction in latency was observed across all benchmarks.\n\n"
        "Sincerely,\nA. Author\n",
        encoding="utf-8",
    )
    result = jf.run_journal_fit(letter, "generic", SKILL_ROOT)
    axes = {axis.axis: axis.verdict for axis in result.axes}
    assert axes["evidence_density"] != "LOW"


def test_evidence_density_zero_claims_stays_low(tmp_path) -> None:
    """A letter with no claim-bearing sentences at all must still be LOW."""
    jf = _load("journal_fit_check")
    empty_letter = tmp_path / "empty_claims.md"
    empty_letter.write_text(
        "Dear Editor,\n\n"
        "We hope this finds you well. Thank you for your consideration.\n\n"
        "Sincerely,\nA. Author\n",
        encoding="utf-8",
    )
    result = jf.run_journal_fit(empty_letter, "generic", SKILL_ROOT)
    axes = {axis.axis: axis.verdict for axis in result.axes}
    assert axes["evidence_density"] == "LOW"


# --- A-CL-6: top-journal scope_fit 1-hit=HIGH + paradigm double-count fix ---


def test_scope_fit_low_for_fixture_letter_zero_hits() -> None:
    jf = _load("journal_fit_check")
    result = jf.run_journal_fit(FIXTURES / "journal_fit_fixture_letter.md", "nature", SKILL_ROOT)
    axes = {axis.axis: axis.verdict for axis in result.axes}
    assert axes["scope_fit"] == "LOW"


def test_scope_fit_top_journal_one_hit_is_high(tmp_path) -> None:
    jf = _load("journal_fit_check")
    base = (FIXTURES / "journal_fit_fixture_letter.md").read_text(encoding="utf-8")
    augmented = base.replace(
        "Sincerely,",
        "This result should interest the broader field.\n\nSincerely,",
    )
    letter = tmp_path / "augmented_nature_letter.md"
    letter.write_text(augmented, encoding="utf-8")
    result = jf.run_journal_fit(letter, "nature", SKILL_ROOT)
    axes = {axis.axis: axis.verdict for axis in result.axes}
    assert axes["scope_fit"] == "HIGH"


def test_scope_fit_mid_tier_one_hit_stays_medium() -> None:
    """ieee-trans is not top-journal, so its 1-hit case ('...pattern recognition
    systems.' matches the 'system' keyword) must keep the original 2-hit-for-HIGH
    rule -> MEDIUM, unaffected by the top-journal calibration."""
    jf = _load("journal_fit_check")
    result = jf.run_journal_fit(
        FIXTURES / "align_check_fixture_letter.md", "ieee-trans", SKILL_ROOT
    )
    axes = {axis.axis: axis.verdict for axis in result.axes}
    assert axes["scope_fit"] == "MEDIUM"


def test_broad_scientific_no_longer_double_counts_as_novelty_paradigm_signal(tmp_path) -> None:
    """'broad scientific' is a scope keyword, not a paradigm-shift verb; it must
    no longer inflate novelty_framing's paradigm_signals count (original audit
    finding 8). One real paradigm word ('resolve') alone is not enough for
    top-journal HIGH."""
    jf = _load("journal_fit_check")
    letter = tmp_path / "paradigm_letter.md"
    letter.write_text(
        "Dear Editor,\n\n"
        "Our work aims to resolve a long-standing question of broad scientific "
        "interest to the field.\n\n"
        "Sincerely,\nA. Author\n",
        encoding="utf-8",
    )
    result = jf.run_journal_fit(letter, "nature", SKILL_ROOT)
    axes = {axis.axis: axis.verdict for axis in result.axes}
    assert axes["novelty_framing"] == "MEDIUM"


# --- A-CL-5: --dedup-length lets journal-fit skip its own length axis ------


def test_dedup_length_flag_skips_length_axis_but_keeps_banned_phrases(tmp_path) -> None:
    jf = _load("journal_fit_check")
    long_letter = tmp_path / "long_letter.md"
    body = "We demonstrate a strong result. " * 100  # well past Nature's 350-word ceiling
    long_letter.write_text(
        f"Dear Editor,\n\n{body}\nThis is groundbreaking work.\n\nSincerely,\nA. Author\n",
        encoding="utf-8",
    )

    default_result = jf.run_journal_fit(long_letter, "nature", SKILL_ROOT)
    default_format = next(a for a in default_result.axes if a.axis == "format_compliance")
    assert default_format.verdict == "LOW"
    assert any("words" in ev.lower() for ev in default_format.evidence)

    dedup_result = jf.run_journal_fit(long_letter, "nature", SKILL_ROOT, dedup_length=True)
    dedup_format = next(a for a in dedup_result.axes if a.axis == "format_compliance")
    assert not any("words" in ev.lower() for ev in dedup_format.evidence)
    assert any("banned phrase" in ev.lower() for ev in dedup_format.evidence)


def test_dedup_length_default_false_is_unchanged_behavior(tmp_path) -> None:
    """Omitting `dedup_length` (default False) must be identical to calling it
    explicitly False — no behavior change unless the flag is passed."""
    jf = _load("journal_fit_check")
    long_letter = tmp_path / "long_letter2.md"
    body = "We demonstrate a strong result. " * 100
    long_letter.write_text(f"Dear Editor,\n\n{body}\n\nSincerely,\nA. Author\n", encoding="utf-8")
    implicit = jf.run_journal_fit(long_letter, "nature", SKILL_ROOT)
    explicit = jf.run_journal_fit(long_letter, "nature", SKILL_ROOT, dedup_length=False)
    implicit_format = next(a for a in implicit.axes if a.axis == "format_compliance")
    explicit_format = next(a for a in explicit.axes if a.axis == "format_compliance")
    assert implicit_format.verdict == explicit_format.verdict == "LOW"
    assert implicit_format.evidence == explicit_format.evidence


# --- A-CL-10: custom template missing `tier` emits a warning ---------------


def test_journal_fit_warns_when_custom_template_lacks_tier(tmp_path) -> None:
    jf = _load("journal_fit_check")
    skill_dir = tmp_path / "skill"
    templates_dir = skill_dir / "templates"
    templates_dir.mkdir(parents=True)
    (templates_dir / "customvenue.md").write_text(
        "---\n"
        "venue: Custom Venue\n"
        "word_limit: 400\n"
        "required_declarations:\n"
        "  - originality\n"
        "---\n\n# Custom Venue\n",
        encoding="utf-8",
    )
    letter = tmp_path / "letter.md"
    letter.write_text(
        "Dear Editor,\n\nWe report a strong result.\n\nSincerely,\nA. Author\n",
        encoding="utf-8",
    )
    result = jf.run_journal_fit(letter, "customvenue", skill_dir)
    assert result.tier == "mid-journal"
    assert result.warnings
    assert any("tier" in w.lower() for w in result.warnings)


def test_journal_fit_no_warnings_for_builtin_nature_template() -> None:
    jf = _load("journal_fit_check")
    result = jf.run_journal_fit(FIXTURES / "journal_fit_fixture_letter.md", "nature", SKILL_ROOT)
    assert result.warnings == []
