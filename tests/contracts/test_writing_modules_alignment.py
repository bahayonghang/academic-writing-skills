"""Alignment lint for shared modules across the writing trio.

The three writing skills (``latex-paper-en``, ``latex-thesis-zh``,
``typst-paper``) each ship their own ``scripts/`` so they can be installed
in isolation under ``~/.claude/skills/{skill}/``. Stage 4 of the
optimization plan investigated whether the trio could be re-platformed
onto a shared ``core/`` layer; the PoC (see ``findings.md`` Stage 4 PoC
Results) showed that only seven modules are byte-identical or near-identical
between two or more of the three skills, while the rest carry intentional
language / format specialization. Rather than introduce a fragile
cross-directory import (the same trap stage 2 walked back), we keep the
copies vendored and use this test to fail loudly on accidental drift.

Tier definitions (see findings.md):

* **Tier 1** — byte-identical groups; this file pins their hashes.
* **Tier 2** — high (85-95%) similarity, intentionally not deduplicated:
  EN/Typst share helpers but carry per-format docstrings & CLI examples.
* **Tier 3** — Chinese specialization (60-77%); not aligned.
* **Tier 4** — architecturally distinct (compile.py, check_format.py,
  verify_bib.py, check_pseudocode.py); never aligned.

When a fix lands in one Tier-1 copy, mirror it to every other copy in the
same group. Canonical source = ``latex-paper-en`` for groups containing
``en``; otherwise pick the first listed key.
"""

from __future__ import annotations

import difflib
import hashlib
from pathlib import Path

import pytest

from tests.support.paths import SKILLS_ROOT

SKILL_DIRS: dict[str, Path] = {
    "en": SKILLS_ROOT / "latex-paper-en" / "scripts",
    "zh": SKILLS_ROOT / "latex-thesis-zh" / "scripts",
    "typst": SKILLS_ROOT / "typst-paper" / "scripts",
}


def _module_path(skill_key: str, module_name: str) -> Path:
    return SKILL_DIRS[skill_key] / module_name


def _file_hash(path: Path) -> str:
    """Hash a file after normalizing line endings and BOM.

    git stores LF in the index; Windows checkouts can introduce CRLF in the
    working tree depending on per-file ``core.autocrlf`` / ``.gitattributes``
    handling. Either is fine on disk — we want this lint to fire only on real
    content drift, so normalize CRLF→LF and strip a leading UTF-8 BOM before
    hashing.
    """
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return hashlib.sha256(raw).hexdigest()


# (module file name, skill keys whose copies must hash-match)
#
# Each group lists every skill that ships a copy of the module AND whose copy
# is expected to be byte-identical with the others in the same group. If a
# skill ships its own intentionally-specialized version, omit its key here
# (e.g. typst's check_tables.py is a Typst rewrite, so it stays out of the
# check_tables group).
TIER1_HASH_GROUPS: list[tuple[str, list[str]]] = [
    # 2026-06: ZH analyze_abstract.py / check_tables.py left these groups —
    # they now assemble multi-file thesis projects via the ZH-only
    # ``tex_loader`` module (Chinese degree theses are \include-skeletons;
    # EN/Typst papers stay single-file). See latex-thesis-zh audit F3.
    ("analyze_abstract.py", ["en", "typst"]),
    ("analyze_grammar.py", ["en", "typst"]),
    ("analyze_sentences.py", ["en", "typst"]),
    ("improve_expression.py", ["en", "typst"]),
    # 2026-06: EN generate_table.py implements `--style plain` (audit E10); the
    # ZH copy is intentionally left untouched (latex-thesis-zh is diff-frozen by
    # its own audit), so this module is no longer en+zh aligned.
    ("generate_table.py", ["en"]),
    ("online_bib_verify.py", ["zh", "typst"]),
]


@pytest.mark.parametrize(
    ("module_name", "skill_keys"),
    TIER1_HASH_GROUPS,
    ids=[f"{m}::{'+'.join(k)}" for m, k in TIER1_HASH_GROUPS],
)
def test_tier1_modules_hash_aligned(module_name: str, skill_keys: list[str]) -> None:
    """Tier-1 modules must be byte-identical across the listed skills."""
    hashes = {key: _file_hash(_module_path(key, module_name)) for key in skill_keys}
    unique = set(hashes.values())
    assert len(unique) == 1, (
        f"Drift detected for {module_name} across {skill_keys}: {hashes}. "
        f"Sync the copies (canonical source = {skill_keys[0]}) or, if the "
        "divergence is intentional, remove the affected skill key from the "
        "TIER1_HASH_GROUPS entry and document the specialization."
    )


