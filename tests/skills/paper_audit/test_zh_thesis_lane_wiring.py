"""Wiring tests for the zh_thesis_review canonical lane."""

from __future__ import annotations

import json
from pathlib import Path

from tests.support.paths import SKILLS_ROOT


def test_selected_lanes_zh_gated() -> None:
    from audit import _selected_lanes_for_focus

    assert "zh_thesis_review" in _selected_lanes_for_focus("full", lang="zh")
    assert "zh_thesis_review" in _selected_lanes_for_focus("editor", lang="zh")
    assert "zh_thesis_review" not in _selected_lanes_for_focus("full")
    assert "zh_thesis_review" not in _selected_lanes_for_focus("full", lang="en")
    assert "zh_thesis_review" not in _selected_lanes_for_focus("methodology", lang="zh")


def test_guides_name_the_lane() -> None:
    root = SKILLS_ROOT / "paper-audit" / "references"
    assert "zh_thesis_review" in (root / "REVIEW_LANE_GUIDE.md").read_text(encoding="utf-8")
    assert "### Lane: zh_thesis_review" in (root / "SUBAGENT_TEMPLATES.md").read_text(
        encoding="utf-8"
    )
    mode = (root / "MODE_GUIDE.md").read_text(encoding="utf-8")
    assert "zh_thesis_review" in mode
    assert 'lang == "zh"' in mode or "lang == `zh`" in mode or '`lang == "zh"`' in mode


def test_fallback_emits_zh_thesis_lane_for_chinese_text() -> None:
    from audit import _fallback_cross_cutting_issues, _selected_lanes_for_focus

    issues = _fallback_cross_cutting_issues(
        {"headline_claims": [], "closure_targets": []},
        {"introduction": "本文研究工业过程质量预测方法。"},
    )
    lanes = {issue["review_lane"] for issue in issues}
    assert "zh_thesis_review" in lanes
    allowed = _selected_lanes_for_focus("full", lang="zh")
    assert "zh_thesis_review" in allowed
    assert "zh_thesis_review" not in _selected_lanes_for_focus("full", lang="en")


def test_write_lane_outputs_registers_zh_thesis_json(tmp_path: Path) -> None:
    from audit import _write_lane_outputs
    from paths import WorkspaceLayout

    workspace = tmp_path / "review"
    layout = WorkspaceLayout(workspace)
    layout.sections_dir.mkdir(parents=True, exist_ok=True)
    (layout.sections_dir / "introduction.md").write_text("本文提出一种方法。", encoding="utf-8")
    section_index = [{"section_key": "introduction", "file_name": "introduction.md"}]
    _write_lane_outputs(workspace, section_index, {}, focus="full", lang="zh")
    comment = layout.comments_dir / "zh_thesis_review.json"
    assert comment.is_file()
    payload = json.loads(comment.read_text(encoding="utf-8"))
    items = payload if isinstance(payload, list) else payload.get("issues", [])
    assert items
    assert all(item.get("review_lane") == "zh_thesis_review" for item in items)


def test_en_focus_does_not_write_zh_thesis_lane(tmp_path: Path) -> None:
    from audit import _write_lane_outputs
    from paths import WorkspaceLayout

    workspace = tmp_path / "review"
    layout = WorkspaceLayout(workspace)
    layout.sections_dir.mkdir(parents=True, exist_ok=True)
    (layout.sections_dir / "introduction.md").write_text("We present a method.", encoding="utf-8")
    section_index = [{"section_key": "introduction", "file_name": "introduction.md"}]
    _write_lane_outputs(workspace, section_index, {}, focus="full", lang="en")
    assert not (layout.comments_dir / "zh_thesis_review.json").exists()


def test_checkpoint_recognizes_zh_thesis_lane_name(tmp_path: Path) -> None:
    from checkpoint import init_checkpoint, load_checkpoint, mark_lane_completed

    workspace = tmp_path / "review"
    workspace.mkdir()
    init_checkpoint(workspace)
    mark_lane_completed(workspace, "zh_thesis_review")
    checkpoint = load_checkpoint(workspace)
    assert checkpoint is not None
    assert "zh_thesis_review" in checkpoint.get("completed_lanes", [])

    from audit import _load_completed_lanes

    assert "zh_thesis_review" in _load_completed_lanes(workspace)


def test_consolidator_accepts_zh_thesis_lane(tmp_path: Path) -> None:
    from consolidate_review_findings import consolidate_findings, load_comment_files
    from paths import WorkspaceLayout

    workspace = tmp_path / "review"
    layout = WorkspaceLayout(workspace)
    layout.comments_dir.mkdir(parents=True, exist_ok=True)
    (layout.comments_dir / "zh_thesis_review.json").write_text(
        json.dumps(
            [
                {
                    "title": "工作量需评阅人判断",
                    "quote": "本文完成了研究",
                    "explanation": "脚本无法判定工作量",
                    "comment_type": "missing_information",
                    "severity": "moderate",
                    "source_kind": "llm",
                    "source_section": "conclusion",
                    "review_lane": "zh_thesis_review",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    findings = load_comment_files(layout.comments_dir)
    consolidated = consolidate_findings(findings)
    assert any(item.get("review_lane") == "zh_thesis_review" for item in consolidated)
