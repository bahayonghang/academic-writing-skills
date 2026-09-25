"""Tests for scripts/plan_deck.py on the mini-thesis inventory."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from tests.support.paths import SKILLS_ROOT

SCRIPT = SKILLS_ROOT / "latex-defense-zh" / "scripts" / "plan_deck.py"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
CONTENT_EXCLUDED = ("cover", "toc", "thanks", "backup")


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPT), *args],
        capture_output=True,
        encoding="utf-8",
        env=ENV,
        check=False,
    )


def content_frames(plan: dict) -> list[dict]:
    return [frame for frame in plan["frames"] if frame["role"] not in CONTENT_EXCLUDED]


def by_id(plan: dict) -> dict[str, dict]:
    return {frame["id"]: frame for frame in plan["frames"]}


@pytest.mark.parametrize("minutes", [30, 40, 60])
def test_content_pages_inside_budget_range(inventory: dict, defense_scripts, minutes: int) -> None:
    plan = defense_scripts.plan_deck.build_plan(inventory, minutes, "predefense", "yanshan", "0")
    roles = [chapter["role"] for chapter in plan["meta"]["chapters"]]
    budget = defense_scripts.defense_budget.compute_budget(roles, minutes)
    low, high = budget.page_range
    assert low <= len(content_frames(plan)) <= high
    assert len(plan["frames"]) == budget.total_frames
    for chapter in (3, 4, 5):
        pages = [f for f in content_frames(plan) if f["chapter"] == chapter]
        assert len(pages) >= 6


def test_frame_order_ids_and_seconds(inventory: dict, defense_scripts) -> None:
    plan = defense_scripts.plan_deck.build_plan(inventory, 40, "predefense", "yanshan", "0")
    frames = plan["frames"]
    ids = [frame["id"] for frame in frames]
    assert len(ids) == len(set(ids)) == 54
    assert ids[:3] == ["cover", "toc", "c1-background-1"]
    assert ids[-3:] == ["c7-innovation", "c7-outlook", "thanks"]
    for number in range(2, 8):
        index = ids.index(f"c{number}-toc")
        assert frames[index + 1]["chapter"] == number
        assert all(frame["chapter"] != number for frame in frames[:index])
    research_roles = [f["role"] for f in frames if f["chapter"] == 3 and f["role"] != "toc"]
    assert research_roles == ["intro", "problem"] + ["method"] * 3 + ["experiment"] * 4 + [
        "summary"
    ]
    seconds = {frame["id"]: frame["notes"]["seconds"] for frame in frames}
    assert (seconds["cover"], seconds["toc"], seconds["c2-toc"], seconds["thanks"]) == (
        30,
        20,
        8,
        10,
    )
    assert (seconds["c1-status-1"], seconds["c3-method-1"], seconds["c7-outlook"]) == (50, 51, 68)


def test_candidates_layouts_and_papers(inventory: dict, defense_scripts) -> None:
    plan = defense_scripts.plan_deck.build_plan(inventory, 40, "predefense", "generic", "0")
    frames = by_id(plan)
    placeholder = defense_scripts.plan_deck.PLACEHOLDER
    assert plan["meta"]["theme"] == "generic"
    intro = frames["c3-intro"]
    assert (intro["layout"], intro["position"]) == ("figure-bullets", "top")
    assert intro["subsection"] == "研究内容 1：基于时空图卷积的流量补全方法研究"
    assert frames["c5-intro"]["subsection"].startswith("研究内容 3：")
    assert frames["c2-foundation-2"]["equations"] == [{"label": "eq:c2-target"}]
    method = frames["c3-method-3"]
    assert method["layout"] == "equations-figure"
    assert method["subsection"] == "3.3.2 补全网络设计"
    assert method["figures"] == [{"label": "fig:c3-network"}]
    grid = frames["c3-experiment-3"]
    assert grid["layout"] == "figure-grid"
    assert grid["figures"] == [{"label": "fig:c3-compare", "subfigures": ["a", "b", "c"]}]
    assert grid["bullets"] == []
    assert frames["c3-experiment-1"]["table"] == "tab:c3-datasets"
    assert [frames[f"c{n}-summary"]["paper"] for n in (3, 4, 5)] == ["P1", "P2", "P3"]
    assert any(hint.startswith("P2 ") for hint in frames["c3-summary"]["hints"])
    assert frames["c1-challenges"]["bullets"] == [placeholder] * 3
    assert frames["c7-innovation"]["subsection"] == "01　主要创新点"
    assert len(frames["c7-outlook"]["bullets"]) == 2
    assert frames["c6-architecture"]["figures"] == [{"label": "fig:c6-architecture"}]
    assert frames["c6-application-2"]["table"] == "tab:c6-effect"
    assert "chapters/chapter3.tex:" in frames["c3-method-3"]["source"][0]


def test_defense_stage_adds_achievements(inventory: dict, defense_scripts) -> None:
    plan = defense_scripts.plan_deck.build_plan(inventory, 40, "defense", "yanshan", "0")
    ids = [frame["id"] for frame in plan["frames"]]
    assert ids[-4:] == ["c7-innovation", "c7-outlook", "c7-achievements", "thanks"]
    assert len(content_frames(plan)) == 43


def test_role_override_from_inventory(inventory: dict, defense_scripts) -> None:
    inventory["chapters"][1]["role"] = "research"
    plan = defense_scripts.plan_deck.build_plan(inventory, 40, "predefense", "yanshan", "0")
    assert plan["meta"]["chapters"][1]["role"] == "research"
    assert "c2-intro" in by_id(plan)
    assert by_id(plan)["c2-intro"]["subsection"].startswith("研究内容 1：")


@pytest.mark.parametrize("body", [None, "\\begin{longtable}{cc}\na & b \\\\\n\\end{longtable}"])
def test_tables_that_cannot_fit_are_not_candidates(
    inventory: dict, defense_scripts, body: str | None
) -> None:
    for table in inventory["tables"]:
        table["tabular_source"] = body
    plan = defense_scripts.plan_deck.build_plan(inventory, 40, "predefense", "yanshan", "0")
    assert all(frame.get("table") is None for frame in plan["frames"])
    assert all(frame["layout"] != "table" for frame in plan["frames"])


def test_cli_writes_plan_and_outline(inventory: dict, tmp_path: Path) -> None:
    out = tmp_path / "plan" / "slide_plan.yaml"
    result = run_cli("--inventory", str(tmp_path / "inventory.json"), "--out", str(out))
    assert result.returncode == 0, result.stderr
    plan = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert len(plan["meta"]["inventory_sha256"]) == 64
    outline = run_cli("--plan", str(out), "--outline")
    assert outline.returncode == 0, outline.stderr
    lines = outline.stdout.splitlines()
    assert len(lines) == len(plan["frames"]) + 1
    assert lines[0].startswith("1  cover  ")
    assert lines[-1].startswith(f"帧数 {len(plan['frames'])}，内容页数 45，占位符 ")


def test_cli_input_errors_exit_2(inventory: dict, tmp_path: Path) -> None:
    bad = dict(inventory)
    bad["chapters"] = [dict(chapter) for chapter in inventory["chapters"]]
    bad["chapters"][-1]["role"] = "research"
    bad_path = tmp_path / "bad.json"
    bad_path.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
    result = run_cli("--inventory", str(bad_path), "--out", str(tmp_path / "p.yaml"))
    assert result.returncode == 2
    assert "role" in result.stderr
    empty = tmp_path / "empty.yaml"
    empty.write_text("meta: {}\n", encoding="utf-8")
    assert run_cli("--plan", str(empty), "--outline").returncode == 2
    assert run_cli("--outline").returncode == 2
    assert run_cli("--inventory", str(tmp_path / "none.json"), "--out", "p.yaml").returncode == 2


def test_filled_plan_has_no_placeholders(filled_plan: dict, defense_scripts) -> None:
    assert defense_scripts.plan_deck.count_placeholders(filled_plan) == 0
    say = by_id(filled_plan)["c3-method-1"]["notes"]["say"]
    assert 150 <= len(say) <= 250
