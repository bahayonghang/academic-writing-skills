"""Lock corrected guidance and its input-bound output review corpus, not model quality."""

from __future__ import annotations

import hashlib
import json
import re

import pytest

from tests.support.paths import SKILLS_ROOT

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
