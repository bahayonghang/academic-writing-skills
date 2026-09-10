"""Exercise the shipped ZH compiler with real paths and mocked external tools."""

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from tests.support.paths import SCRIPT_DIR_ZH


def _load_compile():
    saved_path = list(sys.path)
    saved = {name: sys.modules.pop(name, None) for name in ("parsers", "tex_loader")}
    try:
        spec = importlib.util.spec_from_file_location(
            "zh_compile_outdir", SCRIPT_DIR_ZH / "compile.py"
        )
        assert spec and spec.loader
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


compile_zh = _load_compile()
ROUTES = [({}, []), ({"recipe": "latexmk"}, ["--recipe", "latexmk"])] + [
    ({"compiler": engine}, ["--compiler", engine]) for engine in ("xelatex", "lualatex")
]
ROUTE_IDS = ["default", "recipe-latexmk", "compiler-xelatex", "compiler-lualatex"]
MANUAL_RECIPES = [
    "xelatex",
    "lualatex",
    "xelatex-bibtex",
    "xelatex-biber",
    "lualatex-bibtex",
    "lualatex-biber",
]


def test_loads_zh_compiler():
    module_file = compile_zh.__file__
    assert module_file is not None
    assert Path(module_file).resolve() == (SCRIPT_DIR_ZH / "compile.py").resolve()
    assert compile_zh.LaTeXCompiler.DEFAULT_RECIPE == "latexmk"
    assert "xelatex-biber" in compile_zh.LaTeXCompiler.RECIPES


@pytest.fixture
def tex_file(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    tex = source / "main.tex"
    tex.write_text(
        "% !TEX program = xelatex\n"
        "\\documentclass{article}\n\\begin{document}Synthetic test.\\end{document}\n",
        encoding="utf-8",
    )
    return tex


@pytest.mark.parametrize(("options", "cli_args"), ROUTES, ids=ROUTE_IDS)
@pytest.mark.parametrize("path_kind", ["none", "relative", "absolute", "unicode-space"])
@pytest.mark.parametrize("outcome", ["target", "missing", "nonzero-target", "source-only"])
def test_compile_output_contract(
    tex_file, tmp_path, monkeypatch, capsys, options, cli_args, path_kind, outcome
):
    outdir = {
        "none": None,
        "relative": "build",
        "absolute": str(tmp_path / "external" / "build"),
        "unicode-space": "构建 目录",
    }[path_kind]
    output_dir = tex_file.parent if outdir is None else (tex_file.parent / outdir).resolve()
    target_pdf = output_dir / "main.pdf"
    source_pdf = tex_file.with_suffix(".pdf")
    if outcome in ("target", "nonzero-target"):
        output_dir.mkdir(parents=True, exist_ok=True)
        target_pdf.write_bytes(b"%PDF-1.4\nrequested output\n")
    if outcome == "source-only":
        source_pdf.write_bytes(b"%PDF-1.4\nold source output\n")

    calls = []

    def fake_run(cmd, *, cwd, capture_output):
        calls.append(cmd)
        assert cwd == tex_file.parent
        assert capture_output is False
        return SimpleNamespace(returncode=7 if outcome == "nonzero-target" else 0)

    monkeypatch.setattr(compile_zh.shutil, "which", lambda _: "/fake/tool")
    monkeypatch.setattr(compile_zh.subprocess, "run", fake_run)
    # Run from elsewhere: relative --outdir belongs to the source directory, not the caller.
    monkeypatch.chdir(tmp_path)
    compiler = compile_zh.LaTeXCompiler(str(tex_file), **options)
    code = compiler.compile(outdir=outdir)
    output = capsys.readouterr().out

    assert len(calls) == 1
    assert calls[0][0] == "latexmk"
    assert calls[0][-1] == str(tex_file)
    output_args = [arg for arg in calls[0] if arg.startswith("-outdir=")]
    assert output_args == ([] if outdir is None else [f"-outdir={output_dir}"])
    expected = 7 if outcome == "nonzero-target" else (0 if target_pdf.exists() else 1)
    assert code == expected
    if expected == 0:
        assert f"[SUCCESS] PDF generated: {target_pdf}" in output
    else:
        assert "[SUCCESS]" not in output
        assert "[ERROR]" in output
        if expected == 1:
            assert f"PDF not found: {target_pdf}" in output


@pytest.mark.parametrize(("options", "cli_args"), ROUTES, ids=ROUTE_IDS)
@pytest.mark.parametrize("create_target", [True, False])
def test_cli_passes_outdir_and_returns_wrapper_result(
    tex_file, monkeypatch, capsys, options, cli_args, create_target
):
    target_pdf = tex_file.parent / "build" / "main.pdf"

    def fake_run(cmd, *, cwd, capture_output):
        assert cwd == tex_file.parent
        assert f"-outdir={target_pdf.parent}" in cmd
        if create_target:
            target_pdf.parent.mkdir()
            target_pdf.write_bytes(b"%PDF-1.4\nnew output\n")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(compile_zh.shutil, "which", lambda _: "/fake/tool")
    monkeypatch.setattr(compile_zh.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["compile.py", str(tex_file), *cli_args, "--outdir", "build"])
    with pytest.raises(SystemExit) as exit_info:
        compile_zh.main()
    assert exit_info.value.code == (0 if create_target else 1)
    assert str(target_pdf) in capsys.readouterr().out


@pytest.mark.parametrize("recipe", MANUAL_RECIPES)
@pytest.mark.parametrize("tools_available", [True, False])
def test_manual_outdir_rejected_before_subprocess(
    tex_file, monkeypatch, capsys, recipe, tools_available
):
    calls = []
    monkeypatch.setattr(
        compile_zh.shutil, "which", lambda _: "/fake/tool" if tools_available else None
    )
    monkeypatch.setattr(
        compile_zh.subprocess,
        "run",
        lambda *args, **kwargs: calls.append(args) or SimpleNamespace(returncode=0),
    )
    tex_file.with_suffix(".pdf").write_bytes(b"%PDF-1.4\nold source output\n")
    monkeypatch.setattr(
        sys, "argv", ["compile.py", str(tex_file), "--recipe", recipe, "--outdir", "build"]
    )
    with pytest.raises(SystemExit) as exit_info:
        compile_zh.main()
    assert exit_info.value.code == 1
    assert calls == []
    output = capsys.readouterr().out
    assert "[ERROR]" in output
    assert "--outdir" in output
    assert "--recipe latexmk" in output
    assert "--compiler" in output
    assert "[SUCCESS]" not in output


@pytest.mark.parametrize("options", [ROUTES[1][0], ROUTES[2][0]])
@pytest.mark.parametrize("shell_escape", [False, True])
def test_outdir_preserves_engine_shell_mode(tex_file, monkeypatch, capsys, options, shell_escape):
    target = tex_file.parent / "build" / "main.pdf"
    target.parent.mkdir()
    target.write_bytes(b"%PDF-1.4\n")
    calls = []
    monkeypatch.setattr(compile_zh.shutil, "which", lambda _: "/fake/tool")
    monkeypatch.setattr(
        compile_zh.subprocess,
        "run",
        lambda cmd, **kwargs: calls.append(cmd) or SimpleNamespace(returncode=0),
    )
    compiler = compile_zh.LaTeXCompiler(str(tex_file), shell_escape=shell_escape, **options)
    assert compiler.compile(outdir="build") == 0
    mode = "-shell-escape" if shell_escape else "-no-shell-escape"
    assert f"-xelatex=xelatex {mode} %O %S" in calls[0]
    assert ("Only use with trusted sources" in capsys.readouterr().out) is shell_escape
