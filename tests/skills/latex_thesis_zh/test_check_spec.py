"""check_spec.py（规范逐项终检）单测与 fixture 集成冒烟。

加载约定：zh 副本脚本必须 importlib 按路径加载并对称恢复 sys.path/sys.modules
（见 .trellis/spec/academic-writing-skills/testing-and-tooling.md）。
"""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT

_SKILL_DIR = SKILLS_ROOT / "latex-thesis-zh"
FIXTURE = _SKILL_DIR / "evals" / "fixtures" / "thesis-project"
MAIN_TEX = FIXTURE / "main.tex"


def _load_zh():
    saved_path = list(sys.path)
    saved = {m: sys.modules.pop(m, None) for m in ("parsers", "tex_loader")}
    try:
        spec = importlib.util.spec_from_file_location(
            "zh_check_spec", SCRIPT_DIR_ZH / "check_spec.py"
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, mod in saved.items():
            if mod is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = mod


check_spec = _load_zh()


def test_loader_guard_zh_copy():
    """加载守卫：确认拿到的是 zh 副本的 check_spec（而非 EN 侧同名物）。"""
    assert hasattr(check_spec, "SpecContext")
    assert hasattr(check_spec, "parse_checklist")
    assert "kw_count" in check_spec.CHECKERS
    assert "yanshan" in check_spec.TEMPLATE_THRESHOLDS


# ── 清单解析 ─────────────────────────────────────────────────


def _write_checklist(tmp_path: Path, rows: str) -> Path:
    md = tmp_path / "spec.md"
    md.write_text(
        "# 某校规范\n\n## 逐项检查清单\n\n"
        "| ID | 检查项 | 规范依据 | 检查方式 | 适用 |\n"
        "| --- | --- | --- | --- | --- |\n" + rows,
        encoding="utf-8",
    )
    return md


class TestParseChecklist:
    def test_parse_valid_table(self, tmp_path: Path):
        md = _write_checklist(
            tmp_path,
            "| XX-01 | 关键词 3~8 个 | §1.2 | script:kw_count | 通用 |\n"
            "| XX-02 | 摘要自含 | §1.3 | llm | 博士 |\n",
        )
        items = check_spec.parse_checklist(md)
        assert [i.id for i in items] == ["XX-01", "XX-02"]
        assert items[0].method == "script:kw_count"
        assert items[1].scope == "博士"

    def test_tolerates_formatter_alignment(self, tmp_path: Path):
        md = _write_checklist(
            tmp_path,
            "| XX-01   | 关键词 3~8 个      | §1.2    | script:kw_count   | 通用   |\n",
        )
        assert len(check_spec.parse_checklist(md)) == 1

    def test_duplicate_id_rejected(self, tmp_path: Path):
        md = _write_checklist(
            tmp_path,
            "| XX-01 | a | §1 | llm | 通用 |\n| XX-01 | b | §2 | llm | 通用 |\n",
        )
        with pytest.raises(ValueError, match="重复"):
            check_spec.parse_checklist(md)

    def test_bad_method_rejected(self, tmp_path: Path):
        md = _write_checklist(tmp_path, "| XX-01 | a | §1 | robot | 通用 |\n")
        with pytest.raises(ValueError, match="检查方式"):
            check_spec.parse_checklist(md)

    def test_missing_section_rejected(self, tmp_path: Path):
        md = tmp_path / "spec.md"
        md.write_text("# 无清单\n", encoding="utf-8")
        with pytest.raises(ValueError, match="逐项检查清单"):
            check_spec.parse_checklist(md)


# ── 检查器单测（tmp_path 微型工程） ──────────────────────────


def _ctx(tmp_path: Path, content: str, degree: str = "master", template: str = "yanshan"):
    tex = tmp_path / "main.tex"
    tex.write_text(content, encoding="utf-8")
    return check_spec.SpecContext(tex, degree, template, None, 2026)


def _check(name: str, ctx):
    return check_spec.CHECKERS[name](ctx)


class TestTitleLen:
    def test_pass_short(self, tmp_path: Path):
        status, _ = _check("title_len", _ctx(tmp_path, "\\ctitle{基于占位的研究}\n"))
        assert status == "PASS"

    def test_fail_over_25_without_subtitle(self, tmp_path: Path):
        status, ev = _check("title_len", _ctx(tmp_path, "\\ctitle{" + "长" * 26 + "}\n"))
        assert status == "FAIL"
        assert "25" in ev

    def test_pass_subtitle_within_35(self, tmp_path: Path):
        title = "主" * 20 + "——" + "副" * 10
        status, ev = _check("title_len", _ctx(tmp_path, f"\\ctitle{{{title}}}\n"))
        assert status == "PASS"
        assert "副题名" in ev

    def test_needs_llm_without_title(self, tmp_path: Path):
        status, _ = _check("title_len", _ctx(tmp_path, "\\chapter{绪论}\n"))
        assert status == "NEEDS-LLM"


class TestAbstractChecks:
    def test_no_cite_fail(self, tmp_path: Path):
        content = "\\begin{cabstract}\n引用了文献\\cite{a}。\n\\end{cabstract}\n"
        status, ev = _check("abstract_no_cite", _ctx(tmp_path, content))
        assert status == "FAIL"
        assert "cite" in ev

    def test_no_cite_pass(self, tmp_path: Path):
        content = "\\begin{cabstract}\n干净的摘要。\n\\end{cabstract}\n"
        assert _check("abstract_no_cite", _ctx(tmp_path, content))[0] == "PASS"

    def test_inline_math_needs_llm(self, tmp_path: Path):
        content = "\\begin{cabstract}\n精度达 $\\alpha$ 水平。\n\\end{cabstract}\n"
        assert _check("abstract_no_cite", _ctx(tmp_path, content))[0] == "NEEDS-LLM"

    def test_abstract_len_pass_master(self, tmp_path: Path):
        content = "\\begin{cabstract}\n" + "字" * 550 + "\n\\end{cabstract}\n"
        assert _check("abstract_len", _ctx(tmp_path, content))[0] == "PASS"

    def test_abstract_len_fail_short(self, tmp_path: Path):
        content = "\\begin{cabstract}\n" + "字" * 100 + "\n\\end{cabstract}\n"
        assert _check("abstract_len", _ctx(tmp_path, content))[0] == "FAIL"

    def test_abstract_len_soft_band_needs_llm(self, tmp_path: Path):
        content = "\\begin{cabstract}\n" + "字" * 480 + "\n\\end{cabstract}\n"
        status, ev = _check("abstract_len", _ctx(tmp_path, content))
        assert status == "NEEDS-LLM"
        assert "临界" in ev

    def test_abstract_len_no_threshold_template(self, tmp_path: Path):
        content = "\\begin{cabstract}\n" + "字" * 100 + "\n\\end{cabstract}\n"
        status, _ = _check("abstract_len", _ctx(tmp_path, content, template="unknown"))
        assert status == "NEEDS-LLM"

    def test_order_pass_zh_first(self, tmp_path: Path):
        content = (
            "\\begin{cabstract}\n中文摘要内容较多一些。\n\\end{cabstract}\n"
            "\\begin{abstract}\nThis is the English abstract text only.\n\\end{abstract}\n"
        )
        assert _check("abstract_order", _ctx(tmp_path, content))[0] == "PASS"

    def test_order_fail_en_first(self, tmp_path: Path):
        content = (
            "\\begin{abstract}\nEnglish abstract comes first here.\n\\end{abstract}\n"
            "\\begin{cabstract}\n中文摘要在后。\n\\end{cabstract}\n"
        )
        assert _check("abstract_order", _ctx(tmp_path, content))[0] == "FAIL"


class TestKeywords:
    def test_kw_count_pass(self, tmp_path: Path):
        ctx = _ctx(tmp_path, "\\ckeywords{占位；对齐；融合}\n")
        assert _check("kw_count", ctx)[0] == "PASS"

    def test_kw_count_fail_too_few(self, tmp_path: Path):
        ctx = _ctx(tmp_path, "\\ckeywords{占位；对齐}\n")
        assert _check("kw_count", ctx)[0] == "FAIL"

    def test_kw_count_fail_comma_separator(self, tmp_path: Path):
        ctx = _ctx(tmp_path, "\\ckeywords{占位，对齐，融合，系统}\n")
        status, ev = _check("kw_count", ctx)
        assert status == "FAIL"
        assert "分号" in ev

    def test_kw_count_needs_llm_missing(self, tmp_path: Path):
        assert _check("kw_count", _ctx(tmp_path, "\\chapter{绪论}\n"))[0] == "NEEDS-LLM"

    def test_kw_match_pass(self, tmp_path: Path):
        content = "\\ckeywords{甲；乙；丙}\n\\ekeywords{a; b; c}\n"
        assert _check("kw_zh_en_match", _ctx(tmp_path, content))[0] == "PASS"

    def test_kw_match_fail_unequal(self, tmp_path: Path):
        content = "\\ckeywords{甲；乙；丙}\n\\ekeywords{a; b}\n"
        assert _check("kw_zh_en_match", _ctx(tmp_path, content))[0] == "FAIL"


class TestTemplateThresholdOverrides:
    """新模板阈值键（title_max/title_sub_max/kw_range/kw_sep/abstract）与缺省回退语义。

    负面证据红线：清华/北大官方指南无副题名合计条款与燕山字数规则，
    对应键缺省时不得回落到燕山数值（见任务 07-08-template-checklists research/）。
    """

    def test_title_thuthesis_25_pass_and_fail(self, tmp_path: Path):
        assert (
            _check(
                "title_len", _ctx(tmp_path, "\\ctitle{" + "题" * 24 + "}\n", template="thuthesis")
            )[0]
            == "PASS"
        )
        status, ev = _check(
            "title_len", _ctx(tmp_path, "\\ctitle{" + "题" * 26 + "}\n", template="thuthesis")
        )
        assert status == "FAIL"
        assert "25" in ev

    def test_title_pku_20_limit(self, tmp_path: Path):
        status, ev = _check(
            "title_len", _ctx(tmp_path, "\\ctitle{" + "题" * 21 + "}\n", template="pkuthss")
        )
        assert status == "FAIL"
        assert "20" in ev

    def test_title_pku_no_yanshan_subtitle_spillover(self, tmp_path: Path):
        # 25 chars with a subtitle dash: PASS under yanshan (≤35) but must FAIL
        # under pkuthss (no combined-subtitle allowance beyond 20).
        title = "主" * 15 + "——" + "副" * 8
        assert _check("title_len", _ctx(tmp_path, f"\\ctitle{{{title}}}\n"))[0] == "PASS"
        status, ev = _check(
            "title_len", _ctx(tmp_path, f"\\ctitle{{{title}}}\n", template="pkuthss")
        )
        assert status == "FAIL"
        assert "20" in ev

    def test_kw_pku_comma_rule(self, tmp_path: Path):
        ok = _ctx(tmp_path, "\\ckeywords{甲，乙，丙}\n", template="pkuthss")
        assert _check("kw_count", ok)[0] == "PASS"

    def test_kw_pku_semicolon_fails(self, tmp_path: Path):
        ctx = _ctx(tmp_path, "\\ckeywords{甲；乙；丙}\n", template="pkuthss")
        status, ev = _check("kw_count", ctx)
        assert status == "FAIL"
        assert "逗号" in ev

    def test_kw_pku_range_3_to_5(self, tmp_path: Path):
        ctx = _ctx(tmp_path, "\\ckeywords{甲，乙，丙，丁，戊，己}\n", template="pkuthss")
        status, ev = _check("kw_count", ctx)
        assert status == "FAIL"
        assert "3~5" in ev

    def test_kw_generic_no_separator_rule(self, tmp_path: Path):
        # GB/T 7713.1-2006 §5.1.6 has no separator rule: comma-separated must pass.
        ctx = _ctx(tmp_path, "\\ckeywords{甲，乙，丙}\n", template="generic")
        assert _check("kw_count", ctx)[0] == "PASS"

    def test_abstract_thuthesis_800_1000(self, tmp_path: Path):
        good = "\\begin{cabstract}\n" + "字" * 900 + "\n\\end{cabstract}\n"
        assert _check("abstract_len", _ctx(tmp_path, good, template="thuthesis"))[0] == "PASS"
        short = "\\begin{cabstract}\n" + "字" * 90 + "\n\\end{cabstract}\n"
        assert _check("abstract_len", _ctx(tmp_path, short, template="thuthesis"))[0] == "FAIL"

    def test_abstract_pku_doctor_800_1000(self, tmp_path: Path):
        good = "\\begin{cabstract}\n" + "字" * 900 + "\n\\end{cabstract}\n"
        ctx = _ctx(tmp_path, good, degree="doctor", template="pkuthss")
        assert _check("abstract_len", ctx)[0] == "PASS"

    def test_abstract_pku_master_no_threshold(self, tmp_path: Path):
        # "一般 600 汉字左右" has no official range: must degrade, not invent bounds.
        content = "\\begin{cabstract}\n" + "字" * 600 + "\n\\end{cabstract}\n"
        status, ev = _check("abstract_len", _ctx(tmp_path, content, template="pkuthss"))
        assert status == "NEEDS-LLM"
        assert "无字数阈值依据" in ev

    def test_no_yanshan_wordcount_bib_spillover(self, tmp_path: Path):
        # Guides of THU/PKU/GB-generic define no body/intro/bib_min thresholds;
        # those checkers must degrade to NEEDS-LLM instead of using yanshan values.
        (tmp_path / "refs.bib").write_text(
            "@article{k0, author={A}, title={T}, journal={J}, year={2018}}",
            encoding="utf-8",
        )
        content = "\\chapter{绪论}\n" + "字" * 200 + "\n\\bibliography{refs}\n"
        for template in ("thuthesis", "pkuthss", "generic"):
            ctx = _ctx(tmp_path, content, template=template)
            assert _check("wordcount", ctx)[0] == "NEEDS-LLM"
            assert _check("intro_len", ctx)[0] == "NEEDS-LLM"
            status, ev = _check("bib_count", ctx)  # 1 篇也不得套燕山下限判 FAIL
            assert status == "NEEDS-LLM"
            assert "无数量阈值依据" in ev


class TestBodyChecks:
    def test_intro_len_pass_master(self, tmp_path: Path):
        content = "\\chapter{绪论}\n" + "字" * 3500 + "\n\\chapter{总结与展望}\n结束。\n"
        assert _check("intro_len", _ctx(tmp_path, content))[0] == "PASS"

    def test_intro_len_fail_short(self, tmp_path: Path):
        content = "\\chapter{绪论}\n太短。\n\\chapter{总结与展望}\n结束。\n"
        assert _check("intro_len", _ctx(tmp_path, content))[0] == "FAIL"

    def test_wordcount_pass_master(self, tmp_path: Path):
        content = "\\chapter{绪论}\n" + "字" * 31000 + "\n\\chapter{总结与展望}\n" + "字" * 800
        assert _check("wordcount", _ctx(tmp_path, content))[0] == "PASS"

    def test_wordcount_fail_tiny(self, tmp_path: Path):
        content = "\\chapter{绪论}\n很短。\n"
        assert _check("wordcount", _ctx(tmp_path, content))[0] == "FAIL"

    def test_chapter_summary_pass(self, tmp_path: Path):
        content = (
            "\\chapter{绪论}\n背景。\n"
            "\\chapter{占位方法}\n正文。\n\\section{本章小结}\n小结。\n"
            "\\chapter{总结与展望}\n结束。\n"
        )
        assert _check("chapter_summary", _ctx(tmp_path, content))[0] == "PASS"

    def test_chapter_summary_fail_missing(self, tmp_path: Path):
        content = (
            "\\chapter{绪论}\n背景。\n"
            "\\chapter{占位方法}\n正文没有小结。\n"
            "\\chapter{总结与展望}\n结束。\n"
        )
        status, ev = _check("chapter_summary", _ctx(tmp_path, content))
        assert status == "FAIL"
        assert "占位方法" in ev

    def test_chapter_summary_skip_no_body(self, tmp_path: Path):
        content = "\\chapter{绪论}\n背景。\n\\chapter{总结与展望}\n结束。\n"
        assert _check("chapter_summary", _ctx(tmp_path, content))[0] == "SKIP"


class TestConclusionChecks:
    def test_no_cite_fail(self, tmp_path: Path):
        content = "\\chapter{总结与展望}\n工作总结\\cite{a}。\n"
        status, ev = _check("conclusion_no_cite", _ctx(tmp_path, content))
        assert status == "FAIL"
        assert "cite" in ev

    def test_fail_when_body_chapter_after_conclusion(self, tmp_path: Path):
        content = "\\chapter{总结与展望}\n总结。\n\\chapter{补充实验}\n又一章。\n"
        status, ev = _check("conclusion_no_cite", _ctx(tmp_path, content))
        assert status == "FAIL"
        assert "补充实验" in ev

    def test_pass_clean_last(self, tmp_path: Path):
        content = "\\chapter{占位方法}\n正文。\n\\chapter{总结与展望}\n总结。\n"
        assert _check("conclusion_no_cite", _ctx(tmp_path, content))[0] == "PASS"

    def test_len_fail_over_2200(self, tmp_path: Path):
        content = "\\chapter{总结与展望}\n" + "字" * 2300 + "\n"
        assert _check("conclusion_len", _ctx(tmp_path, content))[0] == "FAIL"

    def test_hedge_fail(self, tmp_path: Path):
        content = "\\chapter{总结与展望}\n该方法可能是最优的。\n"
        status, ev = _check("conclusion_hedge", _ctx(tmp_path, content))
        assert status == "FAIL"
        assert "可能是" in ev


class TestBibChecks:
    @staticmethod
    def _project(tmp_path: Path, n: int, years):
        entries = []
        for i in range(n):
            year = years[i % len(years)]
            entries.append(
                f"@article{{k{i}, author={{A}}, title={{T{i}}}, journal={{J}}, year={{{year}}}}}"
            )
        (tmp_path / "refs.bib").write_text("\n".join(entries), encoding="utf-8")
        return "\\chapter{绪论}\n正文\\cite{k0}。\n\\bibliography{refs}\n"

    def test_bib_count_pass_master(self, tmp_path: Path):
        content = self._project(tmp_path, 40, [2025])
        assert _check("bib_count", _ctx(tmp_path, content))[0] == "PASS"

    def test_bib_count_fail_few(self, tmp_path: Path):
        content = self._project(tmp_path, 5, [2025])
        assert _check("bib_count", _ctx(tmp_path, content))[0] == "FAIL"

    def test_bib_recency_pass(self, tmp_path: Path):
        content = self._project(tmp_path, 9, [2025, 2024, 2016])
        assert _check("bib_recency", _ctx(tmp_path, content))[0] == "PASS"

    def test_bib_recency_fail_no_recent(self, tmp_path: Path):
        content = self._project(tmp_path, 6, [2018])
        status, ev = _check("bib_recency", _ctx(tmp_path, content))
        assert status == "FAIL"
        assert "近两年" in ev

    def test_bib_needs_llm_without_bib(self, tmp_path: Path):
        assert _check("bib_count", _ctx(tmp_path, "\\chapter{绪论}\n无文献。\n"))[0] == "NEEDS-LLM"

    def test_thebibliography_fallback(self, tmp_path: Path):
        content = (
            "\\chapter{绪论}\n正文。\n"
            "\\begin{thebibliography}{9}\n"
            "\\bibitem{a} 某作者. 某文献. 2025.\n"
            "\\bibitem{b} 某作者. 另一文献. 2024.\n"
            "\\end{thebibliography}\n"
        )
        status, ev = _check("bib_count", _ctx(tmp_path, content))
        assert status == "FAIL"  # 2 < 40
        assert "2 篇" in ev


class TestHeadingChecks:
    def test_heading_len_fail(self, tmp_path: Path):
        content = "\\chapter{" + "标" * 16 + "}\n正文。\n"
        assert _check("heading_len", _ctx(tmp_path, content))[0] == "FAIL"

    def test_heading_depth_fail_paragraph(self, tmp_path: Path):
        content = "\\chapter{绪论}\n\\paragraph{五级标题}\n正文。\n"
        assert _check("heading_depth", _ctx(tmp_path, content))[0] == "FAIL"

    def test_cite_in_heading_fail(self, tmp_path: Path):
        content = "\\chapter{绪论}\n\\section{基于\\cite{a}的方法}\n正文。\n"
        assert _check("cite_in_heading", _ctx(tmp_path, content))[0] == "FAIL"

    def test_new_page_chapter_fail_section_only(self, tmp_path: Path):
        content = "\\section{绪论}\n正文。\n"
        assert _check("new_page_chapter", _ctx(tmp_path, content))[0] == "FAIL"

    def test_appendix_letter_pass_with_command(self, tmp_path: Path):
        content = "\\chapter{绪论}\n正文。\n\\appendix\n\\chapter{附录内容}\n附录。\n"
        assert _check("appendix_letter", _ctx(tmp_path, content))[0] == "PASS"

    def test_appendix_letter_fail_without_command(self, tmp_path: Path):
        content = "\\chapter{绪论}\n正文。\n\\chapter{附录：补充}\n附录。\n"
        assert _check("appendix_letter", _ctx(tmp_path, content))[0] == "FAIL"

    def test_appendix_letter_skip_absent(self, tmp_path: Path):
        content = "\\chapter{绪论}\n正文。\n"
        assert _check("appendix_letter", _ctx(tmp_path, content))[0] == "SKIP"


# ── run_checklist 分流语义 ────────────────────────────────────


class TestRunChecklist:
    def test_scope_skip_by_degree(self, tmp_path: Path):
        items = [
            check_spec.ChecklistItem("XX-01", "博士项", "§1", "llm", "博士"),
            check_spec.ChecklistItem("XX-02", "通用项", "§1", "manual", "通用"),
        ]
        ctx = _ctx(tmp_path, "\\chapter{绪论}\n正文。\n", degree="master")
        results = check_spec.run_checklist(items, ctx)
        assert results[0].status == "SKIP"
        assert results[1].status == "MANUAL"

    def test_unknown_checker_degrades_to_needs_llm(self, tmp_path: Path):
        items = [check_spec.ChecklistItem("XX-01", "未知项", "§1", "script:nonexistent", "通用")]
        ctx = _ctx(tmp_path, "\\chapter{绪论}\n正文。\n")
        results = check_spec.run_checklist(items, ctx)
        assert results[0].status == "NEEDS-LLM"
        assert "nonexistent" in results[0].evidence

    def test_module_maps_to_command(self, tmp_path: Path):
        items = [check_spec.ChecklistItem("XX-01", "表格项", "§1", "module:tables", "通用")]
        ctx = _ctx(tmp_path, "\\chapter{绪论}\n正文。\n")
        results = check_spec.run_checklist(items, ctx)
        assert results[0].status == "MODULE"
        assert "check_tables.py" in results[0].evidence


# ── CLI 集成（fixture 工程 + 自定义清单） ─────────────────────


def _run_cli(*args: str, cwd: Path = FIXTURE) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPT_DIR_ZH / "check_spec.py"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(cwd),
        env=env,
        check=False,
    )


