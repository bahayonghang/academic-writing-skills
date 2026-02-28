"""Tests for paper-audit skill components."""

import sys
from pathlib import Path

import pytest
from detect_language import _is_cjk, detect_language
from pdf_parser import PdfParser
from report_generator import (
    AuditIssue,
    AuditResult,
    ChecklistItem,
    calculate_scores,
    render_gate_report,
    render_report,
    render_review_report,
    render_self_check_report,
)

# Add latex-paper-en scripts for check_references import
_scripts_en = (
    Path(__file__).parent.parent / "academic-writing-skills" / "latex-paper-en" / "scripts"
)
if str(_scripts_en) not in sys.path:
    sys.path.insert(0, str(_scripts_en))


# ============================================================
# detect_language tests
# ============================================================


class TestDetectLanguage:
    """Tests for language detection module."""

    def test_english_text(self) -> None:
        assert detect_language("Hello world, this is a test.") == "en"

    def test_chinese_text(self) -> None:
        assert detect_language("这是一篇中文学术论文的摘要部分") == "zh"

    def test_mixed_mostly_english(self) -> None:
        text = "This paper proposes a method for 深度学习 in NLP tasks."
        assert detect_language(text) == "en"

    def test_mixed_mostly_chinese(self) -> None:
        text = "本文提出了一种新的deep learning方法用于自然语言处理任务的研究"
        assert detect_language(text) == "zh"

    def test_empty_string(self) -> None:
        assert detect_language("") == "en"

    def test_whitespace_only(self) -> None:
        assert detect_language("   \n\t  ") == "en"

    def test_numbers_only(self) -> None:
        assert detect_language("12345 67890") == "en"

    def test_custom_threshold(self) -> None:
        # Text with moderate CJK content
        text = "这是一些中文内容 mixed with English words"
        assert detect_language(text, threshold=0.1) == "zh"
        assert detect_language(text, threshold=0.9) == "en"

    def test_is_cjk_basic(self) -> None:
        assert _is_cjk("中")
        assert _is_cjk("学")
        assert not _is_cjk("A")
        assert not _is_cjk("1")

    def test_fullwidth_detected(self) -> None:
        # Fullwidth forms are in CJK range
        assert _is_cjk("\uff01")  # Fullwidth exclamation


# ============================================================
# PdfParser tests
# ============================================================


