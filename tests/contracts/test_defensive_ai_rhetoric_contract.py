"""Cross-skill contract for defensive speculative explanations."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.support.paths import REPO_ROOT, SKILLS_ROOT

RUNTIME_CONTRACTS: tuple[tuple[Path, tuple[str, ...]], ...] = (
    (
        SKILLS_ROOT / "latex-paper-en" / "references" / "deai" / "guide.md",
        (
            "Defensive speculative explanation",
            "terminal caveat",
            "mechanism is undetermined",
            "`hedge_application`",
            "`[LLM]`",
        ),
    ),
    (
        SKILLS_ROOT / "latex-paper-en" / "references" / "modules" / "deai.md",
        ("defensive speculative explanations", "evidence anchor", "`hedge_application`"),
    ),
    (
        SKILLS_ROOT / "latex-paper-en" / "references" / "modules" / "experiment.md",
        ("LLM evidence boundary", "per-mechanism support", "undetermined"),
    ),
    (
        SKILLS_ROOT / "latex-thesis-zh" / "references" / "deai" / "guide.md",
        ("防御性推测解释", "区分性检验", "机制尚未确定", "`hedge_application`", "`[LLM]`"),
    ),
    (
        SKILLS_ROOT / "latex-thesis-zh" / "references" / "modules" / "deai.md",
        ("defensive speculative explanations", "evidence anchor", "`hedge_application`"),
    ),
    (
        SKILLS_ROOT / "latex-thesis-zh" / "references" / "modules" / "experiment.md",
        ("LLM 证据边界", "证据锚点", "机制尚未确定"),
    ),
    (
        SKILLS_ROOT / "typst-paper" / "references" / "DEAI_GUIDE.md",
        ("Defensive speculative explanation", "terminal caveat", "`hedge_application`"),
    ),
    (
        SKILLS_ROOT / "typst-paper" / "references" / "modules" / "DEAI.md",
        ("防御性推测解释", "区分性检验", "`hedge_application`"),
    ),
    (
        SKILLS_ROOT / "typst-paper" / "references" / "modules" / "EXPERIMENT.md",
        ("LLM evidence boundary", "per-mechanism support", "undetermined"),
    ),
    (
        SKILLS_ROOT / "paper-audit" / "references" / "CLAIM_EVIDENCE_CONTRACT.md",
        ("Defensive Speculative Explanations", "`unsupported extrapolation`", "`undetermined`"),
    ),
    (
        SKILLS_ROOT / "paper-audit" / "references" / "OVER_CLAIM_GUARD.md",
        ("Hedging Is Not Evidence", "`is consistent with`", "`CLAIM_EVIDENCE_CONTRACT.md`"),
    ),
    (
        SKILLS_ROOT / "paper-audit" / "references" / "SUBAGENT_TEMPLATES.md",
        ("defensive speculative explanations", "max 8 issues", "not as a separate quota"),
    ),
    (
        SKILLS_ROOT / "paper-audit" / "agents" / "claims_evidence_reviewer_agent.md",
        ("defensive speculative explanations", "max-8 lane budget", "style-only findings"),
    ),
)


@pytest.mark.parametrize(
    ("path", "required_tokens"),
    RUNTIME_CONTRACTS,
    ids=[path.parent.parent.name + "/" + path.name for path, _ in RUNTIME_CONTRACTS],
)
def test_runtime_surfaces_define_the_same_judgment_contract(
    path: Path, required_tokens: tuple[str, ...]
) -> None:
    text = path.read_text(encoding="utf-8")
    for token in required_tokens:
        assert token in text, f"{path}: missing defensive-rhetoric contract token {token!r}"


@pytest.mark.parametrize(
    ("skill", "fixture_name", "prompt_anchor", "case_labels", "assertion_tokens"),
    (
        (
            "latex-paper-en",
            "defensive_speculative_explanation.tex",
            "five labeled Discussion cases",
            ("Case A", "Case B", "Case C", "Case D", "Case E"),
            ("defensive speculative explanation", "evidence anchor", "undetermined", "controlled"),
        ),
        (
            "latex-thesis-zh",
            "defensive_speculative_explanation.tex",
            "五个带标签的讨论段落",
            ("样例 A", "样例 B", "样例 C", "样例 D", "样例 E"),
            ("防御性推测解释", "证据锚点", "机制尚未确定", "受控"),
        ),
        (
            "typst-paper",
            "defensive_speculative_explanation.typ",
            "five labeled Discussion cases",
            ("Case A", "Case B", "Case C", "Case D", "Case E"),
            ("defensive speculative explanation", "evidence anchor", "undetermined", "controlled"),
        ),
        (
            "paper-audit",
            "defensive_speculative_explanation.tex",
            "five labeled Discussion cases",
            ("Case A", "Case B", "Case C", "Case D", "Case E"),
            ("unsupported extrapolation", "claim_accuracy", "evidence anchor", "max.?8"),
        ),
    ),
)
def test_each_surface_has_a_local_composite_fixture_and_eval(
    skill: str,
    fixture_name: str,
    prompt_anchor: str,
    case_labels: tuple[str, ...],
    assertion_tokens: tuple[str, ...],
) -> None:
    skill_root = SKILLS_ROOT / skill
    eval_path = skill_root / "evals" / "evals.json"
    payload = json.loads(eval_path.read_text(encoding="utf-8"))
    fixture_rel = f"evals/fixtures/{fixture_name}"
    matches = [item for item in payload["evals"] if fixture_rel in item.get("files", [])]

    assert len(matches) == 1, f"{skill}: expected one semantic eval for {fixture_rel}"
    semantic_eval = matches[0]
    assert semantic_eval is payload["evals"][-1], f"{skill}: new eval must be append-only"
    assert prompt_anchor in semantic_eval["prompt"]
    assert len({item["id"] for item in payload["evals"]}) == len(payload["evals"])

    fixture_path = skill_root / fixture_rel
    assert fixture_path.is_file(), f"{skill}: missing fixture {fixture_rel}"
    fixture_text = fixture_path.read_text(encoding="utf-8")
    for label in case_labels:
        assert label in fixture_text, f"{skill}: fixture missing local boundary {label}"

    eval_contract = json.dumps(semantic_eval, ensure_ascii=False)
    for token in assertion_tokens:
        assert token in eval_contract, f"{skill}: eval does not lock {token!r}"


def test_paper_audit_lane_reuses_existing_budget_and_collapses_repetition() -> None:
    template = (SKILLS_ROOT / "paper-audit" / "references" / "SUBAGENT_TEMPLATES.md").read_text(
        encoding="utf-8"
    )
    agent = (
        SKILLS_ROOT / "paper-audit" / "agents" / "claims_evidence_reviewer_agent.md"
    ).read_text(encoding="utf-8")

    for text in (template, agent):
        assert "unsupported" in text
        assert "style-only" in text
    assert "multiple example" in template and "locations" in template
    assert "multiple locations" in agent
    assert "not as a separate quota" in template
    assert "max-8 lane budget" in agent


def test_trellis_contract_is_discoverable_and_executable() -> None:
    spec_dir = REPO_ROOT / ".trellis" / "spec" / "academic-writing-skills"
    spec = (spec_dir / "defensive-ai-rhetoric-contract.md").read_text(encoding="utf-8")
    index = (spec_dir / "index.md").read_text(encoding="utf-8")

    assert "[defensive-ai-rhetoric-contract.md]" in index
    assert "## Contract:" in spec
    assert "## Convention:" in spec
    assert "**Tests Required**" in spec
    assert "**Validation**" in spec
    assert "C 档 `llm-only`" in spec
    assert "provider-backed" in spec and "`missing evidence`" in spec
