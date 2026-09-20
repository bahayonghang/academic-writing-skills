"""Tests for latex-thesis-zh paragraph-roles checks (--paragraph-roles)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

from tests.support.paths import REPO_ROOT, SCRIPT_DIR_ZH, SKILLS_ROOT

_SCRIPT = SCRIPT_DIR_ZH / "analyze_logic.py"
_SKILL_DIR = SKILLS_ROOT / "latex-thesis-zh"


def _load_zh_logic():
    saved_path = list(sys.path)
    saved = {name: sys.modules.pop(name, None) for name in ("parsers", "tex_loader")}
    try:
        spec = importlib.util.spec_from_file_location("zh_paragraph_roles", _SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


logic = _load_zh_logic()


def test_loaded_module_is_zh_logic() -> None:
    assert hasattr(logic, "_check_paragraph_roles")
    assert hasattr(logic, "PR_INTRO_BG_MIN_HITS")
    assert hasattr(logic, "DEFAULT_PARAGRAPH_ROLES_TERMS")
    assert Path(logic.__file__).resolve() == _SCRIPT.resolve()


def test_guide_section_example_uses_known_keys_not_chapter_numbers() -> None:
    guide = (_SKILL_DIR / "references" / "writing" / "paragraph-roles-zh.md").read_text(
        encoding="utf-8"
    )
    assert "--section 3" not in guide
    assert "--section method" in guide
    assert "阈值不提供命令行覆盖" in guide
    assert "支持词表与命令行配置" not in guide


def test_yaml_terms_equal_builtin_defaults() -> None:
    yaml_path = _SKILL_DIR / "references" / "writing" / "paragraph-roles-terms.yaml"
    assert yaml_path.exists()
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    for key, values in logic.DEFAULT_PARAGRAPH_ROLES_TERMS.items():
        assert key in data
        assert tuple(data[key]) == values


def test_docs_mirrors_equal_source_yaml() -> None:
    src = (_SKILL_DIR / "references" / "writing" / "paragraph-roles-terms.yaml").read_bytes()
    zh_mirror = (
        REPO_ROOT
        / "docs"
        / "zh"
        / "skills"
        / "latex-thesis-zh"
        / "resources"
        / "references"
        / "writing"
        / "paragraph-roles-terms.yaml"
    ).read_bytes()
    en_mirror = (
        REPO_ROOT
        / "docs"
        / "skills"
        / "latex-thesis-zh"
        / "resources"
        / "references"
        / "writing"
        / "paragraph-roles-terms.yaml"
    ).read_bytes()
    assert src.replace(b"\r\n", b"\n") == zh_mirror.replace(b"\r\n", b"\n")
    assert src.replace(b"\r\n", b"\n") == en_mirror.replace(b"\r\n", b"\n")


def test_yaml_per_field_fallback(tmp_path: Path) -> None:
    fake_writing = tmp_path / "references" / "writing"
    fake_writing.mkdir(parents=True)
    yaml_file = fake_writing / "paragraph-roles-terms.yaml"

    terms = logic._load_paragraph_roles_terms(tmp_path / "scripts")
    assert terms == logic.DEFAULT_PARAGRAPH_ROLES_TERMS

    yaml_file.write_text("not a yaml dict: [unclosed", encoding="utf-8")
    terms = logic._load_paragraph_roles_terms(tmp_path / "scripts")
    assert terms == logic.DEFAULT_PARAGRAPH_ROLES_TERMS

    yaml_file.write_text("background_markers:\n  - 自定义背景词\n", encoding="utf-8")
    terms = logic._load_paragraph_roles_terms(tmp_path / "scripts")
    assert terms["background_markers"] == ("自定义背景词",)
    assert terms["roadmap_markers"] == logic.DEFAULT_PARAGRAPH_ROLES_TERMS["roadmap_markers"]

    yaml_file.write_text(
        "background_markers: not-a-list\nroadmap_markers:\n  - 自定义路线\n",
        encoding="utf-8",
    )
    terms = logic._load_paragraph_roles_terms(tmp_path / "scripts")
    assert terms["background_markers"] == logic.DEFAULT_PARAGRAPH_ROLES_TERMS["background_markers"]
    assert terms["roadmap_markers"] == ("自定义路线",)


SAMPLE_PROJECT = r"""\documentclass{ctexbook}
\begin{document}