class TestPdfParser:
    """Tests for PDF parser module."""

    @pytest.fixture
    def basic_parser(self) -> PdfParser:
        return PdfParser(mode="basic")

    @pytest.fixture
    def enhanced_parser(self) -> PdfParser:
        return PdfParser(mode="enhanced")

    def test_invalid_mode(self) -> None:
        with pytest.raises(ValueError, match="Invalid PDF mode"):
            PdfParser(mode="invalid")

    def test_basic_mode_creation(self, basic_parser: PdfParser) -> None:
        assert basic_parser.mode == "basic"

    def test_enhanced_mode_creation(self, enhanced_parser: PdfParser) -> None:
        assert enhanced_parser.mode == "enhanced"

    def test_comment_prefix(self, basic_parser: PdfParser) -> None:
        assert basic_parser.get_comment_prefix() == ">"

    def test_extract_visible_text_strips_headers(self, basic_parser: PdfParser) -> None:
        assert basic_parser.extract_visible_text("## Introduction") == "Introduction"
        assert basic_parser.extract_visible_text("### 2.1 Method") == "2.1 Method"
        assert basic_parser.extract_visible_text("Plain text") == "Plain text"

    def test_extract_visible_text_empty(self, basic_parser: PdfParser) -> None:
        assert basic_parser.extract_visible_text("") == ""
        assert basic_parser.extract_visible_text("  ") == ""

    def test_clean_text_removes_page_numbers(self, basic_parser: PdfParser) -> None:
        content = "Some text\n\n42\n\nMore text"
        cleaned = basic_parser.clean_text(content)
        assert "42" not in cleaned
        assert "Some text" in cleaned
        assert "More text" in cleaned

    def test_clean_text_removes_horizontal_rules(self, basic_parser: PdfParser) -> None:
        content = "Text above\n---\nText below"
        cleaned = basic_parser.clean_text(content)
        assert "---" not in cleaned
        assert "Text above" in cleaned
        assert "Text below" in cleaned

    def test_clean_text_removes_images(self, basic_parser: PdfParser) -> None:
        content = "Text\n![Figure 1](image.png)\nMore text"
        cleaned = basic_parser.clean_text(content)
        assert "![" not in cleaned
        assert "More text" in cleaned

    def test_clean_text_strips_markdown_formatting(self, basic_parser: PdfParser) -> None:
        content = "## Header\n**bold text** and *italic*\n`code`"
        cleaned = basic_parser.clean_text(content)
        assert "##" not in cleaned
        assert "**" not in cleaned
        assert "Header" in cleaned
        assert "bold text" in cleaned

    def test_clean_text_keep_structure(self, basic_parser: PdfParser) -> None:
        content = "Line 1\n\nLine 2\n\n42\n\nLine 3"
        cleaned = basic_parser.clean_text(content, keep_structure=True)
        # Empty lines preserved, page number removed
        assert "Line 1" in cleaned
        assert "Line 3" in cleaned

    def test_split_sections_english(self, basic_parser: PdfParser) -> None:
        content = (
            "## Abstract\nSome abstract text\n## Introduction\nIntro text\n## Method\nMethod text"
        )
        sections = basic_parser.split_sections(content)
        assert "abstract" in sections
        assert "introduction" in sections
        assert "method" in sections

    def test_split_sections_chinese(self, basic_parser: PdfParser) -> None:
        content = "## 摘要\n摘要内容\n## 绪论\n绪论内容\n## 相关工作\n相关工作内容"
        sections = basic_parser.split_sections(content)
        assert "abstract" in sections
        assert "introduction" in sections
        assert "related" in sections

    def test_split_sections_empty(self, basic_parser: PdfParser) -> None:
        sections = basic_parser.split_sections("No sections here")
        assert len(sections) == 0

    def test_is_document_parser(self, basic_parser: PdfParser) -> None:
        from parsers import DocumentParser

        assert isinstance(basic_parser, DocumentParser)


# ============================================================
# report_generator tests
# ============================================================


class TestScoring:
    """Tests for scoring engine."""

    def test_no_issues_perfect_score(self) -> None:
        scores = calculate_scores([])
        assert scores["quality"] == 6.0
        assert scores["clarity"] == 6.0
        assert scores["significance"] == 6.0
        assert scores["originality"] == 6.0
        assert scores["overall"] == 6.0

    def test_single_critical_issue(self) -> None:
        issues = [AuditIssue("FORMAT", 1, "Critical", "P0", "Error")]
        scores = calculate_scores(issues)
        # FORMAT maps to clarity
        assert scores["clarity"] == 4.5  # 6.0 - 1.5
        assert scores["quality"] == 6.0  # Unaffected
        assert scores["overall"] < 6.0

    def test_single_major_issue(self) -> None:
        issues = [AuditIssue("GRAMMAR", 1, "Major", "P1", "Error")]
        scores = calculate_scores(issues)
        assert scores["clarity"] == 5.25  # 6.0 - 0.75

    def test_single_minor_issue(self) -> None:
        issues = [AuditIssue("SENTENCES", 1, "Minor", "P2", "Warning")]
        scores = calculate_scores(issues)
        assert scores["clarity"] == 5.75  # 6.0 - 0.25

    def test_floor_at_one(self) -> None:
        # Many critical issues should floor at 1.0
        issues = [AuditIssue("FORMAT", i, "Critical", "P0", f"Error {i}") for i in range(10)]
        scores = calculate_scores(issues)
        assert scores["clarity"] == 1.0

    def test_multi_dimension_issue(self) -> None:
        # LOGIC maps to quality AND significance
        issues = [AuditIssue("LOGIC", 1, "Major", "P1", "Logic gap")]
        scores = calculate_scores(issues)
        assert scores["quality"] == 5.25
        assert scores["significance"] == 5.25
        assert scores["clarity"] == 6.0  # Unaffected

    def test_weighted_average(self) -> None:
        issues = [
            AuditIssue("FORMAT", 1, "Critical", "P0", "E1"),  # clarity -1.5
            AuditIssue("GRAMMAR", 2, "Major", "P1", "E2"),  # clarity -0.75
            AuditIssue("SENTENCES", 3, "Minor", "P2", "E3"),  # clarity -0.25
            AuditIssue("BIB", 4, "Critical", "P0", "E4"),  # quality -1.5
            AuditIssue("LOGIC", 5, "Major", "P1", "E5"),  # quality -0.75, significance -0.75
            AuditIssue("DEAI", 6, "Critical", "P0", "E6"),  # clarity -1.5, originality -1.5
        ]
        scores = calculate_scores(issues)
        # Verify overall equals the weighted sum of dimension scores
        expected = (
            scores["quality"] * 0.30
            + scores["clarity"] * 0.30
            + scores["significance"] * 0.20
            + scores["originality"] * 0.20
        )
        assert abs(scores["overall"] - expected) < 0.1


