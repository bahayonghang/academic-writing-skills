"""Cross-surface contract for paragraph-arc observations in paper-audit."""

from __future__ import annotations

import re
from pathlib import Path

from tests.support.paths import SKILLS_ROOT

PAPER_AUDIT = SKILLS_ROOT / "paper-audit"
REFERENCES = PAPER_AUDIT / "references"
AGENTS = PAPER_AUDIT / "agents"

ARC_CODES = {"P-ARC-LEAD", "P-ARC-CLOSE", "P-ARC-LINK", "P-ARC-FLAT"}
ARC_OBSERVATION_SET = (
    "observe the same four paragraph-arc signals: `P-ARC-LEAD` (topic lead / opening), "
    "`P-ARC-CLOSE` (wrap-up / closing), `P-ARC-LINK` (adjacent-paragraph interface), "
    "and `P-ARC-FLAT` (body expansion)"
)

FOUR_DIMENSION_CLARITY = """Primary checks: FORMAT, GRAMMAR, SENTENCES, CONSISTENCY, REFERENCES, VISUAL, FIGURES, DEAI

| Score Range | Level        | Behavioral Indicators                                                                                          |
| ----------- | ------------ | -------------------------------------------------------------------------------------------------------------- |
| 5.5 - 6.0   | Exceptional  | Crystal clear writing; perfect formatting; all figures/tables well-designed and referenced; no grammar issues  |
| 4.5 - 5.4   | Strong       | Clear writing with minor formatting issues; figures readable; occasional grammar or style issues               |
| 3.5 - 4.4   | Adequate     | Generally understandable but some sections unclear; several formatting inconsistencies; grammar errors present |
| 2.5 - 3.4   | Weak         | Frequently unclear; significant formatting problems; many grammar errors; figures poorly designed              |
| 1.0 - 2.4   | Insufficient | Very difficult to follow; pervasive formatting issues; grammar errors impede comprehension                     |"""

NINE_DIMENSION_PRESENTATION = """| Score Range | Level     | Behavioral Indicators                                                                       |
| ----------- | --------- | ------------------------------------------------------------------------------------------- |
| 9.0 - 10.0  | Excellent | Professional layout; all figures/tables publication-ready; consistent formatting throughout |
| 7.0 - 8.9   | Good      | Good layout; figures clear; minor formatting inconsistencies                                |
| 5.0 - 6.9   | Fair      | Acceptable layout; some figures unclear or poorly labeled; formatting issues present        |
| 3.0 - 4.9   | Poor      | Significant layout problems; figures hard to read; inconsistent formatting throughout       |
| 1.0 - 2.9   | Failing   | Unprofessional presentation; figures missing or illegible; major formatting problems        |"""

