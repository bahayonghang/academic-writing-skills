"""Regression guards for claim-evidence mapping contracts."""

from __future__ import annotations

from build_claim_map import build_claim_map

from tests.support.paths import SKILLS_ROOT


def _single_section(
    text: str, section_key: str = "abstract"
) -> tuple[str, list[dict], dict[str, str]]:
    return (
        text,
        [
            {
                "section_key": section_key,
                "title": section_key.title(),
                "start_line": 1,
                "end_line": len(text.splitlines()),
                "line_base": 1,
            }
        ],
        {section_key: text},
    )


def test_claim_map_keeps_legacy_fields_and_adds_candidates() -> None:
    content, section_index, section_texts = _single_section(
        "We demonstrate state-of-the-art performance across all domains."
    )

    claim_map = build_claim_map(content, section_index, section_texts=section_texts)

    assert claim_map["headline_claims"] == [
        "We demonstrate state-of-the-art performance across all domains."
    ]
    assert claim_map["section_claims"]["abstract"] == claim_map["headline_claims"]
    assert claim_map["claim_candidates"][0]["claim_strength"] == "unsupported"
    assert claim_map["claim_candidates"][0]["evidence_anchor"] == []
    assert "citation" in claim_map["claim_candidates"][0]["missing_evidence"][0]


def test_metric_and_table_anchor_promote_claim_strength_to_strong() -> None:
    content, section_index, section_texts = _single_section(
        r"We demonstrate a 12.4% speedup in Table~\ref{tab:main}.",
        section_key="results",
    )

    claim_map = build_claim_map(content, section_index, section_texts=section_texts)
    candidate = claim_map["claim_candidates"][0]
    anchor_types = {anchor["type"] for anchor in candidate["evidence_anchor"]}

    assert candidate["claim_strength"] == "strong"
    assert {"metric", "figure_or_table"} <= anchor_types
    assert any(anchor["text"] == "12.4%" for anchor in candidate["evidence_anchor"])
    assert candidate["missing_evidence"] == []


def test_citation_anchor_still_requires_claim_support_verification() -> None:
    content, section_index, section_texts = _single_section(
        r"This paper builds on prior work \cite{smith2020} and introduces a new taxonomy.",
        section_key="introduction",
    )

    claim_map = build_claim_map(content, section_index, section_texts=section_texts)
    candidate = claim_map["claim_candidates"][0]

    assert candidate["claim_strength"] == "supported"
    assert candidate["evidence_anchor"][0]["type"] == "citation"
    assert candidate["missing_evidence"] == [
        "verify that the cited source supports this manuscript sentence"
    ]


def test_claim_evidence_reference_files_are_installed_and_linked() -> None:
    paper_contract = SKILLS_ROOT / "paper-audit/references/CLAIM_EVIDENCE_CONTRACT.md"
    writing_contract = SKILLS_ROOT / "latex-paper-en/references/evidence/claim-evidence-contract.md"
    skill_md = (SKILLS_ROOT / "paper-audit/SKILL.md").read_text(encoding="utf-8")

    for path in (paper_contract, writing_contract):
        text = path.read_text(encoding="utf-8")
        assert "unsupported|observed|supported|strong" in text
        assert "A citation key proves only" in text

    assert "CLAIM_EVIDENCE_CONTRACT.md" in skill_md
    assert "claim_candidates" in skill_md


def test_data_availability_advisory_documents_non_blocking_default() -> None:
    advisory = SKILLS_ROOT / "paper-audit/references/DATA_AVAILABILITY_ADVISORY.md"
    text = advisory.read_text(encoding="utf-8")

    assert "not a data-hosting workflow" in text
    assert "Gate blocker only when venue policy requires it" in text
    assert "missing_evidence" in text


def test_latex_paper_references_use_claim_evidence_contract() -> None:
    literature = (SKILLS_ROOT / "latex-paper-en/references/modules/literature.md").read_text(
        encoding="utf-8"
    )
    experiment = (SKILLS_ROOT / "latex-paper-en/references/modules/experiment.md").read_text(
        encoding="utf-8"
    )

    assert "Claim-Evidence Map" in literature
    assert "citation key only proves" in literature
    assert "claim_strength" in experiment
    assert "Do not promote a metric-only observation" in experiment
