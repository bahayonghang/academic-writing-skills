"""Read-only product probe: compare checkout and a temporary standalone skill."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "academic-writing-skills" / "paper-audit"
PAPER = ROOT / "tests/fixtures/paper_audit/sample_paper.tex"
base_env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
base_env.pop("PYTHONIOENCODING", None)
base_env.pop("PYTHONUTF8", None)

with tempfile.TemporaryDirectory(prefix="academic-audit-probe-") as temp:
    workspace = Path(temp).resolve()
    isolated = workspace / "paper-audit"
    assert isolated.resolve().is_relative_to(workspace)
    shutil.copytree(SOURCE, isolated, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    cases = (
        ("checkout-default", SOURCE, base_env),
        ("checkout-stream-utf8", SOURCE, dict(base_env, PYTHONIOENCODING="utf-8")),
        ("checkout-utf8-mode", SOURCE, dict(base_env, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")),
        ("standalone-utf8-mode", isolated, dict(base_env, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")),
    )
    for label, skill, env in cases:
        result = subprocess.run(
            [sys.executable, "-B", str(skill / "scripts/audit.py"), str(PAPER),
             "--mode", "quick-audit", "--lang", "en", "--format", "json"],
            cwd=workspace, env=env, capture_output=True, timeout=120,
        )
        stdout = result.stdout.decode("utf-8" if "PYTHONIOENCODING" in env else "gbk", errors="replace")
        stderr = result.stderr.decode("utf-8" if "PYTHONIOENCODING" in env else "gbk", errors="replace")
        (Path(__file__).parent / f"probe-{label}.txt").write_text(stdout + "\nSTDERR:\n" + stderr, encoding="utf-8")
        runs = [line for line in stdout.splitlines() if "[audit] RUN " in line]
        missing = [line for line in stdout.splitlines() if "script not found" in line]
        print(f"{label}: exit={result.returncode}, RUN={len(runs)}, missing={len(missing)}")
        for line in missing:
            print(line)
        if stderr:
            print(stderr[-1700:])
