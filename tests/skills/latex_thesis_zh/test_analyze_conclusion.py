"""CC-* 结论章内容检查（analyze_conclusion.py）正反例。

针对 latex-thesis-zh 的 analyze_conclusion.py 副本，经 importlib 按路径隔离加载
（SCRIPT_DIR_ZH 不在默认 sys.path，裸 import 会误解析到 EN/AUDIT 副本）。

fixture 为合成脱敏样本（通用过程工业措辞），保留问题模式、替换领域内容，
不使用用户论文原文。
"""

import importlib.util
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH

_ZH_DIR = SCRIPT_DIR_ZH
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load_zh(name: str):
    """Canonical isolated path-loader（见 test_process_chapter.py）。"""
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


mod = _load_zh("analyze_conclusion")


# ── fixture 片段 ─────────────────────────────────────────────

_ABSTRACT = (
    "\\begin{cabstract}\n"
    "本文研究某工业过程的智能建模与优化控制。针对复杂工况下建模难的关键问题，"
    "提出了一种融合方法并加以验证。实验结果表明所提方法有效。\n"
    "\\end{cabstract}\n"
)
_INTRO = "\\chapter{绪论}\n本章介绍研究背景。行业需求增长明显，技术挑战突出。\n"
_BODY = "\\chapter{预测建模方法}\n本文建立预测模型并在生产数据上验证其性能。\n"


def _doc(concl: str, *, abstract: str = _ABSTRACT, body: str = _BODY) -> str:
    return abstract + _INTRO + body + concl


def _analyze(tmp_path: Path, tex: str):
    f = tmp_path / "main.tex"
    f.write_text(tex, encoding="utf-8")
    return mod.ConclusionAnalyzer(str(f)).analyze()


def _codes(result) -> set[str]:
    return {f.code for f in result.findings}


def _by_code(result, code: str) -> list:
    return [f for f in result.findings if f.code == code]


# 合规结论章：三段式齐全、承上序词、3 条贡献、承接过渡、2 条具体展望。
_CONCL_OK = (
    "\\chapter{总结与展望}\n"
    "本文围绕某过程的建模与控制问题展开研究。首先分析工艺流程，其次建立预测模型，"
    "然后设计优化策略，最后进行工业验证。本文主要创新性工作如下：\n"
    "（1）针对高维数据不平衡问题，提出了数据增强方法，实验表明预测精度显著提升。\n"
    "（2）针对多工况切换问题，建立了工况识别模型，验证了有效性。\n"
    "（3）针对能耗优化问题，设计了优化控制策略，现场应用表明节能效果明显。\n"
    "然而，所提方法在更复杂工况下的泛化能力仍存在一定不足。\n"
    "未来研究可从以下方面进一步深入。\n"
    "（1）研究多尺度数据融合的建模方法，提升模型鲁棒性。\n"
    "（2）开展工程部署研究，将算法部署到工业控制系统。\n"
)


# ── 加载守卫 ─────────────────────────────────────────────────


def test_loads_the_zh_copy() -> None:
    assert hasattr(mod, "ConclusionAnalyzer")
    assert hasattr(mod, "Finding")
    assert hasattr(mod, "OUTLOOK_EMPTY_BLACKLIST")
    # 黑名单落在 8~15 条区间。
    assert 8 <= len(mod.OUTLOOK_EMPTY_BLACKLIST) <= 15


# ── 合规样本：无 Error/Warning ────────────────────────────────


def test_compliant_no_error_or_warning(tmp_path: Path) -> None:
    result = _analyze(tmp_path, _doc(_CONCL_OK))
    assert result.status in ("PASS", "INFO"), [f.code for f in result.findings]
    sevs = {f.severity for f in result.findings}
    assert "Error" not in sevs
    assert "Warning" not in sevs
    # 三段齐全 -> 无 CC-TRIAD；承上足量 -> 无 CC-OPEN。
    assert "CC-TRIAD" not in _codes(result)
    assert "CC-OPEN" not in _codes(result)


def test_llm_lane_always_present(tmp_path: Path) -> None:
    result = _analyze(tmp_path, _doc(_CONCL_OK))
    lane = {h.code for h in result.llm_lane}
    assert lane == {"CC-SKELETON", "CC-NEW-CONCEPT"}


# ── CC-TRIAD ─────────────────────────────────────────────────


def test_triad_missing_outlook_is_error(tmp_path: Path) -> None:
    concl = (
        "\\chapter{结论}\n"
        "本文针对某问题展开研究。本文主要创新性工作如下：\n"
        "（1）提出了一种方法，实验表明有效。\n"
        "（2）建立了一个模型，验证了性能。\n"
        "（3）设计了一种策略，应用表明可行。\n"
    )
    result = _analyze(tmp_path, _doc(concl))
    triad = _by_code(result, "CC-TRIAD")
    assert any(f.severity == "Error" and "展望" in f.message for f in triad)
    assert result.status == "FAIL"


