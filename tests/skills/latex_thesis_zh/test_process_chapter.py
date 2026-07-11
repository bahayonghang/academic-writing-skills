"""R3 过程分析章主线检查（--process-chapter：P-FLOW/P-DERIVE/P-FRAME/P-ORDER/P-PAPER）。

针对 latex-thesis-zh 的 analyze_logic.py 副本，经 importlib 按路径加载。

fixture 为合成脱敏样本（通用流程工业：污水处理 / 换热过程），保留问题模式、替换领域
内容，不使用用户论文原文。
"""

import importlib.util
import sys
from pathlib import Path

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

_INTRO = "\\chapter{绪论}\n本章介绍研究背景与问题。\n\\section{研究背景}\n需求增长。\n"
_TAIL = "\\chapter{总结与展望}\n全文总结与展望。\n"


def _run(tmp_path: Path, tex: str, **kwargs) -> str:
    f = tmp_path / "main.tex"
    f.write_text(tex, encoding="utf-8")
    return "\n".join(logic.analyze(f, **kwargs))


# 合规过程分析章：工艺节有流程图；难点节特性词+因果；框架节有框架图+方法模块名（不写章号）。
_COMPLIANT = (
    _INTRO
    + "\\chapter{某污水处理工艺流程分析与总体框架}\n"
    + "\\section{引言}\n"
    + "本章围绕污水处理过程展开。首先介绍工艺流程，然后分析关键难点，最后给出总体研究框架。\n"
    + "\\section{工艺流程分析}\n"
    + "污水处理全流程如图\\ref{fig:flow}所示，按物料流分为预处理、生化反应、沉淀出水三段。\n"
    + "\\section{关键难点分析}\n"
    + "生化反应过程具有强非线性与大滞后特性，多工况切换频繁，导致溶解氧浓度难以精确建模。\n"
    + "\\section{总体研究框架}\n"
    + "总体框架如图\\ref{fig:frame}所示。本文构建水质预测模型，设计工况识别网络，"
    + "并给出溶解氧优化策略实现节能控制。\n"
    + "\\section{本章小结}\n本章分析了工艺流程与难点，给出总体框架。\n"
    + _TAIL
)

# 病例过程分析章：工艺节缺流程图；难点节有特性词无因果；框架节空泛；框架先于难点；含“源论文”。
_SICK = (
    _INTRO
    + "\\chapter{某换热过程分析与方案}\n"
    + "\\section{引言}\n"
    + "本章围绕换热过程展开。三篇源论文分别对应三个核心问题。首先介绍工艺，然后给出方案。\n"
    + "\\section{工艺流程简介}\n"
    + "换热过程分为加热与冷却两段，涉及多个换热器与管路。\n"
    + "\\section{总体方案框架}\n"
    + "本章给出总体方案框架，如图\\ref{fig:frame}所示，后续章节将逐步展开各部分内容。\n"
    + "\\section{关键难点分析}\n"
    + "换热过程存在强非线性与强耦合，多工况运行，参数波动明显。\n"
    + "\\section{本章小结}\n本章给出了工艺与方案。\n"
    + _TAIL
)

# 方法+实验章式（边界例）：无过程分析章特征词，章式预判应输出 Info、不套 P-*。
_METHOD = (
    _INTRO
    + "\\chapter{预测控制算法设计}\n"
    + "\\section{问题建模}\n本章建立被控对象的状态空间模型，给出预测方程与目标函数。\n"
    + "\\section{滚动优化算法}\n设计滚动优化求解器，采用二次规划实现在线求解。\n"
    + "\\section{仿真实验}\n在仿真平台上验证算法性能，对比多种基线。\n"
    + _TAIL
)


# ── 加载守卫 ──────────────────────────────────────────────────


def test_loads_the_zh_copy_not_the_en_copy() -> None:
    assert hasattr(logic, "_check_process_chapter")
    assert hasattr(logic, "PROCESS_TRAIT_RE_ZH")


# ── 合规样本零 Major 误报（P-FRAME 章号缺失只 Info）───────────


def test_compliant_no_major_and_frame_chapter_map_info(tmp_path: Path) -> None:
    report = _run(tmp_path, _COMPLIANT, process_chapter=True)
    # P-FLOW / P-DERIVE / P-ORDER / P-PAPER 均不触发。
    assert "P-FLOW" not in report
    assert "P-DERIVE" not in report
    assert "P-ORDER" not in report
    assert "P-PAPER" not in report
    # P-FRAME：有框架图 + ≥2 方法模块名 -> 不报 Major；仅缺章号 -> Info。
    assert "P-FRAME 总体框架节内容空泛" not in report
    assert "P-FRAME 总体框架/方案节未见框架图" not in report
    assert "[Severity: Info] [Priority: P3]: [Script] P-FRAME 框架节未显式标注" in report


# ── P-FLOW：工艺节无流程图 -> Major ─────────────────────────


def test_pflow_missing_figure_flagged(tmp_path: Path) -> None:
    report = _run(tmp_path, _SICK, process_chapter=True)
    assert "P-FLOW" in report
    assert "过程分析章" in report and "[Severity: Major]" in report


# ── P-DERIVE：有特性词无因果 -> Minor ───────────────────────


