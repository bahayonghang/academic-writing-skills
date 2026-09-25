"""Lock corrected guidance and its input-bound output review corpus, not model quality."""

from __future__ import annotations

import hashlib
import json
import re

import pytest

from tests.support.paths import REPO_ROOT, SKILLS_ROOT

SKILL = SKILLS_ROOT / "latex-thesis-zh"
FIXTURE = "evals/fixtures/guidance_fidelity.tex"


def _read(relative: str) -> str:
    return (SKILL / relative).read_text(encoding="utf-8")


def test_philosophy_does_not_replace_uncertainty_with_invented_measurements() -> None:
    text = _read("references/writing/writing-philosophy-zh.md")
    for shortcut in (
        '"可能有助于提升" → ✅ "准确率提升了3.2%"',
        '"大幅提升" → ✅ "提升了12.3%"',
        '"显著" → ✅ "统计显著 (p < 0.05)"',
    ):
        assert shortcut not in text
    assert "保留不确定性" in text
    assert "不得补造" in text
    assert "(results-analysis-guide-zh.md)" in text


def test_axes_single_accuracy_supports_an_observation_not_a_mechanism() -> None:
    text = _read("references/modules/logic.md")
    axes = text.split("## AXES Model", 1)[1].split("## Heading Lead-In", 1)[0]
    assert "95%" in axes
    assert "没有比较基线" in axes
    assert "这一提升源于其捕获长程依赖的能力" not in axes
    assert "(../writing/results-analysis-guide-zh.md)" in axes


def test_claim_wording_cannot_substitute_labels_or_hedges_for_evidence() -> None:
    text = _read("references/writing/over-claim-guard.md")
    for shortcut in (
        "← 干预实验（消融/受控对比）",
        "否则一律用相关性表述",
        '没有就加"据我们所知"',
        "据我们所知，首次 / 最早的工作之一",
        '得到因果结果 → 用"证明"',
    ):
        assert shortcut not in text
    assert "(results-analysis-guide-zh.md)" in text
    assert "训练预算不同" in text
    assert "组件贡献" in text and "区分性证据" in text
    assert re.search(r"未检索.*移除.*待核", text)
    assert "保留证据支持的强结论" in text


def test_chapter_advice_defers_to_school_and_actual_evidence() -> None:
    philosophy = _read("references/writing/writing-philosophy-zh.md")
    abstract = _read("references/writing/abstract-structure.md")
    assert "同一句并列引用不超过 2 个" not in philosophy
    assert "逐篇讨论每篇文献" not in philosophy
    assert "(../modules/literature.md)" in philosophy
    assert "(engineering-application-chapter-guide-zh.md)" in philosophy
    assert "GPU" in philosophy and "无需" in philosophy
    assert "Chinese thesis (GB/T)" not in abstract
    assert "five-model writing references" in abstract
    assert "学校" in abstract and "优先" in abstract
    assert "900~1200" in abstract and "500~650" in abstract


def test_conclusion_guidance_separates_synthesis_from_abstract_problem_opening() -> None:
    text = _read("references/writing/conclusion-guide-zh.md")
    assert "首段总领式总述" in text
    assert "全文方法链" in text
    assert "提出/建立/构建/设计了" in text
    assert "“针对……问题”可以补充问题背景，但不是结论条目的必备起句" in text
    assert '每条贡献遵循骨架"**针对……问题' not in text


def test_reverse_outline_keeps_a_sound_paragraph_and_limits_edit_authority() -> None:
    text = _read("examples/logic-and-experiment.md")
    for token in (
        "段主题",
        "章目标",
        "证据",
        "处置",
        "chapters/review.tex:24",
        "chapters/review.tex:29",
        "chapters/review.tex:33",
        "保留",
        "收窄",
        "移位",
        "current",
        "prev.tail",
        "next.head",
        "(../references/writing/paragraph-arc-zh.md)",
        "(../references/writing/subsection-context-zh.md)",
    ):
        assert token in text
    assert "没有显式过渡词" in text
    assert "不改正文" in text


def test_output_eval_binds_all_eight_input_cases_without_expected_answers_in_fixture() -> None:
    payload = json.loads(_read("evals/evals.json"))
    matches = [entry for entry in payload["evals"] if FIXTURE in entry.get("files", [])]
    assert len(matches) == 1
    entry = matches[0]
    fixture = _read(FIXTURE)
    assert re.findall(r"^% 场景 (\d+)$", fixture, re.MULTILINE) == list("12345678")
    assert "expected_output" not in fixture and "assertions" not in fixture
    assert "八个" in entry["prompt"]
    for token in (
        "可能",
        "95\\%",
        "100轮",
        "50轮",
        "区分",
        "噪声通路N",
        "没有检索",
        "1000—1500",
        "CPU",
        "\\cite{regular,masked,survey}",
        "$z=x+\\epsilon$",
        "\\ref{tab:intervention}",
    ):
        assert token in fixture
    contract = entry["expected_output"]
    for number in range(1, 9):
        assert f"场景{number}" in contract
    assert "保真" in contract and "独立" in contract


