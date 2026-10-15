#!/usr/bin/env python3
"""
Read thesis review reports and start the rebuttal ledger (latex-thesis-zh).

The script reads every review report (PDF with a text layer, TXT, or MD) in the
review directory, removes repeated watermark and footer lines, splits the
academic comments from the numbered shortcomings, and parses the total score,
the overall grade, and the defense decision. It creates two sibling directories
of the review directory: responses/ (paste-ready Markdown, written later by
rebuttal_build.py) and workspace/ (intermediate files). It writes
workspace/reviews/R<n>.md, workspace/rebuttal_state.json, and, when absent,
the ledger skeleton workspace/concerns.yaml. The review directory and the
thesis repository are read only.

Contract: references/rebuttal-workflow.md.

Usage:
    uv run python -B $SKILL_DIR/scripts/rebuttal_intake.py --reviews DIR [--thesis DIR] \
        [--main FILE] [--root DIR] [--stage pre-review|final-review|predefense|other] \
        [--form-title TEXT] [--order FILE,FILE,...] [--base-commit SHA] [--force] [--json]

Exit codes: 0 success (warnings allowed); 2 input error; 3 a PDF needs PyMuPDF
and PyMuPDF is not installed; 4 workspace/reviews/ exists and --force is not set.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

try:
    import rebuttal_common
    import tex_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import rebuttal_common
    import tex_loader

try:
    import pymupdf as _pymupdf_module

    _PYMUPDF_AVAILABLE = True
except ImportError:
    _pymupdf_module = None  # type: ignore[assignment]
    _PYMUPDF_AVAILABLE = False

SUPPORTED_SUFFIXES = (".pdf", ".txt", ".md")
BLOCKED_SUFFIXES = (".docx", ".doc", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp")
STAGES = ("pre-review", "final-review", "predefense", "other")
FORM_TITLES = {
    "pre-review": "博士学位论文预评审评阅意见修改审查表",
    "final-review": "学位论文评阅意见修改说明",
    "predefense": "学位论文预答辩意见修改说明",
    "other": "学位论文评阅意见修改说明",
}
PRAISE_HEADINGS = ("对学位论文的学术评语", "学术评语", "评阅意见")
ISSUE_HEADINGS = (
    "论文的不足之处和建议",
    "不足之处和建议",
    "存在的不足",
    "主要问题",
    "修改意见",
    "问题与建议",
)
MIN_TEXT_CHARS = 50
MISSING_PYMUPDF = "缺少 PyMuPDF：运行 `uv pip install pymupdf` 后重试，或把评阅书导出为 TXT"

PAGE_FOOTER_RE = re.compile(r"第\s*\d+\s*页\s*$")
PAGE_NUMBER_RE = re.compile(r"^\d{1,3}$")
HEADER_LINE_RE = re.compile(r"^(?:论文编号|论文题目|学号|作者姓名)\s*[:：]")
ITEM_RE = re.compile(r"^\s*(?:(\d+)\s*[.．](?!\d)|(\d+)\s*[、)）]|[（(]\s*(\d+)\s*[)）])\s*")
ORDER_NUMBER_RE = re.compile(r"(?:评阅书|评阅意见|评审意见|评审书)\s*(\d+)")
TOTAL_RE = re.compile(r"总分\s*[:：]?\s*(\d{1,3})")
GRADE_RE = re.compile(r"总体评价\s*[:：]?\s*([A-E])(?![A-Za-z])")
AGREE_RE = re.compile(r"是否同意答辩\s*[:：]?\s*(\S+)")
REVIEW_FILE_RE = re.compile(r"R\d+\.md")


class IntakeError(Exception):
    """Input error (exit code 2)."""


@dataclass
class Review:
    id: str
    path: Path
    pages: list[str]
    text_layer: bool = True
    total_score: int | None = None
    grade: str | None = None
    agree_defense: str | None = None
    praise: str = ""
    items: list[str] = field(default_factory=list)


@dataclass
class Warnings:
    items: list[dict[str, str]] = field(default_factory=list)

    def add(self, code: str, message: str, source: str | None = None) -> None:
        entry = {"code": code, "message": message}
        if source:
            entry["source"] = source
        self.items.append(entry)


# ---------------------------------------------------------------------------
# Input files
# ---------------------------------------------------------------------------


def _inside(path: Path, other: Path) -> bool:
    return path == other or other in path.parents


def resolve_layout(reviews: Path, root_arg: str | None) -> tuple[Path, Path, Path]:
    """Return (root, responses, workspace); refuse layouts that write into the reviews."""
    if not reviews.is_dir():
        raise IntakeError(f"评阅书目录不存在：{reviews}")
    reviews = reviews.resolve()
    root = Path(root_arg).resolve() if root_arg else reviews.parent
    responses = root / "responses"
    workspace = root / "workspace"
    for output in (responses, workspace):
        if _inside(reviews, output) or _inside(output, reviews):
            raise IntakeError(f"评阅书目录与输出目录 {output} 相同或嵌套；请改用 --root")
    return root, responses, workspace


def order_key(path: Path) -> tuple[int, int, str]:
    match = ORDER_NUMBER_RE.search(path.stem)
    if match:
        return (0, int(match.group(1)), path.name)
    numbers = re.findall(r"\d+", path.stem)
    if numbers:
        return (1, int(numbers[-1]), path.name)
    return (2, 0, path.name)


def list_review_files(reviews: Path, order: str | None, warnings: Warnings) -> list[Path]:
    files = sorted((path for path in reviews.iterdir() if path.is_file()), key=lambda p: p.name)
    blocked = [path.name for path in files if path.suffix.lower() in BLOCKED_SUFFIXES]
    if blocked:
        raise IntakeError(f"不支持的评阅书格式：{'、'.join(blocked)}；请导出为 PDF 或 TXT")
    supported = [path for path in files if path.suffix.lower() in SUPPORTED_SUFFIXES]
    for path in files:
        if path not in supported:
            warnings.add("W-SKIP-FILE", f"忽略非评阅书文件 {path.name}")
    if not supported:
        raise IntakeError(f"{reviews} 中没有 PDF、TXT 或 MD 评阅书")
    kept: dict[str, Path] = {}
    for path in sorted(supported, key=lambda p: SUPPORTED_SUFFIXES[::-1].index(p.suffix.lower())):
        same = kept.setdefault(path.stem, path)
        if same is not path:
            warnings.add("W-SKIP-FILE", f"忽略 {path.name}：同名评阅书已读取 {same.name}")
    supported = [path for path in supported if path in kept.values()]
    if order:
        names = [name.strip() for name in order.split(",") if name.strip()]
        by_name = {path.name: path for path in supported}
        if sorted(names) != sorted(by_name):
            raise IntakeError(f"--order 须恰好列出全部评阅书文件：{'、'.join(sorted(by_name))}")
        return [by_name[name] for name in names]
    return sorted(supported, key=order_key)


def read_pages(path: Path) -> list[str]:
    if path.suffix.lower() == ".pdf":
        try:
            document = _pymupdf_module.open(path)  # type: ignore[union-attr]
        except Exception as exc:  # PyMuPDF raises several error types for a bad file
            raise IntakeError(f"无法打开 PDF {path.name}：{exc}") from exc
        with document:
            return [cast(str, page.get_text("text", sort=True)) for page in document]
    text = tex_loader.read_text_robust(path)[0]
    return text.split("\f")


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------


def join_lines(lines: list[str]) -> str:
    """Join wrapped lines: no separator between CJK text, one space between ASCII words."""
    text = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if text and (text[-1] + line[0]).isascii() and (text[-1] + line[0]).isalnum():
            text += " "
        text += line
    return text


def clean_pages(pages: list[str]) -> list[str]:
    """Drop repeated watermark/header lines, page footers, page numbers, and header fields."""
    page_lines = [[line.strip() for line in page.splitlines()] for page in pages]
    repeated: set[str] = set()
    if len(page_lines) > 1:
        threshold = max(2, math.ceil(2 * len(page_lines) / 3))
        counts: dict[str, int] = {}
        for lines in page_lines:
            for line in {line for line in lines if line}:
                counts[line] = counts.get(line, 0) + 1
        repeated = {line for line, count in counts.items() if count >= threshold}
    kept: list[str] = []
    for lines in page_lines:
        for line in lines:
            if not line or line in repeated:
                continue
            if PAGE_FOOTER_RE.search(line):
                continue
            # A lone number is a page number unless it is the value of a score label.
            if PAGE_NUMBER_RE.fullmatch(line) and not (kept and kept[-1].endswith("总分")):
                continue
            if HEADER_LINE_RE.match(line):
                continue
            kept.append(line)
    return kept


def _heading(line: str, headings: tuple[str, ...]) -> bool:
    compact = re.sub(r"\s+", "", line).lstrip("#").rstrip(":：")
    return compact in headings


def split_items(lines: list[str]) -> tuple[str, list[str]]:
    """Return (text before item 1, numbered items); a number counts only when it is the next one."""
    preamble: list[str] = []
    items: list[list[str]] = []
    for line in lines:
        match = ITEM_RE.match(line)
        if match:
            number = int(next(group for group in match.groups() if group))
            if number == len(items) + 1:
                items.append([line[match.end() :]])
                continue
        (items[-1] if items else preamble).append(line)
    return join_lines(preamble), [join_lines(item) for item in items]


def parse_review(review: Review, warnings: Warnings) -> None:
    source = review.path.name
    if review.path.suffix.lower() == ".pdf":
        chars = [len(re.sub(r"\s+", "", page)) for page in review.pages]
        if not chars or all(count < MIN_TEXT_CHARS for count in chars):
            review.text_layer = False
            warnings.add(
                "W-NO-TEXT", "PDF 没有文字层，生成空骨架；请提供 TXT 或由 LLM 读图后填写", source
            )
            return
    lines = clean_pages(review.pages)
    full = "\n".join(lines)
    total = TOTAL_RE.search(full)
    grade = GRADE_RE.search(full)
    agree = AGREE_RE.search(full)
    review.total_score = int(total.group(1)) if total else None
    review.grade = grade.group(1) if grade else None
    review.agree_defense = agree.group(1) if agree else None
    for name, value in (("总分", total), ("总体评价", grade), ("是否同意答辩", agree)):
        if value is None:
            warnings.add("W-NO-SCORE", f"未解析到「{name}」", source)

    praise_at = next((i for i, line in enumerate(lines) if _heading(line, PRAISE_HEADINGS)), None)
    issue_at = next((i for i, line in enumerate(lines) if _heading(line, ISSUE_HEADINGS)), None)
    if praise_at is not None:
        end = issue_at if issue_at is not None and issue_at > praise_at else len(lines)
        review.praise = join_lines(lines[praise_at + 1 : end])
    if issue_at is None:
        warnings.add(
            "W-NO-SECTION", "未找到「不足之处和建议」标题，全文按一节切分，请 LLM 复核", source
        )
        start = praise_at + 1 if praise_at is not None else 0
        issue_lines = lines[start:]
    else:
        issue_lines = lines[issue_at + 1 :]
    preamble, review.items = split_items(issue_lines)
    if not review.items and preamble:
        warnings.add("W-NO-NUMBER", "不足之处没有编号，整节记为第 1 条，请 LLM 切分", source)
        review.items = [preamble]
    elif preamble:
        warnings.add("W-UNNUMBERED", f"编号前的文字未入台账：{preamble[:40]}", source)


# ---------------------------------------------------------------------------
# Anchors and outputs
# ---------------------------------------------------------------------------


def map_anchor(
    anchor: rebuttal_common.Anchor,
    labels: dict[str, rebuttal_common.AuxLabel] | None,
    cites: dict[str, str] | None,
    warnings: Warnings,
    source: str,
) -> dict[str, object]:
    entry: dict[str, object] = {
        "text": anchor.text,
        "kind": anchor.kind,
        "label": None,
        "base_number": anchor.key,
        "base_page": None,
    }
    if labels is None or cites is None:
        return entry
    if anchor.kind == "reference":
        entry["label"] = cites.get(anchor.key)
    else:
        matches = [
            label
            for label in labels.values()
            if label.kind == anchor.kind and label.number == anchor.key
        ]
        if len(matches) > 1:
            names = "、".join(label.label for label in matches)
            warnings.add(
                "W-ANCHOR-AMBIGUOUS", f"{anchor.text} 对应多个标签：{names}，取第一个", source
            )
        if matches:
            entry["label"] = matches[0].label
            page = matches[0].page
            entry["base_page"] = int(page) if page.isdigit() else page or None
    if entry["label"] is None:
        target = f"{anchor.text}（{anchor.kind} {anchor.key}）"
        warnings.add("W-ANCHOR-MISSING", f"{target} 在论文 aux 中找不到对应标签", source)
    return entry


def review_markdown(review: Review) -> str:
    def value(item: object) -> str:
        return "未解析" if item is None else str(item)

    parts = [
        f"# {review.id} {review.path.name}",
        "",
        "## 评分",
        f"总分：{value(review.total_score)}",
        f"总体评价：{value(review.grade)}",
        f"是否同意答辩：{value(review.agree_defense)}",
        "",
        "## 学术评语",
        review.praise or "（无）",
        "",
        "## 不足之处和建议",
    ]
    parts += [f"{index}. {item}" for index, item in enumerate(review.items, 1)] or ["（无）"]
    return "\n".join(parts) + "\n"


def build_ledger(
    reviews: list[Review],
    labels: dict[str, rebuttal_common.AuxLabel] | None,
    cites: dict[str, str] | None,
    warnings: Warnings,
) -> dict:
    concerns = []
    for review in reviews:
        for index, item in enumerate(review.items, 1):
            anchors = [
                map_anchor(anchor, labels, cites, warnings, review.path.name)
                for anchor in rebuttal_common.find_anchors(item)
            ]
            concerns.append(
                {
                    "id": f"{review.id}-{index}",
                    "reviewer": review.id,
                    "item": index,
                    "quote": item,
                    "quote_short": None,
                    "category": None,
                    "severity": None,
                    "priority": None,
                    "shared_with": [],
                    "anchors": anchors,
                    "action": None,
                    "status": "open",
                    "owner": None,
                    "plan": "",
                    "response": "",
                    "locations": [],
                    "evidence": {"kind": "none", "files": [], "note": ""},
                    "source": "[Script]",
                }
            )
    return {
        "schema": rebuttal_common.LEDGER_SCHEMA,
        "reviewers": [
            {
                "id": review.id,
                "total_score": review.total_score,
                "grade": review.grade,
                "agree_defense": review.agree_defense,
                "praise": review.praise,
            }
            for review in reviews
        ],
        "concerns": concerns,
    }


def missing_ledger_items(ledger: dict, reviews: list[Review]) -> list[str]:
    present = {
        (concern.get("reviewer"), concern.get("item"))
        for concern in ledger.get("concerns") or []
        if isinstance(concern, dict)
    }
    return [
        f"{review.id}-{index}"
        for review in reviews
        for index in range(1, len(review.items) + 1)
        if (review.id, index) not in present
    ]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "读取学位论文评阅书，在评阅书目录同级创建 responses/ 与 workspace/，"
            "写入归一化评阅原文、状态文件与意见台账骨架；评阅书与论文仓库只读。"
        )
    )
    parser.add_argument("--reviews", required=True, help="评阅书目录（PDF、TXT 或 MD）")
    parser.add_argument("--thesis", help="论文仓库根目录；提供时用 aux 映射锚点并记录 git 基线提交")
    parser.add_argument("--main", help="论文主文件（相对 --thesis），记录到状态文件供后续脚本使用")
    parser.add_argument("--root", help="输出父目录；缺省为评阅书目录的父目录")
    parser.add_argument("--stage", choices=STAGES, default="pre-review", help="评阅阶段")
    parser.add_argument("--form-title", help="修改审查表标题；缺省按 --stage 取")
    parser.add_argument("--order", help="评阅人顺序：以逗号分隔的评阅书文件名")
    parser.add_argument("--base-commit", help="送审版本对应的论文仓库提交；缺省为当前 HEAD")
    parser.add_argument(
        "--force", action="store_true", help="重写 reviews/ 与状态文件（台账不覆盖）"
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON 摘要")
    args = parser.parse_args(argv)

    warnings = Warnings()
    try:
        reviews_dir = Path(args.reviews)
        root, responses, workspace = resolve_layout(reviews_dir, args.root)
        reviews_dir = reviews_dir.resolve()
        thesis = Path(args.thesis).resolve() if args.thesis else None
        if thesis is not None and not thesis.is_dir():
            raise IntakeError(f"论文仓库不存在：{thesis}")
        files = list_review_files(reviews_dir, args.order, warnings)
    except IntakeError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    if any(path.suffix.lower() == ".pdf" for path in files) and not _PYMUPDF_AVAILABLE:
        print(f"错误：{MISSING_PYMUPDF}", file=sys.stderr)
        return 3
    review_out = workspace / "reviews"
    if review_out.exists() and not args.force:
        print(f"错误：{review_out} 已存在；确认重写时加 --force（台账不会被覆盖）", file=sys.stderr)
        return 4

    try:
        reviews = [
            Review(id=f"R{index}", path=path, pages=read_pages(path))
            for index, path in enumerate(files, 1)
        ]
    except IntakeError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    for review in reviews:
        parse_review(review, warnings)

    labels = cites = None
    base_commit = args.base_commit
    if thesis is not None:
        labels = rebuttal_common.load_aux_labels(thesis)
        cites = rebuttal_common.load_bibcites(thesis)
        if not labels:
            warnings.add("W-NO-AUX", "论文仓库中没有 aux 标签；请先编译送审版本")
        if base_commit is None:
            base_commit = rebuttal_common.git_head(thesis)
            if base_commit is None:
                warnings.add("W-NO-GIT", "论文仓库不是 git 仓库，修改证据只能由用户确认")
    ledger = build_ledger(reviews, labels, cites, warnings)

    responses.mkdir(parents=True, exist_ok=True)
    review_out.mkdir(parents=True, exist_ok=True)
    for old in review_out.iterdir():
        if REVIEW_FILE_RE.fullmatch(old.name) and old.is_file():
            old.unlink()
    for review in reviews:
        (review_out / f"{review.id}.md").write_text(
            review_markdown(review), encoding="utf-8", newline="\n"
        )

    ledger_path = workspace / "concerns.yaml"
    ledger_written = not ledger_path.exists()
    if ledger_written:
        rebuttal_common.dump_ledger(ledger_path, ledger)
    else:
        try:
            existing = rebuttal_common.load_ledger(ledger_path)
        except ValueError as exc:
            warnings.add("W-LEDGER", f"现有台账无法读取：{exc}")
        else:
            missing = missing_ledger_items(existing, reviews)
            if missing:
                warnings.add("W-LEDGER-MISSING", f"台账缺少条目：{'、'.join(missing)}，请合并")

    state_path = workspace / "rebuttal_state.json"
    today = datetime.date.today().isoformat()
    previous: dict = {}
    if state_path.exists():
        try:
            previous = rebuttal_common.load_state(state_path)
        except (ValueError, json.JSONDecodeError):
            previous = {}
    state = {
        "schema": rebuttal_common.STATE_SCHEMA,
        "stage": args.stage,
        "form_title": args.form_title or FORM_TITLES[args.stage],
        "reviews_dir": Path(os.path.relpath(reviews_dir, root)).as_posix(),
        "reviews": [
            {
                "id": review.id,
                "file": review.path.name,
                "sha256": sha256_file(review.path),
                "pages": len(review.pages),
                "text_layer": review.text_layer,
            }
            for review in reviews
        ],
        "thesis": {
            "given": thesis is not None,
            "main": args.main,
            "base_commit": base_commit,
            "aux_labels": len(labels) if labels is not None else 0,
        },
        "rendered": previous.get("rendered", {}),
        "created": previous.get("created", today),
        "updated": today,
    }
    rebuttal_common.dump_state(state_path, state)

    summary = []
    for review in reviews:
        anchors = sum(
            len(concern["anchors"])
            for concern in ledger["concerns"]
            if concern["reviewer"] == review.id
        )
        summary.append(
            {
                "id": review.id,
                "file": review.path.name,
                "grade": review.grade,
                "total_score": review.total_score,
                "items": len(review.items),
                "anchors": anchors,
            }
        )
    if args.json:
        payload = {
            "root": str(root),
            "reviewers": summary,
            "warnings": warnings.items,
            "ledger_written": ledger_written,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"已初始化 {root}：responses/ 与 workspace/；评阅人 {len(reviews)} 位")
        for item in summary:
            print(
                f"  {item['id']} {item['file']}：总体评价 {item['grade'] or '未解析'}，"
                f"总分 {item['total_score'] if item['total_score'] is not None else '未解析'}，"
                f"意见 {item['items']} 条，锚点 {item['anchors']} 个"
            )
        print(f"台账：{'已生成' if ledger_written else '已存在，未覆盖'} {ledger_path}")
        for warning in warnings.items:
            location = f"（{warning['source']}）" if warning.get("source") else ""
            print(f"  {warning['code']}: {warning['message']}{location}")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
