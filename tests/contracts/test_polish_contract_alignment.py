"""Cross-skill alignment for the two-layer polish (rewrite) contract.

Scope note: these assertions cover *documentation* only — SKILL.md, the routing
docs, and the polish module docs. Assertions about what the polish scripts
actually emit belong to the tasks that change those scripts; asserting script
output here would turn this file red before those changes land.
"""

from __future__ import annotations

import re
from pathlib import Path

from tests.support.paths import SKILLS_ROOT

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

SCRIPT_SETTABLE_FLAGS = {
    "none",
    "not-assessed",
    "lexical-substitution",
    "whitespace-normalized",
}

GOAL_VALUES = ("grammar", "clarity", "concision", "coherence")
STRENGTH_VALUES = ("minimal", "moderate", "restructure")

NEGATIONS = ("never", "only", "unrelated", "绝不", "只能", "不得", "无关")

SKILL_MD = {
    "latex-paper-en": SKILLS_ROOT / "latex-paper-en" / "SKILL.md",
    "latex-thesis-zh": SKILLS_ROOT / "latex-thesis-zh" / "SKILL.md",
    "typst-paper": SKILLS_ROOT / "typst-paper" / "SKILL.md",
}

ROUTING_DOC = {
    "latex-paper-en": (
        SKILLS_ROOT / "latex-paper-en" / "references" / "modules" / "routing-rules.md"
    ),
    "latex-thesis-zh": (
        SKILLS_ROOT / "latex-thesis-zh" / "references" / "modules" / "routing-rules.md"
    ),
    "typst-paper": SKILLS_ROOT / "typst-paper" / "references" / "skill-routing-notes.md",
}

# ZH gains its own polish module doc when the ZH expression module lands; the
# path is listed now so it is covered automatically instead of being forgotten.
POLISH_MODULE_DOCS = {
    "latex-paper-en": [
        SKILLS_ROOT / "latex-paper-en" / "references" / "modules" / "expression.md",
        SKILLS_ROOT / "latex-paper-en" / "references" / "modules" / "grammar.md",
        SKILLS_ROOT / "latex-paper-en" / "references" / "modules" / "sentences.md",
    ],
    "latex-thesis-zh": [
        SKILLS_ROOT / "latex-thesis-zh" / "references" / "modules" / "expression.md",
    ],
    "typst-paper": [
        SKILLS_ROOT / "typst-paper" / "references" / "modules" / "EXPRESSION.md",
        SKILLS_ROOT / "typst-paper" / "references" / "modules" / "GRAMMAR.md",
        SKILLS_ROOT / "typst-paper" / "references" / "modules" / "SENTENCES.md",
    ],
}

OVER_CLAIM_GUARD = {
    "latex-paper-en": "../evidence/over-claim-guard.md",
    "latex-thesis-zh": "../writing/over-claim-guard.md",
    "typst-paper": "../OVER_CLAIM_GUARD.md",
}

BACKTICKED = re.compile(r"`([^`]+)`")
ENUM_IN_ANGLES = re.compile(r"<([^<>]+)>")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _existing_polish_docs() -> list[tuple[str, Path]]:
    return [
        (skill, path)
        for skill, paths in POLISH_MODULE_DOCS.items()
        for path in paths
        if path.exists()
    ]


def _field_line(text: str, field: str) -> str:
    """Return the contract-block line that defines ``field``."""
    for line in text.splitlines():
        stripped = line.lstrip("%/ \t")
        if stripped.startswith(field):
            return stripped
    raise AssertionError(f"no contract line starting with {field!r}")


def _enum_values(line: str) -> set[str]:
    match = ENUM_IN_ANGLES.search(line)
    assert match, f"contract line is not an angle-bracket enum: {line!r}"
    return {token.strip() for token in match.group(1).split("|")}


def _lines_with(text: str, *needles: str) -> list[str]:
    return [line for line in text.splitlines() if all(needle in line for needle in needles)]


