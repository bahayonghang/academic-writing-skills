"""Cross-skill contract for evidence-aware de-AI pattern clusters."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from tests.support.paths import REPO_ROOT, SKILLS_ROOT

CLUSTERS = (
    "H-ING",
    "H-PROMO",
    "H-ATTR",
    "H-PRED",
    "H-TERM",
    "H-SCOPE",
    "H-OUTLOOK",
)

CONTRACT_FIELDS = ("Changed:", "Protected:", "Meaning-Check:", "Risk-Flags:")

RISK_FLAGS = {
    "none",
    "not-assessed",
    "lexical-substitution",
    "whitespace-normalized",
    "overstatement",
    "ambiguity",
    "terminology-drift",
    "invented-claim",
}

DETAILED_REFERENCES: tuple[tuple[str, Path, tuple[str, ...]], ...] = (
    (
        "latex-paper-en",
        SKILLS_ROOT / "latex-paper-en" / "references" / "deai" / "pattern-clusters.md",
        ("explicit prose request", "author-confirmed sample", "cannot override"),
    ),
    (
        "latex-thesis-zh",
        SKILLS_ROOT / "latex-thesis-zh" / "references" / "deai" / "pattern-clusters.md",
        ("只有用户明确要求", "作者确认的样本", "不能覆盖"),
    ),
    (
        "typst-paper",
        SKILLS_ROOT / "typst-paper" / "references" / "DEAI_PATTERN_CLUSTERS.md",
        ("explicit request", "author-confirmed sample", "cannot override"),
    ),
)

ENTRY_POINTS: tuple[tuple[Path, tuple[str, ...]], ...] = (
    (
        SKILLS_ROOT / "latex-paper-en" / "references" / "deai" / "guide.md",
        ("[pattern-clusters.md](pattern-clusters.md)", "claim-local", "AI authorship"),
    ),
    (
        SKILLS_ROOT / "latex-paper-en" / "references" / "modules" / "deai.md",
        ("[pattern-clusters.md](../deai/pattern-clusters.md)", "fidelity audit", "AI-authorship"),
    ),
    (
        SKILLS_ROOT / "latex-thesis-zh" / "references" / "deai" / "guide.md",
        ("[pattern-clusters.md](pattern-clusters.md)", "claim-local", "AI 作者身份"),
    ),
    (
        SKILLS_ROOT / "latex-thesis-zh" / "references" / "modules" / "deai.md",
        (
            "[`pattern-clusters.md`](../deai/pattern-clusters.md)",
            "fidelity audit",
            "AI-authorship",
        ),
    ),
    (
        SKILLS_ROOT / "typst-paper" / "references" / "DEAI_GUIDE.md",
        ("[DEAI_PATTERN_CLUSTERS.md](DEAI_PATTERN_CLUSTERS.md)", "claim-local", "AI authorship"),
    ),
    (
        SKILLS_ROOT / "typst-paper" / "references" / "modules" / "DEAI.md",
        (
            "[DEAI_PATTERN_CLUSTERS.md](../DEAI_PATTERN_CLUSTERS.md)",
            "fidelity audit",
            "AI 作者身份",
        ),
    ),
)

AUTOMATION_SURFACES = (
    SKILLS_ROOT / "latex-paper-en" / "scripts" / "deai_check.py",
    SKILLS_ROOT / "latex-thesis-zh" / "scripts" / "deai_check.py",
    SKILLS_ROOT / "typst-paper" / "scripts" / "deai_check.py",
    SKILLS_ROOT / "latex-paper-en" / "references" / "deai" / "tone-thresholds.yaml",
    SKILLS_ROOT / "latex-thesis-zh" / "references" / "deai" / "tone-thresholds.yaml",
    SKILLS_ROOT / "typst-paper" / "references" / "AI_TONE_THRESHOLDS.yaml",
    SKILLS_ROOT / "latex-paper-en" / "references" / "deai" / "tone-terms-en.md",
    SKILLS_ROOT / "latex-thesis-zh" / "references" / "deai" / "tone-terms-zh.md",
    SKILLS_ROOT / "typst-paper" / "references" / "AI_TONE_TERMS.md",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _literal_assignment(path: Path, name: str) -> object:
    tree = ast.parse(_read(path), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError(f"{path}: missing literal assignment {name}")


def test_nine_runtime_sources_define_progressive_loading_without_authorship_claims() -> None:
    assert len(DETAILED_REFERENCES) + len(ENTRY_POINTS) == 9
    for path, required_tokens in ENTRY_POINTS:
        text = _read(path)
        for token in required_tokens:
            assert token in text, f"{path}: missing progressive-loading token {token!r}"


@pytest.mark.parametrize(
    ("skill", "path", "surface_tokens"),
    DETAILED_REFERENCES,
    ids=[skill for skill, _, _ in DETAILED_REFERENCES],
)
def test_detailed_references_lock_clusters_fidelity_and_evidence_status(
    skill: str, path: Path, surface_tokens: tuple[str, ...]
) -> None:
    text = _read(path)
    for token in (
        *CLUSTERS,
        "`source_span`",
        "`rhetorical_move`",
        "`evidence_anchor`",
        "`scope_and_certainty`",
        "`protected_units`",
        "C-grade" if skill != "latex-thesis-zh" else "C 档",
        "`llm-only`",
        "primary",
        "secondary",
        "`paper-audit`",
        "missing evidence / UNVERIFIED",
        *CONTRACT_FIELDS,
        *surface_tokens,
    ):
        assert token in text, f"{path}: missing pattern-cluster contract token {token!r}"

    risk_line = next(line for line in text.splitlines() if line.startswith("Risk-Flags:"))
    assert {
        value.strip() for value in risk_line.removeprefix("Risk-Flags:").split("|")
    } == RISK_FLAGS


@pytest.mark.parametrize(
    ("skill", "eval_id", "fixture_name", "case_prefix", "protected_tokens"),
    (
        (
            "latex-paper-en",
            23,
            "anti_ai_pattern_clusters.tex",
            "Case",
            (r"\ref{tab:main}", r"\cite{smith2024}", "$z$", "Dataset-B"),
        ),
        (
            "latex-thesis-zh",
            31,
            "anti_ai_pattern_clusters.tex",
            "样例",
            (r"\ref{tab:main}", r"\cite{smith2024}", "$z$", "数据集 B"),
        ),
        (
            "typst-paper",
            16,
            "anti_ai_pattern_clusters.typ",
            "Case",
            ("@tab:main", "@smith2024", "$z$", "<sec:pattern-clusters>"),
        ),
    ),
)
def test_each_surface_binds_a_local_eight_case_fixture_and_append_only_eval(
    skill: str,
    eval_id: int,
    fixture_name: str,
    case_prefix: str,
    protected_tokens: tuple[str, ...],
) -> None:
    skill_root = SKILLS_ROOT / skill
    fixture_rel = f"evals/fixtures/{fixture_name}"
    fixture_text = _read(skill_root / fixture_rel)
    for label in "ABCDEFGH":
        assert f"{case_prefix} {label}" in fixture_text
    for token in (*CLUSTERS, *protected_tokens):
        assert token in fixture_text, f"{skill}: fixture missing {token!r}"

    payload = json.loads(_read(skill_root / "evals" / "evals.json"))
    eval_ids = [item["id"] for item in payload["evals"]]
    assert eval_ids == sorted(eval_ids)
    assert len(eval_ids) == len(set(eval_ids))

    matches = [
        item
        for item in payload["evals"]
        if item.get("id") == eval_id and fixture_rel in item.get("files", [])
    ]
    assert len(matches) == 1, f"{skill}: expected one eval bound to {fixture_rel}"
    eval_contract = json.dumps(matches[0], ensure_ascii=False)
    for token in (*CLUSTERS, *CONTRACT_FIELDS, "fidelity audit"):
        assert token in eval_contract, f"{skill}: eval does not lock {token!r}"
    for label in "ABCDEFGH":
        assert f"{case_prefix} {label}" in eval_contract
    assert "AI authorship" in eval_contract or "AI 作者身份" in eval_contract
    assert "invent" in eval_contract or "虚构" in eval_contract or "补造" in eval_contract


def test_llm_only_clusters_do_not_expand_checker_or_tone_configuration() -> None:
    for path in AUTOMATION_SURFACES:
        text = _read(path)
        for cluster in CLUSTERS:
            assert cluster not in text, f"{path}: {cluster} leaked into an automation surface"

    for skill in ("latex-paper-en", "latex-thesis-zh", "typst-paper"):
        script = SKILLS_ROOT / skill / "scripts" / "deai_check.py"
        defaults = _literal_assignment(script, "DEFAULT_THRESHOLDS")
        dimensions = _literal_assignment(script, "DIMENSION_MAP")
        serialized = repr((defaults, dimensions))
        for cluster in CLUSTERS:
            assert cluster not in serialized


def test_trellis_contract_is_discoverable_and_executable() -> None:
    spec_dir = REPO_ROOT / ".trellis" / "spec" / "academic-writing-skills"
    spec = _read(spec_dir / "deai-pattern-cluster-contract.md")
    index = _read(spec_dir / "index.md")

    assert "[deai-pattern-cluster-contract.md]" in index
    for token in (
        "## Contract:",
        "## Convention:",
        "**Tests Required**",
        "C 档 `llm-only`",
        "H-OUTLOOK",
        "fidelity audit",
        "missing evidence / UNVERIFIED",
    ):
        assert token in spec
