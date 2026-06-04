"""Regression tests for latex-thesis-zh script behaviors."""

import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

# ZH scripts dir — must be first on sys.path during ZH module loading
# so intra-package imports (e.g. `from parsers import get_parser`) resolve to ZH versions
_ZH_DIR = Path(__file__).parent.parent / "academic-writing-skills" / "latex-thesis-zh" / "scripts"


def _load_zh(name: str):
    """Load a module from the ZH scripts directory by file path.

    Temporarily puts ZH dir first on sys.path so internal imports resolve correctly.
    Uses save/restore to prevent sys.modules pollution across test suites.
    """
    # Ensure ZH is first for intra-module imports
    zh_str = str(_ZH_DIR)
    inserted = False
    if zh_str not in sys.path or sys.path.index(zh_str) != 0:
        sys.path.insert(0, zh_str)
        inserted = True

    # Save and remove collision-prone modules so ZH versions get loaded fresh
    _collision_names = ("parsers", "compile", "verify_bib", "optimize_title", "map_structure")
    _saved = {}
    for mod_name in list(sys.modules):
        if mod_name in _collision_names:
            _saved[mod_name] = sys.modules.pop(mod_name)

    spec = importlib.util.spec_from_file_location(f"zh_{name}", _ZH_DIR / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # Restore original modules to prevent cross-suite pollution
    for mod_name in _collision_names:
        if mod_name in sys.modules and mod_name not in _saved:
            del sys.modules[mod_name]
        if mod_name in _saved:
            sys.modules[mod_name] = _saved[mod_name]

    # Restore sys.path: put EN back first for other test files
    if inserted and zh_str in sys.path:
        sys.path.remove(zh_str)
        sys.path.append(zh_str)

    return mod


deai_check = _load_zh("deai_check")
detect_template = _load_zh("detect_template")
map_structure = _load_zh("map_structure")
check_consistency = _load_zh("check_consistency")
optimize_title_zh = _load_zh("optimize_title")
compile_zh = _load_zh("compile")
verify_bib_zh = _load_zh("verify_bib")
parsers_zh = _load_zh("parsers")
analyze_logic_zh = _load_zh("analyze_logic")
analyze_literature_zh = _load_zh("analyze_literature")
analyze_experiment_zh = _load_zh("analyze_experiment")


# ── deai_check.py ──────────────────────────────────────────────


class TestDeaiCheck:
    """Tests for ChineseAITraceChecker regex and detection."""

    def test_template_expressions_regex_compile(self):
        """All TEMPLATE_EXPRESSIONS patterns must compile without error."""
        for pattern in deai_check.ChineseAITraceChecker.TEMPLATE_EXPRESSIONS:
            re.compile(pattern)

    def test_empty_phrases_match(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n本文方法取得了显著提升，全面分析了问题。\n",
            encoding="utf-8",
        )
        checker = deai_check.ChineseAITraceChecker(tex)
        result = checker.check_section("introduction")
        assert result["trace_count"] >= 1

    def test_false_positive_with_number(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n显著提升了12.5%的准确率。\n",
            encoding="utf-8",
        )
        checker = deai_check.ChineseAITraceChecker(tex)
        result = checker.check_section("introduction")
        # Should be filtered as false positive (number follows)
        assert result["trace_count"] == 0

    def test_density_score_calculation(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("\\chapter{绪论}\nline1\nline2\nline3\n", encoding="utf-8")
        checker = deai_check.ChineseAITraceChecker(tex)
        result = {"total_lines": 10, "trace_count": 2, "traces": []}
        score = checker.calculate_density_score(result)
        assert score == pytest.approx(20.0)

    def test_density_score_zero_lines(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("", encoding="utf-8")
        checker = deai_check.ChineseAITraceChecker(tex)
        result = {"total_lines": 0, "trace_count": 0, "traces": []}
        assert checker.calculate_density_score(result) == 0.0

    def test_template_expression_match(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n近年来，随着科技的快速发展，越来越多的研究关注此问题。\n",
            encoding="utf-8",
        )
        checker = deai_check.ChineseAITraceChecker(tex)
        result = checker.check_section("introduction")
        assert result["trace_count"] >= 2  # 近年来 + 越来越多的 + 随着...发展


# ── detect_template.py ─────────────────────────────────────────


class TestDetectTemplate:
    """Tests for template detection."""

    def test_thuthesis_detection(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\documentclass{thuthesis}\n\\begin{document}\n\\end{document}", encoding="utf-8"
        )
        mapper = map_structure.ThesisStructureMapper(str(tex))
        mapper.map()
        assert mapper.template == "thuthesis"

    def test_pkuthss_detection(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\documentclass{pkuthss}\n\\begin{document}\n\\end{document}", encoding="utf-8"
        )
        mapper = map_structure.ThesisStructureMapper(str(tex))
        mapper.map()
        assert mapper.template == "pkuthss"

    def test_ctexbook_detection(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\documentclass{ctexbook}\n\\begin{document}\n\\end{document}", encoding="utf-8"
        )
        mapper = map_structure.ThesisStructureMapper(str(tex))
        mapper.map()
        assert mapper.template == "ctexbook"


# ── map_structure.py ───────────────────────────────────────────


class TestMapStructure:
    """Tests for ThesisStructureMapper."""

    def test_basic_structure_mapping(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\documentclass{ctexbook}\n\\begin{document}\n"
            "\\chapter{绪论}\n内容\n\\chapter{结论}\n总结\n\\end{document}",
            encoding="utf-8",
        )
        mapper = map_structure.ThesisStructureMapper(str(tex))
        structure = mapper.map()
        assert len(structure) >= 1

    def test_template_info(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\documentclass{thuthesis}\n\\begin{document}\\end{document}", encoding="utf-8"
        )
        mapper = map_structure.ThesisStructureMapper(str(tex))
        mapper.map()
        info = mapper.get_template_info()
        assert info is not None
        assert "Tsinghua" in info["name"]


# ── check_consistency.py ───────────────────────────────────────


class TestCheckConsistency:
    """Tests for ConsistencyChecker."""

    def test_detects_term_inconsistency(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "深度学习是一种方法。深层学习也被广泛使用。",
            encoding="utf-8",
        )
        checker = check_consistency.ConsistencyChecker([str(tex)])
        result = checker.check_terms()
        assert result["status"] == "WARNING"
        assert len(result["inconsistencies"]) >= 1

    def test_no_inconsistency_when_consistent(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("深度学习是一种方法。深度学习被广泛使用。", encoding="utf-8")
        checker = check_consistency.ConsistencyChecker([str(tex)])
        result = checker.check_terms()
        assert result["status"] == "PASS"

    def test_abbreviation_undefined(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("本文使用 BERT 模型进行实验。", encoding="utf-8")
        checker = check_consistency.ConsistencyChecker([str(tex)])
        result = checker.check_abbreviations()
        assert any(i["abbreviation"] == "BERT" for i in result["issues"])

    def test_abbreviation_defined(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "双向编码器表示（BERT）是一种预训练模型。本文使用 BERT 进行实验。",
            encoding="utf-8",
        )
        checker = check_consistency.ConsistencyChecker([str(tex)])
        result = checker.check_abbreviations()
        # BERT is defined, so no "undefined" issue for it
        undefined = [
            i for i in result["issues"] if i["type"] == "undefined" and i["abbreviation"] == "BERT"
        ]
        assert len(undefined) == 0

    def test_custom_terms_loading(self, tmp_path: Path):
        terms_file = tmp_path / "terms.json"
        terms_file.write_text('{"zh": [["自编码器", "AE"]], "en": []}', encoding="utf-8")
        tex = tmp_path / "main.tex"
        tex.write_text("自编码器和AE都出现了。", encoding="utf-8")
        checker = check_consistency.ConsistencyChecker(
            [str(tex)], custom_terms_file=str(terms_file)
        )
        result = checker.check_terms()
        assert result["status"] == "WARNING"


# ── optimize_title.py ──────────────────────────────────────────


class TestOptimizeTitle:
    """Tests for title scoring and optimization."""

    def test_score_title_ineffective_words(self):
        score_data = optimize_title_zh.score_title("关于基于深度学习的时间序列预测的研究")
        assert score_data["total"] < 80
        assert any("无效词汇" in issue for issue in score_data["issues"])

    def test_score_title_good_title(self):
        score_data = optimize_title_zh.score_title("Transformer时间序列预测方法")
        assert score_data["total"] >= 60

    def test_count_chinese_chars(self):
        assert optimize_title_zh.count_chinese_chars("深度学习方法") == 6
        assert optimize_title_zh.count_chinese_chars("LSTM模型") == 2

    def test_optimize_removes_ineffective_words(self):
        result = optimize_title_zh.optimize_title("关于基于深度学习的研究")
        assert "关于" not in result
        assert "的研究" not in result

    def test_generate_candidates(self):
        keywords = {"method": ["Transformer"], "problem": ["预测"], "domain": ["工业"]}
        candidates = optimize_title_zh.generate_title_candidates(keywords)
        assert len(candidates) >= 1
        assert any("Transformer" in c[0] for c in candidates)


# ── parsers.py (zh) ───────────────────────────────────────────


class TestParsersZh:
    """Tests for Chinese thesis parsers."""

    def test_extract_title_ctitle(self):
        content = "\\ctitle{基于深度学习的时间序列预测方法}"
        assert "时间序列预测" in parsers_zh.extract_title(content)

    def test_extract_title_standard(self):
        content = "\\title{深度学习方法研究}"
        assert "深度学习" in parsers_zh.extract_title(content)

    def test_extract_title_empty(self):
        assert parsers_zh.extract_title("no title here") == ""

    def test_extract_abstract_cabstract(self):
        content = "\\begin{cabstract}本文研究了深度学习方法。\\end{cabstract}"
        result = parsers_zh.extract_abstract(content)
        assert "深度学习" in result

    def test_extract_abstract_standard(self):
        content = "\\begin{abstract}本文提出一种新方法。\\end{abstract}"
        result = parsers_zh.extract_abstract(content)
        assert "新方法" in result

    def test_extract_abstract_empty(self):
        assert parsers_zh.extract_abstract("no abstract") == ""

    def test_latex_parser_split_sections(self):
        content = "前言\n\\chapter{绪论}\n内容1\n\\chapter{结论}\n内容2"
        parser = parsers_zh.LatexParser()
        sections = parser.split_sections(content)
        assert "introduction" in sections
        assert "conclusion" in sections

    def test_typst_parser_split_sections(self):
        content = "前言\n= 绪论\n内容1\n= 结论\n内容2"
        parser = parsers_zh.TypstParser()
        sections = parser.split_sections(content)
        assert "introduction" in sections
        assert "conclusion" in sections

    def test_get_parser_latex(self):
        parser = parsers_zh.get_parser("main.tex")
        assert isinstance(parser, parsers_zh.LatexParser)

    def test_get_parser_typst(self):
        parser = parsers_zh.get_parser("main.typ")
        assert isinstance(parser, parsers_zh.TypstParser)

    def test_extract_latex_headings(self):
        content = (
            "\\chapter{绪论}\n"
            "\\section{研究背景}\n"
            "\\subsection{问题定义}\n"
            "\\subsubsection{数据来源}\n"
        )
        parser = parsers_zh.LatexParser()
        headings = parser.extract_headings(content)
        assert [heading["command"] for heading in headings] == [
            "chapter",
            "section",
            "subsection",
            "subsubsection",
        ]

    def test_extract_typst_headings(self):
        content = "= 绪论\n== 研究背景\n=== 问题定义\n==== 数据来源\n"
        parser = parsers_zh.TypstParser()
        headings = parser.extract_headings(content)
        assert [heading["level"] for heading in headings] == [1, 2, 3, 4]


# ── compile.py (zh) ───────────────────────────────────────────


class TestCompileZh:
    """Tests for LaTeX compiler (Chinese thesis)."""

    def test_detect_chinese_content(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\documentclass{ctexbook}\n\\begin{document}你好\\end{document}", encoding="utf-8"
        )
        compiler = compile_zh.LaTeXCompiler(str(tex))
        assert compiler.compiler == "xelatex"

    def test_detect_xecjk(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("\\usepackage{xeCJK}\n\\begin{document}\\end{document}", encoding="utf-8")
        compiler = compile_zh.LaTeXCompiler(str(tex))
        assert compiler.compiler == "xelatex"

    def test_recipe_selection(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\documentclass{article}\\begin{document}x\\end{document}", encoding="utf-8"
        )
        tex.with_suffix(".pdf").write_bytes(b"%PDF-1.4\n")

        calls: list[list[str]] = []

        def fake_run(cmd, cwd=None, capture_output=False):
            calls.append(cmd)
            return SimpleNamespace(returncode=0)

        monkeypatch.setattr(compile_zh.shutil, "which", lambda _: "/usr/bin/fake")
        monkeypatch.setattr(compile_zh.subprocess, "run", fake_run)

        compiler = compile_zh.LaTeXCompiler(str(tex), recipe="xelatex-biber")
        code = compiler.compile()
        assert code == 0
        assert compiler.recipe == "xelatex-biber"
        assert any("biber" in str(cmd) for cmd in calls)

    def test_shell_escape_requires_trusted_source(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\documentclass{ctexbook}\\begin{document}你好\\end{document}", encoding="utf-8"
        )

        result = subprocess.run(
            [sys.executable, "-B", str(_ZH_DIR / "compile.py"), str(tex), "--shell-escape"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 1
        assert "--trusted-source" in result.stdout


# ── verify_bib.py (zh) ────────────────────────────────────────


class TestVerifyBibZh:
    """Tests for BibTeX verification."""

    def test_required_fields_check(self, tmp_path: Path):
        bib = tmp_path / "refs.bib"
        bib.write_text(
            "@article{key1, title={Title}, year={2020}}",
            encoding="utf-8",
        )
        verifier = verify_bib_zh.BibTeXVerifier(str(bib))
        result = verifier.verify()
        # Missing author and journal
        assert result["status"] == "FAIL"
        missing = [i for i in result["issues"] if i["type"] == "missing_field"]
        assert len(missing) >= 2

    def test_valid_entry_passes(self, tmp_path: Path):
        bib = tmp_path / "refs.bib"
        bib.write_text(
            "@article{key1, title={Title}, author={Author}, journal={Journal}, year={2020}}",
            encoding="utf-8",
        )
        verifier = verify_bib_zh.BibTeXVerifier(str(bib))
        result = verifier.verify()
        assert result["valid_entries"] == 1

    def test_duplicate_detection(self, tmp_path: Path):
        bib = tmp_path / "refs.bib"
        bib.write_text(
            "@article{key1, title={T1}, author={A}, journal={J}, year={2020}}\n"
            "@article{key1, title={T2}, author={B}, journal={J}, year={2021}}",
            encoding="utf-8",
        )
        verifier = verify_bib_zh.BibTeXVerifier(str(bib))
        verifier.parse()
        keys = [e["key"] for e in verifier.entries]
        assert keys.count("key1") == 2


# ── analyze_logic.py (WP1: Chinese Literature Review Quality) ──


class TestAnalyzeLogicZh:
    """Tests for Chinese literature review quality checks."""

    def test_detects_chinese_author_enumeration(self, tmp_path: Path):
        """A1: Flag 3+ consecutive author/year enumeration in Chinese."""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{相关工作}\n"
            "张三（2019）提出了一种基于注意力的方法。\n"
            "李四（2020）提出了图神经网络方案。\n"
            "王五（2021）提出了混合架构方法。\n"
            "赵六（2022）提出了高效剪枝策略。\n",
            encoding="utf-8",
        )
        findings = analyze_logic_zh.analyze(tex, "related")
        joined = "\n".join(findings)
        assert "枚举" in joined or "罗列" in joined or "enumeration" in joined.lower()

    def test_detects_missing_gap_derivation_zh(self, tmp_path: Path):
        """A3: Flag Related Work lacking gap language in Chinese."""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{相关工作}\n"
            "现有方法在图像分类任务中取得了不错的效果。\n"
            "上述方法各有优势和特点。\n"
            "这些技术为本领域的发展做出了贡献。\n",
            encoding="utf-8",
        )
        findings = analyze_logic_zh.analyze(tex, "related")
        joined = "\n".join(findings)
        assert "空白" in joined or "gap" in joined.lower()

    def test_marks_borderline_comparative_synthesis_zh_for_review(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{相关工作}\n"
            "张三（2019）提出了一种注意力方法。\n"
            "李四（2020）提出了图神经网络方案。\n"
            "王五（2021）提出了混合架构方法。\n"
            "赵六（2022）提出了高效剪枝策略。\n",
            encoding="utf-8",
        )
        findings = analyze_literature_zh.analyze(tex, "related")
        joined = "\n".join(findings)
        assert "Needs Review" in joined

    def test_detects_repeated_missing_comparative_synthesis_zh(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{相关工作}\n"
            "张三（2019）提出了一种注意力方法。\n"
            "李四（2020）提出了图神经网络方案。\n"
            "\n"
            "王五（2021）提出了混合架构方法。\n"
            "赵六（2022）提出了高效剪枝策略。\n",
            encoding="utf-8",
        )
        findings = analyze_literature_zh.analyze(tex, "related")
        joined = "\n".join(findings)
        assert "多个引文密集段落" in joined

    def test_detects_missing_heading_lead_before_list(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{方法设计}\n"
            "\\section{总体流程}\n"
            "\\begin{itemize}\n"
            "\\item 数据预处理\n"
            "\\item 模型训练\n"
            "\\end{itemize}\n",
            encoding="utf-8",
        )
        findings = analyze_logic_zh.analyze(tex)
        joined = "\n".join(findings)
        assert "缺少导语段落" in joined

    def test_detects_weak_heading_lead_when_too_short(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{实验分析}\n"
            "如下。\n"
            "\\section{结果对比}\n"
            "说明如下。\n"
            "\\subsection{主结果}\n"
            "下面从准确率和召回率两个方面展开分析。\n",
            encoding="utf-8",
        )
        findings = analyze_logic_zh.analyze(tex)
        joined = "\n".join(findings)
        assert "导语可能过短" in joined
        assert "主结果" not in joined

    def test_detects_thesis_mainline_breaks(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n研究背景如下。\n"
            "\\chapter{方法一}\n本章介绍第一个工作并展示结果。\n"
            "\\chapter{方法二}\n本章介绍第二个工作并展示结果。\n"
            "\\chapter{结论}\n总结全文。\n",
            encoding="utf-8",
        )
        findings = analyze_logic_zh.analyze(tex)
        joined = "\n".join(findings)
        assert "章节主线" in joined

    def test_detects_abstract_contribution_conclusion_misalignment(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\begin{abstract}\n本文研究工业预测问题，并提出了一种稀疏模型。\n\\end{abstract}\n"
            "\\chapter{创新点}\n本文的主要贡献在于提出一种新模型并验证其效率优势。\n"
            "\\chapter{结论}\n未来工作将考虑更多场景。\n",
            encoding="utf-8",
        )
        findings = analyze_logic_zh.analyze(tex)
        joined = "\n".join(findings)
        assert "摘要、创新点/贡献来源、结论之间可能存在错位" in joined

    def test_motivation_thread_flags_untested_promise(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n本文提出 FastFormer，一种稀疏注意力机制以降低推理延迟。\n"
            "\\chapter{实验}\n训练数据集包含五万个气象样本，覆盖三年观测。\n"
            "\\chapter{结论}\n该气象数据集将支撑未来研究。\n",
            encoding="utf-8",
        )
        findings = analyze_logic_zh.analyze(tex, motivation_thread=True)
        joined = "\n".join(findings)
        assert "动机主线：承诺映射" in joined
        assert "[未找到证据]" in joined

    def test_motivation_thread_matches_closed_loop(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n本文提出 FastFormer，一种稀疏注意力机制以降低推理延迟。\n"
            "\\chapter{实验}\nFastFormer 通过稀疏注意力将推理延迟降低了 42\\%。\n"
            "\\chapter{结论}\n本文证明了 FastFormer 借助稀疏注意力显著降低推理延迟。\n",
            encoding="utf-8",
        )
        findings = analyze_logic_zh.analyze(tex, motivation_thread=True)
        joined = "\n".join(findings)
        assert "[已匹配" in joined
        assert "[已闭合" in joined
        assert "[未找到证据]" not in joined
        assert "[未闭合]" not in joined

    def test_motivation_thread_off_by_default(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n本文提出 FastFormer 以降低推理延迟。\n"
            "\\chapter{结论}\n本文证明了方法有效。\n",
            encoding="utf-8",
        )
        findings = analyze_logic_zh.analyze(tex)
        assert "动机主线" not in "\n".join(findings)


# ── deai_check.py (WP6: AI Filler Connectors + Parallel) ──────


class TestDeaiCheckEnhanced:
    """Tests for C1/C2 AI marker supplements."""

    def test_deai_detects_filler_connectors(self, tmp_path: Path):
        """C1: Detect AI filler connectors like 总之, 综上所述."""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{结论}\n"
            "总之，本文提出了一种新方法。\n"
            "综上所述，实验结果验证了方法的有效性。\n"
            "值得注意的是，该方法具有较好的泛化能力。\n",
            encoding="utf-8",
        )
        checker = deai_check.ChineseAITraceChecker(tex)
        result = checker.check_section("conclusion")
        assert result["trace_count"] >= 2

    def test_deai_detects_parallel_sentences(self, tmp_path: Path):
        """C2: Detect 3+ consecutive lines with same opening pattern."""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n"
            "本文首先分析了数据预处理的关键步骤。\n"
            "本文接着验证了模型的有效性。\n"
            "本文最后证明了方法的泛化能力。\n"
            "本文还探讨了未来的研究方向。\n",
            encoding="utf-8",
        )
        checker = deai_check.ChineseAITraceChecker(tex)
        result = checker.check_section("introduction")
        parallel = [t for t in result["traces"] if t["category"] == "parallel_structure"]
        assert len(parallel) >= 1

    def test_deai_detects_low_information_density(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n近年来，该问题引起了广泛关注。\n"
            "本文具有重要意义。\n"
            "本文开展了全面研究。\n"
            "本文取得了显著提升。\n",
            encoding="utf-8",
        )
        checker = deai_check.ChineseAITraceChecker(tex)
        result = checker.check_section("introduction")
        categories = {trace["category"] for trace in result["traces"]}
        assert "low_information_density" in categories

    _UNIFORM = (
        "\\chapter{绪论}\n"
        "模型在数据上训练。模型在数据上测试。模型在数据上调优。"
        "模型在数据上评分。模型在磁盘上保存。模型再次被加载。\n"
    )

    def test_tier_flags_uniform_sentence_length(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(self._UNIFORM, encoding="utf-8")
        checker = deai_check.ChineseAITraceChecker(tex, tier="heavy")
        result = checker.check_section("introduction")
        assert any(t["category"] == "sentence_length" for t in result["traces"])

    def test_tier_default_omits_tier_only_checks(self, tmp_path: Path):
        """回归保护：不传 --tier 时不应出现 D1 与维度标签。"""
        tex = tmp_path / "main.tex"
        tex.write_text(self._UNIFORM, encoding="utf-8")
        checker = deai_check.ChineseAITraceChecker(tex)
        result = checker.check_section("introduction")
        assert not any(t["category"] == "sentence_length" for t in result["traces"])
        suggestions = checker.generate_suggestions_json(checker.analyze_document())
        assert all("dimension" not in s for s in suggestions)

    def test_tier_adds_dimension_labels(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n近年来，该问题引起了广泛关注。\n"
            "本文具有重要意义。\n本文开展了全面研究。\n本文取得了显著提升。\n",
            encoding="utf-8",
        )
        checker = deai_check.ChineseAITraceChecker(tex, tier="medium")
        suggestions = checker.generate_suggestions_json(checker.analyze_document())
        assert any(s.get("dimension") for s in suggestions)


def test_analyze_experiment_flags_unlayered_discussion_zh(tmp_path: Path):
    tex = tmp_path / "main.tex"
    tex.write_text(
        "\\chapter{讨论}\n模型在数据集A上的准确率为95.2%。\n"
        "模型在数据集B上的准确率为94.8%。\n"
        "模型在数据集C上的准确率为94.1%。\n"
        "宏平均F1分别为0.92、0.90和0.89。\n"
        "整体结果较好。\n"
        "实验数值如上所示。\n",
        encoding="utf-8",
    )
    findings = analyze_experiment_zh.analyze(tex, "discussion")
    joined = "\n".join(findings)
    assert "layered structure" in joined


# ── deai_check.py (Stage 1 — data-driven AI tone checkers, ZH) ────────────────


def _ai_tone_sample_zh(tmp_path: Path) -> Path:
    tex = tmp_path / "ai_tone_zh.tex"
    tex.write_text(
        "\\chapter{绪论}\n"
        "近年来，深度学习取得了显著进展。本文提出一种新颖方法。\n"
        "首先，模型架构是核心，关键模块的核心思想是核心层的核心创新！\n"
        "\n"
        "首先，我们设计了第一阶段。\n"
        "\n"
        "首先，我们设计了第二阶段。\n"
        "\n"
        "首先，我们设计了第三阶段。\n"
        "\n"
        "综上所述，本文的研究是全面深入的。\n"
        "\n"
        "由此可见，这种设计是核心中的核心！\n",
        encoding="utf-8",
    )
    return tex


def test_deai_zh_term_threshold_flags_chinese_term(tmp_path: Path) -> None:
    tex = _ai_tone_sample_zh(tmp_path)
    checker = deai_check.ChineseAITraceChecker(tex)
    analysis = checker.analyze_document()
    cats = {t["category"] for t in analysis["document_traces"]}
    assert "term_threshold" in cats
    core_hits = [t for t in analysis["document_traces"] if "核心" in t["pattern"]]
    assert core_hits, "expected '核心' to exceed per-doc cap"


def test_deai_zh_burstiness_flags_repeated_opening(tmp_path: Path) -> None:
    tex = _ai_tone_sample_zh(tmp_path)
    checker = deai_check.ChineseAITraceChecker(tex)
    result = checker.check_section("introduction")
    cats = {t["category"] for t in result["traces"]}
    assert "burstiness" in cats


def test_deai_zh_throat_clearing_flags_summary_lead(tmp_path: Path) -> None:
    tex = _ai_tone_sample_zh(tmp_path)
    checker = deai_check.ChineseAITraceChecker(tex)
    result = checker.check_section("introduction")
    patterns = {t["pattern"] for t in result["traces"] if t["category"] == "throat_clearing"}
    assert any("综上所述" in p or "由此可见" in p or "首先" in p for p in patterns)


def test_deai_zh_punctuation_flags_chinese_exclamation(tmp_path: Path) -> None:
    tex = _ai_tone_sample_zh(tmp_path)
    checker = deai_check.ChineseAITraceChecker(tex)
    analysis = checker.analyze_document()
    excl = [
        t for t in analysis["document_traces"] if t["pattern"] == "punctuation:exclamation_in_body"
    ]
    assert excl, "expected exclamation in body to be flagged"
