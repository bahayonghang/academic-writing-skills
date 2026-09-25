"""Tests for scripts/defense_budget.py (formula in references/time-budget.md)."""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from tests.support.paths import SKILLS_ROOT

SCRIPT = SKILLS_ROOT / "latex-defense-zh" / "scripts" / "defense_budget.py"
DEFAULT_ROLES = [
    "intro",
    "foundation",
    "research",
    "research",
    "research",
    "application",
    "conclusion",
]
FOUR_RESEARCH = [
    "intro",
    "research",
    "research",
    "research",
    "research",
    "application",
    "conclusion",
]


@pytest.mark.parametrize(
    (
        "roles",
        "minutes",
        "stage",
        "pages",
        "method",
        "experiment",
        "content",
        "page_range",
        "frames",
    ),
    [
        (DEFAULT_ROLES, 30, "predefense", 7, 2, 2, 35, (30, 40), 44),
        (DEFAULT_ROLES, 40, "predefense", 10, 3, 4, 45, (38, 52), 54),
        (DEFAULT_ROLES, 60, "predefense", 15, 5, 7, 66, (56, 76), 75),
        (FOUR_RESEARCH, 40, "predefense", 8, 2, 3, 44, (37, 51), 53),
        (DEFAULT_ROLES, 40, "defense", 9, 3, 3, 43, (37, 49), 52),
    ],
)
def test_budget_matches_time_budget_reference(
    defense_scripts,
    roles: list[str],
    minutes: int,
    stage: str,
    pages: int,
    method: int,
    experiment: int,
    content: int,
    page_range: tuple[int, int],
    frames: int,
) -> None:
    budget = defense_scripts.defense_budget.compute_budget(roles, minutes, stage)

    research = [chapter for chapter in budget.chapters if chapter.role == "research"]
    for chapter in research:
        counts = {item.role: item.pages for item in chapter.roles}
        assert sum(counts.values()) == pages
        assert counts == {
            "intro": 1,
            "problem": 1,
            "method": method,
            "experiment": experiment,
            "summary": 1,
        }
    assert budget.content_pages == content
    assert budget.page_range == page_range
    assert budget.total_frames == frames


def test_budget_default_structure_seconds(defense_scripts) -> None:
    budget = defense_scripts.defense_budget.compute_budget(DEFAULT_ROLES)
    seconds = {
        chapter.role: {item.role: item.seconds_per_page for item in chapter.roles}
        for chapter in budget.chapters
    }

    assert seconds["intro"] == {
        "background": 50,
        "status": 50,
        "challenges": 50,
        "organization": 50,
    }
    assert seconds["foundation"] == {"foundation": 50}
    assert seconds["research"] == {
        "intro": 51,
        "problem": 51,
        "method": 51,
        "experiment": 51,
        "summary": 51,
    }
    assert seconds["application"] == {"intro": 45, "architecture": 45, "application": 45}
    assert seconds["conclusion"] == {"innovation": 68, "outlook": 68}


def test_round_half_up_rounds_point_five_upward(defense_scripts) -> None:
    round_half_up = defense_scripts.defense_budget.round_half_up

    assert [round_half_up(value) for value in (0.5, 1.5, 2.5, 2.49, 9.6)] == [1, 2, 3, 2, 10]


@pytest.mark.parametrize(
    ("roles", "minutes", "stage"),
    [
        (DEFAULT_ROLES, 14, "predefense"),
        (DEFAULT_ROLES, 91, "predefense"),
        (DEFAULT_ROLES, 40, "final"),
        (["intro", "foundation", "application", "conclusion"], 40, "predefense"),
        (["research", "research", "conclusion"], 40, "predefense"),
        (["intro", "research", "summary"], 40, "predefense"),
    ],
)
def test_budget_rejects_invalid_input(
    defense_scripts, roles: list[str], minutes: int, stage: str
) -> None:
    with pytest.raises(ValueError):
        defense_scripts.defense_budget.compute_budget(roles, minutes, stage)


def test_budget_cli_outputs_json_and_rejects_bad_roles() -> None:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")

    def run(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *args],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            check=False,
        )

    good = run("--roles", ",".join(DEFAULT_ROLES), "--minutes", "40")
    bad = run("--roles", "research,conclusion")

    assert good.returncode == 0, good.stderr
    assert json.loads(good.stdout)["content_pages"] == 45
    assert bad.returncode == 2
    assert "intro" in bad.stderr
