"""Read-only in-memory reproductions for planning; no TeX process or file writes."""

import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


repo = Path(__file__).resolve().parents[4]
scripts = repo / "academic-writing-skills" / "latex-thesis-zh" / "scripts"
sys.path.insert(0, str(scripts))

def load(name):
    spec = importlib.util.spec_from_file_location("probe_" + name, scripts / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

consistency = load("check_consistency")
compiler_module = load("compile")
observations = {}
cases = {
    "different_concepts": "深度学习是一类研究方法。深度神经网络是该领域使用的模型。",
    "defined_late": "CNN 用于第一阶段。\nCNN 用于第二阶段。\n卷积神经网络（CNN）用于分类。",
    "per_chapter": "\\chapter{方法一}\n卷积神经网络（CNN）用于分类。\n"
                   "\\chapter{方法二}\n卷积神经网络（CNN）用于编码。",
}
for name, content in cases.items():
    path = (repo / (name + ".tex")).resolve()
    checker = consistency.ConsistencyChecker([str(path)])
    checker.content_cache[path] = content
    result = checker.check_terms() if name == "different_concepts" else checker.check_abbreviations()
    observations[name] = {"input": content, "actual": result}

compiler = compiler_module.LaTeXCompiler(
    str(repo / "nonexistent-fixture" / "main.tex"), compiler="xelatex", recipe="latexmk"
)
for name, available in [
    ("only_requested_output", compiler.work_dir / "build" / "main.pdf"),
    ("stale_source_pdf", compiler.tex_file.with_suffix(".pdf")),
]:
    capture = io.StringIO()
    with patch.object(compiler_module.subprocess, "run",
                      return_value=SimpleNamespace(returncode=0)), \
         patch.object(Path, "exists", lambda path: path == available), \
         contextlib.redirect_stdout(capture):
        code = compiler._compile_with_recipe("build")
    observations[name] = {"exit": code, "stdout": capture.getvalue().replace(str(repo), "<repo>")}

print(json.dumps({"kind": "in_memory_and_mock", "observations": observations},
                 ensure_ascii=False, indent=2))