\chapter{第二章 过程分析与建模基础}
第二章引言是概述式引言。近年来智能制造和工业互联网在国民经济中蓬勃发展并起到关键作用。
针对上述现实需求，本章首先给出总体框架，其次设计分析流程，最后完成工况分析。

\section{2.1 工艺流程与变量分析}
本节首先分析实际工业工艺流程中的主要测量变量与输入输出关系。

\chapter{第三章 自适应动态状态估计方法}
第2章给出了基线模型，但在复杂工况下存在泛化漂移瓶颈。
近年来智能制造和工业互联网飞速发展，在国民经济和战略需求中发挥着核心支撑作用，具有广泛应用前景。
针对上述问题，本章提出自适应重加权机制。
本章组织如下：3.1 节介绍模型结构，3.2 节介绍更新准则，3.3 节给出实验验证。同时，本章首先建立数学模型，其次推导更新算法，最后完成实验对比。

\section{3.1 状态估计系统框架}
针对非平稳工况下传统估计方法误差大、泛化能力弱的核心挑战，本章整体提出了由动态特征提取、自适应重加权和多任务输出组成的完整估计系统。本节作为该系统的核心组成部分，将围绕上述系统面临的所有泛化问题与特征提取瓶颈展开深入研究。

\subsection{3.1.1 特征投影算子构建}
在构建特征投影算子时，现有研究通常面临多重挑战：首先是高维观测带来的特征冗余瓶颈，其次是多模态采样不同步导致的分布漂移难题。为了克服上述全部挑战，本小节展开深入推导。
针对上节输出的异步特征表征，本小节构建时间连续投影算子。

\subsection{3.1.2 投影矩阵在线更新}
本小节建立投影矩阵在线更新准则。给定输入序列向量，通过梯度投影更新参数。
\begin{equation}
\mathbf{y} = \mathbf{W} \mathbf{x} + \mathbf{b}
\end{equation}
上式中，首先计算矩阵相乘，再将乘积进行矩阵转置并加上偏置，最后应用激活函数计算出各项最终输出概率。
\begin{equation}
\mathbf{z} = \mathbf{A} \mathbf{y}
\end{equation}
式中：$\mathbf{A}$ 为投影矩阵。该变换将状态向量映射到正交子空间，滤除高频随机测量噪声。

\section{3.2 实验验证与分析}
本节对比四种算法的均方根误差。

\section{3.3 本章小结}
本章针对非平稳工况下的状态估计漂移瓶颈，提出了自适应动态重加权方法。
如图 \ref{fig:framework} 与表 \ref{tab:comparison} 所示，本文方法显著降低了估计误差。
在此基础上，根据文献 \cite{smith2024} 的收敛准则完成训练：
\begin{equation}
\mathcal{L} = \alpha \mathcal{L}_1 + \beta \mathcal{L}_2
\end{equation}

\end{document}
"""


def test_pr_intro_bg_and_toc_triggers(tmp_path: Path) -> None:
    doc = tmp_path / "main.tex"
    doc.write_text(SAMPLE_PROJECT, encoding="utf-8")

    out = logic.analyze(doc, paragraph_roles=True)
    report = "\n".join(out)

    # Chapter 2 overview intro has background markers but MUST NOT trigger PR-INTRO-BG
    assert "第二章" not in report or "PR-INTRO-BG" not in "\n".join(
        line for line in out if "第二章" in line
    )

    # Chapter 3 intro has background markers without "第X章" in that sentence -> triggers PR-INTRO-BG
    assert "[Script] PR-INTRO-BG" in report
    assert "第三章" in report

    # Chapter 3 intro has both 3.1/3.2/3.3 preview and 首先/其次/最后 -> triggers PR-INTRO-TOC
    assert "[Script] PR-INTRO-TOC" in report


def test_pr_intro_toc_negative_cases(tmp_path: Path) -> None:
    # 1. Standalone section directory (< 5 sections, no roadmap words) -> passes
    sample_standalone_toc = r"""\documentclass{ctexbook}