def test_triad_missing_innovation_is_warning(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "本文针对某问题展开研究。所取得的成果总结如下：\n"
        "（1）提出了一种处理方案，实验表明有效。\n"
        "（2）建立了一个识别模型，验证了性能。\n"
        "（3）给出了一种调控方案，应用表明可行。\n"
        "仍存在一些不足。未来研究可进一步深入优化建模方法。\n"
    )
    result = _analyze(tmp_path, _doc(concl))
    triad = _by_code(result, "CC-TRIAD")
    assert any(f.severity == "Warning" and "创新" in f.message for f in triad)
    # 缺创新只 Warning，不应有 Error。
    assert "Error" not in {f.severity for f in result.findings}


# ── CC-OPEN ──────────────────────────────────────────────────


def test_open_few_ordinals_is_info(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "本文开展了系统研究工作。本文主要创新性工作如下：\n"
        "（1）提出创新方法A，实验有效。\n"
        "（2）建立模型B，验证性能。\n"
        "（3）设计策略C，应用可行。\n"
        "仍存在不足。未来研究可深入优化控制算法。\n"
    )
    result = _analyze(tmp_path, _doc(concl))
    opens = _by_code(result, "CC-OPEN")
    assert opens and opens[0].severity == "Info"


# ── CC-ENUM ──────────────────────────────────────────────────


def test_enum_five_items_is_info(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "本文开展研究。首先分析，其次建模。本文主要创新性工作如下：\n"
        "（1）提出创新方法A。\n（2）方法B。\n（3）方法C。\n（4）方法D。\n（5）方法E。\n"
        "仍存在不足。未来研究可深入优化建模方法。\n"
    )
    result = _analyze(tmp_path, _doc(concl))
    enums = _by_code(result, "CC-ENUM")
    assert enums and "5" in enums[0].message


def test_enum_three_items_silent(tmp_path: Path) -> None:
    result = _analyze(tmp_path, _doc(_CONCL_OK))
    assert "CC-ENUM" not in _codes(result)


# ── CC-OUTLOOK-EMPTY ─────────────────────────────────────────


def test_outlook_empty_boilerplate_is_warning(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "本文开展研究。首先分析，其次建模。本文主要创新性工作如下：\n"
        "（1）提出创新方法A，实验有效。\n（2）建立模型B，验证性能。\n（3）设计策略C，应用可行。\n"
        "仍存在不足。展望未来，本领域前景广阔，值得进一步研究。\n"
    )
    result = _analyze(tmp_path, _doc(concl))
    empty = _by_code(result, "CC-OUTLOOK-EMPTY")
    assert any(f.severity == "Warning" for f in empty)


def test_outlook_concrete_not_flagged_empty(tmp_path: Path) -> None:
    # 合规展望条含具体技术名词（建模/部署）-> 不判空话。
    result = _analyze(tmp_path, _doc(_CONCL_OK))
    warns = [f for f in _by_code(result, "CC-OUTLOOK-EMPTY") if f.severity == "Warning"]
    assert not warns


# ── CC-OUTLOOK-TRANS ─────────────────────────────────────────


def test_outlook_missing_transition_is_info(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "本文开展研究。首先分析，其次建模。本文主要创新性工作如下：\n"
        "（1）提出创新方法A，实验有效。\n（2）建立模型B，验证性能。\n（3）设计策略C，应用可行。\n"
        "未来研究可深入优化建模方法与控制算法。\n"
    )
    result = _analyze(tmp_path, _doc(concl))
    trans = _by_code(result, "CC-OUTLOOK-TRANS")
    assert trans and trans[0].severity == "Info"


def test_outlook_with_transition_silent(tmp_path: Path) -> None:
    result = _analyze(tmp_path, _doc(_CONCL_OK))
    assert "CC-OUTLOOK-TRANS" not in _codes(result)


# ── CC-OUTLOOK-COUNT ─────────────────────────────────────────


def test_outlook_count_five_is_info(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "本文开展研究。首先分析，其次建模。本文主要创新性工作如下：\n"
        "（1）提出创新方法A，实验有效。\n（2）建立模型B，验证性能。\n（3）设计策略C，应用可行。\n"
        "仍存在不足。未来研究方向如下。\n"
        "（1）研究建模方法一。\n（2）研究优化方法二。\n（3）研究控制方法三。\n"
        "（4）研究部署方法四。\n（5）研究调度方法五。\n"
    )
    result = _analyze(tmp_path, _doc(concl))
    counts = _by_code(result, "CC-OUTLOOK-COUNT")
    assert counts and "5" in counts[0].message


