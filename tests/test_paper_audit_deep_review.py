"""Tests for paper-audit deep-review-first additions."""

import json
import re
from pathlib import Path

from report_generator import (
    AuditResult,
    DeepReviewIssue,
    coerce_deep_review_issue,
    normalize_deep_review_issue_dict,
    render_deep_review_report,
    render_json_report,
    render_report,
)


def test_normalize_mode_aliases() -> None:
    from audit import normalize_mode

    assert normalize_mode("self-check") == ("quick-audit", "self-check")
    assert normalize_mode("review") == ("deep-review", "review")
    assert normalize_mode("gate") == ("gate", None)


def test_mode_checks_include_new_primary_modes() -> None:
    from audit import MODE_CHECKS

    assert "quick-audit" in MODE_CHECKS
    assert "deep-review" in MODE_CHECKS
    assert "self-check" in MODE_CHECKS
    assert "review" in MODE_CHECKS


def test_deep_review_issue_helpers_normalize_persisted_payload() -> None:
    raw_issue = {
        "title": "Claim outruns evidence",
        "quote": "We achieve state-of-the-art efficiency.",
        "explanation": "The claim is too broad.",
        "comment_type": "claim_accuracy",
        "severity": "major",
        "source_section": "abstract",
        "review_lane": "claims_vs_evidence",
        "quote_verified": True,
        "source_file": "claims_vs_evidence.json",
    }

    issue = coerce_deep_review_issue(raw_issue)

    assert issue.title == raw_issue["title"]
    assert issue.review_lane == "claims_vs_evidence"
    assert issue.quote_verified is True
    assert not hasattr(issue, "source_file")
    assert normalize_deep_review_issue_dict(raw_issue) == issue.to_dict()


def test_render_deep_review_report_groups_issue_bundle() -> None:
    result = AuditResult(
        file_path="paper.tex",
        language="en",
        mode="deep-review",
        mode_alias_used="review",
        issue_bundle=[
            DeepReviewIssue(
                title="Headline claim outruns evidence",
                quote="We achieve state-of-the-art efficiency.",
                explanation="The claim is not supported across all evaluated settings.",
                comment_type="claim_accuracy",
                severity="major",
                source_section="abstract",
                review_lane="claims_vs_evidence",
            ),
            DeepReviewIssue(
                title="Appendix totals do not reconcile",
                quote="Average gain: 12.4",
                explanation="The appendix values average to a different number.",
                comment_type="claim_accuracy",
                severity="moderate",
                source_section="appendix",
                review_lane="notation_and_numeric_consistency",
            ),
        ],
        overall_assessment="Important paper, but the central claim needs recalibration.",
        revision_roadmap=[
            {
                "priority": "Priority 1",
                "title": "Qualify headline claim",
                "source": "[LLM]",
                "section": "abstract",
            }
        ],
    )

    report = render_deep_review_report(result)
    assert "Deep Review Report" in report
    assert "Compatibility Note" in report
    assert "Major Issues" in report
    assert "Moderate Issues" in report
    assert "Revision Roadmap" in report


def test_render_deep_review_report_uses_issue_bundle_recommendation() -> None:
    result = AuditResult(
        file_path="paper.tex",
        language="en",
        mode="deep-review",
        issue_bundle=[
            DeepReviewIssue(
                title="Headline claim outruns evidence",
                quote="We achieve state-of-the-art efficiency.",
                explanation="The claim is too broad for the demonstrated scope.",
                comment_type="claim_accuracy",
                severity="major",
                source_section="abstract",
                review_lane="claims_vs_evidence",
            )
        ],
        overall_assessment="The central claim still needs stronger evidence alignment.",
    )

    report = render_deep_review_report(result)
    assert "Reviewer Recommendation" in report
    assert "Major Revision" in report
    assert "Strong Accept" not in report


