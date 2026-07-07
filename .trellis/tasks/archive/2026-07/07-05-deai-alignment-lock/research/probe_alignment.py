"""Probe: hash-compare members across the three deai_check.py copies.

Run from repo root:  python .trellis/tasks/07-05-deai-alignment-lock/research/probe_alignment.py
Outputs, per member, which copies hash-match — raw evidence for the ALIGNMENTS list.
"""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / "academic-writing-skills"

COPIES = {
    "en": SKILLS / "latex-paper-en" / "scripts" / "deai_check.py",
    "zh": SKILLS / "latex-thesis-zh" / "scripts" / "deai_check.py",
    "typst": SKILLS / "typst-paper" / "scripts" / "deai_check.py",
}

SIDECAR_MODULES = ("parsers", "tex_loader", "deai_check")


def load(key: str, path: Path):
    saved_path = list(sys.path)
    saved = {m: sys.modules.pop(m, None) for m in SIDECAR_MODULES}
    try:
        spec = importlib.util.spec_from_file_location(f"probe_deai_{key}", path)
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(path.parent))
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path[:] = saved_path
        for name, mod in saved.items():
            if mod is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = mod


def hash_obj(obj) -> str:
    if inspect.isfunction(obj) or inspect.ismethod(obj) or inspect.isclass(obj):
        payload = inspect.getsource(obj)
    else:
        payload = repr(obj)
    return hashlib.md5(payload.encode("utf-8")).hexdigest()[:8]


def main() -> None:
    mods = {k: load(k, p) for k, p in COPIES.items()}
    checkers = {
        "en": mods["en"].AITraceChecker,
        "zh": mods["zh"].ChineseAITraceChecker,
        "typst": mods["typst"].AITraceChecker,
    }

    print("== top-level members ==")
    top_names = set()
    for mod in mods.values():
        top_names |= {
            n
            for n, v in vars(mod).items()
            if not n.startswith("__")
            and (inspect.isfunction(v) or isinstance(v, (dict, frozenset, str, list, tuple)))
            and getattr(v, "__module__", mod.__name__) == mod.__name__
        }
    for name in sorted(top_names):
        row = {}
        for k, mod in mods.items():
            row[k] = hash_obj(getattr(mod, name)) if hasattr(mod, name) else "-"
        groups = {}
        for k, h in row.items():
            groups.setdefault(h, []).append(k)
        verdict = "MATCH" if len({h for h in row.values() if h != "-"}) == 1 else "DIFF"
        print(f"{verdict:5} {name:28} {row}")

    print(
        "\n== checker methods (en=AITraceChecker, zh=ChineseAITraceChecker, typst=AITraceChecker) =="
    )
    method_names = set()
    for cls in checkers.values():
        method_names |= {
            n for n, v in vars(cls).items() if inspect.isfunction(v) and not n.startswith("__")
        }
    for name in sorted(method_names):
        row = {}
        for k, cls in checkers.items():
            row[k] = hash_obj(vars(cls)[name]) if name in vars(cls) else "-"
        present = [h for h in row.values() if h != "-"]
        verdict = (
            "MATCH"
            if len(set(present)) == 1 and len(present) > 1
            else ("SOLO " if len(present) == 1 else "DIFF")
        )
        print(f"{verdict:5} {name:40} {row}")

    print("\n== DEFAULT_THRESHOLDS subkeys ==")
    all_keys = set()
    for mod in mods.values():
        all_keys |= set(mod.DEFAULT_THRESHOLDS.keys())
    for key in sorted(all_keys):
        row = {}
        for k, mod in mods.items():
            row[k] = hash_obj(mod.DEFAULT_THRESHOLDS[key]) if key in mod.DEFAULT_THRESHOLDS else "-"
        present = [h for h in row.values() if h != "-"]
        verdict = (
            "MATCH"
            if len(set(present)) == 1 and len(present) > 1
            else ("SOLO " if len(present) == 1 else "DIFF")
        )
        print(f"{verdict:5} {key:28} {row}")


if __name__ == "__main__":
    main()
