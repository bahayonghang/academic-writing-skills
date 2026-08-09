"""Lock the shared method-narrative criteria across the writing skills."""

from __future__ import annotations

import importlib.util
import re
import sys
from types import ModuleType

from tests.support.paths import SCRIPT_DIR_EN, SCRIPT_DIR_TYPST, SCRIPT_DIR_ZH


def _load_logic(name: str, script_dir, collisions: tuple[str, ...]) -> ModuleType:
    saved_path = list(sys.path)
    saved_modules = {module: sys.modules.pop(module, None) for module in collisions}
    try:
        sys.path.insert(0, str(script_dir))
        spec = importlib.util.spec_from_file_location(name, script_dir / "analyze_logic.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for module_name, module in saved_modules.items():
            if module is None:
                sys.modules.pop(module_name, None)
            else:
                sys.modules[module_name] = module


EN = _load_logic("method_logic_en", SCRIPT_DIR_EN, ("parsers", "tex_loader"))
TYPST = _load_logic("method_logic_typst", SCRIPT_DIR_TYPST, ("parsers",))
ZH = _load_logic("method_logic_zh", SCRIPT_DIR_ZH, ("parsers", "tex_loader"))


def _mn_patterns(module: ModuleType) -> dict[str, str]:
    return {
        name: value.pattern
        for name, value in vars(module).items()
        if name.startswith("MN_") and isinstance(value, re.Pattern)
    }


def test_method_narrative_loaders_target_each_skill_copy() -> None:
    assert str(SCRIPT_DIR_EN) in str(EN.__file__)
    assert str(SCRIPT_DIR_TYPST) in str(TYPST.__file__)
    assert str(SCRIPT_DIR_ZH) in str(ZH.__file__)


def test_method_narrative_structural_constants_align() -> None:
    expected = (3, 2, 3)
    names = ("MN_HEADING_RUN", "MN_HEADING_HITS", "MN_EQUATION_LOOKAHEAD")

    assert tuple(getattr(EN, name) for name in names) == expected
    assert tuple(getattr(TYPST, name) for name in names) == expected
    assert tuple(getattr(ZH, name) for name in names) == expected


def test_english_and_typst_method_regexes_align() -> None:
    patterns = _mn_patterns(EN)

    assert patterns == _mn_patterns(TYPST)
    assert set(patterns) == {
        "MN_ANNOUNCE_RE",
        "MN_SEQ_OPEN_RE",
        "MN_CAUSE_EXEMPT_RE",
        "MN_EQ_GLOSS_RE",
    }


def test_chinese_method_regexes_remain_explicit() -> None:
    for name in (
        "MN_ANNOUNCE_RE_ZH",
        "MN_SEQ_OPEN_RE_ZH",
        "MN_CAUSE_EXEMPT_RE_ZH",
        "MN_EQ_GLOSS_RE_ZH",
    ):
        assert isinstance(getattr(ZH, name), re.Pattern)