def test_render_deep_review_report_embeds_committee_section(tmp_path: Path) -> None:
    committee_dir = tmp_path / "committee"
    committee_dir.mkdir(parents=True, exist_ok=True)
    (committee_dir / "editor.md").write_text("Editor notes go here.", encoding="utf-8")
    (committee_dir / "theory.md").write_text("Theory notes go here.", encoding="utf-8")
    (committee_dir / "consensus.md").write_text("Consensus notes go here.", encoding="utf-8")

    result = AuditResult(
        file_path="paper.tex",
        language="en",
        mode="deep-review",
        issue_bundle=[
            DeepReviewIssue(
                title="Headline claim outruns evidence",
                quote="We achieve state-of-the-art efficiency.",
                explanation="The claim is not supported across all evaluated settings.",
                comment_type="claim_accuracy",
                severity="major",
                source_section="abstract",
                review_lane="claims_vs_evidence",
            ),
        ],
        overall_assessment="Assessment.",
        artifact_dir=str(tmp_path),
    )

    report = render_deep_review_report(result)
    assert "Academic Pre-Review Committee" in report
    assert "Editor notes go here." in report
    assert "Theory notes go here." in report
    assert "Consensus notes go here." in report


def test_render_report_returns_combined_deep_review_summary(tmp_path: Path) -> None:
    result = AuditResult(
        file_path="paper.tex",
        language="en",
        mode="deep-review",
        artifact_dir=str(tmp_path),
        review_focus="methodology",
        issue_bundle=[
            DeepReviewIssue(
                title="Comparison protocol is asymmetric",
                quote="We tune our method over three retries.",
                explanation="The proposed method receives more tuning budget than the baseline.",
                comment_type="methodology",
                severity="major",
                source_section="results",
                review_lane="evaluation_fairness_and_reproducibility",
            )
        ],
        overall_assessment="The paper needs a tighter methodology story before review.",
    )

    report = render_report(result, report_style="peer-review")
    assert "Deep Review Summary" in report
    assert "Primary View" in report
    assert "peer-review" in report
    assert "peer_review_report.md" in report
    assert "review_report.md" in report
    assert "`methodology`" in report


def test_render_json_report_includes_issue_bundle() -> None:
    result = AuditResult(
        file_path="paper.tex",
        language="en",
        mode="deep-review",
        issue_bundle=[
            DeepReviewIssue(
                title="Comparison protocol is asymmetric",
                quote="We tune our method over three retries.",
                explanation="The proposed method gets extra opportunities relative to baselines.",
                comment_type="methodology",
                severity="major",
                source_section="experiment",
            )
        ],
        overall_assessment="Main comparison is not calibrated fairly.",
    )

    payload = json.loads(render_json_report(result))
    assert payload["mode"] == "deep-review"
    assert payload["issue_bundle"][0]["title"] == "Comparison protocol is asymmetric"
    assert payload["overall_assessment"] == "Main comparison is not calibrated fairly."


def test_prepare_review_workspace_creates_expected_artifacts(tmp_path: Path) -> None:
    from prepare_review_workspace import prepare_workspace

    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"""
\title{A Test Paper}
\begin{document}
\begin{abstract}
We show a new method for long-context reasoning.
\end{abstract}
\section{Introduction}
This paper proposes a new method.
\section{Method}
We define x as the main state variable.
\section{Conclusion}
We show strong results.
\end{document}
""".strip(),
        encoding="utf-8",
    )

    workspace = prepare_workspace(str(tex), output_dir=str(tmp_path / "review_results"))
    assert (workspace / "full_text.md").exists()
    assert (workspace / "metadata.json").exists()
    assert (workspace / "section_index.json").exists()
    assert (workspace / "claim_map.json").exists()
    assert (workspace / "paper_summary.md").exists()
    assert (workspace / "committee").exists()
    assert (workspace / "references" / "DEEP_REVIEW_CRITERIA.md").exists()

    section_index = json.loads((workspace / "section_index.json").read_text(encoding="utf-8"))
    assert any(section["section_key"] == "introduction" for section in section_index)


def test_consolidate_review_findings_deduplicates_exact_overlaps() -> None:
    from consolidate_review_findings import consolidate_findings, sanitize_issue

    issues = [
        sanitize_issue(
            {
                "title": "Claim outruns evidence",
                "quote": "We achieve state-of-the-art efficiency.",
                "explanation": "Too broad.",
                "comment_type": "claim_accuracy",
                "severity": "major",
                "source_section": "abstract",
            }
        ),
        sanitize_issue(
            {
                "title": "Claim outruns evidence",
                "quote": "We achieve state-of-the-art efficiency.",
                "explanation": "The claim is too broad for short sequences.",
                "comment_type": "claim_accuracy",
                "severity": "moderate",
                "source_section": "abstract",
            }
        ),
    ]

    consolidated = consolidate_findings(issues)
    assert len(consolidated) == 1
    assert consolidated[0]["severity"] == "major"


