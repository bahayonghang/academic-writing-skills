"""Contract tests for skill packaging, command hygiene, and runtime cleanliness."""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
SKILLS_ROOT = REPO_ROOT / "academic-writing-skills"
_DEFAULT_MANDATORY_SECTIONS = [
    "## Capability Summary",
    "## Triggering",
    "## Do Not Use",
    "## Module Router",
    "## Required Inputs",
    "## Output Contract",
    "## Workflow",
    "## Safety Boundaries",
    "## Reference Map",
    "## Example Requests",
]
SKILLS = {
    "latex-paper-en": {
        "modules": [
            "compile",
            "format",
            "bibliography",
            "grammar",
            "sentences",
            "logic",
            "expression",
            "translation",
            "title",
            "figures",
            "deai",
            "experiment",
        ],
    },
    "latex-thesis-zh": {
        "modules": [
            "compile",
            "format",
            "structure",
            "consistency",
            "template",
            "bibliography",
            "title",
            "deai",
            "experiment",
        ],
        "mandatory_sections": [
            "## Module Router",
            "## Workflow",
            "## Safety",
            "## Scope Exclusions",
        ],
    },
    "typst-paper": {
        "modules": [
            "compile",
            "format",
            "bibliography",
            "grammar",
            "sentences",
            "logic",
            "expression",
            "translation",
            "title",
            "deai",
            "experiment",
        ],
    },
}
COMMAND_RE = re.compile(r"(^|[\s`(])python\s+\S")
ROUTER_ROW_RE = re.compile(r"^\| `(?P<module>[^`]+)` \| .*? \| `(?P<command>[^`]+)` \|", re.MULTILINE)


def _iter_skill_text_files(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix in {".md", ".py", ".yaml", ".yml"}
    ]


def _command_violations(root: Path) -> list[str]:
    violations: list[str] = []
    for path in _iter_skill_text_files(root):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#!/usr/bin/env python3"):
                continue
            if stripped.startswith("```python"):
                continue
            if "uv run python" in line:
                continue
            if COMMAND_RE.search(line):
                violations.append(f"{path}:{line_no}: {stripped}")
            if "```uv run python" in line or "uv run python uv run python" in line:
                violations.append(f"{path}:{line_no}: malformed replacement -> {stripped}")
            if "pip install pyyaml" in stripped.lower():
                violations.append(f"{path}:{line_no}: legacy pip guidance -> {stripped}")
    return violations


def test_skill_assets_exist() -> None:
    for skill_name in SKILLS:
        root = SKILLS_ROOT / skill_name
        assert (root / "SKILL.md").exists()
        assert (root / "examples").is_dir()
        assert len(list((root / "examples").glob("*.md"))) >= 2
        assert (root / "evals" / "evals.json").exists()
        assert (root / "agents" / "openai.yaml").exists()


def test_skill_markdown_contract() -> None:
    for skill_name, config in SKILLS.items():
        skill_md = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
        for section in config.get("mandatory_sections", _DEFAULT_MANDATORY_SECTIONS):
            assert section in skill_md, f"{skill_name} missing section: {section}"
        for module_name in config["modules"]:
            assert f"`{module_name}`" in skill_md, f"{skill_name} missing module `{module_name}`"
        assert "uv run python" in skill_md


def test_skill_command_examples_use_uv_run_python() -> None:
    violations: list[str] = []
    for skill_name in SKILLS:
        violations.extend(_command_violations(SKILLS_ROOT / skill_name))
    assert not violations, "\n".join(violations)


def test_skill_directories_do_not_contain_runtime_artifacts() -> None:
    bad_paths: list[str] = []
    for skill_name in SKILLS:
        root = SKILLS_ROOT / skill_name
        for path in root.rglob("*"):
            if path.name in {"__pycache__", ".omc"}:
                bad_paths.append(str(path))
    assert not bad_paths, "\n".join(bad_paths)


def test_latex_skills_do_not_reference_typst_examples() -> None:
    bad_lines: list[str] = []
    for skill_name in ("latex-paper-en", "latex-thesis-zh"):
        root = SKILLS_ROOT / skill_name
        for path in _iter_skill_text_files(root):
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if "main.typ" in line:
                    bad_lines.append(f"{path}:{line_no}: {line.strip()}")
    assert not bad_lines, "\n".join(bad_lines)


def test_evals_json_shape() -> None:
    for skill_name in SKILLS:
        evals_path = SKILLS_ROOT / skill_name / "evals" / "evals.json"
        payload = json.loads(evals_path.read_text(encoding="utf-8"))
        assert payload["skill_name"] == skill_name
        assert isinstance(payload["evals"], list)
        assert len(payload["evals"]) >= 3
        for item in payload["evals"]:
            assert {"id", "prompt", "expected_output", "files"} <= set(item)
            assert isinstance(item["files"], list)


def test_openai_yaml_shape() -> None:
    required_keys = {"interface:", "display_name:", "short_description:", "default_prompt:"}
    for skill_name in SKILLS:
        yaml_text = (SKILLS_ROOT / skill_name / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        for key in required_keys:
            assert key in yaml_text, f"{skill_name} missing {key} in openai.yaml"


def test_latex_paper_en_module_router_commands_match_script_help() -> None:
    skill_root = SKILLS_ROOT / "latex-paper-en"
    skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    rows = ROUTER_ROW_RE.findall(skill_md)

    assert rows, "latex-paper-en module router table not found"

    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    for module_name, command in rows:
        tokens = shlex.split(command)
        script_token = next(token for token in tokens if token.startswith("$SKILL_DIR/"))
        script_path = skill_root / script_token.replace("$SKILL_DIR/", "")
        assert script_path.exists(), f"{module_name} script missing: {script_path}"

        result = subprocess.run(
            [sys.executable, "-B", str(script_path), "--help"],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        assert result.returncode == 0, f"{module_name} help failed: {result.stderr}"

        help_text = result.stdout + result.stderr
        for option in [token for token in tokens if token.startswith("--")]:
            assert option in help_text, f"{module_name} command advertises unsupported option {option}"
