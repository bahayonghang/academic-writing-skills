"""Contract tests for skill packaging, command hygiene, and runtime cleanliness."""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

from tests.support.paths import REPO_ROOT, SKILLS_ROOT

MIN_SKILL_DESCRIPTION_CHARS = 120
MAX_SKILL_DESCRIPTION_CHARS = 400
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
    "bib-search-citation": {
        "modules": ["query", "spec-json", "spec-file", "preview"],
        "min_examples": 3,
        "min_evals": 5,
        "expects_uv_commands": True,
        "enforce_command_hygiene": True,
        "router_help": True,
    },
    "cover-letter": {
        "modules": ["generate", "optimize", "align-check", "journal-fit", "presubmission"],
        "min_examples": 4,
        "min_evals": 6,
        "expects_uv_commands": True,
        "router_help": True,
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
            "tables",
            "caption",
            "abstract",
            "section-writing",
            "adapt",
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
            "references",
            "title",
            "deai",
            "logic",
            "literature",
            "experiment",
            "tables",
            "abstract",
            "spec-check",
        ],
        "min_examples": 3,
        "min_evals": 5,
        "expects_uv_commands": True,
        "router_help": True,
    },
    "paper-audit": {
        "modules": ["quick-audit", "deep-review", "gate", "re-audit", "polish"],
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
            "tables",
            "references",
            "abstract",
            "adapt",
        ],
        "min_examples": 3,
        "min_evals": 5,
        "expects_uv_commands": True,
        "router_help": True,
    },
}
COMMAND_RE = re.compile(r"(^|[\s`(])python\s+\S")
REFERENCE_LAYOUTS = {
    "latex-paper-en": {
        "citations",
        "deai",
        "evidence",
        "formatting",
        "latex",
        "modules",
        "review",
        "venues",
        "writing",
    },
    "latex-thesis-zh": {
        "citations",
        "deai",
        "formatting",
        "latex",
        "modules",
        "writing",
    },
}
KEBAB_CASE_FILE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.(?:md|ya?ml)$")
# Whitespace-tolerant so the row still parses whether the markdown table is
# compact (`| `mod` | ... |`) or column-aligned by a formatter (`| `mod`   | ... |`).
ROUTER_ROW_RE = re.compile(
    r"^\|\s*`(?P<module>[^`]+)`\s*\|.*?\|\s*`(?P<command>[^`]+)`\s*\|", re.MULTILINE
)


def _frontmatter_description(skill_md: str) -> str:
    lines = skill_md.splitlines()
    assert lines and lines[0] == "---"

    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            break
        if not line.startswith("description:"):
            continue

        value = line.removeprefix("description:").strip()
        if value.startswith((">", "|")):
            block_lines: list[str] = []
            for block_line in lines[index + 1 :]:
                if block_line == "---" or (block_line and not block_line[0].isspace()):
                    break
                if block_line.strip():
                    block_lines.append(block_line.strip())
            return " ".join(block_lines)

        return value.strip("\"'")

    raise AssertionError("missing frontmatter description")


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


def test_skill_security_boundaries_are_declared() -> None:
    for skill_name in SKILLS:
        skill_md = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "untrusted" in skill_md.lower(), f"{skill_name} must mark source data untrusted"

    assert "allowed-tools: Read, Bash(uv *)" in (
        SKILLS_ROOT / "bib-search-citation" / "SKILL.md"
    ).read_text(encoding="utf-8")
    for skill_name in ("latex-paper-en", "latex-thesis-zh", "typst-paper"):
        skill_md = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "allowed-tools: Read, Glob, Grep, Bash(uv *)" in skill_md
        assert "Bash(latexmk *)" not in skill_md
        assert "Bash(typst *)" not in skill_md
    for skill_name in ("latex-paper-en", "latex-thesis-zh"):
        skill_md = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "--trusted-source" in skill_md


def test_latex_reference_configs_disable_shell_escape_by_default() -> None:
    bad_lines: list[str] = []
    unsafe_engine_config = re.compile(r"\$[a-z]*latex\s*=\s*['\"][^'\"]*(?<!no)-shell-escape")
    for skill_name in ("latex-paper-en", "latex-thesis-zh"):
        for path in (SKILLS_ROOT / skill_name / "references").rglob("*.md"):
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if unsafe_engine_config.search(line):
                    bad_lines.append(f"{path}:{line_no}: {line.strip()}")
    assert not bad_lines, "\n".join(bad_lines)


def test_latex_reference_layout_is_discoverable_and_kebab_case() -> None:
    violations: list[str] = []
    for skill_name, allowed_dirs in REFERENCE_LAYOUTS.items():
        references_dir = SKILLS_ROOT / skill_name / "references"
        top_files = [path.name for path in references_dir.iterdir() if path.is_file()]
        if top_files:
            violations.append(f"{skill_name}: top-level reference files: {sorted(top_files)}")

        top_dirs = {path.name for path in references_dir.iterdir() if path.is_dir()}
        unexpected_dirs = top_dirs - allowed_dirs
        missing_dirs = allowed_dirs - top_dirs
        if unexpected_dirs:
            violations.append(f"{skill_name}: unexpected reference dirs: {sorted(unexpected_dirs)}")
        if missing_dirs:
            violations.append(f"{skill_name}: missing reference dirs: {sorted(missing_dirs)}")

        for path in references_dir.rglob("*"):
            if path.is_file() and not KEBAB_CASE_FILE_RE.fullmatch(path.name):
                rel_path = path.relative_to(SKILLS_ROOT / skill_name).as_posix()
                violations.append(f"{skill_name}: non-kebab-case reference file: {rel_path}")

    assert not violations, "\n".join(violations)


