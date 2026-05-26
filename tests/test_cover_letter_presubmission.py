"""Tests for cover-letter presubmission mechanical checks."""

from __future__ import annotations

import importlib.util
import sys
from types import ModuleType

import yaml
from conftest import SCRIPT_DIR_COVER_LETTER

SKILL_ROOT = SCRIPT_DIR_COVER_LETTER.parent
TEMPLATES = SKILL_ROOT / "templates"
FIXTURES = SKILL_ROOT / "evals" / "fixtures"


def _load(module_name: str) -> ModuleType:
    path = SCRIPT_DIR_COVER_LETTER / f"{module_name}.py"
    if str(SCRIPT_DIR_COVER_LETTER) in sys.path:
        sys.path.remove(str(SCRIPT_DIR_COVER_LETTER))
    sys.path.insert(0, str(SCRIPT_DIR_COVER_LETTER))
    spec = importlib.util.spec_from_file_location(f"_cl_ps_{module_name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_templates_have_valid_frontmatter() -> None:
    """Every template must declare a YAML frontmatter with required keys."""
    required_keys = {"venue", "tier", "word_limit", "required_declarations"}
    for path in sorted(TEMPLATES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{path.name}: missing YAML frontmatter"
        end = text.find("\n---", 3)
        assert end > 0, f"{path.name}: malformed frontmatter delimiters"
        meta = yaml.safe_load(text[3:end])
        assert isinstance(meta, dict), f"{path.name}: frontmatter is not a mapping"
        missing = required_keys - set(meta)
        assert not missing, f"{path.name}: frontmatter missing keys {missing}"
        assert isinstance(meta["word_limit"], int)
        assert isinstance(meta["required_declarations"], list)


def test_ai_tone_detection_triggers_at_three_hits() -> None:
    """The optimize_fixture has many cover-letter cliché phrases; expect findings."""
    presub = _load("presubmission_check")
    issues = presub.run_checks(
        FIXTURES / "optimize_fixture_letter.md",
        journal="ieee-trans",
        skill_dir=SKILL_ROOT,
    )
    # The fixture salts in banned cliché phrases (J1*) and an opener cliché (L2*).
    cliche_codes = [i.code for i in issues if i.code.startswith(("J1", "L2"))]
    assert cliche_codes, "expected at least one cover-letter cliché finding"


def test_length_check_emits_minor_or_major_above_limit() -> None:
    """A letter that exceeds the template ceiling must produce L1."""
    presub = _load("presubmission_check")
    # Synthesize a long letter that exceeds the conference 400-word limit.
    long_letter = FIXTURES.parent / "_long_letter.md"
    body = "We demonstrate a strong result. " * 200  # ~1200 words
    long_letter.write_text(f"Dear Editor,\n\n{body}\n\nSincerely,\nA. Author\n", encoding="utf-8")
    try:
        issues = presub.run_checks(long_letter, journal="neurips", skill_dir=SKILL_ROOT)
        l1 = [i for i in issues if i.code == "L1"]
        assert l1, "expected L1 length violation"
        assert any(i.severity == "major" for i in l1)
    finally:
        long_letter.unlink()


def test_required_declarations_detected_in_well_formed_letter() -> None:
    """A letter that includes all required declarations should not raise D-* major findings."""
    presub = _load("presubmission_check")
    good_letter = FIXTURES.parent / "_good_letter.md"
    good_letter.write_text(
        "Dear Editor,\n\n"
        "We submit our manuscript. This manuscript has not been published elsewhere "
        "and is not under concurrent consideration. All authors have approved the "
        "submission. We declare no competing interests. Data and code will be made "
        "available upon acceptance.\n\n"
        "Sincerely,\nA. Author\n",
        encoding="utf-8",
    )
    try:
        issues = presub.run_checks(good_letter, journal="ieee-trans", skill_dir=SKILL_ROOT)
        major_decl = [i for i in issues if i.code.startswith("D-") and i.severity == "major"]
        assert not major_decl, (
            "all required declarations present; should be no major D-* findings: "
            f"{[i.message for i in major_decl]}"
        )
    finally:
        good_letter.unlink()


def test_presubmission_issue_schema_and_lowercase_severity() -> None:
    presub = _load("presubmission_check")
    issues = presub.run_checks(
        FIXTURES / "optimize_fixture_letter.md",
        journal="ieee-trans",
        skill_dir=SKILL_ROOT,
    )
    assert issues
    for issue in issues:
        assert issue.severity in {"major", "moderate", "minor"}
        assert issue.priority in {"P1", "P2", "P3"}
        assert issue.source_kind == "script"
        assert issue.comment_type in {"declaration_missing", "presentation", "tone"}
        assert issue.title
        assert issue.explanation


def test_no_latex_specific_rules_applied() -> None:
    """Cover-letter presubmission must NOT emit equation / label / citation-tilde rules."""
    presub = _load("presubmission_check")
    issues = presub.run_checks(
        FIXTURES / "optimize_fixture_letter.md",
        journal="ieee-trans",
        skill_dir=SKILL_ROOT,
    )
    forbidden_codes = {"L4", "L5", "L1-tex"}
    bad = [i for i in issues if i.code in forbidden_codes]
    assert not bad, f"cover-letter must not emit LaTeX-only codes: {[i.code for i in bad]}"
