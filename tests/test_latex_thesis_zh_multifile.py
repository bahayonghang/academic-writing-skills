"""Regression tests for latex-thesis-zh multi-file assembly & section splitting.

Covers the P0 audit fixes (F3/F4/F11/F22):
- tex_loader assembles \\include skeletons with source-location mapping;
- split_sections no longer overwrites duplicate keys, follows commented-out
  headings, or misses starred/spaced titles;
- ``--section`` accepts Chinese section names and lists alternatives;
- GB18030-encoded sources are decoded (with an explicit warning) instead of
  being silently mangled.
"""

import importlib.util
import sys
from pathlib import Path

_ZH_DIR = Path(__file__).parent.parent / "academic-writing-skills" / "latex-thesis-zh" / "scripts"


def _load_zh(name: str):
    """Load a ZH script by path with ZH dir first on sys.path (see
    test_latex_thesis_zh_scripts._load_zh for the save/restore rationale)."""
    zh_str = str(_ZH_DIR)
    inserted = False
    if zh_str not in sys.path or sys.path.index(zh_str) != 0:
        sys.path.insert(0, zh_str)
        inserted = True

    _collision_names = ("parsers", "tex_loader")
    _saved = {}
    for mod_name in list(sys.modules):
        if mod_name in _collision_names:
            _saved[mod_name] = sys.modules.pop(mod_name)

    spec = importlib.util.spec_from_file_location(f"zh_mf_{name}", _ZH_DIR / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    # Register before exec: dataclasses resolves string annotations through
    # sys.modules[cls.__module__] (PEP 563 semantics).
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)

    for mod_name in _collision_names:
        if mod_name in sys.modules and mod_name not in _saved:
            del sys.modules[mod_name]
        if mod_name in _saved:
            sys.modules[mod_name] = _saved[mod_name]

    if inserted and zh_str in sys.path:
        sys.path.remove(zh_str)
        sys.path.append(zh_str)

    return mod


tex_loader = _load_zh("tex_loader")
parsers_zh = _load_zh("parsers")
analyze_logic_zh = _load_zh("analyze_logic")
deai_check_zh = _load_zh("deai_check")
check_consistency_zh = _load_zh("check_consistency")


# ── fixtures ──────────────────────────────────────────────────


def _write_multifile_project(tmp_path: Path) -> Path:
    """Minimal thuthesis-style skeleton: main.tex only \\include's chapters."""
    (tmp_path / "chapters").mkdir()
    main = tmp_path / "main.tex"
    main.write_text(
        "\\documentclass{thuthesis}\n"
        "\\begin{document}\n"
        "\\include{chapters/intro}\n"
        "\\include{chapters/method}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    (tmp_path / "chapters" / "intro.tex").write_text(
        "\\chapter{绪论}\n"
        "近年来，该领域发展迅速。\n"
        "\\section{研究背景}\n"
        "\\begin{itemize}\n"
        "\\item 背景一\n"
        "\\end{itemize}\n",
        encoding="utf-8",
    )
    (tmp_path / "chapters" / "method.tex").write_text(
        "\\chapter{稀疏注意力方法}\n本章提出一种方法。\n",
        encoding="utf-8",
    )
    return main


# ── tex_loader ────────────────────────────────────────────────


class TestTexLoader:
    def test_assemble_expands_includes_in_order(self, tmp_path: Path):
        main = _write_multifile_project(tmp_path)
        doc = tex_loader.assemble(main)
        assert doc.multi_file
        assert "\\chapter{绪论}" in doc.content
        assert "\\chapter{稀疏注意力方法}" in doc.content
        assert doc.content.index("绪论") < doc.content.index("稀疏注意力方法")

    def test_origin_maps_back_to_source_file(self, tmp_path: Path):
        main = _write_multifile_project(tmp_path)
        doc = tex_loader.assemble(main)
        line_no = next(i for i, line in enumerate(doc.lines, 1) if "绪论" in line)
        src, src_line = doc.origin(line_no)
        assert src == "chapters/intro.tex"
        assert src_line == 1

    def test_missing_include_is_reported_not_silent(self, tmp_path: Path):
        main = tmp_path / "main.tex"
        main.write_text("\\include{chapters/ghost}\n", encoding="utf-8")
        doc = tex_loader.assemble(main)
        assert doc.missing, "missing include must be recorded"
        warn = "\n".join(doc.warning_lines("%"))
        assert "ghost" in warn

    def test_commented_include_is_not_expanded(self, tmp_path: Path):
        (tmp_path / "old.tex").write_text("\\chapter{废稿}\n", encoding="utf-8")
        main = tmp_path / "main.tex"
        main.write_text("% \\include{old}\n正文\n", encoding="utf-8")
        doc = tex_loader.assemble(main)
        assert "废稿" not in doc.content

    def test_circular_include_terminates(self, tmp_path: Path):
        a = tmp_path / "a.tex"
        b = tmp_path / "b.tex"
        a.write_text("A\n\\input{b}\n", encoding="utf-8")
        b.write_text("B\n\\input{a}\n", encoding="utf-8")
        doc = tex_loader.assemble(a)
        assert "A" in doc.content and "B" in doc.content

    def test_gb18030_file_decoded_with_warning(self, tmp_path: Path):
        main = tmp_path / "main.tex"
        main.write_bytes("\\chapter{绪论}\n这是国标编码正文。\n".encode("gb18030"))
        doc = tex_loader.assemble(main)
        assert "这是国标编码正文" in doc.content, "GB18030 content must decode, not mojibake"
        assert any("GB18030" in w for w in doc.warnings)


