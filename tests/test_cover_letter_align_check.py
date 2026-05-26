"""End-to-end test: align-check fixture letter against fixture manuscript."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

from conftest import SCRIPT_DIR_COVER_LETTER

SKILL_ROOT = SCRIPT_DIR_COVER_LETTER.parent
FIXTURES = SKILL_ROOT / "evals" / "fixtures"


def _load(module_name: str) -> ModuleType:
    path = SCRIPT_DIR_COVER_LETTER / f"{module_name}.py"
    if str(SCRIPT_DIR_COVER_LETTER) in sys.path:
        sys.path.remove(str(SCRIPT_DIR_COVER_LETTER))
    sys.path.insert(0, str(SCRIPT_DIR_COVER_LETTER))
    spec = importlib.util.spec_from_file_location(f"_cl_ac_{module_name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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


def test_align_check_works_with_aligned_letter() -> None:
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
    tmp = Path(SKILL_ROOT / "evals" / "fixtures" / "_tmp_aligned.md")
    tmp.write_text(aligned, encoding="utf-8")
    try:
        issues, _ = align.run_align_check(tmp, FIXTURES / "generate_fixture.tex")
        # At most minor-severity issues; no major overclaim.
        severities = {issue.severity for issue in issues}
        assert "major" not in severities
    finally:
        tmp.unlink()


def test_align_check_does_not_report_manuscript_supported_observed_metrics() -> None:
    align = _load("align_check")
    aligned = (
        "Dear Editor,\n\n"
        "On the SWaT-Stream benchmark, ALAI reduces inference latency by 47% with no "
        "F1 degradation. On WADI-Stream, ALAI matches the F1 of the strongest baseline "
        "while running 2.1x faster.\n\n"
        "Sincerely,\nJia Wei\n"
    )
    tmp = Path(SKILL_ROOT / "evals" / "fixtures" / "_tmp_metrics_aligned.md")
    tmp.write_text(aligned, encoding="utf-8")
    try:
        issues, claim_map = align.run_align_check(tmp, FIXTURES / "generate_fixture.tex")
        claims_by_text = {
            candidate["claim"]: candidate for candidate in claim_map["claim_candidates"]
        }
        assert any("47%" in claim for claim in claims_by_text)
        assert any("2.1x" in claim for claim in claims_by_text)
        assert not issues
    finally:
        tmp.unlink()


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