\begin{document}
\chapter{第三章 方法}
第2章奠定了基础。本章提出新机制。本章组织如下：3.1 节介绍模型，3.2 节介绍算法，3.3 节进行验证。
\section{3.1 模型}
正文。
\end{document}
"""
    doc1 = tmp_path / "doc1.tex"
    doc1.write_text(sample_standalone_toc, encoding="utf-8")
    out1 = logic.analyze(doc1, paragraph_roles=True)
    assert not any("PR-INTRO-TOC" in line for line in out1)

    # 2. Standalone roadmap ("首先...其次...最后", no section numbers) -> passes
    sample_standalone_roadmap = r"""\documentclass{ctexbook}
\begin{document}
\chapter{第三章 方法}
第2章奠定了基础。本章提出新机制。本章首先给出数学模型，其次推导优化算法，最后通过实验验证其有效性。
\section{3.1 模型}
正文。
\end{document}
"""
    doc2 = tmp_path / "doc2.tex"
    doc2.write_text(sample_standalone_roadmap, encoding="utf-8")
    out2 = logic.analyze(doc2, paragraph_roles=True)
    assert not any("PR-INTRO-TOC" in line for line in out2)

    # 3. >= 5 section preview numbers -> triggers PR-INTRO-TOC
    sample_five_sections = r"""\documentclass{ctexbook}
\begin{document}
\chapter{第三章 方法}
第2章奠定了基础。本章组织如下：3.1 节建模，3.2 节推导，3.3 节分析，3.4 节求解，3.5 节验证。
\section{3.1 建模}
正文。
\end{document}
"""
    doc3 = tmp_path / "doc3.tex"
    doc3.write_text(sample_five_sections, encoding="utf-8")
    out3 = logic.analyze(doc3, paragraph_roles=True)
    assert any("PR-INTRO-TOC" in line for line in out3)


def test_pr_lead_dup_triggers_and_negative(tmp_path: Path) -> None:
    sample_dup = r"""\documentclass{ctexbook}
\begin{document}
\chapter{第三章 自适应动态状态估计方法}
第2章给出了基线模型，但在复杂工况下存在泛化漂移瓶颈。针对上述问题，本章提出自适应重加权机制。本章首先建立数学模型，其次推导更新算法，最后完成实验对比。

\section{3.1 状态估计系统框架}
第2章给出了基线模型，但在复杂工况下存在泛化漂移瓶颈。针对上述问题，本章提出自适应重加权机制，本节首先建立数学模型，其次推导更新算法，最后完成实验验证，并针对泛化漂移瓶颈与自适应重加权展开深入研究。

\subsection{3.1.1 数学模型}
正文建立数学模型。

\subsection{3.1.2 在线准则}
正文推导准则。
\end{document}
"""
    doc_dup = tmp_path / "doc_dup.tex"
    doc_dup.write_text(sample_dup, encoding="utf-8")
    out_dup = logic.analyze(doc_dup, paragraph_roles=True)
    assert any("PR-LEAD-DUP" in line for line in out_dup)

    sample_reading_map = r"""\documentclass{ctexbook}
\begin{document}
\chapter{第三章 状态估计}
第2章给出了基线模型。针对动态泛化瓶颈，本章提出自适应重加权机制，利用在线时序残差动态调整估计器权重。
本章首先给出数学描述，其次设计更新准则，最后完成泛化性能验证。