# ── parsers.split_sections（F4 三连缺陷） ─────────────────────


class TestSplitSectionsFixes:
    def test_duplicate_method_chapters_both_kept(self):
        content = (
            "\\chapter{基线方法}\n基线内容\n\\chapter{改进方法}\n改进内容\n\\chapter{结论}\n总结\n"
        )
        sections = parsers_zh.LatexParser().split_sections(content)
        assert "method" in sections and "method_2" in sections
        assert sections["method"][0] == 1
        assert sections["method_2"][0] == 3

    def test_commented_chapter_ignored(self):
        content = "\\chapter{绪论}\n内容\n%\\chapter{结论}\n更多内容\n"
        sections = parsers_zh.LatexParser().split_sections(content)
        assert "conclusion" not in sections
        # 绪论区间不被注释行截断（含结尾空行共 5 行）
        assert sections["introduction"] == (1, 5)

    def test_starred_and_spaced_titles_recognized(self):
        content = "\\chapter*{摘要}\n摘要内容\n\\chapter{绪\\quad 论}\n绪论内容\n"
        sections = parsers_zh.LatexParser().split_sections(content)
        assert "abstract" in sections
        assert "introduction" in sections

    def test_optional_arg_title_recognized(self):
        content = "\\chapter[短标题]{相关工作}\n内容\n"
        sections = parsers_zh.LatexParser().split_sections(content)
        assert "related" in sections

    def test_unmatched_chapter_not_swallowed_by_previous(self):
        content = (
            "\\chapter{绪论}\n绪论内容\n"
            "\\chapter{多模态情感识别模型研究}\n正文章内容\n"
            "\\chapter{结论}\n总结\n"
        )
        sections = parsers_zh.LatexParser().split_sections(content)
        # 绪论区间止于下一个 level-1 标题，而不是吞并未匹配的正文章
        assert sections["introduction"] == (1, 2)

    def test_chapter_ranges_enumerates_unmatched_chapters(self):
        content = (
            "\\chapter{绪论}\n绪论内容\n"
            "\\chapter{多模态情感识别模型研究}\n正文章内容\n"
            "\\chapter{结论}\n总结\n"
        )
        ranges = parsers_zh.LatexParser().chapter_ranges(content)
        titles = [r["title"] for r in ranges]
        assert "多模态情感识别模型研究" in titles
        unmatched = next(r for r in ranges if r["title"] == "多模态情感识别模型研究")
        assert unmatched["key"] is None
        assert (unmatched["start"], unmatched["end"]) == (3, 4)

    def test_typst_duplicate_sections_both_kept(self):
        content = "= 基线方法\n内容\n= 改进方法\n内容\n"
        sections = parsers_zh.TypstParser().split_sections(content)
        assert "method" in sections and "method_2" in sections


# ── resolve_section_keys（F11） ───────────────────────────────


class TestResolveSectionKeys:
    SECTIONS = {"introduction": (1, 5), "method": (6, 10), "method_2": (11, 15)}

    def test_chinese_alias_resolves(self):
        keys, _ = parsers_zh.resolve_section_keys("绪论", self.SECTIONS)
        assert keys == ["introduction"]

    def test_english_key_resolves(self):
        keys, _ = parsers_zh.resolve_section_keys("introduction", self.SECTIONS)
        assert keys == ["introduction"]

    def test_base_key_matches_duplicates(self):
        keys, _ = parsers_zh.resolve_section_keys("方法", self.SECTIONS)
        assert keys == ["method", "method_2"]

    def test_unknown_returns_available_list(self):
        keys, available = parsers_zh.resolve_section_keys("不存在的章节", self.SECTIONS)
        assert keys == []
        assert "introduction" in available