def test_arxiv_references_use_https() -> None:
    bad_lines: list[str] = []
    insecure_arxiv_url = "http://" + "export.arxiv.org/api/query"
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".py"}:
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if insecure_arxiv_url in line:
                bad_lines.append(f"{path}:{line_no}: {line.strip()}")
    assert not bad_lines, "\n".join(bad_lines)


def test_skill_frontmatter_description_stays_within_runtime_limit() -> None:
    for skill_name in SKILLS:
        skill_md = (SKILLS_ROOT / skill_name / "SKILL.md").read_text(encoding="utf-8")
        description = _frontmatter_description(skill_md)
        description_len = len(description)
        assert MIN_SKILL_DESCRIPTION_CHARS <= description_len <= MAX_SKILL_DESCRIPTION_CHARS, (
            f"{skill_name} description has {description_len} characters; "
            f"expected {MIN_SKILL_DESCRIPTION_CHARS}-{MAX_SKILL_DESCRIPTION_CHARS}"
        )


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

    # The H1 version must track the frontmatter version (major.minor) rather
    # than a hardcoded literal, so the contract never silently locks a stale
    # version against the frontmatter single source.
    version_match = re.search(r'^\s*version:\s*"?(\d+)\.(\d+)\.\d+"?', skill_md, re.MULTILINE)
    assert version_match, "paper-audit SKILL.md frontmatter must declare a version"
    major, minor = version_match.group(1), version_match.group(2)
    assert f"# Paper Audit Skill v{major}.{minor}" in skill_md, (
        f"SKILL.md H1 must read 'Paper Audit Skill v{major}.{minor}' to match frontmatter"
    )
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


def test_typst_paper_evals_bind_to_real_fixtures() -> None:
    """typst-paper evals must bind to real fixture files (mirrors paper-audit)."""
    skill_root = SKILLS_ROOT / "typst-paper"
    payload = json.loads((skill_root / "evals" / "evals.json").read_text(encoding="utf-8"))
    bound = [item for item in payload["evals"] if item["files"]]
    assert len(bound) >= 8, f"expected >= 8 fixture-bound typst evals, got {len(bound)}"
    for item in bound:
        for rel_path in item["files"]:
            fixture_path = skill_root / rel_path
            assert fixture_path.exists(), (
                f"typst eval {item['id']} references missing fixture: {rel_path}"
            )
    # The two mini-projects (template + bare) and both bibliography formats exist.
    for required in (
        "evals/fixtures/charged_ieee_fixture.typ",
        "evals/fixtures/refs.bib",
        "evals/fixtures/bare_fixture.typ",
        "evals/fixtures/refs.yml",
    ):
        assert (skill_root / required).exists(), f"missing fixture asset: {required}"


def test_typst_paper_router_section_values_resolve() -> None:
    """Every ``--section <value>`` in the typst router must be a recognized
    section identifier — a canonical key or a known alias (guards the T3 blind
    spot: a router command naming a section the parser can never produce, e.g.
    ``methods`` when the key is ``method``)."""
    skill_root = SKILLS_ROOT / "typst-paper"
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "_typst_parsers_section", skill_root / "scripts" / "parsers.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    canonical = {key for key, _level, _pat in mod.TypstParser.SECTION_TITLE_RULES}
    valid = canonical | set(mod.SECTION_KEY_ALIASES)

    skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    section_values = re.findall(r"--section\s+([A-Za-z]+)", skill_md)
    # Skip generic placeholders like "--section <name>" / "--section SECTION".
    section_values = [v for v in section_values if not v.isupper()]
    assert section_values, "no --section values found in typst router"
    for value in section_values:
        assert value.lower() in valid, (
            f"router --section {value} is not a canonical key or alias; "
            f"known identifiers: {sorted(valid)}"
        )


def test_typst_paper_module_doc_flags_match_script_help() -> None:
    """Every ``--flag`` advertised in a typst module doc must exist in that
    script's --help (guards T12-T15: docs that described the LaTeX-sibling CLI)."""
    skill_root = SKILLS_ROOT / "typst-paper"
    modules_dir = skill_root / "references" / "modules"
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    help_cache: dict[str, str] = {}

    def _help(script_name: str) -> str:
        if script_name not in help_cache:
            result = subprocess.run(
                [sys.executable, "-B", str(skill_root / "scripts" / script_name), "--help"],
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            assert result.returncode == 0, f"{script_name} --help failed: {result.stderr}"
            help_cache[script_name] = result.stdout + result.stderr
        return help_cache[script_name]

    cmd_re = re.compile(r"scripts/(\w+\.py)([^\n`]*)")
    flag_re = re.compile(r"\s(--[a-z][\w-]*)")
    checked = 0
    for doc in modules_dir.glob("*.md"):
        for script_name, rest in cmd_re.findall(doc.read_text(encoding="utf-8")):
            script_path = skill_root / "scripts" / script_name
            if not script_path.exists():
                continue
            help_text = _help(script_name)
            for flag in flag_re.findall(rest):
                checked += 1
                assert flag in help_text, (
                    f"{doc.name}: {script_name} doc advertises unsupported flag {flag}"
                )
    assert checked > 0, "no module-doc CLI flags were validated"


def test_cover_letter_module_router_commands_match_script_help() -> None:
    _assert_module_router_commands_match_script_help("cover-letter")


def test_bib_search_citation_module_router_commands_match_script_help() -> None:
    _assert_module_router_commands_match_script_help("bib-search-citation")
