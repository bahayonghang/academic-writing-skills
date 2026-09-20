"""Observable unit planning and drift checks for the shipped Chinese thesis script."""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT

SCRIPT = SCRIPT_DIR_ZH / "polish_unit_zh.py"
FIXTURES = SKILLS_ROOT / "latex-thesis-zh/evals/fixtures"
PROJECT = FIXTURES / "subsection-context/main.tex"
NO_DEPTH3 = FIXTURES / "thesis-project/main.tex"
SYNTHETIC = FIXTURES / "unit-polish"
EXPECTED_IDS = ["1.1.1", "1.2.1", "1.2.2", "1.2.3", "1.3.1", "1.4.1", "1.4.2", "1.4.3", "2.1.1"]
FROZEN_HASHES = {
    "analyze_logic.py": "d88c933981247dd79c1131c48c4d45f4d6750fabd90299c68ed42899297dae44",
    "deai_check.py": "08afae7e2ebc82636ceea9ac083d448a72e5e1dab1534663273238c7d59da135",
    "parsers.py": "49dc31832a14307a6cf7ab183de793a0b0c273478e5b9375e78bef66e75bb53c",
    "check_style_zh.py": "3774ff1d228d85c9999e5730c2c8fac11d71633a4953aa11b7fe751aa0104cbc",
    "check_claim_forward.py": "f289e13e293faa57248078b7c3db88e0f659c5537058a6372abf8000826a1f72",
    "tex_loader.py": "a3053d93432cf9ef0fbcd320f101b2497c7ae787138eb500b0cfd5d71fb9c525",
}


def _load_zh():
    saved_path = sys.path[:]
    saved = {
        name: sys.modules.pop(name, None) for name in ("parsers", "tex_loader", "analyze_logic")
    }
    try:
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec = importlib.util.spec_from_file_location("zh_polish_unit_tests", SCRIPT)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


polish: Any = _load_zh()


def _cli(entry: Path, *arguments: str):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(entry), *arguments],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
        timeout=30,
    )


def _write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def _codes(original: str, revised: str, **kwargs) -> set[str]:
    return {finding["code"] for finding in polish.verify(original, revised, **kwargs)}


def _unit_text(entry: Path, unit_id: str) -> str:
    doc = polish.assemble(entry)
    units, paragraphs, _sections = polish.build_units(doc)
    unit = next(unit for unit in units + paragraphs if unit["unit_id"] == unit_id)
    return "\n".join(doc.lines[unit["assembled_start"] - 1 : unit["assembled_end"]])


def test_loader_targets_zh_and_restores_sidecars():
    before_path = sys.path[:]
    before = {name: sys.modules.get(name) for name in ("parsers", "tex_loader", "analyze_logic")}
    loaded = _load_zh()
    assert loaded.__file__ is not None
    assert Path(loaded.__file__).resolve() == SCRIPT.resolve()
    assert Path(loaded.logic.__file__).resolve() == (SCRIPT_DIR_ZH / "analyze_logic.py").resolve()
    assert sys.path == before_path
    assert {name: sys.modules.get(name) for name in before} == before


@pytest.mark.parametrize(
    ("name", "parameters"),
    [
        ("_build_subsection_cursor", ["doc", "parser", "sections", "first_chapter"]),
        ("_split_arc_paragraphs", ["content", "parser", "sections"]),
        ("_build_context_window", ["units", "index", "paragraphs"]),
    ],
)
def test_reused_logic_helpers_exist(name, parameters):
    assert list(inspect.signature(getattr(polish.logic, name)).parameters) == parameters


@pytest.mark.parametrize(("name", "digest"), FROZEN_HASHES.items())
def test_frozen_scripts_keep_lf_normalized_hash(name, digest):
    data = (SCRIPT_DIR_ZH / name).read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(data).hexdigest() == digest


def test_plan_matches_subsection_cursor_and_exposes_only_coordinates():
    completed = _cli(PROJECT, "--plan", "--json")
    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)
    assert [unit["unit_id"] for unit in result["units"]] == EXPECTED_IDS
    assert all(unit["unit_type"] == "subsection" for unit in result["units"])
    assert "离散容器保存局部符号" not in completed.stdout
    unit = result["units"][1]
    assert (unit["source_file"], unit["source_start"], unit["source_end"]) == (
        "chapters/method-a.tex",
        15,
        19,
    )
    assert list(unit["context"]) == ["prev.tail", "parent_lead", "next.head"]
    assert unit["context"]["next.head"]["source_start"] == 21


