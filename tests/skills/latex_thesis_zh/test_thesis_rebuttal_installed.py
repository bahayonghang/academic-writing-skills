"""Run the shipped response pipeline with only the thesis package installed."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from tests.support.paths import SKILLS_ROOT

SKILL = SKILLS_ROOT / "latex-thesis-zh"


def digest_tree(root: Path) -> dict[str, str]:
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*")
        if p.is_file() and ".git" not in p.parts
    }


def run_cli(installed: Path, cwd: Path, name: str, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-B", str(installed / "scripts" / f"rebuttal_{name}.py"), *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        encoding="utf-8",
        timeout=60,
    )


def test_standalone_completed_pipeline(tmp_path: Path, rebuttal_case) -> None:
    installed = tmp_path / "installed" / "latex-thesis-zh"
    shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__"))
    cwd = tmp_path / "outside"
    cwd.mkdir()
    assert not (installed.parent / "latex-defense-zh").exists()
    thesis = tmp_path / "submitted"
    shutil.copytree(installed / "evals/fixtures/rebuttal/mini-thesis", thesis)
    # The fixture holds an actual submitted/revised git history, not user_confirmed evidence.
    state = json.loads((rebuttal_case.workspace / "rebuttal_state.json").read_text("utf-8"))
    baseline = state["thesis"]["base_commit"]
    shutil.copytree(rebuttal_case.thesis / ".git", thesis / ".git")
    # Restore submitted aux content explicitly; never reset the shared working tree.
    original_aux = subprocess.run(
        ["git", "-C", str(thesis), "show", f"{baseline}:document.aux"],
        capture_output=True,
        check=True,
    ).stdout
    (thesis / "document.aux").write_bytes(original_aux)
    reviews = tmp_path / "review-input"
    shutil.copytree(installed / "evals/fixtures/rebuttal/reviews", reviews)
    review_before = digest_tree(reviews)
    output = tmp_path / "response-output"
    before = digest_tree(thesis)
    result = run_cli(
        installed,
        cwd,
        "intake",
        "--reviews",
        str(reviews),
        "--thesis",
        str(thesis),
        "--main",
        "document.tex",
        "--base-commit",
        baseline,
        "--root",
        str(output),
        "--json",
    )
    assert result.returncode == 0, result.stderr
    assert digest_tree(thesis) == before
    # Apply the same real synthetic revision used by the original gate regression.
    for rel in ("chapters/chapter2.tex", "chapters/chapter2.aux", "document.aux", "references.bib"):
        shutil.copyfile(rebuttal_case.thesis / rel, thesis / rel)
    for path in thesis.rglob("*.aux"):
        os.utime(path, (2_000_000_000, 2_000_000_000))
    workspace = output / "workspace"
    shutil.copyfile(
        installed / "evals/fixtures/rebuttal/concerns-done.yaml", workspace / "concerns.yaml"
    )
    before = digest_tree(thesis)
    result = run_cli(
        installed, cwd, "build", "--workspace", str(workspace), "--thesis", str(thesis), "--json"
    )
    assert result.returncode == 0, result.stderr
    result = run_cli(
        installed, cwd, "check", "--workspace", str(workspace), "--thesis", str(thesis), "--json"
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["findings"] == []
    assert payload["skipped"] == []
    assert digest_tree(thesis) == before
    assert digest_tree(reviews) == review_before
    assert (output / "responses/response-all.md").is_file()
    assert json.loads((workspace / "check.json").read_text("utf-8")) == payload


def test_standalone_review_only_reports_skips(tmp_path: Path) -> None:
    installed = tmp_path / "installed" / "latex-thesis-zh"
    shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__"))
    cwd = tmp_path / "outside"
    cwd.mkdir()
    reviews = tmp_path / "review-input"
    shutil.copytree(installed / "evals/fixtures/rebuttal/reviews", reviews)
    output = tmp_path / "response-output"
    before = digest_tree(reviews)
    result = run_cli(
        installed, cwd, "intake", "--reviews", str(reviews), "--root", str(output), "--json"
    )
    assert result.returncode == 0, result.stderr
    workspace = output / "workspace"
    result = run_cli(installed, cwd, "build", "--workspace", str(workspace), "--json")
    assert result.returncode == 0, result.stderr
    result = run_cli(installed, cwd, "check", "--workspace", str(workspace), "--json")
    assert result.returncode == 1  # An open ledger must not be reported as complete.
    assert set(json.loads(result.stdout)["skipped"]) == {
        "R-COMMIT(git)",
        "R-LOC(aux)",
        "R-PAGE-STALE",
        "R-RENUM",
        "R-NUM-SRC",
    }
    assert digest_tree(reviews) == before


def test_thesis_owns_response_routes_and_local_fixtures() -> None:
    text = (SKILL / "SKILL.md").read_text("utf-8")
    defense = (SKILLS_ROOT / "latex-defense-zh/SKILL.md").read_text("utf-8")
    for name in ("intake", "build", "check"):
        assert f"| `rebuttal-{name}` |" in text
        assert f"rebuttal-{name}" not in defense
    for item in json.loads((SKILL / "evals/evals.json").read_text("utf-8"))["evals"]:
        for rel in item["files"]:
            assert (SKILL / rel).is_file(), rel
    cases = json.loads((SKILL / "evals/trigger_eval.json").read_text("utf-8"))["queries"]
    assert any(c["category"] == "edge-review-only" and c["should_trigger"] for c in cases)
    assert any(
        c["category"] == "negative-overlap-latex-defense-zh" and not c["should_trigger"]
        for c in cases
    )


def test_rebuttal_imports_are_thesis_local(thesis_rebuttal_scripts) -> None:
    module = thesis_rebuttal_scripts.rebuttal_check
    assert Path(module.__file__).parent == SKILL / "scripts"
    assert Path(module.rc.__file__).parent == SKILL / "scripts"
    assert Path(module.rc.tex_loader.__file__).parent == SKILL / "scripts"