def test_verify_quotes_marks_missing_quotes() -> None:
    from verify_quotes import verify_quotes

    issues = [
        {
            "title": "Found",
            "quote": "exact text",
            "explanation": "",
            "comment_type": "presentation",
            "severity": "minor",
            "source_kind": "llm",
        },
        {
            "title": "Missing",
            "quote": "not present",
            "explanation": "",
            "comment_type": "presentation",
            "severity": "minor",
            "source_kind": "llm",
        },
    ]

    updated = verify_quotes("This contains exact text in the body.", issues)
    assert updated[0]["quote_verified"] is True
    assert updated[1]["quote_verified"] is False


def test_run_deep_review_creates_workspace_artifacts_and_issue_bundle(tmp_path: Path) -> None:
    from audit import run_deep_review

    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"""
\title{A Deep Review Test Paper}
\begin{document}
\begin{abstract}
We show state-of-the-art efficiency on long-context reasoning tasks.
\end{abstract}
\section{Introduction}
This paper proposes a novel baseline comparison strategy.
\section{Method}
We define x as the latent state and assume a fixed calibration constant.
\section{Results}
Our method improves accuracy by 12.4 over the baseline.
\section{Appendix}
Table A reports the same metric as 10.1 under a different aggregation rule.
\section{Conclusion}
We conclude that the method is broadly superior.
\end{document}
""".strip(),
        encoding="utf-8",
    )

    result = run_deep_review(str(tex), lang="en")

    artifact_dir = Path(result.artifact_dir)
    assert artifact_dir.exists()
    assert (artifact_dir / "final_issues.json").exists()
    assert (artifact_dir / "all_comments.json").exists()
    assert (artifact_dir / "overall_assessment.txt").exists()
    assert (artifact_dir / "revision_roadmap.md").exists()
    assert (artifact_dir / "phase0_context.md").exists()
    assert (artifact_dir / "review_report.md").exists()
    assert (artifact_dir / "committee" / "consensus.md").exists()
    assert (artifact_dir / "claim_map.json").exists()
    assert (artifact_dir / "section_index.json").exists()
    assert result.issue_bundle
    assert result.revision_roadmap
    assert result.section_index

    payload = json.loads((artifact_dir / "final_issues.json").read_text(encoding="utf-8"))
    first_issue = payload[0]
    assert first_issue["severity"] in {"major", "moderate", "minor"}
    assert first_issue["source_kind"] in {"llm", "script"}
    assert "review_lane" in first_issue
    assert "quote_verified" in first_issue
    assert {
        "title",
        "quote",
        "explanation",
        "comment_type",
        "severity",
        "source_kind",
        "review_lane",
        "root_cause_key",
        "quote_verified",
    }.issubset(first_issue)
    assert any(issue["review_lane"] == "claims_vs_evidence" for issue in payload)
    assert any(
        issue["review_lane"] == "evaluation_fairness_and_reproducibility" for issue in payload
    )
    assert any(issue["review_lane"] == "section_methods" for issue in payload)


def test_compute_committee_score_applies_desk_reject_cap() -> None:
    from audit import _compute_committee_score

    issues = [
        {"severity": "minor"},
        {"severity": "minor"},
    ]
    score_without_cap = _compute_committee_score(issues, "Pass to Review")
    score_with_cap = _compute_committee_score(issues, "Desk Reject")

    assert score_without_cap == 8.6
    assert score_with_cap == 4.0


def test_run_deep_review_caps_score_from_editor_verdict(tmp_path: Path) -> None:
    from audit import _write_committee_consensus

    review_dir = tmp_path / "workspace"
    committee_dir = review_dir / "committee"
    committee_dir.mkdir(parents=True, exist_ok=True)
    (committee_dir / "editor.md").write_text(
        "## Editor Pre-Screen\n\nVerdict: Desk Reject\n",
        encoding="utf-8",
    )
    phase0 = AuditResult(
        file_path="paper.tex",
        language="en",
        mode="quick-audit",
    )
    issues = [
        {"severity": "minor", "title": "Minor issue A", "source_section": "introduction"},
        {"severity": "minor", "title": "Minor issue B", "source_section": "conclusion"},
    ]
    _write_committee_consensus(review_dir, phase0, issues)

    consensus = (committee_dir / "consensus.md").read_text(encoding="utf-8")

    assert "Editor Verdict: Desk Reject" in consensus
    match = re.search(r"Overall Score:\s*([0-9]+(?:\.[0-9]+)?)\/10", consensus)
    assert match is not None
    assert float(match.group(1)) <= 4.0