def test_build_units_restores_logic_document_cursor():
    previous = polish.logic._DOC
    polish.build_units(polish.assemble(PROJECT))
    assert polish.logic._DOC is previous


def test_no_depth3_lists_prose_paragraphs_without_document_controls():
    completed = _cli(NO_DEPTH3, "--plan", "--json")
    assert completed.returncode == 0
    result = json.loads(completed.stdout)
    assert "本文档无 depth-3 标题" in result["notice"]
    assert result["units"]
    assert all(unit["unit_type"] == "paragraph" for unit in result["units"])
    assert all(unit["han_count"] > 0 for unit in result["units"])
    text = _cli(NO_DEPTH3, "--plan")
    assert "润色单元清单" in text.stdout
    assert "本文档无 depth-3 标题" in text.stdout


def test_plan_text_ends_with_unit_guidance_not_a_verification_conclusion():
    completed = _cli(PROJECT, "--plan")
    assert completed.returncode == 0
    assert completed.stdout.rstrip().endswith("超过 1200 字的单元按内部段落单元逐段处理。")
    assert "核对结论" not in completed.stdout
    assert "Meaning-Check" not in completed.stdout


def test_paragraphs_keep_heading_leads_english_and_numeric_prose(tmp_path):
    entry = _write(
        tmp_path,
        "prose.tex",
        (
            "\\documentclass{ctexbook}\n\\title{这是不应入清单的中文题名}\n"
            "\\begin{document}\n\\chapter{方法}\n这是需要保留的章节导语。\n\n"
            "A model predicts output.\n\n20 samples; 5 s.\n\n"
            "\\bibliography{references}\n\\end{document}\n"
        ),
    )
    doc = polish.assemble(entry)
    units, paragraphs, _sections = polish.build_units(doc)
    assert units == paragraphs
    assert len(units) == 3
    assert [unit["unit_id"] for unit in units] == ["method#1", "method#2", "method#3"]
    assert [unit["source_start"] for unit in units] == [5, 7, 9]
    assert units[0]["context"]["next.head"]["source_start"] == 7
    assert units[1]["context"]["prev.tail"]["source_start"] == 5
    assert units[2]["context"]["prev.tail"]["source_start"] == 7


def test_long_subsection_lists_internal_paragraphs_and_can_select_one(tmp_path):
    paragraph = "本段记录测量步骤并保留各个操作之间的关系。" * 36
    entry = _write(
        tmp_path,
        "long.tex",
        (
            "\\chapter{方法}\n\\section{过程}\n\\subsection{测量}\n"
            f"{paragraph}\n\n{paragraph}\n"
        ),
    )
    result = json.loads(_cli(entry, "--plan", "--json").stdout)
    unit = result["units"][0]
    assert unit["han_count"] > 1200
    assert len(unit["paragraph_units"]) == 2
    assert "需拆分" in _cli(entry, "--plan").stdout
    selected = unit["paragraph_units"][0]
    plan = json.loads(_cli(entry, "--plan", "--unit", selected["unit_id"], "--json").stdout)
    assert plan["units"] == [selected]
    revised = _write(tmp_path, "paragraph.tex", paragraph)
    verified = _cli(entry, "--verify", "--unit", selected["unit_id"], "--revised", str(revised))
    assert verified.returncode == 0
    assert "PASS-SCRIPT" in verified.stdout


def test_first_chapter_and_section_filter_reuse_existing_semantics():
    result = json.loads(_cli(PROJECT, "--plan", "--first-chapter", "4", "--json").stdout)
    assert result["units"][0]["unit_id"] == "4.1.1"
    assert result["units"][-1]["unit_id"] == "5.1.1"
    filtered = json.loads(_cli(PROJECT, "--plan", "--section", "method", "--json").stdout)
    assert [unit["unit_id"] for unit in filtered["units"]] == EXPECTED_IDS[:-1]
    missing = _cli(PROJECT, "--plan", "--section", "missing")
    assert missing.returncode == 0 and "% ERROR:" in missing.stdout