# ── CC-VERBATIM ──────────────────────────────────────────────

_ABS_V = (
    "\\begin{cabstract}\n"
    "本文针对复杂工业过程建模精度不足的关键问题展开深入研究。"
    "提出了一种融合机理与数据的智能建模方法并加以充分验证。"
    "实验结果表明所提方法显著提升了预测精度与鲁棒性能。\n"
    "\\end{cabstract}\n"
)
_OWN1 = "本文围绕多工况切换场景设计了在线工况识别与自适应调度算法。"
_OWN2 = "现场应用结果显示该系统在实际生产线上取得了显著的节能降耗效果。"
_OWN3 = "本文构建了面向工业部署的软件平台并完成了长期稳定性测试验证。"
_TAIL_V = (
    "本文主要创新性工作如下：\n"
    "（1）提出创新方法。\n（2）建立模型。\n（3）设计策略。\n"
    "仍存在不足。未来研究可深入优化建模方法。\n"
)


def test_verbatim_exact_copies_warns(tmp_path: Path) -> None:
    # 2 句照抄摘要 + 1 句自有长句 -> 命中占比 2/3 ≥30% -> Warning。
    concl = (
        "\\chapter{总结与展望}\n"
        "本文针对复杂工业过程建模精度不足的关键问题展开深入研究。\n"
        "提出了一种融合机理与数据的智能建模方法并加以充分验证。\n" + _OWN1 + "\n" + _TAIL_V
    )
    result = _analyze(tmp_path, _doc(concl, abstract=_ABS_V))
    vb = _by_code(result, "CC-VERBATIM")
    assert any(f.severity == "Warning" for f in vb)
    # 单句命中列 Info 明细。
    assert any(f.severity == "Info" for f in vb)


def test_verbatim_below_share_info_only(tmp_path: Path) -> None:
    # 1 句照抄 + 3 句自有长句 -> 命中占比 1/4 <30% -> 无 Warning，仅 Info 明细。
    concl = (
        "\\chapter{总结与展望}\n"
        "本文针对复杂工业过程建模精度不足的关键问题展开深入研究。\n"
        + _OWN1
        + "\n"
        + _OWN2
        + "\n"
        + _OWN3
        + "\n"
        + _TAIL_V
    )
    result = _analyze(tmp_path, _doc(concl, abstract=_ABS_V))
    vb = _by_code(result, "CC-VERBATIM")
    assert vb, "应至少列出单句命中明细"
    assert all(f.severity != "Warning" for f in vb)
    assert any(f.severity == "Info" for f in vb)


def test_verbatim_near_copy_hits(tmp_path: Path) -> None:
    # 近似复制（个别字改动）应仍被 0.85 阈值捕获。
    concl = (
        "\\chapter{总结与展望}\n"
        "本文针对复杂工业过程建模精度不足的关键问题展开系统研究。\n"  # 深入->系统
        "提出了一种融合机理与数据的智能建模方法并加以有效验证。\n"  # 充分->有效
        + _OWN1
        + "\n"
        + _TAIL_V
    )
    result = _analyze(tmp_path, _doc(concl, abstract=_ABS_V))
    vb = _by_code(result, "CC-VERBATIM")
    assert any(f.severity == "Warning" for f in vb)


def test_verbatim_paraphrase_no_hit(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "围绕工业过程里的种种建模难题，本文尝试了不少与以往颇为不同的探索路子。\n"
        + _OWN1
        + "\n"
        + _OWN2
        + "\n"
        + _TAIL_V
    )
    result = _analyze(tmp_path, _doc(concl, abstract=_ABS_V))
    assert "CC-VERBATIM" not in _codes(result)


# ── CC-QUANT ─────────────────────────────────────────────────

_BODY_Q = "\\chapter{预测建模方法}\n本文建立预测模型，精度达到 0.95 ，能耗下降 3.46 。\n"


def test_quant_value_absent_from_body_notes(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "本文开展研究。首先分析，其次建模。本文主要创新性工作如下：\n"
        "（1）提出方法，预测精度达到 0.97 。\n（2）建立模型。\n（3）设计策略。\n"
        "仍存在不足。未来研究可深入优化建模方法。\n"
    )
    result = _analyze(tmp_path, _doc(concl, body=_BODY_Q))
    assert any("0.97" in n for n in result.quant_notes)


def test_quant_value_present_no_note(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "本文开展研究。首先分析，其次建模。本文主要创新性工作如下：\n"
        "（1）提出方法，预测精度达到 0.95 。\n（2）建立模型，能耗下降 3.46 。\n（3）设计策略。\n"
        "仍存在不足。未来研究可深入优化建模方法。\n"
    )
    result = _analyze(tmp_path, _doc(concl, body=_BODY_Q))
    assert result.quant_notes == []


