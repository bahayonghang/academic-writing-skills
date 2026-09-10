"""Observable terminology/abbreviation contracts for the shipped ZH checker."""

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests.support.paths import SCRIPT_DIR_ZH


def _load_zh():
    saved_path = sys.path[:]
    saved_modules = sys.modules.copy()
    try:
        sys.modules.pop("tex_loader", None)
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        spec = importlib.util.spec_from_file_location(
            "zh_consistency_semantics", SCRIPT_DIR_ZH / "check_consistency.py"
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name in set(sys.modules) - set(saved_modules):
            del sys.modules[name]
        sys.modules.update(saved_modules)


consistency = _load_zh()


def _write(root: Path, name: str, content: str) -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _checker(tmp_path: Path, content: str):
    path = _write(tmp_path, "main.tex", content)
    return consistency.ConsistencyChecker([str(path)])


def _cli(path: Path, *args: str):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(SCRIPT_DIR_ZH / "check_consistency.py"), str(path), *args],
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
        timeout=30,
    )


def _json_output(result):
    # The existing CLI prints an INFO preamble before its JSON payload.
    return json.loads(result.stdout[result.stdout.index("{") :])


def test_loads_shipped_zh_and_restores_import_state():
    before_path, before_modules = sys.path[:], sys.modules.copy()
    module = _load_zh()
    assert module.__file__ is not None
    assert Path(module.__file__).resolve() == (SCRIPT_DIR_ZH / "check_consistency.py").resolve()
    assert sys.path == before_path
    assert sys.modules == before_modules


@pytest.mark.parametrize(
    "body",
    [
        "深度学习是一类方法。深度神经网络是一类模型。",
        "机器学习与机器智能的研究范围不同。",
        "循环神经网络与递归神经网络处理不同的结构。",
        "deep learning uses a deep neural network.",
    ],
)
def test_distinct_concepts_are_not_variant_mix(tmp_path: Path, body: str):
    result = _checker(tmp_path, body).check_terms()
    assert result["status"] == "PASS", result


def test_builtin_candidates_do_not_choose_a_name_by_frequency(tmp_path: Path):
    result = _checker(tmp_path, "深度学习。深层学习。深层学习。").check_terms()
    assert result["inconsistencies"][0]["type"] == "variant_mix"
    suggestion = result["inconsistencies"][0]["suggestion"]
    assert "NEEDS-LLM" in suggestion
    assert "统一使用 '" not in suggestion


@pytest.mark.parametrize(
    "body,line",
    [
        ("CNN 用于分类。卷积神经网络（CNN）用于建模。", 1),
        ("\\chapter{绪论}\nCNN 用于分类。\n卷积神经网络（CNN）用于建模。", 2),
    ],
)
def test_first_use_before_definition_is_located(tmp_path: Path, body: str, line: int):
    result = _checker(tmp_path, body).check_abbreviations()
    assert result["status"] == "WARNING"
    issue = next(i for i in result["issues"] if i["type"] == "undefined")
    assert Path(issue["first_usage"][0]) == tmp_path / "main.tex"
    assert issue["first_usage"][1] == line
    assert "before" in issue["message"]


def test_chinese_adjacent_use_is_detected_without_matching_ascii_identifiers(tmp_path: Path):
    result = _checker(
        tmp_path,
        "someCNN CNN2 CNN_layer xCNN xCNN CNN2 CNN_layer。\n"
        "使用CNN进行分析。卷积神经网络（CNN）用于分类。",
    ).check_abbreviations()
    assert result["usages"] == {"CNN": 1}
    assert result["issues"][0]["first_usage"] == (str(tmp_path / "main.tex"), 2)


@pytest.mark.parametrize("chapter", ["", "\\chapter{方法}\n"])
def test_identical_reintroduction_is_legal(tmp_path: Path, chapter: str):
    result = _checker(
        tmp_path,
        "\\chapter{绪论}\n卷积神经网络（CNN）用于建模。\n"
        f"{chapter}卷积神经网络（CNN）用于预测。\nCNN 用于分类。",
    ).check_abbreviations()
    assert result["definitions"] == {"CNN": 2}
    assert result["usages"] == {"CNN": 1}
    assert result["issues"] == []


