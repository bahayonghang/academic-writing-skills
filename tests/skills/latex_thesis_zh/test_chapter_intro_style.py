"""Tests for latex-thesis-zh chapter introduction style observation (--chapter-intro-style)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml

from tests.support.paths import REPO_ROOT, SCRIPT_DIR_ZH, SKILLS_ROOT

_ZH_DIR = SCRIPT_DIR_ZH
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")
_FIXTURE = (
    SKILLS_ROOT / "latex-thesis-zh" / "evals" / "fixtures" / "chapter-intro-style" / "main.tex"
)


def _load_zh(name: str):
    """Canonical isolated path-loader."""
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


def test_chapter_intro_style_load_guard() -> None:
    """Verify that zh copy of analyze_logic was loaded."""
    assert Path(logic.__file__).resolve() == (_ZH_DIR / "analyze_logic.py").resolve()
    assert hasattr(logic, "_check_chapter_intro_style")
    assert hasattr(logic, "_chapter_intro_span")
    assert hasattr(logic, "CHAPTER_INTRO_STYLE_TERMS_FILENAME")
    assert hasattr(logic, "CI_ONE_PARA_MAX_HAN")
    assert logic.CI_ONE_PARA_MAX_HAN == 600


def test_chapter_dep_ref_re_matches_enumerations_and_ranges() -> None:
    """R5.1: CHAPTER_DEP_REF_RE recognizes chapter lists, ranges, and single chapter refs."""
    pat = logic.CHAPTER_DEP_REF_RE
    assert pat.search("第 3、4、5 章") is not None
    assert pat.search("第 3～5 章") is not None
    assert pat.search("第3-5章") is not None
    assert pat.search("第三章和第四章") is not None
    assert pat.search("第三至五章") is not None
    assert pat.search("第 2 章") is not None

    # Verify that a chapter intro with chapter list bridge does NOT report missing bridge
    tex = (
        "\\documentclass{ctexbook}\n"
        "\\begin{document}\n"
        "\\chapter{第一章 绪论}\n"
        "\\section{1.1 背景}\n"
        "\\chapter{第二章 过程基础}\n"
        "\\section{2.1 基础}\n"
        "\\chapter{第三章 建模方法}\n"
        "工业过程数据存在非平稳漂移难题。本章将第 1、2 章建立的模型作为基础，提出新方法。本章首先设计算法，最后验证，为后续提供支撑。\n"
        "\\section{3.1 方法设计}\n"
        "\\end{document}\n"
    )
    logic._DOC = None
    parser = logic.get_parser("main.tex")
    lines = tex.splitlines()
    findings = logic._check_chapter_intro(tex, lines, parser)
    text = "\n".join(findings)
    assert "第三章”章章引言缺少承上衔接" not in text


def test_default_suggestions_are_paragraph_style_neutral() -> None:
    """R5.2: Default chapter intro suggestions do not hardcode '第一段/第二段/两段'."""
    tex_short = (
        "\\documentclass{ctexbook}\n"
        "\\begin{document}\n"
        "\\chapter{第一章 绪论}\n"
        "\\section{1.1 背景}\n"
        "\\chapter{第二章 过程基础}\n"
        "\\section{2.1 基础}\n"
        "\\chapter{第三章 建模方法}\n"
        "短引言。\n"
        "\\section{3.1 方法设计}\n"
        "\\end{document}\n"
    )
    logic._DOC = None
    parser = logic.get_parser("main.tex")
    lines = tex_short.splitlines()
    findings = logic._check_chapter_intro(tex_short, lines, parser)
    text = "\n".join(findings)

    # Observe line is preserved
    assert "章引言过简" in text
    # Suggestion lines must not contain forbidden phrases
    for line in findings:
        if line.startswith("% 建议："):
            assert "第一段" not in line
            assert "第二段" not in line
            assert "两段式" not in line
            assert "扩展为承上启下两段" not in line
            assert "保留承上启下两段" not in line

    tex_long = (
        "\\documentclass{ctexbook}\n"
        "\\begin{document}\n"
        "\\chapter{第一章 绪论}\n"
        "\\section{1.1 背景}\n"
        "\\chapter{第二章 过程基础}\n"
        "\\section{2.1 基础}\n"
        "\\chapter{第三章 建模方法}\n"
        + ("工业过程存在非平稳漂移难题，影响软测量精度。" * 50)
        + "\n\\section{3.1 方法设计}\n"
        "\\end{document}\n"
    )
    findings_long = logic._check_chapter_intro(tex_long, tex_long.splitlines(), parser)
    assert any("章引言过长" in line for line in findings_long)
    for line in findings_long:
        if line.startswith("% 建议："):
            assert "第一段" not in line
            assert "第二段" not in line
            assert "扩展为承上启下两段" not in line
            assert "保留承上启下两段" not in line


def test_ci_style_and_moves_positive_and_negative() -> None:
    """CI-STYLE always reports observed style/moves on non-empty intro; CI-MOVES reports missing moves."""
    # Positive case: full moves
    tex_full = (
        "\\documentclass{ctexbook}\n"
        "\\begin{document}\n"
        "\\chapter{第一章 绪论}\n"
        "\\section{1.1 背景}\n"
        "\\chapter{第二章 基础方法}\n"
        "第二章引言解决基础问题。针对上述难题，本章提出基础模型。本章首先分析，最后验证，为后续提供支撑。\n"
        "\\section{2.1 基础}\n"
        "\\section{2.2 扩展}\n"
        "\\chapter{第三章 算法方法}\n"
        "时序数据存在非平稳漂移瓶颈，影响软测量。第 2 章建立了基础模型。针对该问题，本章提出自适应算法。本章首先设计算法，随后优化，最后完成实验验证，为后续提供支撑。\n"
        "\\section{3.1 详细设计}\n"
        "\\end{document}\n"
    )
    logic._DOC = None
    parser = logic.get_parser("main.tex")
    lines = tex_full.splitlines()
    sections = parser.split_sections(tex_full)
    ranges = [(1, len(lines))]
    findings = logic._check_chapter_intro_style(tex_full, lines, parser, sections, ranges)
    text = "\n".join(findings)

    # Chapter 2 marks 承上:不适用
    assert "第“第二章 基础方法”章章引言段式与要件观察" in text
    assert "承上:不适用" in text
    # Chapter 3 marks 一段式, all ✓
    assert "第“第三章 算法方法”章章引言段式与要件观察" in text
    assert "段式=一段式" in text
    assert "问题:✓ 承上:✓ 方案:✓ 收束或路线:✓" in text
    # No CI-MOVES for full moves
    assert "CI-MOVES" not in text

    # Negative case for moves: missing closing/roadmap
    tex_missing_closing = (
        "\\documentclass{ctexbook}\n"
        "\\begin{document}\n"
        "\\chapter{第一章 绪论}\n"
        "\\section{1.1 背景}\n"
        "\\chapter{第二章 基础方法}\n"
        "\\section{2.1 基础}\n"
        "\\chapter{第三章 算法方法}\n"
        "时序数据存在非平稳漂移瓶颈，影响软测量。第 2 章建立了基础模型。针对该问题，本章提出自适应算法。\n"
        "\\section{3.1 详细设计}\n"
        "\\end{document}\n"
    )
    findings_missing = logic._check_chapter_intro_style(
        tex_missing_closing, tex_missing_closing.splitlines(), parser, sections, ranges
    )
    text_missing = "\n".join(findings_missing)
    assert "CI-MOVES" in text_missing
    assert "缺少要件：收束或路线" in text_missing


def test_ci_long_positive_and_negative() -> None:
    """CI-LONG triggers only when one-paragraph han > 600 and han <= max_chars (900/1600)."""
    # 650 Han characters in a single paragraph
    long_sentences = (
        "工业全流程多工况协同优化控制在现代流程工业中具有重要工程应用价值，但实际生产过程中上游工序与下游单元之间存在强烈的动态耦合与大时滞特性，导致全局操作指标难以在单一时间尺度上实现最优寻优，严重影响了综合生产效益与能效水平。"
        "为此，亟需建立能够统筹多工况动态响应与多变量交互约束的协同优化控制体系，解决多层级决策之间的信息孤岛瓶颈。"
        "第 2 章建立的鲁棒补偿预测模型为动态工况辨识提供了精确的状态基准，但在遭遇多单元协同负荷阶跃调整时，局部稳态设定值与全流程闭环动态跟踪之间仍存在显著的协调冲突与超调风险。"
        "针对上述多工况强耦合协同优化难题，本章基于分层分布式预测控制理论，构建多工况动态闭环协同优化控制方法，用于实现工序级设定值协同寻优与回路级抗扰跟踪的闭环协同。"
        "本方法首先在全流程尺度上构建多目标性能指标函数，将能耗成本与产品合格率转化为多目标优化问题；"
        "其次，设计基于拉格朗日乘子法的双层分布式分解算法，将全局大系统优化问题分解为各工序子系统能够独立并行求解的局部优化子问题，并建立子系统之间的拉格朗日乘子迭代协调通信机制以消除工序间耦合影响；"
        "再次，为应对生产负荷切换带来的暂态不平稳扰动，设计带有约束松弛缓冲区的时变预测控制律，在保证物理设备运行安全的前提下实现负荷快速平稳切换；"
        "最后，在典型工业生产工况仿真平台与半物理实物测试回路中对所提协同优化控制方法进行多场景对比测试，全面评估该算法在多种典型阶跃扰动与模型失配条件下的闭环响应速度与收敛稳定性，实验结果表明全局能耗得到有效降低，为第 4 章全厂综合工程示范应用提供了关键控制支撑。"
    )
    tex_long = (
        "\\documentclass{ctexbook}\n"
        "\\begin{document}\n"
        "\\chapter{第一章 绪论}\n"
        "\\section{1.1 背景}\n"
        "\\chapter{第二章 基础方法}\n"
        "\\section{2.1 基础}\n"
        "\\chapter{第三章 协同优化方法}\n" + long_sentences + "\n\\section{3.1 详细设计}\n"
        "\\end{document}\n"
    )
    logic._DOC = None
    parser = logic.get_parser("main.tex")
    sections = parser.split_sections(tex_long)
    ranges = [(1, len(tex_long.splitlines()))]
    findings = logic._check_chapter_intro_style(
        tex_long, tex_long.splitlines(), parser, sections, ranges
    )
    text = "\n".join(findings)
    assert "CI-LONG" in text
    assert "一段式章引言偏长" in text

    # Han > default lead max (900): default 过长 owns it; CI-LONG must not overlap.
    over_max = "工业过程存在非平稳漂移难题，影响软测量精度。" * 50
    tex_over = (
        "\\documentclass{ctexbook}\n"
        "\\begin{document}\n"
        "\\chapter{第一章 绪论}\n"
        "\\section{1.1 背景}\n"
        "\\chapter{第二章 基础方法}\n"
        "\\section{2.1 基础}\n"
        "\\chapter{第三章 协同优化方法}\n" + over_max + "\n\\section{3.1 详细设计}\n"
        "\\end{document}\n"
    )
    default_over = logic._check_chapter_intro(tex_over, tex_over.splitlines(), parser)
    style_over = logic._check_chapter_intro_style(
        tex_over,
        tex_over.splitlines(),
        parser,
        parser.split_sections(tex_over),
        [(1, len(tex_over.splitlines()))],
    )
    assert any("章引言过长" in line for line in default_over)
    assert "CI-LONG" not in "\n".join(style_over)


def test_ci_section_scoping(tmp_path: Path) -> None:
    """--section restricts chapter intro style findings to target section."""
    tex = (
        "\\documentclass{ctexbook}\n"
        "\\begin{document}\n"
        "\\chapter{第一章 绪论}\n"
        "\\section{1.1 背景}\n"
        "\\chapter{相关工作}\n"
        "既有软测量方法存在漂移难题。本章综述对比代表性工作。本章首先梳理文献，最后给出空白。\n"
        "\\section{2.1 综述}\n"
        "\\chapter{自适应门控状态估计方法}\n"
        "工业过程数据存在非平稳漂移瓶颈，影响软测量。第 2 章综述了基线。针对该问题，本章提出自适应算法。本章首先设计，最后验证，为后续提供支撑。\n"
        "\\section{3.1 方法}\n"
        "\\end{document}\n"
    )
    tex_path = tmp_path / "main.tex"
    tex_path.write_text(tex, encoding="utf-8")
    logic._DOC = None
    report = logic.analyze(tex_path, section="method", chapter_intro_style=True)
    text = "\n".join(report)
    assert "自适应门控状态估计方法" in text
    assert "第“相关工作”章章引言段式与要件观察" not in text


def test_ci_first_chapter() -> None:
    """--first-chapter uses all-chapter index, matching _check_chapter_intro."""
    tex = (
        "\\documentclass{ctexbook}\n"
        "\\begin{document}\n"
        "\\chapter{绪论}\n"
        "\\section{1.1 背景}\n"
        "\\chapter{状态估计方法}\n"
        "工业数据存在漂移难题。本章提出自适应算法。本章首先设计，最后验证，为后续提供支撑。\n"
        "\\section{2.1 设计}\n"
        "\\end{document}\n"
    )
    logic._DOC = None
    parser = logic.get_parser("main.tex")
    sections = parser.split_sections(tex)
    ranges = [(1, len(tex.splitlines()))]

    findings_default = logic._check_chapter_intro_style(
        tex, tex.splitlines(), parser, sections, ranges, first_chapter=None
    )
    assert "承上:不适用" in "\n".join(findings_default)

    # first_chapter=1 -> 状态估计 is chapter 2 (index 1) -> 承上不适用
    findings_ch2 = logic._check_chapter_intro_style(
        tex, tex.splitlines(), parser, sections, ranges, first_chapter=1
    )
    assert "承上:不适用" in "\n".join(findings_ch2)

    # first_chapter=2 -> 状态估计 is chapter 3 (index 1) -> 承上缺失
    findings_ch3 = logic._check_chapter_intro_style(
        tex, tex.splitlines(), parser, sections, ranges, first_chapter=2
    )
    assert "承上:✗" in "\n".join(findings_ch3)


def test_terms_yaml_and_defaults_match_and_fallback(tmp_path: Path) -> None:
    """Verify built-in defaults match YAML, docs mirrors, and per-key fallback."""
    yaml_path = (
        SCRIPT_DIR_ZH.parent / "references" / "writing" / logic.CHAPTER_INTRO_STYLE_TERMS_FILENAME
    )
    assert yaml_path.exists()
    yaml_data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

    for key, expected_tuple in logic.DEFAULT_CHAPTER_INTRO_STYLE_TERMS.items():
        assert tuple(yaml_data[key]) == expected_tuple

    source = yaml_path.read_bytes().replace(b"\r\n", b"\n")
    for rel in (
        "docs/skills/latex-thesis-zh/resources/references/writing/chapter-intro-style-terms.yaml",
        "docs/zh/skills/latex-thesis-zh/resources/references/writing/chapter-intro-style-terms.yaml",
    ):
        mirrored = (REPO_ROOT / rel).read_bytes().replace(b"\r\n", b"\n")
        assert mirrored == source

    fake_writing = tmp_path / "references" / "writing"
    fake_writing.mkdir(parents=True)
    fake_script_dir = tmp_path / "scripts"
    fake_script_dir.mkdir(parents=True)

    corrupted = {
        "problem_markers": ["自定义问题"],
        "solution_markers": "not a list",
    }
    (fake_writing / logic.CHAPTER_INTRO_STYLE_TERMS_FILENAME).write_text(
        yaml.dump(corrupted, allow_unicode=True), encoding="utf-8"
    )

    loaded = logic._load_chapter_intro_style_terms(fake_script_dir)
    assert loaded["problem_markers"] == ("自定义问题",)
    assert loaded["solution_markers"] == logic.DEFAULT_CHAPTER_INTRO_STYLE_TERMS["solution_markers"]
    assert loaded["closing_markers"] == logic.DEFAULT_CHAPTER_INTRO_STYLE_TERMS["closing_markers"]


def test_fixture_run_end_to_end() -> None:
    """AC-09: analyze with --chapter-intro-style on fixture satisfies contract."""
    logic._DOC = None
    report = logic.analyze(_FIXTURE, chapter_intro_style=True)
    text = "\n".join(report)

    # AC-09 assertions
    assert "CI-STYLE" in text
    assert "CI-MOVES" in text
    assert "CI-LONG" in text

    # Chapter 3: 一段式
    assert "第三章 基于自适应门控的状态估计方法”章章引言段式与要件观察" in text
    assert "段式=一段式" in text
    # Chapter 6: 两段式
    assert "第六章 工业综合验证与工程应用方法”章章引言段式与要件观察" in text
    assert "段式=两段式" in text

    # Chapter 4: CI-MOVES
    assert "第四章 动态时序鲁棒预测方法”章章引言缺少核心要件" in text
    # Chapters 3 and 6 do not emit CI-MOVES
    assert "第三章 基于自适应门控的状态估计方法”章章引言缺少核心要件" not in text
    assert "第六章 工业综合验证与工程应用方法”章章引言缺少核心要件" not in text

    # Chapter 5: CI-LONG
    assert "第五章 多工况闭环协同优化方法”章一段式章引言偏长" in text

    # Chapter 2: 承上:不适用
    assert "第二章 过程监测与分析基础方法”章章引言段式与要件观察" in text
    assert "承上:不适用" in text

    # Contract format checks
    assert "Meaning-Check: PRESERVED" not in text
    for i, line in enumerate(report):
        if line.startswith("% 章引言段式"):
            assert "[Script] CI-" in line
            assert "[Severity: Info] [Priority: P3]" in line
            block = "\n".join(report[i : i + 6])
            assert "% Meaning-Check: NEEDS-LLM" in block
        if line.startswith("% Current:"):
            # Check that no whole sentence from fixture is copied
            assert "工业过程数据存在非平稳漂移瓶颈" not in line
            assert "时序数据缺失导致预测精度下降" not in line
            assert "工业全流程多工况协同优化控制在现代流程工业中具有重要工程应用价值" not in line
