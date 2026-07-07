"""Skill version alignment with pyproject.toml.

All SKILL.md files must declare the same version as the project version in
pyproject.toml. This keeps released skill metadata, docs, and release notes
moving in lockstep so a release tag never points at heterogeneous skill
versions.
"""

from __future__ import annotations

import re

from tests.support.paths import REPO_ROOT, SKILLS_ROOT

PYPROJECT = REPO_ROOT / "pyproject.toml"
SKILL_NAMES = (
    "bib-search-citation",
    "cover-letter",
    "latex-paper-en",
    "latex-thesis-zh",
    "paper-audit",
    "typst-paper",
)

_PYPROJECT_VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE)
_FRONTMATTER_VERSION_RE = re.compile(r'^\s*version:\s*"?([^"\s]+)"?\s*$', re.MULTILINE)


def _pyproject_version() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    match = _PYPROJECT_VERSION_RE.search(text)
    assert match, "pyproject.toml must declare a top-level version"
    return match.group(1)


def _skill_frontmatter(skill_name: str) -> str:
    skill_md = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
    lines = skill_md.splitlines()
    assert lines and lines[0] == "---", f"{skill_name} SKILL.md missing frontmatter"
    end = next(i for i, line in enumerate(lines[1:], start=1) if line == "---")
    return "\n".join(lines[1:end])


def _skill_version(skill_name: str) -> str:
    frontmatter = _skill_frontmatter(skill_name)
    match = _FRONTMATTER_VERSION_RE.search(frontmatter)
    assert match, f"{skill_name} SKILL.md frontmatter missing version field"
    return match.group(1)


def test_all_skills_match_pyproject_version() -> None:
    project_version = _pyproject_version()
    mismatches: list[str] = []
    for skill_name in SKILL_NAMES:
        skill_version = _skill_version(skill_name)
        if skill_version != project_version:
            mismatches.append(
                f"{skill_name}: SKILL.md version={skill_version!r} "
                f"!= pyproject version={project_version!r}"
            )
    assert not mismatches, "Skill versions out of sync with pyproject.toml:\n" + "\n".join(
        mismatches
    )
