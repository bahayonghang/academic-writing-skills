"""Tests for paper-audit i18n dictionary."""

from __future__ import annotations

import sys

from tests.support.paths import SCRIPT_DIR_AUDIT

if str(SCRIPT_DIR_AUDIT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR_AUDIT))

from i18n import EN, STRINGS, ZH, available_languages, normalize_lang, t


def test_available_languages_includes_en_zh() -> None:
    langs = available_languages()
    assert "en" in langs
    assert "zh" in langs


def test_zh_covers_every_en_key() -> None:
    """Every English key must have a Chinese counterpart so renders never fall back."""
    missing = sorted(set(EN) - set(ZH))
    assert not missing, (
        f"zh dictionary missing keys: {missing[:8]}{'...' if len(missing) > 8 else ''}"
    )


def test_no_extra_zh_keys() -> None:
    """The Chinese dict should not introduce keys absent from English."""
    extra = sorted(set(ZH) - set(EN))
    assert not extra, f"zh dictionary has stray keys: {extra}"


def test_normalize_lang_aliases() -> None:
    assert normalize_lang(None) == "en"
    assert normalize_lang("") == "en"
    assert normalize_lang("EN") == "en"
    assert normalize_lang("zh") == "zh"
    assert normalize_lang("ZH-CN") == "zh"
    assert normalize_lang("cn") == "zh"
    assert normalize_lang("fr") == "en"  # unknown -> default en


def test_t_returns_translation_for_known_keys() -> None:
    assert t("title.deep_review", "en") == "# Deep Review Report"
    assert t("title.deep_review", "zh") == "# 深度审稿报告"
    assert t("common.paper", "en") == "**Paper**"
    assert t("common.paper", "zh") == "**论文**"


def test_t_falls_back_to_english_when_zh_missing() -> None:
    """Sanity check: stash a temp en-only key, query it from zh."""
    EN["__tmp_test_key__"] = "ONLY_EN"
    try:
        # zh dict does not contain __tmp_test_key__; should fall back to EN
        assert t("__tmp_test_key__", "zh") == "ONLY_EN"
    finally:
        EN.pop("__tmp_test_key__", None)


def test_t_returns_key_when_missing_entirely() -> None:
    assert t("__no_such_key__", "en") == "__no_such_key__"
    assert t("__no_such_key__", "zh") == "__no_such_key__"


def test_t_supports_format_args() -> None:
    assert t(
        "status.executive_template", "en", total=3, critical=1, overall=4.2, label="Accept"
    ) == ("Found **3 issues** (1 critical). Overall score: **4.2/6.0** (Accept).")
    formatted_zh = t(
        "status.executive_template", "zh", total=3, critical=1, overall=4.2, label="录用"
    )
    assert "共发现 **3 个问题**" in formatted_zh
    assert "**4.2/6.0**" in formatted_zh


def test_strings_dict_only_lists_supported_languages() -> None:
    assert set(STRINGS.keys()) == {"en", "zh"}
