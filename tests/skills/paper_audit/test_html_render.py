"""Tests for paper-audit HTML rendering."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from tests.support.paths import SCRIPT_DIR_AUDIT

if str(SCRIPT_DIR_AUDIT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR_AUDIT))

try:
    import jinja2  # noqa: F401
except ImportError:  # pragma: no cover - dependency not installed in this env
    pytest.skip("Jinja2 not installed", allow_module_level=True)

from paths import WorkspaceLayout
from render_html_report import render_html_reports


def _seed_workspace(root: Path, *, language: str = "en") -> WorkspaceLayout:
    """Materialise the minimum artifacts that load_result + the HTML templates need."""
    layout = WorkspaceLayout(root)
    layout.ensure_dirs()
    layout.metadata.write_text(
        json.dumps(
            {
                "slug": "fixture",
                "title": "Fixture Paper",
                "source_path": "/tmp/fixture.tex",
                "language": language,
                "format": ".tex",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    layout.section_index.write_text(
        json.dumps(
            [
                {
                    "section_key": "introduction",
                    "title": "Introduction",
                    "start_line": 1,
                    "end_line": 12,
                    "line_base": 1,
                    "word_count": 50,
                    "char_count": 250,
                    "file_name": "introduction.md",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    layout.full_text.write_text("placeholder text for fixture.", encoding="utf-8")
    layout.paper_summary.write_text(
        "# Paper Summary: Fixture\n\n## Research Question\n- demo question\n",
        encoding="utf-8",
    )
    layout.overall_assessment.write_text(
        "Fixture overall assessment for HTML render test.",
        encoding="utf-8",
    )
    layout.final_issues.write_text(
        json.dumps(
            [
                {
                    "title": "Headline claim too strong",
                    "quote": "we achieve state-of-the-art across all benchmarks",
                    "explanation": "The current evidence does not support a universal claim.",
                    "comment_type": "claim_accuracy",
                    "severity": "major",
                    "confidence": "high",
                    "source_kind": "llm",
                    "source_section": "introduction",
                    "related_sections": ["abstract"],
                    "root_cause_key": "claim-scope-mismatch",
                    "review_lane": "claims_vs_evidence",
                    "gate_blocker": True,
                    "quote_verified": True,
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    layout.revision_suggestions_md.write_text(
        "# Revision Suggestions\n\n## Priority 1\n\n- [ ] Soften the headline claim "
        "([LLM]; introduction)\n",
        encoding="utf-8",
    )
    layout.revision_suggestions_json.write_text(
        json.dumps(
            [
                {
                    "issue_id": "M1",
                    "title": "Headline claim too strong",
                    "root_cause_key": "claim-scope-mismatch",
                    "severity": "major",
                    "section": "introduction",
                    "original_text": "we achieve state-of-the-art across all benchmarks",
                    "suggested_text": (
                        "we observe improved performance in the reported benchmarks"
                    ),
                    "rationale": "The wording must stay within the evaluated setting.",
                    "additional_actions": ["Add a benchmarks-vs-claims table"],
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return layout


def test_render_html_reports_writes_both_files_in_english(tmp_path: Path) -> None:
    layout = _seed_workspace(tmp_path, language="en")
    review_html_path, revision_html_path = render_html_reports(tmp_path, lang="en")

    assert review_html_path == layout.review_report_html
    assert revision_html_path == layout.revision_suggestions_html
    assert review_html_path.exists()
    assert revision_html_path.exists()

    review_html = review_html_path.read_text(encoding="utf-8")
    assert "Deep Review Report" in review_html
    assert "Headline claim too strong" in review_html
    assert "severity-major" in review_html
    # Original quote must survive verbatim
    assert "we achieve state-of-the-art" in review_html

    revision_html = revision_html_path.read_text(encoding="utf-8")
    assert "Revision Suggestions" in revision_html
    assert "Suggested rewrite" in revision_html
    assert "improved performance" in revision_html


def test_render_html_reports_localizes_chinese(tmp_path: Path) -> None:
    _seed_workspace(tmp_path, language="zh")
    review_html_path, revision_html_path = render_html_reports(tmp_path, lang="zh")
    review_html = review_html_path.read_text(encoding="utf-8")
    revision_html = revision_html_path.read_text(encoding="utf-8")
    # Section headings localised to Chinese
    assert "深度审稿报告" in review_html
    assert "修订建议" in revision_html
    # Quote still in original language
    assert "state-of-the-art" in review_html
