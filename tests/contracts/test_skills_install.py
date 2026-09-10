"""Installer for catalog skills into project agent skill directories."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from tests.support.paths import REPO_ROOT, SKILLS_ROOT

_INSTALLER_PATH = REPO_ROOT / "scripts" / "skills_install.py"
_SKILL_NAMES = (
    "bib-search-citation",
    "cover-letter",
    "latex-paper-en",
    "latex-thesis-zh",
    "paper-audit",
    "typst-paper",
)


def _load_installer():
    spec = importlib.util.spec_from_file_location("skills_install", _INSTALLER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


installer = _load_installer()


def _tiny_catalog(root: Path) -> Path:
    catalog = root / "catalog"
    for name in _SKILL_NAMES:
        skill_dir = catalog / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: test {name}\n---\n# {name}\n",
            encoding="utf-8",
        )
        (skill_dir / "scripts").mkdir()
        (skill_dir / "scripts" / "helper.py").write_text("# helper\n", encoding="utf-8")
    return catalog


def test_discover_skills_finds_six_catalog_packages() -> None:
    skills = installer.discover_skills(SKILLS_ROOT)
    names = [skill.name for skill in skills]
    assert names == list(_SKILL_NAMES)


def test_parse_selection_star_and_numbers() -> None:
    items = ["cover-letter", "paper-audit", "typst-paper"]
    assert installer.parse_selection("*", items) == items
    assert installer.parse_selection("1,3", items) == ["cover-letter", "typst-paper"]
    assert installer.parse_selection("1,1,2", items) == ["cover-letter", "paper-audit"]


def test_parse_selection_rejects_empty_and_range() -> None:
    with pytest.raises(ValueError, match="empty selection"):
        installer.parse_selection("  ", ["cover-letter"])
    with pytest.raises(ValueError, match="out of range"):
        installer.parse_selection("0", ["cover-letter"])


def test_list_does_not_write(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code = installer.main(["--list", "--source", str(SKILLS_ROOT), "--dest", str(tmp_path)])
    assert code == 0
    assert list(tmp_path.iterdir()) == []
    output = capsys.readouterr().out
    for name in _SKILL_NAMES:
        assert name in output


def test_unknown_skill_exits_nonzero(tmp_path: Path) -> None:
    code = installer.main(
        [
            "--copy",
            "-y",
            "--agent",
            "claude-code",
            "--source",
            str(SKILLS_ROOT),
            "--dest",
            str(tmp_path),
            "not-a-skill",
        ]
    )
    assert code == 1


def test_non_interactive_without_selection_fails() -> None:
    code = installer.main([], isatty=False)
    assert code == 1


def test_copy_installs_sibling_layout(tmp_path: Path) -> None:
    code = installer.main(
        [
            "--copy",
            "-y",
            "--agent",
            "claude-code",
            "--source",
            str(SKILLS_ROOT),
            "--dest",
            str(tmp_path),
            "paper-audit",
            "latex-paper-en",
        ]
    )
    assert code == 0
    skills_root = tmp_path / ".claude" / "skills"
    assert (skills_root / "paper-audit" / "SKILL.md").is_file()
    assert (skills_root / "latex-paper-en" / "scripts").is_dir()
    assert (skills_root / "paper-audit").parent == (skills_root / "latex-paper-en").parent
    assert not (skills_root / "latex-paper-en" / "scripts").is_symlink()


def test_paper_audit_only_warns(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    catalog = _tiny_catalog(tmp_path)
    dest = tmp_path / "project"
    code = installer.main(
        [
            "--copy",
            "-y",
            "--agent",
            "claude-code",
            "--source",
            str(catalog),
            "--dest",
            str(dest),
            "paper-audit",
        ]
    )
    assert code == 0
    captured = capsys.readouterr()
    assert "limited coverage" in captured.err
    assert (dest / ".claude" / "skills" / "paper-audit" / "SKILL.md").is_file()
    assert not (dest / ".claude" / "skills" / "latex-paper-en").exists()


def test_writing_skill_with_paper_audit_has_no_limited_warning(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    catalog = _tiny_catalog(tmp_path)
    dest = tmp_path / "project"
    code = installer.main(
        [
            "--copy",
            "-y",
            "--agent",
            "claude-code",
            "--source",
            str(catalog),
            "--dest",
            str(dest),
            "paper-audit",
            "latex-paper-en",
        ]
    )
    assert code == 0
    assert "limited coverage" not in capsys.readouterr().err


def test_replaces_existing_directory(tmp_path: Path) -> None:
    catalog = _tiny_catalog(tmp_path)
    dest = tmp_path / "project"
    skill_dir = dest / ".claude" / "skills" / "cover-letter"
    skill_dir.mkdir(parents=True)
    marker = skill_dir / "OLD.txt"
    marker.write_text("stale", encoding="utf-8")
    code = installer.main(
        [
            "--copy",
            "-y",
            "--agent",
            "claude-code",
            "--source",
            str(catalog),
            "--dest",
            str(dest),
            "cover-letter",
        ]
    )
    assert code == 0
    assert not marker.exists()
    assert (skill_dir / "SKILL.md").is_file()


def test_replace_symlink_does_not_delete_source(tmp_path: Path) -> None:
    catalog = _tiny_catalog(tmp_path)
    dest_parent = tmp_path / "project" / ".claude" / "skills"
    dest_parent.mkdir(parents=True)
    source = catalog / "cover-letter"
    link = dest_parent / "cover-letter"
    try:
        link.symlink_to(source.resolve(), target_is_directory=True)
    except OSError:
        pytest.skip("symlinks are not supported on this platform")
    code = installer.main(
        [
            "--copy",
            "-y",
            "--agent",
            "claude-code",
            "--source",
            str(catalog),
            "--dest",
            str(tmp_path / "project"),
            "cover-letter",
        ]
    )
    assert code == 0
    assert (source / "SKILL.md").is_file()
    assert not link.is_symlink()
    assert (link / "SKILL.md").is_file()


def test_symlink_points_at_source(tmp_path: Path) -> None:
    catalog = _tiny_catalog(tmp_path)
    dest = tmp_path / "project"
    dest_parent = dest / ".claude" / "skills"
    source = catalog / "cover-letter"
    try:
        installer.install_skill(source, dest_parent, "symlink")
    except OSError:
        pytest.skip("symlinks are not supported on this platform")
    installed = dest_parent / "cover-letter"
    assert installed.is_symlink()
    assert installed.resolve() == source.resolve()


def test_all_installs_every_agent(tmp_path: Path) -> None:
    catalog = _tiny_catalog(tmp_path)
    dest = tmp_path / "project"
    code = installer.main(
        [
            "--copy",
            "--all",
            "--source",
            str(catalog),
            "--dest",
            str(dest),
        ]
    )
    assert code == 0
    for rel in installer.AGENT_PATHS.values():
        for name in _SKILL_NAMES:
            assert (dest / rel / name / "SKILL.md").is_file()


def test_yes_defaults_agents_to_existing_harness_dirs(tmp_path: Path) -> None:
    catalog = _tiny_catalog(tmp_path)
    dest = tmp_path / "project"
    (dest / ".cursor").mkdir(parents=True)
    code = installer.main(
        [
            "--copy",
            "-y",
            "--source",
            str(catalog),
            "--dest",
            str(dest),
            "cover-letter",
        ]
    )
    assert code == 0
    assert (dest / ".cursor" / "skills" / "cover-letter" / "SKILL.md").is_file()
    assert not (dest / ".claude" / "skills" / "cover-letter").exists()
