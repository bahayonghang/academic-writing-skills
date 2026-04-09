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
    "industrial-ai-research": {
        "modules": [
            "research",
            "survey-outline",
            "survey-evidence",
            "survey-write",
            "survey-merge",
        ],
        "min_examples": 4,
        "min_evals": 4,
        "expects_uv_commands": False,
    },
    "latex-paper-en": {
        "modules": [
            "compile",
            "format",
            "bibliography",
            "grammar",
            "sentences",
            "logic",
            "literature",
            "expression",
            "translation",
            "title",
            "figures",
            "pseudocode",
            "deai",
            "experiment",
        ],
        "min_examples": 5,
        "min_evals": 6,
        "expects_uv_commands": True,
        "router_help": True,
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
            "logic",
            "literature",
            "experiment",
        ],
        "min_examples": 3,
        "min_evals": 5,
        "expects_uv_commands": True,
        "router_help": True,
    },
    "paper-audit": {
        "modules": ["self-check", "review", "gate", "polish", "re-audit"],
        "mandatory_sections": [
            "## What This Skill Produces",
            "## Do Not Use",
            "## Critical Rules",
            "## Mode Selection",
            "## Review Standard",
            "## Workflow",
            "## Output Contract",
            "## References",
        ],
        "min_examples": 3,
        "min_evals": 5,
        "expects_uv_commands": True,
    },
    "typst-paper": {
        "modules": [
            "compile",
            "format",
            "bibliography",
            "grammar",
            "sentences",
            "logic",
            "literature",
            "expression",
            "translation",
            "title",
            "pseudocode",
            "deai",
            "experiment",
        ],
        "min_examples": 3,
        "min_evals": 5,
        "expects_uv_commands": True,
        "router_help": True,
    },
}
COMMAND_RE = re.compile(r"(^|[\s`(])python\s+\S")
ROUTER_ROW_RE = re.compile(
    r"^\| `(?P<module>[^`]+)` \| .*? \| `(?P<command>[^`]+)` \|", re.MULTILINE
)


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
    for skill_name, config in SKILLS.items():
        root = SKILLS_ROOT / skill_name
        assert (root / "SKILL.md").exists()
        assert (root / "examples").is_dir()
        assert len(list((root / "examples").glob("*.md"))) >= config.get("min_examples", 3)
        assert (root / "evals" / "evals.json").exists()
        openai_yaml = root / "agents" / "openai.yaml"
        if openai_yaml.exists():
            pass  # optional; paper-audit removed it in v3.0


def test_skill_markdown_contract() -> None:
    for skill_name, config in SKILLS.items():
        skill_md = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
        for section in config.get("mandatory_sections", _DEFAULT_MANDATORY_SECTIONS):
            assert section in skill_md, f"{skill_name} missing section: {section}"
        for module_name in config["modules"]:
            assert f"`{module_name}`" in skill_md, f"{skill_name} missing module `{module_name}`"
        if config.get("expects_uv_commands", False):
            assert "uv run python" in skill_md


def test_skill_command_examples_use_uv_run_python() -> None:
    violations: list[str] = []
    for skill_name, config in SKILLS.items():
        if not config.get("expects_uv_commands", False):
            continue
        if not config.get("enforce_command_hygiene", skill_name != "paper-audit"):
            continue
        violations.extend(_command_violations(SKILLS_ROOT / skill_name))
    assert not violations, "\n".join(violations)


def test_skill_directories_do_not_contain_runtime_artifacts() -> None:
    bad_paths: list[str] = []
    for skill_name in SKILLS:
        root = SKILLS_ROOT / skill_name
        for path in root.rglob("*"):
            if path.name in {"__pycache__", ".omc", ".omx"}:
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
    for skill_name, config in SKILLS.items():
        evals_path = SKILLS_ROOT / skill_name / "evals" / "evals.json"
        payload = json.loads(evals_path.read_text(encoding="utf-8"))
        assert payload["skill_name"] == skill_name
        assert isinstance(payload["evals"], list)
        assert len(payload["evals"]) >= config.get("min_evals", 4)
        for item in payload["evals"]:
            assert {"id", "prompt", "expected_output", "files"} <= set(item)
            assert isinstance(item["files"], list)


