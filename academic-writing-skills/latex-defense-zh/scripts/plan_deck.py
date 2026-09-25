#!/usr/bin/env python3
"""
Plan skeleton for latex-defense-zh: inventory.json -> slide_plan.yaml.

The script maps each thesis chapter to its page roles with the time budget of
defense_budget.py, picks candidate figures, tables, and equations for each page,
and writes the placeholder 〔待填写〕 into every text field. --outline prints one
line per frame so that the takeaway sentences can be read in page order.

Field details: references/plan-schema.md.

Usage:
    uv run python -B $SKILL_DIR/scripts/plan_deck.py --inventory inventory.json \
        --out slide_plan.yaml [--minutes 40] [--stage predefense|defense] \
        [--theme yanshan|generic]
    uv run python -B $SKILL_DIR/scripts/plan_deck.py --plan slide_plan.yaml --outline

Exit codes: 0 success; 2 argument or input error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

try:
    import defense_budget
    import tex_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import defense_budget
    import tex_loader

PLACEHOLDER = "〔待填写〕"
THEMES = ("yanshan", "generic")
NON_CONTENT_ROLES = ("cover", "toc", "thanks", "backup")
FIGURE_ROLES = (
    "background",
    "status",
    "organization",
    "foundation",
    "intro",
    "problem",
    "method",
    "experiment",
    "architecture",
    "application",
)
INTRO_KEYWORDS = {
    "background": re.compile("背景|意义"),
    "status": re.compile("现状|综述|进展"),
    "challenges": re.compile("问题|挑战"),
    "organization": re.compile("内容|安排|组织"),
}
ARCHITECTURE_RE = re.compile("架构|总体|框架|结构")
# longtable and xltabular do not compile inside \adjustbox (build_deck.py rejects them too).
LONG_TABLE_RE = re.compile(r"\\begin\s*\{(?:longtable|xltabular)\}")
CONCLUSION_SUBSECTIONS = {
    "innovation": "01　主要创新点",
    "outlook": "02　未来研究展望",
    "achievements": "03　攻读学位期间取得的成果",
}
THANKS_SAY = "汇报完毕，请各位老师批评指正。"
OUTLINE_LABELS = {"cover": "封面", "toc": "目录", "thanks": "致谢"}


class PlanError(Exception):
    """Input error (exit code 2)."""


def read_json(path: Path) -> tuple[dict, bytes]:
    try:
        data = path.read_bytes()
        return json.loads(tex_loader.read_text_robust(path)[0]), data
    except (OSError, ValueError) as exc:
        raise PlanError(f"无法读取清单 {path}：{exc}") from exc


def split_even(count: int, parts: int) -> list[int]:
    """Sizes of ``parts`` contiguous groups that cover ``count`` items; larger groups first."""
    base, extra = divmod(count, parts)
    return [base + (1 if index < extra else 0) for index in range(parts)]


def entry_label(entry: dict) -> str:
    return f"{entry['number']} {entry.get('short_title') or entry['title']}"


def chapter_title(chapter: dict) -> str:
    return chapter.get("short_title") or chapter["title"]


@dataclass
class Scope:
    """The sections (and optionally subsections) that one page covers."""

    sections: list[dict]
    subsections: list[dict] | None = None

    def contains(self, item: dict) -> bool:
        if item.get("section") not in {section["number"] for section in self.sections}:
            return False
        if self.subsections is None or item.get("subsection") is None:
            return True
        return item["subsection"] in {sub["number"] for sub in self.subsections}

    def labels(self) -> list[str]:
        return [entry_label(entry) for entry in self.sections + (self.subsections or [])]

    def sources(self) -> list[str]:
        return [entry["source"] for entry in self.sections + (self.subsections or [])]


def distribute(sections: list[dict], pages: int) -> list[Scope]:
    """Map ``pages`` pages onto sections, then onto subsections (C2 design 5.2)."""
    if not sections:
        return [Scope([]) for _ in range(pages)]
    scopes: list[Scope] = []
    if len(sections) >= pages:
        start = 0
        for size in split_even(len(sections), pages):
            scopes.append(Scope(sections[start : start + size]))
            start += size
        return scopes
    for section, count in zip(sections, split_even(pages, len(sections))):
        subsections = section.get("subsections") or []
        if count == 1 or not subsections:
            scopes.extend(Scope([section]) for _ in range(count))
        elif len(subsections) >= count:
            start = 0
            for size in split_even(len(subsections), count):
                scopes.append(Scope([section], subsections[start : start + size]))
                start += size
        else:
            for subsection, repeat in zip(subsections, split_even(count, len(subsections))):
                scopes.extend(Scope([section], [subsection]) for _ in range(repeat))
    return scopes


def chapter_scopes(chapter: dict, plan: defense_budget.ChapterPlan) -> dict[str, list[Scope]]:
    sections = chapter["sections"]
    pages = {item.role: item.pages for item in plan.roles}

    def first(items: list[dict]) -> list[dict]:
        return items[:1]

    def of_kind(kind: str) -> list[dict]:
        return [section for section in sections if section["kind"] == kind]

    if plan.role == "intro":
        return {
            role: distribute(
                first([s for s in sections if INTRO_KEYWORDS[role].search(s["title"])]), count
            )
            for role, count in pages.items()
        }
    if plan.role == "research":
        return {
            "intro": distribute(first(of_kind("intro")), 1),
            "problem": distribute(first(of_kind("problem")), 1),
            "method": distribute(of_kind("method"), pages["method"]),
            "experiment": distribute(of_kind("experiment"), pages["experiment"]),
            "summary": distribute(first(of_kind("summary")), 1),
        }
    if plan.role == "foundation":
        body = [s for s in sections if s["kind"] not in ("intro", "summary")] or sections
        return {"foundation": distribute(body, pages["foundation"])}
    if plan.role == "application":
        body = [s for s in sections if s["kind"] != "summary"]
        intro = next((s for s in body if s["kind"] == "intro"), None)
        architecture = next(
            (s for s in body if s is not intro and ARCHITECTURE_RE.search(s["title"])), None
        )
        if intro is None:
            intro = next((s for s in body if s is not architecture), None)
        rest = [s for s in body if s is not intro and s is not architecture]
        return {
            "intro": distribute([intro] if intro else [], 1),
            "architecture": distribute(
                [architecture] if architecture else [], pages["architecture"]
            ),
            "application": distribute(rest, pages["application"]),
        }
    return {role: distribute([], count) for role, count in pages.items()}


def choose_layout(role: str, figure: dict | None, equation: dict | None, table: dict | None) -> str:
    """Default layout of the page role (defense-framework.md), by candidate availability."""
    if role in ("challenges", "innovation"):
        return "cards"
    if role == "summary":
        return "paper-summary"
    if role == "outlook":
        return "outlook"
    if role in ("method", "foundation"):
        if equation:
            return "equations-figure"
        return "figure-bullets" if figure else "bullets"
    if role in ("experiment", "application"):
        if figure:
            letters = [sub for sub in figure.get("subfigures", []) if sub.get("letter")]
            return "figure-grid" if role == "experiment" and len(letters) >= 2 else "figure"
        return "table" if table else "bullets"
    if role in ("status", "organization", "architecture"):
        return "figure" if figure else "bullets"
    if role in ("background", "problem", "intro"):
        return "figure-bullets" if figure else "bullets"
    return "bullets"


def content_notes(seconds: int) -> dict:
    return {
        "say": PLACEHOLDER,
        "key": PLACEHOLDER,
        "seconds": seconds,
        "transition": PLACEHOLDER,
        "questions": [PLACEHOLDER],
    }


def frame_notes(seconds: int, say: str = PLACEHOLDER, transition: str = PLACEHOLDER) -> dict:
    return {"say": say, "key": "", "seconds": seconds, "transition": transition, "questions": []}


def showable(kind: str, item: dict) -> bool:
    """Figures need an image file; tables need a body that fits in the deck's adjustbox."""
    if kind == "figures":
        return bool(item.get("files"))
    if kind == "tables":
        body = item.get("tabular_source") or ""
        return bool(body) and not LONG_TABLE_RE.match(body)
    return True


