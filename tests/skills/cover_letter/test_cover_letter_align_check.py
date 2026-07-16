"""End-to-end test: align-check fixture letter against fixture manuscript."""

from __future__ import annotations

import importlib.util
import json
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


def test_claim_offsets_drive_source_section_and_json_output(tmp_path, capsys) -> None:
    align = _load("align_check")
    letter = tmp_path / "letter.md"
    letter.write_text(
        "Dear Editor,\n\n"
        "We report a 47% reduction in latency on Bench-X.\n\n"
        "Our work demonstrates a 5 GB memory reduction on Bench-Y.\n\n"
        "Sincerely,\nA. Author\n",
        encoding="utf-8",
    )
    manuscript = tmp_path / "paper.tex"
    manuscript.write_text(
        r"\title{Unrelated Study}\begin{abstract}No matching metrics appear here.\end{abstract}",
        encoding="utf-8",
    )

    issues, claim_map = align.run_align_check(letter, manuscript)
    candidates = claim_map["claim_candidates"]
    assert candidates and all(candidate["char_offset"] >= 0 for candidate in candidates)
    issues_by_quote = {
        issue.quote: issue for issue in issues if issue.comment_type == "claim_accuracy"
    }
    opening = next(claim for claim in candidates if "47%" in claim["claim"])
    body = next(claim for claim in candidates if "5 GB" in claim["claim"])
    assert issues_by_quote[opening["claim"]].source_section == "opening"
    assert issues_by_quote[body["claim"]].source_section == "body"
    assert {issue.source_section for issue in issues} <= {
        "header",
        "opening",
        "body",
        "contributions",
        "fit",
        "declarations",
        "closing",
    }

    code = align.main(["--letter", str(letter), "--manuscript", str(manuscript), "--json"])
    assert code in {1, 2}
    payload = json.loads(capsys.readouterr().out)
    claim_issues = [item for item in payload if item["comment_type"] == "claim_accuracy"]
    assert claim_issues and all(item["char_offset"] >= 0 for item in claim_issues)


def test_candidate_to_issue_without_letter_text_falls_back_to_body() -> None:
    align = _load("align_check")
    candidate = {
        "claim": "Our work demonstrates a 5 GB memory reduction.",
        "claim_strength": "unsupported",
        "confidence": "unverified",
        "evidence_anchor": [],
        "missing_evidence": ["matching manuscript evidence"],
        "allowed_wording": "",
        "forbidden_wording": [],
        "quote_verified": False,
        "char_offset": -1,
    }
    issue = align.candidate_to_issue(candidate, {})
    assert issue is not None
    assert issue.source_section == "body"
    assert issue.char_offset == -1


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


# --- CL-4: AI-disclosure consistency lane -----------------------------------

_MS_DISCLOSES = r"""\documentclass{article}
\title{Widget Study}
\begin{document}
\begin{abstract}
We study widgets and report a 5\% gain over the baseline.
\end{abstract}
\section{Acknowledgments}
The authors used a large language model (ChatGPT) to polish the grammar.
\end{document}
"""

_MS_DENIES = r"""\documentclass{article}
\title{Widget Study}
\begin{document}
\begin{abstract}
We study widgets. The authors did not use any generative AI in this work.
\end{abstract}
\end{document}
"""

_MS_SILENT = r"""\documentclass{article}
\title{Widget Study}
\begin{document}
\begin{abstract}
We study widgets and report a 5\% gain over the baseline.
\end{abstract}
\end{document}
"""

_LETTER_SILENT = (
    "Dear Editor,\n\nWe submit our widget study. It reports a 5% gain.\n\nSincerely,\nA. Author\n"
)
_LETTER_DISCLOSES = (
    "Dear Editor,\n\nWe submit our widget study. We used a large language model (GPT-4) "
    "to polish the grammar.\n\nSincerely,\nA. Author\n"
)


def _disclosure_findings(align, letter_text: str, manuscript_text: str, tmp_path):
    letter = tmp_path / "letter.md"
    letter.write_text(letter_text, encoding="utf-8")
    manuscript = tmp_path / "paper.tex"
    manuscript.write_text(manuscript_text, encoding="utf-8")
    issues, _ = align.run_align_check(letter, manuscript)
    return [i for i in issues if i.comment_type == "disclosure_consistency"]


def test_align_check_flags_manuscript_discloses_letter_silent(tmp_path) -> None:
    """CL-4 case 1: manuscript discloses AI use, cover letter is silent."""
    align = _load("align_check")
    disc = _disclosure_findings(align, _LETTER_SILENT, _MS_DISCLOSES, tmp_path)
    assert len(disc) == 1
    issue = disc[0]
    assert issue.severity == "moderate"
    assert issue.priority == "P2"
    assert issue.source_kind == "script"
    assert issue.quote == ""  # nothing to quote from the silent letter — that is the gap
    assert issue.quote_verified is False
    assert issue.evidence_anchor and "ChatGPT" in issue.evidence_anchor[0]["text"]
    # ISSUE_SCHEMA required seven fields must all be present and populated.
    for field in ("title", "quote", "explanation", "comment_type", "severity", "source_kind"):
        assert hasattr(issue, field)
    assert issue.explanation


