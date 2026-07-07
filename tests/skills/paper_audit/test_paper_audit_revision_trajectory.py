"""Tests for paper-audit revision trajectory rendering and bundle wrapping."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from diff_review_issues import load_issues
from render_revision_trajectory import (
    DEGRADATION_THRESHOLD,
    load_bundle,
    normalize_scores,
    render_trajectory,
    write_trajectory,
)

from tests.support.paths import SCRIPT_DIR_AUDIT


def _write_json(path: Path, payload: object) -> Path:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def test_load_bundle_accepts_legacy_list(tmp_path: Path) -> None:
    path = _write_json(tmp_path / "old.json", [{"title": "x", "root_cause_key": "k"}])
    issues, scores = load_bundle(path)
    assert issues == [{"title": "x", "root_cause_key": "k"}]
    assert scores == {}


def test_load_bundle_unwraps_dict_with_round_scores(tmp_path: Path) -> None:
    payload = {
        "issues": [{"title": "y"}],
        "round_scores": {"quality": 72, "clarity": 70},
    }
    path = _write_json(tmp_path / "new.json", payload)
    issues, scores = load_bundle(path)
    assert issues == [{"title": "y"}]
    assert scores == {"quality": 72, "clarity": 70}


def test_normalize_scores_drops_non_numeric() -> None:
    raw = {"quality": "78", "clarity": 73, "broken": "n/a", "missing": None}
    assert normalize_scores(raw) == {"quality": 78.0, "clarity": 73.0}


def test_render_trajectory_returns_empty_when_no_scores() -> None:
    assert render_trajectory({}, {}) == ""


def test_render_trajectory_flags_per_dimension_drop() -> None:
    previous = {"quality": 78.0, "clarity": 75.0, "originality": 70.0}
    current = {"quality": 78.0, "clarity": 70.0, "originality": 66.0}

    table = render_trajectory(previous, current)

    assert "Round" in table
    assert "| R1 | 78 | 75 | 70 |" in table
    # clarity dropped exactly threshold => flagged
    assert "70 ⚠️↓" in table
    # originality dropped only 4 (< threshold) => no flag
    assert "66 |" in table
    assert "66 ⚠️↓" not in table


def test_render_trajectory_respects_custom_threshold() -> None:
    previous = {"quality": 80.0}
    current = {"quality": 77.0}

    relaxed = render_trajectory(previous, current, threshold=5.0)
    strict = render_trajectory(previous, current, threshold=2.0)

    assert "77 ⚠️↓" not in relaxed
    assert "77 ⚠️↓" in strict


def test_render_trajectory_unions_dimensions() -> None:
    previous = {"quality": 70.0}
    current = {"clarity": 72.0}

    table = render_trajectory(previous, current)

    # Header should keep R1-first dimensions before new ones from R2
    header_line = table.splitlines()[0]
    assert header_line.index("quality") < header_line.index("clarity")
    # Missing values render as "-"
    assert "| - |" in table


def test_write_trajectory_skips_when_no_scores(tmp_path: Path) -> None:
    previous = _write_json(tmp_path / "prev.json", [])
    current = _write_json(tmp_path / "cur.json", {"issues": []})
    output = tmp_path / "revision_trajectory.md"

    body = write_trajectory(previous, current, output)

    assert body == ""
    assert not output.exists()


def test_write_trajectory_emits_markdown_with_header(tmp_path: Path) -> None:
    previous = _write_json(
        tmp_path / "prev.json",
        {"issues": [], "round_scores": {"quality": 72, "clarity": 75}},
    )
    current = _write_json(
        tmp_path / "cur.json",
        {"issues": [], "round_scores": {"quality": 78, "clarity": 70}},
    )
    output = tmp_path / "revision_trajectory.md"

    body = write_trajectory(previous, current, output)

    assert output.exists()
    assert "# Revision Score Trajectory" in body
    assert f"{DEGRADATION_THRESHOLD:g}" in body
    # clarity dropped 5 => flagged
    assert "70 ⚠️↓" in body
    # quality improved => unflagged
    assert "| R2 | 78 |" in body


def test_diff_review_issues_load_issues_accepts_dict(tmp_path: Path) -> None:
    payload = {
        "issues": [{"title": "claim drift", "root_cause_key": "claim-scope-mismatch"}],
        "round_scores": {"quality": 72},
    }
    path = _write_json(tmp_path / "bundle.json", payload)
    assert load_issues(path) == payload["issues"]


def test_diff_review_issues_cli_writes_trajectory_alongside_current(tmp_path: Path) -> None:
    previous = _write_json(
        tmp_path / "prev.json",
        {
            "issues": [{"title": "p", "root_cause_key": "k", "severity": "major"}],
            "round_scores": {"quality": 80, "clarity": 75},
        },
    )
    current_dir = tmp_path / "review_results"
    current_dir.mkdir()
    current = _write_json(
        current_dir / "final_issues.json",
        {
            "issues": [{"title": "p", "root_cause_key": "k", "severity": "moderate"}],
            "round_scores": {"quality": 78, "clarity": 70},
        },
    )

    script = SCRIPT_DIR_AUDIT / "diff_review_issues.py"

    result = subprocess.run(
        [sys.executable, "-B", str(script), str(previous), str(current)],
        check=True,
        capture_output=True,
        text=True,
    )

    stdout_payload = json.loads(result.stdout.split("\n[trajectory]")[0])
    assert stdout_payload["statuses"][0]["status"] == "PARTIALLY_ADDRESSED"

    trajectory = current_dir / "revision_trajectory.md"
    assert trajectory.exists()
    assert "70 ⚠️↓" in trajectory.read_text(encoding="utf-8")


def test_diff_review_issues_cli_skips_trajectory_for_legacy_lists(tmp_path: Path) -> None:
    previous = _write_json(tmp_path / "prev.json", [{"title": "p", "root_cause_key": "k"}])
    current = _write_json(tmp_path / "cur.json", [{"title": "p", "root_cause_key": "k"}])

    script = SCRIPT_DIR_AUDIT / "diff_review_issues.py"

    result = subprocess.run(
        [sys.executable, "-B", str(script), str(previous), str(current)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "[trajectory]" not in result.stdout
    assert not (tmp_path / "revision_trajectory.md").exists()


def test_diff_review_issues_cli_supports_no_trajectory_flag(tmp_path: Path) -> None:
    previous = _write_json(
        tmp_path / "prev.json",
        {"issues": [], "round_scores": {"quality": 80}},
    )
    current = _write_json(
        tmp_path / "cur.json",
        {"issues": [], "round_scores": {"quality": 70}},
    )

    script = SCRIPT_DIR_AUDIT / "diff_review_issues.py"

    result = subprocess.run(
        [sys.executable, "-B", str(script), str(previous), str(current), "--no-trajectory"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "[trajectory]" not in result.stdout
    assert not (tmp_path / "revision_trajectory.md").exists()
