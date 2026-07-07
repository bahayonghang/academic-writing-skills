"""Tests for paper-audit deep-review checkpoint protocol (stage 6)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from checkpoint import (
    CHECKPOINT_VERSION,
    DEFAULT_PHASES,
    VALID_STATUSES,
    init_checkpoint,
    load_checkpoint,
    mark_lane_completed,
    mark_lane_suspended,
    mark_phase,
    register_generated_file,
    reset_checkpoint,
    save_checkpoint,
    set_status,
    summarize_checkpoint,
)
from paths import WorkspaceLayout

from tests.support.paths import SCRIPT_DIR_AUDIT


def test_init_checkpoint_writes_default_schema(tmp_path: Path) -> None:
    payload = init_checkpoint(tmp_path)

    assert payload["version"] == CHECKPOINT_VERSION
    assert payload["status"] == "prepared"
    assert payload["phase_index"] == 1
    assert [p["name"] for p in payload["phases"]] == list(DEFAULT_PHASES)
    assert payload["phases"][0]["status"] == "completed"  # prepare auto-marked
    assert all(p["status"] == "pending" for p in payload["phases"][1:])
    assert payload["completed_lanes"] == []
    assert payload["suspended_lanes"] == []
    assert payload["generated_files"] == []
    assert WorkspaceLayout(tmp_path).checkpoint.is_file()


def test_init_checkpoint_records_generated_files_sorted(tmp_path: Path) -> None:
    payload = init_checkpoint(tmp_path, generated_files=["b.json", "a.json", "b.json"])
    assert payload["generated_files"] == ["a.json", "b.json"]


def test_load_checkpoint_returns_none_when_missing(tmp_path: Path) -> None:
    assert load_checkpoint(tmp_path) is None


def test_save_checkpoint_refreshes_updated_at(tmp_path: Path) -> None:
    init_checkpoint(tmp_path)
    payload = load_checkpoint(tmp_path)
    assert payload is not None
    first = payload["updated_at"]
    save_checkpoint(tmp_path, payload)
    refreshed = load_checkpoint(tmp_path)
    assert refreshed is not None
    assert refreshed["updated_at"] >= first


def test_mark_phase_updates_named_status(tmp_path: Path) -> None:
    init_checkpoint(tmp_path)
    mark_phase(tmp_path, "phase0_audit", "completed")
    payload = load_checkpoint(tmp_path)
    assert payload is not None
    phase = next(p for p in payload["phases"] if p["name"] == "phase0_audit")
    assert phase["status"] == "completed"


def test_mark_phase_rejects_unknown_phase(tmp_path: Path) -> None:
    init_checkpoint(tmp_path)
    with pytest.raises(ValueError):
        mark_phase(tmp_path, "nonexistent_phase", "completed")


def test_mark_lane_completed_and_suspended_are_mutually_exclusive(tmp_path: Path) -> None:
    init_checkpoint(tmp_path)
    mark_lane_suspended(tmp_path, "claims_vs_evidence")
    payload = load_checkpoint(tmp_path)
    assert payload is not None
    assert "claims_vs_evidence" in payload["suspended_lanes"]
    assert payload["status"] == "suspended"

    mark_lane_completed(tmp_path, "claims_vs_evidence")
    payload = load_checkpoint(tmp_path)
    assert payload is not None
    assert "claims_vs_evidence" in payload["completed_lanes"]
    assert "claims_vs_evidence" not in payload["suspended_lanes"]


def test_mark_lane_suspended_no_op_when_already_completed(tmp_path: Path) -> None:
    init_checkpoint(tmp_path)
    mark_lane_completed(tmp_path, "claims_vs_evidence")
    mark_lane_suspended(tmp_path, "claims_vs_evidence")  # should not flip
    payload = load_checkpoint(tmp_path)
    assert payload is not None
    assert payload["completed_lanes"] == ["claims_vs_evidence"]
    assert payload["suspended_lanes"] == []


def test_register_generated_file_is_idempotent(tmp_path: Path) -> None:
    init_checkpoint(tmp_path)
    register_generated_file(tmp_path, "review_report.md")
    register_generated_file(tmp_path, "review_report.md")
    register_generated_file(tmp_path, "all_comments.json")
    payload = load_checkpoint(tmp_path)
    assert payload is not None
    assert payload["generated_files"] == ["all_comments.json", "review_report.md"]


def test_set_status_validates_against_enum(tmp_path: Path) -> None:
    init_checkpoint(tmp_path)
    for status in VALID_STATUSES:
        set_status(tmp_path, status)
        payload = load_checkpoint(tmp_path)
        assert payload is not None
        assert payload["status"] == status
    with pytest.raises(ValueError):
        set_status(tmp_path, "bogus")


def test_reset_checkpoint_clears_progress_but_preserves_generated_files(
    tmp_path: Path,
) -> None:
    init_checkpoint(tmp_path, generated_files=["full_text.md"])
    mark_lane_completed(tmp_path, "claims_vs_evidence")
    mark_phase(tmp_path, "lanes", "completed")
    set_status(tmp_path, "suspended")

    reset_checkpoint(tmp_path)
    payload = load_checkpoint(tmp_path)
    assert payload is not None
    assert payload["status"] == "prepared"
    assert payload["completed_lanes"] == []
    assert payload["suspended_lanes"] == []
    assert payload["generated_files"] == ["full_text.md"]


def test_summarize_checkpoint_format() -> None:
    payload = {
        "status": "suspended",
        "phase_index": 3,
        "completed_lanes": ["a", "b"],
        "suspended_lanes": ["c"],
    }
    line = summarize_checkpoint(payload)
    assert line.startswith("[checkpoint] ")
    assert "status=suspended" in line
    assert "phase_index=3" in line
    assert "lanes_completed=2" in line
    assert "lanes_suspended=1" in line


def test_audit_cli_no_resume_resets_checkpoint(tmp_path: Path) -> None:
    review_dir = tmp_path / "review"
    review_dir.mkdir()
    init_checkpoint(review_dir, generated_files=["full_text.md"])
    mark_lane_completed(review_dir, "claims_vs_evidence")
    set_status(review_dir, "suspended")

    # The audit CLI still needs a source file argument; --no-resume now resets
    # the checkpoint before the normal deep-review resume path continues.
    placeholder = tmp_path / "paper.tex"
    placeholder.write_text("\\section{Stub}\n", encoding="utf-8")

    script = SCRIPT_DIR_AUDIT / "audit.py"

    proc = subprocess.run(
        [
            sys.executable,
            "-B",
            str(script),
            str(placeholder),
            "--mode",
            "deep-review",
            "--review-dir",
            str(review_dir),
            "--no-resume",
        ],
        capture_output=True,
        text=True,
    )

    payload = json.loads(WorkspaceLayout(review_dir).checkpoint.read_text(encoding="utf-8"))
    assert payload["status"] == "prepared"
    assert payload["completed_lanes"] == []
    assert payload["generated_files"] == ["full_text.md"]
    assert "[checkpoint] reset" in proc.stdout


def test_audit_cli_without_review_dir_does_not_touch_checkpoint(tmp_path: Path) -> None:
    """Sanity: omitting --review-dir keeps the audit path identical to before."""
    placeholder = tmp_path / "paper.tex"
    placeholder.write_text("\\section{Stub}\n", encoding="utf-8")

    script = SCRIPT_DIR_AUDIT / "audit.py"

    proc = subprocess.run(
        [
            sys.executable,
            "-B",
            str(script),
            str(placeholder),
            "--mode",
            "deep-review",
        ],
        capture_output=True,
        text=True,
    )

    # No checkpoint chatter should appear on stdout when --review-dir is absent.
    assert "[checkpoint]" not in proc.stdout


def test_prepare_review_workspace_refuses_implicit_overwrite(tmp_path: Path) -> None:
    from prepare_review_workspace import prepare_workspace

    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"""
