"""Regression tests for check_references.py multi-file assemble adoption (A-EN-1).

``check_references.py`` previously read only the entry ``.tex`` file, so a
skeleton ``main.tex`` that keeps labels/refs in ``\\input``-ed sub-files
reported every cross-file ``\\ref`` as a false "Undefined reference" Critical/
P0 issue (exit 1). Fixed via ``tex_loader.assemble()`` with source-location
mapping through ``AssembledDocument.origin()/lineref()``.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from tests.support.paths import SCRIPT_DIR_EN

CHECK_REFERENCES = SCRIPT_DIR_EN / "check_references.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    # PYTHONIOENCODING pinned on the child process env (not the pytest
    # invocation itself) so em-dash punctuation in issue messages round-trips
    # on Windows where a piped child stdout otherwise defaults to the ANSI
    # codepage instead of UTF-8 (see spec gotcha in testing-and-tooling.md).
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-B", str(CHECK_REFERENCES), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )


def _write_project(tmp_path: Path) -> Path:
    """label + caption live in sections/method.tex; main.tex's own body directly
    references that label (as a paper's own text commonly does), so a
    read-the-entry-file-only checker sees the \\ref but never the \\label —
    reproducing the true false-P0 (a real cross-file ref, visible today,
    wrongly flagged undefined). sections/intro.tex is a second included file
    with no refs of its own, kept to prove real multi-file assembly (not just
    a two-file special case)."""
    (tmp_path / "sections").mkdir()
    main = tmp_path / "main.tex"
    main.write_text(
        "\\documentclass{article}\n"
        "\\begin{document}\n"
        "\\input{sections/method}\n"
        "\\input{sections/intro}\n"
        "As shown in Figure~\\ref{fig:arch}, the architecture is described above.\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    (tmp_path / "sections" / "method.tex").write_text(
        "\\section{Methods}\n"
        "\\begin{figure}\n"
        "\\includegraphics{arch}\n"
        "\\caption{Architecture}\n"
        "\\label{fig:arch}\n"
        "\\end{figure}\n",
        encoding="utf-8",
    )
    (tmp_path / "sections" / "intro.tex").write_text(
        "\\section{Introduction}\nBackground text with no references of its own.\n",
        encoding="utf-8",
    )
    return main


# ── A: no false "Undefined reference" across \input boundaries ───────────────


def test_multifile_no_false_undefined_reference(tmp_path: Path) -> None:
    main = _write_project(tmp_path)
    result = _run(str(main), "--json")
    issues = json.loads(result.stdout)
    undefined = [i for i in issues if "Undefined reference" in i["message"]]
    assert undefined == []


# ── B: CLI exit code is 0 (previously 1: false P0) ────────────────────────────


def test_multifile_exit_code_zero(tmp_path: Path) -> None:
    main = _write_project(tmp_path)
    result = _run(str(main))
    assert result.returncode == 0


# ── C: a genuinely undefined ref reports a source-file:line location ─────────


def test_multifile_undefined_ref_location_points_to_source_file(tmp_path: Path) -> None:
    main = _write_project(tmp_path)
    (tmp_path / "sections" / "intro.tex").write_text(
        "\\section{Introduction}\nSee Figure~\\ref{fig:ghost} for details.\n",
        encoding="utf-8",
    )
    result = _run(str(main))
    assert result.returncode == 1
    assert "sections/intro.tex:" in result.stdout
    assert "fig:ghost" in result.stdout
    # The genuinely-resolved cross-file ref must not also be reported.
    assert "fig:arch" not in result.stdout

    result_json = _run(str(main), "--json")
    issues = json.loads(result_json.stdout)
    ghost_issue = next(i for i in issues if "fig:ghost" in i["message"])
    assert ghost_issue["file"] == "sections/intro.tex"
    assert ghost_issue["source_line"] == 2


# ── D: a missing \input target produces a WARN line, not a crash ─────────────


def test_missing_input_reported_as_warning_not_crash(tmp_path: Path) -> None:
    main = tmp_path / "main.tex"
    main.write_text(
        "\\documentclass{article}\n\\begin{document}\n\\input{sections/ghost}\n\\end{document}\n",
        encoding="utf-8",
    )
    result = _run(str(main))
    assert result.returncode == 0
    assert "WARN" in result.stdout
    assert "ghost" in result.stdout


# ── E: single-file input is byte-for-byte unchanged ("Line N" format) ────────


def test_single_file_output_unchanged(tmp_path: Path) -> None:
    tex = tmp_path / "solo.tex"
    tex.write_text(
        "\\documentclass{article}\n\\begin{document}\n\\ref{fig:missing}\n\\end{document}\n",
        encoding="utf-8",
    )
    result = _run(str(tex))
    assert result.returncode == 1
    assert "(Line 3)" in result.stdout
    assert "sections/" not in result.stdout
    assert "WARN" not in result.stdout


def test_single_file_json_output_unchanged_keys(tmp_path: Path) -> None:
    """Single-file JSON keeps the additive file/source_line fields consistent
    with the entry file (not a behavior change, just always-present metadata)."""
    tex = tmp_path / "solo.tex"
    tex.write_text(
        "\\documentclass{article}\n\\begin{document}\n\\ref{fig:missing}\n\\end{document}\n",
        encoding="utf-8",
    )
    result = _run(str(tex), "--json")
    issues = json.loads(result.stdout)
    assert issues[0]["line"] == 3
    assert issues[0]["severity"] == "Critical"