def test_different_definition_fragments_are_located_candidates(tmp_path: Path):
    result = _checker(
        tmp_path,
        "\\chapter{绪论}\n卷积神经网络（CNN）。\n"
        "\\chapter{方法}\nConvolutional neural network (CNN).\n",
    ).check_abbreviations()
    issue = next(i for i in result["issues"] if i["type"] == "multiple_definitions")
    assert issue["definitions"] == [
        ("卷积神经网络", str(tmp_path / "main.tex"), 2),
        ("Convolutional neural network", str(tmp_path / "main.tex"), 4),
    ]
    assert "NEEDS-LLM" in issue["message"]
    assert "main.tex:2" in issue["message"] and "main.tex:4" in issue["message"]


@pytest.mark.parametrize("prefix", ["术语在上一行\n", "\\chapter{标题}", "前一句。", "名称" * 100])
def test_unreliable_name_boundary_requests_review(tmp_path: Path, prefix: str):
    result = _checker(tmp_path, prefix + "（CNN）\nCNN 用于分类。").check_abbreviations()
    assert any("NEEDS-LLM" in i["message"] for i in result["issues"])


def test_definition_prefix_does_not_cross_sentence_or_command(tmp_path: Path):
    result = _checker(
        tmp_path,
        "\\chapter{背景}前一句。卷积神经网络（CNN）。\n"
        "\\section{方法}另一句。脉冲神经网络（CNN）。",
    ).check_abbreviations()
    assert result["issues"][0]["definitions"] == [
        ("卷积神经网络", str(tmp_path / "main.tex"), 1),
        ("脉冲神经网络", str(tmp_path / "main.tex"), 2),
    ]


def test_noise_thresholds_and_normal_expansion(tmp_path: Path):
    result = _checker(
        tmp_path,
        "% CNN CNN\n\\cite{CNN,CNN}\n\\label{CNN}\n"
        "\\ref{CNN}\\input{CNN}\nGPU CPU IEEE API XYZC。\n"
        "卷积神经网络（CNN）用于建模。CNN 用于分类。\nBERT 用于编码。BERT 用于训练。",
    ).check_abbreviations()
    assert result["definitions"] == {"CNN": 1}
    assert result["usages"] == {"XYZC": 1, "CNN": 1, "BERT": 2}
    assert [(i["type"], i["abbreviation"]) for i in result["issues"]] == [("undefined", "BERT")]


def test_multiline_citation_mask_preserves_source_line(tmp_path: Path):
    result = _checker(tmp_path, "\\cite{CNN,\nCNN}\nBERT BERT").check_abbreviations()
    assert result["issues"][0]["first_usage"] == (str(tmp_path / "main.tex"), 3)


def test_full_name_after_definition_is_only_optional_style(tmp_path: Path):
    result = _checker(
        tmp_path,
        "卷积神经网络（CNN）用于建模。\n" + "卷积神经网络用于预测。\n" * 3,
    ).check_terms()
    for issue in result["inconsistencies"]:
        assert issue["type"] == "full_after_abbrev"
        assert "可选" in issue["suggestion"]
        assert "后文统一用缩写" not in issue["suggestion"]


@pytest.mark.parametrize(
    "main_body,expected_line",
    [
        ("CNN 用于预测。\\input{chapters/definition}\nCNN 用于分类。", 1),
        ("\\input{chapters/definition}CNN 用于预测。", None),
    ],
)
def test_entry_uses_include_expansion_order(tmp_path: Path, main_body: str, expected_line):
    main = _write(tmp_path, "main.tex", main_body)
    _write(tmp_path, "chapters/definition.tex", "卷积神经网络（CNN）用于建模。")
    _write(tmp_path, "draft.tex", "BERT BERT")
    result = _cli(main, "--abbreviations", "--json")
    assert result.returncode == 0
    payload = _json_output(result)
    assert "BERT" not in payload["usages"]
    if expected_line:
        assert payload["issues"][0]["first_usage"] == ["main.tex", expected_line]
    else:
        assert payload["issues"] == []


def test_entry_api_reuses_definition_in_later_chapter_and_assembles_once(
    tmp_path: Path, monkeypatch
):
    main = _write(tmp_path, "main.tex", "\\input{one/chapter}\n\\input{two/chapter}")
    _write(tmp_path, "one/chapter.tex", "\\chapter{绪论}\n卷积神经网络（CNN）。")
    _write(tmp_path, "two/chapter.tex", "\\chapter{方法}\nCNN 用于分类。")
    original = consistency.assemble
    calls = []

    def assemble(path):
        calls.append(path)
        return original(path)

    monkeypatch.setattr(consistency, "assemble", assemble)
    checker = consistency.ConsistencyChecker([str(main)], entry_file=str(main))
    assert checker.check_terms()["status"] == "PASS"
    assert checker.check_abbreviations()["issues"] == []
    assert len(calls) == 1


