"""Tests for checker precision fixes (audit F5/F6/F7/F8/F16/F23/F24)."""

import importlib.util
import sys
from pathlib import Path

import pytest

from tests.support.paths import SCRIPT_DIR_ZH

_ZH_DIR = SCRIPT_DIR_ZH
_ZH_REFS = _ZH_DIR.parent / "references"


def _load_zh(name: str):
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

    spec = importlib.util.spec_from_file_location(f"zh_cp_{name}", _ZH_DIR / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
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


deai_check = _load_zh("deai_check")
check_consistency = _load_zh("check_consistency")
check_format = _load_zh("check_format")


# ── F5 破折号去重 ─────────────────────────────────────────────


class TestEmDashCounting:
    def test_two_em_dashes_do_not_trigger(self, tmp_path: Path):
        """2 处 "——" 在默认阈值 5 下不得告警（旧实现一处计 3 次会误报）。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\chapter{绪论}\n第一处——插入语。\n第二处——另一个插入语。\n",
            encoding="utf-8",
        )
        checker = deai_check.ChineseAITraceChecker(tex)
        analysis = checker.analyze_document()
        dash = [
            t for t in analysis["document_traces"] if t["pattern"] == "punctuation:em_dash_overuse"
        ]
        assert not dash

    def test_six_em_dashes_trigger(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        body = "\n".join(f"第{i}处——插入语。" for i in range(6))
        tex.write_text(f"\\chapter{{绪论}}\n{body}\n", encoding="utf-8")
        checker = deai_check.ChineseAITraceChecker(tex)
        analysis = checker.analyze_document()
        dash = [
            t for t in analysis["document_traces"] if t["pattern"] == "punctuation:em_dash_overuse"
        ]
        assert dash and "6 处" in dash[0]["text"]


# ── F6 全章节覆盖 ─────────────────────────────────────────────


def test_unmatched_chapter_included_in_analyze(tmp_path: Path):
    """标题为"多模态情感识别模型研究"的章必须进入章节级检查范围。"""
    tex = tmp_path / "main.tex"
    tex.write_text(
        "\\chapter{绪论}\n背景介绍。\n"
        "\\chapter{多模态情感识别模型研究}\n近年来，越来越多的研究关注此问题。\n",
        encoding="utf-8",
    )
    checker = deai_check.ChineseAITraceChecker(tex)
    analysis = checker.analyze_document()
    assert "多模态情感识别模型研究" in analysis["sections"]
    assert analysis["sections"]["多模态情感识别模型研究"]["trace_count"] >= 1


# ── F7 前向上下文参与误报过滤 ─────────────────────────────────


def test_false_positive_with_number_before(tmp_path: Path):
    """前文 20 字内已有具体百分比时，"显著提升"不再标记。"""
    tex = tmp_path / "main.tex"
    tex.write_text(
        "\\chapter{绪论}\n误差降低了12.5%，显著提升了模型表现。\n",
        encoding="utf-8",
    )
    checker = deai_check.ChineseAITraceChecker(tex)
    result = checker.check_section("introduction")
    empty = [t for t in result["traces"] if t["category"] == "empty_phrase"]
    assert not empty


# ── F8 PyYAML 可选 ────────────────────────────────────────────


def test_deai_check_works_without_pyyaml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """缺 PyYAML 的环境（import 失败）必须回落默认阈值而非崩溃。"""
    monkeypatch.setitem(sys.modules, "yaml", None)  # 使 `import yaml` 抛 ImportError
    tex = tmp_path / "main.tex"
    tex.write_text("\\chapter{绪论}\n近年来，研究增多。\n", encoding="utf-8")
    checker = deai_check.ChineseAITraceChecker(tex)
    assert checker.thresholds["punctuation"]["max_em_dashes_per_doc"] == 5
    result = checker.check_section("introduction")
    assert result["trace_count"] >= 1


# ── F16 术语组语义 ────────────────────────────────────────────


class TestConsistencySemantics:
    def test_canonical_full_then_abbrev_zero_false_positive(self, tmp_path: Path):
        """国标推荐写法：首次"卷积神经网络（CNN）"后文全用 CNN → 零误报。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "卷积神经网络（CNN）是一类深度模型。\n"
            "CNN 在图像任务中应用广泛。\n"
            "本文基于 CNN 设计了新结构。\n",
            encoding="utf-8",
        )
        checker = check_consistency.ConsistencyChecker([str(tex)])
        result = checker.check_terms()
        assert result["status"] == "PASS", result["inconsistencies"]

    def test_real_variant_drift_still_reported(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "深度神经网络是主流方法。\n深层学习也被广泛使用。\n",
            encoding="utf-8",
        )
        checker = check_consistency.ConsistencyChecker([str(tex)])
        result = checker.check_terms()
        assert result["status"] == "WARNING"
        assert any(i["type"] == "variant_mix" for i in result["inconsistencies"])

    def test_full_name_after_definition_flagged(self, tmp_path: Path):
        """缩写已定义后正文仍大量（≥3 次）使用全称 → 提示统一用缩写。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "卷积神经网络（CNN）是一类深度模型。\n"
            "卷积神经网络可以提取局部特征。\n"
            "卷积神经网络的层数影响感受野。\n"
            "卷积神经网络在多个任务上表现出色。\n",
            encoding="utf-8",
        )
        checker = check_consistency.ConsistencyChecker([str(tex)])
        result = checker.check_terms()
        hits = [i for i in result["inconsistencies"] if i["type"] == "full_after_abbrev"]
        assert hits
        assert "首次出现用全称" in hits[0]["suggestion"]

    def test_suggestion_never_says_unify_to_abbrev_blindly(self, tmp_path: Path):
        """建议语不再是"统一使用 'CNN'"这类与国标冲突的措辞。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "卷积神经网络（CNN）模型。\nCNN 应用。\nCNN 结构。\nCNN 层。\n",
            encoding="utf-8",
        )
        checker = check_consistency.ConsistencyChecker([str(tex)])
        result = checker.check_terms()
        for inc in result["inconsistencies"]:
            assert "统一使用 'CNN'" not in inc["suggestion"]

    def test_comment_occurrences_excluded(self, tmp_path: Path):
        """注释里的术语变体不计入统计（visible-text 过滤）。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "深度学习是主流方法。\n% 旧稿用的是深层学习，已废弃\n",
            encoding="utf-8",
        )
        checker = check_consistency.ConsistencyChecker([str(tex)])
        result = checker.check_terms()
        assert result["status"] == "PASS"

    def test_cite_key_pseudo_hit_excluded(self, tmp_path: Path):
        """\\cite 键里的缩写不算使用。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "深度学习方法\\cite{CNN2020}取得进展。\n",
            encoding="utf-8",
        )
        checker = check_consistency.ConsistencyChecker([str(tex)])
        result = checker.check_abbreviations()
        assert not any(i["abbreviation"] == "CNN" for i in result["issues"])


