"""latex-thesis-zh/scripts/check_claim_forward.py 回归覆盖。"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT

_SCRIPT = SCRIPT_DIR_ZH / "check_claim_forward.py"
_FIXTURE = SKILLS_ROOT / "latex-thesis-zh" / "evals" / "fixtures" / "claim_forward_cases_zh.tex"


_SHARED_MODULE_NAMES = ("parsers", "tex_loader")


def _load_module():
    """Isolated path-loader (see test_analyze_conclusion.py).

    ZH scripts sit *after* EN on sys.path, so a bare ``import parsers`` inside the
    script would resolve to the EN copy (no Chinese chapter-title rules). Load the
    ZH copies explicitly and restore the shared modules afterwards.
    """
    saved_path = list(sys.path)
    saved_modules = {n: sys.modules.pop(n, None) for n in _SHARED_MODULE_NAMES}
    try:
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec = importlib.util.spec_from_file_location("check_claim_forward_zh", _SCRIPT)
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


cf = _load_module()


def _findings(path: Path, section: str | None = None):
    findings, errors, _meta = cf.run(path, section)
    return findings, errors


def _write(tmp_path: Path, body: str, *, chapter: str = "绪论") -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    tex = tmp_path / "main.tex"
    tex.write_text(
        "\\documentclass{ctexart}\n\\begin{document}\n\\chapter{"
        + chapter
        + "}\n"
        + body
        + "\n\\end{document}\n",
        encoding="utf-8",
    )
    return tex


def test_fixture_hits_each_code_once_and_boundaries_stay_silent() -> None:
    findings, errors = _findings(_FIXTURE)
    assert not errors
    counts = {code: len([f for f in findings if f.code == code]) for code in cf.CODES}
    assert counts == dict.fromkeys(cf.CODES, 1), counts
    originals = "".join(f.original for f in findings)
    assert "仅为0.018" not in originals  # Case H 裸“仅为”
    assert "尚未解决" not in originals  # Case I 痛点词
    assert "普通硬件上达到实时速率" not in originals  # Case F 引用句
    assert "离线方法" not in originals  # Case F 引用后主语为“该类方法”
    assert "强光照变化" not in originals  # Case G 不足小节


def test_fixture_severity_and_priority_follow_contract() -> None:
    findings, _ = _findings(_FIXTURE)
    table = {f.code: (f.severity, f.priority) for f in findings}
    assert table["CF-DISCLAIM"] == ("Minor", "P2")
    assert table["CF-SELFWEAK"] == ("Minor", "P2")
    assert table["CF-CAVEAT-POS"] == ("Info", "P3")
    assert table["CF-HEDGE-STACK"] == ("Info", "P3")
    assert table["CF-CLOSE-NEG"] == ("Minor", "P2")


def test_disclaim_is_info_outside_high_impact_chapters(tmp_path: Path) -> None:
    tex = _write(
        tmp_path, "本文不试图覆盖室外场景。本文在室内场景上将准确率提高5\\%。", chapter="方法设计"
    )
    findings, _ = _findings(tex)
    d = next(f for f in findings if f.code == "CF-DISCLAIM")
    assert (d.severity, d.priority) == ("Info", "P3")


def test_disclaim_skipped_in_related_work_and_scope_section(tmp_path: Path) -> None:
    tex = _write(
        tmp_path, "本文不试图综述全部跟踪方法。本文给出三类最相关的方法。", chapter="相关工作"
    )
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code == "CF-DISCLAIM"]
    tex2 = _write(
        tmp_path / "scope",
        "\\section{研究范围}\n本文不讨论室外场景。本文提出的方法在室内场景上提升5\\%。",
        chapter="绪论",
    )
    findings, _ = _findings(tex2)
    assert not [f for f in findings if f.code in {"CF-DISCLAIM", "CF-CAVEAT-POS"}]


def test_caveat_pos_candidate_keeps_the_limitation(tmp_path: Path) -> None:
    tex = _write(
        tmp_path, "虽然本研究只使用了一个数据集，趋势是一致的。本文提出的方法相比基线提升7\\%。"
    )
    findings, _ = _findings(tex)
    cav = [f for f in findings if f.code == "CF-CAVEAT-POS"]
    assert len(cav) == 1
    assert cav[0].candidate.startswith("本文提出的方法")
    assert "虽然本研究只使用了一个数据集" in cav[0].candidate


def test_selfweak_subject_gate_and_citation_exemption(tmp_path: Path) -> None:
    tex = _write(
        tmp_path,
        "已有方法\\upcite{a}未能处理长序列漂移。该类方法在长序列上仍明显落后于离线方法。"
        "现有方法仅能处理固定帧率。本文提出一种校正器消除该漂移。",
        chapter="讨论",
    )
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code == "CF-SELFWEAK"]
    own = _write(tmp_path / "own", "本文方法仅能处理固定帧率的输入。", chapter="实验结果")
    findings, _ = _findings(own)
    sw = [f for f in findings if f.code == "CF-SELFWEAK"]
    assert len(sw) == 1 and "能够" in sw[0].candidate


def test_selfweak_bare_jin_and_shangwei_not_flagged(tmp_path: Path) -> None:
    tex = _write(
        tmp_path,
        "本文方法的误差仅为0.018，不仅优于基线，而且内存更低。现有方法尚未解决该问题。",
        chapter="实验结果",
    )
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code == "CF-SELFWEAK"]


def test_hedge_stack_threshold_and_outlook_exception(tmp_path: Path) -> None:
    two = _write(tmp_path / "two", "本文提出的方法可能或许能够提升召回率。", chapter="方法设计")
    three = _write(
        tmp_path / "three", "本文提出的方法可能在一定程度上或许能够提升召回率。", chapter="方法设计"
    )
    non_claim = _write(tmp_path / "nc", "天气可能在一定程度上或许会变化。", chapter="方法设计")
    outlook = _write(
        tmp_path / "ol",
        "本文提出的方法有望在一定程度上或许能够扩展到室外场景。",
        chapter="结论与展望",
    )
    for path, expected in ((two, 0), (three, 1), (non_claim, 0), (outlook, 0)):
        findings, _ = _findings(path)
        assert len([f for f in findings if f.code == "CF-HEDGE-STACK"]) == expected, path


def test_close_neg_suppressed_by_outlook_transition(tmp_path: Path) -> None:
    body = (
        "本文验证了12\\%的准确率提升。\n\n"
        "本文提出的框架达到实时速率。然而，该框架无法处理帧率可变的输入，这有待后续工作扩展缓冲机制。"
    )
    tex = _write(tmp_path, body, chapter="结论与展望")
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code == "CF-CLOSE-NEG"]


def test_close_neg_only_in_final_paragraph_of_closing_chapters(tmp_path: Path) -> None:
    body = "本文提出的框架达到实时速率。然而，该框架无法处理帧率可变的输入。\n\n本文整体验证了12\\%的提升。"
    tex = _write(tmp_path, body, chapter="结论与展望")
    findings, _ = _findings(tex)
    assert not [f for f in findings if f.code == "CF-CLOSE-NEG"]
    disc = _write(
        tmp_path / "d",
        "本文提出的框架达到实时速率。然而，该框架无法处理帧率可变的输入。",
        chapter="讨论",
    )
    findings, _ = _findings(disc)
    assert not [f for f in findings if f.code == "CF-CLOSE-NEG"]


def test_limitation_section_is_exempt(tmp_path: Path) -> None:
    tex = _write(
        tmp_path,
        "\\section{本文的不足}\n本文的评估未能覆盖室外场景。本文仅能在室内基准上给出结果。",
        chapter="结论与展望",
    )
    findings, _ = _findings(tex)
    assert not findings


def test_missing_section_reports_error_and_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(_SCRIPT), str(_FIXTURE), "--section", "nosuch"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert result.returncode == 0
    assert "ERROR [Severity: Critical] [Priority: P0]: Section not found: nosuch" in result.stdout


def test_text_output_uses_contract_block_shape() -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(_SCRIPT), str(_FIXTURE), "--section", "conclusion"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert result.returncode == 0
    lines = result.stdout.splitlines()
    heads = [ln for ln in lines if ln.startswith("% CLAIM-FORWARD (")]
    assert heads and "[Script] CF-CLOSE-NEG" in heads[0]
    assert any(ln.startswith("% Original: ") for ln in lines)
    assert any(ln.startswith("% Candidate: ") for ln in lines)
    assert "% Meaning-Check: NEEDS-LLM" in lines
    assert not any("PRESERVED" in ln for ln in lines)


def test_json_output_fields() -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(_SCRIPT), str(_FIXTURE), "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["summary"]["total"] == 5
    assert set(payload["summary"]["by_code"]) == set(cf.CODES)
    for field in ("code", "line", "severity", "priority", "original", "candidate", "section"):
        assert field in payload["findings"][0]


def test_terms_yaml_matches_builtin_fallback() -> None:
    import yaml

    yaml_path = SKILLS_ROOT / "latex-thesis-zh" / "references" / "writing" / cf.TERMS_FILENAME
    data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    for key in cf._LIST_KEYS:
        assert data[key] == cf._DEFAULT_TERMS[key], key
    assert data["self_weakening"] == cf._DEFAULT_TERMS["self_weakening"]


def test_terms_fallback_when_yaml_missing_or_partial(tmp_path: Path) -> None:
    (tmp_path / "scripts").mkdir()
    terms, source = cf._load_terms(tmp_path / "scripts")
    assert source == "builtin" and terms["hedges"] == cf._DEFAULT_TERMS["hedges"]
    (tmp_path / "references" / "writing").mkdir(parents=True)
    (tmp_path / "references" / "writing" / cf.TERMS_FILENAME).write_text(
        "hedges: [大概]\nself_weakening: 3\n", encoding="utf-8"
    )
    terms, source = cf._load_terms(tmp_path / "scripts")
    assert source == "yaml"
    assert terms["hedges"] == ["大概"]
    assert terms["self_weakening"] == cf._DEFAULT_TERMS["self_weakening"]


@pytest.mark.parametrize("code", cf.CODES)
def test_positional_candidates_keep_the_original_sentence(code: str) -> None:
    findings, _ = _findings(_FIXTURE)
    f = next(f for f in findings if f.code == code)
    if code in {"CF-DISCLAIM", "CF-CAVEAT-POS", "CF-CLOSE-NEG"}:
        assert f.original in f.candidate