def test_run_audit_deep_review_dispatches_to_issue_bundle(tmp_path: Path) -> None:
    from audit import run_audit
    from render_deep_review_report import load_result

    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"""
\title{Dispatch Test}
\begin{document}
\begin{abstract}
We show significant gains.
\end{abstract}
\section{Introduction}
This paper compares against a baseline.
\section{Results}
The model improves accuracy by 5.2.
\section{Conclusion}
We conclude the gains are broadly effective.
\end{document}
""".strip(),
        encoding="utf-8",
    )

    result = run_audit(str(tex), mode="deep-review", lang="en")
    reloaded = load_result(Path(result.artifact_dir))

    assert result.mode == "deep-review"
    assert result.issue_bundle
    assert result.artifact_dir
    assert Path(result.artifact_dir, "review_report.md").exists()
    assert [issue.to_dict() for issue in reloaded.issue_bundle] == [
        issue.to_dict() for issue in result.issue_bundle
    ]
    assert reloaded.revision_roadmap == result.revision_roadmap
    assert reloaded.section_index == result.section_index


def test_run_audit_deep_review_focus_methodology_limits_issue_bundle(tmp_path: Path) -> None:
    from audit import run_audit

    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"""
\title{Method Focus Test}
\begin{document}
\begin{abstract}
We show significant gains over prior work.
\end{abstract}
\section{Introduction}
This paper claims broad superiority over prior work.
\section{Method}
We define x as the latent state and assume a fixed calibration constant.
\section{Results}
We tune our method over three retry runs while reporting each baseline once.
\section{Conclusion}
We conclude the method is broadly superior.
\end{document}
""".strip(),
        encoding="utf-8",
    )

    result = run_audit(str(tex), mode="deep-review", focus="methodology", lang="en")
    payload = json.loads(
        (Path(result.artifact_dir) / "final_issues.json").read_text(encoding="utf-8")
    )
    lanes = {issue["review_lane"] for issue in payload}

    assert result.review_focus == "methodology"
    assert lanes
    assert lanes <= {
        "section_methods",
        "section_results",
        "notation_and_numeric_consistency",
        "evaluation_fairness_and_reproducibility",
    }
    assert (Path(result.artifact_dir) / "committee" / "methodology.md").exists()
    assert not (Path(result.artifact_dir) / "committee" / "theory.md").exists()


def test_run_audit_relative_path_does_not_report_missing_existing_file(
    tmp_path: Path,
    monkeypatch,
) -> None:
    from audit import run_audit

    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"""
\title{Relative Path Test}
\begin{document}
\begin{abstract}
We present a short test paper.
\end{abstract}
\section{Introduction}
This paper introduces a bounded method.
\end{document}
""".strip(),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    result = run_audit("paper.tex", mode="quick-audit", lang="en")
    assert not any("File not found" in issue.message for issue in result.issues)


def test_repeated_deep_review_runs_clear_stale_workspace_artifacts(tmp_path: Path) -> None:
    from audit import run_audit

    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"""
\title{Repeat Run Test}
\begin{document}
\begin{abstract}
We show significant gains over prior work.
\end{abstract}
\section{Introduction}
This paper claims broad superiority over prior work.
\section{Method}
We define x as the latent state and assume a fixed calibration constant.
\section{Results}
We tune our method over three retry runs while reporting each baseline once.
\section{Conclusion}
We conclude the method is broadly superior.
\end{document}
""".strip(),
        encoding="utf-8",
    )

    full = run_audit(str(tex), mode="deep-review", focus="full", lang="en")
    assert (Path(full.artifact_dir) / "committee" / "theory.md").exists()

    focused = run_audit(str(tex), mode="deep-review", focus="methodology", lang="en")

    focused_committee = Path(focused.artifact_dir) / "committee" / "theory.md"
    focused_payload = json.loads(
        (Path(focused.artifact_dir) / "final_issues.json").read_text(encoding="utf-8")
    )
    focused_lanes = {issue["review_lane"] for issue in focused_payload}

    assert not focused_committee.exists()
    assert focused_lanes <= {
        "section_methods",
        "section_results",
        "notation_and_numeric_consistency",
        "evaluation_fairness_and_reproducibility",
    }