def test_same_basename_files_have_distinct_source_coordinates(tmp_path: Path):
    main = _write(tmp_path, "main.tex", "\\input{one/chapter}\n\\input{two/chapter}")
    _write(tmp_path, "one/chapter.tex", "\\chapter{绪论}\nCNN 用于分类。")
    _write(tmp_path, "two/chapter.tex", "\\chapter{方法}\n卷积神经网络（CNN）。\n另一释义（CNN）。")
    payload = _json_output(_cli(main, "--abbreviations", "--json"))
    assert payload["issues"][0]["first_usage"] == ["one/chapter.tex", 2]
    assert payload["issues"][1]["definitions"] == [
        ["卷积神经网络", "two/chapter.tex", 2],
        ["另一释义", "two/chapter.tex", 3],
    ]


@pytest.mark.parametrize("all_files", [False, True])
def test_unordered_cli_input_declares_file_only_coverage(tmp_path: Path, all_files: bool):
    main = _write(tmp_path, "main.tex", "\\input{a}\n\\input{b}")
    _write(tmp_path, "a.tex", "卷积神经网络（CNN）。")
    _write(tmp_path, "b.tex", "CNN 用于分类。CNN 用于预测。")
    result = _cli(
        main if all_files else tmp_path, "--json", *(["--all-files"] if all_files else [])
    )
    assert "跨文件顺序未验证" in result.stdout + result.stderr
    issue = _json_output(result)["abbreviations"]["issues"][0]
    assert issue["type"] == "undefined"
    assert Path(issue["first_usage"][0]) == tmp_path / "b.tex"


def test_unordered_api_does_not_infer_reading_order(tmp_path: Path, capsys):
    one = _write(tmp_path, "one/chapter.tex", "卷积神经网络（CNN）。")
    two = _write(tmp_path, "two/chapter.tex", "CNN 用于分类。CNN 用于预测。")
    checker = consistency.ConsistencyChecker([str(one), str(two)])
    result = checker.check_abbreviations()
    assert result["issues"][0]["first_usage"] == (str(two), 1)
    report = checker.generate_report(checker.check_terms(), result)
    assert "跨文件顺序未验证" in report + capsys.readouterr().err


def test_missing_include_warning_is_visible(tmp_path: Path):
    main = _write(tmp_path, "main.tex", "\\input{missing}\n普通正文。")
    result = _cli(main, "--json")
    assert "missing" in result.stderr and "WARN" in result.stderr


def test_read_failure_does_not_cache_partial_scope_as_pass(tmp_path: Path, capsys):
    readable = _write(tmp_path, "readable.tex", "普通正文。")
    missing = tmp_path / "missing.tex"
    checker = consistency.ConsistencyChecker([str(readable), str(missing)])
    for _ in range(2):
        with pytest.raises(OSError):
            checker.check_abbreviations()
    assert "Cannot read" in capsys.readouterr().err


@pytest.mark.parametrize("args,exit_code", [((), 1), (("--terms",), 0), (("--abbreviations",), 0)])
def test_cli_preserves_modes_custom_terms_and_exit_protocol(tmp_path: Path, args, exit_code):
    main = _write(tmp_path, "main.tex", "自编码器与自动编码器。BERT BERT。")
    terms = _write(tmp_path, "terms.json", '{"zh": [["自编码器", "自动编码器"]], "en": []}')
    before = main.read_bytes(), terms.read_bytes()
    result = _cli(main, *args, "--custom-terms", str(terms), "--json")
    assert result.returncode == exit_code
    payload = _json_output(result)
    if not args or args == ("--terms",):
        data = payload if args else payload["terms"]
        assert data["inconsistencies"][0]["counts"] == {"自编码器": 1, "自动编码器": 1}
        assert "NEEDS-LLM" in data["inconsistencies"][0]["suggestion"]
    if not args or args == ("--abbreviations",):
        data = payload if args else payload["abbreviations"]
        assert data["issues"][0]["abbreviation"] == "BERT"
    assert before == (main.read_bytes(), terms.read_bytes())
