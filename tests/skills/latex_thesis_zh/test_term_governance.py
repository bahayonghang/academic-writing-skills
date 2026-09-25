"""Opt-in term governance, abbreviation style, and degree-wording contracts."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_ZH, SKILLS_ROOT

FIXTURE = SKILLS_ROOT / "latex-thesis-zh" / "evals" / "fixtures" / "term-governance"
PASS_MARKERS = (
    "No inconsistencies",
    "no governance candidates",
    "no abbreviation-style candidates",
    "✅",
    "Status: PASS",
)


def _load(name: str, filename: str):
    saved_path = sys.path[:]
    saved_modules = sys.modules.copy()
    try:
        sys.modules.pop("parsers", None)
        sys.modules.pop("tex_loader", None)
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR_ZH / filename)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for module_name in set(sys.modules) - set(saved_modules):
            del sys.modules[module_name]
        sys.modules.update(saved_modules)


consistency = _load("zh_term_governance_consistency", "check_consistency.py")
style = _load("zh_term_governance_style", "check_style_zh.py")


def test_loaders_resolve_the_zh_copies() -> None:
    assert (
        Path(consistency.__file__).resolve() == (SCRIPT_DIR_ZH / "check_consistency.py").resolve()
    )
    assert Path(style.__file__).resolve() == (SCRIPT_DIR_ZH / "check_style_zh.py").resolve()
    assert hasattr(consistency, "load_governance_terms")
    assert hasattr(style, "DEGREE_PHRASES")


def _write(root: Path, name: str, content: str) -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _cli(script: str, path: Path, *args: str):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(SCRIPT_DIR_ZH / script), str(path), *args],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
        timeout=30,
    )


def _checker(tmp_path: Path, content: str, config: dict | None, *, name: str = "main.tex"):
    path = _write(tmp_path, name, content)
    payload = None
    if config is not None:
        terms = _write(tmp_path, "terms.json", json.dumps(config, ensure_ascii=False))
        payload = consistency.load_governance_terms(str(terms))
    return consistency.ConsistencyChecker(
        [str(path)],
        entry_file=str(path),
        governance=payload,
    )


def _kinds(result: dict, kind: str) -> list[dict]:
    return [finding for finding in result["findings"] if finding["kind"] == kind]


def test_governance_requires_custom_terms_and_rejects_bad_input(tmp_path: Path) -> None:
    tex = _write(tmp_path, "main.tex", "\\begin{document}\n旧称。\n\\end{document}\n")
    missing_flag = _cli("check_consistency.py", tex, "--governance")
    assert missing_flag.returncode != 0
    assert "[ERROR]" in missing_flag.stderr
    assert "--governance requires --custom-terms" in missing_flag.stderr
    assert not any(marker in missing_flag.stdout for marker in PASS_MARKERS)

    absent = tmp_path / "absent.json"
    missing_file = _cli("check_consistency.py", tex, "--governance", "--custom-terms", str(absent))
    assert missing_file.returncode != 0
    assert "custom terms file not found" in missing_file.stderr
    assert not any(marker in missing_file.stdout for marker in PASS_MARKERS)

    broken = _write(tmp_path, "broken.json", '{"banned":')
    invalid = _cli("check_consistency.py", tex, "--governance", "--custom-terms", str(broken))
    assert invalid.returncode != 0
    assert "invalid JSON" in invalid.stderr
    assert not any(marker in invalid.stdout for marker in PASS_MARKERS)

    raw_bytes = tmp_path / "raw.json"
    raw_bytes.write_bytes(b'\xff\xfe{"banned": }')
    decoded = _cli("check_consistency.py", tex, "--governance", "--custom-terms", str(raw_bytes))
    assert decoded.returncode != 0
    assert "[ERROR]" in decoded.stderr
    assert "not valid UTF-8" in decoded.stderr
    assert "Traceback" not in decoded.stderr
    assert not any(marker in decoded.stdout for marker in PASS_MARKERS)

    bad_field = _write(
        tmp_path,
        "bad.json",
        json.dumps({"zh": [], "en": [], "locked": ["不是对象"], "schema": 1}, ensure_ascii=False),
    )
    rejected = _cli("check_consistency.py", tex, "--governance", "--custom-terms", str(bad_field))
    assert rejected.returncode != 0
    assert "[ERROR]" in rejected.stderr
    assert not any(marker in rejected.stdout for marker in PASS_MARKERS)


def test_banned_hit_lists_every_candidate_once_and_locked_reports_canonical(tmp_path: Path) -> None:
    config = {
        "zh": [["合成甲", "合成乙"]],
        "en": [],
        "banned": {
            "旧称": {
                "candidates": [
                    {"text": "候选甲", "slot": "过程"},
                    {"text": "候选乙", "slot": "对象"},
                ]
            }
        },
        "locked": {"标准名": ["旧别名"]},
    }
    checker = _checker(
        tmp_path,
        "\\begin{document}\n标准名标准名。前旧称后，再写旧别名。\n\\end{document}\n",
        config,
    )
    result = checker.check_governance()
    banned = _kinds(result, "banned")
    locked = _kinds(result, "locked")
    assert len(banned) == 1
    assert banned[0]["term"] == "旧称"
    assert banned[0]["candidates"] == [
        {"text": "候选甲", "slot": "过程"},
        {"text": "候选乙", "slot": "对象"},
    ]
    assert len(locked) == 1
    assert locked[0]["canonical"] == "标准名"
    assert locked[0]["term"] == "旧别名"
    for finding in banned + locked:
        assert finding["severity"] == "Info"
        assert finding["priority"] == "P3"
        assert finding["source"] == "[Script]"
        assert finding["meaning_check"] == "NEEDS-LLM"
        assert "前旧称后" not in json.dumps(finding, ensure_ascii=False)
    assert ["合成甲", "合成乙"] in checker.term_groups_zh


def test_governance_keeps_synonym_groups_and_ignores_them_when_disabled(tmp_path: Path) -> None:
    config = {
        "zh": [["自编码器", "自动编码器"]],
        "en": [],
        "banned": {"旧称": {"candidates": [{"text": "候选甲"}]}},
    }
    tex = "自编码器与自动编码器。旧称出现。"
    enabled = _checker(tmp_path, tex, config)
    assert enabled.check_terms()["inconsistencies"][0]["group"] == ["自编码器", "自动编码器"]
    assert _kinds(enabled.check_governance(), "banned")[0]["candidates"][0]["slot"] is None
    disabled = consistency.ConsistencyChecker(
        [str(tmp_path / "main.tex")],
        custom_terms_file=str(tmp_path / "terms.json"),
    )
    assert disabled.governance is None
    assert "候选甲" not in disabled.generate_report(
        disabled.check_terms(), disabled.check_abbreviations()
    )


def test_empty_governance_has_no_new_candidates_and_macros_block_a_clean_pass(
    tmp_path: Path,
) -> None:
    empty = _checker(
        tmp_path, "\\begin{document}\n普通句子。\n\\end{document}\n", {"zh": [], "en": []}
    )
    result = empty.check_governance()
    assert result["findings"] == []
    assert result["coverage_notes"] == []
    assert result["status"] == "PASS"

    macro = _checker(
        tmp_path / "macro",
        "\\newcommand{\\foo}{占位}\n\\begin{document}\n普通句子。\n\\end{document}\n",
        {"banned": {}},
    )
    covered = macro.check_governance()
    assert covered["findings"] == []
    assert covered["status"] == "INCOMPLETE"
    assert any("不能据此认为没有问题" in note for note in covered["coverage_notes"])
    report = macro.generate_report(macro.check_terms(), macro.check_abbreviations(), covered, None)
    section = report.split("[3] Term Governance", 1)[1]
    assert "不能据此认为没有问题" in section
    assert "no governance candidates" not in section
    assert "✅" not in section


def test_fixed_protection_and_user_environments_skip_governance_hits(tmp_path: Path) -> None:
    config = {
        "banned": {"旧称": {"candidates": [{"text": "候选甲", "slot": "对象"}]}},
        "exempt": {"environments": ["localterms"]},
    }
    checker = _checker(
        tmp_path,
        "\n".join(
            [
                "\\newcommand{\\hidden}{旧称}",
                "\\begin{document}",
                "注释外旧称。",
                "% 旧称",
                "$旧称$ \\(旧称\\)",
                "\\begin{equation}旧称\\end{equation}",
                "\\cite{旧称} \\cite[见旧称]{key}",
                "\\label{sec:旧称} \\ref{sec:旧称}",
                "\\includegraphics{旧称.png}",
                "\\begin{verbatim}旧称\\end{verbatim}",
                "\\begin{thebibliography}{1}\\bibitem{a} 旧称\\end{thebibliography}",
                "\\begin{abbreviations}旧称\\end{abbreviations}",
                "\\begin{localterms}旧称\\end{localterms}",
                "\\begin{table}表中旧称。\\end{table}",
                "\\section{缩略词表}",
                "节内旧称。",
                "\\section{缩略词对照表}",
                "对照表旧称。",
                "\\section{正文}",
                "正文旧称。",
                "\\end{document}",
            ]
        ),
        config,
    )
    banned = _kinds(checker.check_governance(), "banned")
    assert [finding["term"] for finding in banned].count("旧称") == 3
    report = json.dumps(banned, ensure_ascii=False)
    assert "候选甲" in report
    assert "slot" in report


def test_ordinary_longer_title_and_ascii_boundaries(tmp_path: Path) -> None:
    config = {
        "banned": {
            "旧称": {"candidates": [{"text": "候选甲"}]},
            "QV": {"candidates": [{"text": "候选丙"}]},
        }
    }
    checker = _checker(
        tmp_path,
        "\n".join(
            [
                "\\begin{document}",
                "\\section{附录缩略词表}",
                "旧称仍检查。",
                "xQV QV2 QV_layer 与QV相邻。",
                "\\end{document}",
            ]
        ),
        config,
    )
    result = checker.check_governance()
    assert len(_kinds(result, "banned")) == 2
    qv = _kinds(result, "banned")
    assert sum(1 for finding in qv if finding["term"] == "QV") == 1


def test_abbreviation_style_positive_and_negative_cases(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "\\begin{document}",
            "：合成指标（synthetic index，ZX）。",
            "合成指标（ZX）再次括注。",
            "合成指标 ZX 并列。",
            "：样例名称（Synthetic Index, AbX）。",
            "：另一名称（example unit，X-2）。另一名称 X-2 收尾。",
            "合成装置（ZX）没有合格首现。",
            "ZX 为合成指标。",
            "已登记后的数学括注合成指标（$Y$）。",
            "Kalman 滤波（Kalman filter，KF）。",
            "\\section{缩略词表}",
            "合成指标（ZX）",
            "\\section{正文}",
            "\\end{document}",
        ]
    )
    checker = _checker(tmp_path, text, None)
    result = checker.check_abbreviation_style()
    kinds = {
        (finding["kind"], finding["term"], finding["abbreviation"])
        for finding in result["findings"]
    }
    assert ("second_parenthetical", "合成指标", "ZX") in kinds
    assert ("juxtaposition", "合成指标", "ZX") in kinds
    assert ("title_case", "样例名称", "AbX") in kinds
    assert ("juxtaposition", "另一名称", "X-2") in kinds
    assert ("second_parenthetical", "合成装置", "ZX") not in kinds
    assert not any(
        finding["kind"] != "title_case" and finding["abbreviation"] == "KF"
        for finding in result["findings"]
    )
    assert not any(finding["abbreviation"] == "Y" for finding in result["findings"])
    title = next(finding for finding in result["findings"] if finding["kind"] == "title_case")
    assert title["field"] == "Synthetic Index"
    assert "synthetic index" not in title["detail"]
    assert result["project_form"] == "（英文全称，缩写）"
    assert title["meaning_check"] == "NEEDS-LLM"
    assert all(
        finding["severity"] == "Info" and finding["priority"] == "P3"
        for finding in result["findings"]
    )


def test_unclear_boundary_is_one_note_and_not_a_false_xor(tmp_path: Path) -> None:
    checker = _checker(
        tmp_path,
        "\\begin{document}\n采用合成指标（synthetic index，ZX）。\n合成指标（ZX）不应视为二次。\n\\end{document}\n",
        None,
    )
    result = checker.check_abbreviation_style()
    assert result["findings"] == []
    assert result["coverage_notes"].count(consistency._UNCLEAR_NAME_NOTE) == 1
    assert result["status"] != "PASS"


def test_abbreviation_order_follows_the_entry_assembly(tmp_path: Path) -> None:
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    _write(chapters, "a.tex", "：合成指标（synthetic index，ZX）。\n")
    _write(chapters, "b.tex", "合成指标（ZX）在后章。\n")
    forward = _write(
        tmp_path,
        "forward.tex",
        "\\begin{document}\n\\input{chapters/a}\n\\input{chapters/b}\n\\end{document}\n",
    )
    backward = _write(
        tmp_path,
        "backward.tex",
        "\\begin{document}\n\\input{chapters/b}\n\\input{chapters/a}\n\\end{document}\n",
    )
    forward_checker = consistency.ConsistencyChecker([str(forward)], entry_file=str(forward))
    backward_checker = consistency.ConsistencyChecker([str(backward)], entry_file=str(backward))
    forward_hits = _kinds(forward_checker.check_abbreviation_style(), "second_parenthetical")
    backward_hits = _kinds(backward_checker.check_abbreviation_style(), "second_parenthetical")
    assert len(forward_hits) == 1
    assert forward_hits[0]["file"] == "chapters/b.tex"
    assert backward_hits == []


def test_style_dedupes_same_position_without_replacing_the_old_recognizer(tmp_path: Path) -> None:
    duplicated = {
        "kind": "second_parenthetical",
        "term": "合成指标",
        "abbreviation": "ZX",
        "field": "",
        "file": "main.tex",
        "line": 2,
        "offset": 10,
    }
    assert len(consistency.dedupe_style_findings([duplicated, dict(duplicated)])) == 1
    kept = consistency.dedupe_style_findings(
        [duplicated, {**duplicated, "kind": "juxtaposition", "offset": 11}],
        [{"type": "undefined", "first_usage": ("main.tex", 4), "abbreviation": "BERT"}],
    )
    assert len(kept) == 2
    tex = _write(
        tmp_path,
        "main.tex",
        "\\begin{document}\n：合成指标（synthetic index，ZX）。\n合成指标（ZX）。\nBERT BERT。\n\\end{document}\n",
    )
    combined = _cli(
        "check_consistency.py", tex, "--abbreviations", "--abbreviation-style", "--json"
    )
    assert combined.returncode == 0
    payload = json.loads(combined.stdout[combined.stdout.index("{") :])
    assert "definitions" in payload and "issues" in payload and "abbreviation_style" in payload
    assert any(issue["abbreviation"] == "BERT" for issue in payload["issues"])
    assert any(
        item["kind"] == "second_parenthetical" for item in payload["abbreviation_style"]["findings"]
    )
    assert "governance" not in payload


def test_old_json_keys_stay_without_new_flags(tmp_path: Path) -> None:
    tex = _write(tmp_path, "main.tex", "普通句子。BERT BERT。\n")
    result = _cli("check_consistency.py", tex, "--json")
    payload = json.loads(result.stdout[result.stdout.index("{") :])
    assert set(payload) == {"terms", "abbreviations"}
    assert set(payload["terms"]) == {"term_occurrences", "inconsistencies", "status"}
    assert set(payload["abbreviations"]) == {"definitions", "usages", "issues", "status"}


def test_fixture_project_governance_and_abbreviation_style() -> None:
    result = _cli(
        "check_consistency.py",
        FIXTURE / "main.tex",
        "--governance",
        "--custom-terms",
        str(FIXTURE / "terms.json"),
        "--abbreviation-style",
        "--json",
    )
    assert result.returncode in {0, 1}
    assert "不应被扫描" not in result.stdout
    payload = json.loads(result.stdout[result.stdout.index("{") :])
    assert set(payload["terms"]) == {"term_occurrences", "inconsistencies", "status"}
    governance = payload["governance"]
    banned = _kinds(governance, "banned")
    assert [finding["line"] for finding in banned if finding["term"] == "旧称"] == [25, 30]
    assert banned[0]["candidates"] == [
        {"text": "候选甲", "slot": "过程"},
        {"text": "候选乙", "slot": "对象"},
    ]
    assert sum(finding["term"] == "QV" for finding in banned) == 1
    locked = _kinds(governance, "locked")
    assert len(locked) == 1
    assert locked[0]["canonical"] == "标准名"
    assert locked[0]["term"] == "旧别名"
    assert locked[0]["file"] == "chapters/body.tex"
    assert locked[0]["line"] == 30
    assert any("不能据此认为没有问题" in note for note in governance["coverage_notes"])
    style_result = payload["abbreviation_style"]
    observed = {
        (finding["kind"], finding["file"], finding["line"], finding["abbreviation"])
        for finding in style_result["findings"]
    }
    assert ("second_parenthetical", "chapters/later.tex", 1, "ZX") in observed
    assert ("juxtaposition", "chapters/later.tex", 2, "ZX") in observed
    assert ("title_case", "chapters/later.tex", 3, "AbX") in observed
    assert ("juxtaposition", "chapters/later.tex", 4, "X-2") in observed
    assert not any(
        finding["file"] == "chapters/body.tex" and finding["kind"] == "second_parenthetical"
        for finding in style_result["findings"]
    )
    assert any(note.startswith("NEEDS-LLM") for note in style_result["coverage_notes"])
    assert style_result["project_form"] == "（英文全称，缩写）"


def test_degree_cli_error_is_not_a_clean_pass(tmp_path: Path) -> None:
    missing = tmp_path / "missing.tex"
    result = _cli("check_style_zh.py", missing, "--degree-wording")
    assert result.returncode != 0
    assert "未发现规则级表达问题" not in result.stdout
    assert "[ERROR]" in result.stderr


def test_degree_cli_default_output_has_no_degree_code(tmp_path: Path) -> None:
    tex = _write(
        tmp_path,
        "main.tex",
        "\\documentclass{ctexbook}\n\\begin{document}\n极易发散。\n\\end{document}\n",
    )
    default = _cli("check_style_zh.py", tex)
    enabled = _cli("check_style_zh.py", tex, "--degree-wording")
    assert default.returncode == 0
    assert "E-DEGREE" not in default.stdout
    assert enabled.returncode == 0
    assert "E-DEGREE" in enabled.stdout
    assert "Meaning-Check: NEEDS-LLM" in enabled.stdout
    assert "[Severity: Info]" in enabled.stdout
    assert "[Priority: P3]" in enabled.stdout
    assert "[Script]" in enabled.stdout
    assert "% 建议:" not in enabled.stdout


def test_biblatex_and_cleveref_payloads_are_masked_from_new_scans(tmp_path: Path) -> None:
    config = {"zh": [], "en": [], "banned": {"旧称": {"candidates": [{"text": "候选甲"}]}}}
    payloads = (
        "\\parencite{旧称}\\textcite[见][12]{旧称}\\autocite{旧称}\\footcite{旧称}"
        "\\citet{旧称}\\citep[12]{旧称}\\nameref{旧称}\\cref{旧称}\\Cref{旧称}"
        "\\eqref{旧称}\\autoref{旧称}"
    )
    masked = _checker(tmp_path, "\\begin{document}\n" + payloads + "\n\\end{document}\n", config)
    assert _kinds(masked.check_governance(), "banned") == []
    visible = _checker(tmp_path, "\\begin{document}\n正文旧称。\n\\end{document}\n", config)
    assert len(_kinds(visible.check_governance(), "banned")) == 1
    style = _checker(
        tmp_path,
        "\\begin{document}\n：合成指标（synthetic index，ZX）。\\parencite{合成指标（ZX）}\n"
        "\\end{document}\n",
        None,
    )
    assert style.check_abbreviation_style()["findings"] == []
