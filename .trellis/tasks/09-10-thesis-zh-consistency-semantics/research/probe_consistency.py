"""Repeat G4/G5 against the shipped ZH checker with disposable input."""

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[4]
scripts = root / "academic-writing-skills/latex-thesis-zh/scripts"
saved_path = sys.path[:]
saved_modules = sys.modules.copy()
try:
    sys.modules.pop("tex_loader", None)
    sys.path.insert(0, str(scripts))
    spec = importlib.util.spec_from_file_location("probe_zh_consistency", scripts / "check_consistency.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
finally:
    sys.path[:] = saved_path
    for name in set(sys.modules) - set(saved_modules):
        del sys.modules[name]
    sys.modules.update(saved_modules)

cases = {
    "G4_distinct_concepts": "深度学习是一类研究方法。深度神经网络是该领域使用的模型。",
    "G5_late_definition": "CNN 用于提取特征。\n随后使用 CNN。\n卷积神经网络（CNN）用于建模。",
    "G5_legal_reintroduction": "\\chapter{第一章}\n卷积神经网络（CNN）用于建模。\n\\chapter{第二章}\n卷积神经网络（CNN）用于预测。",
}
with tempfile.TemporaryDirectory() as directory:
    for name, text in cases.items():
        tex = Path(directory) / "main.tex"
        tex.write_text(text, encoding="utf-8")
        checker = module.ConsistencyChecker([str(tex)])
        result = checker.check_terms() if name.startswith("G4") else checker.check_abbreviations()
        print(json.dumps({"probe": name, "result": result}, ensure_ascii=False))
