"""R2 章引言形态适配：编号引言节形态 + 第 2 章承上特判 + 篇幅上限拆分。

针对 latex-thesis-zh 的 analyze_logic.py 副本。副本经 importlib 按路径加载——裸
``import analyze_logic`` 会解析到 latex-paper-en 副本（见 conftest），后者没有
``INTRO_SECTION_TITLES_ZH`` 等 zh 专有常量。

R2 改 ``_check_chapter_intro`` 与 ``_check_heading_leads``（S1 对编号引言形态的豁免）。
这里直接调用这两个函数以隔离验证承上/启下/篇幅判定与 S1 导语豁免，互不干扰。
"""

import importlib.util
import sys

from tests.support.paths import SCRIPT_DIR_ZH

_ZH_DIR = SCRIPT_DIR_ZH
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load_zh(name: str):
    """Canonical isolated path-loader (see test_intro_mainline.py)."""
    path = _ZH_DIR / f"{name}.py"
    saved_path = list(sys.path)
    saved_modules = {n: sys.modules.pop(n, None) for n in _SHARED_MODULE_NAMES}
    try:
        sys.path.insert(0, str(_ZH_DIR))
        spec = importlib.util.spec_from_file_location(f"zh_{name}", path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for n, mod in saved_modules.items():
            if mod is not None:
                sys.modules[n] = mod
            else:
                sys.modules.pop(n, None)


logic = _load_zh("analyze_logic")


def _intro_findings(tex: str) -> str:
    """直接调用 _check_chapter_intro，返回拼接后的诊断文本。"""
    logic._DOC = None
    parser = logic.get_parser("main.tex")
    return "\n".join(logic._check_chapter_intro(tex, tex.split("\n"), parser))


def _lead_findings(tex: str) -> str:
    """直接调用 _check_heading_leads（S1），返回拼接后的诊断文本。"""
    logic._DOC = None
    parser = logic.get_parser("main.tex")
    return "\n".join(logic._check_heading_leads(tex, tex.split("\n"), parser))


_PREAMBLE = (
    "\\chapter{绪论}\n本章介绍研究背景与待解决的问题。\n\\section{研究背景}\n该领域需求快速增长。\n"
)


def _numbered_ch2(intro_body: str, first_extra_section: str = "工艺流程分析") -> str:
    """绪论 + 第 2 章（编号引言节形态：章标题后直接 \\section{引言}）。"""
    return (
        _PREAMBLE
        + "\\chapter{某污水处理工艺流程分析}\n"
        + "\\section{引言}\n"
        + f"{intro_body}\n"
        + f"\\section{{{first_extra_section}}}\n工艺流程见图。\n"
    )


# ── 加载守卫 ──────────────────────────────────────────────────


def test_loads_the_zh_copy_not_the_en_copy() -> None:
    assert hasattr(logic, "_check_chapter_intro")
    assert hasattr(logic, "INTRO_SECTION_TITLES_ZH")
    assert hasattr(logic, "CHAPTER_INTRO_NUMBERED_MAX_CHARS")


# ── 编号引言节形态：第 2 章不再误报 ──────────────────────────


def test_numbered_intro_second_chapter_no_false_positive() -> None:
    """第 2 章编号引言节（承上启下概述式）不应报承上/启下缺失。"""
    body = (
        "本章围绕污水处理过程展开研究。首先介绍工艺流程，然后分析关键难点，"
        "接着建立统一数据契约，最后给出总体研究框架。"
    )
    report = _intro_findings(_numbered_ch2(body))
    assert "章引言缺少启下" not in report
    assert "章引言缺少承上" not in report
    assert "章引言过简" not in report


def test_numbered_intro_second_chapter_missing_qi_flagged() -> None:
    """第 2 章编号引言节若不预告各节，启下缺失应能从引言小节正文查出。"""
    body = "污水处理是重要的环保工艺过程，涉及预处理、生化反应与沉淀出水多个工序段以及众多关键运行变量。"
    report = _intro_findings(_numbered_ch2(body))
    assert "章引言缺少启下" in report
    # 第 2 章特判：仍不报承上。
    assert "章引言缺少承上" not in report


def test_numbered_intro_third_chapter_missing_cheng_flagged() -> None:
    """第 3 章编号引言节缺“第 X 章/承接”时，承上缺失应能从引言小节正文查出。"""
    tex = (
        _PREAMBLE
        + "\\chapter{某工艺流程分析}\n\\section{引言}\n"
        + "本章围绕工艺展开。首先介绍流程，然后分析难点，最后给出框架。\n"
        + "\\section{工艺流程}\n流程内容。\n"
        + "\\chapter{污水处理预测控制方法}\n\\section{引言}\n"
        + "本章设计预测控制方法。首先给出模型，然后设计控制器，最后验证效果。\n"
        + "\\section{方法框架}\n框架内容。\n"
    )
    report = _intro_findings(tex)
    # 第 3 章（非首个正文章）承上缺失被指出……
    assert "第“污水处理预测控制方法”章章引言缺少承上" in report
    # ……而第 2 章（首个正文章）承上仍豁免。
    assert "第“某工艺流程分析”章章引言缺少承上" not in report


# ── 编号引言节篇幅上限（1600）拆分 ───────────────────────────


def test_numbered_intro_over_limit_flagged() -> None:
    """编号引言节超 1600 字应报“编号引言节过长”。"""
    body = "本章围绕某过程展开研究。" * 150  # 约 1800 字，含 本章 + 展开（启下通过）
    report = _intro_findings(_numbered_ch2(body))
    assert "编号引言节过长" in report
    assert "章引言缺少启下" not in report


def test_numbered_intro_within_limit_passes() -> None:
    """编号引言节 900~1600 字（超章后导语上限、未超编号上限）不应报过长。"""
    body = "本章围绕某过程展开研究。" * 80  # 约 960 字
    report = _intro_findings(_numbered_ch2(body))
    assert "过长" not in report
    assert "过简" not in report


# ── 章后导语形态回归（锌冶炼式）──────────────────────────────


def test_lead_form_compliant_unchanged() -> None:
    """章后导语（不编号）承上启下齐全时，仍走原路径、零告警。"""
    tex = (
        _PREAMBLE
        + "\\chapter{锌冶炼工艺分析}\n"
        + "本章承接绪论背景，围绕湿法炼锌浸出工序展开。首先介绍工艺流程，然后分析难点，最后给出框架。\n"
        + "\\section{工艺流程}\n流程内容。\n"
    )
    report = _intro_findings(tex)
    assert "% 章引言" not in report


def test_lead_form_over_limit_uses_lead_wording() -> None:
    """章后导语超 900 字用“章引言过长”措辞，不套用编号引言节上限。"""
    long_lead = "本章围绕某过程展开研究。" * 80  # 约 960 字，作为章后导语（非编号引言节）
    tex = (
        _PREAMBLE
        + "\\chapter{某过程分析}\n"
        + f"{long_lead}\n"
        + "\\section{工艺流程}\n流程内容。\n"
    )
    report = _intro_findings(tex)
    assert "章引言过长" in report
    assert "编号引言节过长" not in report


# ── 两处“引言”角色区分 ───────────────────────────────────────


def test_chapter_titled_introduction_stays_exempt() -> None:
    """章标题为“引言”的整章仍整体豁免，不被当作编号引言节处理。"""
    tex = (
        "\\chapter{引言}\n本章介绍研究背景。\n\\section{背景}\n背景内容。\n"
        "\\chapter{方法设计}\n本章承接引言、围绕方法展开。本章组织如下：先框架再细节。\n"
        "\\section{总体框架}\n框架内容。\n"
    )
    report = _intro_findings(tex)
    assert "第“引言”章" not in report


# ── S1 导语检查对编号引言形态的豁免（_check_heading_leads）─────


def test_s1_skips_chapter_lead_flag_for_numbered_intro() -> None:
    """编号引言形态：S1 不对章标题报“未发现/缺少导语段落”（引言小节即本章导语）。"""
    tex = (
        _PREAMBLE
        + "\\chapter{某污水处理工艺流程分析}\n"
        + "\\section{引言}\n"
        + "本章围绕污水处理过程展开。首先介绍工艺流程，然后分析难点，最后给出框架。\n"
        + "\\section{工艺流程分析}\n工艺流程见图。\n"
    )
    report = _lead_findings(tex)
    assert "某污水处理工艺流程分析”后未发现导语段落" not in report
    assert "某污水处理工艺流程分析”后缺少导语段落" not in report


def test_s1_still_flags_normal_chapter_without_intro_section() -> None:
    """普通章（章标题后直接跳到非引言小节）S1 仍报“未发现导语段落”，防豁免过宽。"""
    tex = _PREAMBLE + "\\chapter{某方法设计}\n\\section{总体框架}\n本节给出总体框架。\n"
    report = _lead_findings(tex)
    assert "标题“某方法设计”后未发现导语段落" in report
