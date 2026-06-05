"""Smoke tests for per-venue template snapshots (stage 4)."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent / "academic-writing-skills"


SKILL_EXPECTATIONS = {
    "latex-paper-en": {
        "files": ["ieee.md", "acm.md", "neurips.md", "icml.md", "springer-lncs.md"],
        "skill_marker": "templates/<venue>.md",
    },
    "latex-thesis-zh": {
        "files": ["generic.md", "thuthesis.md", "pkuthss.md"],
        "skill_marker": "templates/<template>.md",
    },
    "typst-paper": {
        "files": ["ieee.md", "acm.md", "neurips.md"],
        "skill_marker": "templates/<venue>.md",
    },
}


@pytest.mark.parametrize("skill", sorted(SKILL_EXPECTATIONS))
def test_templates_directory_exists(skill: str) -> None:
    directory = ROOT / skill / "templates"
    assert directory.is_dir(), f"missing templates dir for {skill}: {directory}"


@pytest.mark.parametrize(
    "skill,filename",
    [(s, f) for s, cfg in SKILL_EXPECTATIONS.items() for f in cfg["files"]],
)
def test_template_files_are_kebab_case_and_non_empty(skill: str, filename: str) -> None:
    path = ROOT / skill / "templates" / filename
    assert path.is_file(), f"missing {path}"
    stem = path.stem
    assert stem == stem.lower(), f"non-lowercase filename: {filename}"
    assert "_" not in stem, f"underscores not allowed in kebab-case: {filename}"
    text = path.read_text(encoding="utf-8").strip()
    assert text, f"{path} is empty"
    assert text.startswith("# "), f"{path} should start with a H1 title"


@pytest.mark.parametrize("skill", sorted(SKILL_EXPECTATIONS))
def test_skill_md_advertises_templates(skill: str) -> None:
    skill_md = (ROOT / skill / "SKILL.md").read_text(encoding="utf-8")
    marker = SKILL_EXPECTATIONS[skill]["skill_marker"]
    assert marker in skill_md, (
        f"{skill}/SKILL.md does not advertise per-venue templates via '{marker}'"
    )


def test_thesis_templates_match_universities_source_byte_for_byte() -> None:
    """Stage-4 plan requires 1:1 content migration for the thesis suite."""
    pairs = [
        ("generic.md", "generic.md"),
        ("thuthesis.md", "tsinghua.md"),
        ("pkuthss.md", "pku.md"),
    ]
    for template_name, source_name in pairs:
        template = (ROOT / "latex-thesis-zh" / "templates" / template_name).read_text(
            encoding="utf-8"
        )
        source = (
            ROOT / "latex-thesis-zh" / "references" / "university-templates" / source_name
        ).read_text(encoding="utf-8")
        assert template == source, (
            f"templates/{template_name} drifted from university-templates/{source_name}"
        )
