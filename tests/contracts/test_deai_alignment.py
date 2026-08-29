"""Alignment lint for the three vendored copies of ``deai_check.py``.

Like ``parsers.py`` (see ``test_parsers_alignment.py``), each skill keeps its
own ``scripts/deai_check.py`` so it installs in isolation. The EN copy is
canonical; ZH / Typst mirror the shared tier machinery, overclaim / tense /
throat-clearing logic and threshold tables, then specialize for their language
and markup. This test hash-locks the intentionally shared surface and registers
the documented divergences so drift (XC-3) can no longer land silently.

Specialization map (for human readers):

* ``latex-thesis-zh`` — ``ChineseAITraceChecker``. Chinese docstrings on shared
  logic (locked via docstring-stripped AST hashes), Chinese term / pattern
  tables, English-abstract region gating instead of ``TENSE_SECTIONS``, extra
  ``_check_parallel_sentences`` / ``_region_is_english`` / ``_loc`` helpers.
* ``typst-paper`` — bilingual (EN + CJK) ``AITraceChecker``. Character-based
  burstiness keys, CJK-aware punctuation / sentence-length / density checks,
  ``@fig``-reference tense guard (``_typst_ref_kw_re``), extra
  ``_check_parallel_openings`` and CJK signal tables, flat ``references/``
  layout for the thresholds YAML.

Intentionally divergent (language / markup driven — NOT locked): burstiness
opening keys (pinned below instead), ``_check_low_information_density``,
``_check_punctuation``, ``_check_sentence_length_variance``, ``_check_tense``,
``_check_term_threshold``, ``_get_instruction``, ``_is_false_positive``,
``check_section``, ``generate_report``, ``_load_thresholds``, ``main``.

When changing shared behavior, edit ``latex-paper-en/scripts/deai_check.py``
first, then mirror to Typst verbatim and to ZH preserving its Chinese
docstrings. Evidence for this classification lives in
``.trellis/tasks/07-05-deai-alignment-lock/research/findings.md``.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import inspect
import sys
import textwrap
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from tests.support.paths import SKILLS_ROOT

DEAI_FILES: dict[str, Path] = {
    "en": SKILLS_ROOT / "latex-paper-en" / "scripts" / "deai_check.py",
    "zh": SKILLS_ROOT / "latex-thesis-zh" / "scripts" / "deai_check.py",
    "typst": SKILLS_ROOT / "typst-paper" / "scripts" / "deai_check.py",
}

# The checker class name is itself a registered divergence.
CHECKER_CLASS = {"en": "AITraceChecker", "zh": "ChineseAITraceChecker", "typst": "AITraceChecker"}

# Registered divergence: each skill keeps its own references layout, so the
# user-overridable thresholds YAML lives at a different path per copy.
THRESHOLDS_YAML: dict[str, Path] = {
    "en": SKILLS_ROOT / "latex-paper-en" / "references" / "deai" / "tone-thresholds.yaml",
    "zh": SKILLS_ROOT / "latex-thesis-zh" / "references" / "deai" / "tone-thresholds.yaml",
    "typst": SKILLS_ROOT / "typst-paper" / "references" / "AI_TONE_THRESHOLDS.yaml",
}

# Modules the copies import from their own scripts dir; popped/restored so this
# test neither sees nor pollutes the EN/AUDIT modules conftest puts on sys.path.
_SIDECAR_MODULES = ("parsers", "tex_loader", "deai_check")


def _load_module(key: str, path: Path) -> ModuleType:
    """Load one copy by file path (never bare import — XC-3b: ``import
    deai_check`` silently resolves to the EN copy on ``sys.path``)."""
    saved_path = list(sys.path)
    saved = {m: sys.modules.pop(m, None) for m in _SIDECAR_MODULES}
    try:
        spec = importlib.util.spec_from_file_location(f"_deai_alignment_{key}", path)
        assert spec is not None and spec.loader is not None, f"cannot build spec for {path}"
        mod = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(path.parent))
        spec.loader.exec_module(mod)
        return mod
    finally:
        sys.path[:] = saved_path
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


@pytest.fixture(scope="module")
def deai_modules() -> dict[str, ModuleType]:
    return {key: _load_module(key, path) for key, path in DEAI_FILES.items()}


def _resolve(mod: ModuleType, key: str, dotted_path: str) -> Any:
    """Resolve ``Checker.<member>`` through the per-copy checker class name."""
    parts = dotted_path.split(".")
    obj: Any = mod
    for part in parts:
        obj = getattr(obj, CHECKER_CLASS[key] if part == "Checker" else part)
    return obj


def _hash_source(obj: Any) -> str:
    """Byte-strict hash: source for callables, ``repr`` for data."""
    if inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isclass(obj):
        payload = inspect.getsource(obj)
    else:
        payload = repr(obj)
    return hashlib.md5(payload.encode("utf-8")).hexdigest()


def _hash_logic(obj: Any) -> str:
    """Docstring-stripped AST hash: tolerates the Chinese docstrings that
    legitimately differ in the ZH copy while still locking executable logic."""
    tree = ast.parse(textwrap.dedent(inspect.getsource(obj)))
    for node in ast.walk(tree):
        if isinstance(node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            body = node.body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                node.body = body[1:] or [ast.Pass()]
    return hashlib.md5(ast.dump(tree).encode("utf-8")).hexdigest()


# (dotted attribute, copies that must hash-match byte-for-byte)
ALIGNMENTS: list[tuple[str, list[str]]] = [
    # Tier machinery shared verbatim across all three copies
    ("_TIER_FACTORS", ["en", "zh", "typst"]),
    # ZH carries a Chinese docstring on _apply_tier — logic locked in
    # LOGIC_ALIGNMENTS below; the EN/Typst pair must stay byte-identical.
    ("_apply_tier", ["en", "typst"]),
    # ZH has no TENSE_SECTIONS: it gates tense checks to the English-abstract
    # region (_english_abstract_range) instead of by section kind.
    ("TENSE_SECTIONS", ["en", "typst"]),
    # Checker internals shared verbatim across all three copies
    ("Checker._check_throat_clearing", ["en", "zh", "typst"]),
    ("Checker._iter_visible_lines", ["en", "typst"]),
    ("Checker._corpus_size", ["en", "typst"]),
    ("Checker._density_cap", ["en", "typst"]),
    ("Checker._check_term_threshold", ["en", "typst"]),
    ("Checker.calculate_density_score", ["en", "zh", "typst"]),
    # Shared verbatim by the EN family; ZH differs only in docstrings/comments
    # (locked below) or in section handling (_find_pattern_in_section,
    # analyze_document, generate_suggestions_json — Chinese output/flow).
    ("Checker._dim_tag", ["en", "typst"]),
    ("Checker._find_pattern_in_section", ["en", "typst"]),
    ("Checker._tense_false_positive", ["en", "typst"]),
    ("Checker.analyze_document", ["en", "typst"]),
    ("Checker.generate_suggestions_json", ["en", "typst"]),
]

# (dotted attribute, copies whose docstring-stripped AST must match). This is
# how the ZH copy participates in locks despite its Chinese docstrings.
LOGIC_ALIGNMENTS: list[tuple[str, list[str]]] = [
    ("_apply_tier", ["en", "zh", "typst"]),
    ("Checker._check_overclaim", ["en", "zh", "typst"]),
    ("Checker._iter_section_paragraphs", ["en", "zh", "typst"]),
    ("Checker._iter_visible_lines", ["en", "zh", "typst"]),
    ("Checker._corpus_size", ["en", "zh", "typst"]),
    ("Checker._density_cap", ["en", "zh", "typst"]),
    ("Checker._check_term_threshold", ["en", "zh", "typst"]),
    ("Checker._tense_false_positive", ["en", "zh", "typst"]),
    ("Checker._dim_tag", ["en", "zh", "typst"]),
]

# DEFAULT_THRESHOLDS sub-tables shared verbatim across all three copies.
# burstiness / term_thresholds / throat_clearing are registered divergences
# covered by the relationship tests below.
THRESHOLD_ALIGNMENTS: list[tuple[str, list[str]]] = [
    ("overclaim", ["en", "zh", "typst"]),
    ("punctuation", ["en", "zh", "typst"]),
    ("sentence_length", ["en", "zh", "typst"]),
    ("tense", ["en", "zh", "typst"]),
]


@pytest.mark.parametrize(
    ("dotted_path", "keys"),
    ALIGNMENTS,
    ids=[f"{path}::{'+'.join(keys)}" for path, keys in ALIGNMENTS],
)
def test_shared_attribute_aligned(
    deai_modules: dict[str, ModuleType], dotted_path: str, keys: list[str]
) -> None:
    """Members in ``ALIGNMENTS`` must be byte-identical across the listed copies."""
    hashes = {k: _hash_source(_resolve(deai_modules[k], k, dotted_path)) for k in keys}
    assert len(set(hashes.values())) == 1, (
        f"Drift detected for {dotted_path} across {keys}: {hashes}. "
        "Sync the copies (canonical = latex-paper-en) or update ALIGNMENTS "
        "if the divergence is intentional."
    )


@pytest.mark.parametrize(
    ("dotted_path", "keys"),
    LOGIC_ALIGNMENTS,
    ids=[f"{path}::{'+'.join(keys)}" for path, keys in LOGIC_ALIGNMENTS],
)
def test_shared_logic_aligned(
    deai_modules: dict[str, ModuleType], dotted_path: str, keys: list[str]
) -> None:
    """Members in ``LOGIC_ALIGNMENTS`` must match after stripping docstrings."""
    hashes = {k: _hash_logic(_resolve(deai_modules[k], k, dotted_path)) for k in keys}
    assert len(set(hashes.values())) == 1, (
        f"Logic drift detected for {dotted_path} across {keys}: {hashes}. "
        "Only docstrings/comments may differ (ZH translates them); sync the "
        "executable logic with the canonical latex-paper-en copy."
    )


@pytest.mark.parametrize(
    ("subkey", "keys"),
    THRESHOLD_ALIGNMENTS,
    ids=[f"{subkey}::{'+'.join(keys)}" for subkey, keys in THRESHOLD_ALIGNMENTS],
)
def test_shared_threshold_tables_aligned(
    deai_modules: dict[str, ModuleType], subkey: str, keys: list[str]
) -> None:
    """Shared ``DEFAULT_THRESHOLDS`` sub-tables must be identical."""
    values = {k: deai_modules[k].DEFAULT_THRESHOLDS[subkey] for k in keys}
    first = values[keys[0]]
    assert all(v == first for v in values.values()), (
        f"DEFAULT_THRESHOLDS[{subkey!r}] drifted: {values}"
    )


def test_burstiness_config_pinned(deai_modules: dict[str, ModuleType]) -> None:
    """Burstiness opening keys are a registered divergence — pinned, not synced.

    EN keys a paragraph opening by its first 2 *word tokens*; ZH slices the
    first 4 *characters* (CJK has no whitespace tokenization; 4 chars ≈ 2
    words); bilingual Typst slices 8 characters (≈ 2 English words).
    Adjudicated intentional on 2026-07-06 (07-05-deai-alignment-lock) — a value
    change here means the sensitivity design changed and needs re-adjudication.
    """
    expected = {"en": 2, "zh": 4, "typst": 8}
    for key, mod in deai_modules.items():
        cfg = mod.DEFAULT_THRESHOLDS["burstiness"]
        assert cfg["opening_token_count"] == expected[key], f"{key}: {cfg}"
        assert cfg["consecutive_paragraphs"] == 3, f"{key}: {cfg}"


def test_tense_presents_signal_is_verb_only(deai_modules: dict[str, ModuleType]) -> None:
    """SH-1 regression: ``\\bpresents\\b`` (verb only) in both config layers.

    ``presents?`` also matched the adjective in "the present study"; the fix
    must hold in DEFAULT_THRESHOLDS *and* the per-skill thresholds YAML (the
    YAML overrides the default, and the default is the no-PyYAML fallback).
    """
    for key, mod in deai_modules.items():
        signals = mod.DEFAULT_THRESHOLDS["tense"]["present_signals"]
        assert r"\bpresents\b" in signals, f"{key}: presents signal missing"
        assert not any("presents?" in p for p in signals), f"{key}: presents? crept back"
    for key, yaml_path in THRESHOLDS_YAML.items():
        text = yaml_path.read_text(encoding="utf-8")
        assert "\\\\bpresents\\\\b" in text, f"{key}: presents signal missing in YAML"
        assert "presents?" not in text, f"{key}: presents? crept back in YAML"


def test_thresholds_yaml_exists_where_loader_looks(deai_modules: dict[str, ModuleType]) -> None:
    """Pin THRESHOLDS_FILENAME to the real per-skill YAML (layout divergence
    is intentional; renaming either side without the other must go red)."""
    for key, mod in deai_modules.items():
        expected = THRESHOLDS_YAML[key]
        assert expected.name == mod.THRESHOLDS_FILENAME, (
            f"{key}: THRESHOLDS_FILENAME={mod.THRESHOLDS_FILENAME!r} != {expected.name!r}"
        )
        assert expected.exists(), f"{key}: {expected} missing"


def test_dimension_map_relationships(deai_modules: dict[str, ModuleType]) -> None:
    """Shared signal categories must agree on their dimension tag; ZH/Typst
    extend EN's map with identical CJK-specific categories."""
    maps = {k: mod.DIMENSION_MAP for k, mod in deai_modules.items()}
    shared = set(maps["en"]) & set(maps["zh"]) & set(maps["typst"])
    for cat in sorted(shared):
        tags = {k: maps[k][cat] for k in maps}
        assert len(set(tags.values())) == 1, f"dimension tag drift for {cat}: {tags}"
    assert set(maps["en"]) <= set(maps["zh"]), "EN categories missing from ZH map"
    assert set(maps["en"]) <= set(maps["typst"]), "EN categories missing from Typst map"
    assert maps["zh"] == maps["typst"], "ZH and Typst dimension maps drifted apart"