class Planner:
    def __init__(self, inventory: dict, roles: list[str]) -> None:
        self.inventory = inventory
        self.used: set[str] = set()
        self.research = [
            chapter for chapter, role in zip(inventory["chapters"], roles) if role == "research"
        ]

    def candidates(self, kind: str, chapter: int, scope: Scope) -> list[dict]:
        return [
            item
            for item in self.inventory.get(kind, [])
            if item.get("chapter") == chapter and scope.contains(item)
        ]

    def first_unused(self, kind: str, chapter: int, scope: Scope) -> dict | None:
        """First candidate not used on an earlier page that the deck can show."""
        return next(
            (
                item
                for item in self.candidates(kind, chapter, scope)
                if item["label"] not in self.used and showable(kind, item)
            ),
            None,
        )

    def hints(self, role: str, chapter: dict, scope: Scope) -> list[str]:
        number = chapter["number"]
        hints = scope.labels()
        if role in FIGURE_ROLES:
            hints += [
                f"图{f['number']} {f['caption']}" for f in self.candidates("figures", number, scope)
            ]
            hints += [
                f"表{t['number']} {t['caption']}" for t in self.candidates("tables", number, scope)
            ]
            hints += [f"式({e['number']})" for e in self.candidates("equations", number, scope)]
        conclusion = self.inventory.get("conclusion") or {}
        research = [
            f"研究内容 {index}：第 {c['number']} 章 {chapter_title(c)}"
            for index, c in enumerate(self.research, 1)
        ]
        if role == "challenges":
            hints += research
        elif role == "innovation":
            hints += research + list(conclusion.get("contributions", []))
        elif role == "outlook":
            hints += list(conclusion.get("outlook", []))
        elif role == "summary":
            papers = [p for p in self.inventory.get("publications", []) if number in p["chapters"]]
            hints += [f"{p['id']} {p['text']}" for p in papers[1:]]
        elif role == "achievements":
            hints += [f"{p['id']} {p['text']}" for p in self.inventory.get("publications", [])]
        return hints

    def frame(
        self, frame_id: str, role: str, chapter: dict, chapter_role: str, scope: Scope, seconds: int
    ) -> dict:
        number = chapter["number"]
        figure = self.first_unused("figures", number, scope) if role in FIGURE_ROLES else None
        table = None
        if role in ("experiment", "application"):
            table = self.first_unused("tables", number, scope)
        equation = None
        if role in ("method", "foundation"):
            equation = self.first_unused("equations", number, scope)
        layout = choose_layout(role, figure, equation, table)

        figures: list[dict] = []
        if figure and layout in ("figure", "figure-bullets", "figure-grid", "equations-figure"):
            entry: dict = {"label": figure["label"]}
            if layout == "figure-grid":
                letters = [s["letter"] for s in figure["subfigures"] if s.get("letter")]
                entry["subfigures"] = letters[:6]
            figures.append(entry)
        equations = (
            [{"label": equation["label"]}] if equation and layout == "equations-figure" else []
        )
        table_label = table["label"] if table and layout == "table" else None
        chosen = [f["label"] for f in figures] + [e["label"] for e in equations]
        chosen += [table_label] if table_label else []
        self.used.update(chosen)

        if role == "intro" and chapter_role == "research":
            index = next(i for i, c in enumerate(self.research, 1) if c["number"] == number)
            subsection = f"研究内容 {index}：{chapter_title(chapter)}"
        elif role in CONCLUSION_SUBSECTIONS:
            subsection = CONCLUSION_SUBSECTIONS[role]
        elif scope.subsections and len(scope.subsections) == 1:
            subsection = entry_label(scope.subsections[0])
        else:
            subsection = ""

        if layout in ("figure", "figure-grid", "table"):
            bullets = []
        elif role in ("challenges", "innovation"):
            bullets = [PLACEHOLDER] * len(self.research)
        elif role == "outlook":
            outlook = (self.inventory.get("conclusion") or {}).get("outlook", [])
            bullets = [PLACEHOLDER] * (min(3, len(outlook)) if outlook else 2)
        else:
            bullets = [PLACEHOLDER]

        paper = None
        if role == "summary":
            paper = next(
                (
                    p["id"]
                    for p in self.inventory.get("publications", [])
                    if number in p["chapters"]
                ),
                None,
            )

        items = {
            item["label"]: item
            for kind in ("figures", "tables", "equations")
            for item in self.inventory.get(kind, [])
        }
        frame: dict = {
            "id": frame_id,
            "role": role,
            "layout": layout,
            "chapter": number,
            "section": entry_label(scope.sections[0]) if scope.sections else chapter_title(chapter),
            "subsection": subsection,
        }
        if layout == "figure-bullets":
            frame["position"] = "top" if role == "intro" and chapter_role == "research" else "left"
        frame.update(
            {
                "takeaway": PLACEHOLDER,
                "bullets": bullets,
                "figures": figures,
                "equations": equations,
                "table": table_label,
                "paper": paper,
                "notes": content_notes(seconds),
                "source": scope.sources() + [items[label]["source"] for label in chosen],
                "hints": self.hints(role, chapter, scope),
            }
        )
        return frame