def test_quant_no_numbers_silent(tmp_path: Path) -> None:
    result = _analyze(tmp_path, _doc(_CONCL_OK))
    assert result.quant_notes == []


# ── CC-NO-FIG ────────────────────────────────────────────────


def test_no_fig_environment_is_error(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "本文开展研究。首先分析，其次建模。本文主要创新性工作如下：\n"
        "（1）提出创新方法A。\n（2）建立模型B。\n（3）设计策略C。\n"
        "\\begin{figure}\n\\centering\n\\includegraphics{x}\n\\end{figure}\n"
        "仍存在不足。未来研究可深入优化建模方法。\n"
    )
    result = _analyze(tmp_path, _doc(concl))
    figs = _by_code(result, "CC-NO-FIG")
    assert figs and figs[0].severity == "Error"


def test_no_fig_clean_silent(tmp_path: Path) -> None:
    result = _analyze(tmp_path, _doc(_CONCL_OK))
    assert "CC-NO-FIG" not in _codes(result)


# ── CC-RATIO ─────────────────────────────────────────────────


def test_ratio_out_of_range_is_info(tmp_path: Path) -> None:
    # 总结极短、展望极长 -> 比值 <1.5 -> Info。
    concl = (
        "\\chapter{总结与展望}\n"
        "本文主要创新性工作如下：（1）提出创新方法A。\n"
        "仍存在不足。未来研究方向如下，需长期深入推进各项工作。\n"
        "（1）研究多尺度数据融合建模方法以提升模型在复杂工况下的鲁棒性与泛化能力。\n"
        "（2）开展面向工业现场的工程部署研究，将算法集成到工业控制系统并长期测试。\n"
        "（3）研究在线自适应优化调度方法以进一步降低生产过程的综合能耗与运行成本。\n"
    )
    result = _analyze(tmp_path, _doc(concl))
    ratios = _by_code(result, "CC-RATIO")
    assert ratios and ratios[0].severity == "Info"


# ── CC-SUBSEC ────────────────────────────────────────────────


def test_subsec_numbered_style_is_info(tmp_path: Path) -> None:
    concl = (
        "\\chapter{总结与展望}\n"
        "\\section{总结}\n"
        "本文开展研究。首先分析，其次建模。本文主要创新性工作如下：\n"
        "（1）提出创新方法A。\n（2）建立模型B。\n（3）设计策略C。\n"
        "\\section{展望}\n"
        "仍存在不足。未来研究可深入优化建模方法。研究方向如下。\n"
        "（1）研究建模方法。\n（2）研究部署方法。\n"
    )
    result = _analyze(tmp_path, _doc(concl))
    sub = _by_code(result, "CC-SUBSEC")
    assert sub and sub[0].severity == "Info"


def test_subsec_flat_style_silent(tmp_path: Path) -> None:
    result = _analyze(tmp_path, _doc(_CONCL_OK))
    assert "CC-SUBSEC" not in _codes(result)


# ── 多文件 \include 工程 ─────────────────────────────────────


def test_multifile_include_project(tmp_path: Path) -> None:
    (tmp_path / "abstract.tex").write_text(_ABSTRACT, encoding="utf-8")
    (tmp_path / "intro.tex").write_text(_INTRO, encoding="utf-8")
    concl = (
        "\\chapter{结论}\n"
        "本文针对某问题展开研究。本文主要创新性工作如下：\n"
        "（1）提出了一种方法，实验表明有效。\n"
        "（2）建立了一个模型，验证了性能。\n"
        "（3）设计了一种策略，应用表明可行。\n"
    )
    (tmp_path / "concl.tex").write_text(concl, encoding="utf-8")
    main = tmp_path / "main.tex"
    main.write_text(
        "\\documentclass{book}\n\\input{abstract}\n\\input{intro}\n\\input{concl}\n",
        encoding="utf-8",
    )
    result = mod.ConclusionAnalyzer(str(main)).analyze()
    assert result.conclusion is not None
    # 多文件定位标签指向源文件。
    assert "concl.tex" in result.conclusion["loc"]
    # 缺展望 -> CC-TRIAD Error，且定位到 concl.tex。
    triad = _by_code(result, "CC-TRIAD")
    assert any(f.severity == "Error" and "concl.tex" in f.loc for f in triad)


# ── 无结论章 SKIP ────────────────────────────────────────────


def test_no_conclusion_skips(tmp_path: Path) -> None:
    tex = _ABSTRACT + _INTRO + _BODY
    result = _analyze(tmp_path, tex)
    assert result.status == "SKIP"
    assert result.conclusion is None
    assert not result.findings


def test_missing_file_errors(tmp_path: Path) -> None:
    result = mod.ConclusionAnalyzer(str(tmp_path / "nope.tex")).analyze()
    assert result.status == "ERROR"