# online_bib_verify.py: ZH and Typst are byte-identical, EN diverges by a
# small number of lines (98.9% similarity per stage 4 PoC). Cap the drift so
# accidental rewrites are caught without forcing EN to track the others.
ONLINE_BIB_VERIFY_EN_DRIFT_LIMIT = 12  # 4 add + 4 del + small headroom


def test_online_bib_verify_en_drift_bounded() -> None:
    """EN ``online_bib_verify.py`` may diverge from ZH/Typst only marginally.

    The three copies have the same line count (354) and share 98.9% of lines.
    If the diff grows beyond the documented headroom, either fold the change
    back into ZH/Typst (most likely correct) or update this limit with a
    matching note in findings.md.
    """
    en = _module_path("en", "online_bib_verify.py").read_text(encoding="utf-8").splitlines()
    zh = _module_path("zh", "online_bib_verify.py").read_text(encoding="utf-8").splitlines()
    matcher = difflib.SequenceMatcher(a=en, b=zh)
    changed_lines = sum(
        max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in matcher.get_opcodes() if tag != "equal"
    )
    assert changed_lines <= ONLINE_BIB_VERIFY_EN_DRIFT_LIMIT, (
        f"EN online_bib_verify.py drifted {changed_lines} lines from ZH copy "
        f"(limit {ONLINE_BIB_VERIFY_EN_DRIFT_LIMIT}). Either reconcile or "
        "raise the limit with a note in findings.md."
    )


# Modules that are intentionally absent from a given skill. Keeping this map
# under test prevents silent re-introduction (someone copying an unrelated
# module across) and silent removal (someone deleting a skill-specific module).
EXPECTED_ABSENCES: dict[str, list[str]] = {
    # EN-only — LaTeX-figure / prose-extraction tools with no Typst or ZH
    # analogue
    "check_figures.py": ["zh", "typst"],
    "extract_prose.py": ["zh", "typst"],
    # ZH-only — Chinese-thesis specialization
    "check_consistency.py": ["en", "typst"],
    "detect_template.py": ["en", "typst"],
    "map_structure.py": ["en", "typst"],
    # ZH does not ship these — kept on EN/Typst only
    "analyze_grammar.py": ["zh"],
    "analyze_sentences.py": ["zh"],
    "improve_expression.py": ["zh"],
    "translate_academic.py": ["zh"],
    "check_pseudocode.py": ["zh"],
}


@pytest.mark.parametrize(
    ("module_name", "absent_skill_keys"),
    sorted(EXPECTED_ABSENCES.items()),
    ids=sorted(EXPECTED_ABSENCES.keys()),
)
def test_expected_absences_hold(module_name: str, absent_skill_keys: list[str]) -> None:
    """Modules listed as absent for a skill must not appear there.

    Also asserts the module is present in at least one *other* skill, so
    deleting the canonical copy without updating EXPECTED_ABSENCES fails fast.
    """
    for key in absent_skill_keys:
        path = _module_path(key, module_name)
        assert not path.exists(), (
            f"{module_name} unexpectedly appeared in {key}. Either remove it "
            "or update EXPECTED_ABSENCES to reflect a deliberate cross-skill copy."
        )
    other_keys = set(SKILL_DIRS) - set(absent_skill_keys)
    present_elsewhere = any(_module_path(k, module_name).exists() for k in other_keys)
    assert present_elsewhere, (
        f"{module_name} is no longer present in any of {sorted(other_keys)}. "
        "Remove the EXPECTED_ABSENCES entry or restore the canonical copy."
    )


# Architecturally distinct modules — never aligned across skills. Listed only
# for documentation and to assert each copy still exists. Hash drift here is
# expected and not gated.
TIER4_ARCH_DISTINCT: list[tuple[str, list[str]]] = [
    ("compile.py", ["en", "zh", "typst"]),
    ("check_format.py", ["en", "zh", "typst"]),
    ("verify_bib.py", ["en", "zh", "typst"]),
]


@pytest.mark.parametrize(
    ("module_name", "skill_keys"),
    TIER4_ARCH_DISTINCT,
    ids=[m for m, _ in TIER4_ARCH_DISTINCT],
)
def test_tier4_modules_present_in_each_skill(module_name: str, skill_keys: list[str]) -> None:
    """Architecturally-distinct modules must each carry their own copy.

    Hashes are intentionally not aligned (latexmk vs typst, GB/T 7714 vs
    IEEE, etc.). This test simply asserts each skill keeps its copy.
    """
    for key in skill_keys:
        path = _module_path(key, module_name)
        assert path.exists(), (
            f"{key} is missing {module_name}; this module is architecturally "
            "distinct per skill and must remain vendored."
        )