class TestReportRendering:
    """Tests for report rendering."""

    @pytest.fixture
    def sample_issues(self) -> list[AuditIssue]:
        return [
            AuditIssue("FORMAT", 42, "Critical", "P0", "Missing figure reference"),
            AuditIssue("GRAMMAR", 87, "Major", "P1", "Subject-verb disagreement"),
            AuditIssue("SENTENCES", 123, "Minor", "P2", "Sentence too long"),
        ]

    @pytest.fixture
    def sample_checklist(self) -> list[ChecklistItem]:
        return [
            ChecklistItem("Paper compiles", True),
            ChecklistItem("No TODO found", False, "TODO on line 256"),
        ]

    def test_self_check_report_structure(
        self, sample_issues: list[AuditIssue], sample_checklist: list[ChecklistItem]
    ) -> None:
        result = AuditResult(
            file_path="paper.tex",
            language="en",
            mode="self-check",
            venue="neurips",
            issues=sample_issues,
            checklist=sample_checklist,
        )
        report = render_self_check_report(result)
        assert "# Paper Audit Report" in report
        assert "Executive Summary" in report
        assert "Scores" in report
        assert "Issues" in report
        assert "Critical" in report
        assert "Major" in report
        assert "Minor" in report
        assert "Pre-Submission Checklist" in report
        assert "[x] Paper compiles" in report
        assert "[ ] No TODO found" in report

    def test_review_report_structure(self, sample_issues: list[AuditIssue]) -> None:
        result = AuditResult(
            file_path="paper.tex",
            language="en",
            mode="review",
            issues=sample_issues,
            strengths=["Strong methodology", "Clear writing"],
            weaknesses=["Missing baselines"],
            questions=["Why not compare with X?"],
            summary="This paper proposes...",
        )
        report = render_review_report(result)
        assert "# Peer Review Report" in report
        assert "Summary" in report
        assert "Strengths" in report
        assert "Weaknesses" in report
        assert "Questions for Authors" in report
        assert "Overall Assessment" in report
        assert "Recommendation" in report

    def test_gate_report_pass(self) -> None:
        result = AuditResult(
            file_path="paper.tex",
            language="en",
            mode="gate",
            issues=[AuditIssue("GRAMMAR", 1, "Minor", "P2", "Typo")],
            checklist=[ChecklistItem("Compiles", True)],
        )
        report = render_gate_report(result)
        assert "PASS" in report
        # "Blocking Issues (must fix)" should NOT appear; only "Non-Blocking Issues"
        assert "Blocking Issues (must fix)" not in report

    def test_gate_report_fail(self) -> None:
        result = AuditResult(
            file_path="paper.tex",
            language="en",
            mode="gate",
            issues=[AuditIssue("FORMAT", 1, "Critical", "P0", "Missing ref")],
            checklist=[
                ChecklistItem("Compiles", True),
                ChecklistItem("No TODOs", False, "Found TODO"),
            ],
        )
        report = render_gate_report(result)
        assert "FAIL" in report
        assert "Blocking Issues" in report

    def test_render_report_dispatches_correctly(self, sample_issues: list[AuditIssue]) -> None:
        for mode, expected_title in [
            ("self-check", "Paper Audit Report"),
            ("review", "Peer Review Report"),
            ("gate", "Quality Gate Report"),
        ]:
            result = AuditResult(
                file_path="paper.tex",
                language="en",
                mode=mode,
                issues=sample_issues,
            )
            report = render_report(result)
            assert expected_title in report

    def test_report_with_no_issues(self) -> None:
        result = AuditResult(
            file_path="paper.tex",
            language="en",
            mode="self-check",
        )
        report = render_report(result)
        assert "0 issues" in report
        assert "6.0/6.0" in report
        assert "Strong Accept" in report

    def test_report_with_chinese_language(self, sample_issues: list[AuditIssue]) -> None:
        result = AuditResult(
            file_path="thesis.tex",
            language="zh",
            mode="self-check",
            issues=sample_issues,
        )
        report = render_report(result)
        assert "ZH" in report