class TestCliIntegration:
    def test_fixture_yanshan_doctor_report(self):
        result = _run_cli(
            "main.tex", "--template", "yanshan", "--degree", "doctor", "--year", "2026"
        )
        assert result.returncode == 1
        out = result.stdout
        assert "规范逐项终检报告" in out
        # fixture 天然违规（文献 5 篇 / 摘要 90 字 / 正文远低于下限）
        for item_id in ("YS-18", "YS-24", "YS-26"):
            assert f"[Script]: {item_id}" in out
        # 天然通过项与自查单结构
        assert "- YS-13" in out
        assert "打印前自查单" in out
        assert "GB18030" in out  # 编码告警透传（fixture 埋点 #22）

    def test_fixture_json_output(self):
        result = _run_cli(
            "main.tex", "--template", "yanshan", "--degree", "doctor", "--year", "2026", "--json"
        )
        payload = json.loads(result.stdout)
        assert payload["status"] == "FAIL"
        assert payload["summary"]["FAIL"] >= 3
        ids = {item["id"] for item in payload["items"]}
        assert {"YS-01", "YS-18", "YS-58"} <= ids

    def test_fixture_master_skips_doctor_items(self):
        result = _run_cli(
            "main.tex", "--template", "yanshan", "--degree", "master", "--year", "2026", "--json"
        )
        payload = json.loads(result.stdout)
        by_id = {item["id"]: item for item in payload["items"]}
        assert by_id["YS-16"]["status"] == "SKIP"  # 博士结论三部分
        assert by_id["YS-49"]["status"] == "SKIP"  # 博士书脊

    def test_spec_file_custom_checklist(self, tmp_path: Path):
        md = _write_checklist(
            tmp_path,
            "| ZZ-01 | 关键词 3~8 个 | §9.9 | script:kw_count | 通用 |\n"
            "| ZZ-02 | 自定义未知检查 | §9.9 | script:no_such_checker | 通用 |\n",
        )
        result = _run_cli(
            "main.tex", "--spec-file", str(md), "--degree", "doctor", "--year", "2026"
        )
        out = result.stdout
        assert "ZZ-01" in out
        assert "ZZ-02" in out
        assert "no_such_checker" in out  # 未知检查器降级说明

    def test_unknown_template_exits_2_with_hint(self):
        result = _run_cli("main.tex", "--template", "no-such-school", "--degree", "doctor")
        assert result.returncode == 2
        # stderr 必须列出全部可用清单（thuthesis/pkuthss/generic 清单落地后一并展示）
        for name in ("yanshan", "thuthesis", "pkuthss", "generic"):
            assert name in result.stderr

    # ── thuthesis / pkuthss / generic 清单（07-08-template-checklists） ──
    # fixture 天然违规（埋点 #24）：摘要约 90 字、附录章无 \appendix、无关键词宏。
    # 负面证据红线：THU-/PKU- 清单不得出现燕山字数/文献量类 script 条目。

    BANNED_NON_YS_METHODS = {
        "script:wordcount",
        "script:intro_len",
        "script:conclusion_len",
        "script:bib_count",
        "script:bib_recency",
        "script:conclusion_no_cite",
        "script:chapter_summary",
    }

    def test_fixture_thuthesis_checklist(self):
        result = _run_cli(
            "main.tex", "--template", "thuthesis", "--degree", "doctor", "--year", "2026", "--json"
        )
        assert result.returncode == 1
        payload = json.loads(result.stdout)
        assert payload["template"] == "thuthesis"
        by_id = {item["id"]: item for item in payload["items"]}
        assert by_id["THU-01"]["status"] == "PASS"  # 题名 13 字 ≤ 25
        assert by_id["THU-02"]["status"] == "FAIL"  # 摘要约 90 字，区间 800~1000
        assert by_id["THU-24"]["status"] == "FAIL"  # 附录章无 \appendix
        assert not self.BANNED_NON_YS_METHODS & {i["method"] for i in payload["items"]}

    def test_fixture_pkuthss_checklist_degree_split(self):
        result = _run_cli(
            "main.tex", "--template", "pkuthss", "--degree", "master", "--year", "2026", "--json"
        )
        assert result.returncode == 1
        payload = json.loads(result.stdout)
        by_id = {item["id"]: item for item in payload["items"]}
        assert by_id["PKU-01"]["status"] == "PASS"  # 题名 13 字 ≤ 20
        assert by_id["PKU-02"]["status"] == "SKIP"  # 博士摘要阈值项，master 跳过
        assert by_id["PKU-03"]["status"] == "NEEDS-LLM"  # 硕士"600左右"落 llm
        assert by_id["PKU-22"]["status"] == "FAIL"  # 附录章无 \appendix
        assert not self.BANNED_NON_YS_METHODS & {i["method"] for i in payload["items"]}

    def test_fixture_generic_checklist(self):
        result = _run_cli(
            "main.tex", "--template", "generic", "--degree", "master", "--year", "2026", "--json"
        )
        assert result.returncode == 1
        payload = json.loads(result.stdout)
        by_id = {item["id"]: item for item in payload["items"]}
        assert by_id["GEN-01"]["status"] == "PASS"  # 题名 13 字 ≤ 20（国标值）
        # 国标摘要字数不作阈值：只报实测数并降级 NEEDS-LLM
        assert by_id["GEN-05"]["status"] == "NEEDS-LLM"
        assert "实测" in by_id["GEN-05"]["evidence"]
        assert by_id["GEN-06"]["status"] == "PASS"  # 摘要无引用/图表/公式
        assert by_id["GEN-21"]["status"] == "FAIL"  # 附录章无 \appendix
