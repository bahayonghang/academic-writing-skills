"""Tests for the latex-thesis-zh ``expression`` module (``check_style_zh.py``).

Each of the nine E-* checkers gets a positive case and a counter-example that
exercises the exclusion its design declares — the exclusions are part of the
contract, not an optimization.

The ZH copy is loaded by file path via importlib: a bare ``import`` would
resolve ``parsers`` / ``tex_loader`` to the latex-paper-en copies that
``tests/conftest.py`` puts first on ``sys.path``, silently testing the wrong
objects.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT

_ZH_DIR = SCRIPT_DIR_ZH
_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load_zh(name: str):
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


check_style_zh = _load_zh("check_style_zh")


def test_loader_guard_resolves_the_zh_copy() -> None:
    """Guard: a regression in the loader must fail here, not silently pass."""
    assert hasattr(check_style_zh, "ChineseStyleChecker")
    assert hasattr(check_style_zh, "COLLOC_ERRORS")


def _codes(tmp_path: Path, *body: str, **kwargs) -> list[str]:
    return [f.code for f in _findings(tmp_path, *body, **kwargs)]


def _findings(tmp_path: Path, *body: str, **kwargs):
    tex = tmp_path / "main.tex"
    tex.write_text(
        "\\documentclass{ctexbook}\n\\begin{document}\n" + "\n".join(body) + "\n\\end{document}\n",
        encoding="utf-8",
    )
    checker = check_style_zh.ChineseStyleChecker(tex, max_chars=kwargs.pop("max_chars", 80))
    return checker.analyze(**kwargs).findings


def _by_code(findings, code):
    return [f for f in findings if f.code == code]


# ── E-COLLOQ ─────────────────────────────────────────────────────────────────


def test_colloq_flags_spoken_adverbs(tmp_path: Path) -> None:
    findings = _by_code(_findings(tmp_path, "很多研究表明该方法有效。"), "E-COLLOQ")

    assert findings
    assert findings[0].tier == "auto"
    assert "大量" in findings[0].suggestion


def test_colloq_exempts_the_recommended_connective(tmp_path: Path) -> None:
    """`特别是` is the §3.4 example connective, not a colloquialism."""
    assert "E-COLLOQ" not in _codes(tmp_path, "特别是在高噪声场景下，该模型仍然稳定。")


# ── E-ABSOLUTE ───────────────────────────────────────────────────────────────


def test_absolute_flags_categorical_wording(tmp_path: Path) -> None:
    findings = _by_code(_findings(tmp_path, "显然，该策略是最好的选择。"), "E-ABSOLUTE")

    assert findings
    assert findings[0].tier == "candidate"
    assert not findings[0].suggestion, "B 档不得给可直接套用的替换文本"


def test_absolute_exempts_quoted_positions(tmp_path: Path) -> None:
    assert "E-ABSOLUTE" not in _codes(tmp_path, "文献[1]认为显然存在计算瓶颈。")


# ── E-COLLOC ─────────────────────────────────────────────────────────────────


def test_colloc_flags_wrong_verb_object_pair(tmp_path: Path) -> None:
    findings = _by_code(_findings(tmp_path, "该策略有效增加了模型的效率。"), "E-COLLOC")

    assert findings
    assert findings[0].tier == "auto"
    assert "提高了模型的效率" in findings[0].suggestion


def test_colloc_does_not_cross_punctuation(tmp_path: Path) -> None:
    assert "E-COLLOC" not in _codes(tmp_path, "该策略增加了训练数据，效率也随之提高。")


# ── E-INCOMP ─────────────────────────────────────────────────────────────────


def test_incomp_reports_a_candidate_only(tmp_path: Path) -> None:
    findings = _by_code(_findings(tmp_path, "通过对比实验，验证了所提方法的有效性。"), "E-INCOMP")

    assert findings
    assert findings[0].tier == "candidate"
    assert not findings[0].suggestion
    assert "人工判断" in findings[0].candidate


def test_incomp_exempts_a_sentence_that_has_a_subject(tmp_path: Path) -> None:
    assert "E-INCOMP" not in _codes(tmp_path, "通过对比实验，本文验证了所提方法的有效性。")


# ── E-PUNCT ──────────────────────────────────────────────────────────────────


def test_punct_flags_ascii_punctuation_in_chinese_context(tmp_path: Path) -> None:
    findings = _by_code(_findings(tmp_path, "该模型在训练集上收敛, 速度提升明显。"), "E-PUNCT")

    assert findings
    assert findings[0].tier == "candidate"


def test_punct_exempts_an_all_ascii_parenthesis(tmp_path: Path) -> None:
    """§5.3 explicitly allows English punctuation inside an all-English bracket."""
    assert "E-PUNCT" not in _codes(tmp_path, "该模型（见 Fig. 1, right）在此场景下表现稳定。")


# ── E-NUMSPACE ───────────────────────────────────────────────────────────────


def test_numspace_flags_missing_space_before_unit(tmp_path: Path) -> None:
    findings = _by_code(_findings(tmp_path, "样本质量为 3.2kg，测量重复三次。"), "E-NUMSPACE")

    assert findings
    assert findings[0].tier == "auto"
    assert "3.2\\,kg" in findings[0].suggestion
    assert findings[0].risk_flags == "whitespace-normalized"


def test_numspace_exempts_units_that_take_no_space(tmp_path: Path) -> None:
    assert "E-NUMSPACE" not in _codes(tmp_path, "准确率为 92.1%，温度为 25℃。")


# ── E-UNITFONT ───────────────────────────────────────────────────────────────


def test_unitfont_reports_without_any_replacement_text(tmp_path: Path) -> None:
    findings = _by_code(_findings(tmp_path, "其质量为 $m = 3.2 kg$ 时结果稳定。"), "E-UNITFONT")

    assert findings
    finding = findings[0]
    assert finding.tier == "candidate"
    assert not finding.suggestion, "红线一：数学环境永不给替换文本"
    assert "数学环境" in finding.candidate
    assert "手动" in finding.candidate


def test_unitfont_exempts_units_already_upright(tmp_path: Path) -> None:
    assert "E-UNITFONT" not in _codes(tmp_path, "其质量为 $m = 3.2\\,\\mathrm{kg}$ 时结果稳定。")


# ── E-NUMSTYLE ───────────────────────────────────────────────────────────────


def test_numstyle_flags_arabic_approximations_and_latin_ordinals(tmp_path: Path) -> None:
    approx = _by_code(_findings(tmp_path, "实验重复了 10 几次。"), "E-NUMSTYLE")
    ordinal = _by_code(_findings(tmp_path, "参见第 1st 章的说明。"), "E-NUMSTYLE")

    assert approx and ordinal
    assert all(f.tier == "candidate" for f in approx + ordinal)


def test_numstyle_exempts_figure_and_chapter_numbering(tmp_path: Path) -> None:
    assert "E-NUMSTYLE" not in _codes(tmp_path, "如图 3 多组结果所示，该趋势稳定。")


# ── E-LONGSENT ───────────────────────────────────────────────────────────────


def test_longsent_flags_a_single_over_long_sentence(tmp_path: Path) -> None:
    long_sentence = (
        "本文提出了一种融合注意力机制与图卷积网络的时间序列预测模型，"
        "该模型通过引入多尺度特征提取模块与自适应权重分配策略，"
        "在保持较低计算开销的同时显著提升了长期预测精度，"
        "并在多个公开数据集上验证了其有效性与鲁棒性。"
    )
    findings = _by_code(_findings(tmp_path, long_sentence), "E-LONGSENT")

    assert findings
    assert findings[0].tier == "candidate"
    assert "moderate" in findings[0].candidate


def test_longsent_exempts_enumerated_items(tmp_path: Path) -> None:
    item = "（1）" + "本文提出了一种融合注意力机制与图卷积网络的时间序列预测模型" * 3 + "。"
    assert "E-LONGSENT" not in _codes(tmp_path, item)


# ── Boundaries this module must not cross ────────────────────────────────────


def test_no_person_checker_exists() -> None:
    """人称归 abstract 的 T-VOICE / T-OPEN；这里出现人称检查即为越界。"""
    source = (SKILLS_ROOT / "latex-thesis-zh" / "scripts" / "check_style_zh.py").read_text(
        encoding="utf-8"
    )
    codes = {
        line.split('code="')[1].split('"')[0] for line in source.splitlines() if 'code="E-' in line
    }
    assert codes == {
        "E-COLLOQ",
        "E-ABSOLUTE",
        "E-COLLOC",
        "E-INCOMP",
        "E-PUNCT",
        "E-NUMSPACE",
        "E-UNITFONT",
        "E-NUMSTYLE",
        "E-LONGSENT",
    }, f"checker set drifted: {sorted(codes)}"


def test_first_person_wording_is_not_reported_here(tmp_path: Path) -> None:
    assert not _codes(tmp_path, "我们提出了一种新的求解框架。")


# ── C1 contract fields and edit axes ─────────────────────────────────────────


def test_report_carries_the_four_contract_fields(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        "\\documentclass{ctexbook}\n\\begin{document}\n很多研究表明该方法有效。\n\\end{document}\n",
        encoding="utf-8",
    )
    checker = check_style_zh.ChineseStyleChecker(tex)
    report = check_style_zh.generate_report(checker.analyze())

    for field in ("% Changed:", "% Protected:", "% Meaning-Check:", "% Risk-Flags:"):
        assert field in report
    assert "% Meaning-Check: NEEDS-LLM" in report
    assert "PRESERVED" not in report


def test_report_records_the_declared_envelope(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        "\\documentclass{ctexbook}\n\\begin{document}\n很多研究表明该方法有效。\n\\end{document}\n",
        encoding="utf-8",
    )
    checker = check_style_zh.ChineseStyleChecker(tex)
    report = check_style_zh.generate_report(checker.analyze(None, "concision", "moderate"))

    assert "% CONTRACT [Script]: goal=concision strength=moderate" in report


def test_unsupported_goal_routes_to_logic(tmp_path: Path) -> None:
    tex = tmp_path / "main.tex"
    tex.write_text(
        "\\documentclass{ctexbook}\n\\begin{document}\n很多研究表明该方法有效。\n\\end{document}\n",
        encoding="utf-8",
    )
    checker = check_style_zh.ChineseStyleChecker(tex)
    result = checker.analyze(None, "coherence", "minimal")

    assert result.routed_to == "logic"
    assert not result.findings
    assert "`logic` 模块" in check_style_zh.generate_report(result)


def test_multi_file_project_locates_the_source_file(tmp_path: Path) -> None:
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    (chapters / "chap01.tex").write_text("很多研究表明该方法有效。\n", encoding="utf-8")
    main = tmp_path / "main.tex"
    main.write_text(
        "\\documentclass{ctexbook}\n\\begin{document}\n"
        "\\include{chapters/chap01}\n\\end{document}\n",
        encoding="utf-8",
    )

    findings = check_style_zh.ChineseStyleChecker(main).analyze().findings

    assert findings
    assert any(f.loc.startswith("chapters/chap01.tex:") for f in findings), [
        f.loc for f in findings
    ]