# ── analyze_logic 多文件集成 ──────────────────────────────────


class TestAnalyzeLogicMultifile:
    def test_reports_issue_inside_include_with_source_lineref(self, tmp_path: Path):
        main = _write_multifile_project(tmp_path)
        findings = analyze_logic_zh.analyze(main)
        joined = "\n".join(findings)
        # 缺少导语段落问题位于 chapters/intro.tex，行号必须指向源文件
        assert "缺少导语段落" in joined
        assert "chapters/intro.tex:" in joined

    def test_section_accepts_chinese_name(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{相关工作}\n"
            "张三（2019）提出了一种方法。\n"
            "李四（2020）提出了另一种方法。\n"
            "王五（2021）提出了第三种方法。\n"
            "赵六（2022）提出了第四种方法。\n",
            encoding="utf-8",
        )
        zh = "\n".join(analyze_logic_zh.analyze(tex, "相关工作"))
        en = "\n".join(analyze_logic_zh.analyze(tex, "related"))
        assert zh == en
        assert "罗列" in zh

    def test_invalid_section_lists_available(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("\\chapter{绪论}\n内容\n", encoding="utf-8")
        findings = analyze_logic_zh.analyze(tex, "豆腐章节")
        joined = "\n".join(findings)
        assert "未找到章节" in joined
        assert "可用章节" in joined
        assert "introduction" in joined

    def test_gb18030_source_analyzed_with_warning(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_bytes(
            (
                "\\chapter{方法设计}\n"
                "\\section{总体流程}\n"
                "\\begin{itemize}\n\\item 数据预处理\n\\end{itemize}\n"
            ).encode("gb18030")
        )
        findings = analyze_logic_zh.analyze(tex)
        joined = "\n".join(findings)
        assert "WARN" in joined and "GB18030" in joined
        assert "缺少导语段落" in joined  # 内容真被解析了，而非乱码后“无问题”


# ── deai_check 多文件集成 ─────────────────────────────────────


class TestDeaiCheckMultifile:
    def test_suggestions_point_at_source_files(self, tmp_path: Path):
        (tmp_path / "chapters").mkdir()
        main = tmp_path / "main.tex"
        main.write_text("\\include{chapters/intro}\n", encoding="utf-8")
        (tmp_path / "chapters" / "intro.tex").write_text(
            "\\chapter{绪论}\n近年来，越来越多的研究关注此问题。\n",
            encoding="utf-8",
        )
        checker = deai_check_zh.ChineseAITraceChecker(main)
        suggestions = checker.generate_suggestions_json(checker.analyze_document())
        assert suggestions, "include 文件内的痕迹必须被检出"
        assert any(s["file"] == "chapters/intro.tex" and s["line"] == 2 for s in suggestions)

    def test_both_method_chapters_analyzed(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{基线方法}\n近年来，越来越多的研究关注此问题。\n"
            "\\chapter{改进方法}\n显然，这取得了显著提升，具有重要意义。\n",
            encoding="utf-8",
        )
        checker = deai_check_zh.ChineseAITraceChecker(tex)
        analysis = checker.analyze_document()
        assert "method" in analysis["sections"]
        assert "method_2" in analysis["sections"]
        assert analysis["sections"]["method"]["trace_count"] >= 1
        assert analysis["sections"]["method_2"]["trace_count"] >= 1


# ── check_consistency include 图（F17 接口约定） ───────────────


class TestConsistencyFileSet:
    def test_default_excludes_unincluded_drafts(self, tmp_path: Path):
        main = tmp_path / "main.tex"
        main.write_text("\\input{used}\n", encoding="utf-8")
        (tmp_path / "used.tex").write_text("正文使用深度学习。\n", encoding="utf-8")
        (tmp_path / "draft_backup.tex").write_text("废稿使用深层学习。\n", encoding="utf-8")

        files = check_consistency_zh.find_tex_files(str(main))
        names = {Path(f).name for f in files}
        assert "used.tex" in names
        assert "draft_backup.tex" not in names

    def test_all_files_flag_keeps_rglob(self, tmp_path: Path):
        main = tmp_path / "main.tex"
        main.write_text("\\input{used}\n", encoding="utf-8")
        (tmp_path / "used.tex").write_text("正文。\n", encoding="utf-8")
        (tmp_path / "draft_backup.tex").write_text("废稿。\n", encoding="utf-8")

        files = check_consistency_zh.find_tex_files(str(main), all_files=True)
        names = {Path(f).name for f in files}
        assert {"main.tex", "used.tex", "draft_backup.tex"} <= names
