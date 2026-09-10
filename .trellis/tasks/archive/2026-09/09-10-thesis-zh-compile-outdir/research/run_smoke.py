"""Record isolated real-TeX runs through the shipped wrapper; never clean user files."""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


repo = Path(__file__).resolve().parents[4]
evidence = Path(__file__).parent / "tex-smoke"
evidence.mkdir(exist_ok=True)
isolated = Path(tempfile.mkdtemp(prefix="c3-wrapper-"))
wrapper = repo / "academic-writing-skills/latex-thesis-zh/scripts/compile.py"
environment = dict(os.environ)
environment["PYTHONIOENCODING"] = "utf-8"

versions = {}
for tool in ("latexmk", "xelatex", "lualatex"):
    executable = shutil.which(tool)
    if executable is None:
        raise SystemExit(f"Missing tool: {tool}")
    result = subprocess.run([executable, "--version"], capture_output=True, check=False)
    versions[tool] = {
        "executable": executable,
        "exit": result.returncode,
        "stdout": result.stdout.decode("utf-8", errors="backslashreplace"),
        "stderr": result.stderr.decode("utf-8", errors="backslashreplace"),
    }

cases = [
    ("recipe-relative", ["--recipe", "latexmk"], "build"),
    ("compiler-xelatex-absolute", ["--compiler", "xelatex"], str(isolated / "external output")),
    ("compiler-lualatex-unicode-space", ["--compiler", "lualatex"], "构建 目录"),
    ("default-relative", [], "build"),
    ("default-no-outdir", [], None),
    ("recipe-up-to-date", ["--recipe", "latexmk"], "build"),
]
records = []
for name, options, outdir in cases:
    source = isolated / ("recipe-relative" if name == "recipe-up-to-date" else name)
    source.mkdir(exist_ok=True)
    entry = source / "main.tex"
    if name != "recipe-up-to-date":
        entry.write_text(
            "% !TEX program = xelatex\n"
            "\\documentclass{article}\n\\begin{document}\n"
            "Synthetic wrapper output-location smoke.\n\\end{document}\n",
            encoding="utf-8",
        )
    target = (source / outdir if outdir else source) / "main.pdf"
    before_mtime = target.stat().st_mtime_ns if target.exists() else None
    command = ["uv", "run", "--no-sync", "python", str(wrapper), str(entry), *options]
    if outdir:
        command.extend(["--outdir", outdir])
    result = subprocess.run(command, cwd=repo, env=environment, capture_output=True, check=False)
    for stream in ("stdout", "stderr"):
        (evidence / f"{name}.{stream}.txt").write_text(
            getattr(result, stream).decode("utf-8", errors="backslashreplace"),
            encoding="utf-8",
            newline="",
        )
    records.append(
        {
            "name": name,
            "cwd": str(repo),
            "command": command,
            "exit": result.returncode,
            "target_pdf": str(target),
            "target_exists": target.exists(),
            "target_size": target.stat().st_size if target.exists() else None,
            "mtime_before": before_mtime,
            "mtime_after": target.stat().st_mtime_ns if target.exists() else None,
            "source_pdf_exists": entry.with_suffix(".pdf").exists(),
            "stdout": f"tex-smoke/{name}.stdout.txt",
            "stderr": f"tex-smoke/{name}.stderr.txt",
        }
    )
    print(json.dumps(records[-1], ensure_ascii=False), flush=True)

(evidence / "results.json").write_text(
    json.dumps(
        {"kind": "isolated_real_wrapper", "isolated": str(isolated), "versions": versions, "runs": records},
        ensure_ascii=False,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)
