"""正文方法+实验章（第3章起）逐章检查测试。

文件分区：

- experiment 区：analyze_experiment.py 的 R4a 结构提示与 R4b `--per-chapter` E-* 检查族。
- logic 区：analyze_logic.py 的 R2d（方法论论证误报）、R2e（章式预判双信号）、R3a（P-PAPER
  泛化默认全章）、R4c（--first-chapter）、R5（缺承上分级）。

针对 latex-thesis-zh 的脚本副本，经 importlib 按路径加载。
fixture 为合成脱敏样本（通用流程工业），保留问题模式、替换领域内容，不用用户论文原文。
"""

import importlib.util
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH

_ZH_DIR = SCRIPT_DIR_ZH
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load_zh(name: str):
    """Canonical isolated path-loader (see test_process_chapter.py)."""
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


experiment = _load_zh("analyze_experiment")


def _run(tmp_path: Path, tex: str, **kwargs) -> str:
    f = tmp_path / "main.tex"
    f.write_text(tex, encoding="utf-8")
    return "\n".join(experiment.analyze(f, **kwargs))


_INTRO = "\\chapter{绪论}\n本章介绍研究背景与问题。\n"
_TAIL = "\\chapter{总结与展望}\n全文总结，未来工作有待推进，具有应用价值。\n"

# 病例方法章：实验节无数据描述/无图表引用/无归因/无参数；框架节无图；无消融；无第2章回指。
# 触发全部 8 项 E-*。
_SICK = (
    "\\chapter{基于GA的某对象预测方法}\n"
    "\\section{引言}\n"
    "本章提出一种预测方法。\n"
    "\\section{总体框架}\n"
    "本节给出总体结构，后续逐步展开各部分内容。\n"
    "\\section{仿真实验}\n"
    "本节展示实验，RMSE 为 0.12，MAE 为 0.08，整体结果较好，数值如上所示。\n"
    "第二段继续报数字，误差更小，性能不错。\n"
    "第三段仍在报数字，效果提升明显。\n"
    "\\section{本章小结}\n"
    "本章提出了方法并验证。\n"
)

# 规范方法章：含教科书基础理论节（无图，须不触发 E-FIG）+ 框架节（有图）+ 规范实验节。
# 零 E-*（含 E-ABL/E-ECHO）。
_COMPLIANT = (
    "\\chapter{基于PSO的某对象优化模型}\n"
    "\\section{引言}\n"
    "本章将第2章的预测模型作为适应度函数，与第2章总体框架呼应。\n"
    "\\section{LSTM基础理论}\n"
    "本节介绍长短期记忆网络的基本原理，属通用理论。指标定义见式\\eqref{eq:rmse}：\n"
    "\\begin{equation}\\label{eq:rmse}\n"
    "\\mathrm{RMSE}=\\sqrt{\\tfrac{1}{n}\\sum e^2}\n"
    "\\end{equation}\n"
    "\\section{优化策略设计}\n"
    "优化策略如图\\ref{fig:frame}所示，包含三个模块。\n"
    "\\section{案例研究与结果分析}\n"
    "数据来自某厂装置，训练集与测试集按 8:2 划分，如表\\ref{tab:res}与图\\ref{fig:cur}所示。\n"
    "RMSE 降低明显，这是因为优化策略增强了全局搜索能力，其原因在于种群多样性提升。\n"
    "参数设置见表\\ref{tab:param}，对比方法包含人工经验操作作为基线。\n"
    "消融实验表明各模块均有效，去除任一模块性能均下降。\n"
    "\\section{本章小结}\n"
    "本章提出优化模型。\n"
)

# 并列方法章（红线）：整体规范，但独立立论、全章无第2章回指、所有 \\ref 目标均本章内定义。
# 仅应产出 E-ECHO Info，零 Major/Minor（锁定：无显著性检验/无均值±方差/人工经验基线均不误报）。
_PARALLEL = (
    "\\chapter{基于DE的某对象控制策略}\n"
    "\\section{引言}\n"
    "本章面向控制问题独立立论，提出一种控制策略。\n"
    "\\section{总体结构设计}\n"
    "总体结构如图\\ref{fig:arch}所示。\n"
    "\\begin{figure}\\label{fig:arch}\\end{figure}\n"
    "\\section{仿真实验与结果分析}\n"
    "数据来自某装置，训练与测试按 7:3 划分，如表\\ref{tab:r}与图\\ref{fig:c}所示。\n"
    "\\begin{table}\\label{tab:r}\\end{table}\\begin{figure}\\label{fig:c}\\end{figure}\n"
    "ISE 下降明显，这是因为控制策略提升了稳定性，其原因在于抑制了超调。\n"
    "参数设置见表，对比包含人工经验操作。指标定义见式：\n"
    "\\begin{equation}\\label{eq:ise}E=\\int e^2\\end{equation}\n"
    "消融实验表明各环节均有效。\n"
    "\\section{本章小结}\n本章提出控制策略。\n"
)

