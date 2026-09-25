"""Tests for scripts/render_preview.py."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest
from PIL import Image

from tests.support.paths import SKILLS_ROOT

SCRIPT = SKILLS_ROOT / "latex-defense-zh" / "scripts" / "render_preview.py"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
PAGE_SIZE = (693, 390)  # 16:9 page at 110 dpi; the thumbnail is 480 x 270


def fresh_module() -> ModuleType:
    """Load render_preview.py again, so that its PyMuPDF import sees the current sys.modules."""
    spec = importlib.util.spec_from_file_location("_defense_render_preview_fresh", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_page(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", PAGE_SIZE, (200, 210, 225)).save(path)
    return path


def sheet_size(module: ModuleType, columns: int, rows: int, height: int) -> tuple[int, int]:
    cell = height + module.LABEL_HEIGHT
    return (
        columns * (module.THUMB_WIDTH + module.GAP) + module.GAP,
        rows * (cell + module.GAP) + module.GAP,
    )


def tree_hashes(*roots: Path) -> dict[str, str]:
    found = {}
    for root in roots:
        paths = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file())
        for path in paths:
            found[path.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return found


def test_missing_pymupdf_exits_3(monkeypatch, tmp_path: Path, capsys) -> None:
    monkeypatch.setitem(sys.modules, "pymupdf", None)
    module = fresh_module()
    pdf = tmp_path / "defense.pdf"
    pdf.write_bytes(b"%PDF-1.5\n")
    assert module.main(["--pdf", str(pdf), "--out", str(tmp_path / "preview")]) == 3
    assert capsys.readouterr().err.strip() == "缺少 PyMuPDF：运行 `uv pip install pymupdf` 后重试"
    assert not (tmp_path / "preview").exists()


@pytest.mark.parametrize(
    ("pdf", "option"),
    [("missing.pdf", []), ("defense.pdf", ["--cols", "0"]), ("defense.pdf", ["--dpi", "0"])],
    ids=["missing-pdf", "cols", "dpi"],
)
def test_bad_input_exits_2(
    defense_scripts, tmp_path: Path, capsys, pdf: str, option: list[str]
) -> None:
    (tmp_path / "defense.pdf").write_bytes(b"%PDF-1.5\n")
    args = ["--pdf", str(tmp_path / pdf), "--out", str(tmp_path / "preview"), *option]
    assert defense_scripts.render_preview.main(args) == 2
    assert "错误：" in capsys.readouterr().err
    assert not (tmp_path / "preview").exists()


@pytest.mark.parametrize(("cols", "columns", "rows"), [(2, 2, 2), (4, 3, 1)])
def test_contact_sheet_layout(
    defense_scripts, tmp_path: Path, cols: int, columns: int, rows: int
) -> None:
    module = defense_scripts.render_preview
    pages = [write_page(tmp_path / f"page-{number:03d}.png") for number in (1, 2, 3)]
    sheet = module.contact_sheet(pages, cols)
    assert sheet.size == sheet_size(module, columns, rows, 270)
    assert sheet.getpixel((0, 0)) == (255, 255, 255)


def test_render_pages_and_sheet(defense_scripts, tmp_path: Path, capsys) -> None:
    pymupdf = pytest.importorskip("pymupdf")
    pdf = tmp_path / "defense.pdf"
    with pymupdf.open() as document:
        for number in (1, 2, 3):
            page = document.new_page(width=453.54, height=255.12)
            page.insert_text((72, 72), f"page {number}")
        document.save(str(pdf))
    out = tmp_path / "preview"
    write_page(out / "page-009.png")
    (out / "keep.txt").write_text("keep", encoding="utf-8")
    module = defense_scripts.render_preview
    assert module.main(["--pdf", str(pdf), "--out", str(out), "--cols", "2"]) == 0
    assert sorted(path.name for path in out.iterdir()) == [
        "contact-sheet.png",
        "keep.txt",
        "page-001.png",
        "page-002.png",
        "page-003.png",
    ]
    with Image.open(out / "page-001.png") as page:
        height = round(page.height * module.THUMB_WIDTH / page.width)
    with Image.open(out / "contact-sheet.png") as sheet:
        assert sheet.size == sheet_size(module, 2, 2, height)
    assert capsys.readouterr().out.split("\n")[0] == "页数：3"


def test_preview_writes_only_into_out(
    built_deck: Path, tmp_path: Path, defense_scripts, capsys
) -> None:
    """AC6: the deck directory, plan, inventory, and thesis stay the same; only --out changes."""
    pymupdf = pytest.importorskip("pymupdf")
    pdf = built_deck / "defense.pdf"
    with pymupdf.open() as document:
        document.new_page(width=453.54, height=255.12)
        document.save(str(pdf))
    roots = (
        built_deck,
        tmp_path / "inventory.json",
        tmp_path / "slide_plan.yaml",
        tmp_path / "mini-thesis",
    )
    before = tree_hashes(*roots)
    out = built_deck / "preview"
    assert defense_scripts.render_preview.main(["--pdf", str(pdf), "--out", str(out)]) == 0
    capsys.readouterr()
    after = tree_hashes(*roots)
    assert {k: v for k, v in after.items() if not k.startswith(f"{out.as_posix()}/")} == before
    assert sorted(path.name for path in out.iterdir()) == ["contact-sheet.png", "page-001.png"]


def test_unreadable_pdf_exits_2(defense_scripts, tmp_path: Path, capsys) -> None:
    pytest.importorskip("pymupdf")
    pdf = tmp_path / "defense.pdf"
    pdf.write_text("not a pdf", encoding="utf-8")
    out = tmp_path / "preview"
    assert defense_scripts.render_preview.main(["--pdf", str(pdf), "--out", str(out)]) == 2
    assert "错误：" in capsys.readouterr().err
    assert not out.exists()


def test_cli_reports_missing_pdf(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            str(SCRIPT),
            "--pdf",
            str(tmp_path / "missing.pdf"),
            "--out",
            str(tmp_path / "preview"),
        ],
        capture_output=True,
        encoding="utf-8",
        env=ENV,
        check=False,
    )
    assert result.returncode == 2
    assert result.stderr.startswith("错误：PDF 不存在：")
