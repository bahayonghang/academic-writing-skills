"""Regression coverage for the opt-in latex-thesis-zh paragraph-arc checks."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT, TESTS_ROOT

_SCRIPT = SCRIPT_DIR_ZH / "analyze_logic.py"
_FIXTURE_DIR = TESTS_ROOT / "fixtures" / "paragraph_arc"
_SKILL_DIR = SKILLS_ROOT / "latex-thesis-zh"


def _load_zh_logic():
    saved_path = list(sys.path)
    saved = {name: sys.modules.pop(name, None) for name in ("parsers", "tex_loader")}
    try:
        spec = importlib.util.spec_from_file_location("zh_paragraph_arc", _SCRIPT)
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

HEADING_LEAD = (
    "本节围绕复杂工业过程的观测延迟展开，说明研究对象、工程约束与后续分析安排。"
    "这一导语为段落检查建立明确作用域。"
)
GOOD_FIRST = "复杂工业过程的时变运行状态是在线质量估计必须处理的基础对象与判断依据。"
GOOD_CLOSE = "综上，该段分析表明观测约束需要在后续模型设计中被显式处理。"
PLAIN_CLOSE = "现有离线估计方法仍然依赖稀疏标签与固定采样条件完成状态辨识。"


def _write_tex(tmp_path: Path, body: str, *, chapter: str = "绪论") -> Path:
    tex = tmp_path / "case.tex"
    tex.write_text(f"\\chapter{{{chapter}}}\n{HEADING_LEAD}\n\n{body}\n", encoding="utf-8")
    return tex


def _arc_headers(report: list[str], code: str | None = None) -> list[str]:
    headers = [line for line in report if "[Script] P-ARC-" in line]
    return [line for line in headers if code in line] if code else headers


def _paragraph(
    first: str,
    last: str,
    *,
    start: int = 10,
    section: str = "introduction",
    segment_id: int = 1,
) -> object:
    return logic.ArcParagraph(
        start=start,
        end=start + 1,
        visible=f"{first}{last}",
        raw=f"{first}{last}",
        sentences=(first, last),
        section=section,
        segment_id=segment_id,
        is_heading_lead=False,
        in_item=False,
        ends_with_env=False,
    )


def test_loader_targets_zh_copy_and_exports_arc_contract() -> None:
    assert logic.__file__ is not None
    assert Path(logic.__file__).resolve() == _SCRIPT.resolve()
    assert logic.PARAGRAPH_ARC_DOUBLE_MISSING_RUN == 3
    assert logic.PARAGRAPH_ARC_LINK_THRESHOLD == 0.0200


def test_default_output_is_byte_identical_to_pre_change_baseline() -> None:
    sample = _FIXTURE_DIR / "baseline-sample.tex"
    expected = (_FIXTURE_DIR / "baseline-before.txt").read_bytes()
    actual = ("\n".join(logic.analyze(sample, "introduction")) + "\n").encode("utf-8")
    assert actual == expected
    assert b"P-ARC-" not in actual


def test_lead_and_close_findings_are_independent_and_located(tmp_path: Path) -> None:
    weak_lead = f"面向复杂工况。\n观测窗口覆盖多个运行阶段并保留关键时序信息。\n{GOOD_CLOSE}"
    missing_close = f"{GOOD_FIRST}\n动态特征随后进入统一编码器形成状态表示。\n{PLAIN_CLOSE}"
    tex = _write_tex(tmp_path, f"{weak_lead}\n\n{missing_close}")

    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    lead = _arc_headers(report, "P-ARC-LEAD")
    close = _arc_headers(report, "P-ARC-CLOSE")

    assert len(lead) == 1 and "第4行" in lead[0]
    assert len(close) == 1 and "第10行" in close[0]


def test_sentence_locations_ignore_standalone_label_lines(tmp_path: Path) -> None:
    body = (
        "\\label{par:arc-location}\n"
        "面向复杂工况。\n"
        "观测窗口覆盖多个运行阶段并保留关键时序信息。\n"
        f"{GOOD_CLOSE}\n"
        "\\label{par:arc-location-end}"
    )
    tex = _write_tex(tmp_path, body)
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    lead = _arc_headers(report, "P-ARC-LEAD")
    assert len(lead) == 1 and "第5行" in lead[0]


def test_clean_lead_and_close_emit_no_corresponding_findings(tmp_path: Path) -> None:
    body = f"{GOOD_FIRST}该段进一步说明多源记录需要按统一时间基准完成对齐。{GOOD_CLOSE}"
    tex = _write_tex(tmp_path, body)
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report, "P-ARC-LEAD")
    assert not _arc_headers(report, "P-ARC-CLOSE")
    assert not _arc_headers(report, "P-ARC-FLAT")


@pytest.mark.parametrize(
    "environment",
    [
        "equation",
        "alignat",
        "figure",
        "table",
        "longtable",
        "algorithm",
        "itemize",
        "description",
    ],
)
def test_link_never_crosses_protected_environment(tmp_path: Path, environment: str) -> None:
    left = f"{GOOD_FIRST}前一段继续讨论延迟观测条件下的状态辨识边界。{PLAIN_CLOSE}"
    right = (
        "多源记录的异步采样模式需要独立建模并保留各通道的时间索引关系。"
        "编码后的状态表示进入质量估计器形成连续输出。"
    )
    if environment == "itemize":
        protected = "\\begin{itemize}\n\\item 列表项\n\\end{itemize}"
    else:
        protected = f"\\begin{{{environment}}}\n受保护内容\n\\end{{{environment}}}"
    tex = _write_tex(tmp_path, f"{left}\n{protected}\n{right}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report, "P-ARC-LINK")


def test_heading_lead_and_dedicated_sections_are_exempt() -> None:
    content = (
        "\\begin{abstract}\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n"
        "\\end{abstract}\n"
        "\\chapter{绪论}\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n\n"
        "\\section{论文组织结构}\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n"
        "\\section{本章小结}\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n"
        "\\chapter{结论}\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n"
        "\\chapter{致谢}\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n"
        "\\appendix\n\\chapter{附录 A}\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n"
    )
    parser = logic.get_parser(Path("case.tex"))
    sections = parser.split_sections(content)
    paragraphs = logic._split_arc_paragraphs(content, parser, sections)
    assert paragraphs
    assert all(not logic._arc_is_eligible(paragraph) for paragraph in paragraphs)


def test_chapter_ownership_resumes_after_exempt_child_section() -> None:
    content = (
        "\\chapter{绪论}\n"
        f"{HEADING_LEAD}\n"
        "\\section{论文组织结构}\n"
        f"{HEADING_LEAD}\n"
        "\\section{研究问题}\n"
        f"{HEADING_LEAD}\n\n"
        f"{GOOD_FIRST}{PLAIN_CLOSE}\n"
    )
    parser = logic.get_parser(Path("case.tex"))
    sections = parser.split_sections(content)
    paragraphs = logic._split_arc_paragraphs(content, parser, sections)
    target = paragraphs[-1]
    assert target.section == "introduction"
    assert logic._arc_is_eligible(target)


@pytest.mark.parametrize(
    "display_math",
    ["\\[\nE = mc^2\n\\]", "$$\nE = mc^2\n$$"],
)
def test_link_never_crosses_display_math(tmp_path: Path, display_math: str) -> None:
    left = f"{GOOD_FIRST}前段围绕状态辨识建立约束集合并保留过程动态信息。{PLAIN_CLOSE}"
    right = (
        "质量估计器接收对齐后的多源状态表示并输出连续质量变量预测结果。"
        "预测结果用于后续运行分析与参数核对。"
    )
    tex = _write_tex(tmp_path, f"{left}\n{display_math}\n{right}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report, "P-ARC-LINK")


def test_original_adjacency_is_not_rebuilt_across_short_paragraph(tmp_path: Path) -> None:
    left = f"{GOOD_FIRST}前段围绕状态辨识建立约束集合并保留过程动态信息。{PLAIN_CLOSE}"
    short = "短段落不进入检查。"
    right = (
        "质量估计器接收对齐后的多源状态表示并输出连续质量变量预测结果。"
        "预测结果用于后续运行分析与参数核对。"
    )
    tex = _write_tex(tmp_path, f"{left}\n\n{short}\n\n{right}")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report, "P-ARC-LINK")


def test_link_explicit_marker_and_overlap_are_pass_paths() -> None:
    terms = logic.DEFAULT_PARAGRAPH_ARC_TERMS
    left = _paragraph(GOOD_FIRST, "状态表示保留过程动态关系并进入质量估计模块。")
    explicit = _paragraph(
        "另一方面，状态表示保留过程动态关系并进入质量估计模块。",
        PLAIN_CLOSE,
        start=20,
    )
    overlap = _paragraph(
        "状态表示保留过程动态关系并进入质量估计模块完成在线预测。",
        PLAIN_CLOSE,
        start=30,
    )
    assert logic._arc_link_missing(left, explicit, terms) == (False, None)
    missing, score = logic._arc_link_missing(left, overlap, terms)
    assert missing is False and score is not None and score >= 0.0200


def test_link_rounding_empty_sets_and_strict_threshold(monkeypatch: pytest.MonkeyPatch) -> None:
    terms = logic.DEFAULT_PARAGRAPH_ARC_TERMS
    left_sentinel = "左侧接口端点句子具有足够长度并用于执行词面重叠阈值计算。"
    right_sentinel = "右侧接口端点句子同样具有足够长度并用于执行词面阈值计算。"
    left = _paragraph("左端点句子具有足够长度用于执行接口阈值计算。", left_sentinel)
    right = _paragraph(right_sentinel, PLAIN_CLOSE, start=20)

    exact_left = {"common", *(f"l{i}" for i in range(24))}
    exact_right = {"common", *(f"r{i}" for i in range(25))}
    monkeypatch.setattr(
        logic,
        "_thread_tokens",
        lambda text: exact_left if text == left_sentinel else exact_right,
    )
    assert logic._arc_link_missing(left, right, terms) == (False, 0.0200)

    below_right = {"common", *(f"r{i}" for i in range(26))}
    monkeypatch.setattr(
        logic,
        "_thread_tokens",
        lambda text: exact_left if text == left_sentinel else below_right,
    )
    assert logic._arc_link_missing(left, right, terms) == (True, 0.0196)

    monkeypatch.setattr(logic, "_thread_tokens", lambda _text: set())
    assert logic._arc_link_missing(left, right, terms) == (True, 0.0)


def test_flat_single_sentence_and_author_enumeration_paths(tmp_path: Path) -> None:
    single = "复杂工业过程的多源采样条件具有明显异步特征并持续影响在线质量估计器的状态表示稳定性。"
    enumeration = (
        "张三（2020）提出一种面向复杂过程的状态估计方法并报告了实验结果。"
        "李四（2021）构建另一种多源特征编码框架并比较了基准性能。"
    )
    tex = _write_tex(tmp_path, f"{single}\n\n{enumeration}", chapter="方法设计")
    report = logic.analyze(tex, paragraph_arc=True)
    flat = _arc_headers(report, "P-ARC-FLAT")
    assert len(flat) == 2

    related = _write_tex(tmp_path, enumeration, chapter="相关工作")
    related_report = logic.analyze(related, "related", paragraph_arc=True)
    assert not _arc_headers(related_report, "P-ARC-FLAT")


def test_three_consecutive_double_missing_paragraphs_upgrade_once(tmp_path: Path) -> None:
    paragraph = (
        "围绕现场约束。"
        "多源采样记录覆盖多个运行阶段并保留异步通道的原始时间索引关系。"
        "状态编码器随后生成连续表示并交给质量估计模块完成在线预测。"
    )
    tex = _write_tex(tmp_path, "\n\n".join([paragraph, paragraph, paragraph]))
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    joined = "\n".join(report)
    assert joined.count("[Severity: Minor] [Priority: P2]: [Script] P-ARC-LEAD+CLOSE") == 1
    assert sum("[Script] P-ARC-LEAD " in line for line in report) == 3
    assert sum("[Script] P-ARC-CLOSE " in line for line in report) == 3


@pytest.mark.parametrize(
    "barrier",
    [
        "短段落不进入检查。",
        "\\section{新的分析边界}\n" + HEADING_LEAD,
        "\\begin{equation}\ny = f(x)\n\\end{equation}",
        "\\begin{itemize}\n\\item 列表项不进入段落弧线检查。\n\\end{itemize}",
    ],
)
def test_double_missing_run_resets_at_ineligible_or_segment_boundary(
    tmp_path: Path, barrier: str
) -> None:
    paragraph = (
        "围绕现场约束。"
        "多源采样记录覆盖多个运行阶段并保留异步通道的原始时间索引关系。"
        "状态编码器随后生成连续表示并交给质量估计模块完成在线预测。"
    )
    body = "\n\n".join([paragraph, paragraph, barrier, paragraph, paragraph])
    tex = _write_tex(tmp_path, body)
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report, "P-ARC-LEAD+CLOSE")


def test_list_items_never_emit_paragraph_arc_findings(tmp_path: Path) -> None:
    item = (
        "围绕现场约束。"
        "多源采样记录覆盖多个运行阶段并保留异步通道的原始时间索引关系。"
        "状态编码器随后生成连续表示并交给质量估计模块完成在线预测。"
    )
    tex = _write_tex(
        tmp_path,
        f"\\begin{{itemize}}\n\\item {item}\n\\item {item}\n\\end{{itemize}}",
    )
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report)


def test_section_scope_excludes_other_chapters(tmp_path: Path) -> None:
    paragraph = (
        "围绕现场约束。"
        "多源采样记录覆盖多个运行阶段并保留异步通道的原始时间索引关系。"
        "状态编码器随后生成连续表示并交给质量估计模块完成在线预测。"
    )
    content = (
        f"\\chapter{{绪论}}\n{HEADING_LEAD}\n\n{GOOD_FIRST}{GOOD_CLOSE}\n"
        f"\\chapter{{方法设计}}\n{HEADING_LEAD}\n\n{paragraph}\n"
    )
    tex = tmp_path / "case.tex"
    tex.write_text(content, encoding="utf-8")
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    assert not _arc_headers(report)


def test_every_arc_finding_has_script_and_meaning_check(tmp_path: Path) -> None:
    paragraph = (
        "围绕现场约束。"
        "多源采样记录覆盖多个运行阶段并保留异步通道的原始时间索引关系。"
        "状态编码器随后生成连续表示并交给质量估计模块完成在线预测。"
    )
    tex = _write_tex(tmp_path, paragraph)
    report = logic.analyze(tex, "introduction", paragraph_arc=True)
    headers = _arc_headers(report)
    assert headers
    for index, line in enumerate(report):
        if "[Script] P-ARC-" in line:
            assert "% Meaning-Check: NEEDS-LLM" in report[index + 1 : index + 6]


def test_yaml_defaults_and_neutral_docs_copies_match() -> None:
    source = _SKILL_DIR / "references" / "writing" / "paragraph-arc-terms.yaml"
    configured = yaml.safe_load(source.read_text(encoding="utf-8"))
    assert set(configured) == set(logic.DEFAULT_PARAGRAPH_ARC_TERMS)
    for key, values in logic.DEFAULT_PARAGRAPH_ARC_TERMS.items():
        assert configured[key] == list(values)

    repo_root = SKILLS_ROOT.parent
    for locale in ("skills", "zh/skills"):
        mirror = (
            repo_root
            / "docs"
            / locale
            / "latex-thesis-zh"
            / "resources"
            / "references"
            / "writing"
            / source.name
        )
        assert mirror.read_bytes() == source.read_bytes()


def test_terms_loader_falls_back_for_missing_and_invalid_fields(tmp_path: Path) -> None:
    script_dir = tmp_path / "scripts"
    script_dir.mkdir()
    missing = logic._load_paragraph_arc_terms(script_dir)
    assert missing == logic.DEFAULT_PARAGRAPH_ARC_TERMS

    terms_dir = tmp_path / "references" / "writing"
    terms_dir.mkdir(parents=True)
    (terms_dir / logic.PARAGRAPH_ARC_TERMS_FILENAME).write_text(
        "judgment_predicates: invalid\n"
        "prospective_patterns:\n"
        "  - '[invalid'\n"
        "explicit_link_markers:\n"
        "  - 自定义接口\n",
        encoding="utf-8",
    )
    loaded = logic._load_paragraph_arc_terms(script_dir)
    assert loaded["judgment_predicates"] == logic.DEFAULT_PARAGRAPH_ARC_TERMS["judgment_predicates"]
    assert (
        loaded["prospective_patterns"] == logic.DEFAULT_PARAGRAPH_ARC_TERMS["prospective_patterns"]
    )
    assert loaded["explicit_link_markers"] == ("自定义接口",)


def test_logic_remains_outside_rewrite_contract() -> None:
    routing = (_SKILL_DIR / "references" / "modules" / "routing-rules.md").read_text(
        encoding="utf-8"
    )
    assert "`logic`、`literature`" in routing
    arc_route = routing.split("--paragraph-arc", maxsplit=1)[1][:300]
    assert "不增加改写契约" in arc_route