@pytest.mark.parametrize(
    ("code", "original", "revised", "kwargs", "severity", "priority"),
    [
        ("UP-SCOPE", "原始正文。", "\\subsection{新增标题}\n原始正文。", {}, "Error", "P1"),
        ("UP-CITE", r"正文\cite{a,b}。", r"正文\cite{a}。", {}, "Error", "P1"),
        ("UP-REF", r"见图\ref{a}。", r"见图\ref{b}。", {}, "Error", "P1"),
        ("UP-LABEL", r"正文\label{a}。", r"正文\label{b}。", {}, "Error", "P1"),
        ("UP-MATH", r"公式 $x=y$。", r"公式 $x=z$。", {}, "Error", "P1"),
        ("UP-NUM", "取 20 个样本。", "取 21 个样本。", {}, "Error", "P1"),
        ("UP-TOKEN", "采用 CNN。", "采用 RNN。", {}, "Warning", "P2"),
        ("UP-TERM", "采用软测量。", "采用软传感。", {"terms": ("软测量",)}, "Warning", "P2"),
        ("UP-STRENGTH", "结果可能支持关系。", "结果证明关系。", {}, "Warning", "P2"),
        ("UP-NEG", "没有检测到信号。", "已经检测到信号。", {}, "Info", "P3"),
        (
            "UP-LENGTH",
            "本研究比较样本。",
            "本研究比较样本并且逐一记录各个样本的具体数值。",
            {},
            "Info",
            "P3",
        ),
    ],
)
def test_each_code_reports_expected_severity(code, original, revised, kwargs, severity, priority):
    findings = polish.verify(original, revised, **kwargs)
    finding = next(finding for finding in findings if finding["code"] == code)
    assert (finding["severity"], finding["priority"]) == (severity, priority)
    assert finding["tier"] == ("A" if severity == "Error" else "B")
    assert "risk_flags" not in finding


@pytest.mark.parametrize(
    ("code", "original", "revised", "kwargs"),
    [
        (
            "UP-SCOPE",
            "\\subsection{原始标题}\n本研究比较样本。",
            "\\subsection{原始标题}\n本研究核对样本。",
            {},
        ),
        ("UP-CITE", r"正文\cite{a,b}。", r"正文\citep[参见]{ b,a }。", {}),
        ("UP-REF", r"见图\ref{a}和图\ref{b}。", r"见图\cref{b,a}。", {}),
        ("UP-LABEL", r"正文\label{a}。", r"正文\label{a}\label{a}。", {}),
        ("UP-MATH", r"公式 $x = y$。", r"公式 \(x=y\)。", {}),
        ("UP-NUM", r"间隔 5\,s，比例 20\%。", r"间隔 5 s，比例 20\%。", {}),
        ("UP-TOKEN", "采用 CNN 和 CNN。", "采用 CNN。", {}),
        ("UP-TERM", "采用软测量。", "本节采用软测量。", {"terms": ("软测量",)}),
        ("UP-STRENGTH", "结果可能支持关系。", "此结果可能支持所述关系。", {}),
        ("UP-NEG", "没有检测到信号。", "在样本中没有检测到信号。", {}),
        ("UP-LENGTH", "甲乙丙丁戊己庚辛壬癸", "甲乙丙丁戊己庚辛壬癸甲乙", {}),
    ],
)
def test_each_code_has_non_drift_counterexample(code, original, revised, kwargs):
    assert code not in _codes(original, revised, **kwargs)


@pytest.mark.parametrize(
    "command",
    [
        "cite",
        "cite*",
        "Cite",
        "citep",
        "Citep",
        "citet",
        "Citet",
        "upcite",
        "parencite",
        "Parencite*",
        "autocite",
        "Autocite*",
        "textcite",
        "Textcite",
        "footcite",
        "Footcite",
        "footcitetext",
        "Footcitetext",
        "smartcite",
        "Smartcite",
        "supercite",
    ],
)
def test_citations_count_repetitions_and_optional_arguments(command):
    original = rf"正文\{command}[见][第 3 页]{{a,b,a}}。"
    revised = rf"正文\{command}[见][第 3 页]{{a,b}}。"
    assert "UP-CITE" in _codes(original, revised)
    assert "UP-CITE" not in _codes(original, original + " % \\cite{extra}")


