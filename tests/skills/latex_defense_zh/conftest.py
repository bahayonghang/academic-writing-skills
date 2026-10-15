"""Shared fixtures for the latex-defense-zh script tests.

Scripts load by file path. The sibling modules that the scripts import
(``tex_loader``, ``defense_budget``, ``extract_thesis``) are evicted from
``sys.modules`` before each load and restored afterward, so the
latex-defense-zh copies win without leaking into other skills' tests.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from types import ModuleType

import pytest
import yaml

from tests.support.paths import SKILLS_ROOT

SKILL_ROOT = SKILLS_ROOT / "latex-defense-zh"
SCRIPTS = SKILL_ROOT / "scripts"
FIXTURE_DIR = SKILL_ROOT / "evals" / "fixtures" / "mini-thesis"
_SHARED_MODULE_NAMES = ("tex_loader", "defense_budget", "extract_thesis")

# PyMuPDF binds sys.stdout for its messages at first import. Import it here, under
# pytest's session capture, rather than inside a capsys test whose stream closes at teardown.
with contextlib.suppress(ImportError):
    importlib.import_module("pymupdf")


def load_script(name: str) -> ModuleType:
    """Load ``scripts/<name>.py`` in isolation from other skills' modules."""
    saved_path = list(sys.path)
    saved_modules = {module: sys.modules.pop(module, None) for module in _SHARED_MODULE_NAMES}
    try:
        sys.path.insert(0, str(SCRIPTS))
        spec = importlib.util.spec_from_file_location(f"_defense_{name}", SCRIPTS / f"{name}.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for module, saved in saved_modules.items():
            if saved is None:
                sys.modules.pop(module, None)
            else:
                sys.modules[module] = saved


class _Scripts:
    """Attribute access loads the script of the same name once."""

    def __getattr__(self, name: str) -> ModuleType:
        if name.startswith("_"):
            raise AttributeError(name)
        module = load_script(name)
        setattr(self, name, module)
        return module


_SCRIPTS = _Scripts()


@pytest.fixture
def defense_scripts() -> _Scripts:
    return _SCRIPTS


def write_png(path: Path) -> None:
    """Write a plain 800x500 PNG; the fixture does not commit images."""
    from PIL import Image

    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (800, 500), (200, 210, 225)).save(path)


@pytest.fixture
def mini_thesis(tmp_path: Path, defense_scripts: _Scripts) -> Path:
    """Copy of the mini-thesis fixture with a PNG for every figure file and the logo."""
    root = tmp_path / "mini-thesis"
    shutil.copytree(FIXTURE_DIR, root)
    for figure in defense_scripts.extract_thesis.extract_inventory(root)["figures"]:
        for item in figure["files"]:
            write_png(root / item["resolved"])
    write_png(root / "fig" / "logo.png")
    return root


@pytest.fixture
def inventory(mini_thesis: Path, tmp_path: Path, defense_scripts: _Scripts) -> dict:
    """Extraction result of ``mini_thesis``, also written to ``tmp_path/inventory.json``."""
    data = defense_scripts.extract_thesis.extract_inventory(mini_thesis)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    (tmp_path / "inventory.json").write_text(text, encoding="utf-8")
    return data


SAY_FILLER = "本页先给出结论，再说明依据，并指出图表在页面中的位置与阅读顺序。"


def fill_plan(plan: dict, placeholder: str) -> dict:
    """Replace every placeholder with deterministic synthetic text (C2 design 8)."""
    for frame in plan["frames"]:
        frame_id = frame["id"]
        if "bullets" in frame:
            frame["bullets"] = [
                f"合成要点 {frame_id}-{index}" for index in range(1, len(frame["bullets"]) + 1)
            ]
        if "takeaway" in frame:
            frame["takeaway"] = f"合成结论 {frame_id}"
        notes = frame["notes"]
        if notes["say"] == placeholder:
            notes["say"] = f"合成讲稿 {frame_id}。"
            if frame["role"] not in ("cover", "toc", "thanks"):
                notes["say"] += SAY_FILLER * 5
        if notes["key"] == placeholder:
            notes["key"] = f"合成要点 {frame_id}"
        if notes["transition"] == placeholder:
            notes["transition"] = f"合成过渡 {frame_id}"
        notes["questions"] = [
            f"合成提问 {frame_id}" if question == placeholder else question
            for question in notes["questions"]
        ]
    return plan


@pytest.fixture
def filled_plan(inventory: dict, tmp_path: Path, defense_scripts: _Scripts) -> dict:
    """40-minute plan of ``inventory`` with synthetic text, written to ``tmp_path/slide_plan.yaml``."""
    plan_deck = defense_scripts.plan_deck
    digest = hashlib.sha256((tmp_path / "inventory.json").read_bytes()).hexdigest()
    plan = plan_deck.build_plan(inventory, 40, "predefense", "yanshan", digest)
    plan = fill_plan(plan, plan_deck.PLACEHOLDER)
    text = yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=1000)
    (tmp_path / "slide_plan.yaml").write_text(text, encoding="utf-8")
    return plan


@pytest.fixture
def built_deck(filled_plan: dict, tmp_path: Path, defense_scripts: _Scripts) -> Path:
    """Output directory of build_deck.py for ``filled_plan`` (no compile)."""
    out = tmp_path / "deck"
    code = defense_scripts.build_deck.main(
        [
            "--plan",
            str(tmp_path / "slide_plan.yaml"),
            "--inventory",
            str(tmp_path / "inventory.json"),
            "--out",
            str(out),
        ]
    )
    assert code == 0
    return out
