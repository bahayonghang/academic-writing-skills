"""Regression tests for latex-thesis-zh script behaviors."""

import importlib.util
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

# ZH scripts dir — must be first on sys.path during ZH module loading
# so intra-package imports (e.g. `from parsers import get_parser`) resolve to ZH versions
_ZH_DIR = Path(__file__).parent.parent / "academic-writing-skills" / "latex-thesis-zh" / "scripts"
_EN_DIR = Path(__file__).parent.parent / "academic-writing-skills" / "latex-paper-en" / "scripts"


def _load_zh(name: str):
    """Load a module from the ZH scripts directory by file path.

    Temporarily puts ZH dir first on sys.path so internal imports resolve correctly.
    """
    # Ensure ZH is first for intra-module imports
    zh_str = str(_ZH_DIR)
    inserted = False
    if zh_str not in sys.path or sys.path.index(zh_str) != 0:
        sys.path.insert(0, zh_str)
        inserted = True

    # Remove any cached bare modules that collide (parsers, compile, etc.)
    for mod_name in list(sys.modules):
        if mod_name in ("parsers", "compile", "verify_bib", "optimize_title", "map_structure"):
            cached_file = getattr(sys.modules[mod_name], "__file__", "") or ""
            if _EN_DIR.name in cached_file or "latex-paper-en" in cached_file:
                del sys.modules[mod_name]

    spec = importlib.util.spec_from_file_location(f"zh_{name}", _ZH_DIR / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

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