\section{3.1 估计器构建}
本节重点设计重加权模块。该模块接收时序特征并估计权重矩阵。下文 3.1.1 节建立数学模型，3.1.2 节推导在线更新准则。

\subsection{3.1.1 数学模型}
正文建立数学模型。

\subsection{3.1.2 在线准则}
正文推导准则。
\end{document}
"""
    doc_clean = tmp_path / "doc_clean.tex"
    doc_clean.write_text(sample_reading_map, encoding="utf-8")
    out_clean = logic.analyze(doc_clean, paragraph_roles=True)
    assert not any("PR-LEAD-DUP" in line for line in out_clean)


def test_pr_sub_chal_triggers_and_exemptions(tmp_path: Path) -> None:
    doc = tmp_path / "main.tex"
    doc.write_text(SAMPLE_PROJECT, encoding="utf-8")

    out = logic.analyze(doc, paragraph_roles=True)
    report = "\n".join(out)
    # Subsection 3.1.1 opening has challenges + enumeration -> PR-SUB-CHAL
    assert "[Script] PR-SUB-CHAL" in report

    # Exemption 1: Literature / review chapter
    lit_sample = r"""\documentclass{ctexbook}
\begin{document}
\chapter{第二章 文献综述与相关工作}
\section{2.1 综述概览}
\subsection{2.1.1 现状分析}
在研究时现有方法面临多重挑战：首先是特征瓶颈问题，其次是分布漂移难题。本节展开综述。
\end{document}
"""
    doc_lit = tmp_path / "doc_lit.tex"
    doc_lit.write_text(lit_sample, encoding="utf-8")
    out_lit = logic.analyze(doc_lit, paragraph_roles=True)
    assert not any("PR-SUB-CHAL" in line for line in out_lit)

    # Exemption 2: Subsection title contains "引言" / "概述"
    intro_sub_sample = r"""\documentclass{ctexbook}
\begin{document}
\chapter{第三章 方法}
第2章已奠定基础。本章提出新机制。
\section{3.1 模块架构}
\subsection{3.1.1 模块引言}
在研究时现有方法面临多重挑战：首先是特征瓶颈问题，其次是分布漂移难题。本节进行介绍。
\end{document}
"""
    doc_intro = tmp_path / "doc_intro.tex"
    doc_intro.write_text(intro_sub_sample, encoding="utf-8")
    out_intro = logic.analyze(doc_intro, paragraph_roles=True)
    assert not any("PR-SUB-CHAL" in line for line in out_intro)


def test_pr_eq_narr_triggers_and_gloss_exemption(tmp_path: Path) -> None:
    doc = tmp_path / "main.tex"
    doc.write_text(SAMPLE_PROJECT, encoding="utf-8")

    out = logic.analyze(doc, paragraph_roles=True)
    report = "\n".join(out)

    # Equation 1 has verbatim operator translation -> triggers PR-EQ-NARR
    assert "[Script] PR-EQ-NARR" in report

    # Equation 2 has pure glossing ("式中：...") without operator words -> does not trigger PR-EQ-NARR
    sample_pure_gloss = r"""\documentclass{ctexbook}
\begin{document}
\chapter{第三章 方法}
第2章奠定基础。本章提出新机制。
\section{3.1 公式}
\begin{equation}
\mathbf{z} = \mathbf{A} \mathbf{y}
\end{equation}
式中：$\mathbf{A}$ 为正交投影矩阵，$\mathbf{y}$ 为输入时序特征向量。该变换将观测向量映射到主成分补空间，用于消除稳态噪声干扰。
\end{document}
"""
    doc_gloss = tmp_path / "doc_gloss.tex"
    doc_gloss.write_text(sample_pure_gloss, encoding="utf-8")
    out_gloss = logic.analyze(doc_gloss, paragraph_roles=True)
    assert not any("PR-EQ-NARR" in line for line in out_gloss)


def test_pr_sum_new_triggers_and_ref_exemption(tmp_path: Path) -> None:
    doc = tmp_path / "main.tex"
    doc.write_text(SAMPLE_PROJECT, encoding="utf-8")

    out = logic.analyze(doc, paragraph_roles=True)
    report = "\n".join(out)

    # Summary in SAMPLE_PROJECT has \cite and \begin{equation} -> triggers PR-SUM-NEW
    assert "[Script] PR-SUM-NEW" in report

    # Summary with ONLY \ref and \eqref -> does NOT trigger PR-SUM-NEW
    sample_ref_only = r"""\documentclass{ctexbook}
