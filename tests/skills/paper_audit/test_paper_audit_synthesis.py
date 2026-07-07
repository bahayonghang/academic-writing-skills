"""Synthesis protocol, troubleshooting, and revision-coach contract tests.

These cover the v5.1 paper-audit additions:
- explicit Three-Step Synthesis Protocol in synthesis_agent.md
- F1-F8 review-quality failure paths in TROUBLESHOOTING.md
- editorial_decision_standards.md + quality_rubrics.md loaded by SKILL.md
- revision_coach_agent.md with the 6-step parsing protocol
- per-lane focus blocks in SUBAGENT_TEMPLATES.md
"""

from __future__ import annotations

from pathlib import Path

from tests.support.paths import SKILLS_ROOT

PAPER_AUDIT = SKILLS_ROOT / "paper-audit"
AGENTS = PAPER_AUDIT / "agents"
REFERENCES = PAPER_AUDIT / "references"
SKILL_MD = PAPER_AUDIT / "SKILL.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_synthesis_agent_references_editorial_standards() -> None:
    text = _read(AGENTS / "synthesis_agent.md")
    assert "editorial_decision_standards" in text, (
        "synthesis_agent.md must cite references/editorial_decision_standards.md"
    )
    assert "CONSENSUS" in text, "synthesis_agent.md must surface CONSENSUS labels"


def test_synthesis_agent_has_three_step_protocol() -> None:
    text = _read(AGENTS / "synthesis_agent.md")
    assert "Three-Step Synthesis Protocol" in text
    for step in ("Step 1", "Step 2", "Step 3"):
        assert step in text, f"synthesis_agent.md missing {step}"


def test_synthesis_agent_has_forbidden_operations() -> None:
    text = _read(AGENTS / "synthesis_agent.md")
    assert "## Forbidden Operations" in text
    section = text.split("## Forbidden Operations", 1)[1]
    bullet_count = sum(1 for line in section.splitlines() if line.strip().startswith("- "))
    assert bullet_count >= 5, (
        f"synthesis_agent.md Forbidden Operations must list at least 5 rules, got {bullet_count}"
    )
    assert "preserve" in section.lower() or "singleton" in section.lower(), (
        "Forbidden Operations must explicitly protect singleton findings"
    )


def test_troubleshooting_covers_canonical_failure_paths() -> None:
    text = _read(REFERENCES / "TROUBLESHOOTING.md")
    for failure_id in ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"):
        assert f"### {failure_id}" in text, (
            f"TROUBLESHOOTING.md missing canonical failure path {failure_id}"
        )
    assert "Review Quality Failure Paths" in text


def test_skill_review_standard_includes_editorial_and_rubrics() -> None:
    text = _read(SKILL_MD)
    assert "references/editorial_decision_standards.md" in text, (
        "SKILL.md Review Standard list must include editorial_decision_standards.md"
    )
    assert "references/quality_rubrics.md" in text, (
        "SKILL.md Review Standard list must include quality_rubrics.md"
    )


def test_revision_coach_agent_has_six_step_protocol() -> None:
    agent_path = AGENTS / "revision_coach_agent.md"
    assert agent_path.exists(), "revision_coach_agent.md must exist under agents/"
    text = _read(agent_path)
    for step in ("Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6"):
        assert step in text, f"revision_coach_agent.md missing {step}"
    assert "6-Step Parsing Protocol" in text


def test_subagent_templates_covers_all_cross_cutting_lanes() -> None:
    text = _read(REFERENCES / "SUBAGENT_TEMPLATES.md")
    for lane in (
        "claims_vs_evidence",
        "notation_and_numeric_consistency",
        "evaluation_fairness_and_reproducibility",
        "self_standard_consistency",
        "prior_art_and_novelty_grounding",
        "pre_submission_readiness",
    ):
        assert f"### Lane: {lane}" in text, (
            f"SUBAGENT_TEMPLATES.md missing focus block for lane {lane}"
        )


def test_revision_coach_listed_in_skill_lanes() -> None:
    text = _read(SKILL_MD)
    assert "revision_coach_agent.md" in text, (
        "SKILL.md Reviewer Lanes section must list revision_coach_agent.md"
    )


def test_mode_guide_has_auto_detection_block() -> None:
    text = _read(REFERENCES / "MODE_GUIDE.md")
    assert "### Auto-Detection at Intake" in text, (
        "MODE_GUIDE.md must include the Auto-Detection at Intake subsection"
    )
    assert "revision_coach_agent" in text, (
        "MODE_GUIDE.md Auto-Detection must dispatch revision_coach_agent for letter inputs"
    )