def test_teaching_notes_cover_same_dimensions(deai_modules: dict[str, ModuleType]) -> None:
    """Note text is per-language, but all copies must teach the same D1–D5."""
    key_sets = {k: set(mod.TEACHING_NOTES) for k, mod in deai_modules.items()}
    assert key_sets["en"] == key_sets["zh"] == key_sets["typst"], key_sets


def test_term_thresholds_relationships(deai_modules: dict[str, ModuleType]) -> None:
    """Typst's term table = EN's English terms + a curated subset of ZH's
    Chinese terms; every shared entry must carry the same config."""
    tables = {k: mod.DEFAULT_THRESHOLDS["term_thresholds"] for k, mod in deai_modules.items()}
    en, zh, typst = tables["en"], tables["zh"], tables["typst"]
    assert set(en) <= set(typst), "EN terms missing from Typst table"
    for term in en:
        assert en[term] == typst[term], f"config drift for shared term {term!r}"
    cjk_extras = set(typst) - set(en)
    assert cjk_extras <= set(zh), f"Typst CJK terms not sourced from ZH: {cjk_extras - set(zh)}"
    # C1 calibrates the ZH thesis table only. Typst keeps its pre-C1 absolute
    # limits under threshold_unit=per_document until a Typst corpus is measured.
    expected_typst_cjk = {
        "首先": 4,
        "其次": 4,
        "然而": 5,
        "因此": 6,
        "显然": 3,
        "显著": 5,
        "全面": 3,
        "深入": 3,
        "重要": 5,
        "关键": 5,
        "核心": 4,
    }
    assert {term: typst[term] for term in cjk_extras} == expected_typst_cjk