\title{Overwrite Safety Test}
\begin{document}
\begin{abstract}We test workspace overwrite safety.\end{abstract}
\section{Introduction}
Content.
\end{document}
""".strip(),
        encoding="utf-8",
    )
    output_dir = tmp_path / "review_results"
    workspace = prepare_workspace(str(tex), output_dir=str(output_dir))
    sentinel = workspace / "sentinel.txt"
    sentinel.write_text("keep", encoding="utf-8")

    with pytest.raises(FileExistsError):
        prepare_workspace(str(tex), output_dir=str(output_dir))

    assert sentinel.exists()


def test_prepare_review_workspace_allows_explicit_overwrite(tmp_path: Path) -> None:
    from prepare_review_workspace import prepare_workspace

    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"""
\title{Overwrite Safety Test}
\begin{document}
\begin{abstract}We test workspace overwrite safety.\end{abstract}
\section{Introduction}
Content.
\end{document}
""".strip(),
        encoding="utf-8",
    )
    output_dir = tmp_path / "review_results"
    workspace = prepare_workspace(str(tex), output_dir=str(output_dir))
    sentinel = workspace / "sentinel.txt"
    sentinel.write_text("replace", encoding="utf-8")

    overwritten = prepare_workspace(str(tex), output_dir=str(output_dir), overwrite=True)

    assert overwritten == workspace
    assert not sentinel.exists()


def test_run_deep_review_resume_skips_completed_lane(tmp_path: Path) -> None:
    from audit import run_deep_review
    from prepare_review_workspace import prepare_workspace

    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"""