def test_align_check_flags_letter_discloses_manuscript_silent(tmp_path) -> None:
    """CL-4 case 2: cover letter discloses AI use, manuscript is silent."""
    align = _load("align_check")
    disc = _disclosure_findings(align, _LETTER_DISCLOSES, _MS_SILENT, tmp_path)
    assert len(disc) == 1
    issue = disc[0]
    assert issue.severity == "moderate"
    assert "large language model" in issue.quote.lower()
    assert issue.quote_verified is True
    assert issue.evidence_anchor and issue.evidence_anchor[0]["type"] == "missing"


def test_align_check_flags_disclosure_polarity_contradiction(tmp_path) -> None:
    """CL-4 case 3: letter affirms AI use while the manuscript denies it."""
    align = _load("align_check")
    disc = _disclosure_findings(align, _LETTER_DISCLOSES, _MS_DENIES, tmp_path)
    assert len(disc) == 1
    issue = disc[0]
    assert issue.severity == "moderate"
    assert "large language model" in issue.quote.lower()
    assert issue.evidence_anchor and "did not use" in issue.evidence_anchor[0]["text"].lower()


def test_align_check_consistent_disclosure_no_finding(tmp_path) -> None:
    """Both sides disclose AI use with the same polarity → no disclosure finding."""
    align = _load("align_check")
    disc = _disclosure_findings(align, _LETTER_DISCLOSES, _MS_DISCLOSES, tmp_path)
    assert disc == []


def test_align_check_both_silent_no_disclosure_finding(tmp_path) -> None:
    """Neither side mentions AI → nothing to reconcile in this lane."""
    align = _load("align_check")
    disc = _disclosure_findings(align, _LETTER_SILENT, _MS_SILENT, tmp_path)
    assert disc == []


def test_align_check_commented_manuscript_disclosure_not_flagged(tmp_path) -> None:
    """A commented-out manuscript disclosure (% ...) must not count as present."""
    align = _load("align_check")
    commented = (
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "\\begin{abstract}\n"
        "We study widgets.\n"
        "\\end{abstract}\n"
        "% The authors used a large language model (ChatGPT) to polish the grammar.\n"
        "\\end{document}\n"
    )
    disc = _disclosure_findings(align, _LETTER_SILENT, commented, tmp_path)
    assert disc == []


# --- A-CL-2: .tex letter claim pipeline strips % comments -------------------


def test_align_check_tex_letter_comment_does_not_produce_claim(tmp_path) -> None:
    """A commented-out `.tex` letter line must not surface as a claim
    candidate, while an active line with an escaped `47\\%` still does."""
    align = _load("align_check")
    letter = tmp_path / "letter.tex"
    letter.write_text(
        "Dear Editor,\n\n"
        "% Our work demonstrates a 99\\% reduction in latency on Bench-9.\n"
        "We report a 47\\% reduction in latency on Bench-1.\n",
        encoding="utf-8",
    )
    _, claim_map = align.run_align_check(letter, FIXTURES / "generate_fixture.tex")
    claims = [c["claim"] for c in claim_map["claim_candidates"]]
    assert not any("99" in claim for claim in claims), "commented-out claim must not surface"
    assert any("47" in claim for claim in claims), "active escaped claim must survive"


def test_align_check_md_letter_percent_claim_extraction_unaffected(tmp_path) -> None:
    """A-CL-2 control: `.md` letters are never comment-stripped (`%` there is
    prose, e.g. "47% reduction") — behavior must be unchanged by the fix."""
    align = _load("align_check")
    letter = tmp_path / "letter.md"
    letter.write_text(
        "Dear Editor,\n\nOur work demonstrates a 47% reduction in latency on Bench-1.\n",
        encoding="utf-8",
    )
    _, claim_map = align.run_align_check(letter, FIXTURES / "generate_fixture.tex")
    claims = [c["claim"] for c in claim_map["claim_candidates"]]
    assert any("47" in claim for claim in claims)


# --- A-CL-4: direction-only numeric verification needs a tight window -------


def test_direction_only_numeric_match_requires_tight_window() -> None:
    """A direction-only claim (reduction/improvement, no specific metric
    keyword) must require the direction word within `_DIRECTION_WINDOW` (60
    chars) of the number in the manuscript, not the old 160-char loose gate."""
    verifier = _load("verify_letter_against_manuscript")
    # "improvement" sits ~142 chars from "30%", describing an unrelated
    # subsystem — inside the old 160-char loose window (used to falsely
    # verify) but outside the new 60-char direction window.
    manuscript = (
        "We measured a 30% change in an unrelated subsystem metric today. "
        "This sentence is only here as neutral padding text to add some length. "
        "A completely different improvement occurred in another subsystem entirely."
    )
    assert (
        verifier._has_numeric_match("achieves a 30% improvement over baseline", manuscript) is False
    )
    # Sanity: the CL-1 pinned direction-only case (distance ~1 char) still verifies.
    assert verifier._has_numeric_match("47% reduction", "we report a 47% reduction in latency")
