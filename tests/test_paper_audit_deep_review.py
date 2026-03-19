"""Tests for paper-audit deep-review-first additions."""

import json
from pathlib import Path

from report_generator import (
    AuditResult,
    DeepReviewIssue,
    coerce_deep_review_issue,
    normalize_deep_review_issue_dict,
    render_deep_review_report,
    render_json_report,
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
            {"priority": "Priority 1", "title": "Qualify headline claim", "source": "[LLM]", "section": "abstract"}
        ],
    )

    report = render_deep_review_report(result)
    assert "Deep Review Report" in report
    assert "Compatibility Note" in report
    assert "Major Issues" in report
    assert "Moderate Issues" in report
    assert "Revision Roadmap" in report


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
        {"title": "Found", "quote": "exact text", "explanation": "", "comment_type": "presentation", "severity": "minor", "source_kind": "llm"},
        {"title": "Missing", "quote": "not present", "explanation": "", "comment_type": "presentation", "severity": "minor", "source_kind": "llm"},
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
    assert {"title", "quote", "explanation", "comment_type", "severity", "source_kind", "review_lane", "root_cause_key", "quote_verified"}.issubset(first_issue)
    assert any(issue["review_lane"] == "claims_vs_evidence" for issue in payload)
    assert any(issue["review_lane"] == "evaluation_fairness_and_reproducibility" for issue in payload)
    assert any(issue["review_lane"] == "section_methods" for issue in payload)


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