# ============================================================
# Integration: audit module imports
# ============================================================


class TestAuditModule:
    """Tests for audit.py module imports and configuration."""

    def test_mode_checks_defined(self) -> None:
        from audit import MODE_CHECKS

        assert "self-check" in MODE_CHECKS
        assert "review" in MODE_CHECKS
        assert "gate" in MODE_CHECKS

    def test_self_check_has_expected_checks(self) -> None:
        from audit import MODE_CHECKS

        checks = MODE_CHECKS["self-check"]
        assert "format" in checks
        assert "grammar" in checks
        assert "logic" in checks
        assert "bib" in checks

    def test_gate_has_minimal_checks(self) -> None:
        from audit import MODE_CHECKS

        gate_checks = MODE_CHECKS["gate"]
        assert len(gate_checks) < len(MODE_CHECKS["self-check"])
        assert "format" in gate_checks
        assert "checklist" in gate_checks

    def test_zh_extra_checks(self) -> None:
        from audit import ZH_EXTRA_CHECKS

        assert "consistency" in ZH_EXTRA_CHECKS

    def test_resolve_script_english(self) -> None:
        from audit import _resolve_script

        script = _resolve_script("grammar", "en", ".tex")
        assert script is not None
        assert script.name == "analyze_grammar.py"

    def test_resolve_script_unknown(self) -> None:
        from audit import _resolve_script

        script = _resolve_script("nonexistent_check", "en", ".tex")
        assert script is None

    def test_run_checklist_basic(self) -> None:
        from audit import _run_checklist

        content = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
This is a TODO item.
\label{fig:test}
\end{document}
"""
        items = _run_checklist(content, "paper.tex", "en")
        assert len(items) > 0
        # Should detect TODO
        todo_item = next((i for i in items if "TODO" in i.description), None)
        assert todo_item is not None
        assert not todo_item.passed

    def test_run_checklist_clean(self) -> None:
        from audit import _run_checklist

        content = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
This is clean text with no issues.
\end{document}
"""
        items = _run_checklist(content, "paper.tex", "en")
        todo_item = next((i for i in items if "TODO" in i.description), None)
        assert todo_item is not None
        assert todo_item.passed


# ============================================================
# P0-3: check_references tests
# ============================================================


