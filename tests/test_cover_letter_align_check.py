"""End-to-end test: align-check fixture letter against fixture manuscript."""

from __future__ import annotations

import importlib.util
import sys
from types import ModuleType

from conftest import SCRIPT_DIR_COVER_LETTER

SKILL_ROOT = SCRIPT_DIR_COVER_LETTER.parent
FIXTURES = SKILL_ROOT / "evals" / "fixtures"

_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load(module_name: str) -> ModuleType:
    path = SCRIPT_DIR_COVER_LETTER / f"{module_name}.py"
    saved_path = list(sys.path)
    saved_modules = {name: sys.modules.pop(name, None) for name in _SHARED_MODULE_NAMES}
    try:
        sys.path.insert(0, str(SCRIPT_DIR_COVER_LETTER))
        spec = importlib.util.spec_from_file_location(f"_cl_ac_{module_name}", path)
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


def test_align_check_run_pipeline_emits_unsupported_claim() -> None:
    align = _load("align_check")
    issues, claim_map = align.run_align_check(
        FIXTURES / "align_check_fixture_letter.md",
        FIXTURES / "generate_fixture.tex",
    )
    # The fixture letter overshoots with: $1.2M cost savings, 12 sensor
    # modalities, 73% memory reduction — none of which the manuscript supports.
    assert issues, "expected at least one unsupported claim issue"
    overclaim_titles = [issue.title for issue in issues]
    assert all("claim" in title.lower() or "support" in title.lower() for title in overclaim_titles)
    # The claim map must contain at least one strong-wording overclaim candidate.
    candidates = claim_map.get("claim_candidates", [])
    assert any(c.get("claim_strength") in {"unsupported", "observed"} for c in candidates)


def test_align_check_issue_schema_has_required_fields() -> None:
    align = _load("align_check")
    issues, _ = align.run_align_check(
        FIXTURES / "align_check_fixture_letter.md",
        FIXTURES / "generate_fixture.tex",
    )
    assert issues
    required = {
        "title",
        "quote",
        "explanation",
        "comment_type",
        "severity",
        "priority",
        "source_kind",
    }
    for issue in issues:
        as_dict = issue.__dict__
        missing = required - set(as_dict)
        assert not missing, f"issue missing fields {missing}: {as_dict}"


def test_align_check_severity_classification_caps_at_major() -> None:
    align = _load("align_check")
    issues, _ = align.run_align_check(
        FIXTURES / "align_check_fixture_letter.md",
        FIXTURES / "generate_fixture.tex",
    )
    severities = {issue.severity for issue in issues}
    assert severities <= {"major", "moderate", "minor"}


def test_align_check_works_with_aligned_letter(tmp_path) -> None:
    """A letter that does not overclaim should produce few or no issues."""
    align = _load("align_check")
    # Synthesize an aligned letter inline: only claims that trace to manuscript.
    aligned = (
        "Dear Editor,\n\n"
        "We submit our manuscript on adaptive latency-aware inference for streaming "
        "anomaly detection. On the SWaT-Stream benchmark, our framework reduces "
        "inference latency by 47% with no F1 degradation.\n\n"
        "Sincerely,\nJia Wei\n"
    )
    tmp = tmp_path / "_tmp_aligned.md"
    tmp.write_text(aligned, encoding="utf-8")
    issues, _ = align.run_align_check(tmp, FIXTURES / "generate_fixture.tex")
    # At most minor-severity issues; no major overclaim.
    severities = {issue.severity for issue in issues}
    assert "major" not in severities


def test_align_check_does_not_report_manuscript_supported_observed_metrics(tmp_path) -> None:
    align = _load("align_check")
    aligned = (
        "Dear Editor,\n\n"
        "On the SWaT-Stream benchmark, ALAI reduces inference latency by 47% with no "
        "F1 degradation. On WADI-Stream, ALAI matches the F1 of the strongest baseline "
        "while running 2.1x faster.\n\n"
        "Sincerely,\nJia Wei\n"
    )
    tmp = tmp_path / "_tmp_metrics_aligned.md"
    tmp.write_text(aligned, encoding="utf-8")
    issues, claim_map = align.run_align_check(tmp, FIXTURES / "generate_fixture.tex")
    claims_by_text = {candidate["claim"]: candidate for candidate in claim_map["claim_candidates"]}
    assert any("47%" in claim for claim in claims_by_text)
    assert any("2.1x" in claim for claim in claims_by_text)
    assert not issues


def test_align_check_reports_memory_modality_and_deployment_overclaims() -> None:
    align = _load("align_check")
    issues, claim_map = align.run_align_check(
        FIXTURES / "align_check_fixture_letter.md",
        FIXTURES / "generate_fixture.tex",
    )
    claims = [candidate["claim"] for candidate in claim_map["claim_candidates"]]
    assert any("73% reduction in memory footprint" in claim for claim in claims)
    assert any("12 sensor modalities" in claim for claim in claims)
    assert any("deployed in three industrial pilot studies" in claim for claim in claims)

    issue_quotes = [issue.quote for issue in issues]
    assert any("73% reduction in memory footprint" in quote for quote in issue_quotes)
    assert any("deployed in three industrial pilot studies" in quote for quote in issue_quotes)
    assert all(issue.priority in {"P1", "P2", "P3"} for issue in issues)
    assert all(issue.source_kind == "script" for issue in issues)