def test_pderive_traits_without_causal_is_minor(tmp_path: Path) -> None:
    report = _run(tmp_path, _SICK, process_chapter=True)
    # _SICK 难点节有特性词（强非线性/强耦合/多工况/波动）但无因果连接 -> Minor 分支措辞唯一。
    assert "P-DERIVE 难点/问题节出现工艺特性词" in report
    assert "未见工艺特性词" not in report


def test_pderive_missing_traits_is_major(tmp_path: Path) -> None:
    """难点节完全无特性词 -> Major（缺特性词）。"""
    tex = (
        _INTRO
        + "\\chapter{某过程工艺分析}\n"
        + "\\section{工艺流程}\n流程如图\\ref{fig:flow}所示，分为多个工序。\n"
        + "\\section{关键问题}\n本节讨论运行中遇到的一些实际问题与注意事项。\n"
        + "\\section{总体框架}\n框架如图\\ref{fig:frame}所示，含水质预测模型与优化策略。\n"
        + _TAIL
    )
    report = _run(tmp_path, tex, process_chapter=True)
    assert "P-DERIVE" in report
    assert "未见工艺特性词" in report


# ── P-FRAME：框架空泛 + 章号缺失 Info ───────────────────────


def test_pframe_vague_is_major(tmp_path: Path) -> None:
    report = _run(tmp_path, _SICK, process_chapter=True)
    # _SICK 框架节有图但无方法模块名、无第X章 -> 空泛 Major + 章号 Info。
    assert "P-FRAME 总体框架节内容空泛" in report
    assert "P-FRAME 框架节未显式标注" in report


def test_pframe_missing_figure_is_major(tmp_path: Path) -> None:
    """框架节无框架图引用 -> Major（缺框架图）。"""
    tex = (
        _INTRO
        + "\\chapter{某过程工艺流程分析}\n"
        + "\\section{工艺流程}\n流程如图\\ref{fig:flow}所示。\n"
        + "\\section{关键难点}\n过程强非线性导致难以建模。\n"
        + "\\section{总体框架}\n本文构建水质预测模型，设计工况识别网络，第3章与第4章分别展开。\n"
        + _TAIL
    )
    report = _run(tmp_path, tex, process_chapter=True)
    assert "P-FRAME 总体框架/方案节未见框架图" in report
    # 显式写了第3章/第4章 -> 不再出章号映射 Info。
    assert "P-FRAME 框架节未显式标注" not in report


# ── P-ORDER：框架先于难点 -> Minor ─────────────────────────


def test_porder_frame_before_difficulty_flagged(tmp_path: Path) -> None:
    report = _run(tmp_path, _SICK, process_chapter=True)
    assert "P-ORDER" in report


def test_porder_correct_order_silent(tmp_path: Path) -> None:
    report = _run(tmp_path, _COMPLIANT, process_chapter=True)
    assert "P-ORDER" not in report


# ── P-PAPER：源论文表述 -> Minor ───────────────────────────


def test_ppaper_source_paper_phrase_flagged(tmp_path: Path) -> None:
    report = _run(tmp_path, _SICK, process_chapter=True)
    assert "P-PAPER" in report


def test_ppaper_absent_when_clean(tmp_path: Path) -> None:
    report = _run(tmp_path, _COMPLIANT, process_chapter=True)
    assert "P-PAPER" not in report


# ── 章式预判：方法+实验章式输出 Info、不套 P-* ─────────────


def test_method_chapter_gets_info_not_process_checks(tmp_path: Path) -> None:
    report = _run(tmp_path, _METHOD, process_chapter=True)
    assert "未见过程分析章特征" in report
    for marker in ("P-FLOW", "P-DERIVE", "P-FRAME", "P-ORDER", "P-PAPER"):
        assert marker not in report


# ── 默认章定位（第 2 章）与 --section 覆盖 ─────────────────


def test_default_targets_second_chapter(tmp_path: Path) -> None:
    """无 --section 时默认定位第 2 章（绪论后首个正文章）。"""
    tex = _SICK.replace(_TAIL, "") + _METHOD.split(_INTRO, 1)[1]
    report = _run(tmp_path, tex, process_chapter=True)
    # 第 2 章是过程分析章 -> 跑 P-*。
    assert "P-FLOW" in report
    # 未定位到第 3 章方法章 -> 不出方法章式 Info。
    assert "未见过程分析章特征" not in report


def test_section_override_targets_named_chapter(tmp_path: Path) -> None:
    """--section 指定第 3 章方法章时目标切换，输出方法章式 Info、不跑 P-*。"""
    tex = _SICK.replace(_TAIL, "") + _METHOD.split(_INTRO, 1)[1]
    report = _run(tmp_path, tex, section="预测控制算法设计", process_chapter=True)
    assert "未见过程分析章特征" in report
    assert "P-FLOW" not in report


# ── flag off：默认行为零变化 ───────────────────────────────


def test_flag_off_no_process_checks(tmp_path: Path) -> None:
    report = _run(tmp_path, _SICK)
    for marker in ("P-FLOW", "P-DERIVE", "P-FRAME", "P-ORDER", "P-PAPER", "过程分析章"):
        assert marker not in report
