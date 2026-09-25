"""Asset tests for the latex-defense-zh Beamer themes, demo deck, and references.

The compile test runs only when ``DEFENSE_ZH_COMPILE=1`` and ``xelatex`` is on PATH.
"""

from __future__ import annotations

import importlib
import math
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from tests.support.paths import SKILLS_ROOT

SKILL_ROOT = SKILLS_ROOT / "latex-defense-zh"
BEAMER_DIR = SKILL_ROOT / "templates" / "beamer"
REFERENCES = SKILL_ROOT / "references"
LAYOUTS_STY = BEAMER_DIR / "defense-layouts.sty"
DEMO_DECK = BEAMER_DIR / "demo-deck.tex"
THEME_FILES = {
    "yanshan": BEAMER_DIR / "beamerthemeYanshanDefense.sty",
    "generic": BEAMER_DIR / "beamerthemeGenericDefense.sty",
}

# Yanshan colors measured from the reference predefense deck (C1 design section 2.4).
YANSHAN_COLORS = {
    "defenseNavy": "1F296A",
    "defenseBlue": "2F5597",
    "defenseAccent": "4472C4",
    "defenseBoxHead": "376092",
    "defensePaper": "002060",
    "defenseRed": "FF0000",
}

# Macros and environments of the public API (parent design section 5).
LAYOUT_API = (
    "DefenseSetup",
    "DefenseStage",
    "DefenseSupervisor",
    "DefenseSubject",
    "DefenseSchool",
    "DefenseAddChapter",
    "DefenseDefineLabel",
    "DefenseCoverFrame",
    "DefenseTocFrame",
    "DefenseThanksFrame",
    "DefenseSubsection",
    "DefenseTakeaway",
    "DefenseHighlight",
    "DefenseBoxTitle",
    "DefenseFigure",
    "DefenseCaption",
    "DefensePaperBox",
    "DefenseCard",
    "DefenseSource",
)