\title{Resume Test}
\begin{document}
\begin{abstract}
We show significant gains over prior work.
\end{abstract}
\section{Introduction}
This paper claims broad superiority over prior work.
\section{Method}
We define x as the latent state and assume a fixed calibration constant.
\section{Results}
Our method improves accuracy by 12.4 over the baseline.
\section{Conclusion}
We conclude the method is broadly superior.
\end{document}
""".strip(),
        encoding="utf-8",
    )
    review_dir = prepare_workspace(str(tex), output_dir=str(tmp_path / "review_results"))
    layout = WorkspaceLayout(review_dir)
    sentinel = [
        {
            "title": "Sentinel claim review",
            "quote": "This paper claims broad superiority over prior work.",
            "explanation": "Pre-existing reviewer output must survive resume.",
            "comment_type": "claim_accuracy",
            "severity": "moderate",
            "confidence": "high",
            "source_kind": "llm",
            "source_section": "introduction",
            "related_sections": ["introduction"],
            "review_lane": "claims_vs_evidence",
            "gate_blocker": False,
        }
    ]
    comments_dir = layout.comments_dir
    comments_dir.mkdir(parents=True, exist_ok=True)
    sentinel_path = comments_dir / "claims_vs_evidence.json"
    sentinel_path.write_text(json.dumps(sentinel, indent=2), encoding="utf-8")
    mark_lane_completed(review_dir, "claims_vs_evidence")
    set_status(review_dir, "suspended")

    result = run_deep_review(str(tex), lang="en", review_dir=str(review_dir))

    assert result.artifact_dir == str(review_dir.resolve())
    assert json.loads(sentinel_path.read_text(encoding="utf-8")) == sentinel
    assert layout.final_issues.exists()
    assert layout.review_report_md.exists()
    assert (layout.committee_dir / "consensus.md").exists()

    checkpoint = load_checkpoint(review_dir)
    assert checkpoint is not None
    assert checkpoint["status"] == "completed"
    assert "claims_vs_evidence" in checkpoint["completed_lanes"]
    assert "artifacts/meta/phase0_context.md" in checkpoint["generated_files"]
    assert "artifacts/data/final_issues.json" in checkpoint["generated_files"]
    assert "review_report.md" in checkpoint["generated_files"]
    assert any(issue.title == "Sentinel claim review" for issue in result.issue_bundle)