def _section(text: str, heading: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == heading:
            rest = lines[index + 1 :]
            for offset, candidate in enumerate(rest):
                if candidate.startswith("## "):
                    return "\n".join(rest[:offset])
            return "\n".join(rest)
    raise AssertionError(f"section {heading!r} not found")


def test_every_skill_md_declares_the_four_contract_fields() -> None:
    for skill, path in SKILL_MD.items():
        text = _read(path)
        for field in CONTRACT_FIELDS:
            assert _field_line(text, field), f"{skill}: missing contract field {field}"


def test_risk_flags_closed_set_is_identical_across_skills() -> None:
    seen: dict[str, set[str]] = {}
    for skill, path in SKILL_MD.items():
        seen[skill] = _enum_values(_field_line(_read(path), "Risk-Flags:"))
    for skill, values in seen.items():
        assert values == RISK_FLAGS, f"{skill}: Risk-Flags set drifted: {sorted(values)}"
    assert len({frozenset(values) for values in seen.values()}) == 1


def test_meaning_check_enum_is_identical_across_skills() -> None:
    for skill, path in SKILL_MD.items():
        values = _enum_values(_field_line(_read(path), "Meaning-Check:"))
        assert values == {"PRESERVED", "NEEDS-LLM"}, f"{skill}: Meaning-Check enum drifted"


def test_script_layer_may_never_claim_preserved() -> None:
    for docs in (SKILL_MD, ROUTING_DOC):
        for skill, path in docs.items():
            text = _read(path)
            candidates = [
                line
                for line in _lines_with(text, "[Script]", "PRESERVED")
                if any(negation in line for negation in NEGATIONS)
            ]
            assert candidates, f"{skill} ({path.name}): no rule forbidding [Script] PRESERVED"


def test_routing_docs_restrict_script_layer_to_determinable_flags() -> None:
    for skill, path in ROUTING_DOC.items():
        script_lines = _lines_with(_read(path), "[Script]")
        assert script_lines, f"{skill}: routing doc never mentions the [Script] layer"
        allowed = set()
        for line in script_lines:
            allowed |= {token for token in BACKTICKED.findall(line) if token in RISK_FLAGS}
        assert allowed == SCRIPT_SETTABLE_FLAGS, (
            f"{skill}: [Script]-settable flags drifted: {sorted(allowed)}"
        )


def test_routing_docs_list_an_explicit_exclusion_set() -> None:
    for skill, path in ROUTING_DOC.items():
        # Anchor on the bolded list marker, not on the bare word: "排除" also
        # appears in per-checker exclusion notes, which would drag unrelated
        # backticked names into the set.
        excluded_lines = [
            line
            for line in _read(path).splitlines()
            if ("**Excluded" in line or "**排除" in line) and "`" in line
        ]
        assert excluded_lines, f"{skill}: no explicit exclusion list in the routing doc"
        modules = set()
        for line in excluded_lines:
            modules |= set(BACKTICKED.findall(line))
        assert len(modules) >= 8, f"{skill}: exclusion list is too thin: {sorted(modules)}"
        assert "expression" not in modules, f"{skill}: expression must not be excluded"


def test_skill_md_declares_both_edit_axes_with_smallest_defaults() -> None:
    for skill, path in SKILL_MD.items():
        text = _read(path)
        goal_lines = _lines_with(text, "--goal")
        strength_lines = _lines_with(text, "--strength")
        assert goal_lines, f"{skill}: --goal is not documented"
        assert strength_lines, f"{skill}: --strength is not documented"
        goal_blob = "\n".join(goal_lines)
        strength_blob = "\n".join(strength_lines)
        for value in GOAL_VALUES:
            assert value in goal_blob, f"{skill}: --goal is missing {value}"
        for value in STRENGTH_VALUES:
            assert value in strength_blob, f"{skill}: --strength is missing {value}"
        assert "`grammar`" in goal_blob, f"{skill}: --goal default is not stated"
        assert "`minimal`" in strength_blob, f"{skill}: --strength default is not stated"


def test_tier_is_never_conflated_with_the_edit_axes() -> None:
    for docs in (SKILL_MD, ROUTING_DOC):
        for skill, path in docs.items():
            text = _read(path)
            for line in _lines_with(text, "--tier"):
                assert "--strength" not in line, f"{skill}: --tier conflated with --strength"
                assert "--goal" not in line, f"{skill}: --tier conflated with --goal"
            disclaimers = [
                line
                for line in _lines_with(text, "--tier", "deai")
                if any(negation in line for negation in NEGATIONS)
            ]
            assert disclaimers, f"{skill} ({path.name}): --tier ownership is not disclaimed"


def test_polish_module_docs_carry_the_contract_and_guard_pointer() -> None:
    docs = _existing_polish_docs()
    assert len(docs) >= 6, "expected at least the EN and Typst polish module docs"
    for skill, path in docs:
        text = _read(path)
        for field in CONTRACT_FIELDS:
            assert field in text, f"{path.name}: missing contract field {field}"
        assert "NEEDS-LLM" in text, f"{path.name}: does not pin the [Script] meaning check"
        assert OVER_CLAIM_GUARD[skill] in text, (
            f"{path.name}: missing pointer to {OVER_CLAIM_GUARD[skill]}"
        )


def test_over_claim_guard_stays_out_of_the_top_level_reference_map() -> None:
    for skill, path in SKILL_MD.items():
        reference_map = _section(_read(path), "## Reference Map").lower()
        assert "over-claim" not in reference_map, f"{skill}: guard leaked into the Reference Map"
        assert "over_claim" not in reference_map, f"{skill}: guard leaked into the Reference Map"
