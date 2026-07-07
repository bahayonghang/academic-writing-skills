"""Probe 3: classify remaining DIFF members (en vs typst, zh vs typst)."""

from __future__ import annotations

import ast
import difflib
import hashlib
import inspect
import pprint
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_alignment import COPIES, load  # noqa: E402


def logic_hash(obj) -> str:
    """AST hash with docstrings stripped — insensitive to comments/docs/formatting."""
    src = inspect.getsource(obj)
    tree = ast.parse(src.strip() and __import__("textwrap").dedent(src))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            body = getattr(node, "body", [])
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                node.body = body[1:] or [ast.Pass()]
    return hashlib.md5(ast.dump(tree).encode()).hexdigest()[:8]


def src_lines(obj) -> list[str]:
    if inspect.isfunction(obj) or inspect.isclass(obj):
        return inspect.getsource(obj).splitlines()
    return pprint.pformat(obj, width=100).splitlines()


def show(title, a_key, a, b_key, b, n=140):
    print(f"\n{'=' * 16} {title}: {a_key} vs {b_key} {'=' * 16}")
    lines = list(
        difflib.unified_diff(
            src_lines(a), src_lines(b), fromfile=a_key, tofile=b_key, lineterm="", n=1
        )
    )
    for line in lines[:n]:
        print(line)
    if len(lines) > n:
        print(f"... ({len(lines) - n} more)")


def main() -> None:
    mods = {k: load(k, p) for k, p in COPIES.items()}
    en, zh, ty = mods["en"], mods["zh"], mods["typst"]
    en_c, zh_c, ty_c = en.AITraceChecker, zh.ChineseAITraceChecker, ty.AITraceChecker

    undecided = [
        "_check_low_information_density",
        "_check_punctuation",
        "_check_sentence_length_variance",
        "_check_term_threshold",
        "_get_instruction",
        "_is_false_positive",
        "_iter_section_paragraphs",
        "check_section",
        "generate_report",
    ]
    print("== logic-hash (docstring-stripped AST) for checker methods ==")
    names = set()
    for cls in (en_c, zh_c, ty_c):
        names |= {
            n for n, v in vars(cls).items() if inspect.isfunction(v) and not n.startswith("__")
        }
    for name in sorted(names):
        row = {}
        for key, cls in (("en", en_c), ("zh", zh_c), ("typst", ty_c)):
            row[key] = logic_hash(vars(cls)[name]) if name in vars(cls) else "-"
        present = [h for h in row.values() if h != "-"]
        verdict = (
            "MATCH"
            if len(set(present)) == 1 and len(present) > 1
            else ("SOLO " if len(present) == 1 else "DIFF")
        )
        print(f"{verdict:5} {name:40} {row}")

    print("\n== logic-hash for top-level funcs ==")
    for name in ("_apply_tier", "_load_thresholds", "main"):
        row = {k: logic_hash(getattr(m, name)) for k, m in mods.items()}
        print(f"{name:20} {row}")

    for name in undecided:
        show(name, "en", vars(en_c)[name], "typst", vars(ty_c)[name])

    show(
        "_check_burstiness",
        "zh",
        vars(zh_c)["_check_burstiness"],
        "typst",
        vars(ty_c)["_check_burstiness"],
    )

    print("\n== TEACHING_NOTES keys ==")
    for k, m in mods.items():
        print(f"{k}: {sorted(m.TEACHING_NOTES.keys())}")
    print("\n== term_thresholds keys ==")
    for k, m in mods.items():
        print(f"{k}: {sorted(m.DEFAULT_THRESHOLDS['term_thresholds'].keys())}")
    print("\n== throat_clearing cfg ==")
    for k, m in mods.items():
        print(f"{k}: {m.DEFAULT_THRESHOLDS['throat_clearing']}")
    print("\n== tense patterns contain presents? ==")
    for k, m in mods.items():
        pats = m.DEFAULT_THRESHOLDS["tense"]["patterns"]
        print(f"{k}: n={len(pats)}; presents entries: {[p for p in pats if 'presents' in str(p)]}")


if __name__ == "__main__":
    main()
