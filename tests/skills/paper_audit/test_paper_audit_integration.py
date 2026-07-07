"""Integration tests for the paper-audit consuming pipeline (06-13-paper-audit-integrity, A8/A6).

These exercise the audit pipeline's wiring to the shared parser foundation
rather than the parser units (those live in ``test_en_family_parsers_multifile.py``
and are hash-locked by ``test_parsers_alignment.py``):

- ``prepare_workspace`` runs end-to-end on a multi-section paper and produces
  every ``WorkspaceLayout`` artifact downstream agents consume;
- non-UTF-8 manuscripts are ingested via ``read_text_robust`` (A6) instead of
  crashing the audit at first read.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from paths import WorkspaceLayout

MULTI_SECTION_PAPER = "\n".join(
    [
        r"\documentclass{article}",
        r"\title{A Robust Method for Testing Pipelines}",
        r"\begin{document}",
        r"\maketitle",
        r"\begin{abstract}",
        r"We present a method and report results on standard benchmarks.",
        r"\end{abstract}",
        r"\section{Introduction}",
        r"Prior work is limited; we address that gap directly.",
        r"\section{Method}",
        r"We use a carefully designed approach with explicit assumptions.",
        r"\section{Experiments}",
        r"Our method improves over the baselines by a clear margin.",
        r"\section{Conclusion}",
        r"We conclude and outline future directions.",
        r"\end{document}",
        "",
    ]
)


def test_prepare_workspace_end_to_end_produces_layout_artifacts(tmp_path: Path) -> None:
    """The deep-review workspace builder wires the shared parser to every
    artifact the committee/consolidate/render steps later read."""
    from prepare_review_workspace import prepare_workspace

    paper = tmp_path / "paper.tex"
    paper.write_text(MULTI_SECTION_PAPER, encoding="utf-8")

    workspace = prepare_workspace(str(paper), output_dir=str(tmp_path / "review_results"))
    assert workspace.exists()

    layout = WorkspaceLayout(workspace)
    # The five artifacts prepare_workspace advertises as its initial output.
    for artifact in (
        layout.full_text,
        layout.metadata,
        layout.section_index,
        layout.claim_map,
        layout.paper_summary,
    ):
        assert artifact.exists(), f"prepare_workspace did not produce {artifact.name}"

    # Section bodies were split out for the section-reviewer lane.
    section_files = list(layout.sections_dir.glob("*.md"))
    assert section_files, "expected per-section markdown files under artifacts/sections/"

    full_text = layout.full_text.read_text(encoding="utf-8")
    assert "carefully designed approach" in full_text


def test_prepare_workspace_handles_non_utf8_source(tmp_path: Path) -> None:
    """A latin-1 manuscript (non-UTF-8 bytes) must ingest via the robust reader
    instead of raising UnicodeDecodeError at the first read (A6)."""
    from prepare_review_workspace import prepare_workspace

    paper = tmp_path / "paper_latin1.tex"
    # 0xE9 is 'é' in latin-1 but an invalid standalone UTF-8 byte.
    paper.write_bytes(MULTI_SECTION_PAPER.replace("method", "méthode").encode("latin-1"))

    workspace = prepare_workspace(str(paper), output_dir=str(tmp_path / "review_results"))
    assert workspace.exists()
    assert WorkspaceLayout(workspace).full_text.exists()


def test_read_source_decodes_non_utf8_with_warning(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """audit._read_source returns text for a non-UTF-8 source and warns on stderr
    rather than crashing (A6)."""
    from audit import _read_source

    paper = tmp_path / "weird.tex"
    paper.write_bytes(b"\\section{Intro}\nCaf\xe9 results are strong.\n")

    text = _read_source(paper)
    assert isinstance(text, str)
    assert "results are strong" in text

    captured = capsys.readouterr()
    assert "not UTF-8" in captured.err