class TestCheckReferences:
    """Tests for reference integrity checker."""

    def test_find_labels(self) -> None:
        from check_references import ReferenceChecker

        content = r"""
\begin{figure}
\caption{Architecture}
\label{fig:arch}
\end{figure}
\begin{table}
\caption{Results}
\label{tab:results}
\end{table}
\label{eq:loss}
"""
        checker = ReferenceChecker(content, "test.tex")
        labels = checker.find_labels()
        names = {lbl.name for lbl in labels}
        assert "fig:arch" in names
        assert "tab:results" in names
        assert "eq:loss" in names

    def test_find_refs(self) -> None:
        from check_references import ReferenceChecker

        content = r"""
As shown in Figure~\ref{fig:arch} and Table~\ref{tab:results}.
See also Equation~\eqref{eq:loss} and \autoref{fig:arch}.
"""
        checker = ReferenceChecker(content, "test.tex")
        refs = checker.find_refs()
        names = {r.name for r in refs}
        assert "fig:arch" in names
        assert "tab:results" in names
        assert "eq:loss" in names

    def test_undefined_reference(self) -> None:
        from check_references import ReferenceChecker

        content = r"""
\ref{fig:missing}
\label{fig:existing}
"""
        checker = ReferenceChecker(content, "test.tex")
        issues = checker.run_all()
        critical = [i for i in issues if i["severity"] == "Critical"]
        assert any("fig:missing" in i["message"] for i in critical)

    def test_unreferenced_label(self) -> None:
        from check_references import ReferenceChecker

        content = r"""
\begin{figure}
\caption{Test}
\label{fig:unused}
\end{figure}
"""
        checker = ReferenceChecker(content, "test.tex")
        issues = checker.run_all()
        minor = [i for i in issues if i["severity"] == "Minor"]
        assert any("fig:unused" in i["message"] for i in minor)

    def test_missing_caption(self) -> None:
        from check_references import ReferenceChecker

        content = r"""
\begin{figure}
\label{fig:nocap}
\end{figure}
"""
        checker = ReferenceChecker(content, "test.tex")
        issues = checker.run_all()
        major = [i for i in issues if i["severity"] == "Major"]
        assert any("caption" in i["message"].lower() for i in major)

    def test_all_clean(self) -> None:
        from check_references import ReferenceChecker

        content = r"""
\begin{figure}
\caption{Good figure}
\label{fig:good}
\end{figure}
See Figure~\ref{fig:good}.
"""
        checker = ReferenceChecker(content, "test.tex")
        issues = checker.run_all()
        # No critical or major issues
        critical_major = [i for i in issues if i["severity"] in ("Critical", "Major")]
        assert len(critical_major) == 0

    def test_skip_commented_lines(self) -> None:
        from check_references import ReferenceChecker

        content = r"""
% \label{fig:commented}
% \ref{fig:commented}
\label{fig:real}
\ref{fig:real}
"""
        checker = ReferenceChecker(content, "test.tex")
        labels = checker.find_labels()
        names = {lbl.name for lbl in labels}
        assert "fig:commented" not in names
        assert "fig:real" in names


# ============================================================
# P0-2: visual_check tests
# ============================================================


class TestVisualCheck:
    """Tests for visual checker (unit tests without PDF files)."""

    def test_calc_overlap_area(self) -> None:
        from visual_check import _calc_overlap_area

        # No overlap
        assert _calc_overlap_area((0, 0, 10, 10), (20, 20, 30, 30)) == 0
        # Full overlap
        assert _calc_overlap_area((0, 0, 10, 10), (0, 0, 10, 10)) == 100
        # Partial overlap
        assert _calc_overlap_area((0, 0, 10, 10), (5, 5, 15, 15)) == 25

    def test_calc_overlap_area_edge(self) -> None:
        from visual_check import _calc_overlap_area

        # Adjacent (no overlap)
        assert _calc_overlap_area((0, 0, 10, 10), (10, 0, 20, 10)) == 0

    def test_format_issues_empty(self) -> None:
        from visual_check import _format_issues

        result = _format_issues([])
        assert "No layout issues" in result

    def test_format_issues_json(self) -> None:
        import json

        from visual_check import _format_issues

        issues = [
            {
                "module": "VISUAL",
                "page": 1,
                "severity": "Major",
                "priority": "P1",
                "message": "Test issue",
            }
        ]
        result = _format_issues(issues, as_json=True)
        parsed = json.loads(result)
        assert len(parsed) == 1
        assert parsed[0]["page"] == 1

    def test_format_issues_protocol(self) -> None:
        from visual_check import _format_issues

        issues = [
            {
                "module": "VISUAL",
                "page": 3,
                "severity": "Critical",
                "priority": "P0",
                "message": "Block overlap",
            }
        ]
        result = _format_issues(issues)
        assert "Page 3" in result
        assert "Severity: Critical" in result
        assert "Priority: P0" in result


