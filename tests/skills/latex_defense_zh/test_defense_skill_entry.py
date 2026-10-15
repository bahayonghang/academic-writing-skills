"""Tests for the latex-defense-zh skill entry: router, reference map, and fixture paths."""

from __future__ import annotations

import json
import re

from tests.support.paths import SKILLS_ROOT

SKILL_ROOT = SKILLS_ROOT / "latex-defense-zh"
SKILL_MD = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
MODULES = {"extract", "plan", "build", "check", "preview"}


def _section(name: str) -> str:
    return SKILL_MD.split(f"## {name}", 1)[1].split("\n## ", 1)[0]


def test_module_router_rows_match_modules() -> None:
    rows = re.findall(r"^\|\s*`([^`]+)`\s*\|", _section("Module Router"), flags=re.MULTILINE)
    assert set(rows) == MODULES
    assert len(rows) == len(MODULES)


def test_reference_map_lists_every_reference() -> None:
    listed = set(re.findall(r"`references/([a-z0-9-]+\.md)`", _section("Reference Map")))
    present = {path.name for path in (SKILL_ROOT / "references").glob("*.md")}
    assert listed == present
    for agent in re.findall(r"`(agents/[a-z0-9-]+\.md)`", _section("Reference Map")):
        assert (SKILL_ROOT / agent).is_file()


def test_example_requests_point_to_examples() -> None:
    linked = set(re.findall(r"`examples/([a-z0-9-]+\.md)`", _section("Example Requests")))
    present = {path.name for path in (SKILL_ROOT / "examples").glob("*.md")}
    assert linked == present


def test_eval_and_example_fixture_paths_exist() -> None:
    payload = json.loads((SKILL_ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
    for item in payload["evals"]:
        for rel_path in item["files"]:
            assert (SKILL_ROOT / rel_path).is_file(), rel_path
    for example in (SKILL_ROOT / "examples").glob("*.md"):
        for rel_path in re.findall(
            r"`(evals/fixtures/[^`]+)`", example.read_text(encoding="utf-8")
        ):
            assert (SKILL_ROOT / rel_path).exists(), f"{example.name}: {rel_path}"
