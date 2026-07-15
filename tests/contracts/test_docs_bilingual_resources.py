from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

from tests.support.paths import REPO_ROOT

CHECKER_PATH = REPO_ROOT / "docs" / "scripts" / "check_resource_sync.py"
MANIFEST_PATH = REPO_ROOT / "docs" / "resource-manifest.json"


def _load_checker():
    spec = importlib.util.spec_from_file_location("docs_resource_checker", CHECKER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = _load_checker()


def test_resource_hash_normalizes_text_line_endings(tmp_path: Path) -> None:
    lf = tmp_path / "lf.md"
    crlf = tmp_path / "crlf.md"
    lf.write_bytes(b"# Guide\n\nBody\n")
    crlf.write_bytes(b"# Guide\r\n\r\nBody\r\n")
    assert checker.sha256(lf) == checker.sha256(crlf)


def test_manifest_matches_live_public_inventory() -> None:
    entries = checker.load_manifest(MANIFEST_PATH)
    assert not checker.validate_inventory(entries, REPO_ROOT)
    assert {entry["skill"] for entry in entries} == {
        "bib-search-citation",
        "cover-letter",
        "latex-paper-en",
        "latex-thesis-zh",
        "paper-audit",
        "typst-paper",
    }


def test_manifest_uses_canonical_bilingual_paths() -> None:
    entries = checker.load_manifest(MANIFEST_PATH)
    for entry in entries:
        suffix = Path(entry["source"]).relative_to(
            Path("academic-writing-skills") / entry["skill"] / entry["kind"]
        )
        assert (
            entry["en"]
            == (
                Path("docs") / "skills" / entry["skill"] / "resources" / entry["kind"] / suffix
            ).as_posix()
        )
        assert (
            entry["zh"]
            == (
                Path("docs")
                / "zh"
                / "skills"
                / entry["skill"]
                / "resources"
                / entry["kind"]
                / suffix
            ).as_posix()
        )


def test_markdown_comparison_preserves_protected_structure() -> None:
    source = """# Guide

Run `uv run tool --flag`.

| Field | Value |
| --- | --- |
| mode | strict |

```bash
uv run tool --flag
```

See [details](../references/detail.md).
"""
    translated = (
        source.replace("# Guide", "# 指南").replace("Run ", "运行 ").replace("See ", "参见 ")
    )
    assert not checker.compare_markdown(source, translated)
    assert checker.compare_markdown(source, translated.replace("--flag", "--other", 1))


def test_target_validation_supports_skill_and_full_scopes(tmp_path: Path) -> None:
    source = tmp_path / "academic-writing-skills" / "demo" / "references" / "guide.md"
    en = tmp_path / "docs" / "skills" / "demo" / "resources" / "references" / "guide.md"
    zh = tmp_path / "docs" / "zh" / "skills" / "demo" / "resources" / "references" / "guide.md"
    for path in (source, en, zh):
        path.parent.mkdir(parents=True, exist_ok=True)
    source_text = "# Guide\n\nRun `tool --flag`.\n"
    source.write_text(source_text, encoding="utf-8")
    en.write_text(source_text, encoding="utf-8")
    zh.write_text("# 指南\n\n运行 `tool --flag`。\n", encoding="utf-8")
    entry = {
        "skill": "demo",
        "kind": "references",
        "source": source.relative_to(tmp_path).as_posix(),
        "sourceLocale": "en",
        "sourceSha256": checker.sha256(source),
        "en": en.relative_to(tmp_path).as_posix(),
        "zh": zh.relative_to(tmp_path).as_posix(),
    }
    assert not checker.validate_targets([entry], tmp_path, skill="demo")
    assert not checker.validate_targets([entry], tmp_path)
    zh.unlink()
    assert checker.validate_targets([entry], tmp_path, skill="demo")


def test_target_validation_allows_synchronized_link_rewrites(tmp_path: Path) -> None:
    source = tmp_path / "academic-writing-skills" / "demo" / "references" / "guide.md"
    en = tmp_path / "docs" / "skills" / "demo" / "resources" / "references" / "guide.md"
    zh = tmp_path / "docs" / "zh" / "skills" / "demo" / "resources" / "references" / "guide.md"
    for path in (source, en, zh):
        path.parent.mkdir(parents=True, exist_ok=True)
    source_text = "# Guide\n\nSee [details](../references/detail.md).\n"
    source.write_text(source_text, encoding="utf-8")
    en.write_text("# Guide\n\nSee [details](../detail.md).\n", encoding="utf-8")
    zh.write_text("# 指南\n\n参见 [详情](../detail.md)。\n", encoding="utf-8")
    entry = {
        "skill": "demo",
        "kind": "references",
        "source": source.relative_to(tmp_path).as_posix(),
        "sourceLocale": "en",
        "sourceSha256": checker.sha256(source),
        "en": en.relative_to(tmp_path).as_posix(),
        "zh": zh.relative_to(tmp_path).as_posix(),
    }
    assert not checker.validate_targets([entry], tmp_path, skill="demo")

    zh.write_text("# 指南\n\n参见 [详情](../other.md)。\n", encoding="utf-8")
    assert "bilingual link targets differ" in "\n".join(
        checker.validate_targets([entry], tmp_path, skill="demo")
    )

    zh.write_text("# 指南\n\n参见 [详情](../detail.md)。\n", encoding="utf-8")
    en.write_text("# Changed\n\nSee [details](../detail.md).\n", encoding="utf-8")
    assert "must match source except rewritten link targets" in "\n".join(
        checker.validate_targets([entry], tmp_path, skill="demo")
    )


def test_inventory_only_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(CHECKER_PATH), "--inventory-only"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert f"({len(payload['resources'])} manifest entries)" in result.stdout


def _router_tokens(skill: str) -> set[str]:
    text = (REPO_ROOT / "academic-writing-skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    if skill == "paper-audit":
        section = text.split("## Mode Selection", 1)[1].split("## Review Standard", 1)[0]
        return set(re.findall(r"\|\s*`([^`]+)`\s*\|\s*$", section, flags=re.MULTILINE))
    section = text.split("## Module Router", 1)[1].split("\n## ", 1)[0]
    return set(re.findall(r"^\|\s*`([^`]+)`\s*\|", section, flags=re.MULTILINE))


def test_bilingual_usage_pages_cover_live_skill_routers() -> None:
    usage_pages = [
        (REPO_ROOT / "docs" / "usage.md").read_text(encoding="utf-8"),
        (REPO_ROOT / "docs" / "zh" / "usage.md").read_text(encoding="utf-8"),
    ]
    for skill in (
        "bib-search-citation",
        "cover-letter",
        "latex-paper-en",
        "latex-thesis-zh",
        "paper-audit",
        "typst-paper",
    ):
        tokens = _router_tokens(skill)
        assert tokens, f"failed to parse router for {skill}"
        for usage in usage_pages:
            missing = sorted(token for token in tokens if f"`{token}`" not in usage)
            assert not missing, f"{skill} router missing from usage page: {missing}"


def test_bilingual_installation_pages_list_all_six_skills() -> None:
    installation_pages = [
        (REPO_ROOT / "docs" / "installation.md").read_text(encoding="utf-8"),
        (REPO_ROOT / "docs" / "zh" / "installation.md").read_text(encoding="utf-8"),
    ]
    skills = {entry["skill"] for entry in checker.load_manifest(MANIFEST_PATH)}
    for installation in installation_pages:
        for skill in skills:
            command = f"npx skills add bahayonghang/academic-writing-skills/{skill}"
            assert command in installation


def test_vitepress_sidebar_uses_canonical_resource_discovery() -> None:
    config = (REPO_ROOT / "docs" / ".vitepress" / "config.ts").read_text(encoding="utf-8")
    assert 'const RESOURCE_KINDS = ["references", "templates", "examples", "agents"]' in config
    assert "function resourceItems(" in config
    for legacy_function in (
        "latexPaperEnItems",
        "latexThesisZhItems",
        "typstPaperItems",
        "bibSearchCitationItems",
        "paperAuditItems",
        "coverLetterItems",
    ):
        assert legacy_function not in config