def build_plan(inventory: dict, minutes: int, stage: str, theme: str, digest: str) -> dict:
    chapters = inventory.get("chapters") or []
    roles = [chapter.get("role") or chapter.get("role_suggestion") for chapter in chapters]
    try:
        budget = defense_budget.compute_budget(roles, minutes, stage)
    except ValueError as exc:
        raise PlanError(f"{exc}；可在 inventory.json 的章条目中加 role 字段指定章角色") from exc
    planner = Planner(inventory, roles)
    fixed = defense_budget.FIXED_SECONDS
    frames: list[dict] = [
        {
            "id": "cover",
            "role": "cover",
            "layout": "cover",
            "chapter": None,
            "notes": frame_notes(fixed["cover"]),
        },
        {
            "id": "toc",
            "role": "toc",
            "layout": "toc",
            "chapter": 0,
            "notes": frame_notes(fixed["toc"]),
        },
    ]
    for chapter, plan in zip(chapters, budget.chapters):
        number = chapter["number"]
        if number > 1:
            frames.append(
                {
                    "id": f"c{number}-toc",
                    "role": "toc",
                    "layout": "toc",
                    "chapter": number,
                    "notes": frame_notes(fixed["chapter_toc"]),
                }
            )
        scopes = chapter_scopes(chapter, plan)
        for item in plan.roles:
            for index, scope in enumerate(scopes[item.role], 1):
                frame_id = f"c{number}-{item.role}"
                if item.pages > 1:
                    frame_id += f"-{index}"
                frames.append(
                    planner.frame(
                        frame_id, item.role, chapter, plan.role, scope, item.seconds_per_page
                    )
                )
    frames.append(
        {
            "id": "thanks",
            "role": "thanks",
            "layout": "thanks",
            "chapter": None,
            "notes": frame_notes(fixed["thanks"], say=THANKS_SAY, transition=""),
        }
    )
    meta = inventory.get("meta") or {}
    return {
        "meta": {
            "stage": stage,
            "theme": theme,
            "minutes": minutes,
            "title_lines": list(meta.get("title_lines") or []),
            "author": meta.get("author", ""),
            "supervisor": meta.get("supervisor", ""),
            "supervisor_title": meta.get("supervisor_title", ""),
            "subject": meta.get("subject", ""),
            "school": meta.get("school", ""),
            "date": meta.get("date", ""),
            "logo": inventory.get("logo"),
            "inventory_sha256": digest,
            "extra_packages": [],
            "chapters": [
                {"number": c["number"], "title": chapter_title(c), "role": role}
                for c, role in zip(chapters, roles)
            ],
        },
        "frames": frames,
    }


