"""正文方法+实验章（第3章起）逐章检查测试。

文件分区（后续 logic 侧代理会在 logic 区追加 P-PAPER 泛化 / F-PLACEHOLDER /
--first-chapter 等用例）：

- experiment 区（本文件当前内容）：analyze_experiment.py 的 R4a 结构提示与 R4b
  `--per-chapter` E-* 检查族。
- logic 区（待追加）：analyze_logic.py 的拼接感/草稿态/章序相关用例。

针对 latex-thesis-zh 的 analyze_experiment.py 副本，经 importlib 按路径加载。
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