def test_diff_review_issues_reports_statuses() -> None:
    from diff_review_issues import diff_issues

    previous = [
        {"root_cause_key": "claim-a", "title": "Claim A", "severity": "major"},
        {"root_cause_key": "claim-b", "title": "Claim B", "severity": "moderate"},
    ]
    current = [
        {"root_cause_key": "claim-a", "title": "Claim A", "severity": "moderate"},
        {"root_cause_key": "claim-c", "title": "Claim C", "severity": "minor"},
    ]

    diff = diff_issues(previous, current)
    statuses = {item["root_cause_key"]: item["status"] for item in diff["statuses"]}
    assert statuses["claim-a"] == "PARTIALLY_ADDRESSED"
    assert statuses["claim-b"] == "FULLY_ADDRESSED"
    assert diff["new_issues"][0]["root_cause_key"] == "claim-c"


# ============================================================
# v4.1 enhancements: EIC, theory contribution, qualitative,
#                     pseudo-innovation, logic chain
# ============================================================

_AGENTS_DIR = Path(__file__).parent.parent / "academic-writing-skills" / "paper-audit" / "agents"
_REFS_DIR = Path(__file__).parent.parent / "academic-writing-skills" / "paper-audit" / "references"


class TestEditorInChiefAgent:
    """Tests for the new Editor-in-Chief agent file and gate integration."""

    def test_agent_file_exists(self) -> None:
        assert (_AGENTS_DIR / "editor_in_chief_agent.md").exists()

    def test_agent_has_screening_dimensions(self) -> None:
        content = (_AGENTS_DIR / "editor_in_chief_agent.md").read_text(encoding="utf-8")
        assert "Pitch Quality" in content
        assert "Venue Fit" in content
        assert "Fatal Flaw Detection" in content
        assert "Presentation Baseline" in content

    def test_agent_has_decision_thresholds(self) -> None:
        content = (_AGENTS_DIR / "editor_in_chief_agent.md").read_text(encoding="utf-8")
        assert "Pass to Review" in content
        assert "Desk Reject" in content
        assert "Conditional Pass" in content

    def test_gate_mode_references_eic_in_skill(self) -> None:
        skill_md = (_REFS_DIR.parent / "SKILL.md").read_text(encoding="utf-8")
        assert "editor_in_chief_agent.md" in skill_md
        assert "EIC Screening" in skill_md


class TestExpandedTaxonomy:
    """Tests for the expanded 16-part issue taxonomy."""

    def test_deep_review_criteria_has_16_dimensions(self) -> None:
        content = (_REFS_DIR / "DEEP_REVIEW_CRITERIA.md").read_text(encoding="utf-8")
        # Check new dimensions exist
        assert "Theory contribution deficiency" in content
        assert "Qualitative methodology opacity" in content
        assert "Pseudo-innovation" in content
        assert "Paragraph-level argument incoherence" in content

    def test_deep_review_criteria_has_eic_section(self) -> None:
        content = (_REFS_DIR / "DEEP_REVIEW_CRITERIA.md").read_text(encoding="utf-8")
        assert "Editor-in-Chief screening" in content
        assert "gate mode" in content

    def test_skill_md_lists_16_part_taxonomy(self) -> None:
        content = (_REFS_DIR.parent / "SKILL.md").read_text(encoding="utf-8")
        assert "16-part issue taxonomy" in content
        assert "theory contribution deficiency" in content
        assert "pseudo-innovation" in content
        assert "paragraph-level argument incoherence" in content