def count_placeholders(value: object) -> int:
    if isinstance(value, str):
        return value.count(PLACEHOLDER)
    if isinstance(value, dict):
        return sum(count_placeholders(item) for item in value.values())
    if isinstance(value, list):
        return sum(count_placeholders(item) for item in value)
    return 0


def load_plan(path: Path) -> dict:
    try:
        plan = yaml.safe_load(tex_loader.read_text_robust(path)[0])
    except (OSError, yaml.YAMLError) as exc:
        raise PlanError(f"无法读取规划 {path}：{exc}") from exc
    frames = plan.get("frames") if isinstance(plan, dict) else None
    if not isinstance(frames, list) or not frames:
        raise PlanError("规划缺少 frames 列表")
    for index, frame in enumerate(frames, 1):
        if not isinstance(frame, dict) or not frame.get("id") or not frame.get("role"):
            raise PlanError(f"第 {index} 帧缺少 id 或 role")
    return plan


def outline(plan: dict) -> list[str]:
    lines = []
    frames = plan["frames"]
    for index, frame in enumerate(frames, 1):
        title = frame.get("section") or OUTLINE_LABELS.get(frame["role"], "")
        if frame["role"] == "toc" and frame.get("chapter"):
            title = f"第 {frame['chapter']} 章目录"
        lines.append(f"{index}  {frame['id']}  {title} | {frame.get('takeaway') or ''}")
    content = sum(1 for frame in frames if frame["role"] not in NON_CONTENT_ROLES)
    lines.append(f"帧数 {len(frames)}，内容页数 {content}，占位符 {count_placeholders(plan)}")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="由清单生成答辩稿规划骨架（slide_plan.yaml），或按页序输出规划大纲。"
    )
    parser.add_argument("--inventory", help="extract_thesis.py 输出的 inventory.json")
    parser.add_argument("--out", help="输出的 slide_plan.yaml 路径")
    parser.add_argument("--minutes", type=int, default=40, help="汇报分钟数（默认 40，范围 15–90）")
    parser.add_argument("--stage", choices=defense_budget.STAGES, default="predefense", help="阶段")
    parser.add_argument("--theme", choices=THEMES, default="yanshan", help="主题")
    parser.add_argument("--plan", help="已有的 slide_plan.yaml（与 --outline 同用）")
    parser.add_argument("--outline", action="store_true", help="按页序输出帧标题与结论句")
    args = parser.parse_args(argv)

    try:
        if args.outline:
            if not args.plan:
                parser.error("--outline 需要 --plan")
            for line in outline(load_plan(Path(args.plan))):
                print(line)
            return 0
        if not args.inventory or not args.out:
            parser.error("生成骨架需要 --inventory 与 --out")
        inventory, data = read_json(Path(args.inventory))
        digest = hashlib.sha256(data).hexdigest()
        plan = build_plan(inventory, args.minutes, args.stage, args.theme, digest)
    except PlanError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(plan, allow_unicode=True, sort_keys=False, width=1000)
    out.write_text(text, encoding="utf-8")
    content = sum(1 for frame in plan["frames"] if frame["role"] not in NON_CONTENT_ROLES)
    print(
        f"已写入 {out}：帧数 {len(plan['frames'])}，内容页数 {content}，"
        f"占位符 {count_placeholders(plan)}"
    )
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
