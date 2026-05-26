"""Workspace layout for deep-review artifacts.

Single source of truth for all artifact paths produced by paper-audit. Every
consumer (audit, prepare, consolidate, verify_quotes, render_*) goes through
:class:`WorkspaceLayout` instead of hard-coding filenames so the layout can
evolve in one place.

Layout::

    review_results/{slug}/
    ├── review_report.md            # primary report
    ├── revision_suggestions.md     # primary fix recommendations
    ├── review_report.html
    ├── revision_suggestions.html
    └── artifacts/
        ├── summary/    paper_summary.md, overall_assessment.txt,
        │               peer_review_report.md
        ├── data/       final_issues.json, all_comments.json, claim_map.json,
        │               section_index.json, revision_suggestions.json,
        │               revision_trajectory.md
        ├── meta/       metadata.json, checkpoint.json, phase0_context.md,
        │               full_text.md
        ├── sections/   section_key.md ...
        ├── comments/   lane JSON outputs
        ├── committee/  per-reviewer Markdown
        └── references/ minimal skill-references copy
"""

from __future__ import annotations

from pathlib import Path


class WorkspaceLayout:
    """Resolve every artifact path inside a review workspace."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.artifacts = self.root / "artifacts"

    # ---- Root-level outputs (user-visible) -----------------------------------

    @property
    def review_report_md(self) -> Path:
        return self.root / "review_report.md"

    @property
    def revision_suggestions_md(self) -> Path:
        return self.root / "revision_suggestions.md"

    @property
    def review_report_html(self) -> Path:
        return self.root / "review_report.html"

    @property
    def revision_suggestions_html(self) -> Path:
        return self.root / "revision_suggestions.html"

    # ---- artifacts/summary/ ---------------------------------------------------

    @property
    def summary_dir(self) -> Path:
        return self.artifacts / "summary"

    @property
    def paper_summary(self) -> Path:
        return self.summary_dir / "paper_summary.md"

    @property
    def overall_assessment(self) -> Path:
        return self.summary_dir / "overall_assessment.txt"

    @property
    def peer_review_report(self) -> Path:
        return self.summary_dir / "peer_review_report.md"

    # ---- artifacts/data/ ------------------------------------------------------

    @property
    def data_dir(self) -> Path:
        return self.artifacts / "data"

    @property
    def final_issues(self) -> Path:
        return self.data_dir / "final_issues.json"

    @property
    def all_comments(self) -> Path:
        return self.data_dir / "all_comments.json"

    @property
    def claim_map(self) -> Path:
        return self.data_dir / "claim_map.json"

    @property
    def section_index(self) -> Path:
        return self.data_dir / "section_index.json"

    @property
    def revision_suggestions_json(self) -> Path:
        return self.data_dir / "revision_suggestions.json"

    @property
    def revision_trajectory(self) -> Path:
        return self.data_dir / "revision_trajectory.md"

    # ---- artifacts/meta/ ------------------------------------------------------

    @property
    def meta_dir(self) -> Path:
        return self.artifacts / "meta"

    @property
    def metadata(self) -> Path:
        return self.meta_dir / "metadata.json"

    @property
    def checkpoint(self) -> Path:
        return self.meta_dir / "checkpoint.json"

    @property
    def phase0_context(self) -> Path:
        return self.meta_dir / "phase0_context.md"

    @property
    def full_text(self) -> Path:
        return self.meta_dir / "full_text.md"

    # ---- Lane / reference directories ----------------------------------------

    @property
    def sections_dir(self) -> Path:
        return self.artifacts / "sections"

    @property
    def comments_dir(self) -> Path:
        return self.artifacts / "comments"

    @property
    def committee_dir(self) -> Path:
        return self.artifacts / "committee"

    @property
    def references_dir(self) -> Path:
        return self.artifacts / "references"

    # ---- Helpers --------------------------------------------------------------

    def ensure_dirs(self) -> None:
        """Create every directory needed for a deep-review workspace."""
        for directory in (
            self.artifacts,
            self.summary_dir,
            self.data_dir,
            self.meta_dir,
            self.sections_dir,
            self.comments_dir,
            self.committee_dir,
            self.references_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)

    def section_file(self, file_name: str) -> Path:
        """Return ``sections/{file_name}`` (defensive: strips any path traversal)."""
        return self.sections_dir / Path(file_name).name

    def comment_file(self, file_name: str) -> Path:
        return self.comments_dir / Path(file_name).name

    def committee_file(self, file_name: str) -> Path:
        return self.committee_dir / Path(file_name).name

    def reference_file(self, file_name: str) -> Path:
        return self.references_dir / Path(file_name).name

    def relative_to_root(self, path: Path) -> str:
        """Return ``path`` as a posix-style string relative to the workspace root."""
        return path.resolve().relative_to(self.root.resolve()).as_posix()

    def initial_generated_files(self) -> list[str]:
        """Relative paths produced by :func:`prepare_review_workspace.prepare_workspace`."""
        return sorted(
            self.relative_to_root(path)
            for path in (
                self.full_text,
                self.metadata,
                self.section_index,
                self.claim_map,
                self.paper_summary,
            )
        )


def layout_for(review_dir: Path | str) -> WorkspaceLayout:
    """Return a :class:`WorkspaceLayout` for ``review_dir`` (convenience)."""
    return WorkspaceLayout(review_dir)
