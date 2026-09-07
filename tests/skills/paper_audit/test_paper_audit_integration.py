"""Integration tests for the paper-audit consuming pipeline (06-13-paper-audit-integrity, A8/A6).

These exercise the audit pipeline's wiring to the shared parser foundation
rather than the parser units (those live in ``test_en_family_parsers_multifile.py``
and are hash-locked by ``test_parsers_alignment.py``):

- ``prepare_workspace`` runs end-to-end on a multi-section paper and produces
  every ``WorkspaceLayout`` artifact downstream agents consume;
- non-UTF-8 manuscripts are ingested via ``read_text_robust`` (A6) instead of
  crashing the audit at first read.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from paths import WorkspaceLayout

from tests.support.paths import SCRIPT_DIR_AUDIT

# UTF-8 bytes for these characters are not a valid GBK sequence (em dash 0xE2
# 0x80 0x94). A locale-encoded Windows pipe then returns stdout=None.
UNICODE_STDOUT = "方法——结果：精度提升 8%。"
UNICODE_STDERR = "检查失败：编码边界—管道"

_DRIVER_SOURCE = """\
import json
import sys
from pathlib import Path

from audit import _run_check_script

rc, stdout, stderr = _run_check_script(Path(sys.argv[1]), sys.argv[2])
Path(sys.argv[3]).write_text(
    json.dumps(
        {
            "rc": rc,
            "out": stdout,
            "err": stderr,
            "out_is_str": isinstance(stdout, str),
            "err_is_str": isinstance(stderr, str),
        },
        ensure_ascii=False,
    ),
    encoding="utf-8",
)
"""


def _write_unicode_checker(tmp_path: Path, *, returncode: int = 0, hang: bool = False) -> Path:
    if hang:
        script = tmp_path / "hang_checker.py"
        script.write_text("import time\ntime.sleep(3600)\n", encoding="utf-8")
        return script
    script = tmp_path / f"unicode_checker_{returncode}.py"
    lines = [
        "import sys",
        f"print({UNICODE_STDOUT!r})",
    ]
    if returncode != 0:
        lines.append(f"print({UNICODE_STDERR!r}, file=sys.stderr)")
    lines.append(f"raise SystemExit({returncode})")
    script.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return script


def _run_nested_stream_utf8(tmp_path: Path, checker: Path, paper: Path) -> dict:
    """Call shipped _run_check_script in a PYTHONUTF8=0 / stream-UTF-8 parent."""
    driver = tmp_path / "run_check_script_driver.py"
    driver.write_text(_DRIVER_SOURCE, encoding="utf-8")
    result_path = tmp_path / "run_check_script_result.json"
    env = dict(os.environ)
    env["PYTHONUTF8"] = "0"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    extra_path = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        str(SCRIPT_DIR_AUDIT) + os.pathsep + extra_path if extra_path else str(SCRIPT_DIR_AUDIT)
    )
    completed = subprocess.run(
        [sys.executable, "-B", str(driver), str(checker), str(paper), str(result_path)],
        capture_output=True,
        timeout=30,
        env=env,
        cwd=str(tmp_path),
    )
    if not result_path.is_file():
        stderr = completed.stderr.decode("utf-8", errors="replace")
        stdout = completed.stdout.decode("utf-8", errors="replace")
        raise AssertionError(
            "nested _run_check_script driver wrote no result "
            f"(exit={completed.returncode}): {stderr or stdout}"
        )
    payload: dict = json.loads(result_path.read_text(encoding="utf-8"))
    return payload


MULTI_SECTION_PAPER = "\n".join(
    [
        r"\documentclass{article}",
        r"\title{A Robust Method for Testing Pipelines}",
        r"\begin{document}",
        r"\maketitle",
        r"\begin{abstract}",
        r"We present a method and report results on standard benchmarks.",
        r"\end{abstract}",
        r"\section{Introduction}",
        r"Prior work is limited; we address that gap directly.",
        r"\section{Method}",
        r"We use a carefully designed approach with explicit assumptions.",
        r"\section{Experiments}",
        r"Our method improves over the baselines by a clear margin.",
        r"\section{Conclusion}",
        r"We conclude and outline future directions.",
        r"\end{document}",
        "",
    ]
)


def test_prepare_workspace_end_to_end_produces_layout_artifacts(tmp_path: Path) -> None:
    """The deep-review workspace builder wires the shared parser to every
    artifact the committee/consolidate/render steps later read."""
    from prepare_review_workspace import prepare_workspace

    paper = tmp_path / "paper.tex"
    paper.write_text(MULTI_SECTION_PAPER, encoding="utf-8")

    workspace = prepare_workspace(str(paper), output_dir=str(tmp_path / "review_results"))
    assert workspace.exists()

    layout = WorkspaceLayout(workspace)
    # The five artifacts prepare_workspace advertises as its initial output.
    for artifact in (
        layout.full_text,
        layout.metadata,
        layout.section_index,
        layout.claim_map,
        layout.paper_summary,
    ):
        assert artifact.exists(), f"prepare_workspace did not produce {artifact.name}"

    # Section bodies were split out for the section-reviewer lane.
    section_files = list(layout.sections_dir.glob("*.md"))
    assert section_files, "expected per-section markdown files under artifacts/sections/"

    full_text = layout.full_text.read_text(encoding="utf-8")
    assert "carefully designed approach" in full_text


def test_prepare_workspace_handles_non_utf8_source(tmp_path: Path) -> None:
    """A latin-1 manuscript (non-UTF-8 bytes) must ingest via the robust reader
    instead of raising UnicodeDecodeError at the first read (A6)."""
    from prepare_review_workspace import prepare_workspace

    paper = tmp_path / "paper_latin1.tex"
    # 0xE9 is 'é' in latin-1 but an invalid standalone UTF-8 byte.
    paper.write_bytes(MULTI_SECTION_PAPER.replace("method", "méthode").encode("latin-1"))

    workspace = prepare_workspace(str(paper), output_dir=str(tmp_path / "review_results"))
    assert workspace.exists()
    assert WorkspaceLayout(workspace).full_text.exists()


def test_read_source_decodes_non_utf8_with_warning(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """audit._read_source returns text for a non-UTF-8 source and warns on stderr
    rather than crashing (A6)."""
    from audit import _read_source

    paper = tmp_path / "weird.tex"
    paper.write_bytes(b"\\section{Intro}\nCaf\xe9 results are strong.\n")

    text = _read_source(paper)
    assert isinstance(text, str)
    assert "results are strong" in text

    captured = capsys.readouterr()
    assert "not UTF-8" in captured.err


@pytest.mark.skipif(
    sys.platform != "win32",
    reason="Windows stream-only UTF-8 vs GBK subprocess pipe",
)
@pytest.mark.parametrize("returncode", [0, 3])
def test_run_check_script_windows_stream_utf8_keeps_unicode(
    tmp_path: Path, returncode: int
) -> None:
    """Shipped _run_check_script must keep Chinese across a GBK parent pipe."""
    from audit import _run_check_script

    assert callable(_run_check_script)

    paper = tmp_path / "paper.tex"
    paper.write_text("% dummy\n", encoding="utf-8")
    checker = _write_unicode_checker(tmp_path, returncode=returncode)
    payload = _run_nested_stream_utf8(tmp_path, checker, paper)

    assert payload["out_is_str"] is True
    assert isinstance(payload["out"], str)
    assert UNICODE_STDOUT in payload["out"]
    assert payload["rc"] == returncode
    if returncode != 0:
        assert payload["err_is_str"] is True
        assert isinstance(payload["err"], str)
        assert UNICODE_STDERR in payload["err"]


@pytest.mark.skipif(sys.platform == "win32", reason="non-Windows Unicode protocol path")
@pytest.mark.parametrize("returncode", [0, 3])
def test_run_check_script_unicode_protocol_non_windows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, returncode: int
) -> None:
    """Non-Windows path: import shipped _run_check_script and keep Unicode."""
    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    from audit import _run_check_script

    paper = tmp_path / "paper.tex"
    paper.write_text("% dummy\n", encoding="utf-8")
    checker = _write_unicode_checker(tmp_path, returncode=returncode)
    rc, stdout, stderr = _run_check_script(checker, str(paper))

    assert isinstance(stdout, str)
    assert UNICODE_STDOUT in stdout
    assert rc == returncode
    if returncode != 0:
        assert isinstance(stderr, str)
        assert UNICODE_STDERR in stderr


def test_run_check_script_timeout_returns_minus_one(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """TimeoutExpired from a real child still maps to returncode -1."""
    import audit
    from audit import _run_check_script

    paper = tmp_path / "paper.tex"
    paper.write_text("% dummy\n", encoding="utf-8")
    checker = _write_unicode_checker(tmp_path, hang=True)

    real_run = audit.subprocess.run

    def run_with_short_timeout(*args, **kwargs):
        kwargs = dict(kwargs)
        if kwargs.get("timeout") == 120:
            kwargs["timeout"] = 1
        return real_run(*args, **kwargs)

    monkeypatch.setattr(audit.subprocess, "run", run_with_short_timeout)
    rc, stdout, stderr = _run_check_script(checker, str(paper))
    assert rc == -1
    assert stdout == ""
    assert stderr == "Script timed out after 120 seconds"
