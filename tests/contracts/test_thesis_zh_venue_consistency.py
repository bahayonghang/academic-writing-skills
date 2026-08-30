"""Directional coverage among thesis-zh extra_checks, CHECKLIST, and VENUE_RULES."""

from __future__ import annotations

import ast
import re

from tests.support.paths import SKILLS_ROOT

AUDIT = SKILLS_ROOT / "paper-audit" / "scripts" / "audit.py"
CHECKLIST = SKILLS_ROOT / "paper-audit" / "references" / "CHECKLIST.md"
VENUE_RULES = SKILLS_ROOT / "paper-audit" / "references" / "VENUE_RULES.md"
ROSTER = SKILLS_ROOT / "paper-audit" / "references" / "agent-roster.md"
SKILL = SKILLS_ROOT / "paper-audit" / "SKILL.md"
YANSHAN = SKILLS_ROOT / "latex-thesis-zh" / "templates" / "yanshan.md"
PKUTHSS = SKILLS_ROOT / "latex-thesis-zh" / "templates" / "pkuthss.md"

EC_RE = re.compile(r"TZ-EC-([a-z0-9-]+)")
CL_RE = re.compile(r"TZ-CL-([a-z0-9-]+)")


def _thesis_zh_extra_checks() -> list[tuple[str, str]]:
    tree = ast.parse(AUDIT.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", None) == "VENUE_CONFIG":
            assert isinstance(node.value, ast.Dict)
            for key, value in zip(node.value.keys, node.value.values, strict=True):
                if isinstance(key, ast.Constant) and key.value == "thesis-zh":
                    assert isinstance(value, ast.Dict)
                    for field, field_value in zip(value.keys, value.values, strict=True):
                        if isinstance(field, ast.Constant) and field.value == "extra_checks":
                            assert isinstance(field_value, ast.List)
                            rows: list[tuple[str, str]] = []
                            for elt in field_value.elts:
                                assert isinstance(elt, ast.Tuple) and len(elt.elts) == 2
                                label = ast.literal_eval(elt.elts[0])
                                pattern = ast.literal_eval(elt.elts[1])
                                rows.append((str(label), str(pattern)))
                            return rows
    raise AssertionError("VENUE_CONFIG['thesis-zh'] extra_checks not found")


def test_each_tz_ec_has_checklist_and_venue_rules() -> None:
    extra = _thesis_zh_extra_checks()
    checklist = CHECKLIST.read_text(encoding="utf-8")
    rules = VENUE_RULES.read_text(encoding="utf-8")
    slugs = []
    for label, _pattern in extra:
        match = EC_RE.search(label)
        assert match, label
        slug = match.group(1)
        slugs.append(slug)
        assert f"TZ-CL-{slug}" in checklist
        assert f"TZ-EC-{slug}" in rules
    assert slugs
    # Reverse equality is not required: checklist may contain human-only items.
    cl_slugs = set(CL_RE.findall(checklist))
    assert set(slugs) <= cl_slugs
    assert "appendix-optional" in cl_slugs
    assert "symbols-optional" in cl_slugs


def test_extra_checks_omit_optional_chapters() -> None:
    joined = " ".join(label for label, _pattern in _thesis_zh_extra_checks())
    assert "附录" not in joined
    assert "符号" not in joined
    yanshan = YANSHAN.read_text(encoding="utf-8")
    pkuthss = PKUTHSS.read_text(encoding="utf-8")
    assert (
        "附录（可省）" in yanshan
        or "附录 (可省)" in yanshan
        or "附录（可省）" in yanshan.replace(" ", "")
    )
    assert "可省" in yanshan
    assert "非必备章节" in pkuthss or "条件项" in pkuthss


def test_thesis_zh_has_no_required_sections_or_page_limit() -> None:
    tree = ast.parse(AUDIT.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", None) == "VENUE_CONFIG":
            assert isinstance(node.value, ast.Dict)
            for key, value in zip(node.value.keys, node.value.values, strict=True):
                if isinstance(key, ast.Constant) and key.value == "thesis-zh":
                    assert isinstance(value, ast.Dict)
                    fields = {
                        field.value for field in value.keys if isinstance(field, ast.Constant)
                    }
                    assert "required_sections" not in fields
                    assert "page_limit" not in fields
                    assert "blind_review" in fields
                    return
    raise AssertionError("thesis-zh config missing")


def test_criteria_file_is_not_on_agent_roster() -> None:
    roster = ROSTER.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")
    assert "ZH_THESIS_REVIEW_CRITERIA.md" not in roster
    assert "zh_thesis_reviewer_agent.md" in roster
    assert "ZH_THESIS_REVIEW_CRITERIA.md" in skill
    assert "zh_thesis_reviewer_agent.md" in skill
