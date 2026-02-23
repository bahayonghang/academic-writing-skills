"""Tests for paper-audit skill components."""

import pytest

from detect_language import detect_language, _is_cjk
from pdf_parser import PdfParser
from report_generator import (
    AuditIssue,
    AuditResult,
    ChecklistItem,
    calculate_scores,
    render_report,
    render_self_check_report,
    render_review_report,
    render_gate_report,
)


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
        content = "## Abstract\nSome abstract text\n## Introduction\nIntro text\n## Method\nMethod text"
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
        issues = [
            AuditIssue("FORMAT", i, "Critical", "P0", f"Error {i}")
            for i in range(10)
        ]
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
            AuditIssue("FORMAT", 1, "Critical", "P0", "E1"),     # clarity -1.5
            AuditIssue("GRAMMAR", 2, "Major", "P1", "E2"),       # clarity -0.75
            AuditIssue("SENTENCES", 3, "Minor", "P2", "E3"),     # clarity -0.25
            AuditIssue("BIB", 4, "Critical", "P0", "E4"),        # quality -1.5
            AuditIssue("LOGIC", 5, "Major", "P1", "E5"),         # quality -0.75, significance -0.75
            AuditIssue("DEAI", 6, "Critical", "P0", "E6"),       # clarity -1.5, originality -1.5
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
            file_path="paper.tex", language="en", mode="self-check",
            venue="neurips", issues=sample_issues, checklist=sample_checklist,
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
            file_path="paper.tex", language="en", mode="review",
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
            file_path="paper.tex", language="en", mode="gate",
            issues=[AuditIssue("GRAMMAR", 1, "Minor", "P2", "Typo")],
            checklist=[ChecklistItem("Compiles", True)],
        )
        report = render_gate_report(result)
        assert "PASS" in report
        # "Blocking Issues (must fix)" should NOT appear; only "Non-Blocking Issues"
        assert "Blocking Issues (must fix)" not in report

    def test_gate_report_fail(self) -> None:
        result = AuditResult(
            file_path="paper.tex", language="en", mode="gate",
            issues=[AuditIssue("FORMAT", 1, "Critical", "P0", "Missing ref")],
            checklist=[ChecklistItem("Compiles", True), ChecklistItem("No TODOs", False, "Found TODO")],
        )
        report = render_gate_report(result)
        assert "FAIL" in report
        assert "Blocking Issues" in report

    def test_render_report_dispatches_correctly(
        self, sample_issues: list[AuditIssue]
    ) -> None:
        for mode, expected_title in [
            ("self-check", "Paper Audit Report"),
            ("review", "Peer Review Report"),
            ("gate", "Quality Gate Report"),
        ]:
            result = AuditResult(
                file_path="paper.tex", language="en", mode=mode,
                issues=sample_issues,
            )
            report = render_report(result)
            assert expected_title in report

    def test_report_with_no_issues(self) -> None:
        result = AuditResult(
            file_path="paper.tex", language="en", mode="self-check",
        )
        report = render_report(result)
        assert "0 issues" in report
        assert "6.0/6.0" in report
        assert "Strong Accept" in report

    def test_report_with_chinese_language(self, sample_issues: list[AuditIssue]) -> None:
        result = AuditResult(
            file_path="thesis.tex", language="zh", mode="self-check",
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