@pytest.mark.parametrize(
    "command",
    [
        "cites",
        "Cites*",
        "parencites",
        "Parencites*",
        "autocites",
        "Autocites",
        "textcites",
        "Textcites",
        "footcites",
        "Footcites",
        "footcitetexts",
        "Footcitetexts",
        "smartcites",
        "Smartcites",
        "supercites",
    ],
)
def test_biblatex_multicites_compare_every_group_and_mask_all_notes(command):
    original = rf"正文\{command}(参见)(总计 40 页)[见][第 3 页]{{a,b}}[第 5 页]{{b,c}}。"
    revised = rf"正文\{command}(参见)(总计 50 页)[第 7 页]{{c}}[见][第 9 页]{{a,b}}。"
    findings = polish.verify(original, revised)
    assert [finding["code"] for finding in findings] == ["UP-CITE"]
    assert findings[0]["original"] == ["b"]
    assert findings[0]["revised"] == []
    reordered = rf"正文\{command}{{c,b}}[见]{{b,a}}。"
    assert not _codes(original, reordered)


def test_citation_note_braces_delimiters_and_payloads_do_not_leak_into_visible_checks():
    original = (
        r"正文\parencites(可能{含)括号})(CNN2)[见{含]括号}][第 20 页]{可能2}"
        r"[\textbf{RNN3} 显著 30]{未4}。"
    )
    revised = r"正文\parencites(证明)(SVM5)[无 90]{证明6}[相关 80]{不7}。"
    assert _codes(original, revised) == {"UP-CITE"}


@pytest.mark.parametrize("separator", [" ", "\n", "% citation comment\n"])
@pytest.mark.parametrize(
    ("command", "code", "multiple"),
    [
        ("parencite", "UP-CITE", False),
        ("Autocite", "UP-CITE", False),
        ("parencites", "UP-CITE", True),
        ("Autocites", "UP-CITE", True),
        ("Cref", "UP-REF", False),
    ],
)
def test_space_before_star_keeps_keys_protected_and_payloads_masked(
    separator, command, code, multiple
):
    original_args, revised_args = "{可能2}", "{证明3}"
    if code == "UP-CITE":
        original_args = "[见][第 20 页]" + original_args
        revised_args = "[见][第 30 页]" + revised_args
    if multiple:
        original_args = "(总计 40 页)" + original_args + "[第 50 页]{未6}"
        revised_args = "(总计 70 页)" + revised_args + "[第 80 页]{不9}"
    original = f"正文\\{command}{separator}*{original_args}。"
    revised = f"正文\\{command}{separator}*{revised_args}。"
    findings = polish.verify(original, revised)
    assert [finding["code"] for finding in findings] == [code]
    assert findings[0]["severity"] == "Error"
    assert "可能2" in findings[0]["original"] and "证明3" in findings[0]["revised"]
    assert not _codes(original, original)


@pytest.mark.parametrize(
    "command", ["parencitereset", "autocitation", "mycite", "textcitecustom", "cite@helper"]
)
def test_citation_like_macro_names_do_not_create_false_citation_findings(command):
    assert "UP-CITE" not in _codes(rf"正文\{command}{{a}}", rf"正文\{command}{{b}}")
    assert "UP-CITE" not in _codes(rf"正文\{command} *{{a}}", rf"正文\{command} *{{b}}")


def test_single_citation_does_not_consume_a_following_prose_group():
    assert _codes(r"正文\parencite{a}{取 20 个样本}。", r"正文\parencite{a}{取 21 个样本}。") == {
        "UP-NUM"
    }


@pytest.mark.parametrize(
    "command",
    ["ref", "Ref", "eqref", "Eqref", "autoref", "Autoref", "cref", "Cref", "pageref", "Pageref"],
)
def test_all_reference_commands_compare_target_multisets(command):
    assert "UP-REF" in _codes(rf"正文\{command}{{a}}", rf"正文\{command}{{b}}")
    assert "UP-REF" not in _codes(rf"正文\{command}* {{ a,b }}", rf"正文\{command}{{b,a}}")


