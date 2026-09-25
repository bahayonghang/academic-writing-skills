#!/usr/bin/env python3
"""
Time budget for latex-defense-zh: presentation minutes -> page counts and seconds.

Implements the formula in references/time-budget.md. plan_deck.py and the
quality gate share this module.

Usage:
    uv run python -B $SKILL_DIR/scripts/defense_budget.py \
        --roles intro,foundation,research,research,research,application,conclusion \
        [--minutes 40] [--stage predefense|defense]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass

CHAPTER_ROLES = ("intro", "foundation", "research", "application", "conclusion")
STAGES = ("predefense", "defense")
MIN_MINUTES = 15
MAX_MINUTES = 90

# Seconds of the fixed frames. The fixed segment does not scale with the duration.
FIXED_SECONDS = {"cover": 30, "toc": 20, "chapter_toc": 8, "thanks": 10}
# 40-minute subtotal in seconds of each non-research chapter segment.
SEGMENT_SECONDS = {"intro": 300, "foundation": 150, "application": 180, "conclusion": 135}
DEFENSE_CONCLUSION_SECONDS = 180
# 40-minute base page count of the roles that scale with the duration.
SCALED_BASE = {"background": 2, "status": 2, "foundation": 3, "architecture": 1, "application": 2}
SECONDS_PER_RESEARCH_PAGE = 53
MIN_RESEARCH_PAGES = 6


def round_half_up(value: float) -> int:
    """r(x) = floor(x + 0.5). Python round() uses banker's rounding, so it is not used."""
    return math.floor(value + 0.5)


@dataclass(frozen=True)
class RolePages:
    role: str
    pages: int
    seconds_per_page: int


@dataclass(frozen=True)
class ChapterPlan:
    number: int
    role: str  # intro | foundation | research | application | conclusion
    roles: list[RolePages]


@dataclass(frozen=True)
class Budget:
    minutes: int
    stage: str
    chapters: list[ChapterPlan]
    content_pages: int  # N, without cover, TOC pages, and thanks
    page_range: tuple[int, int]  # (r(0.85N), r(1.15N))
    total_frames: int


def _validate(chapter_roles: list[str], minutes: int, stage: str) -> None:
    if stage not in STAGES:
        raise ValueError(f"阶段必须为 {' 或 '.join(STAGES)}：{stage}")
    if not MIN_MINUTES <= minutes <= MAX_MINUTES:
        raise ValueError(f"汇报时长必须在 {MIN_MINUTES}–{MAX_MINUTES} 分钟之间：{minutes}")
    unknown = [role for role in chapter_roles if role not in CHAPTER_ROLES]
    if unknown:
        raise ValueError(f"未知章角色：{', '.join(unknown)}")
    if len(chapter_roles) < 2 or chapter_roles[0] != "intro" or chapter_roles[-1] != "conclusion":
        raise ValueError("第 1 章必须为 intro，最后一章必须为 conclusion")
    if "research" not in chapter_roles:
        raise ValueError("至少需要一个 research 章")


def compute_budget(
    chapter_roles: list[str], minutes: int = 40, stage: str = "predefense"
) -> Budget:
    """Return the page count and seconds per page of each page role, chapter by chapter."""
    _validate(chapter_roles, minutes, stage)
    k = minutes / 40

    def scaled(role: str) -> int:
        return max(1, round_half_up(SCALED_BASE[role] * k))

    sequences = {
        "intro": [
            ("background", scaled("background")),
            ("status", scaled("status")),
            ("challenges", 1),
            ("organization", 1),
        ],
        "foundation": [("foundation", scaled("foundation"))],
        "application": [
            ("intro", 1),
            ("architecture", scaled("architecture")),
            ("application", scaled("application")),
        ],
        "conclusion": [("innovation", 1), ("outlook", 1)]
        + ([("achievements", 1)] if stage == "defense" else []),
    }
    segment_seconds = dict(SEGMENT_SECONDS)
    if stage == "defense":
        segment_seconds["conclusion"] = DEFENSE_CONCLUSION_SECONDS

    fixed = (
        FIXED_SECONDS["cover"]
        + FIXED_SECONDS["toc"]
        + FIXED_SECONDS["chapter_toc"] * (len(chapter_roles) - 1)
        + FIXED_SECONDS["thanks"]
    )
    remainder = 60 * minutes - fixed
    remainder -= sum(segment_seconds[role] * k for role in chapter_roles if role != "research")
    per_chapter = remainder / chapter_roles.count("research")
    pages = max(MIN_RESEARCH_PAGES, round_half_up(per_chapter / SECONDS_PER_RESEARCH_PAGE))
    method = max(2, round_half_up((pages - 3) * 3 / 7))
    experiment = max(1, pages - 3 - method)

    chapters: list[ChapterPlan] = []
    for number, role in enumerate(chapter_roles, 1):
        if role == "research":
            counts = [
                ("intro", 1),
                ("problem", 1),
                ("method", method),
                ("experiment", experiment),
                ("summary", 1),
            ]
            seconds = round_half_up(per_chapter / pages)
        else:
            counts = sequences[role]
            seconds = round_half_up(segment_seconds[role] * k / sum(n for _, n in counts))
        chapters.append(
            ChapterPlan(number, role, [RolePages(name, n, seconds) for name, n in counts])
        )

    content = sum(item.pages for chapter in chapters for item in chapter.roles)
    return Budget(
        minutes=minutes,
        stage=stage,
        chapters=chapters,
        content_pages=content,
        page_range=(round_half_up(0.85 * content), round_half_up(1.15 * content)),
        total_frames=content + len(chapter_roles) + 2,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="按 references/time-budget.md 的公式计算各章各页角色的页数与每页秒数。"
    )
    parser.add_argument(
        "--roles",
        required=True,
        help="逗号分隔的章角色序列，例如 intro,foundation,research,application,conclusion",
    )
    parser.add_argument("--minutes", type=int, default=40, help="汇报时长（分钟），默认 40")
    parser.add_argument("--stage", choices=STAGES, default="predefense", help="答辩阶段")
    args = parser.parse_args(argv)

    roles = [role.strip() for role in args.roles.split(",") if role.strip()]
    try:
        budget = compute_budget(roles, args.minutes, args.stage)
    except ValueError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    print(json.dumps(asdict(budget), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