@pytest.mark.parametrize(
    ("filename", "key", "count", "digest"),
    (
        (
            "evals.json",
            "evals",
            47,
            "75b2a0bcbd22894c16f9b13c1d5e661e35229f73189e6f5298ee353574d52823",
        ),
        (
            "trigger_eval.json",
            "queries",
            49,
            "3c4fbce369f0b690bfc4a4ab5f32299f94f377daf8a4a65bb59106563b73a573",
        ),
    ),
)
def test_historical_eval_prefix_is_unchanged(
    filename: str, key: str, count: int, digest: str
) -> None:
    items = json.loads(_read(f"evals/{filename}"))[key]
    prefix = json.dumps(items[:count], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    assert hashlib.sha256(prefix.encode("utf-8")).hexdigest() == digest


_METHOD_LABELS = (
    "M-CODLANG",
    "M-FIGTEXT",
    "M-FORMDUPE",
    "M-SEMICOLON",
    "N-ISOLATE",
    "M-DETAILINV",
    "M-TERMREG",
    "M-REDUNDANT",
)


def test_method_expression_labels_are_llm_document_checks() -> None:
    text = _read("references/writing/method-description-guide-zh.md")
    for label in _METHOD_LABELS:
        start = text.index(label)
        window = text[start : start + 400]
        assert "范围" in window
        assert "问题例" in window
        assert "改写例" in window
        assert "风险" in window
        assert "LLM" in window
    assert "不得把二者报成同一缺陷" in text
    assert "PR-EQ-NARR" in text
    assert "M-REPRO" in text and "复现" in text
    assert "polish_unit_zh.py --verify" in text
    assert "UP-MATH" in text
    assert "不声称" in text and "语义" in text
    assert "不改数学" in text
    assert "若实现脚本" not in text
    assert "若以后实现" not in text
    assert "[Severity:" in text and "[Priority:" in text and "[LLM]" in text


def test_claim_forward_three_dispositions_keep_and_reject_examples() -> None:
    text = _read("references/writing/claim-forward-zh.md")
    assert text.count("可保留") >= 3
    assert text.count("不可改") >= 3
    assert "未验证的弱点不得写成设计优点" in text
    assert "不得删除" in text
    assert "不是禁词正则" in text
    assert "门禁" in text and "筑牢" in text
    assert "CF-METAPHOR" not in text
    assert "只由 LLM" in text
    assert "[Severity:" in text and "[LLM]" in text


def test_deleted_preview_keeps_an_antecedent_and_legal_sequence_words() -> None:
    text = _read("references/writing/paragraph-roles-zh.md")
    assert "上述" in text and "先行词" in text and "最短" in text
    assert "不得把删掉的预告贴回去" in text
    bridge = text.split("最短桥接：", 1)[1].splitlines()[0]
    revised = text.split("% 修改后：", 1)[1].splitlines()[0]
    assert "上述" in bridge and "上述" in revised
    assert "下一节先对齐" not in bridge
    assert "首先" in text and "其次" in text
    assert "不是去重" in text
    assert "只由 LLM" in text
    assert "[Severity:" in text and "[LLM]" in text


def test_abstract_quotes_and_english_punctuation_keep_payload() -> None:
    text = _read("references/writing/abstract-structure.md")
    assert "U+201C" in text and "U+201D" in text
    assert "英文标点" in text
    assert "中文通过" in text and "中文不通过" in text
    assert "英文通过" in text and "英文不通过" in text
    assert "lee2020" in text
    assert "一步估计" in text
    assert "T-QUOTE" not in text
    assert "只由 LLM" in text
    assert "`analyze_abstract.py` 不检查引号" in text


def test_title_and_arrangement_examples_do_not_authorize_body_edits() -> None:
    structure = _read("references/writing/structure-guide.md")
    introduction = _read("references/writing/introduction-guide-zh.md")
    limit = "不授权改正文数学、受保护术语或模型名。"
    assert limit in structure and limit in introduction
    assert "非平稳序列的状态估计方法" in structure
    assert "第 3 章给出状态估计方法" in introduction
    assert "只由 LLM" in structure and "只由 LLM" in introduction
    assert "[LLM]" in structure and "[LLM]" in introduction


def test_c6_routes_stay_on_existing_modules() -> None:
    skill = _read("SKILL.md")
    routing = _read("references/modules/routing-rules.md")
    for token in (
        "张量",
        "交换轴",
        "Concat",
        "方法一致",
        "claim-forward",
        "上述",
        "U+201C",
        "公式符号",
        "structure",
        "不新增脚本码",
    ):
        assert token in skill
        assert token in routing
    modules = re.findall(r"^\| `([^`]+)`\s*\|", skill, re.M)
    assert "logic" in modules and "claim-forward" in modules
    assert "abstract" in modules and "structure" in modules
    assert "method-expression" not in modules
    assert modules.count("logic") == 1
    method_spec = (
        REPO_ROOT / ".trellis/spec/academic-writing-skills/method-narrative-contract.md"
    ).read_text(encoding="utf-8")
    claim_spec = (
        REPO_ROOT / ".trellis/spec/academic-writing-skills/claim-forward-contract.md"
    ).read_text(encoding="utf-8")
    role_spec = (
        REPO_ROOT / ".trellis/spec/academic-writing-skills/paragraph-roles-contract.md"
    ).read_text(encoding="utf-8")
    assert "不得把二者报成同一缺陷" in method_spec
    assert "不新增观察码" in claim_spec
    assert "不得把删掉的预告贴回去" in role_spec


def test_c6_eval_checks_route_and_do_not_rewrite_without_a_live_run() -> None:
    payload = json.loads(_read("evals/evals.json"))
    ids = [item["id"] for item in payload["evals"]]
    assert ids == sorted(ids)
    assert len(set(ids)) == len(ids)
    assert ids[-1] == 58
    entry = payload["evals"][-1]
    assert "logic" in entry["expected_output"]
    assert "claim-forward" in entry["expected_output"]
    assert "设计优点" in entry["expected_output"]
    assert "不代表已运行" in entry["expected_output"]
    blob = json.dumps(entry, ensure_ascii=False)
    assert "live model passed" not in blob