class TestTheoryContributionDimensions:
    """Tests for A5-A7 theory contribution dimensions in domain reviewer."""

    def test_domain_reviewer_has_a5_a7(self) -> None:
        content = (_AGENTS_DIR / "domain_reviewer_agent.md").read_text(encoding="utf-8")
        assert "(A5)" in content
        assert "(A6)" in content
        assert "(A7)" in content

    def test_a5_concept_clarity(self) -> None:
        content = (_AGENTS_DIR / "domain_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Concept definition clarity" in content

    def test_a6_theory_dialogue(self) -> None:
        content = (_AGENTS_DIR / "domain_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Theory dialogue quality" in content

    def test_a7_incremental_knowledge(self) -> None:
        content = (_AGENTS_DIR / "domain_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Incremental theoretical knowledge" in content

    def test_checklist_has_theory_items(self) -> None:
        content = (_REFS_DIR / "CHECKLIST.md").read_text(encoding="utf-8")
        assert "Theory & Conceptual Framework" in content
        assert "(A5)" in content
        assert "(A6)" in content
        assert "(A7)" in content


class TestQualitativeMethodologySupport:
    """Tests for B6-B10 qualitative methodology dimensions."""

    def test_methodology_reviewer_has_b6_b10(self) -> None:
        content = (_AGENTS_DIR / "methodology_reviewer_agent.md").read_text(encoding="utf-8")
        assert "(B6)" in content
        assert "(B7)" in content
        assert "(B8)" in content
        assert "(B9)" in content
        assert "(B10)" in content

    def test_b6_sampling_logic(self) -> None:
        content = (_AGENTS_DIR / "methodology_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Theoretical sampling logic" in content

    def test_b8_coding_transparency(self) -> None:
        content = (_AGENTS_DIR / "methodology_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Coding process transparency" in content

    def test_qualitative_standards_reference_exists(self) -> None:
        assert (_REFS_DIR / "QUALITATIVE_STANDARDS.md").exists()

    def test_qualitative_standards_has_srqr(self) -> None:
        content = (_REFS_DIR / "QUALITATIVE_STANDARDS.md").read_text(encoding="utf-8")
        assert "SRQR" in content
        assert "Data saturation" in content or "saturation" in content
        assert "Reflexivity" in content or "reflexivity" in content
        assert "Triangulation" in content or "triangulation" in content

    def test_checklist_has_qualitative_items(self) -> None:
        content = (_REFS_DIR / "CHECKLIST.md").read_text(encoding="utf-8")
        assert "Qualitative Methodology" in content
        assert "(B6)" in content
        assert "(B7)" in content
        assert "(B8)" in content
        assert "(B9)" in content
        assert "(B10)" in content

    def test_methodology_reviewer_references_qualitative_standards(self) -> None:
        content = (_AGENTS_DIR / "methodology_reviewer_agent.md").read_text(encoding="utf-8")
        assert "QUALITATIVE_STANDARDS.md" in content


class TestPseudoInnovationDetection:
    """Tests for pseudo-innovation detection in prior art reviewer."""

    def test_prior_art_reviewer_has_pseudo_innovation_section(self) -> None:
        content = (_AGENTS_DIR / "prior_art_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Pseudo-Innovation Detection" in content

    def test_prior_art_reviewer_has_straw_man(self) -> None:
        content = (_AGENTS_DIR / "prior_art_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Straw Man" in content

    def test_prior_art_reviewer_has_fabricated_gap(self) -> None:
        content = (_AGENTS_DIR / "prior_art_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Fabricated Research Gap" in content

    def test_prior_art_reviewer_has_selective_citation(self) -> None:
        content = (_AGENTS_DIR / "prior_art_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Selective Citation" in content

    def test_prior_art_reviewer_has_literature_dialogue(self) -> None:
        content = (_AGENTS_DIR / "prior_art_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Literature Dialogue Quality" in content


class TestLogicChainAnalysis:
    """Tests for C5 paragraph-level logic chain analysis in critical reviewer."""

    def test_critical_reviewer_has_c5(self) -> None:
        content = (_AGENTS_DIR / "critical_reviewer_agent.md").read_text(encoding="utf-8")
        assert "(C5)" in content

    def test_c5_has_topic_sentence_extraction(self) -> None:
        content = (_AGENTS_DIR / "critical_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Topic sentence extraction" in content or "topic sentence" in content.lower()

    def test_c5_has_adjacency_coherence(self) -> None:
        content = (_AGENTS_DIR / "critical_reviewer_agent.md").read_text(encoding="utf-8")
        assert "Adjacency coherence" in content or "adjacency coherence" in content.lower()

    def test_c5_has_causal_inversion(self) -> None:
        content = (_AGENTS_DIR / "critical_reviewer_agent.md").read_text(encoding="utf-8")
        assert "causal inversion" in content.lower()