# ============================================================
# P1-1: scholar_eval tests
# ============================================================


class TestScholarEval:
    """Tests for ScholarEval evaluation framework."""

    def test_no_issues_perfect_score(self) -> None:
        from scholar_eval import evaluate_from_audit

        scores = evaluate_from_audit([])
        assert scores["soundness"] == 10.0
        assert scores["clarity"] == 10.0
        assert scores["presentation"] == 10.0

    def test_deductions(self) -> None:
        from scholar_eval import evaluate_from_audit

        issues = [
            {"module": "LOGIC", "severity": "Critical", "message": "Flaw"},
            {"module": "LOGIC", "severity": "Major", "message": "Gap"},
        ]
        scores = evaluate_from_audit(issues)
        # 10 - 2.5 - 1.25 = 6.25
        assert scores["soundness"] == 6.25

    def test_floor_at_one(self) -> None:
        from scholar_eval import evaluate_from_audit

        issues = [
            {"module": "GRAMMAR", "severity": "Critical", "message": f"E{i}"} for i in range(10)
        ]
        scores = evaluate_from_audit(issues)
        assert scores["clarity"] == 1.0

    def test_merge_script_only(self) -> None:
        from scholar_eval import merge_scores

        script_scores = {
            "soundness": 8.0,
            "clarity": 9.0,
            "presentation": 7.0,
            "reproducibility_partial": 8.5,
        }
        merged = merge_scores(script_scores, llm_scores=None)
        assert merged["soundness"] == 8.0
        assert merged["novelty"] is None
        assert merged["overall"] is not None

    def test_merge_with_llm(self) -> None:
        from scholar_eval import merge_scores

        script_scores = {
            "soundness": 8.0,
            "clarity": 9.0,
            "presentation": 7.0,
            "reproducibility_partial": 7.0,
        }
        llm_scores = {
            "novelty": {"score": 8.0, "evidence": "Novel approach"},
            "significance": {"score": 7.0, "evidence": "Important"},
            "reproducibility_llm": {"score": 6.0, "evidence": "Code missing"},
            "ethics": {"score": 9.0, "evidence": "No concerns"},
        }
        merged = merge_scores(script_scores, llm_scores)
        assert merged["novelty"] == 8.0
        assert merged["significance"] == 7.0
        assert merged["ethics"] == 9.0
        # Reproducibility = avg(7.0, 6.0) = 6.5
        assert merged["reproducibility"] == 6.5
        assert merged["overall"] is not None

    def test_readiness_labels(self) -> None:
        from scholar_eval import get_readiness_label

        assert "Strong Accept" in get_readiness_label(9.5)
        assert "Accept" in get_readiness_label(8.5)
        assert "minor" in get_readiness_label(7.5).lower()
        assert "Major" in get_readiness_label(6.5)
        assert "Not ready" in get_readiness_label(3.0)
        assert "Insufficient" in get_readiness_label(None)

    def test_render_report(self) -> None:
        from scholar_eval import build_result, render_scholar_eval_report

        script_scores = {
            "soundness": 8.0,
            "clarity": 9.0,
            "presentation": 7.0,
            "reproducibility_partial": 8.0,
        }
        result = build_result(script_scores)
        report = render_scholar_eval_report(result)
        assert "ScholarEval" in report
        assert "Soundness" in report
        assert "Publication Readiness" in report

    def test_dimension_map_new_entries(self) -> None:
        """Verify DIMENSION_MAP has entries for new modules."""
        from report_generator import DIMENSION_MAP

        assert "references" in DIMENSION_MAP
        assert "visual" in DIMENSION_MAP
        assert "clarity" in DIMENSION_MAP["references"]
        assert "quality" in DIMENSION_MAP["references"]
        assert "clarity" in DIMENSION_MAP["visual"]


# ============================================================
# P1-2: online_bib_verify tests
# ============================================================