@pytest.mark.parametrize("command", ["Crefname", "RefStep", "autorefname", "pagerefformat"])
def test_reference_macro_prefixes_are_not_targets(command):
    assert "UP-REF" not in _codes(rf"正文\{command}{{a}}", rf"正文\{command}{{b}}")
    assert "UP-REF" not in _codes(rf"正文\{command} *{{a}}", rf"正文\{command} *{{b}}")


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ("$x$", "$y$"),
        ("$$x$$", "$$y$$"),
        (r"\(x\)", r"\(y\)"),
        (r"\[x\]", r"\[y\]"),
        (r"\begin {equation}x\end {equation}", r"\begin {equation}y\end {equation}"),
        ("\\begin\n{align}x\\end\n{align}", "\\begin\n{align}y\\end\n{align}"),
        *[
            (rf"\begin{{{env}}}x\end{{{env}}}", rf"\begin{{{env}}}y\end{{{env}}}")
            for env in ("equation", "equation*", "align", "align*", "gather", "gather*")
        ],
    ],
)
def test_all_supported_math_forms_protect_payloads(left, right):
    assert "UP-MATH" in _codes(left, right)
    assert "UP-MATH" not in _codes(left, left.replace("x", " x "))


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ("12", "13"),
        ("0.12", "0.13"),
        (r"20\%", r"21\%"),
        ("1.2e-3", "1.2e-4"),
        (r"5\,s", r"5\,ms"),
        ("2 kg", "3 kg"),
        (".5", ".6"),
        ("−2", "−3"),
        ("5 m²", "5 m³"),
        ("5 kg/m³", "5 kg/m²"),
    ],
)
def test_numeric_forms_and_units_are_protected(left, right):
    assert "UP-NUM" in _codes(f"取值为 {left}。", f"取值为 {right}。")


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ("CNN", "RNN"),
        ("ResNet50", "ResNet101"),
        ("Model-A", "Model-B"),
    ],
)
def test_protected_identifier_categories(left, right):
    assert "UP-TOKEN" in _codes(f"采用{left}。", f"采用{right}。")


@pytest.mark.parametrize("change", ["remove", "rename", "add", "star"])
def test_heading_changes_block_but_same_nested_payload_does_not(change):
    heading = r"\subsection[短标题]{原始\textbf{嵌套}标题}"
    original = heading + "\n原始正文。"
    revised = {
        "remove": "原始正文。",
        "rename": original.replace("原始\\textbf", "新设\\textbf"),
        "add": original + "\n\\paragraph{新增}",
        "star": original.replace("subsection[", "subsection*["),
    }[change]
    assert "UP-SCOPE" in _codes(original, revised)
    assert "UP-SCOPE" not in _codes(original, original)


@pytest.mark.parametrize("added", [r"\input{extra}", r"\include{extra}", r"\begin{document}"])
def test_new_structure_commands_block(added):
    assert "UP-SCOPE" in _codes("正文。", "正文。\n" + added)
    assert "UP-SCOPE" not in _codes(added + "正文。", added + "正文。")
    assert "UP-SCOPE" not in _codes("正文。", "正文。 % " + added)


def test_neighbor_first_sentence_blocks_only_new_exact_copies():
    sentence = "后续分析只记录占位样本的排列规则并保留独立的讨论范围。"
    neighbor = "\\section{父级标题}\n" + sentence + "第二句仅供理解。"
    original = "本段记录局部实验步骤。"
    assert "UP-SCOPE" in _codes(original, original + sentence, neighbors=(neighbor,))
    assert "UP-SCOPE" not in _codes(original + sentence, original + sentence, neighbors=(neighbor,))
    assert "UP-SCOPE" not in _codes(
        original, original + "短句不足阈值。", neighbors=("短句不足阈值。",)
    )
    assert "UP-SCOPE" not in _codes(original, original + "第二句仅供理解。", neighbors=(neighbor,))


def test_strength_longest_match_hedges_and_directions():
    findings = polish.verify("结果不显著但可能表明局部趋势。", "结果显著并证明局部趋势。")
    strength = next(finding for finding in findings if finding["code"] == "UP-STRENGTH")
    assert "疑似抬升" in strength["title"]
    assert "「不显著」1→0" in strength["candidate"]
    assert "「显著」0→1" in strength["candidate"]
    assert "「可能表明」1→0" in strength["candidate"]
    assert "「可能」" not in strength["candidate"]
    softened = polish.verify("结果证明局部趋势。", "结果可能支持局部趋势。")
    assert any("疑似削弱" in finding["title"] for finding in softened)
    assert "UP-STRENGTH" in _codes("结果与先前观察一致。", "结果符合先前观察。")
    assert "UP-STRENGTH" in _codes("结果在一定程度上支持该解释。", "结果支持该解释。")