def test_paper_audit_evals_contracts_are_artifact_and_schema_aware() -> None:
    evals_path = SKILLS_ROOT / "paper-audit" / "evals" / "evals.json"
    payload = json.loads(evals_path.read_text(encoding="utf-8"))
    evals_by_id = {item["id"]: item for item in payload["evals"]}

    deep_review_ids = {2, 3, 4, 7}
    for eval_id in deep_review_ids:
        item = evals_by_id[eval_id]
        assertion_text = "\n".join(
            assertion.get("text", "") + assertion.get("pattern", "")
            for assertion in item["assertions"]
        )
        assert "deep-review" in assertion_text, (
            f"paper-audit eval {eval_id} must assert canonical deep-review mode"
        )

    artifact_assertions = "\n".join(
        assertion.get("text", "") + assertion.get("pattern", "")
        for assertion in evals_by_id[2]["assertions"]
    )
    assert "final_issues\\.json" in artifact_assertions
    assert "review_report\\.md" in artifact_assertions

    schema_assertions = "\n".join(
        assertion.get("text", "") + assertion.get("pattern", "")
        for assertion in evals_by_id[3]["assertions"]
    )
    assert "review_lane" in schema_assertions
    assert "source_kind" in schema_assertions
    assert "source_section" in schema_assertions or "Related Sections" in schema_assertions

    gate_assertions = "\n".join(
        assertion.get("text", "") + assertion.get("pattern", "")
        for assertion in evals_by_id[5]["assertions"]
    )
    assert "Deep Review Report" in gate_assertions
    assert any(assertion["type"] == "not_contains" for assertion in evals_by_id[5]["assertions"])

    polish_assertions = "\n".join(
        assertion.get("text", "") + assertion.get("pattern", "")
        for assertion in evals_by_id[8]["assertions"]
    )
    assert "Deep Review Report" in polish_assertions
    assert any(assertion["type"] == "not_contains" for assertion in evals_by_id[8]["assertions"])


def test_paper_audit_evals_use_real_mode_specific_fixtures() -> None:
    skill_root = SKILLS_ROOT / "paper-audit"
    evals_path = skill_root / "evals" / "evals.json"
    payload = json.loads(evals_path.read_text(encoding="utf-8"))
    evals_by_id = {item["id"]: item for item in payload["evals"]}

    for item in payload["evals"]:
        assert item["files"], f"paper-audit eval {item['id']} must bind to real fixture inputs"
        for rel_path in item["files"]:
            fixture_path = skill_root / rel_path
            assert fixture_path.exists(), (
                f"paper-audit eval {item['id']} missing fixture: {rel_path}"
            )

    assert evals_by_id[1]["files"] == ["evals/fixtures/quick_audit_fixture.tex"]
    assert evals_by_id[5]["files"] == ["evals/fixtures/gate_ieee_fixture.tex"]
    assert evals_by_id[8]["files"] == ["evals/fixtures/polish_fixture.tex"]

    for eval_id in {2, 3, 4, 7}:
        assert evals_by_id[eval_id]["files"] == ["evals/fixtures/deep_review_fixture.tex"]

    assert evals_by_id[6]["files"] == [
        "evals/fixtures/deep_review_fixture.tex",
        "evals/fixtures/previous_final_issues.json",
        "evals/fixtures/previous_review_report.md",
    ]


def test_paper_audit_skill_argument_hint_matches_cli_contract() -> None:
    skill_root = SKILLS_ROOT / "paper-audit"
    skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")

    assert "# Paper Audit Skill v4.4" in skill_md
    assert "--report-style deep-review|peer-review" in skill_md
    assert "--focus full|editor|theory|literature|methodology|logic" in skill_md
    assert "--format md|json" in skill_md
    assert "markdown|json" not in skill_md

    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    audit_script = skill_root / "scripts" / "audit.py"
    result = subprocess.run(
        [sys.executable, "-B", str(audit_script), "--help"],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert result.returncode == 0, result.stderr
    help_text = result.stdout + result.stderr
    for flag in ("--report-style", "--focus", "--format"):
        assert flag in help_text, f"paper-audit help missing supported flag {flag}"


def test_openai_yaml_shape() -> None:
    required_keys = {"interface:", "display_name:", "short_description:", "default_prompt:"}
    for skill_name in SKILLS:
        yaml_path = SKILLS_ROOT / skill_name / "agents" / "openai.yaml"
        if not yaml_path.exists():
            continue  # optional; paper-audit removed it in v3.0
        yaml_text = yaml_path.read_text(encoding="utf-8")
        for key in required_keys:
            assert key in yaml_text, f"{skill_name} missing {key} in openai.yaml"


def _assert_module_router_commands_match_script_help(skill_name: str) -> None:
    skill_root = SKILLS_ROOT / skill_name
    skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    rows = ROUTER_ROW_RE.findall(skill_md)

    assert rows, f"{skill_name} module router table not found"

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
            assert option in help_text, (
                f"{module_name} command advertises unsupported option {option}"
            )


def test_latex_paper_en_module_router_commands_match_script_help() -> None:
    _assert_module_router_commands_match_script_help("latex-paper-en")


def test_latex_thesis_zh_module_router_commands_match_script_help() -> None:
    _assert_module_router_commands_match_script_help("latex-thesis-zh")


def test_typst_paper_module_router_commands_match_script_help() -> None:
    _assert_module_router_commands_match_script_help("typst-paper")
