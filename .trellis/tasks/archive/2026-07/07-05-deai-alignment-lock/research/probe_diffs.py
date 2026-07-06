"""Probe 2: print unified diffs for members flagged DIFF by probe_alignment.py."""

from __future__ import annotations

import difflib
import inspect
import pprint
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe_alignment import COPIES, load  # noqa: E402


def src(obj) -> list[str]:
    if inspect.isfunction(obj) or inspect.isclass(obj):
        return inspect.getsource(obj).splitlines()
    return pprint.pformat(obj, width=100).splitlines()


def show(title: str, a_key: str, a, b_key: str, b) -> None:
    print(f"\n{'=' * 20} {title}: {a_key} vs {b_key} {'=' * 20}")
    diff = difflib.unified_diff(src(a), src(b), fromfile=a_key, tofile=b_key, lineterm="", n=1)
    lines = list(diff)
    if not lines:
        print("(identical)")
    for line in lines[:120]:
        print(line)
    if len(lines) > 120:
        print(f"... ({len(lines) - 120} more diff lines)")


def main() -> None:
    mods = {k: load(k, p) for k, p in COPIES.items()}
    en, zh, ty = mods["en"], mods["zh"], mods["typst"]
    en_c, zh_c, ty_c = en.AITraceChecker, zh.ChineseAITraceChecker, ty.AITraceChecker

    show("_apply_tier", "en", en._apply_tier, "zh", zh._apply_tier)
    show("DIMENSION_MAP", "en", en.DIMENSION_MAP, "zh", zh.DIMENSION_MAP)
    show(
        "_check_overclaim",
        "en",
        vars(en_c)["_check_overclaim"],
        "zh",
        vars(zh_c)["_check_overclaim"],
    )
    show(
        "_iter_visible_lines",
        "en",
        vars(en_c)["_iter_visible_lines"],
        "zh",
        vars(zh_c)["_iter_visible_lines"],
    )
    show(
        "_check_burstiness",
        "en",
        vars(en_c)["_check_burstiness"],
        "typst",
        vars(ty_c)["_check_burstiness"],
    )
    show("_check_tense", "en", vars(en_c)["_check_tense"], "typst", vars(ty_c)["_check_tense"])
    show("_load_thresholds", "en", en._load_thresholds, "typst", ty._load_thresholds)
    show(
        "burstiness thresholds",
        "en",
        en.DEFAULT_THRESHOLDS["burstiness"],
        "typst",
        ty.DEFAULT_THRESHOLDS["burstiness"],
    )
    show(
        "burstiness thresholds",
        "en",
        en.DEFAULT_THRESHOLDS["burstiness"],
        "zh",
        zh.DEFAULT_THRESHOLDS["burstiness"],
    )


if __name__ == "__main__":
    main()
