"""Shared pytest configuration for script-based tests."""

import sys
from pathlib import Path

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

# Only add EN to sys.path (existing tests rely on bare `import parsers` etc.)
if str(SCRIPT_DIR_EN) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR_EN))

# Add paper-audit scripts for audit tests
if str(SCRIPT_DIR_AUDIT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR_AUDIT))