@pytest.mark.parametrize(
    ("original", "revised", "terms"),
    [
        ("本研究采用SVM完成质量预测。", "本研究采用支持向量机完成质量预测。", ("支持向量机",)),
        ("相关研究采用定量测量步骤。", "已有研究采用定量测量步骤。", ("相关研究",)),
    ],
)
def test_explicit_terms_mask_strength_substrings_only(original, revised, terms):
    findings = polish.verify(original, revised)
    strength = next(finding for finding in findings if finding["code"] == "UP-STRENGTH")
    assert strength["tier"] == "B" and strength["severity"] == "Warning"
    assert "术语或普通用法" in strength["candidate"]
    assert "不代表语义强度已改变" in strength["candidate"]
    assert "原文语境：" in strength["candidate"] and "润色稿语境：" in strength["candidate"]
    assert terms[0] in strength["candidate"]
    masked_codes = _codes(original, revised, terms=terms)
    assert "UP-STRENGTH" not in masked_codes
    assert "UP-TERM" in masked_codes
    assert masked_codes == {finding["code"] for finding in findings} - {"UP-STRENGTH"} | {"UP-TERM"}


def test_terms_preserve_real_claim_checks_and_other_protection_checks():
    findings = polish.verify(
        "支持向量机可能支持局部关系。", "支持向量机证明局部关系。", terms=("支持向量机",)
    )
    strength = next(finding for finding in findings if finding["code"] == "UP-STRENGTH")
    assert "「支持」1→0" in strength["candidate"]
    assert "「可能」1→0" in strength["candidate"]
    assert "「证明」0→1" in strength["candidate"]
    assert "疑似抬升" in strength["title"]
    # Even a user term containing a protected number must not suppress UP-NUM.
    assert {"UP-TERM", "UP-NUM"} <= _codes("取 20 个样本。", "取 21 个样本。", terms=("20 个",))


def test_hedge_loader_reads_distinct_yaml_terms(monkeypatch):
    def custom_yaml(path, *args, **kwargs):
        assert path.name == "claim-forward-terms-zh.yaml"
        return "hedges:\n  - 测试限定词\n"

    monkeypatch.setattr(Path, "read_text", custom_yaml)
    assert polish._load_hedges() == ("测试限定词",)
    assert "UP-STRENGTH" in _codes("结果测试限定词支持关系。", "结果支持关系。")


def test_hedge_loader_falls_back_on_missing_file(monkeypatch):

    def missing(*args, **kwargs):
        raise FileNotFoundError("missing test resource")

    monkeypatch.setattr(Path, "read_text", missing)
    assert polish._load_hedges() == polish.DEFAULT_HEDGES


def test_hedge_loader_falls_back_without_yaml(monkeypatch):
    monkeypatch.setitem(sys.modules, "yaml", None)
    assert polish._load_hedges() == polish.DEFAULT_HEDGES


@pytest.mark.parametrize("payload", ["hedges: [", "[]", "{}", "hedges: []", "hedges: [1]"])
def test_hedge_loader_falls_back_on_invalid_yaml_input(monkeypatch, payload):
    monkeypatch.setattr(Path, "read_text", lambda *args, **kwargs: payload)
    assert polish._load_hedges() == polish.DEFAULT_HEDGES


def test_visible_checks_do_not_count_protected_payloads_or_comments():
    original = r"正文\citep{可能2}\Cref{显著3}\label{不4}$x=5$。"
    revised = r"正文\citep{证明6}\Cref{相关7}\label{未8}$x=9$。"
    codes = _codes(original, revised)
    assert {"UP-CITE", "UP-REF", "UP-LABEL", "UP-MATH"} <= codes
    assert codes.isdisjoint({"UP-NUM", "UP-STRENGTH", "UP-NEG", "UP-TOKEN"})
    assert not _codes("正文。 % 20 可能", "正文。 % 30 证明")


