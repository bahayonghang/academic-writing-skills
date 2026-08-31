"""Runtime wiring tests for the subsection-context polish lane."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from audit import (
    FOCUS_TO_ALLOWED_LANES,
    ROLE_TO_REVIEW_LANES,
    _selected_lanes_for_focus,
    _write_lane_outputs,
    run_polish_precheck,
)
from paths import WorkspaceLayout
from prepare_review_workspace import prepare_workspace

from tests.support.paths import SKILLS_ROOT

_FIXTURE_DIR = SKILLS_ROOT / "latex-thesis-zh" / "evals" / "fixtures" / "subsection-context"


def _copy_fixture(tmp_path: Path) -> Path:
    target = tmp_path / "subsection-context"
    shutil.copytree(_FIXTURE_DIR, target)
    return target / "main.tex"


def test_focus_and_role_matrices_enable_only_full_and_logic() -> None:
    lane = "subsection_context_polish"
    assert lane in _selected_lanes_for_focus("full")
    assert lane in _selected_lanes_for_focus("logic")
    assert lane not in _selected_lanes_for_focus("methodology")
    assert lane not in _selected_lanes_for_focus("literature")
    assert lane in ROLE_TO_REVIEW_LANES["logic"]
    assert FOCUS_TO_ALLOWED_LANES["full"] >= {lane}


def test_polish_state_points_to_real_window_artifacts(tmp_path: Path) -> None:
    paper = _copy_fixture(tmp_path)
    run_polish_precheck(str(paper), lang="zh", skip_logic=True)

    state_root = paper.parent / ".polish-state"
    payload = json.loads((state_root / "precheck.json").read_text(encoding="utf-8"))
    subsection_windows = payload["subsection_windows"]
    assert subsection_windows["status"] == "ok"
    assert subsection_windows["index"] == "artifacts/data/subsection_index.json"
    assert subsection_windows["units"]

    for unit in subsection_windows["units"]:
        window_path = state_root / unit["window"]
        assert window_path.is_file()
        window = json.loads(window_path.read_text(encoding="utf-8"))
        assert unit["source_file"] == window["source_file"]
        assert unit["editable"] == window["editable"]
        assert unit["read_only"] == window["read_only"]
        assert window["editable"]["part"] == "current"
        assert isinstance(window["read_only"], list)


def test_deterministic_fallback_does_not_create_subsection_lane_issue(
    tmp_path: Path,
) -> None:
    paper = _copy_fixture(tmp_path)
    workspace = prepare_workspace(str(paper), output_dir=str(tmp_path / "review-results"))
    layout = WorkspaceLayout(workspace)
    section_index = json.loads(layout.section_index.read_text(encoding="utf-8"))
    claim_map = json.loads(layout.claim_map.read_text(encoding="utf-8"))

    _write_lane_outputs(workspace, section_index, claim_map, focus="logic")

    assert not layout.comment_file("subsection_context_polish.json").exists()
