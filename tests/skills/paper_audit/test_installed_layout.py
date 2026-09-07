"""Isolation smoke for paper-audit sibling skill layout.

Drives the shipped ``paper-audit/scripts/audit.py`` CLI. Full collection copies
all six skill directories as siblings. A paper-audit-only copy is limited
coverage (recorded standalone boundary: missing=8).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from tests.support.paths import REPO_ROOT, SKILLS_ROOT

SAMPLE_PAPER = REPO_ROOT / "tests" / "fixtures" / "paper_audit" / "sample_paper.tex"
SKILL_DIRS = (
    "cover-letter",
    "paper-audit",
    "latex-paper-en",
    "latex-thesis-zh",
    "typst-paper",
    "bib-search-citation",
)
_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")
_AUDIT_TIMEOUT_S = 120
# Recorded isolation probe on SAMPLE_PAPER, quick-audit --lang en --format json.
_FULL_MISSING = 0
_FULL_RUN = 11
_STANDALONE_MISSING = 8
_STANDALONE_RUN = 3


def _utf8_child_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def _copy_skills(dest_parent: Path, names: tuple[str, ...]) -> None:
    dest_parent.mkdir(parents=True, exist_ok=True)
    for name in names:
        shutil.copytree(SKILLS_ROOT / name, dest_parent / name, ignore=_IGNORE)


def _run_audit(audit_script: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-B",
            str(audit_script),
            str(SAMPLE_PAPER),
            "--mode",
            "quick-audit",
            "--lang",
            "en",
            "--format",
            "json",
        ],
        capture_output=True,
        encoding="utf-8",
        timeout=_AUDIT_TIMEOUT_S,
        env=_utf8_child_env(),
        cwd=str(cwd),
        check=False,
    )


def _parse_run_and_missing(stdout: str) -> tuple[list[str], list[str]]:
    run_lines = [line for line in stdout.splitlines() if line.startswith("[audit] RUN ")]
    missing_lines = [
        line
        for line in stdout.splitlines()
        if line.startswith("[audit] SKIP ") and line.endswith(": script not found")
    ]
    return run_lines, missing_lines


def test_installed_layout_full_vs_standalone(tmp_path: Path) -> None:
    assert SAMPLE_PAPER.is_file()

    full_root = tmp_path / "full"
    standalone_root = tmp_path / "standalone"
    _copy_skills(full_root, SKILL_DIRS)
    _copy_skills(standalone_root, ("paper-audit",))

    full_audit = full_root / "paper-audit" / "scripts" / "audit.py"
    standalone_audit = standalone_root / "paper-audit" / "scripts" / "audit.py"
    assert full_audit.is_file()
    assert standalone_audit.is_file()
    assert full_audit.is_relative_to(tmp_path)
    assert standalone_audit.is_relative_to(tmp_path)
    assert not full_audit.is_relative_to(SKILLS_ROOT)

    full = _run_audit(full_audit, full_root)
    standalone = _run_audit(standalone_audit, standalone_root)

    full_run, full_missing = _parse_run_and_missing(full.stdout)
    standalone_run, standalone_missing = _parse_run_and_missing(standalone.stdout)

    assert full.returncode == 0, full.stderr or full.stdout
    assert standalone.returncode == 0, standalone.stderr or standalone.stdout

    assert len(full_missing) == _FULL_MISSING, (
        "full sibling layout must have no unexpected missing scripts; "
        f"RUN={len(full_run)} missing={len(full_missing)} "
        f"lines={full_missing}"
    )
    assert len(standalone_missing) == _STANDALONE_MISSING, (
        "standalone paper-audit is limited coverage; "
        f"RUN={len(standalone_run)} missing={len(standalone_missing)} "
        f"lines={standalone_missing}"
    )
    assert len(standalone_run) == _STANDALONE_RUN, (
        "recorded standalone limited-coverage RUN; "
        f"got RUN={len(standalone_run)} lines={standalone_run}"
    )
    assert len(full_run) == _FULL_RUN, (
        f"recorded full sibling layout RUN; got RUN={len(full_run)} lines={full_run}"
    )
