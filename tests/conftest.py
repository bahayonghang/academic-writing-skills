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
SCRIPT_DIR_COVER_LETTER = (
    Path(__file__).parent.parent / "academic-writing-skills" / "cover-letter" / "scripts"
)

# bib-search-citation ships its own tests/ inside the skill folder and is discovered
# via the `just test` glob `academic-writing-skills/*/tests/`.

# Only add EN to sys.path (existing tests rely on bare `import parsers` etc.)
if str(SCRIPT_DIR_EN) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR_EN))

# Add ZH scripts (appended, not prepended — ZH tests use _load_zh() for priority)
if str(SCRIPT_DIR_ZH) not in sys.path:
    sys.path.append(str(SCRIPT_DIR_ZH))

# Add paper-audit scripts for audit tests
if str(SCRIPT_DIR_AUDIT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR_AUDIT))

# Cover-letter scripts: appended (not prepended) so they never shadow the
# canonical EN/AUDIT `parsers` on the default sys.path. Cover-letter tests load
# their scripts via importlib in a `_load` helper that temporarily evicts the
# shared `parsers`/`tex_loader` modules and puts the cover-letter dir at
# sys.path[0], then restores both — so each test sees the cover-letter copy
# without leaking it to EN/AUDIT tests.
if str(SCRIPT_DIR_COVER_LETTER) not in sys.path:
    sys.path.append(str(SCRIPT_DIR_COVER_LETTER))


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