\begin{document}
\chapter{第三章 方法}
第2章奠定基础。本章提出新机制。
\section{3.1 实验}
正文。
\section{3.2 本章小结}
本章针对非平稳工况提出了自适应重加权方法。如图 \ref{fig:framework} 与表 \ref{tab:comparison} 所示，验证表明本文方法显著降低了估计误差，为第 4 章的全局优化提供了可靠输入。
\end{document}
"""
    doc_ref = tmp_path / "doc_ref.tex"
    doc_ref.write_text(sample_ref_only, encoding="utf-8")
    out_ref = logic.analyze(doc_ref, paragraph_roles=True)
    assert not any("PR-SUM-NEW" in line for line in out_ref)


def test_finding_contract_fields_and_no_prose_copy(tmp_path: Path) -> None:
    doc = tmp_path / "main.tex"
    doc.write_text(SAMPLE_PROJECT, encoding="utf-8")

    out = logic.analyze(doc, paragraph_roles=True)

    pr_findings: list[list[str]] = []
    current_block: list[str] = []
    for line in out:
        if line.startswith("% 段落职责"):
            if current_block:
                pr_findings.append(current_block)
            current_block = [line]
        elif current_block:
            current_block.append(line)
            if line == "% Meaning-Check: NEEDS-LLM":
                pr_findings.append(current_block)
                current_block = []

    assert pr_findings, "expected at least one PR finding"
    for block in pr_findings:
        header = block[0]
        assert "[Severity: Info] [Priority: P3]" in header
        assert "[Script] PR-" in header
        block_text = "\n".join(block)
        assert "% Meaning-Check: NEEDS-LLM" in block_text
        assert "Meaning-Check: PRESERVED" not in block_text

        # Never copy full sentences from SAMPLE_PROJECT into finding
        assert "近年来智能制造和工业互联网飞速发展" not in block_text
        assert "本小节展开深入推导" not in block_text
        assert "上式中，首先计算矩阵相乘" not in block_text


def test_section_scoping_limits_paragraph_roles(tmp_path: Path) -> None:
    doc = tmp_path / "main.tex"
    doc.write_text(SAMPLE_PROJECT, encoding="utf-8")

    # Full analysis has multiple PR findings
    full_out = logic.analyze(doc, paragraph_roles=True)
    assert any("PR-INTRO-BG" in line for line in full_out)

    # Method chapter contains the Ch.3 intro finding; experiment interval must not.
    method_out = logic.analyze(doc, section="method", paragraph_roles=True)
    assert not any("未找到章节" in line for line in method_out)
    assert any("PR-INTRO-BG" in line for line in method_out)

    experiment_out = logic.analyze(doc, section="experiment", paragraph_roles=True)
    assert not any("未找到章节" in line for line in experiment_out)
    assert not any("PR-INTRO-BG" in line for line in experiment_out)


def test_thesis_project_fixture_exits_zero() -> None:
    fixture_path = _SKILL_DIR / "evals" / "fixtures" / "thesis-project" / "main.tex"
    if not fixture_path.exists():
        pytest.skip("thesis-project fixture not available")

    out = logic.analyze(fixture_path, paragraph_roles=True)
    assert isinstance(out, list)