class TestOnlineBibVerify:
    """Tests for online bibliography verification (unit tests, no network)."""

    def test_data_classes(self) -> None:
        from online_bib_verify import EntryVerifyResult, VerifyResult

        vr = VerifyResult(valid=True, metadata={"title": "Test"})
        assert vr.valid
        assert vr.metadata["title"] == "Test"

        evr = EntryVerifyResult(
            status="verified",
            bib_key="smith2020",
            confidence=0.9,
        )
        assert evr.status == "verified"
        assert evr.bib_key == "smith2020"
        assert evr.mismatches == []

    def test_entry_verify_result_mismatch(self) -> None:
        from online_bib_verify import EntryVerifyResult

        evr = EntryVerifyResult(
            status="mismatch",
            bib_key="doe2021",
            mismatches=["year: bib='2021' vs api='2020'"],
            confidence=0.7,
        )
        assert evr.status == "mismatch"
        assert len(evr.mismatches) == 1

    def test_cross_check_match(self) -> None:
        from online_bib_verify import OnlineBibVerifier

        verifier = OnlineBibVerifier()
        result = verifier._cross_check(
            "test_key",
            {"year": "2020", "journal": "Nature"},
            {"year": "2020", "journal": "Nature"},
        )
        assert result.status == "verified"
        assert result.confidence == 0.9

    def test_cross_check_mismatch(self) -> None:
        from online_bib_verify import OnlineBibVerifier

        verifier = OnlineBibVerifier()
        result = verifier._cross_check(
            "test_key",
            {"year": "2020", "journal": "Nature"},
            {"year": "2021", "journal": "Science"},
        )
        assert result.status == "mismatch"
        assert len(result.mismatches) == 2

    def test_match_title_found(self) -> None:
        from online_bib_verify import OnlineBibVerifier

        verifier = OnlineBibVerifier()
        results = [
            {"title": "A Novel Deep Learning Approach", "externalIds": {"DOI": "10.1234/test"}},
        ]
        result = verifier._match_title(
            "test_key",
            {"title": "A Novel Deep Learning Approach"},
            results,
        )
        assert result.status == "verified"
        assert result.suggested_doi == "10.1234/test"

    def test_match_title_not_found(self) -> None:
        from online_bib_verify import OnlineBibVerifier

        verifier = OnlineBibVerifier()
        results = [
            {"title": "Completely Different Paper", "externalIds": {}},
        ]
        result = verifier._match_title(
            "test_key",
            {"title": "A Novel Deep Learning Approach"},
            results,
        )
        assert result.status == "not_found"

    def test_parse_bib_entries(self) -> None:
        import tempfile

        from online_bib_verify import _parse_bib_entries

        bib_content = """
@article{smith2020,
  author = {John Smith},
  title = {A Great Paper},
  journal = {Nature},
  year = {2020},
  doi = {10.1234/great}
}
@inproceedings{doe2021,
  author = {Jane Doe},
  title = {Another Paper},
  booktitle = {ICML},
  year = {2021}
}
"""
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".bib",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(bib_content)
            f.flush()
            entries = _parse_bib_entries(Path(f.name))

        assert len(entries) == 2
        assert entries[0]["key"] == "smith2020"
        assert entries[0]["doi"] == "10.1234/great"
        assert entries[1]["key"] == "doe2021"


# ============================================================
# Integration: audit module configuration
# ============================================================


class TestAuditModuleUpdated:
    """Tests for updated audit module configuration."""

    def test_mode_checks_include_references(self) -> None:
        from audit import MODE_CHECKS

        assert "references" in MODE_CHECKS["self-check"]
        assert "references" in MODE_CHECKS["review"]
        assert "references" in MODE_CHECKS["gate"]

    def test_mode_checks_include_visual(self) -> None:
        from audit import MODE_CHECKS

        assert "visual" in MODE_CHECKS["self-check"]
        assert "visual" in MODE_CHECKS["review"]
        assert "visual" in MODE_CHECKS["gate"]

    def test_resolve_script_references(self) -> None:
        from audit import _resolve_script

        script = _resolve_script("references", "en", ".tex")
        assert script is not None
        assert script.name == "check_references.py"

    def test_resolve_script_visual(self) -> None:
        from audit import _resolve_script

        script = _resolve_script("visual", "en", ".pdf")
        assert script is not None
        assert script.name == "visual_check.py"
