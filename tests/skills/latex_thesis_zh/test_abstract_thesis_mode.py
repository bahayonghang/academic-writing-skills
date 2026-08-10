"""Tests for the degree-thesis abstract skeleton mode (analyze_abstract.py).

Covers the T-* skeleton checks, the char-limit constant lock against
check_spec.py, the --model five fallback, and the --bilingual B-* checks.

The ZH analyze_abstract.py copy is out of the writing-modules hash group
(test_writing_modules_alignment: analyze_abstract only locks en/typst), so it
is free to carry the thesis-only ThesisAbstractAnalyzer. Modules are loaded by
file path via importlib because conftest keeps EN/AUDIT scripts first on
sys.path (bare `import analyze_abstract` would resolve to the EN copy).
"""

import importlib.util
import sys
from pathlib import Path

import pytest

from tests.support.paths import SCRIPT_DIR_ZH

_ZH_DIR = SCRIPT_DIR_ZH


def _load_zh(name: str):
    saved_path = list(sys.path)
    collision = ("parsers", "tex_loader", "map_structure")
    saved = {m: sys.modules.pop(m, None) for m in collision}
    try:
        spec = importlib.util.spec_from_file_location(f"zh_absmode_{name}", _ZH_DIR / f"{name}.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(_ZH_DIR))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for mod_name, mod in saved.items():
            if mod is None:
                sys.modules.pop(mod_name, None)
            else:
                sys.modules[mod_name] = mod


analyze_abstract = _load_zh("analyze_abstract")
check_spec = _load_zh("check_spec")


def test_loader_guard():
    """Confirm we loaded the ZH copy (has the thesis-only class), not the EN one."""
    assert hasattr(analyze_abstract, "ThesisAbstractAnalyzer")
    assert hasattr(analyze_abstract, "THESIS_ABSTRACT_CHARS")


# ── fixtures builders ────────────────────────────────────────


def _tex(
    abstract: str,
    title: str = "水泥烧成系统智能优化控制方法研究",
    keywords: str = "水泥烧成系统；智能优化；预测控制；调控",
    english: str | None = None,
) -> str:
    kw = f"\\cnkeywords{{{keywords}}}\n" if keywords else ""
    en = f"\\begin{{eabstract}}\n{english}\n\\end{{eabstract}}\n" if english is not None else ""
    return (
        "\\documentclass{thuthesis}\n"
        f"\\ctitle{{{title}}}\n{kw}"
        "\\begin{document}\n"
        f"\\begin{{cabstract}}\n{abstract}\n\\end{{cabstract}}\n{en}"
        "\\end{document}\n"
    )


def _analyze(tmp_path: Path, tex: str, **kwargs) -> dict:
    f = tmp_path / "main.tex"
    f.write_text(tex, encoding="utf-8")
    return analyze_abstract.ThesisAbstractAnalyzer(str(f), **kwargs).analyze()


def _check(result: dict, cid: str) -> dict:
    for c in result["checks"]:
        if c["id"] == cid:
            return c
    raise KeyError(cid)


def _bcheck(result: dict, cid: str) -> dict:
    for c in result["bilingual"]["checks"]:
        if c["id"] == cid:
            return c
    raise KeyError(cid)


# A well-formed skeleton: object-first, pain point, lead-in, two numbered
# work segments (each problem-oriented), named verification. Short background.
GOOD_ABSTRACT = (
    "水泥烧成系统是水泥生产的关键环节。然而，该系统难以建立精确机理模型，带来挑战。"
    "主要研究工作和创新点如下："
    "（1）针对建模难题，提出了一种数据驱动的软测量方法，该方法融合多源数据并采用深度网络建模，"
    "采用实际生产数据验证其精度。"
    "（2）针对控制难题，建立了预测优化模型，设计了滚动优化策略，采用实际生产数据进行实验，"
    "实验结果表明所提方法有效，能够提升系统运行稳定性并降低能耗。"
)


# ── constant lock against check_spec ─────────────────────────


def test_char_limits_locked_to_check_spec():
    ys = check_spec.TEMPLATE_THRESHOLDS["yanshan"]
    assert analyze_abstract.THESIS_ABSTRACT_CHARS["doctor"] == ys["doctor"]["abstract"]
    assert analyze_abstract.THESIS_ABSTRACT_CHARS["master"] == ys["master"]["abstract"]


def test_degree_selects_char_bounds(tmp_path: Path):
    res_d = _analyze(tmp_path, _tex(GOOD_ABSTRACT), degree="doctor")
    assert res_d["count"]["limit"] == {"min": 900, "max": 1200}
    res_m = _analyze(tmp_path, _tex(GOOD_ABSTRACT), degree="master")
    assert res_m["count"]["limit"] == {"min": 500, "max": 650}


def test_max_chars_overrides_upper_bound(tmp_path: Path):
    res = _analyze(tmp_path, _tex(GOOD_ABSTRACT), degree="doctor", max_chars=400)
    assert res["count"]["limit"] == {"min": 900, "max": 400}


# ── T-* positive (well-formed abstract) ──────────────────────


@pytest.mark.parametrize(
    "cid",
    [
        "T-OPEN",
        "T-PAIN",
        "T-LEAD",
        "T-ENUM",
        "T-PROB",
        "T-VERIFY",
        "T-VERB",
        "T-INNOV",
        "T-TOC-STYLE",
        "T-VOICE",
    ],
)
def test_good_abstract_passes(tmp_path: Path, cid: str):
    res = _analyze(tmp_path, _tex(GOOD_ABSTRACT))
    assert not _check(res, cid)["flagged"], _check(res, cid)["message"]


def test_good_keyword_matches_title(tmp_path: Path):
    res = _analyze(tmp_path, _tex(GOOD_ABSTRACT))
    assert not _check(res, "T-KW-FIRST")["flagged"]


def test_defined_abbr_not_flagged(tmp_path: Path):
    abstract = GOOD_ABSTRACT.replace("深度网络", "长短期记忆（Long Short-Term Memory, LSTM）网络")
    res = _analyze(tmp_path, _tex(abstract))
    assert not _check(res, "T-ABBR")["flagged"]


# ── T-* negative (each check fires on a crafted flaw) ─────────


def test_open_flagged_when_method_first(tmp_path: Path):
    res = _analyze(tmp_path, _tex("本文提出一种方法。" + GOOD_ABSTRACT))
    c = _check(res, "T-OPEN")
    assert c["flagged"] and c["needs_llm"]


def test_pain_flagged_when_missing(tmp_path: Path):
    abstract = "水泥烧成系统是关键环节。主要研究工作如下：（1）提出方法，采用实验验证。"
    res = _analyze(tmp_path, _tex(abstract))
    assert _check(res, "T-PAIN")["flagged"]


def test_lead_flagged_when_missing(tmp_path: Path):
    abstract = "水泥烧成系统是关键环节，然而难以建模。（1）提出方法，采用实验验证。"
    res = _analyze(tmp_path, _tex(abstract))
    assert _check(res, "T-LEAD")["flagged"]


def test_enum_flagged_when_missing(tmp_path: Path):
    abstract = "水泥烧成系统是关键环节，然而难以建模。本文提出一种方法，采用实验验证其有效性。"
    res = _analyze(tmp_path, _tex(abstract))
    assert _check(res, "T-ENUM")["flagged"]


def test_prob_flagged_when_segments_lack_problem_lead(tmp_path: Path):
    abstract = (
        "水泥烧成系统是关键环节，然而难以建模。主要研究工作如下："
        "（1）提出了一种软测量方法，采用实际生产数据验证。"
        "（2）建立了优化模型，采用实际生产数据实验。"
    )
    res = _analyze(tmp_path, _tex(abstract))
    assert _check(res, "T-PROB")["flagged"]


def test_verify_flagged_when_no_carrier(tmp_path: Path):
    abstract = (
        "水泥烧成系统是关键环节，然而难以建模。主要研究工作如下："
        "（1）针对建模难题，提出了一种方法，验证了所提方法的有效性。"
    )
    res = _analyze(tmp_path, _tex(abstract))
    assert _check(res, "T-VERIFY")["flagged"]


def test_verb_flagged_on_oral_verb(tmp_path: Path):
    abstract = GOOD_ABSTRACT.replace("提出了一种数据驱动的软测量方法", "搞了一个软测量方法")
    res = _analyze(tmp_path, _tex(abstract))
    c = _check(res, "T-VERB")
    assert c["flagged"] and c["level"] == "Info"


def test_abbr_flagged_when_undefined(tmp_path: Path):
    abstract = GOOD_ABSTRACT.replace("深度网络", "LSTM网络")
    res = _analyze(tmp_path, _tex(abstract))
    c = _check(res, "T-ABBR")
    assert c["flagged"] and "LSTM" in c["message"]


def test_num_hedge_skip_without_numbers(tmp_path: Path):
    res = _analyze(tmp_path, _tex(GOOD_ABSTRACT))
    assert _check(res, "T-NUM-HEDGE")["skipped"]


def test_num_hedge_flagged_when_bare_percentage(tmp_path: Path):
    abstract = GOOD_ABSTRACT.replace("提升系统运行稳定性并降低能耗", "使精度提升14%")
    res = _analyze(tmp_path, _tex(abstract))
    c = _check(res, "T-NUM-HEDGE")
    assert not c["skipped"] and c["flagged"]


def test_num_hedge_passes_with_hedge(tmp_path: Path):
    abstract = GOOD_ABSTRACT.replace("提升系统运行稳定性并降低能耗", "使精度提升约14%以上")
    res = _analyze(tmp_path, _tex(abstract))
    assert not _check(res, "T-NUM-HEDGE")["flagged"]


def test_kw_first_flagged_when_unrelated(tmp_path: Path):
    res = _analyze(tmp_path, _tex(GOOD_ABSTRACT, keywords="深度学习；神经网络；控制"))
    assert _check(res, "T-KW-FIRST")["flagged"]


def test_kw_first_skipped_without_keywords(tmp_path: Path):
    res = _analyze(tmp_path, _tex(GOOD_ABSTRACT, keywords=""))
    assert _check(res, "T-KW-FIRST")["skipped"]


def test_innov_flagged_when_missing(tmp_path: Path):
    abstract = "水泥烧成系统是关键环节，然而难以建模。本文提出一种方法，采用实验验证其有效性。"
    res = _analyze(tmp_path, _tex(abstract))
    assert _check(res, "T-INNOV")["flagged"]


def test_toc_style_flagged_on_chapter_list(tmp_path: Path):
    abstract = "本文结构如下：第一章介绍背景，第二章介绍方法，第三章介绍实验。"
    res = _analyze(tmp_path, _tex(abstract))
    c = _check(res, "T-TOC-STYLE")
    assert c["flagged"] and c["needs_llm"]


def test_voice_flagged_on_first_person(tmp_path: Path):
    abstract = GOOD_ABSTRACT.replace("提出了一种数据驱动的软测量方法", "我们提出了一种软测量方法")
    res = _analyze(tmp_path, _tex(abstract))
    c = _check(res, "T-VOICE")
    assert c["flagged"] and c["level"] == "Info"


def test_benguo_not_first_person(tmp_path: Path):
    """PRD constraint 2: 本文/本论文 are legal, not flagged as first person."""
    res = _analyze(tmp_path, _tex(GOOD_ABSTRACT))
    assert not _check(res, "T-VOICE")["flagged"]


# ── --model five fallback ────────────────────────────────────


def test_five_model_still_works(tmp_path: Path):
    f = tmp_path / "main.tex"
    f.write_text(_tex(GOOD_ABSTRACT), encoding="utf-8")
    result = analyze_abstract.AbstractAnalyzer(str(f), lang="zh", max_chars=300).analyze()
    assert "elements" in result
    assert result["status"] != "ERROR"
    assert set(result["elements"]) == {
        "background",
        "objective",
        "methods",
        "results",
        "conclusion",
    }


# ── _extract_english_abstract forms ──────────────────────────


def test_extract_english_from_eabstract():
    content = (
        "\\begin{cabstract}中文\\end{cabstract}\n\\begin{eabstract}English text.\\end{eabstract}"
    )
    assert "English text" in analyze_abstract._extract_english_abstract(content)


def test_extract_english_from_plain_abstract_when_cabstract_used():
    content = (
        "\\begin{cabstract}中文\\end{cabstract}\n\\begin{abstract}English body.\\end{abstract}"
    )
    assert "English body" in analyze_abstract._extract_english_abstract(content)


def test_extract_english_from_heading():
    content = "\\chapter{Abstract}\nEnglish heading body.\n\\chapter{Introduction}\nbody"
    got = analyze_abstract._extract_english_abstract(content)
    assert "English heading body" in got and "Introduction" not in got


def test_extract_english_missing_returns_empty():
    content = "\\begin{cabstract}只有中文摘要。\\end{cabstract}"
    assert analyze_abstract._extract_english_abstract(content) == ""


# ── --bilingual B-* checks ───────────────────────────────────

BI_ZH = (
    "水泥烧成系统是关键环节，然而难以建模。主要研究工作如下："
    "（1）针对建模难题，提出了软测量方法。首先分析特性，然后建立模型，最后验证。"
    "（2）针对控制难题，建立了优化模型，使精度提升约14%。"
)
BI_EN = (
    "The cement calcination system is critical, however it is hard to model. "
    "The main work is as follows: (1) A soft-sensing method is proposed. First the "
    "characteristics are analyzed, then a model is built, finally it is verified. "
    "(2) An optimization model is built, improving accuracy by about 14%."
)


def test_bilingual_aligned_passes(tmp_path: Path):
    res = _analyze(tmp_path, _tex(BI_ZH, english=BI_EN), bilingual=True)
    assert res["bilingual"]["english_found"]
    for cid in ("B-ORD", "B-NUM", "B-ENUM", "B-LEN"):
        assert not _bcheck(res, cid)["flagged"], cid


def test_bilingual_missing_english_flags_len(tmp_path: Path):
    res = _analyze(tmp_path, _tex(BI_ZH), bilingual=True)
    assert not res["bilingual"]["english_found"]
    assert _bcheck(res, "B-LEN")["flagged"]


def test_bilingual_num_mismatch_is_error(tmp_path: Path):
    en_bad = BI_EN.replace("by about 14%", "by about 15%")
    res = _analyze(tmp_path, _tex(BI_ZH, english=en_bad), bilingual=True)
    c = _bcheck(res, "B-NUM")
    assert c["flagged"] and c["level"] == "Error"


def test_bilingual_order_mismatch_flagged(tmp_path: Path):
    en_bad = BI_EN.replace("First the ", "").replace("then a model is built, ", "")
    res = _analyze(tmp_path, _tex(BI_ZH, english=en_bad), bilingual=True)
    assert _bcheck(res, "B-ORD")["flagged"]


def test_bilingual_enum_mismatch_flagged(tmp_path: Path):
    en_bad = BI_EN.replace(
        "(2) An optimization model is built, improving accuracy by about 14%.", ""
    )
    res = _analyze(tmp_path, _tex(BI_ZH, english=en_bad), bilingual=True)
    # english now has one numbered item vs two in Chinese
    assert _bcheck(res, "B-ENUM")["flagged"]


def test_bilingual_semantic_is_llm_lane(tmp_path: Path):
    res = _analyze(tmp_path, _tex(BI_ZH, english=BI_EN), bilingual=True)
    c = _bcheck(res, "B-SEM")
    assert c["source"] == "[LLM]" and not c["flagged"]


def test_bilingual_nature_prompt_is_llm_lane(tmp_path: Path):
    res = _analyze(tmp_path, _tex(BI_ZH, english=BI_EN), bilingual=True)
    c = _bcheck(res, "B-NAT")
    assert c["level"] == "Info" and c["source"] == "[LLM]"
    assert not c["flagged"] and c["ref"] == "nature-writing N3"
    assert "可能缺少领域背景" in c["message"]
    assert "需结合摘要类型判断" in c["message"]
    assert "可能需要收束范围" in c["message"]
    assert "可能缺乏落地感" in c["message"]


def test_bilingual_nature_prompt_requires_english_abstract(tmp_path: Path):
    res = _analyze(tmp_path, _tex(BI_ZH), bilingual=True)
    assert "B-NAT" not in {check["id"] for check in res["bilingual"]["checks"]}


def test_no_bilingual_section_by_default(tmp_path: Path):
    res = _analyze(tmp_path, _tex(GOOD_ABSTRACT))
    assert res["bilingual"] is None