# ── F23 check_format 降噪 ─────────────────────────────────────


class TestFormatNoiseReduction:
    def test_women_downgraded_to_info(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("我们采用三层结构。\n", encoding="utf-8")
        checker = check_format.FormatChecker(str(tex))
        result = checker.check()
        pronoun = [i for i in result["issues"] if i["code"] == "oral_pronoun"]
        assert pronoun and pronoun[0]["severity"] == "info"
        assert "本文" in pronoun[0]["message"]
        # info-only → 整体 PASS（exit 0）
        assert result["status"] == "PASS"

    def test_vague_words_still_warning(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text("实验效果非常好。\n", encoding="utf-8")
        checker = check_format.FormatChecker(str(tex))
        result = checker.check()
        vague = [i for i in result["issues"] if i["code"] == "oral_vague"]
        assert vague and vague[0]["severity"] == "warning"
        assert result["status"] == "WARNING"

    def test_math_and_verbatim_not_flagged(self, tmp_path: Path):
        tex = tmp_path / "main.tex"
        tex.write_text(
            "设 $x_一些 = 1$ 为变量。\n\\begin{lstlisting}\n我们 = load()\n\\end{lstlisting}\n",
            encoding="utf-8",
        )
        checker = check_format.FormatChecker(str(tex))
        result = checker.check()
        oral = [i for i in result["issues"] if i["code"] in ("oral_pronoun", "oral_vague")]
        assert not oral


# ── R5 源码卫生检查 F-MD / F-NOTE ─────────────────────────────


class TestFormatSourceHygiene:
    def test_markdown_bold_flagged_major(self, tmp_path: Path):
        """可见正文里的 Markdown **加粗** 命中 F-MD，且为 actionable（status WARNING）。"""
        tex = tmp_path / "main.tex"
        tex.write_text("本文研究 **多尺度耦合软测量问题** 的建模方法。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        md = [i for i in result["issues"] if i["code"] == "F-MD"]
        assert md and md[0]["severity"] == "warning"
        assert md[0]["line"] == 1
        assert result["status"] == "WARNING"

    def test_escaped_asterisks_not_flagged(self, tmp_path: Path):
        r"""转义星号 \*\* 是字面星号意图（反斜杠隔开无连续两星），不得命中 F-MD。"""
        tex = tmp_path / "main.tex"
        tex.write_text("正则用 \\*\\*通配\\*\\* 表示任意匹配。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "F-MD"]

    def test_double_star_in_math_not_flagged(self, tmp_path: Path):
        """数学环境内的 ** 被 extract_visible_text 剥离，不得命中 F-MD。"""
        tex = tmp_path / "main.tex"
        tex.write_text("指数关系 $y = a**b**c$ 成立。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "F-MD"]

    def test_textbf_not_flagged(self, tmp_path: Path):
        r"""规范的 \textbf{} 写法不得命中 F-MD（避免误伤正确 LaTeX）。"""
        tex = tmp_path / "main.tex"
        tex.write_text("本文研究 \\textbf{多尺度耦合软测量问题} 的建模。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "F-MD"]

    def test_draft_note_flagged_info_only(self, tmp_path: Path):
        """草稿备注命中 F-NOTE 且仅为 info —— 单独出现时整体仍 PASS。"""
        tex = tmp_path / "main.tex"
        tex.write_text("图中占位示意，后续可根据现场图纸替换。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        note = [i for i in result["issues"] if i["code"] == "F-NOTE"]
        assert note and note[0]["severity"] == "info"
        assert note[0]["line"] == 1
        assert result["status"] == "PASS"

    def test_academic_hedging_not_flagged(self, tmp_path: Path):
        """正常学术让步表述（"仍需通过实验确认"）不含备注词形，不得命中 F-NOTE。"""
        tex = tmp_path / "main.tex"
        tex.write_text("该结论仍需通过实验确认，有待进一步研究。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "F-NOTE"]


# ── R2b mixed_punctuation 路径参数剥离 ─────────────────────────


class TestMixedPunctuationPathStrip:
    def test_chinese_figure_name_not_flagged(self, tmp_path: Path):
        r"""\includegraphics/\input 的中文图名+扩展名点号不得触发 mixed_punctuation（R2b 负例）。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\begin{figure}\n"
            "\\includegraphics[width=0.8\\textwidth]{系统总体框架图.png}\n"
            "\\input{chapters/数据预处理.tex}\n"
            "\\end{figure}\n",
            encoding="utf-8",
        )
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "mixed_punctuation"]

    def test_real_mixed_punctuation_still_flagged(self, tmp_path: Path):
        """真正的可见正文"中文,英文"混排仍命中（剥离逻辑不波及正文，R2b 正例）。"""
        tex = tmp_path / "main.tex"
        tex.write_text("本文提出方法,effectiveness 得到验证。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        mixed = [i for i in result["issues"] if i["code"] == "mixed_punctuation"]
        assert mixed and mixed[0]["line"] == 1

    def test_mixed_punctuation_on_figure_line_with_real_error(self, tmp_path: Path):
        """同一行既有中文图名又有真正文混排：图名假阳消除，正文真错仍命中。"""
        tex = tmp_path / "main.tex"
        tex.write_text("见\\includegraphics{框架图.png}，效果好,很明显。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        mixed = [i for i in result["issues"] if i["code"] == "mixed_punctuation"]
        # 只应命中"好,"这一处（半角逗号），"框架图.png"的点号被剥离。
        assert len(mixed) == 1


# ── R2c oral_vague "特别"词边界 ────────────────────────────────


class TestOralVagueTebie:
    def test_tebie_shuoming_not_flagged(self, tmp_path: Path):
        """ "需特别说明"是书面语，不得命中 oral_vague（R2c 负例，修复前会误报）。"""
        tex = tmp_path / "main.tex"
        tex.write_text("需特别说明的是，本文采用固定划分。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "oral_vague"]

    def test_tebie_shi_and_di_not_flagged(self, tmp_path: Path):
        """书面连接词"特别是/特别地"不得命中（R2c 负例）。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "多种工况，特别是高负荷段，误差较大。特别地，需单独建模。\n", encoding="utf-8"
        )
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "oral_vague"]

    def test_tebie_hao_still_flagged(self, tmp_path: Path):
        """ "特别好/特别快"等口语用法仍命中 oral_vague（R2c 正例）。"""
        tex = tmp_path / "main.tex"
        tex.write_text("该方法特别好，收敛特别快。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        vague = [i for i in result["issues"] if i["code"] == "oral_vague"]
        assert vague and vague[0]["severity"] == "warning"


# ── R3b F-NOTE 对冲组扩表 ─────────────────────────────────────


class TestDraftNoteHedge:
    def test_hedge_expression_flagged_info(self, tmp_path: Path):
        """未定稿对冲词（暂以占位/待验证/仍在进行）命中 F-NOTE-HEDGE，severity info（R3b 正例）。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "此参数暂以占位，数值待验证。实验仍在进行。\n",
            encoding="utf-8",
        )
        result = check_format.FormatChecker(str(tex)).check()
        hedge = [i for i in result["issues"] if i["code"] == "F-NOTE-HEDGE"]
        assert hedge and all(h["severity"] == "info" for h in hedge)
        # 文案与核心草稿备注区分开
        assert "对冲" in hedge[0]["message"]

    def test_fusuan_bare_flagged(self, tmp_path: Path):
        """ "按第2章口径复算"裸用法命中（R3b 正例，护栏方向一）。"""
        tex = tmp_path / "main.tex"
        tex.write_text("各项指标按第 2 章口径复算。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        assert [i for i in result["issues"] if i["code"] == "F-NOTE-HEDGE"]

    def test_fusuan_result_not_flagged(self, tmp_path: Path):
        """ "复算结果一致"是正常学术用法，负向断言挡下（R3b 负例，护栏方向二）。"""
        tex = tmp_path / "main.tex"
        tex.write_text("与原文献相比，复算结果一致，验证了实现正确性。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "F-NOTE-HEDGE"]

    def test_core_note_unaffected_by_hedge_split(self, tmp_path: Path):
        """拆表后核心草稿备注仍归 F-NOTE（不误标 HEDGE），保证存量口径不变。"""
        tex = tmp_path / "main.tex"
        tex.write_text("图中占位示意，后续可根据现场图纸替换。\n", encoding="utf-8")
        result = check_format.FormatChecker(str(tex)).check()
        assert [i for i in result["issues"] if i["code"] == "F-NOTE"]
        assert not [i for i in result["issues"] if i["code"] == "F-NOTE-HEDGE"]


# ── R3c F-PLACEHOLDER 占位符表格行 ────────────────────────────


class TestPlaceholderTableRow:
    def test_placeholder_row_flagged_warning(self, tmp_path: Path):
        """表体行 ≥2 个空占位单元格命中 F-PLACEHOLDER，severity warning（R3c 正例）。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\begin{tabular}{lll}\n"
            "方法 & 精度 & 召回 \\\\\n"
            "本文 & --- & --- \\\\\n"
            "\\end{tabular}\n",
            encoding="utf-8",
        )
        result = check_format.FormatChecker(str(tex)).check()
        ph = [i for i in result["issues"] if i["code"] == "F-PLACEHOLDER"]
        assert ph and ph[0]["severity"] == "warning"
        assert ph[0]["line"] == 3

    def test_single_dash_cell_not_flagged(self, tmp_path: Path):
        """单个 - 单元格（合法负号/缺省）不报（R3c 负例）。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\begin{tabular}{lll}\n偏差 & -0.5 & - \\\\\n\\end{tabular}\n",
            encoding="utf-8",
        )
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "F-PLACEHOLDER"]

    def test_normal_data_row_not_flagged(self, tmp_path: Path):
        """正常数值行不报（R3c 负例）。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\begin{tabular}{lll}\n本文 & 3.5 & 4.2 \\\\\n\\end{tabular}\n",
            encoding="utf-8",
        )
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "F-PLACEHOLDER"]

    def test_na_marker_with_real_data_not_flagged(self, tmp_path: Path):
        """以 --- 标"不适用"但同行含真实数字的正常表格不报（用户 ch5 L631/632 型，防新增假阳）。"""
        tex = tmp_path / "main.tex"
        tex.write_text(
            "\\begin{tabular}{lllll}\nAPC & --- & --- & 91.1 & 0.24 \\\\\n\\end{tabular}\n",
            encoding="utf-8",
        )
        result = check_format.FormatChecker(str(tex)).check()
        assert not [i for i in result["issues"] if i["code"] == "F-PLACEHOLDER"]


# ── 旗标与文档 ────────────────────────────────────────────────


def test_optimize_title_interactive_flag_removed():
    source = (_ZH_DIR / "optimize_title.py").read_text(encoding="utf-8")
    assert "--interactive" not in source


def test_deai_guide_covers_aigc_policy():
    """guide.md 新增小节须含校级阈值案例与误判提示，且无"包过检测"类措辞。"""
    guide = (_ZH_REFS / "deai" / "guide.md").read_text(encoding="utf-8")
    assert "AIGC 检测政策" in guide
    assert "四川大学" in guide and "40%" in guide  # 校级阈值案例
    assert "误判" in guide
    assert "允许辅助" in guide and "禁止代写" in guide
    for banned in ("包过", "保证通过检测", "确保通过检测", "帮你规避检测"):
        assert banned not in guide
