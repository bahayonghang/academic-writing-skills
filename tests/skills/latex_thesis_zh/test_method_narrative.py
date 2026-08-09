"""中文方法叙述候选检查的公开接口回归测试。"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH

_ZH_DIR = SCRIPT_DIR_ZH
_SCRIPT = _ZH_DIR / "analyze_logic.py"
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load_zh():
    """按路径加载中文副本，并恢复共享模块与导入路径。"""
    saved_path = list(sys.path)
    saved_modules = {name: sys.modules.pop(name, None) for name in _SHARED_MODULE_NAMES}
    try:
        sys.path.insert(0, str(_ZH_DIR))
        spec = importlib.util.spec_from_file_location("zh_method_narrative", _SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, module in saved_modules.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


logic = _load_zh()


def _write(tmp_path: Path, tex: str) -> Path:
    path = tmp_path / "main.tex"
    path.write_text(tex, encoding="utf-8")
    return path


def _run(tmp_path: Path, tex: str, *, section: str, enabled: bool = True) -> str:
    path = _write(tmp_path, tex)
    return "\n".join(
        logic.analyze(path, section=section, method_narrative=enabled)
        if enabled
        else logic.analyze(path, section=section)
    )


_SICK_METHOD_TITLE = "基于多阶段约束传播的工业质量预测方法"
_SICK_METHOD = (
    f"\\chapter{{{_SICK_METHOD_TITLE}}}\n"
    "\\section{总体方法}\n"
    "本章方法由状态编码、状态投影和监督校准组成。\n"
    "\\subsection{状态编码}\n"
    "接下来，本节将介绍状态编码模块。\n"
    "\\paragraph{动态编码。}\n"
    "本模块主要用于提取动态状态。\n"
    "\\paragraph{上下文聚合。}\n"
    "该模块负责聚合窗口内的上下文。\n"
    "普通段落补充输入窗口和采样边界。\n"
    "\\paragraph{状态投影。}\n"
    "投影算子将聚合状态映射到监督空间。\n"
    "\\begin{equation}\n"
    "z_t = W h_t + b\n"
    "\\end{equation}\n"
    "投影结果保留每个时间窗的状态索引。\n"
    "该对象随后交给校准模块。\n"
    "输出范围由训练样本确定。\n"
    "\\subsection{监督校准}\n"
    "由于投影状态仍含噪声，校准器依据独立阈值筛选候选。\n"
)

_COMPLIANT_METHOD_TITLE = "面向不确定输入的约束校准设计"
_COMPLIANT_METHOD = (
    f"\\chapter{{{_COMPLIANT_METHOD_TITLE}}}\n"
    "\\section{总体方法}\n"
    "原始观测先形成状态表征，再由校准模块生成监督对象。\n"
    "\\subsection{状态表征}\n"
    "由于原始窗口仍含异步采样误差，后续校准不能直接使用原始观测。\n"
    "为获得时间对齐能力，本节采用带掩码的状态编码器。\n"
    "\\begin{equation}\n"
    "h_t = f(x_t, m_t)\n"
    "\\end{equation}\n"
    "式中，$h_t$ 表示对齐后的状态，并作为校准模块的输入。\n"
    "\\subsection{监督校准}\n"
    "由于状态表征尚未给出可信范围，校准器使用独立数据确定准入阈值。\n"
    "该阈值把候选转换为带区间的监督对象，供下游预测器训练。\n"
)

_EXP_PARAGRAPH_OK = (
    "\\chapter{工程验证}\n"
    "\\section{仿真实验与结果分析}\n"
    "\\paragraph{核心结论概括}\n"
    "本模块主要用于概括实验观察。\n"
    "\\paragraph{误差分布}\n"
    "该模块负责汇总不同工况的误差。\n"
    "\\paragraph{稳定性分析}\n"
    "本模块用于说明重复试验结果。\n"
)

_COMMENT_AND_TOKEN_BOUNDARIES = (
    "\\chapter{方法设计}\n"
    "\\subsection{注释与保护边界}\n"
    "然后，本节将介绍边界模块 % 由于已有约束\n"
    "\\paragraph{注释标题。} % 本模块用于伪注释\n"
    "本段只说明输入边界。\n"
    "\\paragraph{真实报幕。}\n"
    "本模块用于处理输入。\n"
    "\\paragraph{受保护标题。}\n"
    "说明见\\cite{本模块用于}，正文不作职责报幕。\n"
    "\\begin{equation}\n"
    "x = 1\n"
    "% \\end{equation}\n"
    "y = 2\n"
    "\\end{equation}\n"
    "输出对象已定义。 % 其中只存在于注释\n"
    "说明见\\cite{其中}，引用键不是释义。\n"
    "$其中$ 只位于受保护数学环境。\n"
)

_SEPARATED_EQUATIONS = (
    "\\chapter{方法设计}\n"
    "\\subsection{分步变换}\n"
    "由于原始输入尚未对齐，先执行第一个变换。\n"
    "\\begin{equation}\n"
    "x = 1\n"
    "\\end{equation}\n"
    "第一个输出仅用于构造下一个变换。\n"
    "\\begin{equation}\n"
    "y = 2\n"
    "\\end{equation}\n"
    "式中，$y$ 表示第二个变换的输出。\n"
)

_CONTINUOUS_EQUATIONS = (
    "\\chapter{方法设计}\n"
    "\\subsection{联合变换}\n"
    "由于输入同时受两项约束，两式连续给出联合变换。\n"
    "\\begin{equation}\n"
    "x = 1\n"
    "\\end{equation}\n"
    "\\begin{align}\n"
    "y &= 2\n"
    "\\end{align}\n"
    "其中，$x$ 和 $y$ 分别表示两步变换的输出。\n"
    "\\begin{equation*}\n"
    "z = 3\n"
    "\\end{equation*}\n"
)

_EQUATION_BEFORE_NEXT_SUBSECTION = (
    "\\chapter{方法设计}\n"
    "\\subsection{第一变换}\n"
    "由于输入未对齐，先构造中间表征。\n"
    "\\begin{equation}\n"
    "x = 1\n"
    "\\end{equation}\n"
    "\\subsection{第二变换}\n"
    "其中，$y$ 只表示第二小节定义的输出。\n"
)


def test_loader_targets_zh_copy() -> None:
    assert logic.__file__ is not None
    assert Path(logic.__file__).resolve() == _SCRIPT.resolve()
    assert hasattr(logic, "MN_ANNOUNCE_RE_ZH")


def test_sick_method_reports_three_findings_and_edge_table(tmp_path: Path) -> None:
    report = _run(tmp_path, _SICK_METHOD, section=_SICK_METHOD_TITLE)

    assert "[Severity: Minor] [Priority: P2]: [Script] M-HEADING" in report
    assert "3 个行内小标题" in report and "2 个报幕句" in report
    assert "[Severity: Info] [Priority: P3]: [Script] M-SEQWORD" in report
    assert "[Severity: Minor] [Priority: P2]: [Script] M-EQUATION" in report
    assert report.count("% Meaning-Check: NEEDS-LLM") == 3
    assert "% M-EDGETABLE" in report
    assert "% 小节标题清单：状态编码 -> 监督校准" in report
    assert "% | 上游小节 | 上游产出 | 连接类型 | 中间变换 | 下游用途 |" in report
    assert "% | 状态编码 |  |  |  |  |" in report
    assert report.rstrip().endswith("% [LLM] 待填写")


def test_compliant_method_has_no_method_narrative_finding(tmp_path: Path) -> None:
    report = _run(tmp_path, _COMPLIANT_METHOD, section=_COMPLIANT_METHOD_TITLE)

    assert "[Script] M-HEADING" not in report
    assert "[Script] M-SEQWORD" not in report
    assert "[Script] M-EQUATION" not in report
    assert "% M-EDGETABLE" in report


def test_method_narrative_is_disabled_without_switch(tmp_path: Path) -> None:
    report = _run(tmp_path, _SICK_METHOD, section=_SICK_METHOD_TITLE, enabled=False)

    assert "M-HEADING" not in report
    assert "M-SEQWORD" not in report
    assert "M-EQUATION" not in report
    assert "M-EDGETABLE" not in report


def test_cli_requires_section_and_lists_candidate_chapters(tmp_path: Path) -> None:
    excluded = (
        "\\chapter{绪\\quad 论}\n"
        "\\section{结果分析}\n"
        "本节说明前期研究结果。\n"
        "\\chapter{总结与展望}\n"
        "总结。\n"
    )
    path = _write(tmp_path, _SICK_METHOD + _EXP_PARAGRAPH_OK + excluded)

    result = subprocess.run(
        [sys.executable, str(_SCRIPT), str(path), "--method-narrative"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        check=False,
    )

    assert result.returncode == 2
    assert "候选方法章清单（仅供选择，不代表自动判定）" in result.stdout
    assert _SICK_METHOD_TITLE in result.stdout
    assert "工程验证" in result.stdout
    assert "绪\\quad 论" not in result.stdout
    assert "总结与展望" not in result.stdout
    assert "--section" in result.stdout


def test_section_scans_only_the_exact_long_chapter_title(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        _SICK_METHOD + _COMPLIANT_METHOD + _EXP_PARAGRAPH_OK,
        section=_COMPLIANT_METHOD_TITLE,
    )

    assert "[Script] M-HEADING" not in report
    assert "[Script] M-SEQWORD" not in report
    assert "[Script] M-EQUATION" not in report
    assert "% 小节标题清单：状态表征 -> 监督校准" in report
    assert "核心结论概括" not in report


def test_section_matches_visible_title_with_latex_spacing(tmp_path: Path) -> None:
    raw_title = "基于多阶段约束传播的\\quad 工业质量预测方法"
    visible_title = "基于多阶段约束传播的工业质量预测方法"
    tex = _SICK_METHOD.replace(_SICK_METHOD_TITLE, raw_title)

    report = _run(tmp_path, tex, section=visible_title)

    assert "[Script] M-HEADING" in report
    assert "% ERROR" not in report


def test_inline_comments_and_protected_tokens_are_not_visible_prose(tmp_path: Path) -> None:
    report = _run(tmp_path, _COMMENT_AND_TOKEN_BOUNDARIES, section="方法设计")

    assert "[Script] M-HEADING" not in report
    assert "[Script] M-SEQWORD" in report
    assert "[Script] M-EQUATION" in report


def test_later_equation_gloss_does_not_close_an_earlier_group(tmp_path: Path) -> None:
    report = _run(tmp_path, _SEPARATED_EQUATIONS, section="方法设计")

    assert report.count("[Script] M-EQUATION") == 1


def test_continuous_numbered_equations_share_one_gloss_and_starred_is_ignored(
    tmp_path: Path,
) -> None:
    report = _run(tmp_path, _CONTINUOUS_EQUATIONS, section="方法设计")

    assert "[Script] M-EQUATION" not in report


def test_equation_gloss_does_not_cross_a_subsection_boundary(tmp_path: Path) -> None:
    report = _run(tmp_path, _EQUATION_BEFORE_NEXT_SUBSECTION, section="方法设计")

    assert report.count("[Script] M-EQUATION") == 1
