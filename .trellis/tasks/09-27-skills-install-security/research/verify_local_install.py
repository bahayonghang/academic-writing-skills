"""Install the four discoverable packages into a disposable project and test copies."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
SKILLS = ("latex-thesis-zh", "latex-paper-en", "paper-audit", "cover-letter")
VERSION = "1.7.0"


def verify_copies(installed: Path) -> int:
    import pytest

    class InstalledCopies:
        def pytest_collection_modifyitems(self, items):
            for item in items:
                if item.path.name == "test_tex_loader_security.py":
                    item.module.SKILLS_ROOT = installed

    return pytest.main(
        [
            str(REPO / "tests/shared/test_tex_loader_security.py"),
            "-q",
            "-k",
            "not latex-defense-zh",
        ],
        plugins=[InstalledCopies()],
    )


def main() -> int:
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    assert npx, "npx is required"
    cli_evidence = {}
    for option, name in (("--version", "version"), ("--help", "help")):
        probe = subprocess.run(
            [npx, "--yes", f"skills@{VERSION}", option],
            cwd=REPO,
            capture_output=True,
            encoding="utf-8",
            timeout=180,
        )
        assert probe.returncode == 0, probe.stderr
        (EVIDENCE / f"install-cli-{name}.txt").write_text(
            probe.stdout + probe.stderr, encoding="utf-8"
        )
        cli_evidence[name] = {
            "command": ["npx", "--yes", f"skills@{VERSION}", option],
            "exit": probe.returncode,
        }
        if name == "version":
            assert probe.stdout.strip() == VERSION, probe.stdout
    with tempfile.TemporaryDirectory(prefix="skills-install-boundary-") as directory:
        sandbox = Path(directory).resolve()
        project = sandbox / "project"
        project.mkdir()
        command = [
            npx,
            "--yes",
            f"skills@{VERSION}",
            "add",
            str(REPO / "academic-writing-skills"),
            "--skill",
            *SKILLS,
            "--agent",
            "codex",
            "--copy",
            "--yes",
            "--json",
        ]
        result = subprocess.run(
            command, cwd=project, capture_output=True, encoding="utf-8", timeout=180
        )

        def redact(text):
            for path, token in ((str(REPO), "<repo>"), (str(sandbox), "<temp>")):
                text = text.replace(path, token).replace(path.replace("\\", "/"), token)
                text = text.replace(path.replace("\\", "\\\\"), token)
            return text

        (EVIDENCE / "install-output.txt").write_text(
            redact(result.stdout + result.stderr), encoding="utf-8"
        )
        assert result.returncode == 0, redact(result.stderr)
        installed = project / ".agents/skills"
        records = []
        for skill in SKILLS:
            source = REPO / "academic-writing-skills" / skill / "scripts/tex_loader.py"
            target = installed / skill / "scripts/tex_loader.py"
            assert target.resolve().is_relative_to(project), (
                "installation escaped temporary project"
            )
            assert target.is_file() and not target.is_symlink()
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            target_hash = hashlib.sha256(target.read_bytes()).hexdigest()
            assert source_hash == target_hash
            records.append(
                {
                    "skill": skill,
                    "sha256": target_hash,
                    "installed_path": target.relative_to(project).as_posix(),
                }
            )
        caller_records = []
        for relative in (
            "latex-thesis-zh/scripts/check_format.py",
            "paper-audit/scripts/prepare_review_workspace.py",
        ):
            source = REPO / "academic-writing-skills" / relative
            target = installed / relative
            assert target.resolve().is_relative_to(project) and not target.is_symlink()
            source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
            target_hash = hashlib.sha256(target.read_bytes()).hexdigest()
            assert source_hash == target_hash
            caller_records.append({"path": relative, "sha256": target_hash})
        env = dict(os.environ)
        # Leave pytest's encoding environment unchanged.
        check = subprocess.run(
            [sys.executable, "-B", str(Path(__file__).resolve()), "--verify", str(installed)],
            cwd=REPO,
            env=env,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
        (EVIDENCE / "installed-tests.txt").write_text(
            redact(check.stdout + check.stderr), encoding="utf-8"
        )
        record = {
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "cli": f"skills@{VERSION}",
            "source": "local working tree",
            "scope": "project",
            "cli_evidence": cli_evidence,
            "mode": "copy",
            "agent_layout": "codex",
            "source_base_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
            ).strip(),
            "command": ["npx", *command[1:4], "<repo>/academic-writing-skills", *command[5:]],
            "install_exit": result.returncode,
            "test_exit": check.returncode,
            "copies": records,
            "caller_copies": caller_records,
            "defense": "UNVERIFIED: local SKILL.md absent; awaiting C4 integration",
            "remote_publication": "not performed",
            "provider_rescan": "pending",
        }
        (EVIDENCE / "install-evidence.json").write_text(
            json.dumps(record, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(record, indent=2))
        print(redact(check.stdout[-1500:]))
        return check.returncode


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        raise SystemExit(verify_copies(Path(sys.argv[2])))
    raise SystemExit(main())
