"""Tests for paper-audit skill components."""

import json
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
    render_reaudit_report,
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
        assert "Submission Blockers" in report
        assert "Quality Improvements" in report
        assert "[Script]" in report
        assert "Pre-Submission Checklist" in report
        assert "Scores" in report
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
        assert report.isascii()

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
        assert "[BLOCKING]" in report

    def test_gate_report_uses_ascii_safe_advisory_labels(self) -> None:
        result = AuditResult(
            file_path="paper.tex",
            language="en",
            mode="gate",
            issues=[AuditIssue("GRAMMAR", 4, "Minor", "P2", "Passive voice")],
            checklist=[ChecklistItem("No TODOs", False, "Found TODO")],
        )
        report = render_gate_report(result)
        assert "Advisory Recommendations" in report
        assert "[INFO]" in report
        assert "[FAIL]" in report
        assert report.isascii()

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
        assert "experiment" in checks
        assert "bib" in checks

    def test_gate_has_minimal_checks(self) -> None:
        from audit import MODE_CHECKS

        gate_checks = MODE_CHECKS["gate"]
        assert len(gate_checks) < len(MODE_CHECKS["self-check"])
        assert "format" in gate_checks
        assert "pseudocode" in gate_checks
        assert "checklist" in gate_checks

    def test_zh_extra_checks(self) -> None:
        from audit import ZH_EXTRA_CHECKS

        assert "consistency" in ZH_EXTRA_CHECKS

    def test_resolve_script_english(self) -> None:
        from audit import _resolve_script

        script = _resolve_script("grammar", "en", ".tex")
        assert script is not None
        assert script.name == "analyze_grammar.py"

    def test_resolve_script_experiment(self) -> None:
        from audit import _resolve_script

        script = _resolve_script("experiment", "en", ".tex")
        assert script is not None
        assert script.name == "analyze_experiment.py"

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

    def test_dimension_map_includes_experiment(self) -> None:
        from report_generator import DIMENSION_MAP

        assert "experiment" in DIMENSION_MAP
        assert "quality" in DIMENSION_MAP["experiment"]

    def test_run_audit_passes_cross_section_to_logic(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import audit

        tex = tmp_path / "paper.tex"
        tex.write_text(
            "\\documentclass{article}\n\\begin{document}\n\\section{Introduction}\nA problem.\n\\section{Conclusion}\nA conclusion.\n\\end{document}\n",
            encoding="utf-8",
        )

        calls: list[tuple[str, list[str]]] = []

        def fake_run(script_path, file_path, extra_args=None):
            calls.append((Path(script_path).name, list(extra_args or [])))
            return 0, "", ""

        monkeypatch.setattr(audit, "_run_check_script", fake_run)
        monkeypatch.setattr(audit, "_run_checklist", lambda *args, **kwargs: [])

        result = audit.run_audit(str(tex), mode="self-check", lang="en")
        assert result is not None
        logic_calls = [args for name, args in calls if name == "analyze_logic.py"]
        assert logic_calls
        assert ["--cross-section"] in logic_calls

    def test_run_audit_schedules_experiment_and_deai(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import audit

        tex = tmp_path / "paper.tex"
        tex.write_text(
            "\\documentclass{article}\n\\begin{document}\n\\section{Discussion}\nResults.\n\\end{document}\n",
            encoding="utf-8",
        )

        calls: list[str] = []

        def fake_run(script_path, file_path, extra_args=None):
            calls.append(Path(script_path).name)
            if Path(script_path).name == "analyze_experiment.py":
                return 0, "% EXPERIMENT (Line 1) [Severity: Major] [Priority: P1]: issue", ""
            return 0, "", ""

        monkeypatch.setattr(audit, "_run_check_script", fake_run)
        monkeypatch.setattr(audit, "_run_checklist", lambda *args, **kwargs: [])

        result = audit.run_audit(str(tex), mode="self-check", lang="en")
        assert "analyze_experiment.py" in calls
        assert any(issue.module == "EXPERIMENT" for issue in result.issues)


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

    def test_resolve_script_pseudocode(self) -> None:
        from audit import _resolve_script

        script = _resolve_script("pseudocode", "en", ".tex")
        assert script is not None
        assert script.name == "check_pseudocode.py"


# ============================================================
# P0-venue: venue filtering tests
# ============================================================


class TestVenueConfig:
    """Tests for VENUE_CONFIG and venue-specific checklist items."""

    def test_venue_config_has_all_keys(self) -> None:
        from audit import VENUE_CONFIG

        expected = {"neurips", "iclr", "icml", "ieee", "acm", "thesis-zh"}
        assert set(VENUE_CONFIG.keys()) == expected

    def test_venue_config_structure(self) -> None:
        from audit import VENUE_CONFIG

        for venue_key, config in VENUE_CONFIG.items():
            assert "checklist_section" in config, f"{venue_key} missing checklist_section"
            assert "blind_review" in config, f"{venue_key} missing blind_review"

    def test_venue_config_neurips_details(self) -> None:
        from audit import VENUE_CONFIG

        cfg = VENUE_CONFIG["neurips"]
        assert cfg["page_limit"] == 9
        assert cfg["blind_review"] is True
        assert len(cfg["extra_checks"]) >= 3

    def test_venue_config_ieee_details(self) -> None:
        from audit import VENUE_CONFIG

        cfg = VENUE_CONFIG["ieee"]
        assert cfg["abstract_max_words"] == 250
        assert cfg["keywords_range"] == (3, 5)
        assert cfg["blind_review"] is False


class TestVenueChecklist:
    """Tests for _run_checklist venue-specific filtering."""

    CLEAN_CONTENT = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
This is clean text with no issues.
\end{document}
"""

    NEURIPS_CONTENT = r"""
\documentclass{article}
\begin{document}
\section{Introduction}
This paper proposes a novel method.
\section*{Broader Impact}
This work may have societal implications.
\section*{Paper Checklist}
We provide our checklist below.
Reproducibility: all code is available.
\end{document}
"""

    IEEE_CONTENT = r"""
\documentclass{IEEEtran}
\begin{abstract}
This is a short abstract about signal processing.
\end{abstract}
\begin{IEEEkeywords}
deep learning, signal processing, classification
\end{IEEEkeywords}
\begin{document}
\section{Introduction}
This paper proposes a method.
\end{document}
"""

    IEEE_FLOAT_ALGO_CONTENT = r"""
\documentclass{IEEEtran}
\begin{abstract}
This is a short abstract about signal processing.
\end{abstract}
\begin{IEEEkeywords}
deep learning, signal processing, classification
\end{IEEEkeywords}
\begin{document}
\section{Introduction}
This paper proposes a method.
\begin{algorithm}
\caption{Adaptive inference procedure}
\label{alg:main}
\begin{algorithmic}
\State Update model state
\end{algorithmic}
\end{algorithm}
\end{document}
"""

    def test_no_venue_returns_only_universal(self) -> None:
        from audit import _run_checklist

        items = _run_checklist(self.CLEAN_CONTENT, "paper.tex", "en", venue="")
        venue_items = [i for i in items if i.description.startswith("[")]
        assert len(venue_items) == 0

    def test_unknown_venue_returns_only_universal(self) -> None:
        from audit import _run_checklist

        items = _run_checklist(self.CLEAN_CONTENT, "paper.tex", "en", venue="unknown_conf")
        venue_items = [i for i in items if i.description.startswith("[")]
        assert len(venue_items) == 0

    def test_neurips_adds_venue_items(self) -> None:
        from audit import _run_checklist

        items = _run_checklist(self.CLEAN_CONTENT, "paper.tex", "en", venue="neurips")
        venue_items = [i for i in items if "NEURIPS" in i.description]
        assert len(venue_items) >= 3  # checklist, broader impact, reproducibility

    def test_neurips_content_passes_checks(self) -> None:
        from audit import _run_checklist

        items = _run_checklist(self.NEURIPS_CONTENT, "paper.tex", "en", venue="neurips")
        neurips_items = [i for i in items if "NEURIPS" in i.description]
        passed = [i for i in neurips_items if i.passed]
        assert len(passed) >= 2  # broader impact + reproducibility should pass

    def test_neurips_page_limit_check(self) -> None:
        from audit import _run_checklist

        items = _run_checklist(self.CLEAN_CONTENT, "paper.tex", "en", venue="neurips")
        page_item = next((i for i in items if "Page limit" in i.description), None)
        assert page_item is not None

    def test_neurips_blind_review_check(self) -> None:
        from audit import _run_checklist

        items = _run_checklist(self.CLEAN_CONTENT, "paper.tex", "en", venue="neurips")
        blind_item = next((i for i in items if "blind" in i.description.lower()), None)
        assert blind_item is not None

    def test_ieee_abstract_limit(self) -> None:
        from audit import _run_checklist

        items = _run_checklist(self.IEEE_CONTENT, "paper.tex", "en", venue="ieee")
        abs_item = next((i for i in items if "Abstract word limit" in i.description), None)
        assert abs_item is not None
        assert abs_item.passed  # Short abstract should pass

    def test_ieee_keywords(self) -> None:
        from audit import _run_checklist

        items = _run_checklist(self.IEEE_CONTENT, "paper.tex", "en", venue="ieee")
        kw_item = next(
            (i for i in items if "Keywords" in i.description and "IEEE" in i.description), None
        )
        assert kw_item is not None

    def test_ieee_pseudocode_float_checklist_item_fails(self) -> None:
        from audit import _run_checklist

        items = _run_checklist(self.IEEE_FLOAT_ALGO_CONTENT, "paper.tex", "en", venue="ieee")
        pseudo_item = next(
            (i for i in items if "No floating pseudocode environment" in i.description),
            None,
        )
        assert pseudo_item is not None
        assert not pseudo_item.passed

    def test_acm_ccs_missing(self) -> None:
        from audit import _run_checklist

        items = _run_checklist(self.CLEAN_CONTENT, "paper.tex", "en", venue="acm")
        ccs_item = next((i for i in items if "CCS" in i.description), None)
        assert ccs_item is not None
        assert not ccs_item.passed  # Clean content has no CCS

    def test_backward_compat_no_venue_arg(self) -> None:
        """Calling _run_checklist without venue arg still works (default='')."""
        from audit import _run_checklist

        # Should work with positional args only (backward compat)
        items = _run_checklist(self.CLEAN_CONTENT, "paper.tex", "en")
        assert len(items) > 0


def test_run_audit_gate_pseudocode_float_becomes_blocking(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import audit

    tex = tmp_path / "paper.tex"
    tex.write_text(
        TestVenueChecklist.IEEE_FLOAT_ALGO_CONTENT,
        encoding="utf-8",
    )

    def fake_resolve_script(check_name: str, lang: str, fmt: str):
        return Path("check_pseudocode.py" if check_name == "pseudocode" else f"{check_name}.py")

    def fake_run(script: Path, file_path: str, extra_args=None):
        if script.name != "check_pseudocode.py":
            return 0, "", ""
        if extra_args and "--json" in extra_args:
            payload = [
                {
                    "module": "PSEUDOCODE",
                    "line": 10,
                    "severity": "Critical",
                    "priority": "P0",
                    "message": "IEEE-safe pseudocode should not use floating algorithm environments; wrap algorithmic content in a figure instead.",
                }
            ]
            return 1, json.dumps(payload), ""
        return (
            1,
            "% PSEUDOCODE (Line 10) [Severity: Critical] [Priority: P0]: IEEE-safe pseudocode "
            "should not use floating algorithm environments; wrap algorithmic content in a figure instead.",
            "",
        )

    monkeypatch.setattr(audit, "_resolve_script", fake_resolve_script)
    monkeypatch.setattr(audit, "_run_check_script", fake_run)

    result = audit.run_audit(str(tex), mode="gate", lang="en", venue="ieee")

    assert any(
        issue.module == "PSEUDOCODE" and issue.severity == "Critical" for issue in result.issues
    )
    assert any(
        "No floating pseudocode environment" in item.description and not item.passed
        for item in result.checklist
    )


def test_run_audit_gate_keeps_missing_line_numbers_advisory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import audit

    tex = tmp_path / "paper.tex"
    tex.write_text(
        TestVenueChecklist.IEEE_CONTENT,
        encoding="utf-8",
    )

    def fake_resolve_script(check_name: str, lang: str, fmt: str):
        return Path("check_pseudocode.py" if check_name == "pseudocode" else f"{check_name}.py")

    def fake_run(script: Path, file_path: str, extra_args=None):
        if script.name != "check_pseudocode.py":
            return 0, "", ""
        if extra_args and "--json" in extra_args:
            payload = [
                {
                    "module": "PSEUDOCODE",
                    "line": 18,
                    "severity": "Minor",
                    "priority": "P2",
                    "message": "Line numbers were not detected. They are recommended for IEEE-like review but not required.",
                }
            ]
            return 0, json.dumps(payload), ""
        return (
            0,
            "% PSEUDOCODE (Line 18) [Severity: Minor] [Priority: P2]: Line numbers were not "
            "detected. They are recommended for IEEE-like review but not required.",
            "",
        )

    monkeypatch.setattr(audit, "_resolve_script", fake_resolve_script)
    monkeypatch.setattr(audit, "_run_check_script", fake_run)

    result = audit.run_audit(str(tex), mode="gate", lang="en", venue="ieee")

    assert not any(issue.severity == "Critical" for issue in result.issues)
    assert any(
        issue.module == "PSEUDOCODE" and issue.severity == "Minor" for issue in result.issues
    )
    assert all(
        item.passed
        for item in result.checklist
        if "Pseudocode" in item.description or "pseudocode" in item.description
    )


# ============================================================
# Re-audit: parse_previous_report tests
# ============================================================


class TestParsePreviousReport:
    """Tests for _parse_previous_report helper."""

    SAMPLE_REPORT = """\
# Audit Report

| # | Module | Line | Severity | Priority | Issue |
|---|--------|------|----------|----------|-------|
| 1 | FORMAT | 42 | Major | P1 | Inconsistent heading levels |
| 2 | GRAMMAR | 88 | Minor | P2 | Passive voice overuse in abstract |
| 3 | BIB | — | Critical | P0 | Undefined citation key: smith2024 |
"""

    def test_parses_correct_count(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.md"
        report_file.write_text(self.SAMPLE_REPORT, encoding="utf-8")

        from audit import _parse_previous_report

        issues = _parse_previous_report(str(report_file))
        assert len(issues) == 3

    def test_parses_module_and_severity(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.md"
        report_file.write_text(self.SAMPLE_REPORT, encoding="utf-8")

        from audit import _parse_previous_report

        issues = _parse_previous_report(str(report_file))
        assert issues[0]["module"] == "FORMAT"
        assert issues[0]["severity"] == "Major"
        assert issues[2]["module"] == "BIB"
        assert issues[2]["severity"] == "Critical"

    def test_parses_line_numbers(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.md"
        report_file.write_text(self.SAMPLE_REPORT, encoding="utf-8")

        from audit import _parse_previous_report

        issues = _parse_previous_report(str(report_file))
        assert issues[0]["line"] == 42
        assert issues[1]["line"] == 88
        assert issues[2]["line"] is None  # "—" should be None

    def test_parses_messages(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.md"
        report_file.write_text(self.SAMPLE_REPORT, encoding="utf-8")

        from audit import _parse_previous_report

        issues = _parse_previous_report(str(report_file))
        assert "heading levels" in issues[0]["message"]
        assert "smith2024" in issues[2]["message"]

    def test_empty_report(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.md"
        report_file.write_text("# Empty Report\n\nNo issues.\n", encoding="utf-8")

        from audit import _parse_previous_report

        issues = _parse_previous_report(str(report_file))
        assert len(issues) == 0

    def test_parses_root_cause_summary_bullets(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.md"
        report_file.write_text(
            "# Previous Review Summary\n\n"
            "- Root cause `claim-scope-mismatch`: headline claim broader than supported evidence.\n",
            encoding="utf-8",
        )

        from audit import _parse_previous_report

        issues = _parse_previous_report(str(report_file))
        assert len(issues) == 1
        assert issues[0]["root_cause_key"] == "claim-scope-mismatch"
        assert issues[0]["match_strategy"] == "root_cause_summary"
        assert "supported evidence" in issues[0]["message"]

    def test_collect_previous_issues_uses_structured_bundle_when_present(
        self, tmp_path: Path
    ) -> None:
        report_file = tmp_path / "report.md"
        report_file.write_text(
            "# Previous Review Summary\n\n"
            "- Root cause `comparison-asymmetry`: proposed method tuned more aggressively.\n",
            encoding="utf-8",
        )
        (tmp_path / "previous_final_issues.json").write_text(
            json.dumps(
                [
                    {
                        "title": "Comparison protocol is asymmetric",
                        "explanation": "The proposed method receives extra opportunities.",
                        "severity": "moderate",
                        "comment_type": "methodology",
                        "review_lane": "evaluation_fairness_and_reproducibility",
                        "root_cause_key": "comparison-asymmetry",
                    }
                ]
            ),
            encoding="utf-8",
        )

        from audit import _collect_previous_issues

        issues = _collect_previous_issues(str(report_file))
        assert any(issue["match_strategy"] == "structured_issue" for issue in issues)
        assert any(issue["root_cause_key"] == "comparison-asymmetry" for issue in issues)


# ============================================================
# Re-audit: fuzzy matching tests
# ============================================================


class TestFuzzyMatch:
    """Tests for _fuzzy_match_score."""

    def test_identical_strings(self) -> None:
        from audit import _fuzzy_match_score

        assert _fuzzy_match_score("hello world", "hello world") == 1.0

    def test_completely_different(self) -> None:
        from audit import _fuzzy_match_score

        score = _fuzzy_match_score("abc", "xyz")
        assert score < 0.3

    def test_similar_strings(self) -> None:
        from audit import _fuzzy_match_score

        score = _fuzzy_match_score(
            "Inconsistent heading levels",
            "Inconsistent heading level detected",
        )
        assert score >= 0.6

    def test_case_insensitive(self) -> None:
        from audit import _fuzzy_match_score

        assert _fuzzy_match_score("Hello", "hello") == 1.0


# ============================================================
# Re-audit: reaudit classification tests
# ============================================================


class TestReauditClassification:
    """Tests for run_reaudit issue classification logic."""

    def _make_result_with_issues(self, issues: list[AuditIssue]) -> AuditResult:
        return AuditResult(
            file_path="paper.tex",
            language="en",
            mode="re-audit",
            issues=issues,
        )

    def test_fully_addressed(self) -> None:
        """Prior issue not in fresh audit -> FULLY_ADDRESSED."""
        from audit import _MATCH_THRESHOLD, _fuzzy_match_score

        prior = {"module": "FORMAT", "severity": "Major", "message": "Bad heading", "line": 10}
        fresh_issues = [
            AuditIssue(
                module="GRAMMAR", line=20, severity="Minor", priority="P2", message="Passive voice"
            ),
        ]
        # Simulate matching: no FORMAT module match
        best_score = 0.0
        for fi in fresh_issues:
            if fi.module != prior["module"]:
                continue
            score = _fuzzy_match_score(prior["message"], fi.message)
            if score > best_score:
                best_score = score
        assert best_score < _MATCH_THRESHOLD  # No match -> would be FULLY_ADDRESSED

    def test_not_addressed(self) -> None:
        """Prior issue still present at same severity -> NOT_ADDRESSED."""
        from audit import _MATCH_THRESHOLD, _SEVERITY_RANK, _fuzzy_match_score

        prior = {
            "module": "FORMAT",
            "severity": "Major",
            "message": "Bad heading levels",
            "line": 10,
        }
        fresh_issues = [
            AuditIssue(
                module="FORMAT",
                line=10,
                severity="Major",
                priority="P1",
                message="Bad heading levels detected",
            ),
        ]
        best_score = 0.0
        for fi in fresh_issues:
            if fi.module != prior["module"]:
                continue
            score = _fuzzy_match_score(prior["message"], fi.message)
            if score > best_score:
                best_score = score
        assert best_score >= _MATCH_THRESHOLD
        # Same severity -> NOT_ADDRESSED
        prior_rank = _SEVERITY_RANK.get(prior["severity"], 1)
        fresh_rank = _SEVERITY_RANK.get(fresh_issues[0].severity, 1)
        assert fresh_rank >= prior_rank  # NOT_ADDRESSED

    def test_partially_addressed(self) -> None:
        """Prior issue downgraded in severity -> PARTIALLY_ADDRESSED."""
        from audit import _MATCH_THRESHOLD, _SEVERITY_RANK, _fuzzy_match_score

        prior = {
            "module": "FORMAT",
            "severity": "Major",
            "message": "Bad heading levels",
            "line": 10,
        }
        fresh_issues = [
            AuditIssue(
                module="FORMAT",
                line=10,
                severity="Minor",
                priority="P2",
                message="Bad heading levels (minor)",
            ),
        ]
        best_score = _fuzzy_match_score(prior["message"], fresh_issues[0].message)
        assert best_score >= _MATCH_THRESHOLD
        prior_rank = _SEVERITY_RANK.get(prior["severity"], 1)
        fresh_rank = _SEVERITY_RANK.get(fresh_issues[0].severity, 1)
        assert fresh_rank < prior_rank  # PARTIALLY_ADDRESSED


# ============================================================
# Re-audit: render_reaudit_report tests
# ============================================================


class TestRenderReauditReport:
    """Tests for render_reaudit_report."""

    def _make_reaudit_result(self) -> AuditResult:
        return AuditResult(
            file_path="paper.tex",
            language="en",
            mode="re-audit",
            venue="neurips",
            issues=[
                AuditIssue(
                    module="GRAMMAR",
                    line=20,
                    severity="Minor",
                    priority="P2",
                    message="Passive voice",
                ),
            ],
            reaudit_data={
                "previous_report": "report_v1.md",
                "prior_issue_count": 3,
                "classifications": [
                    {
                        "prior_module": "FORMAT",
                        "prior_severity": "Major",
                        "prior_message": "Inconsistent heading levels",
                        "root_cause_key": "heading-hierarchy",
                        "status": "FULLY_ADDRESSED",
                        "current_severity": None,
                        "current_message": None,
                        "match_score": 0.3,
                    },
                    {
                        "prior_module": "BIB",
                        "prior_severity": "Critical",
                        "prior_message": "Undefined citation key",
                        "root_cause_key": "citation-resolution",
                        "status": "FULLY_ADDRESSED",
                        "current_severity": None,
                        "current_message": None,
                        "match_score": 0.2,
                    },
                    {
                        "prior_module": "GRAMMAR",
                        "prior_severity": "Major",
                        "prior_message": "Passive voice overuse",
                        "root_cause_key": "passive-voice-overuse",
                        "status": "PARTIALLY_ADDRESSED",
                        "current_severity": "Minor",
                        "current_message": "Passive voice",
                        "match_score": 0.75,
                    },
                ],
                "new_issues": [],
                "summary": {
                    "fully_addressed": 2,
                    "partially_addressed": 1,
                    "not_addressed": 0,
                    "new": 0,
                },
            },
        )

    def test_report_has_title(self) -> None:
        result = self._make_reaudit_result()
        report = render_reaudit_report(result)
        assert "# Re-Audit Report" in report

    def test_report_has_venue(self) -> None:
        result = self._make_reaudit_result()
        report = render_reaudit_report(result)
        assert "neurips" in report

    def test_report_has_summary_table(self) -> None:
        result = self._make_reaudit_result()
        report = render_reaudit_report(result)
        assert "Fully addressed" in report
        assert "| 2 |" in report  # 2 fully addressed

    def test_report_has_resolution_rate(self) -> None:
        result = self._make_reaudit_result()
        report = render_reaudit_report(result)
        assert "67%" in report  # 2/3 = 67%

    def test_report_has_verification_table(self) -> None:
        result = self._make_reaudit_result()
        report = render_reaudit_report(result)
        assert "Prior Issue Verification" in report
        assert "FULLY_ADDRESSED" in report
        assert "PARTIALLY_ADDRESSED" in report
        assert "heading-hierarchy" in report

    def test_report_has_scores(self) -> None:
        result = self._make_reaudit_result()
        report = render_reaudit_report(result)
        assert "Current Scores" in report
        assert "Overall" in report

    def test_report_dispatches_via_render_report(self) -> None:
        result = self._make_reaudit_result()
        report = render_report(result)
        assert "# Re-Audit Report" in report

    def test_all_resolved_recommendation(self) -> None:
        result = self._make_reaudit_result()
        result.reaudit_data["summary"]["partially_addressed"] = 0
        result.reaudit_data["summary"]["not_addressed"] = 0
        report = render_reaudit_report(result)
        assert "Ready for next step" in report

    def test_unresolved_recommendation(self) -> None:
        result = self._make_reaudit_result()
        result.reaudit_data["summary"]["not_addressed"] = 2
        report = render_reaudit_report(result)
        assert "still unresolved" in report
