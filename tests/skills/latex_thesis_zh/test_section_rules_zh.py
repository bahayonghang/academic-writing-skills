"""Regression coverage for audited latex-thesis-zh section and title rules."""

import importlib.util
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH


def _load_zh(name: str):
    saved_path = list(sys.path)
    collisions = ("parsers", "tex_loader")
    saved = {module: sys.modules.pop(module, None) for module in collisions}
    try:
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec = importlib.util.spec_from_file_location(
            f"zh_audit_{name}", SCRIPT_DIR_ZH / f"{name}.py"
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for module, value in saved.items():
            if value is None:
                sys.modules.pop(module, None)
            else:
                sys.modules[module] = value


parsers = _load_zh("parsers")
analyze_conclusion = _load_zh("analyze_conclusion")
compile_zh = _load_zh("compile")
check_spec = _load_zh("check_spec")


def test_loader_guard_and_conclusion_alias() -> None:
    assert parsers.SECTION_KEY_ALIASES["结论与展望"] == "conclusion"


def test_latex_and_typst_conclusion_rules_are_exact() -> None:
    positives = ("结论", "总结", "结论与展望", "总结与展望")
    negatives = ("结论性章节", "实验结论分析", "总结报告")
    for title in positives:
        assert "conclusion" in parsers.LatexParser().split_sections(f"\\chapter{{{title}}}\n正文")
        assert "conclusion" in parsers.TypstParser().split_sections(f"= {title}\n正文")
    for title in negatives:
        assert "conclusion" not in parsers.LatexParser().split_sections(
            f"\\chapter{{{title}}}\n正文"
        )
        assert "conclusion" not in parsers.TypstParser().split_sections(f"= {title}\n正文")


def test_standalone_latex_conclusion_section_remains_supported() -> None:
    assert "conclusion" in parsers.LatexParser().split_sections("\\section{总结}\n正文")


def test_conclusion_analyzer_no_longer_skips_named_fixture(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text("\\chapter{结论与展望}\n本文总结工作并提出未来研究方向。\n", encoding="utf-8")
    result = analyze_conclusion.ConclusionAnalyzer(str(tex)).analyze()
    assert result.status != "SKIP"
    assert "未识别到结论" not in result.message


def test_balanced_heading_and_title_extraction() -> None:
    content = r"\chapter{基于\textbf{X}的方法}" + "\n"
    assert parsers.LatexParser().extract_headings(content)[0]["title"] == r"基于\textbf{X}的方法"
    assert parsers.extract_title(r"\ctitle{基于\textbf{深度学习}的方法}") == "基于深度学习的方法"


def test_nested_long_title_triggers_spec_limit(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        r"\ctitle{基于\textbf{深度学习方法研究}的复杂工业系统智能优化控制与安全决策研究}",
        encoding="utf-8",
    )
    ctx = check_spec.SpecContext(tex, "master", "thuthesis", None, 2026)
    status, evidence = check_spec.check_title_len(ctx)
    assert status == "FAIL"
    assert "深度学习方法研究" in evidence


def test_explicit_lualatex_wins_and_gbk_chinese_is_detected(tmp_path: Path) -> None:
    explicit = tmp_path / "explicit.tex"
    explicit.write_text("% !TEX program = lualatex\n\\documentclass{ctexbook}\n", encoding="utf-8")
    assert compile_zh.LaTeXCompiler(str(explicit)).compiler == "lualatex"

    gbk = tmp_path / "gbk.tex"
    gbk.write_bytes(
        "\\documentclass{article}\n\\begin{document}中文正文\\end{document}".encode("gb18030")
    )
    assert compile_zh.LaTeXCompiler(str(gbk)).compiler == "xelatex"
