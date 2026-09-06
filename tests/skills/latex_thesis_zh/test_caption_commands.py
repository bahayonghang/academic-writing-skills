"""Regression tests for caption and bicaption command recognition."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

from tests.support.paths import SCRIPT_DIR_ZH

_SHARED_MODULES = ("parsers", "tex_loader")


def _load_zh(name: str) -> ModuleType:
    """Load one ZH script by path and restore import state symmetrically."""
    saved_path = list(sys.path)
    saved_shared = {module: sys.modules.pop(module, None) for module in _SHARED_MODULES}
    module_name = f"zh_caption_{name}"
    saved_target = sys.modules.pop(module_name, None)
    try:
        spec = importlib.util.spec_from_file_location(module_name, SCRIPT_DIR_ZH / f"{name}.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(SCRIPT_DIR_ZH))
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        sys.modules.pop(module_name, None)
        if saved_target is not None:
            sys.modules[module_name] = saved_target
        for module_name_shared, saved in saved_shared.items():
            if saved is None:
                sys.modules.pop(module_name_shared, None)
            else:
                sys.modules[module_name_shared] = saved


check_references = _load_zh("check_references")
check_tables = _load_zh("check_tables")


def _missing_caption_issues(content: str) -> list[dict]:
    checker = check_references.ReferenceChecker(content, "chapter.tex")
    return [issue for issue in checker.run_all() if issue["message"].startswith("Missing caption")]


def _write_table(tmp_path: Path, caption_command: str) -> Path:
    tex = tmp_path / "table.tex"
    tex.write_text(
        "\\usepackage{booktabs}\n"
        "\\begin{table}\n"
        f"{caption_command}\n"
        "\\label{tab:sample}\n"
        "\\begin{tabular}{lc}\n"
        "\\toprule\n对象 & 数值 \\\\\n"
        "\\midrule\nA & 1 \\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\end{table}\n",
        encoding="utf-8",
    )
    return tex


@pytest.mark.parametrize(
    "caption_command",
    [
        "\\caption{普通题注}",
        "\\caption [目录短题] \n {普通长题注}",
        "\\bicaption{中文题注}{English Caption}",
        "\\bicaption [中文短题] \n {中文长题注} \n [English Short] {English Long Caption}",
    ],
)
def test_references_accepts_supported_caption_commands(caption_command: str) -> None:
    content = f"\\begin{{figure}}\n{caption_command}\n\\label{{fig:sample}}\n\\end{{figure}}\n"
    assert _missing_caption_issues(content) == []


@pytest.mark.parametrize(
    "caption_command",
    [
        "\\caption{普通表题}",
        "\\caption [目录短题] \n {普通长表题}",
        "\\bicaption{中文表题}{English Table Caption}",
        "\\bicaption [中文短题] \n {中文长表题} \n [English Short] {English Long Table Caption}",
    ],
)
def test_tables_accepts_supported_caption_commands(tmp_path: Path, caption_command: str) -> None:
    result = check_tables.TableChecker(str(_write_table(tmp_path, caption_command))).check()
    assert not [issue for issue in result["issues"] if issue["category"] == "caption"]
    assert not [issue for issue in result["issues"] if issue["category"] == "caption_position"]


def test_references_rejects_comment_and_similar_command_as_caption() -> None:
    content = (
        "\\begin{figure}\n"
        "% \\caption{注释中的伪题注}\n"
        "\\fakecaption{相似命令}\n"
        "\\label{fig:missing}\n"
        "\\end{figure}\n"
    )
    issues = _missing_caption_issues(content)
    assert len(issues) == 1
    assert issues[0]["line"] == 4


def test_tables_rejects_comment_and_captionsetup_as_caption(tmp_path: Path) -> None:
    tex = _write_table(
        tmp_path,
        "% \\caption{注释中的伪题注}\n\\captionsetup{font=small}\n\\fakecaption{相似命令}",
    )
    result = check_tables.TableChecker(str(tex)).check()
    caption_issues = [issue for issue in result["issues"] if issue["category"] == "caption"]
    assert len(caption_issues) == 1


def test_bicaption_below_tabular_still_reports_position(tmp_path: Path) -> None:
    tex = tmp_path / "below.tex"
    tex.write_text(
        "\\usepackage{booktabs}\n"
        "\\begin{table}\n"
        "\\begin{tabular}{lc}\n"
        "\\toprule\n对象 & 数值 \\\\\n"
        "\\midrule\nA & 1 \\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\bicaption{中文表题}{English Table Caption}\n"
        "\\label{tab:below}\n"
        "\\end{table}\n",
        encoding="utf-8",
    )
    result = check_tables.TableChecker(str(tex)).check()
    assert not [issue for issue in result["issues"] if issue["category"] == "caption"]
    position = [issue for issue in result["issues"] if issue["category"] == "caption_position"]
    assert len(position) == 1
    assert position[0]["line"] == 2


def test_multifile_caption_results_keep_source_locations(tmp_path: Path) -> None:
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    main = tmp_path / "main.tex"
    main.write_text("\\input{chapters/captions}\n", encoding="utf-8")
    (chapters / "captions.tex").write_text(
        "\\usepackage{booktabs}\n"
        "\\begin{figure}\n"
        "\\bicaption{有效中文图题}{Valid English Figure Caption}\n"
        "\\label{fig:valid}\n"
        "\\end{figure}\n"
        "\\begin{figure}\n"
        "% \\caption{注释伪题注}\n"
        "\\label{fig:missing}\n"
        "\\end{figure}\n"
        "\\begin{table}\n"
        "\\begin{tabular}{lc}\n"
        "\\toprule\n对象 & 数值 \\\\\n"
        "\\midrule\nA & 1 \\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\bicaption{下方中文表题}{English Caption Below}\n"
        "\\label{tab:below}\n"
        "\\end{table}\n",
        encoding="utf-8",
    )

    reference_result = check_references.ThesisReferenceChecker(str(main)).run_all()
    missing = [
        issue for issue in reference_result if issue["message"].startswith("Missing caption")
    ]
    assert len(missing) == 1
    assert missing[0]["file"] == "chapters/captions.tex"
    assert missing[0]["line"] == 8

    table_result = check_tables.TableChecker(str(main)).check()
    position = [
        issue for issue in table_result["issues"] if issue["category"] == "caption_position"
    ]
    assert len(position) == 1
    assert position[0]["file"] == "chapters/captions.tex"
    assert position[0]["line"] == 10


def test_loaders_target_zh_script_copies() -> None:
    references_file = check_references.__file__
    tables_file = check_tables.__file__
    assert references_file is not None
    assert tables_file is not None
    assert Path(references_file).resolve().parent == SCRIPT_DIR_ZH.resolve()
    assert Path(tables_file).resolve().parent == SCRIPT_DIR_ZH.resolve()
    assert hasattr(check_references, "ReferenceChecker")
    assert hasattr(check_tables, "TableChecker")