def test_comments_respect_even_backslashes_and_escaped_percent():
    assert not _codes(r"正文。\\% \cite{a}", r"正文。\\% \cite{b}")
    assert not _codes(r"正文。\\\\% \cite{a}", r"正文。\\\\% \cite{b}")
    assert "UP-CITE" in _codes(r"正文。\% \cite{a}", r"正文。\% \cite{b}")
    assert "UP-NUM" in _codes(r"比例 20\%。", r"比例 21\%。")


def test_length_threshold_handles_shrink_override_and_empty_text():
    original = "甲乙丙丁戊己庚辛壬癸"
    assert "UP-LENGTH" in _codes(original, "甲乙丙丁戊己庚")
    assert "UP-LENGTH" not in _codes(original, "甲乙丙丁戊己庚", max_growth=0.5)
    assert not _codes("", "")
    assert "UP-LENGTH" in _codes("", "新增正文")


def test_no_op_copy_is_clean_and_still_requires_llm(tmp_path):
    original = _unit_text(PROJECT, "1.2.1")
    revised = _write(tmp_path, "same.tex", original)
    completed = _cli(PROJECT, "--verify", "--unit", "1.2.1", "--revised", str(revised), "--json")
    result = json.loads(completed.stdout)
    assert completed.returncode == 0
    assert result["findings"] == []
    assert result["verdict"] == "PASS-SCRIPT"
    assert result["meaning_check"] == "NEEDS-LLM"
    plain = _cli(PROJECT, "--verify", "--unit", "1.2.1", "--revised", str(revised))
    assert "Meaning-Check: NEEDS-LLM" in plain.stdout
    assert "Risk-Flags" not in plain.stdout and "PRESERVED" not in plain.stdout


def test_synthetic_ok_and_drift_fixtures_are_executable():
    original = SYNTHETIC / "main.tex"
    good = _cli(
        original,
        "--verify",
        "--unit",
        "1.1.1",
        "--revised",
        str(SYNTHETIC / "revised-ok.tex"),
        "--json",
    )
    assert good.returncode == 0 and json.loads(good.stdout)["findings"] == []
    bad = _cli(
        original,
        "--verify",
        "--unit",
        "1.1.1",
        "--revised",
        str(SYNTHETIC / "revised-drift.tex"),
        "--json",
    )
    result = json.loads(bad.stdout)
    assert bad.returncode == 1 and result["verdict"] == "BLOCK"
    assert {finding["code"] for finding in result["findings"]} == {
        "UP-SCOPE",
        "UP-CITE",
        "UP-NUM",
        "UP-STRENGTH",
    }
    plain = _cli(
        original, "--verify", "--unit", "1.1.1", "--revised", str(SYNTHETIC / "revised-drift.tex")
    )
    assert plain.stdout.count("Meaning-Check: NEEDS-LLM") == 5
    assert "% 原文:" in plain.stdout and "% 候选:" in plain.stdout
    assert "Risk-Flags" not in plain.stdout and "PRESERVED" not in plain.stdout


def test_custom_terms_cli_is_opt_in_and_warning_does_not_block(tmp_path):
    original = _write(tmp_path, "original.tex", "本研究采用软测量估计质量。")
    revised = _write(tmp_path, "revised.tex", "本研究采用软传感估计质量。")
    terms = _write(
        tmp_path,
        "terms.json",
        json.dumps({"zh": [["软测量", "软传感"]], "en": [["CNN"]]}, ensure_ascii=False),
    )
    args = ("--verify", "--original", str(original), "--revised", str(revised), "--json")
    without = _cli(tmp_path / "unused-entry.tex", *args)
    assert without.returncode == 0 and not json.loads(without.stdout)["findings"]
    with_terms = _cli(tmp_path / "unused-entry.tex", *args, "--terms", str(terms))
    assert with_terms.returncode == 0
    assert [f["code"] for f in json.loads(with_terms.stdout)["findings"]] == ["UP-TERM"]


