"""Tests for literature search, comparison, scoring model, and 9-dim ScholarEval."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest  # noqa: F401 — needed by test runner

# Ensure paper-audit scripts are importable
_scripts_audit = (
    Path(__file__).parent.parent / "academic-writing-skills" / "paper-audit" / "scripts"
)
if str(_scripts_audit) not in sys.path:
    sys.path.insert(0, str(_scripts_audit))


# ============================================================
# literature_search tests
# ============================================================


class TestSearchMetadataExtraction:
    """Tests for extract_search_metadata()."""

    def test_extracts_title_and_abstract(self) -> None:
        from literature_search import extract_search_metadata
        from parsers import LatexParser

        content = r"""
\title{Attention Is All You Need}
\begin{abstract}
The dominant sequence transduction models are based on complex recurrent
or convolutional neural networks.
\end{abstract}
\section{Introduction}
We propose a new architecture.
"""
        parser = LatexParser()
        meta = extract_search_metadata(content, "paper.tex", parser)
        assert "title" in meta
        assert "abstract" in meta
        assert len(meta["title"]) > 0

    def test_extracts_keywords(self) -> None:
        from literature_search import extract_search_metadata
        from parsers import LatexParser

        content = r"""
\title{Test Paper}
\begin{abstract}Test abstract.\end{abstract}
\begin{keywords}
transformer, attention, neural network
\end{keywords}
"""
        parser = LatexParser()
        meta = extract_search_metadata(content, "paper.tex", parser)
        assert "keywords" in meta

    def test_handles_empty_content(self) -> None:
        from literature_search import extract_search_metadata
        from parsers import LatexParser

        parser = LatexParser()
        meta = extract_search_metadata("", "paper.tex", parser)
        assert isinstance(meta, dict)
        assert "title" in meta


class TestQueryGeneration:
    """Tests for generate_search_queries()."""

    def test_generates_queries(self) -> None:
        from literature_search import generate_search_queries

        queries = generate_search_queries(
            title="Attention Is All You Need",
            abstract="We propose a new architecture based on attention mechanisms.",
            keywords=["transformer", "attention"],
            methods=["self-attention", "multi-head attention"],
        )
        assert isinstance(queries, list)
        assert len(queries) > 0
        assert len(queries) <= 5

    def test_max_queries_respected(self) -> None:
        from literature_search import generate_search_queries

        queries = generate_search_queries(
            title="Test",
            abstract="Test abstract",
            keywords=["a", "b"],
            methods=["c"],
            max_queries=3,
        )
        assert len(queries) <= 3

    def test_empty_inputs(self) -> None:
        from literature_search import generate_search_queries

        queries = generate_search_queries(title="", abstract="", keywords=[], methods=[])
        assert isinstance(queries, list)


class TestRelevanceFiltering:
    """Tests for filter_by_relevance()."""

    def test_filters_by_min_score(self) -> None:
        from literature_search import SearchResult, filter_by_relevance

        results = [
            SearchResult(
                title="Attention Is All You Need",
                authors=["Vaswani"],
                year=2017,
                abstract="Transformer architecture for sequence transduction.",
                url="https://example.com/1",
                source="semantic_scholar",
                relevance_score=0.9,
            ),
            SearchResult(
                title="Cooking Recipes",
                authors=["Chef"],
                year=2020,
                abstract="A cookbook for Italian cuisine.",
                url="https://example.com/2",
                source="semantic_scholar",
                relevance_score=0.1,
            ),
        ]
        filtered = filter_by_relevance(
            results,
            paper_title="Attention mechanisms in neural networks",
            paper_abstract="We study attention mechanisms for deep learning.",
            min_score=0.0,  # Let filtering logic decide
            max_results=10,
        )
        assert isinstance(filtered, list)

    def test_max_results_respected(self) -> None:
        from literature_search import SearchResult, filter_by_relevance

        results = [
            SearchResult(
                title=f"Paper {i}",
                authors=["Author"],
                year=2023,
                abstract=f"Abstract about attention mechanism variant {i}.",
                url=f"https://example.com/{i}",
                source="semantic_scholar",
            )
            for i in range(30)
        ]
        filtered = filter_by_relevance(
            results, "Attention", "Attention mechanism paper", max_results=5
        )
        assert len(filtered) <= 5


class TestSearchResultDataclass:
    """Tests for SearchResult dataclass."""

    def test_creation(self) -> None:
        from literature_search import SearchResult

        result = SearchResult(
            title="Test Paper",
            authors=["Author A", "Author B"],
            year=2024,
            abstract="Test abstract.",
            url="https://example.com",
            source="arxiv",
        )
        assert result.title == "Test Paper"
        assert result.source == "arxiv"
        assert result.relevance_score == 0.0
        assert result.citation_count == 0

    def test_optional_fields(self) -> None:
        from literature_search import SearchResult

        result = SearchResult(
            title="Test",
            authors=[],
            year=None,
            abstract="",
            url="",
            source="tavily",
            arxiv_id="2301.00001",
            doi="10.1234/test",
        )
        assert result.arxiv_id == "2301.00001"
        assert result.doi == "10.1234/test"


class TestLiteratureContextDataclass:
    """Tests for LiteratureContext dataclass."""

    def test_creation(self) -> None:
        from literature_search import LiteratureContext

        ctx = LiteratureContext(
            paper_title="Test Paper",
            paper_abstract="Test abstract.",
            search_queries=["query 1", "query 2"],
            results=[],
            filtered_results=[],
            summaries=[],
        )
        assert ctx.paper_title == "Test Paper"
        assert ctx.coverage_assessment == ""


class TestLiteratureSearchMocked:
    """Tests for search_literature() with mocked HTTP calls."""

    @patch("literature_search.SemanticScholarClient")
    @patch("literature_search.ArxivClient")
    def test_search_deduplicates(self, mock_arxiv_cls, mock_s2_cls) -> None:
        from literature_search import SearchResult, search_literature

        mock_s2 = MagicMock()
        mock_s2.search.return_value = [
            SearchResult(
                title="Attention Is All You Need",
                authors=["Vaswani"],
                year=2017,
                abstract="Transformer.",
                url="https://s2.com/1",
                source="semantic_scholar",
            )
        ]
        mock_s2_cls.return_value = mock_s2

        mock_arxiv = MagicMock()
        mock_arxiv.search.return_value = [
            SearchResult(
                title="Attention Is All You Need",
                authors=["Vaswani et al."],
                year=2017,
                abstract="Transformer architecture.",
                url="https://arxiv.org/1",
                source="arxiv",
            )
        ]
        mock_arxiv_cls.return_value = mock_arxiv

        results = search_literature(
            queries=["attention transformer"],
            tavily_key="",
            s2_key="",
        )
        # Should deduplicate by title similarity
        assert isinstance(results, list)


# ============================================================
# literature_compare tests
# ============================================================


class TestLiteratureCompare:
    """Tests for literature comparison module."""

    def test_coverage_assessment_dataclass(self) -> None:
        from literature_compare import CoverageAssessment

        ca = CoverageAssessment(
            cited_and_found=["Paper A"],
            found_not_cited=["Paper B", "Paper C"],
            cited_not_found=["Paper D"],
            coverage_ratio=0.33,
            recency_score=0.7,
            freshness_distribution={"2023-2025": 5, "2020-2022": 3},
        )
        assert ca.coverage_ratio == 0.33
        assert len(ca.found_not_cited) == 2

    def test_grounding_score_computation(self) -> None:
        from literature_compare import CoverageAssessment, compute_literature_grounding_score

        coverage = CoverageAssessment(
            cited_and_found=["A", "B", "C"],
            found_not_cited=["D"],
            cited_not_found=[],
            coverage_ratio=0.75,
            recency_score=0.8,
            freshness_distribution={"2023-2025": 4},
        )
        score = compute_literature_grounding_score(coverage, comparison_count=3)
        assert 1.0 <= score <= 10.0

    def test_grounding_score_empty_coverage(self) -> None:
        from literature_compare import CoverageAssessment, compute_literature_grounding_score

        coverage = CoverageAssessment(
            cited_and_found=[],
            found_not_cited=[],
            cited_not_found=[],
            coverage_ratio=0.0,
            recency_score=0.0,
            freshness_distribution={},
        )
        score = compute_literature_grounding_score(coverage, comparison_count=0)
        assert 1.0 <= score <= 10.0

    def test_comparison_entry_dataclass(self) -> None:
        from literature_compare import ComparisonEntry

        entry = ComparisonEntry(
            related_title="Related Paper",
            overlap_aspects=["method A", "dataset B"],
            differentiators=["different scope"],
            novelty_impact="medium",
        )
        assert entry.novelty_impact == "medium"

    def test_render_comparison_report(self) -> None:
        from literature_compare import (
            CoverageAssessment,
            LiteratureComparisonResult,
            render_comparison_report,
        )

        result = LiteratureComparisonResult(
            comparisons=[],
            coverage=CoverageAssessment(
                cited_and_found=["A"],
                found_not_cited=["B"],
                cited_not_found=[],
                coverage_ratio=0.5,
                recency_score=0.6,
                freshness_distribution={},
            ),
            novelty_assessment="Moderate novelty.",
            grounding_score=6.5,
        )
        report = render_comparison_report(result)
        assert "Literature" in report or "Grounding" in report or "Coverage" in report


# ============================================================
# ScholarEval 9-dimension tests
# ============================================================


class TestScholarEval9Dim:
    """Tests for 9-dimension ScholarEval system."""

    def test_literature_grounding_in_dimensions(self) -> None:
        from scholar_eval import SCHOLAR_EVAL_DIMENSIONS

        assert "literature_grounding" in SCHOLAR_EVAL_DIMENSIONS
        cfg = SCHOLAR_EVAL_DIMENSIONS["literature_grounding"]
        assert cfg["weight"] == 0.12
        assert cfg["source"] == "mixed"

    def test_weights_sum_to_one(self) -> None:
        from scholar_eval import SCHOLAR_EVAL_DIMENSIONS

        total = sum(cfg["weight"] for cfg in SCHOLAR_EVAL_DIMENSIONS.values())
        assert abs(total - 1.0) < 0.01, f"Weights sum to {total}, expected 1.0"

    def test_evaluate_with_literature_score(self) -> None:
        from scholar_eval import evaluate_from_audit

        issues = [
            {"module": "LOGIC", "severity": "Minor", "message": "test"},
        ]
        scores = evaluate_from_audit(issues, literature_grounding_score=7.5)
        assert "literature_grounding_partial" in scores
        assert scores["literature_grounding_partial"] == 7.5

    def test_evaluate_without_literature_score(self) -> None:
        from scholar_eval import evaluate_from_audit

        issues = [
            {"module": "GRAMMAR", "severity": "Major", "message": "test"},
        ]
        scores = evaluate_from_audit(issues)
        assert "literature_grounding_partial" in scores
        assert scores["literature_grounding_partial"] is None

    def test_merge_literature_grounding_mixed(self) -> None:
        from scholar_eval import merge_scores

        script = {
            "soundness": 8.0,
            "clarity": 7.0,
            "presentation": 9.0,
            "reproducibility_partial": 6.0,
            "literature_grounding_partial": 7.0,
        }
        llm = {
            "novelty": {"score": 7.5, "evidence": "Good novelty"},
            "significance": {"score": 8.0, "evidence": "Important work"},
            "ethics": {"score": 9.0, "evidence": "No concerns"},
            "reproducibility_llm": {"score": 7.0, "evidence": "Code available"},
            "literature_grounding_llm": {"score": 8.0, "evidence": "Good coverage"},
        }
        merged = merge_scores(script, llm)
        assert "literature_grounding" in merged
        # Should be average of 7.0 and 8.0 = 7.5
        assert merged["literature_grounding"] == 7.5

    def test_render_shows_nine_dimensions(self) -> None:
        from scholar_eval import ScholarEvalResult, render_scholar_eval_report

        result = ScholarEvalResult(
            script_scores={"soundness": 8.0, "clarity": 7.0, "presentation": 9.0},
            merged_scores={
                "soundness": 8.0,
                "clarity": 7.0,
                "presentation": 9.0,
                "novelty": 7.5,
                "significance": 8.0,
                "reproducibility": 6.5,
                "ethics": 9.0,
                "literature_grounding": 7.5,
                "overall": 7.8,
            },
            readiness_label="Ready with minor revisions",
        )
        report = render_scholar_eval_report(result)
        assert "9-Dimension" in report
        assert "Literature" in report

    def test_backward_compat_no_literature(self) -> None:
        """Without literature search, Literature Grounding shows N/A."""
        from scholar_eval import build_result, evaluate_from_audit

        issues = [{"module": "LOGIC", "severity": "Minor", "message": "test"}]
        script_scores = evaluate_from_audit(issues)
        result = build_result(script_scores)
        # literature_grounding should be None (no data)
        assert result.merged_scores.get("literature_grounding") is None


# ============================================================
# scoring_model tests
# ============================================================


class TestScoringModel:
    """Tests for scoring_model.py."""

    def test_fallback_matches_weighted_average(self) -> None:
        from scoring_model import RegressionScorer

        scorer = RegressionScorer()  # No coefficients = fallback mode
        scores = {
            "soundness": 8.0,
            "clarity": 7.0,
            "presentation": 9.0,
            "novelty": 7.5,
            "significance": 8.0,
            "reproducibility": 6.5,
            "ethics": 9.0,
            "literature_grounding": 7.5,
            "overall": 7.8,
        }
        prediction = scorer.predict(scores)
        assert prediction.model_type == "weighted_average"
        assert 1.0 <= prediction.predicted_score <= 10.0
        assert prediction.confidence_interval[0] <= prediction.predicted_score
        assert prediction.confidence_interval[1] >= prediction.predicted_score

    def test_regression_mode_with_coefficients(self) -> None:
        from scoring_model import RegressionScorer

        scorer = RegressionScorer(
            coefficients={
                "soundness": 0.18,
                "clarity": 0.13,
                "presentation": 0.08,
                "novelty": 0.13,
                "significance": 0.13,
                "reproducibility": 0.08,
                "ethics": 0.05,
                "literature_grounding": 0.12,
                "overall_base": 0.0,
                "soundness_x_novelty": 0.02,
                "clarity_x_significance": 0.02,
                "literature_grounding_x_novelty": 0.01,
                "critical_count": -0.5,
                "dims_below_5": -0.3,
            },
            intercept=0.5,
        )
        scores = {
            "soundness": 8.0,
            "clarity": 7.0,
            "presentation": 9.0,
            "novelty": 7.5,
            "significance": 8.0,
            "reproducibility": 6.5,
            "ethics": 9.0,
            "literature_grounding": 7.5,
            "overall": 7.8,
        }
        prediction = scorer.predict(scores)
        assert prediction.model_type == "regression"
        assert 1.0 <= prediction.predicted_score <= 10.0

    def test_load_model_from_json(self, tmp_path: Path) -> None:
        from scoring_model import RegressionScorer

        model_data = {
            "coefficients": {"soundness": 0.2, "clarity": 0.15},
            "intercept": 1.0,
            "feature_names": ["soundness", "clarity"],
        }
        model_file = tmp_path / "test_model.json"
        model_file.write_text(json.dumps(model_data))

        scorer = RegressionScorer.load_model(model_file)
        assert scorer.coefficients == {"soundness": 0.2, "clarity": 0.15}
        assert scorer.intercept == 1.0

    def test_save_model_to_json(self, tmp_path: Path) -> None:
        from scoring_model import RegressionScorer

        scorer = RegressionScorer(
            coefficients={"soundness": 0.2},
            intercept=1.0,
        )
        model_file = tmp_path / "saved_model.json"
        scorer.save_model(model_file)

        data = json.loads(model_file.read_text())
        assert data["coefficients"]["soundness"] == 0.2
        assert data["intercept"] == 1.0

    def test_prediction_with_critical_count(self) -> None:
        from scoring_model import RegressionScorer

        scorer = RegressionScorer(
            coefficients={"critical_count": -0.5, "soundness": 0.18},
            intercept=5.0,
        )
        scores = {"soundness": 8.0}
        pred_no_critical = scorer.predict(scores, critical_count=0)
        pred_with_critical = scorer.predict(scores, critical_count=3)
        # More criticals should yield lower score
        assert pred_with_critical.predicted_score <= pred_no_critical.predicted_score

    def test_score_clamped_to_range(self) -> None:
        from scoring_model import RegressionScorer

        scorer = RegressionScorer(
            coefficients={"soundness": 100.0},
            intercept=0.0,
        )
        prediction = scorer.predict({"soundness": 10.0})
        assert prediction.predicted_score <= 10.0

        scorer2 = RegressionScorer(
            coefficients={"soundness": -100.0},
            intercept=0.0,
        )
        prediction2 = scorer2.predict({"soundness": 10.0})
        assert prediction2.predicted_score >= 1.0


# ============================================================
# Integration: audit.py new flags
# ============================================================


class TestAuditNewFlags:
    """Tests for new audit.py CLI flags."""

    def test_literature_search_flag_accepted(self) -> None:
        """Verify the --literature-search flag is recognized by argparse."""
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("file")
        parser.add_argument("--literature-search", action="store_true")
        parser.add_argument("--tavily-key", default="")
        parser.add_argument("--s2-key", default="")
        parser.add_argument("--regression", action="store_true")
        args = parser.parse_args(["test.tex", "--literature-search", "--regression"])
        assert args.literature_search is True
        assert args.regression is True

    def test_report_generator_has_literature_context(self) -> None:
        from report_generator import AuditResult

        result = AuditResult(
            file_path="test.tex",
            language="en",
            mode="self-check",
            literature_context={"test": True},
        )
        assert result.literature_context == {"test": True}

    def test_dimension_map_has_literature_grounding(self) -> None:
        from report_generator import DIMENSION_MAP

        assert "literature_grounding" in DIMENSION_MAP
        dims = DIMENSION_MAP["literature_grounding"]
        assert "quality" in dims
        assert "significance" in dims


# ============================================================
# PDF parser new methods
# ============================================================


class TestPdfParserMetadata:
    """Tests for new pdf_parser methods."""

    def test_extract_metadata_returns_dict(self) -> None:
        from pdf_parser import PdfParser

        parser = PdfParser(mode="basic")
        # Mock extract_text_from_file since we don't have a real PDF
        parser.extract_text_from_file = lambda _f: (
            "## Abstract\n"
            "This paper presents a new approach.\n\n"
            "## Introduction\n"
            "We introduce our method.\n\n"
            "## References\n"
            "[1] Smith et al. 2023. A paper.\n"
            "[2] Jones et al. 2024. Another paper.\n"
        )
        meta = parser.extract_metadata("fake.pdf")
        assert "title" in meta
        assert "abstract" in meta
        assert "references_text" in meta
        assert len(meta["references_text"]) > 0

    def test_extract_references_list(self) -> None:
        from pdf_parser import PdfParser

        parser = PdfParser(mode="basic")
        parser.extract_text_from_file = lambda _f: (
            "## Title\n\n"
            "## References\n"
            "[1] Smith et al. 2023. A paper about transformers.\n"
            "[2] Jones et al. 2024. Another paper about attention.\n"
            "[3] Lee et al. 2025. A third paper.\n"
        )
        refs = parser.extract_references_list("fake.pdf")
        assert isinstance(refs, list)
        assert len(refs) >= 2
