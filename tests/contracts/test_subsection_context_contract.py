"""Cross-skill contract locks for subsection-context review windows."""

from __future__ import annotations

import re
from pathlib import Path

from audit import FOCUS_TO_ALLOWED_LANES, ROLE_TO_REVIEW_LANES

from tests.support.paths import SKILLS_ROOT

_CANONICAL = SKILLS_ROOT / "latex-thesis-zh" / "references" / "writing" / "subsection-context-zh.md"
_MIRROR = SKILLS_ROOT / "paper-audit" / "references" / "SUBSECTION_CONTEXT_PROTOCOL.md"
_PROTOCOL_SENTENCE = (
    "只有 current 可产出改写建议；prev.tail、next.head、parent_lead 一律只读，仅作证据。"
)
_MIRROR_PATH = "academic-writing-skills/paper-audit/references/SUBSECTION_CONTEXT_PROTOCOL.md"


def _contract_block(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"<!-- S-CTX-CONTRACT:BEGIN -->(.*?)<!-- S-CTX-CONTRACT:END -->",
        text,
        re.DOTALL,
    )
    assert match is not None
    return match.group(1)


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def test_canonical_and_mirror_contract_blocks_are_equal() -> None:
    assert _normalized(_contract_block(_CANONICAL)) == _normalized(_contract_block(_MIRROR))


def test_contract_locks_three_codes_and_removed_code() -> None:
    block = _contract_block(_MIRROR)
    codes = set(re.findall(r"S-CTX-(?:IN|OUT|ROLE|DUP)", block))
    assert codes == {"S-CTX-IN", "S-CTX-OUT", "S-CTX-ROLE"}
    assert "S-CTX-DUP" not in _CANONICAL.read_text(encoding="utf-8")
    assert "S-CTX-DUP" not in _MIRROR.read_text(encoding="utf-8")


def test_contract_contains_depth_no_fallback_and_permission_sentences() -> None:
    block = _contract_block(_MIRROR)
    assert "depth = level - root_level + 1" in block
    assert "无 depth-3 不回退" in block
    assert _PROTOCOL_SENTENCE in block


def test_consumers_reference_only_the_mirror_for_permission_contract() -> None:
    paper_audit = SKILLS_ROOT / "paper-audit"
    consumers = [
        paper_audit / "references" / "REVIEW_LANE_GUIDE.md",
        paper_audit / "references" / "SUBAGENT_TEMPLATES.md",
        paper_audit / "agents" / "section_reviewer_agent.md",
        paper_audit / "references" / "POLISH_GUIDE.md",
    ]
    for path in consumers:
        text = path.read_text(encoding="utf-8")
        assert _MIRROR_PATH in text
        assert _PROTOCOL_SENTENCE not in text
        assert "S-CTX-DUP" not in text


def test_lane_runtime_matrix_matches_contract_scope() -> None:
    lane = "subsection_context_polish"
    assert lane in FOCUS_TO_ALLOWED_LANES["full"]
    assert lane in FOCUS_TO_ALLOWED_LANES["logic"]
    assert lane not in FOCUS_TO_ALLOWED_LANES["methodology"]
    assert lane not in FOCUS_TO_ALLOWED_LANES["literature"]
    assert lane in ROLE_TO_REVIEW_LANES["logic"]


def test_issue_schema_adds_optional_subsection_fields_without_required_drift() -> None:
    schema = (SKILLS_ROOT / "paper-audit" / "references" / "ISSUE_SCHEMA.md").read_text(
        encoding="utf-8"
    )
    required_block = re.search(
        r"## Required fields\s+(.*?)\s+## Guidance",
        schema,
        re.DOTALL,
    )
    assert required_block is not None
    assert re.findall(r"^- `([^`]+)`$", required_block.group(1), re.MULTILINE) == [
        "title",
        "quote",
        "explanation",
        "comment_type",
        "severity",
        "source_kind",
    ]
    assert '"subsection_id": "2.1.1"' in schema
    assert '"context_sides": ["current", "prev.tail"]' in schema
    assert "optional subsection-context fields" in schema
    assert 'source_kind: "llm"' in schema
    assert 'severity: "minor"' in schema
    assert 'severity: "moderate"' in schema


def test_polish_guide_preserves_long_unit_and_section_fallback_semantics() -> None:
    guide = (SKILLS_ROOT / "paper-audit" / "references" / "POLISH_GUIDE.md").read_text(
        encoding="utf-8"
    )
    context_section = guide.split("### Context Window Management", 1)[1]
    assert 'subsection_windows.status == "ok"' in context_section
    assert "artifacts/windows/<id>.json" in context_section
    assert "1200 words" in context_section
    assert "paragraph boundaries" in context_section
    assert 'subsection_windows.status != "ok"' in context_section
    assert "section-level" in context_section


def test_skill_routes_are_updated_without_version_bumps() -> None:
    paper_skill = (SKILLS_ROOT / "paper-audit" / "SKILL.md").read_text(encoding="utf-8")
    zh_skill = (SKILLS_ROOT / "latex-thesis-zh" / "SKILL.md").read_text(encoding="utf-8")

    for text in (paper_skill, zh_skill):
        assert 'version: "6.0.0"' in text
        assert 'last_updated: "2026-08-30"' in text

    assert "subsection_context_polish" in paper_skill
    assert "references/SUBSECTION_CONTEXT_PROTOCOL.md" in paper_skill
    paper_mode_router = paper_skill.split("## Mode Selection", 1)[1].split(
        "## Review Standard",
        1,
    )[0]
    assert "subsection_context_polish" in paper_mode_router
    for flag in ("--subsection-context", "--subsection", "--emit-window"):
        assert flag in zh_skill