def test_biblatex_and_capital_refs_block_cli_with_readable_text_differences(tmp_path):
    original = _write(tmp_path, "original.tex", r"正文\parencite{a,b}\Cref{fig:a}，取 20 个样本。")
    revised = _write(tmp_path, "revised.tex", r"正文\parencite{a}\Cref{fig:b}，取 21 个样本。")
    args = ("--verify", "--original", str(original), "--revised", str(revised))
    completed = _cli(original, *args)
    assert completed.returncode == 1
    assert "% 原文: cite{b}\n% 润色稿: 无差异项" in completed.stdout
    assert "% 原文: ref{fig:a}\n% 润色稿: ref{fig:b}" in completed.stdout
    assert "% 原文: 「20」\n% 润色稿: 「21」" in completed.stdout
    assert "['" not in completed.stdout and "[]" not in completed.stdout
    structured = json.loads(_cli(original, *args, "--json").stdout)
    assert structured["verdict"] == "BLOCK"
    cite = next(f for f in structured["findings"] if f["code"] == "UP-CITE")
    assert cite["original"] == ["b"] and cite["revised"] == []


@pytest.mark.parametrize("payload", ["not json", "[]", '{"zh": ["term"]}', '{"zh": [[1]]}'])
def test_invalid_terms_report_error_not_pass(tmp_path, payload):
    original = _write(tmp_path, "original.tex", "正文。")
    terms = _write(tmp_path, "terms.json", payload)
    completed = _cli(
        original,
        "--verify",
        "--original",
        str(original),
        "--revised",
        str(original),
        "--terms",
        str(terms),
        "--json",
    )
    assert completed.returncode == 1
    assert json.loads(completed.stdout)["verdict"] == "ERROR"


@pytest.mark.parametrize(
    "arguments",
    [
        (),
        ("--plan", "--verify"),
        ("--verify",),
        ("--verify", "--revised", "r.tex"),
        ("--verify", "--original", "o.tex"),
        ("--verify", "--unit", "1.1.1", "--original", "o.tex", "--revised", "r.tex"),
        ("--plan", "--max-growth", "-0.1"),
        ("--plan", "--max-growth", "nan"),
        ("--plan", "--max-growth", "inf"),
    ],
)
def test_cli_argument_errors_exit_two(arguments):
    completed = _cli(PROJECT, *arguments)
    assert completed.returncode == 2 and "error:" in completed.stderr


def test_help_explains_every_public_argument():
    completed = _cli(PROJECT, "--help")
    assert completed.returncode == 0
    for option, explanation in (
        ("tex_file", "LaTeX 工程入口"),
        ("--plan", "列出润色单元与只读邻域坐标"),
        ("--verify", "核对单个单元的润色稿"),
        ("--section", "按章节键或标题筛选"),
        ("--unit", "单元 id"),
        ("--first-chapter", "覆盖首个编号章"),
        ("--original", "独立原文文件"),
        ("--revised", "待核对的单元润色稿文件"),
        ("--terms", "zh/en 术语 JSON 文件"),
        ("--max-growth", "字数变化阈值"),
        ("--json", "输出结构化 JSON"),
    ):
        assert option in completed.stdout
        assert explanation in completed.stdout


def test_missing_sources_and_unknown_unit_never_report_pass(tmp_path):
    missing = tmp_path / "missing.tex"
    plan = _cli(missing, "--plan", "--json")
    assert plan.returncode == 0 and json.loads(plan.stdout)["verdict"] == "ERROR"
    for args in (
        ("--original", str(missing), "--revised", str(missing)),
        ("--original", str(PROJECT), "--revised", str(missing)),
        ("--unit", "99.99.99", "--revised", str(PROJECT)),
    ):
        completed = _cli(PROJECT, "--verify", *args, "--json")
        assert completed.returncode == 1
        assert json.loads(completed.stdout)["verdict"] == "ERROR"


def test_missing_include_is_visible_and_blocks_incomplete_unit(tmp_path):
    entry = _write(
        tmp_path,
        "main.tex",
        ("\\chapter{方法}\n\\section{过程}\n\\subsection{单元}\n正文。\n\\input{missing}\n"),
    )
    plan = _cli(entry, "--plan", "--json")
    assert plan.returncode == 0 and json.loads(plan.stdout)["warnings"]
    revised = _write(tmp_path, "revised.tex", "\\subsection{单元}\n正文。")
    checked = _cli(entry, "--verify", "--unit", "1.1.1", "--revised", str(revised), "--json")
    assert checked.returncode == 1 and json.loads(checked.stdout)["verdict"] == "ERROR"