# 无独立讨论/综述章、无结论：默认模式应出 R4a 结构提示、不再假绿。
_NO_DISCUSSION = (
    "\\chapter{绪论}\n研究背景。\n"
    "\\chapter{基于X的方法}\n"
    "\\section{仿真实验}\n数据来自某厂，训练测试 8:2 划分。\n"
)

# 有独立讨论章+综述章：默认模式不应出 R4a 提示（门控回归）。
_WITH_DISCUSSION = (
    "\\chapter{绪论}\n研究背景。\n"
    "\\chapter{相关工作}\n已有研究综述。\n"
    "\\chapter{讨论}\n"
    "本文方法有效，这是因为机制清晰。\n相较于已有研究提升明显。\n仍存在一定局限。\n"
)

# 行号定位样本（人工计数）：\\chapter 行3、\\section{总体框架} 行4、\\section{实验} 行6。
_LINES = (
    "\\chapter{绪论}\n"  # 1
    "背景介绍。\n"  # 2
    "\\chapter{基于X的方法}\n"  # 3
    "\\section{总体框架}\n"  # 4
    "本节给出结构，逐步展开各部分。\n"  # 5
    "\\section{实验}\n"  # 6
    "报数字，结果好，数值如上，再报一行。\n"  # 7
    "\\chapter{总结}\n"  # 8
    "全文总结。\n"  # 9
)


# ── 加载守卫 ──────────────────────────────────────────────────


def test_loads_zh_copy_with_per_chapter_family() -> None:
    # zh 副本独有 R4b 逐章检查；EN 副本无此符号，守卫防止静默退化。
    assert hasattr(experiment, "_check_per_chapter")
    assert hasattr(experiment, "EXP_SEC_RE")
    assert hasattr(experiment, "FRAMEWORK_SEC_RE")


# ── R4b：问题方法章触发全部 E-*（各≥1） ───────────────────────


def test_sick_chapter_triggers_all_eight_checks(tmp_path: Path) -> None:
    report = _run(tmp_path, _INTRO + _SICK + _TAIL, per_chapter=True)
    for code in ("E-DATA", "E-ATTR", "E-REF", "E-FIG", "E-METRIC", "E-PARAM", "E-ABL", "E-ECHO"):
        assert code in report, f"{code} 应命中\n{report}"
    # severity 分级抽查。
    assert "[Severity: Major] [Priority: P1]: [Script] E-DATA" in report
    assert "[Severity: Minor] [Priority: P2]: [Script] E-METRIC" in report
    assert "[Severity: Info] [Priority: P3]: [Script] E-ABL" in report
    # 全部 [Script] 标注。
    assert "[LLM]" not in report


# ── R4b：规范方法章零 E-*（负例） ────────────────────────────


def test_compliant_chapter_no_findings(tmp_path: Path) -> None:
    report = _run(tmp_path, _INTRO + _COMPLIANT + _TAIL, per_chapter=True)
    assert "E-" not in report, f"规范方法章不应产出任何 E-*\n{report}"
    assert "No per-chapter experiment issues detected" in report


def test_textbook_theory_section_does_not_trigger_efig(tmp_path: Path) -> None:
    # _COMPLIANT 含无图的 "LSTM基础理论" 节与有图的 "优化策略设计" 节：
    # E-FIG 只对框架/结构/策略/方案命名节要求图，教科书理论节豁免。
    report = _run(tmp_path, _INTRO + _COMPLIANT + _TAIL, per_chapter=True)
    assert "E-FIG" not in report


# ── R4b 防误报红线：并列章仅 E-ECHO Info ─────────────────────


def test_parallel_chapter_reports_only_echo_info(tmp_path: Path) -> None:
    report = _run(tmp_path, _INTRO + _PARALLEL + _TAIL, per_chapter=True)
    # 无第2章回指且所有 \\ref 目标本章内定义 → E-ECHO Info。
    assert "[Severity: Info] [Priority: P3]: [Script] E-ECHO" in report
    # 红线：无显著性检验/无均值±方差/人工经验基线 → 不得报任何 Major/Minor。
    for code in ("E-DATA", "E-ATTR", "E-REF", "E-FIG", "E-METRIC", "E-PARAM"):
        assert code not in report, f"{code} 不应在规范并列章命中\n{report}"
    assert "[Severity: Major]" not in report
    assert "[Severity: Minor]" not in report


# ── R4b：多章逐章产出且行号定位正确 ──────────────────────────