DEFINE_COLOR_RE = re.compile(r"\\definecolor\{(defense\w+)\}\{HTML\}\{([0-9A-Fa-f]{6})\}")
COLOR_ROW_RE = re.compile(
    r"^\|\s*`(defense\w+)`\s*\|\s*`#([0-9A-Fa-f]{6})`\s*\|\s*`#([0-9A-Fa-f]{6})`\s*\|"
)
COMMAND_DEF_RE = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand|def|NewDocumentCommand|RenewDocumentCommand|"
    r"ProvideDocumentCommand|DeclareDocumentCommand)\*?\s*\{?\\([A-Za-z@]+)"
)
ENV_DEF_RE = re.compile(
    r"\\(?:newenvironment|renewenvironment|NewDocumentEnvironment|RenewDocumentEnvironment)"
    r"\s*\{\s*([A-Za-z]+)\s*\}"
)
LAYOUT_ROW_RE = re.compile(r"^\|\s*`([a-z][a-z-]*)`\s*\|")
LAYOUT_COMMENT_RE = re.compile(r"^% layout: ([a-z][a-z-]*)\s*$", re.MULTILINE)
BUDGET_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(\d+)（(\d+)/(\d+)）\s*\|\s*(\d+)\s*\|\s*\[(\d+),\s*(\d+)\]\s*\|\s*(\d+)\s*\|"
)
DEFAULT_ROLES = (
    "intro",
    "foundation",
    "research",
    "research",
    "research",
    "application",
    "conclusion",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _theme_colors(path: Path) -> dict[str, str]:
    return {name: value.upper() for name, value in DEFINE_COLOR_RE.findall(_read(path))}


def _defined_names(text: str) -> set[str]:
    return set(COMMAND_DEF_RE.findall(text)) | set(ENV_DEF_RE.findall(text))


def test_theme_colors_match_visual_spec() -> None:
    table: dict[str, dict[str, str]] = {"yanshan": {}, "generic": {}}
    for line in _read(REFERENCES / "visual-spec.md").splitlines():
        match = COLOR_ROW_RE.match(line)
        if match:
            table["yanshan"][match.group(1)] = match.group(2).upper()
            table["generic"][match.group(1)] = match.group(3).upper()

    assert table["yanshan"] == YANSHAN_COLORS
    assert _theme_colors(THEME_FILES["yanshan"]) == YANSHAN_COLORS
    assert _theme_colors(THEME_FILES["generic"]) == table["generic"]
    assert set(_theme_colors(LAYOUTS_STY)) == set(YANSHAN_COLORS)


def test_themes_load_layouts_and_define_no_layout_macros() -> None:
    assert set(LAYOUT_API) <= _defined_names(_read(LAYOUTS_STY))
    for path in THEME_FILES.values():
        text = _read(path)
        assert "\\RequirePackage{defense-layouts}" in text, path.name
        assert not _defined_names(text) & set(LAYOUT_API), path.name


def test_slide_layout_catalog_matches_demo_deck() -> None:
    catalog = [
        match.group(1)
        for line in _read(REFERENCES / "slide-layouts.md").splitlines()
        if (match := LAYOUT_ROW_RE.match(line))
    ]
    demo = set(LAYOUT_COMMENT_RE.findall(_read(DEMO_DECK)))

    assert len(catalog) == 12
    assert len(set(catalog)) == 12
    assert set(catalog) == demo


def _round_half_up(value: float) -> int:
    return math.floor(value + 0.5)


def _budget(minutes: int, roles: tuple[str, ...], stage: str = "predefense") -> dict[str, int]:
    """Compute the reference values with the time-budget.md formula."""
    k = minutes / 40

    def scaled(base: int) -> int:
        return max(1, _round_half_up(base * k))

    segment_seconds = {
        "intro": 300,
        "foundation": 150,
        "application": 180,
        "conclusion": 180 if stage == "defense" else 135,
    }
    segment_pages = {
        "intro": scaled(2) + scaled(2) + 2,
        "foundation": scaled(3),
        "application": 1 + scaled(1) + scaled(2),
        "conclusion": 3 if stage == "defense" else 2,
    }
    fixed_seconds = 30 + 20 + 8 * (len(roles) - 1) + 10
    research_count = roles.count("research")
    remainder = 60 * minutes - fixed_seconds
    remainder -= sum(segment_seconds[role] * k for role in roles if role != "research")
    per_chapter = remainder / research_count
    pages = max(6, _round_half_up(per_chapter / 53))
    method = max(2, _round_half_up((pages - 3) * 3 / 7))
    experiment = max(1, pages - 3 - method)
    content = research_count * pages
    content += sum(segment_pages[role] for role in roles if role != "research")
    return {
        "pages": pages,
        "method": method,
        "experiment": experiment,
        "content": content,
        "low": _round_half_up(0.85 * content),
        "high": _round_half_up(1.15 * content),
        "frames": content + len(roles) + 2,
    }


def test_time_budget_reference_values_follow_formula() -> None:
    text = _read(REFERENCES / "time-budget.md")
    rows = {}
    for line in text.splitlines():
        match = BUDGET_ROW_RE.match(line)
        if match:
            values = [int(group) for group in match.groups()]
            rows[values[0]] = values[1:]

    assert sorted(rows) == [30, 40, 60]
    for minutes, row in rows.items():
        pages, method, experiment, content, low, high, frames = row
        expected = _budget(minutes, DEFAULT_ROLES)
        assert row == [
            expected["pages"],
            expected["method"],
            expected["experiment"],
            expected["content"],
            expected["low"],
            expected["high"],
            expected["frames"],
        ], minutes
        assert pages >= 6
        assert method + experiment + 3 == pages
        assert low <= content <= high

    four_research = _budget(
        40, ("intro", "research", "research", "research", "research") + DEFAULT_ROLES[-2:]
    )
    defense = _budget(40, DEFAULT_ROLES, stage="defense")
    assert f"每个研究章 {four_research['pages']} 页，N = {four_research['content']}" in text
    assert f"每个研究章 {defense['pages']} 页，N = {defense['content']}" in text


def _pdf_page_count(pdf: Path, log: str) -> int:
    try:
        fitz = importlib.import_module("fitz")
    except ImportError:
        match = re.search(r"Output written on .*?\((\d+) pages?", log, flags=re.DOTALL)
        assert match, "xelatex log has no page count"
        return int(match.group(1))
    with fitz.open(pdf) as document:
        return document.page_count


@pytest.mark.skipif(
    os.environ.get("DEFENSE_ZH_COMPILE") != "1" or shutil.which("xelatex") is None,
    reason="set DEFENSE_ZH_COMPILE=1 and install xelatex to compile the demo deck",
)
@pytest.mark.parametrize(
    ("theme", "with_logo"),
    [("YanshanDefense", True), ("YanshanDefense", False), ("GenericDefense", False)],
)
def test_demo_deck_compiles(tmp_path: Path, theme: str, with_logo: bool) -> None:
    from PIL import Image

    work = tmp_path / "beamer"
    shutil.copytree(BEAMER_DIR, work)
    if with_logo:
        Image.new("RGB", (1350, 400), (31, 41, 106)).save(work / "logo.png")
    jobname = f"demo-{theme.lower()}"
    result = subprocess.run(
        [
            "xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-jobname={jobname}",
            f"\\def\\DefenseThemeName{{{theme}}}\\input{{demo-deck.tex}}",
        ],
        cwd=work,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=600,
        check=False,
    )
    log = (work / f"{jobname}.log").read_text(encoding="utf-8", errors="replace")

    assert result.returncode == 0, log[-3000:]
    frames = len(re.findall(r"^\\begin\{frame\}", _read(DEMO_DECK), flags=re.MULTILINE))
    assert _pdf_page_count(work / f"{jobname}.pdf", log) == frames
    assert "Overfull \\vbox" not in log
