"""Exercise each installed loader copy with synthetic include graphs."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from tests.support.paths import SKILLS_ROOT

SKILLS = ("latex-thesis-zh", "latex-defense-zh", "latex-paper-en", "paper-audit", "cover-letter")


@pytest.fixture(params=SKILLS)
def loader(request):
    path = SKILLS_ROOT / request.param / "scripts" / "tex_loader.py"
    saved_path = list(sys.path)
    saved_modules = dict(sys.modules)
    try:
        spec = importlib.util.spec_from_file_location("security_tex_loader", path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        assert module.__file__ is not None
        assert Path(module.__file__) == path
        yield module
    finally:
        sys.path[:] = saved_path
        for name in set(sys.modules) - set(saved_modules):
            sys.modules.pop(name, None)
        sys.modules.update(saved_modules)


@pytest.mark.parametrize("api", ["assemble", "iter_files"])
@pytest.mark.parametrize("command", ["input", "include", "subfile"])
@pytest.mark.parametrize("kind", ["parent", "absolute", "symlink", "prefix"])
def test_external_include_is_rejected_before_read(
    loader, tmp_path, monkeypatch, api, command, kind
):
    root = tmp_path / "project"
    root.mkdir()
    outside = tmp_path / "project-other" / "outside.tex"
    outside.parent.mkdir()
    outside.write_text("Synthetic external marker", encoding="utf-8")
    raw = "../project-other/outside"
    if kind == "absolute":
        raw = outside.as_posix()
    elif kind == "symlink":
        link = root / "linked.tex"
        try:
            link.symlink_to(outside)
        except OSError as exc:
            pytest.skip(f"symlink creation unavailable: {exc}")
        raw = "linked"
    elif kind == "parent":
        outside = tmp_path / "outside.tex"
        outside.write_text("Synthetic external marker", encoding="utf-8")
        raw = "../outside"
    main = root / "main.tex"
    main.write_text(f"% synthetic fixture\n\\{command}{{{raw}}}\n", encoding="utf-8")
    external_reads = []
    external_probes = []
    original_read = loader.read_text_robust
    original_exists = Path.exists

    def read(path):
        if not path.is_relative_to(root):
            external_reads.append(path)
        return original_read(path)

    monkeypatch.setattr(loader, "read_text_robust", read)

    def exists(path):
        if not path.is_relative_to(root):
            external_probes.append(path)
        return original_exists(path)

    monkeypatch.setattr(Path, "exists", exists)
    caught = None
    try:
        getattr(loader, api)(main)
    except ValueError as exc:
        caught = exc
    assert external_reads == [], "external read occurred before rejection"
    assert external_probes == [], "external existence probe occurred before rejection"
    assert caught is not None, "include traversal returned success"
    assert isinstance(caught, loader.IncludeBoundaryError)
    assert getattr(caught, "code", None) == "E-INCLUDE-BOUNDARY"
    assert (getattr(caught, "source", None), getattr(caught, "line", None)) == ("main.tex", 2)
    assert getattr(caught, "raw", None) == raw
    assert "main.tex:2" in str(caught)
    assert str(tmp_path) not in str(caught)
    assert tmp_path.as_posix() not in str(caught)


@pytest.mark.parametrize("api", ["assemble", "iter_files"])
def test_nested_main_fixed_root_fallback_and_origins(loader, tmp_path, api):
    root = tmp_path / "project"
    nested = root / "nested"
    nested.mkdir(parents=True)
    chapter = root / "章节 空格.tex"
    chapter.write_text("chapter\n", encoding="utf-8")
    local = nested / "local.tex"
    local.write_text("local\n", encoding="utf-8")
    fallback = root / "fallback.tex"
    fallback.write_text("fallback\n", encoding="utf-8")
    main = nested / "main.tex"
    main.write_text(
        f"\\input{{../章节 空格}}\n\\include{{local}}\n\\subfile{{fallback}}\n"
        f"\\input{{{chapter.as_posix()}}}\n% \\input{{../../outside}}\n",
        encoding="utf-8",
    )
    result = getattr(loader, api)(main, project_root=root)
    if api == "assemble":
        assert result.content.index("chapter") < result.content.index("local")
        assert result.content.index("local") < result.content.index("fallback")
        assert result.content.count("chapter") == 1
        assert result.origin(1) == ("章节 空格.tex", 1)
        assert ("nested/local.tex", 1) in result.origins
    else:
        assert [node.rel for node in result] == [
            "nested/main.tex",
            "章节 空格.tex",
            "nested/local.tex",
            "fallback.tex",
        ]
    with pytest.raises(loader.IncludeBoundaryError):
        getattr(loader, api)(main)


@pytest.mark.parametrize("api", ["assemble", "iter_files"])
@pytest.mark.parametrize("kind", ["mismatch", "missing", "file"])
def test_invalid_project_root_fails_before_entry_read(loader, tmp_path, monkeypatch, api, kind):
    main = tmp_path / "main.tex"
    main.write_text("entry", encoding="utf-8")
    root = tmp_path / "root"
    if kind == "mismatch":
        root.mkdir()
    elif kind == "file":
        root.write_text("not a directory", encoding="utf-8")
    reads = []
    monkeypatch.setattr(loader, "read_text_robust", lambda path: reads.append(path))
    with pytest.raises(loader.IncludeBoundaryError, match="E-INCLUDE-BOUNDARY"):
        getattr(loader, api)(main, project_root=root)
    assert reads == []


@pytest.mark.parametrize("api", ["assemble", "iter_files"])
@pytest.mark.parametrize("kind", ["candidate", "fallback"])
def test_fallback_cannot_hide_or_create_an_escape(loader, tmp_path, api, kind):
    root = tmp_path / "project"
    nested = root / "nested"
    nested.mkdir(parents=True)
    main = root / "main.tex"
    main.write_text("\\input{nested/chapter}", encoding="utf-8")
    chapter = nested / "chapter.tex"
    if kind == "candidate":
        outside = tmp_path / "outside.tex"
        outside.write_text("external", encoding="utf-8")
        (root / "target.tex").write_text("fallback must not mask escape", encoding="utf-8")
        try:
            (nested / "target.tex").symlink_to(outside)
        except OSError as exc:
            pytest.skip(f"symlink creation unavailable: {exc}")
        chapter.write_text("% line one\n\\input{target}", encoding="utf-8")
    else:
        # The current-directory candidate is inside the root but missing.
        # Resolving the same argument from the root would escape.
        chapter.write_text("% line one\n\\input{../missing}", encoding="utf-8")
    with pytest.raises(loader.IncludeBoundaryError, match="nested/chapter.tex:2"):
        getattr(loader, api)(main)


@pytest.mark.parametrize("api", ["assemble", "iter_files"])
def test_missing_cycle_and_encoding_remain_distinct(loader, tmp_path, api):
    main = tmp_path / "main.tex"
    main.write_text("\\input{chapter}\n\\input{missing}", encoding="utf-8")
    (tmp_path / "chapter.tex").write_bytes("中文\n\\input{main}".encode("gb18030"))
    result = getattr(loader, api)(main)
    if api == "assemble":
        assert result.missing == [("missing", "main.tex", 2)]
        assert len(result.warnings) == 1
        if "-zh" in loader.__file__:
            assert "中文" in result.content
    else:
        assert len(result) == 3
        assert result[-1].rel == "missing.tex" and not result[-1].exists
        assert result[1].warning


@pytest.mark.parametrize("api", ["assemble", "iter_files"])
@pytest.mark.parametrize(
    "raw",
    [r"\\server.invalid\share\outside", r"\outside", "Z:/outside", "Z:outside", "bad\x00path"],
)
def test_windows_or_invalid_path_has_no_external_resolution(
    loader, tmp_path, monkeypatch, api, raw
):
    main = tmp_path / "main.tex"
    main.write_text(f"\\input{{{raw}}}", encoding="utf-8")
    original_resolve = Path.resolve
    external_resolves = []

    def resolve(path, *args, **kwargs):
        if not Path(os.path.abspath(path)).is_relative_to(tmp_path):
            external_resolves.append(path)
            pytest.fail("external path resolution attempted")
        return original_resolve(path, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", resolve)
    with pytest.raises(loader.IncludeBoundaryError, match="main.tex:1"):
        getattr(loader, api)(main)
    assert external_resolves == []


@pytest.mark.parametrize("api", ["assemble", "iter_files"])
def test_symlink_loop_is_a_boundary_error(loader, tmp_path, api):
    main = tmp_path / "main.tex"
    main.write_text("\\input{loop}", encoding="utf-8")
    try:
        (tmp_path / "loop.tex").symlink_to("loop.tex")
    except OSError as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")
    with pytest.raises(loader.IncludeBoundaryError, match="main.tex:1"):
        getattr(loader, api)(main)


def test_typst_passthrough_remains_unexpanded(loader, tmp_path):
    main = tmp_path / "main.typ"
    content = r"Typst text \input{../outside}"
    main.write_text(content, encoding="utf-8")
    doc = loader.assemble(main)
    assert doc.content == content
    assert doc.origin(1) == ("main.typ", 1)


def test_native_absolute_path_is_allowed_on_posix(loader, tmp_path, monkeypatch):
    chapter = tmp_path / "chapter.tex"
    chapter.write_text("contained absolute target", encoding="utf-8")
    # Exercise POSIX dispatch on Windows without replacing pathlib's host implementation.
    raw = chapter.as_posix()
    if os.name == "nt":
        raw = raw[len(chapter.drive) :]
    main = tmp_path / "main.tex"
    main.write_text(f"\\input{{{raw}}}", encoding="utf-8")
    monkeypatch.setattr(loader, "os", SimpleNamespace(name="posix", path=os.path))
    assert loader.assemble(main).content == "contained absolute target"


@pytest.mark.parametrize("api", ["assemble", "iter_files"])
def test_internal_symlink_parent_and_project_root_alias(loader, tmp_path, api):
    root = tmp_path / "project"
    (root / "real/sub").mkdir(parents=True)
    (root / "real/target.tex").write_text("real target", encoding="utf-8")
    (root / "target.tex").write_text("root target", encoding="utf-8")
    main = root / "main.tex"
    main.write_text("\\input{link/../target}", encoding="utf-8")
    alias = tmp_path / "alias"
    try:
        (root / "link").symlink_to(root / "real/sub", target_is_directory=True)
        alias.symlink_to(root, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"directory symlink creation unavailable: {exc}")
    # Preserve the host's Path.resolve semantics (Windows and POSIX differ here).
    expected = (root / "link/../target.tex").resolve()
    result = getattr(loader, api)(alias / "main.tex", project_root=alias)
    if api == "assemble":
        assert result.content == expected.read_text(encoding="utf-8")
        assert result.origin(1) == (expected.relative_to(root).as_posix(), 1)
    else:
        assert result[1].content == expected.read_text(encoding="utf-8")
        assert result[1].rel == expected.relative_to(root).as_posix()


@pytest.mark.parametrize("script", ["check_references.py", "check_format.py"])
def test_analysis_cli_reports_boundary_failure(tmp_path, script):
    root = tmp_path / "project"
    root.mkdir()
    main = root / "main.tex"
    main.write_text("\\input{../outside}", encoding="utf-8")
    (tmp_path / "outside.tex").write_text("synthetic marker", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(SKILLS_ROOT / "latex-thesis-zh/scripts" / script),
            str(main),
        ],
        capture_output=True,
        encoding="utf-8",
        env=dict(os.environ, PYTHONIOENCODING="utf-8"),
        check=False,
    )
    assert result.returncode != 0
    assert "E-INCLUDE-BOUNDARY" in result.stderr
    assert "main.tex:1" in result.stderr
    assert "synthetic marker" not in result.stdout + result.stderr


def test_review_workspace_cli_does_not_mask_boundary_failure(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    main = root / "main.tex"
    main.write_text("\\input{../outside}", encoding="utf-8")
    (tmp_path / "outside.tex").write_text("synthetic marker", encoding="utf-8")
    output = tmp_path / "review"
    result = subprocess.run(
        [
            sys.executable,
            str(SKILLS_ROOT / "paper-audit/scripts/prepare_review_workspace.py"),
            str(main),
            "--output-dir",
            str(output),
        ],
        capture_output=True,
        encoding="utf-8",
        env=dict(os.environ, PYTHONIOENCODING="utf-8"),
        check=False,
    )
    assert result.returncode != 0
    assert "E-INCLUDE-BOUNDARY" in result.stderr
    assert "main.tex:1" in result.stderr
    assert "WORKSPACE:" not in result.stdout
    assert not list(output.rglob("*.json"))


@pytest.fixture(
    params=[
        ("latex-thesis-zh", "check_format.py"),
        ("paper-audit", "prepare_review_workspace.py"),
    ]
)
def boundary_caller(request):
    skill, script = request.param
    scripts = SKILLS_ROOT / skill / "scripts"
    saved_path = list(sys.path)
    saved_modules = dict(sys.modules)
    try:
        for sibling in scripts.glob("*.py"):
            sys.modules.pop(sibling.stem, None)
        sys.path.insert(0, str(scripts))
        spec = importlib.util.spec_from_file_location("security_boundary_caller", scripts / script)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        assert module.__file__ is not None
        assert Path(module.__file__) == scripts / script
        assert module.IncludeBoundaryError is sys.modules["tex_loader"].IncludeBoundaryError
        yield skill, module
    finally:
        sys.path[:] = saved_path
        for name in set(sys.modules) - set(saved_modules):
            sys.modules.pop(name, None)
        sys.modules.update(saved_modules)


@pytest.mark.parametrize("error_type", [OSError, UnicodeError, ValueError])
def test_callers_retain_non_boundary_error_fallbacks(
    boundary_caller, tmp_path, monkeypatch, error_type
):
    skill, module = boundary_caller
    main = tmp_path / "main.tex"
    main.write_text("synthetic source", encoding="utf-8")

    def fail_assembly(entry):
        assert entry == main
        raise error_type("synthetic non-boundary failure")

    monkeypatch.setattr(module, "assemble", fail_assembly)
    if skill == "latex-thesis-zh":
        assert module.FormatChecker(str(main))._run_chinese_checks() == ([], [])
    else:
        layout = module.WorkspaceLayout(tmp_path / "review")
        state = module.prepare_subsection_artifacts(main, object(), layout)
        assert state["status"] == "unsupported_format"
        assert json.loads(layout.subsection_index.read_text(encoding="utf-8")) == {
            "subsection_index_status": "unsupported_format",
            "units": [],
        }