def test_per_chapter_line_numbers(tmp_path: Path) -> None:
    report = _run(tmp_path, _LINES, per_chapter=True)
    # E-FIG 指向框架节首行（行4），E-DATA 指向实验节首行（行6），
    # 章级 E-ECHO/E-ABL 指向章首行（行3）。
    assert "(Line 4) [Severity: Major] [Priority: P1]: [Script] E-FIG" in report
    assert "(Line 6) [Severity: Major] [Priority: P1]: [Script] E-DATA" in report
    assert "(Line 3) [Severity: Info] [Priority: P3]: [Script] E-ECHO" in report


def test_per_chapter_multi_chapter_isolates_findings(tmp_path: Path) -> None:
    # 三方法章拼接：问题章全触发、规范章静默、并列章仅 E-ECHO —— 逐章隔离，不串扰。
    report = _run(tmp_path, _INTRO + _SICK + _COMPLIANT + _PARALLEL + _TAIL, per_chapter=True)
    assert report.count("E-DATA") == 1  # 仅 _SICK
    assert report.count("E-FIG") == 1  # 仅 _SICK 框架节无图
    assert report.count("E-ECHO") == 2  # _SICK + _PARALLEL 均无第2章回指


# ── R4a：无讨论/综述章 → 结构提示消假绿 ──────────────────────


def test_r4a_structure_hint_replaces_false_green(tmp_path: Path) -> None:
    report = _run(tmp_path, _NO_DISCUSSION)
    assert "结构提示" in report and "--per-chapter" in report
    assert "[Severity: Info]" in report
    # 关键：不再静默输出假绿。
    assert "No discussion/conclusion issues detected" not in report


def test_r4a_hint_fires_when_only_related_missing(tmp_path: Path) -> None:
    # split_sections 会把含"分析/讨论"的章标题误判为 discussion 键；related 缺失
    # （综述写在绪论）才是逐章实验结构的可靠信号，此时仍须提示、不得假绿。
    tex = (
        "\\chapter{绪论}\n研究背景与文献综述。\n"
        "\\chapter{某系统工艺分析与问题描述}\n本章分析工艺。\n"
        "\\section{结果分析}\n这是因为机制清晰，原因在于此。分析若干。数据说明。\n"
    )
    report = _run(tmp_path, tex)
    assert "结构提示" in report
    assert "No discussion/conclusion issues detected" not in report


def test_r4a_hint_absent_when_discussion_and_related_present(tmp_path: Path) -> None:
    report = _run(tmp_path, _WITH_DISCUSSION)
    assert "结构提示" not in report


# ── 默认零变化：E-* 全部藏在 --per-chapter 后 ────────────────


def test_e_checks_gated_behind_flag(tmp_path: Path) -> None:
    report = _run(tmp_path, _INTRO + _SICK + _TAIL)  # 默认模式
    for code in ("E-DATA", "E-ATTR", "E-REF", "E-FIG", "E-METRIC", "E-PARAM", "E-ABL", "E-ECHO"):
        assert code not in report, f"{code} 不得在默认模式出现\n{report}"


# ══════════════════════════════════════════════════════════════
# logic 区：analyze_logic.py 的 R2d / R2e / R3a / R4c / R5 用例。
# ══════════════════════════════════════════════════════════════

logic = _load_zh("analyze_logic")


def _run_logic(tmp_path: Path, tex: str, **kwargs) -> str:
    f = tmp_path / "logic.tex"
    f.write_text(tex, encoding="utf-8")
    return "\n".join(logic.analyze(f, **kwargs))


# ── R2d：术语定义/分级口径不报方法论论证缺失 ──────────────────


def test_r2d_term_definition_not_flagged(tmp_path: Path) -> None:
    # “本文采用…证据等级”是术语分级定义、非方法选择，不报方法论论证缺失。
    tex = (
        _INTRO
        + "\\chapter{某对象预测方法}\n"
        + "本文采用离线测试、影子调度与现场投用三类证据构成四级证据等级。\n"
        + _TAIL
    )
    report = _run_logic(tmp_path, tex)
    assert "方法选择缺乏论证" not in report


def test_r2d_bare_method_choice_still_flagged(tmp_path: Path) -> None:
    # 无理由、无定义口径的“本文采用X方法”仍应报（R2d 不误伤正例）。
    tex = _INTRO + "\\chapter{某对象预测方法}\n本文采用一种深度神经网络进行建模。\n" + _TAIL
    report = _run_logic(tmp_path, tex)
    assert "方法选择缺乏论证" in report


# ── R2e：方法章 --process-chapter 只出 Info、不套 P-* ──────────