def test_threshold_units_preserve_unscaled_surfaces(
    deai_modules: dict[str, ModuleType],
) -> None:
    assert deai_modules["zh"].DEFAULT_THRESHOLDS["threshold_unit"] == "per_10k_chars"
    for key in ("en", "typst"):
        mod = deai_modules[key]
        assert mod.DEFAULT_THRESHOLDS["threshold_unit"] == "per_document"
        scaled = mod._apply_tier(mod.DEFAULT_THRESHOLDS, "light")
        assert isinstance(
            scaled["term_thresholds"][next(iter(mod.DEFAULT_THRESHOLDS["term_thresholds"]))], int
        )


def test_throat_clearing_relationships(deai_modules: dict[str, ModuleType]) -> None:
    """Typst's throat-clearing patterns = EN's + a curated subset of ZH's."""
    patterns = {
        k: set(mod.DEFAULT_THRESHOLDS["throat_clearing"]["patterns"])
        for k, mod in deai_modules.items()
    }
    assert patterns["en"] <= patterns["typst"], "EN patterns missing from Typst"
    cjk_extras = patterns["typst"] - patterns["en"]
    assert cjk_extras <= patterns["zh"], f"Typst CJK patterns not sourced from ZH: {cjk_extras}"


def test_copy_specializations_present(deai_modules: dict[str, ModuleType]) -> None:
    """Loading guard + divergence register: each copy keeps its specializations.

    Doubles as proof the importlib loader really returned three distinct
    copies (a broken loader would resolve everything to the EN module).
    """
    en, zh, typst = deai_modules["en"], deai_modules["zh"], deai_modules["typst"]

    # EN (canonical): no CJK/Typst extras, section-kind tense gating
    assert hasattr(en, "AITraceChecker") and not hasattr(en, "ChineseAITraceChecker")
    assert hasattr(en, "TENSE_SECTIONS")
    assert "_check_parallel_openings" not in vars(en.AITraceChecker)

    # ZH: Chinese checker with English-abstract region gating
    assert hasattr(zh, "ChineseAITraceChecker") and not hasattr(zh, "AITraceChecker")
    assert not hasattr(zh, "TENSE_SECTIONS"), "ZH gates by abstract region, not section kind"
    for member in (
        "_english_abstract_range",
        "_region_is_english",
        "_check_parallel_sentences",
        "_loc",
        "_span_to_lines",
    ):
        assert member in vars(zh.ChineseAITraceChecker), f"ZH lost {member}"

    # Typst: bilingual checker with @ref tense guard and CJK signal tables
    assert hasattr(typst, "AITraceChecker") and hasattr(typst, "TENSE_SECTIONS")
    assert "_check_parallel_openings" in vars(typst.AITraceChecker)
    for attr in ("AI_FILLER_CONNECTORS", "VAGUE_COMPARATIVES", "COMMAND_TEMPLATE_OPENINGS"):
        assert hasattr(typst.AITraceChecker, attr), f"Typst lost {attr}"
    tense_src = inspect.getsource(typst.AITraceChecker._check_tense)
    assert "_typst_ref_kw_re" in tense_src, "Typst lost its @ref tense guard"
