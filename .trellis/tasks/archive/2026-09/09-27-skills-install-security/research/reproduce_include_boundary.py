"""Read-only loader diagnosis using synthetic files in a temporary directory."""

import ast
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[4]
SKILLS = ("latex-thesis-zh", "latex-defense-zh", "latex-paper-en", "paper-audit", "cover-letter")
rows = []
sources = []
for index, skill in enumerate(SKILLS):
    path = REPO / "academic-writing-skills" / skill / "scripts/tex_loader.py"
    source = path.read_text(encoding="utf-8")
    ast.parse(source)
    sources.append({"skill": skill, "syntax": "pass", "lf_sha256": hashlib.sha256(source.encode()).hexdigest()})
    name = f"boundary_probe_{index}"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix="skills-boundary-probe-") as temp:
        base = Path(temp).resolve()
        root = base / "project"
        root.mkdir()
        outside = base / "outside.tex"
        outside.write_text("SYNTHETIC_OUTSIDE_MARKER\n", encoding="utf-8")
        inside = root / "inside.tex"
        inside.write_text("SYNTHETIC_INSIDE_MARKER\n", encoding="utf-8")
        entry = root / "main.tex"
        cases = {"parent_traversal": "../outside", "absolute_path": outside.as_posix(), "normal_inside": "inside"}
        link = root / "linked.tex"
        try:
            link.symlink_to(outside)
            cases["symlink_escape"] = "linked"
        except OSError as exc:
            rows.append({"skill": skill, "case": "symlink_escape", "status": "unverified", "reason": type(exc).__name__})
        for case, target in cases.items():
            entry.write_text("\\input{" + target + "}\n", encoding="utf-8")
            doc = module.assemble(entry)
            nodes = module.iter_files(entry)
            rows.append({"skill": skill, "case": case,
                         "assemble_outside_read": "SYNTHETIC_OUTSIDE_MARKER" in doc.content,
                         "iter_files_outside_read": any("SYNTHETIC_OUTSIDE_MARKER" in (node.content or "") for node in nodes),
                         "assemble_inside_read": "SYNTHETIC_INSIDE_MARKER" in doc.content,
                         "warning_count": len(doc.warnings), "missing_count": len(doc.missing)})
    del sys.modules[name]
print(json.dumps({"sources": sources, "cases": rows}, indent=2))