CLARITY_ARC_ROWS = (
    "nearly every body paragraph has an identifiable topic lead and closing direction, "
    "with adjacent-paragraph relations and body expansion recoverable from the prose",
    "most body paragraphs have identifiable leads and closings, with only isolated "
    "adjacent-paragraph interfaces or body expansions requiring rereading",
    "several paragraphs have weak leads, closings, interfaces, or body expansion, so "
    "their role must be inferred from surrounding text",
    "many paragraphs lack an identifiable lead or closing direction, and adjacent "
    "interfaces or body expansion repeatedly require rereading",
    "paragraph roles are usually not recoverable from leads or closings, while interfaces "
    "are obscure and body content is predominantly single-sentence or list-like",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _between(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0].strip()


def _arc_codes(path: Path) -> set[str]:
    return set(re.findall(r"\bP-ARC-[A-Z]+(?:-[A-Z]+)*\b", _read(path)))


def test_nine_dimension_clarity_has_five_reviewed_paragraph_observations() -> None:
    rubric = _read(REFERENCES / "quality_rubrics.md")
    clarity = _normalize_whitespace(
        _between(
            rubric,
            "### Clarity (Weight: 13%, Source: Script)",
            "### Presentation (Weight: 8%, Source: Script)",
        )
    )

    for observation in CLARITY_ARC_ROWS:
        assert observation in clarity


def test_non_target_rubric_tables_keep_exact_snapshots() -> None:
    rubric = _read(REFERENCES / "quality_rubrics.md")
    four_dimensional = _between(
        rubric,
        "### Clarity (Weight: 30%)",
        "### Significance (Weight: 20%)",
    )
    presentation = _between(
        rubric,
        "### Presentation (Weight: 8%, Source: Script)",
        "### Novelty (Weight: 13%, Source: LLM)",
    )

    assert four_dimensional == FOUR_DIMENSION_CLARITY
    assert presentation == NINE_DIMENSION_PRESENTATION


def test_scholar_eval_weights_keep_the_pre_arc_contract() -> None:
    from scholar_eval import SCHOLAR_EVAL_DIMENSIONS

    assert {
        dimension: config["weight"] for dimension, config in SCHOLAR_EVAL_DIMENSIONS.items()
    } == {
        "soundness": 0.18,
        "clarity": 0.13,
        "presentation": 0.08,
        "novelty": 0.13,
        "significance": 0.13,
        "reproducibility": 0.08,
        "ethics": 0.05,
        "literature_grounding": 0.12,
        "overall": 0.10,
    }


def test_lane_template_and_reviewer_agents_share_observation_wording() -> None:
    paths = (
        REFERENCES / "REVIEW_LANE_GUIDE.md",
        REFERENCES / "SUBAGENT_TEMPLATES.md",
        AGENTS / "critical_reviewer_agent.md",
        AGENTS / "section_reviewer_agent.md",
    )

    for path in paths:
        assert ARC_OBSERVATION_SET.lower() in _normalize_whitespace(_read(path)).lower(), path.name


def test_intro_related_template_keeps_the_transition_word_boundary() -> None:
    template = _read(REFERENCES / "SUBAGENT_TEMPLATES.md")
    intro_block = _between(
        template,
        "### Lane: section_intro_related - Framing & paragraph-arc recoverability",
        "### Lane: section_methods - Methodological interface & argumentation completeness",
    )

    assert "**DO**:" in intro_block
    assert "**DON'T**:" in intro_block
    assert "do not treat missing transition words alone as a logical break" in intro_block
    assert "specific paragraph" in intro_block

    lane_guide = _read(REFERENCES / "REVIEW_LANE_GUIDE.md")
    intro_lane = _normalize_whitespace(
        _between(lane_guide, "- `section_intro_related`", "- `section_methods`")
    ).lower()
    assert "missing transition words alone are not a logical break" in intro_lane

    for path in (AGENTS / "critical_reviewer_agent.md", AGENTS / "section_reviewer_agent.md"):
        text = _normalize_whitespace(_read(path)).lower()
        assert "missing transition words alone are not a logical break" in text, path.name


def test_pre_submission_readiness_remains_mechanical_and_narrow() -> None:
    lane_guide = _read(REFERENCES / "REVIEW_LANE_GUIDE.md")
    template = _read(REFERENCES / "SUBAGENT_TEMPLATES.md")
    readiness = template.split("### Lane: pre_submission_readiness", 1)[1]

    assert "must not absorb" in lane_guide
    assert "do not absorb methodology, theory, literature, or claim-validity" in readiness
    assert not ARC_CODES.intersection(re.findall(r"P-ARC-[A-Z]+", readiness))


def test_c2_c3_and_audit_psychology_share_exactly_four_arc_codes() -> None:
    paths = (
        SKILLS_ROOT / "latex-thesis-zh" / "references" / "writing" / "paragraph-arc-zh.md",
        SKILLS_ROOT / "latex-paper-en" / "references" / "writing" / "paragraph-arc.md",
        REFERENCES / "REVIEWER_PSYCHOLOGY.md",
    )

    for path in paths:
        assert _arc_codes(path) == ARC_CODES, path.name


def test_reviewer_psychology_keeps_the_evidence_boundary() -> None:
    psychology = _read(REFERENCES / "REVIEWER_PSYCHOLOGY.md")
    section = _normalize_whitespace(
        _between(
            psychology,
            "## Paragraph-arc rereading heuristic (audit-only)",
            "## Where reviewers stop to doubt",
        )
    )

    assert "not as an established universal model of reviewer behavior" in section
    assert "one Chinese thesis chapter" in section
    assert "controlled English fixture" in section
    assert "**UNVERIFIED**" in section


def test_paragraph_arc_does_not_enter_forbidden_scoring_code_paths() -> None:
    for name in ("audit.py", "scholar_eval.py", "scoring_model.py"):
        source = _read(PAPER_AUDIT / "scripts" / name)
        assert "P-ARC-" not in source, name
        assert "--paragraph-arc" not in source, name
