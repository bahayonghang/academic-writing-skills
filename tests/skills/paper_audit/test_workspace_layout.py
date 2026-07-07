"""Tests for paper-audit WorkspaceLayout (paths.py)."""

from __future__ import annotations

import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_AUDIT

if str(SCRIPT_DIR_AUDIT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR_AUDIT))

from paths import WorkspaceLayout, layout_for


def test_workspace_layout_root_files(tmp_path: Path) -> None:
    layout = WorkspaceLayout(tmp_path)
    assert layout.review_report_md == tmp_path / "review_report.md"
    assert layout.revision_suggestions_md == tmp_path / "revision_suggestions.md"
    assert layout.review_report_html == tmp_path / "review_report.html"
    assert layout.revision_suggestions_html == tmp_path / "revision_suggestions.html"


def test_workspace_layout_artifact_paths(tmp_path: Path) -> None:
    layout = WorkspaceLayout(tmp_path)
    assert layout.metadata == tmp_path / "artifacts" / "meta" / "metadata.json"
    assert layout.checkpoint == tmp_path / "artifacts" / "meta" / "checkpoint.json"
    assert layout.full_text == tmp_path / "artifacts" / "meta" / "full_text.md"
    assert layout.phase0_context == tmp_path / "artifacts" / "meta" / "phase0_context.md"
    assert layout.final_issues == tmp_path / "artifacts" / "data" / "final_issues.json"
    assert layout.all_comments == tmp_path / "artifacts" / "data" / "all_comments.json"
    assert layout.claim_map == tmp_path / "artifacts" / "data" / "claim_map.json"
    assert layout.section_index == tmp_path / "artifacts" / "data" / "section_index.json"
    assert (
        layout.revision_suggestions_json
        == tmp_path / "artifacts" / "data" / "revision_suggestions.json"
    )
    assert layout.paper_summary == tmp_path / "artifacts" / "summary" / "paper_summary.md"
    assert (
        layout.overall_assessment == tmp_path / "artifacts" / "summary" / "overall_assessment.txt"
    )
    assert layout.peer_review_report == tmp_path / "artifacts" / "summary" / "peer_review_report.md"


def test_workspace_layout_subdirs(tmp_path: Path) -> None:
    layout = WorkspaceLayout(tmp_path)
    assert layout.sections_dir == tmp_path / "artifacts" / "sections"
    assert layout.comments_dir == tmp_path / "artifacts" / "comments"
    assert layout.committee_dir == tmp_path / "artifacts" / "committee"
    assert layout.references_dir == tmp_path / "artifacts" / "references"


def test_ensure_dirs_is_idempotent(tmp_path: Path) -> None:
    layout = WorkspaceLayout(tmp_path)
    layout.ensure_dirs()
    assert layout.artifacts.is_dir()
    assert layout.data_dir.is_dir()
    assert layout.summary_dir.is_dir()
    assert layout.meta_dir.is_dir()
    assert layout.sections_dir.is_dir()
    assert layout.comments_dir.is_dir()
    assert layout.committee_dir.is_dir()
    assert layout.references_dir.is_dir()
    # Second call must not raise
    layout.ensure_dirs()


def test_section_file_strips_path_traversal(tmp_path: Path) -> None:
    layout = WorkspaceLayout(tmp_path)
    assert layout.section_file("../../etc/passwd") == layout.sections_dir / "passwd"
    assert layout.section_file("intro.md") == layout.sections_dir / "intro.md"


def test_relative_to_root(tmp_path: Path) -> None:
    layout = WorkspaceLayout(tmp_path)
    layout.ensure_dirs()
    layout.final_issues.write_text("[]", encoding="utf-8")
    assert layout.relative_to_root(layout.final_issues) == "artifacts/data/final_issues.json"


def test_initial_generated_files_lists_relative_paths(tmp_path: Path) -> None:
    layout = WorkspaceLayout(tmp_path)
    layout.ensure_dirs()
    for path in (
        layout.full_text,
        layout.metadata,
        layout.section_index,
        layout.claim_map,
        layout.paper_summary,
    ):
        path.write_text("", encoding="utf-8")
    files = layout.initial_generated_files()
    assert "artifacts/meta/full_text.md" in files
    assert "artifacts/meta/metadata.json" in files
    assert "artifacts/data/section_index.json" in files
    assert "artifacts/data/claim_map.json" in files
    assert "artifacts/summary/paper_summary.md" in files


def test_layout_for_shortcut(tmp_path: Path) -> None:
    layout = layout_for(tmp_path)
    assert isinstance(layout, WorkspaceLayout)
    assert layout.root == tmp_path
