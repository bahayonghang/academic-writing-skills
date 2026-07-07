"""Stable filesystem paths shared by tests and pytest configuration."""

from pathlib import Path

TESTS_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = TESTS_ROOT.parent
SKILLS_ROOT = REPO_ROOT / "academic-writing-skills"

SCRIPT_DIR_EN = SKILLS_ROOT / "latex-paper-en" / "scripts"
SCRIPT_DIR_ZH = SKILLS_ROOT / "latex-thesis-zh" / "scripts"
SCRIPT_DIR_TYPST = SKILLS_ROOT / "typst-paper" / "scripts"
SCRIPT_DIR_AUDIT = SKILLS_ROOT / "paper-audit" / "scripts"
SCRIPT_DIR_COVER_LETTER = SKILLS_ROOT / "cover-letter" / "scripts"
