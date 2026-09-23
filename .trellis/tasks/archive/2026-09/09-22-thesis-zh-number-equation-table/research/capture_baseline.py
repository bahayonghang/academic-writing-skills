"""Capture C2 default-path baselines. Not a product script."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / "academic-writing-skills" / "latex-thesis-zh" / "scripts"
FIXTURE = (
    ROOT
    / "academic-writing-skills"
    / "latex-thesis-zh"
    / "evals"
    / "fixtures"
    / "thesis-project"
    / "main.tex"
)
OUT = Path(__file__).resolve().parent / "baseline"
C1_STYLE = (
    ROOT
    / ".trellis"
    / "tasks"
    / "09-22-thesis-zh-term-governance"
    / "research"
    / "baseline"
)

COMMANDS = (
    ("style-default", "check_style_zh.py", []),
    ("format-default", "check_format.py", []),
    ("format-strict", "check_format.py", ["--strict"]),
    ("tables-default", "check_tables.py", []),
    ("tables-fix", "check_tables.py", ["--fix-suggestions"]),
    ("references-default", "check_references.py", []),
)


def run_one(name: str, script: str, extra: list[str]) -> None:
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-X", "utf8", "-B", str(SKILL / script), str(FIXTURE), *extra],
        capture_output=True,
        env=env,
        check=False,
    )
    (OUT / f"{name}.stdout").write_bytes(completed.stdout)
    (OUT / f"{name}.stderr").write_bytes(completed.stderr)
    (OUT / f"{name}.exit").write_bytes(f"{completed.returncode}\n".encode("ascii"))
    print(f"{name} exit={completed.returncode} stdout={len(completed.stdout)} stderr={len(completed.stderr)}")


def compare_style() -> None:
    lines = []
    for suffix in ("stdout", "stderr", "exit"):
        current = (OUT / f"style-default.{suffix}").read_bytes()
        previous = (C1_STYLE / f"style-default.{suffix}").read_bytes()
        same = current == previous
        lines.append(f"style-default.{suffix} c1_match={same} current={len(current)} c1={len(previous)}")
        print(lines[-1])
    (OUT / "c1-style-compare.txt").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def templates_diff() -> None:
    completed = subprocess.run(
        ["git", "diff", "--", "academic-writing-skills/latex-thesis-zh/templates"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    text = completed.stdout.decode("utf-8", errors="replace")
    (OUT / "templates-diff.txt").write_bytes(text.encode("utf-8"))
    print(f"templates diff bytes={len(completed.stdout)} exit={completed.returncode}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not FIXTURE.is_file():
        raise SystemExit(f"missing fixture: {FIXTURE}")
    for name, script, extra in COMMANDS:
        run_one(name, script, extra)
    compare_style()
    templates_diff()


if __name__ == "__main__":
    main()
