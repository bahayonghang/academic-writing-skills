#!/usr/bin/env python3
"""
Page images and a contact sheet of the compiled defense deck.

The script renders each page of defense.pdf to page-NNN.png in the output
directory and joins the page images into contact-sheet.png for visual review.
Before it writes, it deletes the old page-NNN.png files in the output
directory. It does not delete other files.

Visual checklist: references/quality-gate.md.

Usage:
    uv run python -B $SKILL_DIR/scripts/render_preview.py --pdf DIR/defense.pdf \
        --out DIR/preview [--dpi 110] [--cols 4]

Exit codes: 0 done; 2 input error; 3 PyMuPDF is not installed.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Module-level availability check, as in paper-audit/scripts/visual_check.py
try:
    import pymupdf as _pymupdf_module

    _PYMUPDF_AVAILABLE = True
except ImportError:
    _pymupdf_module = None  # type: ignore[assignment]
    _PYMUPDF_AVAILABLE = False

PAGE_RE = re.compile(r"page-\d{3}\.png")
SHEET_NAME = "contact-sheet.png"
THUMB_WIDTH = 480
LABEL_HEIGHT = 32
GAP = 16
FONT_SIZE = 20
MISSING_PYMUPDF = "缺少 PyMuPDF：运行 `uv pip install pymupdf` 后重试"


class PreviewError(Exception):
    """Input error (exit code 2)."""


def render_pages(pdf: Path, out: Path, dpi: int) -> list[Path]:
    """Write page-001.png, page-002.png, ... after the old page images are deleted."""
    try:
        document = _pymupdf_module.open(pdf)  # type: ignore[union-attr]
    except Exception as exc:  # PyMuPDF raises several error types for a bad file
        raise PreviewError(f"无法打开 PDF {pdf}：{exc}") from exc
    with document:
        if document.page_count == 0:
            raise PreviewError(f"PDF {pdf} 没有页面")
        out.mkdir(parents=True, exist_ok=True)
        for old in out.iterdir():
            if PAGE_RE.fullmatch(old.name) and old.is_file():
                old.unlink()
        pages = []
        for number, page in enumerate(document, 1):
            path = out / f"page-{number:03d}.png"
            page.get_pixmap(dpi=dpi).save(str(path))
            pages.append(path)
    return pages


def contact_sheet(pages: list[Path], cols: int) -> Image.Image:
    """Thumbnails 480 px wide in up to ``cols`` columns on white, each with its page number."""
    thumbs = []
    for path in pages:
        with Image.open(path) as image:
            height = max(1, round(image.height * THUMB_WIDTH / image.width))
            thumbs.append(image.convert("RGB").resize((THUMB_WIDTH, height)))
    columns = min(cols, len(thumbs))
    rows = math.ceil(len(thumbs) / columns)
    cell = max(thumb.height for thumb in thumbs) + LABEL_HEIGHT
    size = (columns * (THUMB_WIDTH + GAP) + GAP, rows * (cell + GAP) + GAP)
    sheet = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=FONT_SIZE)
    for index, thumb in enumerate(thumbs):
        x = GAP + index % columns * (THUMB_WIDTH + GAP)
        y = GAP + index // columns * (cell + GAP)
        sheet.paste(thumb, (x, y))
        label = (x + THUMB_WIDTH // 2, y + thumb.height + LABEL_HEIGHT // 2)
        draw.text(label, str(index + 1), fill="black", font=font, anchor="mm")
    return sheet


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="答辩稿预览：把 defense.pdf 逐页渲染为 page-NNN.png，并拼成总览图。"
    )
    parser.add_argument("--pdf", required=True, help="编译得到的 defense.pdf")
    parser.add_argument("--out", required=True, help="输出目录；不存在时创建")
    parser.add_argument("--dpi", type=int, default=110, help="逐页图分辨率，默认 110")
    parser.add_argument("--cols", type=int, default=4, help="总览图列数，默认 4")
    args = parser.parse_args(argv)

    pdf = Path(args.pdf)
    out = Path(args.out)
    try:
        if args.dpi < 1 or args.cols < 1:
            raise PreviewError("--dpi 与 --cols 应为正整数")
        if not pdf.is_file():
            raise PreviewError(f"PDF 不存在：{args.pdf}")
        if not _PYMUPDF_AVAILABLE:
            print(MISSING_PYMUPDF, file=sys.stderr)
            return 3
        pages = render_pages(pdf, out, args.dpi)
    except PreviewError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    sheet = out / SHEET_NAME
    contact_sheet(pages, args.cols).save(sheet)
    print(f"页数：{len(pages)}")
    print(f"输出目录：{out}")
    print(f"总览图：{sheet}")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    sys.exit(main())