def test_align_check_assembles_multifile_manuscript(tmp_path) -> None:
    """A main.tex \\input skeleton must be assembled before anchoring claims, so
    genuinely-supported 47% / 2.1x claims are not all mis-reported (C3)."""
    align = _load("align_check")
    extract = _load("extract_manuscript_facts")
    main_tex = FIXTURES / "multifile" / "main.tex"

    # Facts come from the assembled body, not the near-empty skeleton.
    facts = extract.extract_facts(extract.load_manuscript_text(main_tex))
    assert facts["abstract"].startswith("We address anomaly detection")
    assert any("47%" in n for n in facts["headline_numbers"])

    letter = tmp_path / "aligned_letter.md"
    letter.write_text(
        "Dear Editor,\n\n"
        "On SWaT-Stream, our framework reduces inference latency by 47% with no F1 "
        "degradation, and on WADI-Stream it runs 2.1x faster than the strongest "
        "baseline.\n\n"
        "Sincerely,\nJia Wei\n",
        encoding="utf-8",
    )
    issues, _ = align.run_align_check(letter, main_tex)
    # Both claims trace to the assembled manuscript → no overclaim findings.
    assert "major" not in {issue.severity for issue in issues}
    assert not issues


def test_align_check_numeric_match_requires_local_cooccurrence(tmp_path) -> None:
    """A number and its metric keyword that live far apart in the manuscript must
    not 'verify' a fabricated combination (C4)."""
    verifier = _load("verify_letter_against_manuscript")
    # "73%" appears, and "reduction" appears, but separated by >window chars and
    # never describing memory.
    manuscript = (
        r"\begin{abstract}"
        "Industrial monitoring is hard. "
        * 8
        + "About 73% of sites lack monitoring. "
        + "Unrelated filler sentence here. " * 8
        + "We also observe a latency reduction on one benchmark."
        r"\end{abstract}"
    )
    assert verifier._has_numeric_match("73% reduction in memory footprint", manuscript) is False
    # Sanity: a genuinely co-located number+keyword still verifies.
    assert verifier._has_numeric_match("47% reduction", "we report a 47% reduction in latency")


def test_numeric_match_rejects_metric_swap() -> None:
    """The letter cannot re-attach a manuscript number to a different metric
    (CL-1): the specific metric word next to the number must match too."""
    verifier = _load("verify_letter_against_manuscript")
    manuscript = r"We evaluate the system and measure a 3\% accuracy improvement over the baseline."
    # Same number, different metric identity -> no verification.
    assert verifier._has_numeric_match("3% throughput improvement", manuscript) is False
    # Matching metric identity still verifies.
    assert verifier._has_numeric_match("3% accuracy improvement", manuscript) is True
    # Direction-only claims keep the original any-co-occurrence gate (C4 sanity).
    assert verifier._has_numeric_match("47% reduction", "we report a 47% reduction in latency")


def test_align_check_metric_swap_yields_unverified_and_finding(tmp_path) -> None:
    """End-to-end CL-1: '3% throughput improvement' against a manuscript that
    only supports '3% accuracy improvement' must be unverified and flagged."""
    align = _load("align_check")
    manuscript = tmp_path / "paper.tex"
    manuscript.write_text(
        "\\documentclass{article}\n"
        "\\title{Widget Forecasting}\n"
        "\\begin{document}\n"
        "\\begin{abstract}\n"
        "We evaluate the proposed system and measure a 3\\% accuracy improvement\n"
        "over the strongest baseline.\n"
        "\\end{abstract}\n"
        "\\section{Results}\n"
        "The 3\\% accuracy improvement holds across all seeds.\n"
        "\\end{document}\n",
        encoding="utf-8",
    )

    swapped = tmp_path / "swapped_letter.md"
    swapped.write_text(
        "Dear Editor,\n\n"
        "Our framework delivers a 3% throughput improvement in production settings.\n\n"
        "Sincerely,\nJia Wei\n",
        encoding="utf-8",
    )
    issues, claim_map = align.run_align_check(swapped, manuscript)
    swap_candidates = [c for c in claim_map["claim_candidates"] if "throughput" in c["claim"]]
    assert swap_candidates, "the swapped-metric sentence must be a claim candidate"
    assert all(not c["quote_verified"] for c in swap_candidates)
    assert all(not c.get("manuscript_supported") for c in swap_candidates)
    # The aggregate must track the cleared flags, not the pre-verify values.
    assert claim_map["manuscript_supported_count"] == sum(
        1 for c in claim_map["claim_candidates"] if c.get("manuscript_supported")
    )
    assert any("throughput" in issue.quote for issue in issues), (
        "metric-swapped claim must produce an align-check finding"
    )

    # Positive control: the same sentence with the *matching* metric verifies
    # and produces no finding — the fix must not over-tighten.
    aligned = tmp_path / "aligned_letter.md"
    aligned.write_text(
        "Dear Editor,\n\n"
        "Our framework delivers a 3% accuracy improvement in production settings.\n\n"
        "Sincerely,\nJia Wei\n",
        encoding="utf-8",
    )
    issues_ok, claim_map_ok = align.run_align_check(aligned, manuscript)
    ok_candidates = [c for c in claim_map_ok["claim_candidates"] if "accuracy" in c["claim"]]
    assert ok_candidates and all(c["quote_verified"] for c in ok_candidates)
    assert not any("accuracy improvement" in issue.quote for issue in issues_ok)


def test_split_sentences_strips_salutation() -> None:
    """CL-2: 'Dear Editor,' must not glue itself onto the first claim quote."""
    builder = _load("build_letter_claim_map")
    sentences = builder.split_sentences(
        "Dear Editor,\n\nWe propose FrameX for anomaly detection. It reduces cost."
    )
    assert sentences[0] == "We propose FrameX for anomaly detection."

    claim_map = builder.build_claim_map(
        "Dear Prof. Smith,\n\nOur method improves accuracy by 4% on Bench-1.\n",
        manuscript_facts=None,
    )
    assert claim_map["claim_candidates"], "claim sentence must still be detected"
    for candidate in claim_map["claim_candidates"]:
        assert not candidate["claim"].startswith("Dear")
