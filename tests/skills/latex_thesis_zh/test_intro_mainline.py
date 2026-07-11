"""Intro mainline checks (L-SCI / L-MAP / L-FUN / L-DOM) for the
latex-thesis-zh copy of analyze_logic.py.

The zh copy is loaded by file path via importlib — a bare
``import analyze_logic`` resolves to the latex-paper-en copy on sys.path
(see conftest), which has no ``_check_intro_mainline``.
"""

import importlib.util
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH

_ZH_DIR = SCRIPT_DIR_ZH
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load_zh(name: str):
    """Canonical isolated path-loader (see test_deai_tense_zh.py)."""
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

_TABLE_PROBLEMS = r"""
\begin{table}[htbp]
\begin{tabular}{ll}
科学问题 & 研究内容 \\
状态重叠 & 模块A \\
标签稀疏 & 模块B \\
\end{tabular}
\end{table}
"""

_GOOD_TABLE_PROBLEMS = r"""
\begin{table}[htbp]
\begin{tabular}{ll}
科学问题 & 研究内容 \\
如何在多速率采样下保持质量估计的时间语义一致 & 模块A \\
针对稀疏标签场景能否生成工艺可信的边界样本 & 模块B \\
\end{tabular}
\end{table}
"""


def _intro_tex(
    first_para: str = "智能制造正在快速发展。本文围绕运行优化展开研究。",
    status_body: str = "国外学者提出了方法A。国内团队改进了方法B。",
    problems_block: str = _TABLE_PROBLEMS,
    content_items: int = 3,
    innovation_items: int = 3,
    declaration: str = "",
) -> str:
    items = "\n".join(rf"\item 研究要点{i}。" for i in range(1, content_items + 1))
    innovations = "\n\n".join(
        rf"\textbf{{（{i}）}}本文提出创新机制{i}。" for i in range(1, innovation_items + 1)
    )
    return rf"""\chapter{{绪论}}

{first_para}

\section{{研究背景与意义}}

过程工业存在质量与能耗的权衡瓶颈，本文由此切入。

\section{{国内外研究现状}}

{status_body}

\section{{主要研究}}

本文凝练的科学问题如下。
{problems_block}

\subsection{{主要研究内容}}

\begin{{enumerate}}
{items}
\end{{enumerate}}

{declaration}

\subsection{{主要创新}}

{innovations}
"""


def _run(tmp_path: Path, tex: str) -> str:
    tex_file = tmp_path / "intro.tex"
    tex_file.write_text(tex, encoding="utf-8")
    return "\n".join(logic.analyze(tex_file, intro_mainline=True))


def test_loads_the_zh_copy_not_the_en_copy() -> None:
    assert hasattr(logic, "_check_intro_mainline")
    assert hasattr(logic, "_is_bare_noun_phrase")


def test_lsci_table_noun_phrases_flagged(tmp_path: Path) -> None:
    report = _run(tmp_path, _intro_tex())
    assert "L-SCI 表述“状态重叠”" in report
    assert "L-SCI 表述“标签稀疏”" in report
    assert "对象-问题-方法" in report


def test_lsci_wellformed_table_rows_pass(tmp_path: Path) -> None:
    report = _run(tmp_path, _intro_tex(problems_block=_GOOD_TABLE_PROBLEMS))
    assert "L-SCI" not in report


def test_lsci_enumerate_form_flagged(tmp_path: Path) -> None:
    enum_block = (
        "\\begin{enumerate}\n"
        "\\item 状态重叠。该问题源于原料条件变化。\n"
        "\\item 如何在稀疏标签下保持尾部估计可靠，是第二个问题。\n"
        "\\end{enumerate}\n"
    )
    report = _run(tmp_path, _intro_tex(problems_block=enum_block))
    assert "L-SCI 表述“状态重叠”" in report
    assert report.count("L-SCI") == 1  # the well-formed item passes


def test_lmap_count_mismatch_flagged(tmp_path: Path) -> None:
    report = _run(tmp_path, _intro_tex(content_items=4, innovation_items=3))
    assert "L-MAP" in report
    assert "条数不闭合" in report
    assert "研究内容 4 条" in report and "创新点 3 条" in report


def test_lmap_declared_mismatch_downgrades(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        _intro_tex(
            content_items=4,
            innovation_items=3,
            declaration="其中系统实现作为工程验证贡献，不与三项方法创新等量表述。",
        ),
    )
    assert "条数不闭合" not in report
    assert "视为有意设计" in report


def test_lmap_matching_counts_silent(tmp_path: Path) -> None:
    # 3 content items vs 3 innovations vs 2 science problems -> still a mismatch;
    # align everything to verify true silence.
    report = _run(
        tmp_path,
        _intro_tex(problems_block=_GOOD_TABLE_PROBLEMS, content_items=2, innovation_items=2),
    )
    assert "L-MAP" not in report


def test_lfun_missing_problem_layer_flagged(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        _intro_tex(first_para="智能制造正在快速发展，应用场景广泛。本文由此展开。"),
    )
    assert "L-FUN" in report
    assert "技术瓶颈/问题" in report


def test_lfun_complete_funnel_silent(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        _intro_tex(
            first_para="智能制造应用场景广泛，但质量波动问题仍是瓶颈。本文围绕该问题展开研究。"
        ),
    )
    assert "L-FUN" not in report


def test_ldom_no_split_no_declaration_flagged(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        _intro_tex(status_body="学者们提出了方法A。后续工作改进了方法B。"),
    )
    assert "L-DOM" in report


def test_ldom_domestic_foreign_split_silent(tmp_path: Path) -> None:
    report = _run(tmp_path, _intro_tex())  # default body mentions 国外 + 国内
    assert "L-DOM" not in report


def test_ldom_declared_thematic_order_silent(tmp_path: Path) -> None:
    report = _run(
        tmp_path,
        _intro_tex(status_body="本节按主题组织，各主题内对比中外工作。方法A与方法B先后出现。"),
    )
    assert "L-DOM" not in report


def test_flag_off_keeps_default_behavior(tmp_path: Path) -> None:
    # Without the flag, none of the new diagnostics may appear.
    tex_file = tmp_path / "intro.tex"
    tex_file.write_text(_intro_tex(), encoding="utf-8")
    report = "\n".join(logic.analyze(tex_file))
    for marker in ("L-SCI", "L-MAP", "L-FUN", "L-DOM"):
        assert marker not in report
