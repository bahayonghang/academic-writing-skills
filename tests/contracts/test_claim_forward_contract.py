"""Cross-skill contract for the claim-forward (主张前置 / 自我削弱) module.

Locks the CF-* code set, the [Script] output shape, the routing placement in
SKILL.md / routing-rules.md, and the files that this feature must not touch
(deai copies, TIER1 hash groups, ZH conclusion checker, paper-audit engine).
Spec: .trellis/spec/academic-writing-skills/claim-forward-contract.md
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support.paths import REPO_ROOT, SKILLS_ROOT

CF_CODES: frozenset[str] = frozenset(
    {"CF-DISCLAIM", "CF-SELFWEAK", "CF-CAVEAT-POS", "CF-HEDGE-STACK", "CF-CLOSE-NEG"}
)
AUDIT_CF_CODES: frozenset[str] = CF_CODES
LLM_ONLY_CODES: frozenset[str] = frozenset({"CF-LOSS-FRAME"})
CF_CODE_RE = re.compile(r"\bCF-[A-Z][A-Z-]*[A-Z]\b")

EN = SKILLS_ROOT / "latex-paper-en"
ZH = SKILLS_ROOT / "latex-thesis-zh"
AUDIT = SKILLS_ROOT / "paper-audit"

# (skill root, fixture) pairs that ship the script. ZH is appended by C2.
SCRIPT_SKILLS: list[tuple[Path, Path]] = [
    (EN, EN / "evals" / "fixtures" / "claim_forward_cases.tex"),
]
if (ZH / "scripts" / "check_claim_forward.py").exists():
    SCRIPT_SKILLS.append((ZH, ZH / "evals" / "fixtures" / "claim_forward_cases_zh.tex"))

# Files the feature must never touch: no CF-* code and no claim-forward symbol
# may appear in them (deai copies carry no hedge regex by contract; TIER1 hash
# groups and the ZH conclusion checker feed paper-audit; audit engine is frozen).
NO_LEAK_FILES: tuple[str, ...] = (
    "academic-writing-skills/latex-paper-en/scripts/deai_check.py",
    "academic-writing-skills/latex-thesis-zh/scripts/deai_check.py",
    "academic-writing-skills/typst-paper/scripts/deai_check.py",
    "academic-writing-skills/latex-paper-en/scripts/improve_expression.py",
    "academic-writing-skills/latex-paper-en/scripts/analyze_abstract.py",
    "academic-writing-skills/latex-paper-en/scripts/analyze_grammar.py",
    "academic-writing-skills/latex-paper-en/scripts/analyze_sentences.py",
    "academic-writing-skills/latex-thesis-zh/scripts/analyze_conclusion.py",
    "academic-writing-skills/latex-thesis-zh/scripts/check_style_zh.py",
    "academic-writing-skills/paper-audit/scripts/audit.py",
    "academic-writing-skills/paper-audit/scripts/scholar_eval.py",
    "academic-writing-skills/paper-audit/scripts/zh_check_adapters.py",
    "academic-writing-skills/paper-audit/references/ISSUE_SCHEMA.md",
    "academic-writing-skills/paper-audit/references/quality_rubrics.md",
)
LEAK_RE = re.compile(r"CF-[A-Z]|claim[_-]forward|self[_-]weaken|hedge_stack", re.IGNORECASE)


def _run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


# ---------------------------------------------------------------------------
# Script surface (EN now, ZH once C2 lands)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("skill_root, fixture", SCRIPT_SKILLS, ids=lambda p: p.name)
def test_script_exists_and_help_advertises_flags(skill_root: Path, fixture: Path) -> None:
    script = skill_root / "scripts" / "check_claim_forward.py"
    assert script.is_file()
    result = _run(script, "--help")
    assert result.returncode == 0, result.stderr
    assert "--section" in result.stdout
    assert "--json" in result.stdout
    for forbidden in ("--strength", "--goal", "--tier"):
        assert forbidden not in result.stdout


@pytest.mark.parametrize("skill_root, fixture", SCRIPT_SKILLS, ids=lambda p: p.name)
def test_script_code_set_is_exactly_the_contract(skill_root: Path, fixture: Path) -> None:
    source = (skill_root / "scripts" / "check_claim_forward.py").read_text(encoding="utf-8")
    assert set(CF_CODE_RE.findall(source)) == set(CF_CODES)


@pytest.mark.parametrize("skill_root, fixture", SCRIPT_SKILLS, ids=lambda p: p.name)
def test_script_output_shape_and_exit_zero(skill_root: Path, fixture: Path) -> None:
    script = skill_root / "scripts" / "check_claim_forward.py"
    assert fixture.is_file()
    result = _run(script, str(fixture))
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert lines[0].startswith("% CLAIM-FORWARD [Script]: section=all terms=")
    heads = [
        ln
        for ln in lines
        if re.match(
            r"% CLAIM-FORWARD \(.*\) \[Severity: (Info|Minor)\] \[Priority: P[23]\]: \[Script\] CF-",
            ln,
        )
    ]
    assert heads, result.stdout
    assert {m.group(0) for h in heads for m in [CF_CODE_RE.search(h)] if m} == set(CF_CODES)
    assert all(ln.startswith("% ") or ln == "" for ln in lines)
    assert "% Meaning-Check: NEEDS-LLM" in lines
    assert not any("Meaning-Check: PRESERVED" in ln for ln in lines)
    assert not any(ln.startswith("% Changed:") for ln in lines)
    assert lines[-1].startswith("% CLAIM-FORWARD: ") and "finding(s)" in lines[-1]

    missing = _run(script, str(fixture), "--section", "no-such-section")
    assert missing.returncode == 0
    assert "% ERROR [Severity: Critical] [Priority: P0]: Section not found" in missing.stdout


@pytest.mark.parametrize("skill_root, fixture", SCRIPT_SKILLS, ids=lambda p: p.name)
def test_router_and_routing_rules_place_module_in_llm_only_group(
    skill_root: Path, fixture: Path
) -> None:
    skill_md = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    assert re.search(r"^\| `claim-forward`\s*\|", skill_md, re.M), "router row missing"
    assert "check_claim_forward.py" in skill_md
    assert "references/modules/claim-forward.md" in skill_md
    rules = (skill_root / "references" / "modules" / "routing-rules.md").read_text(encoding="utf-8")
    llm_only_line = next(
        ln
        for ln in rules.splitlines()
        if "[LLM]" in ln and "layer only" in ln or ln.startswith("- **仅 `[LLM]` 层**")
    )
    assert "`claim-forward`" in llm_only_line
    contract_line = next(
        ln
        for ln in rules.splitlines()
        if ln.startswith("- **Contract applies") or ln.startswith("- **纳入契约")
    )
    assert "`claim-forward`" not in contract_line
    assert (skill_root / "references" / "modules" / "claim-forward.md").is_file()


def test_en_reference_docs_carry_attribution_and_rejections() -> None:
    guide = (EN / "references" / "writing" / "claim-forward.md").read_text(encoding="utf-8")
    for needle in (
        "github.com/Kiterlin/anti-defensive-writing",
        "github.com/Adkid-Zephyr/anti-defensive-writing-Skill",
        "MIT",
        "Deleting an unfavorable comparison",
        "CF-LOSS-FRAME",
    ):
        assert needle in guide, needle
    guard = (EN / "references" / "evidence" / "over-claim-guard.md").read_text(encoding="utf-8")
    assert "## Upward calibration (claim-forward)" in guard
    assert "Never delete a caveat" in guard
    assert (EN / "references" / "writing" / "claim-forward-terms.yaml").is_file()


def test_no_new_module_named_defensive() -> None:
    """The 08-05 'defensive speculative explanation' concept keeps that word; this feature does not."""
    for root in (EN, ZH, AUDIT):
        for path in root.rglob("*"):
            if path.is_file() and "claim" in path.name and "forward" in path.name:
                assert "defensive" not in path.name.lower()
        skill_md = (root / "SKILL.md").read_text(encoding="utf-8")
        assert not re.search(r"^\| `defensive[^`]*`", skill_md, re.M)


# ---------------------------------------------------------------------------
# paper-audit observation-code set (documents and agents only)
# ---------------------------------------------------------------------------


# sha256 of the paper-audit engine / schema files the feature must leave byte-identical
# (recorded when C3 landed; update only through a task that deliberately changes them).
AUDIT_FROZEN_SHA256: dict[str, str] = {
    "scripts/audit.py": "72ad368b8b9894e9249062c061dbff5b274ee921e5c66c4bf3c6f27a34e350f8",
    "scripts/scholar_eval.py": "b241f7da8e1757ac87e9a2f5d818705659de31ed58de77168dd9a1a425ae8c67",
    "scripts/zh_check_adapters.py": "8af2cdb59cc0e6024e7da898a994482d746ac1153b0cfba7b18137cbdcce3077",
    "references/quality_rubrics.md": "56f5ee3604ade91a97c97dd45ae733502f298f6a71d6684b6ce2f0d70138f910",
    "references/ISSUE_SCHEMA.md": "42c013cd8fd7113b747b8113c12fe56c83d6fd69b26b524c8083064b6ccf9b23",
}


def test_paper_audit_cf_codes_are_exactly_the_fixed_set() -> None:
    found: set[str] = set()
    for folder in ("references", "agents"):
        for path in (AUDIT / folder).rglob("*.md"):
            found.update(CF_CODE_RE.findall(path.read_text(encoding="utf-8")))
    assert found == AUDIT_CF_CODES, sorted(found ^ AUDIT_CF_CODES)
    # No CF-* code may leak into the scoring / schema layer.
    for name in ("scripts", "evals"):
        for path in (AUDIT / name).rglob("*.py"):
            assert not CF_CODE_RE.search(path.read_text(encoding="utf-8")), path


def test_paper_audit_documents_carry_under_claim_guidance() -> None:
    guard = (AUDIT / "references" / "OVER_CLAIM_GUARD.md").read_text(encoding="utf-8")
    assert "## Under-claim and upward calibration" in guard
    assert "Never recommend deleting a caveat" in guard
    templates = (AUDIT / "references" / "SUBAGENT_TEMPLATES.md").read_text(encoding="utf-8")
    assert "### Lane: section_discussion_conclusion" in templates
    assert (
        "CF-CLOSE-NEG"
        in templates.split("### Lane: section_discussion_conclusion", 1)[1].split(
            "### Lane: claims_vs_evidence", 1
        )[0]
    )
    psychology = (AUDIT / "references" / "REVIEWER_PSYCHOLOGY.md").read_text(encoding="utf-8")
    knife = psychology.split("## Authors handing the reviewer a knife", 1)[1].split("\n## ", 1)[0]
    assert "UNVERIFIED" in knife
    criteria = (AUDIT / "references" / "ZH_THESIS_REVIEW_CRITERIA.md").read_text(encoding="utf-8")
    rows = [ln for ln in criteria.splitlines() if re.match(r"^\| \d+ \|", ln)]
    assert len(rows) == 15
    fixture = AUDIT / "evals" / "fixtures" / "claim_forward_cases.tex"
    assert fixture.is_file()


@pytest.mark.parametrize("rel_path", sorted(AUDIT_FROZEN_SHA256), ids=lambda s: Path(s).name)
def test_paper_audit_engine_files_are_byte_identical(rel_path: str) -> None:
    import hashlib

    digest = hashlib.sha256((AUDIT / rel_path).read_bytes()).hexdigest()
    assert digest == AUDIT_FROZEN_SHA256[rel_path], rel_path


# ---------------------------------------------------------------------------
# Files the feature must not touch
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("rel_path", NO_LEAK_FILES, ids=lambda s: Path(s).name)
def test_no_claim_forward_leakage_into_frozen_files(rel_path: str) -> None:
    path = REPO_ROOT / rel_path
    assert path.is_file(), rel_path
    assert not LEAK_RE.search(path.read_text(encoding="utf-8")), (
        f"{rel_path} mentions claim-forward. The feature lives only in check_claim_forward.py, "
        "its references, and paper-audit documents/agents (see claim-forward-contract.md)."
    )
