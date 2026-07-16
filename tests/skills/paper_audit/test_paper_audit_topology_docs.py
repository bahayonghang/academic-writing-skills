"""Contract tests for paper-audit reviewer topology and issue schema docs."""

from tests.support.paths import SKILLS_ROOT

PAPER_AUDIT = SKILLS_ROOT / "paper-audit"
AGENTS = PAPER_AUDIT / "agents"
REFERENCES = PAPER_AUDIT / "references"


def test_agent_output_templates_use_canonical_severity() -> None:
    forbidden = ('"severity": "MAJOR"', '"severity": "CRITICAL"', '"severity": "Major"')
    agent_names = (
        "critical_reviewer_agent.md",
        "domain_reviewer_agent.md",
        "methodology_reviewer_agent.md",
        "literature_reviewer_agent.md",
        "editor_in_chief_agent.md",
    )

    for name in agent_names:
        content = (AGENTS / name).read_text(encoding="utf-8")
        assert not any(value in content for value in forbidden), name


def test_issue_schema_keeps_three_canonical_severity_levels() -> None:
    content = (REFERENCES / "ISSUE_SCHEMA.md").read_text(encoding="utf-8")

    assert '"severity": "major|moderate|minor"' in content
    assert '"severity": "critical|' not in content.lower()


def test_skill_md_has_no_specialized_dispatch_promise() -> None:
    content = (PAPER_AUDIT / "SKILL.md").read_text(encoding="utf-8")

    assert "4 specialized" not in content
    assert "revision_coach_agent.md" in content
    assert "not auto-dispatched" in content


def test_agent_roster_marks_playbooks_not_dispatched() -> None:
    content = (REFERENCES / "agent-roster.md").read_text(encoding="utf-8")

    assert "not auto-dispatched" in content
    assert "paper-audit-specialized-reviewer-wiring" in content


def test_deep_review_criteria_marks_specialized_agents_as_reference_playbooks() -> None:
    content = (REFERENCES / "DEEP_REVIEW_CRITERIA.md").read_text(encoding="utf-8")

    for name in (
        "domain_reviewer_agent.md",
        "methodology_reviewer_agent.md",
        "critical_reviewer_agent.md",
    ):
        matching_line = next(line for line in content.splitlines() if name in line)
        assert "reference playbook" in matching_line


def test_consensus_formula_consistent() -> None:
    synthesis = (AGENTS / "synthesis_agent.md").read_text(encoding="utf-8")
    editorial = (REFERENCES / "editorial_decision_standards.md").read_text(encoding="utf-8")

    for content in (synthesis, editorial):
        assert "floor(N/2)+1" in content
        assert "ceil(N/2)+1" not in content
    assert "N-1 of N" not in synthesis
    assert "8-dim" not in editorial


def test_synthesis_no_fourth_severity_level() -> None:
    content = (AGENTS / "synthesis_agent.md").read_text(encoding="utf-8").lower()

    assert "critical | major | moderate | minor" not in content
    assert "gate_blocker=true" in content


def test_committee_logic_has_surrender_protocol() -> None:
    content = (AGENTS / "committee_logic_agent.md").read_text(encoding="utf-8")

    assert "surrender_rate" in content
    assert '"issues": [...]' in content
    assert '"frame_lock_alert"' in content
