"""Alignment lint for the four vendored copies of ``parsers.py``.

Each script-based skill keeps its own ``scripts/parsers.py`` so it can be
installed in isolation under ``~/.claude/skills/{skill}/``. The cost of that
choice is drift: a fix landing in one copy may silently miss the others. This
test enforces hash-equality on the parts that are intentionally shared, while
allowing the documented per-skill specializations to differ.

Specialization map (for human readers):

* ``latex-thesis-zh`` — Chinese-thesis variant. Custom section / heading
  patterns, additional ``extract_headings`` helper, dedicated ``\\ctitle`` /
  ``\\cabstract`` extractors, no ``clean_text`` ABC contract.
* ``typst-paper`` — Typst-only subset. Carries ``TypstParser`` and Typst
  helpers, omits ``LatexParser`` and ``_strip_latex_markup``.
* ``paper-audit`` — Vendored copy of the canonical (latex-paper-en) module
  plus an extended ``get_parser`` that dispatches PDF inputs to ``PdfParser``.

When changing shared behavior, edit ``latex-paper-en/scripts/parsers.py``
first, mirror the change to ``paper-audit/scripts/parsers.py``, then update
ZH / Typst copies as their specializations require.
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

SKILLS_ROOT = Path(__file__).parent.parent / "academic-writing-skills"

PARSER_FILES: dict[str, Path] = {
    "en": SKILLS_ROOT / "latex-paper-en" / "scripts" / "parsers.py",
    "zh": SKILLS_ROOT / "latex-thesis-zh" / "scripts" / "parsers.py",
    "typst": SKILLS_ROOT / "typst-paper" / "scripts" / "parsers.py",
    "audit": SKILLS_ROOT / "paper-audit" / "scripts" / "parsers.py",
}


def _load_module(key: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(f"_parsers_alignment_{key}", path)
    assert spec is not None and spec.loader is not None, f"cannot build spec for {path}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def parser_modules() -> dict[str, ModuleType]:
    return {key: _load_module(key, path) for key, path in PARSER_FILES.items()}


def _resolve(mod: ModuleType, dotted_path: str) -> Any:
    obj: Any = mod
    for part in dotted_path.split("."):
        obj = getattr(obj, part)
    return obj


def _hash_obj(obj: Any) -> str:
    if inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isclass(obj):
        payload = inspect.getsource(obj)
    else:
        payload = repr(obj)
    return hashlib.md5(payload.encode("utf-8")).hexdigest()


# (dotted attribute on module, list of skill keys that must hash-match)
ALIGNMENTS: list[tuple[str, list[str]]] = [
    # Free helpers shared verbatim
    ("_normalize_whitespace", ["en", "zh", "typst", "audit"]),
    ("_extract_balanced_block", ["en", "typst", "audit"]),
    ("_strip_typst_markup", ["en", "typst", "audit"]),
    ("_strip_latex_markup", ["en", "audit"]),
    # Class-level pattern lists (data, not source)
    ("LatexParser.PRESERVE_PATTERNS", ["en", "zh", "audit"]),
    ("TypstParser.PRESERVE_PATTERNS", ["en", "zh", "typst", "audit"]),
    # Concrete parser methods (ZH variants are intentionally cosmetic-different)
    ("LatexParser.extract_visible_text", ["en", "audit"]),
    ("TypstParser.extract_visible_text", ["en", "typst", "audit"]),
    # Title / abstract / citation extractors that paper-audit re-exports
    ("extract_title", ["en", "audit"]),
    ("extract_abstract", ["en", "audit"]),
    ("extract_latex_citation_keys", ["en", "audit"]),
]


@pytest.mark.parametrize(
    ("dotted_path", "keys"),
    ALIGNMENTS,
    ids=[f"{path}::{'+'.join(keys)}" for path, keys in ALIGNMENTS],
)
def test_shared_attribute_aligned(
    parser_modules: dict[str, ModuleType],
    dotted_path: str,
    keys: list[str],
) -> None:
    """Members listed in ``ALIGNMENTS`` must hash-match across the listed copies."""
    hashes = {k: _hash_obj(_resolve(parser_modules[k], dotted_path)) for k in keys}
    unique = set(hashes.values())
    assert len(unique) == 1, (
        f"Drift detected for {dotted_path} across {keys}: {hashes}. "
        "Sync the copies (canonical = latex-paper-en) or update ALIGNMENTS "
        "if the divergence is intentional."
    )


REQUIRED_ABC_METHODS = ("split_sections", "extract_visible_text", "get_comment_prefix")


def test_required_abc_methods_present(parser_modules: dict[str, ModuleType]) -> None:
    """Every copy must declare the minimum ``DocumentParser`` contract."""
    for key, mod in parser_modules.items():
        members = set(vars(mod.DocumentParser).keys())
        missing = set(REQUIRED_ABC_METHODS) - members
        assert not missing, f"{key}: DocumentParser missing {missing}"


def test_required_abc_signatures_aligned(parser_modules: dict[str, ModuleType]) -> None:
    """Required-method signatures must match across all four copies."""
    for method_name in REQUIRED_ABC_METHODS:
        sigs = {
            key: str(inspect.signature(getattr(mod.DocumentParser, method_name)))
            for key, mod in parser_modules.items()
        }
        unique = set(sigs.values())
        assert len(unique) == 1, f"Signature drift in {method_name}: {sigs}"


def test_clean_text_is_canonical_only(parser_modules: dict[str, ModuleType]) -> None:
    """``clean_text`` is part of EN / Typst / Audit; ZH intentionally omits it."""
    for key in ("en", "typst", "audit"):
        assert "clean_text" in vars(parser_modules[key].DocumentParser), (
            f"{key}: ABC missing clean_text — keep it aligned with the canonical copy"
        )
    assert "clean_text" not in vars(parser_modules["zh"].DocumentParser), (
        "zh: ABC unexpectedly declared clean_text — ZH variant is intentionally minimal"
    )


def test_audit_get_parser_supports_pdf(parser_modules: dict[str, ModuleType]) -> None:
    """paper-audit's ``get_parser`` keeps its PDF dispatch extension."""
    sig = inspect.signature(parser_modules["audit"].get_parser)
    assert {"file_path", "pdf_mode", "heading_pt", "body_pt"} <= set(sig.parameters), (
        "paper-audit get_parser lost its PDF parameters — restore the extended signature"
    )
