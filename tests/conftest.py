"""Shared pytest configuration for script-based tests."""

import os
import shutil
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

SKILLS_ROOT = Path(__file__).parent.parent / "academic-writing-skills"

SCRIPT_DIR_EN = (
    Path(__file__).parent.parent / "academic-writing-skills" / "latex-paper-en" / "scripts"
)
SCRIPT_DIR_ZH = (
    Path(__file__).parent.parent / "academic-writing-skills" / "latex-thesis-zh" / "scripts"
)
SCRIPT_DIR_TYPST = (
    Path(__file__).parent.parent / "academic-writing-skills" / "typst-paper" / "scripts"
)
SCRIPT_DIR_AUDIT = (
    Path(__file__).parent.parent / "academic-writing-skills" / "paper-audit" / "scripts"
)

# Note: industrial-ai-research has no SCRIPT_DIR by design — it is a pure LLM
# workflow with no scripts/ directory. Its test (test_industrial_ai_research_skill.py)
# is a metadata smoke test that walks SKILL_DIR directly, so no sys.path entry is
# needed. bib-search-citation ships its own tests/ inside the skill folder and is
# discovered via the `just test` glob `academic-writing-skills/*/tests/`.

# Only add EN to sys.path (existing tests rely on bare `import parsers` etc.)
if str(SCRIPT_DIR_EN) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR_EN))

# Add ZH scripts (appended, not prepended — ZH tests use _load_zh() for priority)
if str(SCRIPT_DIR_ZH) not in sys.path:
    sys.path.append(str(SCRIPT_DIR_ZH))

# Add paper-audit scripts for audit tests
if str(SCRIPT_DIR_AUDIT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR_AUDIT))


def _cleanup_runtime_artifacts() -> None:
    for artifact_name in ("__pycache__", ".omc", ".omx"):
        for path in SKILLS_ROOT.rglob(artifact_name):
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)


@pytest.fixture(autouse=True)
def _clean_skill_runtime_artifacts():
    _cleanup_runtime_artifacts()
    yield
    _cleanup_runtime_artifacts()