def test_r2e_method_chapter_not_treated_as_process(tmp_path: Path) -> None:
    # 方法章含“问题描述/总体框架”节（旧宽判据会命中），但章/节标题无过程信号
    # （工艺/流程/过程分析/变量分析）→ 双信号只出 Info，不套 P-DERIVE/P-FRAME/P-ORDER。
    tex = (
        _INTRO
        + "\\chapter{基于GA的某对象预测方法}\n"
        + "\\section{问题描述}\n本章描述预测问题的边界与目标。\n"
        + "\\section{总体框架}\n框架如图\\ref{fig:f}所示，含预测模型与优化策略。\n"
        + "\\section{仿真实验}\n实验验证方法有效性。\n"
        + _TAIL
    )
    report = _run_logic(tmp_path, tex, process_chapter=True)
    assert "未见过程分析章特征" in report
    for marker in ("P-DERIVE", "P-FRAME", "P-ORDER"):
        assert marker not in report, f"{marker} 不应在方法章命中\n{report}"


# ── R3a：P-PAPER 默认全章、逐处报全部命中 ─────────────────────


def test_r3a_paper_stitching_reports_all_hits(tmp_path: Path) -> None:
    # 默认模式（无 flag）扫全部正文行，每处“源论文/小论文/N篇论文”单独一条。
    tex = (
        _INTRO
        + "\\chapter{基于GA的方法}\n"
        + "源论文一的核心问题是预测精度。\n"
        + "\\section{建模}\n第二篇源论文对应优化问题。\n"
        + "\\section{实验}\n三篇论文的方法在此统一验证。\n"
        + _TAIL
    )
    report = _run_logic(tmp_path, tex)
    assert report.count("P-PAPER") == 3, f"应报 3 处 P-PAPER\n{report}"
    assert "[Severity: Minor] [Priority: P2]: [Script] P-PAPER" in report


def test_r3a_paper_stitching_absent_when_clean(tmp_path: Path) -> None:
    tex = _INTRO + "\\chapter{基于GA的方法}\n本章围绕核心问题展开研究内容。\n" + _TAIL
    report = _run_logic(tmp_path, tex)
    assert "P-PAPER" not in report


# ── R4c：--first-chapter 使单章文件承上检查生效 ───────────────


def test_r4c_first_chapter_enables_cheng_check(tmp_path: Path) -> None:
    # 单章文件：首个 \chapter 即第 3 章方法章，引言无承接、章内复用第 2 章成果。
    tex = (
        "\\chapter{基于GA的某对象控制方法}\n\\section{引言}\n"
        "本章面向某对象的约束控制问题，设计一种新的控制方法。"
        "首先给出被控对象模型，然后设计滚动优化控制器，最后通过仿真验证有效性。\n"
        "\\section{方法框架}\n本节将第2章建立的预测模型作为约束条件。\n"
    )
    # 缺省：首个正文章被当第 2 章特判，不查承上。
    assert "缺少承上" not in _run_logic(tmp_path, tex)
    # --first-chapter 3：真实第 3 章，承上缺失被检出（章内有第 2 章依赖线索 → Major）。
    report = _run_logic(tmp_path, tex, first_chapter=3)
    assert "章引言缺少承上" in report


# ── R5：缺承上分级（依赖章维持 Major / 并列章降 Info）─────────


def _two_body_chapters(third_intro: str, third_body: str) -> str:
    """绪论 + 第 2 章（过程分析，编号引言）+ 第 3 章（方法章，可配引言/正文）。"""
    return (
        _INTRO
        + "\\chapter{某对象过程分析}\n\\section{引言}\n"
        + "本章承接绪论，围绕过程展开。首先介绍流程，然后分析难点，最后给出框架。\n"
        + "\\section{流程}\n流程内容若干，交代清楚。\n"
        + f"\\chapter{{基于GA的某对象优化方法}}\n\\section{{引言}}\n{third_intro}\n"
        + f"\\section{{方法框架}}\n{third_body}\n"
        + _TAIL
    )


def test_r5_dependency_chapter_keeps_major(tmp_path: Path) -> None:
    # 第 3 章引言无承上，但章内复用“第2章”成果（依赖线索）→ 维持 Major。
    tex = _two_body_chapters(
        "本章设计一种优化方法。首先给出模型，然后设计算法，最后仿真验证有效性。",
        "本节将第2章的预测模型作为适应度函数。",
    )
    report = _run_logic(tmp_path, tex)
    assert "第“基于GA的某对象优化方法”章章引言缺少承上" in report


def test_r5_parallel_chapter_downgrades_to_info(tmp_path: Path) -> None:
    # 第 3 章引言无承上、章内亦无“第X章”依赖线索（纯并列）→ 降 Info，不报 Major 承上。
    tex = _two_body_chapters(
        "本章面向优化问题独立立论，设计一种优化方法。首先给出模型，然后设计算法，最后仿真验证。",
        "本节给出优化方法的模块组成与数据流。",
    )
    report = _run_logic(tmp_path, tex)
    assert "第“基于GA的某对象优化方法”章章引言缺少承上" not in report
    assert "并列方法章可不承上" in report
