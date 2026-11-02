#!/usr/bin/env python3
"""
Parser of the Touying defense deck (defense.typ) for check_deck.py.

build_deck.py writes plan text as string literals, thesis source between the
``// defense-source-begin`` and ``// defense-source-end`` comment lines, and a
``// defense-frame:`` marker before each frame. This module splits the deck into
frames, reads the visible text, figures, equations, table cells, and notes of
each frame, reads the PDF page labels of the presenter build itself (PyMuPDF
misreads the labels that Typst writes), and asks typst for the first page of
each frame. It does not write files.

The module has no command line. Codes and criteria: references/quality-gate.md.
"""

from __future__ import annotations

import bisect
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import typst_backend
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import typst_backend

MARKER_RE = re.compile(
    r"^//\s*defense-frame:\s*id=(\S+)\s+role=(\S+)\s+chapter=(\S+)\s+layout=(\S+)\s*$"
)
FRAME_START_RE = re.compile(r"^\s*(?:#(?:title-slide|outline-slide|ending-slide)\(|==?\s)")
HEADING_RE = re.compile(r"^\s*(=+)\s")
SKIP_LABEL = "<touying:skip>"
NOTE_RE = re.compile(r"(?<![\w-])note\s*(?:\[|:)")
STRING_ESCAPES = {"\\": "\\", '"': '"', "n": "\n", "t": "\t", "r": "\r"}
SECTION_NUMBER_RE = re.compile(r"^\s*\d+(?:\.\d+)+")
CONFIG_FIELDS = ("title", "author", "supervisor", "school", "subject", "date", "stage-en")
PDF_STRING_RE = re.compile(r"/P\s*(\((?:\\.|[^\\)])*\)|<[0-9A-Fa-f\s]*>)")
NUMS_RE = re.compile(r"(\d+)\s+(?:(\d+)\s+0\s+R|(<<.*?>>))", re.S)


@dataclass
class Literal:
    kind: str  # str, raw, or comment
    start: int
    end: int
    value: str


@dataclass
class TypstFrame:
    order: int
    id: str
    role: str | None
    chapter: int | None
    chapter_text: str | None
    layout: str | None
    marker: int | None  # 1-based line of the frame marker
    start: int  # 1-based first line of the frame
    end: int  # 1-based last line of the frame
    begin: int  # offset of the first line
    stop: int  # offset after the last line
    toc: int | None = None  # 0 for the outline slide, the heading index for an opener


@dataclass
class Call:
    name: str
    start: int  # offset of the name
    open: int  # offset of the first ( or [
    close: int  # offset of the matching ) or ]
    end: int  # offset after the trailing content blocks


@dataclass
class TypstDeck:
    path: Path
    lines: list[str]
    text: str
    code: str  # text with literals and comments blanked
    literals: list[Literal]
    starts: list[int]
    regions: list[tuple[int, int]]
    frames: list[TypstFrame] = field(default_factory=list)
    headings: int = 0
    preamble_end: int = 0

    def line_of(self, offset: int) -> int:
        return bisect.bisect_right(self.starts, offset)

    def in_region(self, offset: int) -> bool:
        return any(start <= offset < end for start, end in self.regions)

    def literals_in(self, start: int, end: int) -> list[Literal]:
        return [lit for lit in self.literals if start <= lit.start and lit.end <= end]

    def plain(self, start: int, end: int, sep: str = "") -> str:
        """Strings and raw text between two offsets, in order (comments excluded)."""
        values = [lit.value for lit in self.literals_in(start, end) if lit.kind != "comment"]
        return sep.join(values)


# ---------------------------------------------------------------------------
# Lexing
# ---------------------------------------------------------------------------


def decode_string(body: str) -> str:
    out = []
    index = 0
    while index < len(body):
        char = body[index]
        if char == "\\" and index + 1 < len(body):
            nxt = body[index + 1]
            if nxt == "u" and body.startswith("{", index + 2):
                close = body.find("}", index + 3)
                if close > 0:
                    try:
                        out.append(chr(int(body[index + 3 : close], 16)))
                        index = close + 1
                        continue
                    except ValueError:
                        pass
            out.append(STRING_ESCAPES.get(nxt, nxt))
            index += 2
            continue
        out.append(char)
        index += 1
    return "".join(out)


def scan_literals(text: str) -> list[Literal]:
    """String literals, raw text, and comments of a generated deck."""
    found: list[Literal] = []
    index = 0
    while index < len(text):
        char = text[index]
        if char == '"':
            end = index + 1
            while end < len(text) and text[end] != '"':
                end += 2 if text[end] == "\\" else 1
            end = min(end, len(text) - 1)
            found.append(Literal("str", index, end + 1, decode_string(text[index + 1 : end])))
            index = end + 1
        elif char == "`":
            run = re.match(r"`+", text[index:])
            assert run is not None
            fence = run.group(0)
            if len(fence) == 2:  # empty inline raw
                found.append(Literal("raw", index, index + 2, ""))
                index += 2
                continue
            close = text.find(fence, index + len(fence))
            close = len(text) if close < 0 else close
            body = text[index + len(fence) : close]
            if len(fence) >= 3:
                body = re.sub(r"^[^\S\n]*\n", "", body, count=1)
                body = re.sub(r"\n[^\S\n]*$", "", body, count=1)
            end = min(close + len(fence), len(text))
            found.append(Literal("raw", index, end, body))
            index = end
        elif text.startswith("//", index):
            end = text.find("\n", index)
            end = len(text) if end < 0 else end
            found.append(Literal("comment", index, end, text[index:end]))
            index = end
        elif text.startswith("/*", index):
            end = text.find("*/", index + 2)
            end = len(text) if end < 0 else end + 2
            found.append(Literal("comment", index, end, text[index:end]))
            index = end
        else:
            index += 1
    return found


def blank(text: str, literals: list[Literal]) -> str:
    chars = list(text)
    for lit in literals:
        for index in range(lit.start, lit.end):
            if chars[index] != "\n":
                chars[index] = " "
    return "".join(chars)


def match_close(code: str, pos: int) -> int:
    """Offset of the bracket that closes the one at ``pos``; the text length when unclosed."""
    pairs = {"(": ")", "[": "]", "{": "}"}
    stack = [pairs[code[pos]]]
    index = pos + 1
    while index < len(code) and stack:
        char = code[index]
        if char in pairs:
            stack.append(pairs[char])
        elif stack and char == stack[-1]:
            stack.pop()
            if not stack:
                return index
        index += 1
    return len(code)


# ---------------------------------------------------------------------------
# Deck structure
# ---------------------------------------------------------------------------


def parse_deck(path: Path, text: str) -> TypstDeck:
    lines = text.split("\n")
    literals = scan_literals(text)
    code = blank(text, literals)
    starts = [0]
    for line in lines[:-1]:
        starts.append(starts[-1] + len(line) + 1)
    regions: list[tuple[int, int]] = []
    opened: int | None = None
    for number, line in enumerate(lines):
        stripped = line.strip()
        if stripped == typst_backend.REGION_BEGIN and opened is None:
            opened = starts[number]
        elif stripped == typst_backend.REGION_END and opened is not None:
            regions.append((opened, starts[number] + len(line)))
            opened = None
    if opened is not None:
        regions.append((opened, len(text)))
    deck = TypstDeck(path, lines, text, code, literals, starts, regions)
    code_lines = code.split("\n")

    def is_start(index: int) -> bool:
        line = code_lines[index]
        if deck.in_region(starts[index]) or SKIP_LABEL in line:
            return False
        return bool(FRAME_START_RE.match(line))

    def is_filler(index: int) -> bool:
        stripped = lines[index].strip()
        return not stripped or bool(MARKER_RE.match(stripped)) or SKIP_LABEL in code_lines[index]

    frame_starts = [index for index in range(len(lines)) if is_start(index)]
    deck.preamble_end = starts[frame_starts[0]] if frame_starts else len(text)
    heading_index = 0
    for order, first in enumerate(frame_starts, 1):
        following = frame_starts[order] if order < len(frame_starts) else len(lines)
        last = following - 1
        while last > first and is_filler(last):
            last -= 1
        frame = TypstFrame(
            order,
            f"#{order}",
            None,
            None,
            None,
            None,
            None,
            first + 1,
            last + 1,
            starts[first],
            starts[last] + len(lines[last]),
        )
        previous = first - 1
        while previous >= 0 and not lines[previous].strip():
            previous -= 1
        match = MARKER_RE.match(lines[previous].strip()) if previous >= 0 else None
        if match:
            frame_id, role, chapter, layout = match.groups()
            frame.id, frame.role, frame.chapter_text, frame.layout = frame_id, role, chapter, layout
            frame.chapter = int(chapter) if chapter.isdecimal() else None
            frame.marker = previous + 1
        deck.frames.append(frame)
    for index, line in enumerate(code_lines):
        heading = HEADING_RE.match(line)
        if heading and len(heading.group(1)) == 1 and not deck.in_region(starts[index]):
            heading_index += 1
            frame = next((f for f in deck.frames if f.start == index + 1), None)
            if frame is not None:
                frame.toc = heading_index
    deck.headings = heading_index
    for frame in deck.frames:
        if re.match(r"\s*#outline-slide\(", code_lines[frame.start - 1]):
            frame.toc = 0
    return deck


def frame_text(deck: TypstDeck, frame: TypstFrame) -> str:
    return deck.text[frame.begin : frame.stop]


def calls(deck: TypstDeck, start: int, end: int, name: str) -> list[Call]:
    """Calls ``name(...)`` or ``name[...]`` between two offsets, with trailing content blocks."""
    found = []
    pattern = re.compile(r"(?<![\w.-])" + re.escape(name) + r"(?=[(\[])")
    for match in pattern.finditer(deck.code, start, end):
        open_at = match.end()
        close = match_close(deck.code, open_at)
        after = close + 1
        while after < len(deck.code) and deck.code[after] == "[":
            after = match_close(deck.code, after) + 1
        found.append(Call(name, match.start(), open_at, close, min(after, len(deck.code))))
    return found


def frame_calls(deck: TypstDeck, frame: TypstFrame, name: str) -> list[Call]:
    return calls(deck, frame.begin, frame.stop, name)


def top_level_args(deck: TypstDeck, call: Call) -> list[tuple[int, int]]:
    """Spans of the comma-separated arguments inside the parentheses of a call."""
    if deck.code[call.open] != "(":
        return []
    spans = []
    depth = 0
    first = call.open + 1
    for index in range(call.open + 1, call.close):
        char = deck.code[index]
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            spans.append((first, index))
            first = index + 1
    spans.append((first, call.close))

    def filled(a: int, b: int) -> bool:
        # A string or raw literal is an argument too; a span with only comments is not.
        return bool(deck.code[a:b].strip()) or any(
            lit.kind != "comment" and a <= lit.start < b for lit in deck.literals
        )

    return [(a, b) for a, b in spans if filled(a, b)]


def named_arg(deck: TypstDeck, call: Call, key: str) -> tuple[int, int] | None:
    """Span of the value of ``key:`` in a call."""
    for start, end in top_level_args(deck, call):
        match = re.match(r"\s*" + re.escape(key) + r"\s*:", deck.code[start:end])
        if match:
            return start + match.end(), end
    return None


def note_count(deck: TypstDeck, frame: TypstFrame) -> int:
    return len(NOTE_RE.findall(deck.code, frame.begin, frame.stop))


def note_line(deck: TypstDeck, number: int) -> bool:
    """True for a line of the deck that holds a speaker note."""
    line = deck.code.split("\n")[number - 1] if number <= len(deck.lines) else ""
    return bool(NOTE_RE.search(line))


def hidden_lines(deck: TypstDeck, frame: TypstFrame) -> set[int]:
    """Lines whose strings are not slide text: headings, notes, and thesis source."""
    hidden = set()
    code_lines = deck.code.split("\n")
    for number in range(frame.start, frame.end + 1):
        offset = deck.starts[number - 1]
        line = code_lines[number - 1]
        if HEADING_RE.match(line) or NOTE_RE.search(line) or deck.in_region(offset):
            hidden.add(number)
    return hidden


def visible_lines(
    deck: TypstDeck, frame: TypstFrame, numbers: bool = False
) -> list[tuple[int, str]]:
    """Slide text by line: strings outside headings, notes, image paths, and thesis source.

    With ``numbers`` the leading section number of ``sub(...)`` is removed (D-NUM-SRC).
    """
    hidden = hidden_lines(deck, frame)
    paths = {
        lit.start
        for call in frame_calls(deck, frame, "image")
        for lit in deck.literals_in(call.open, call.close)[:1]
    }
    subs = {
        lit.start
        for call in frame_calls(deck, frame, "sub")
        for lit in deck.literals_in(call.open, call.close)[:1]
    }
    found: dict[int, list[str]] = {}
    for lit in deck.literals_in(frame.begin, frame.stop):
        line = deck.line_of(lit.start)
        if lit.kind != "str" or line in hidden or lit.start in paths:
            continue
        value = lit.value
        if numbers and lit.start in subs:
            value = SECTION_NUMBER_RE.sub("", value)
        found.setdefault(line, []).append(value)
    return [(line, "".join(parts)) for line, parts in sorted(found.items())]


def call_plain(deck: TypstDeck, call: Call) -> str:
    return deck.plain(call.open, call.close)


def point_count(deck: TypstDeck, frame: TypstFrame) -> int:
    return sum(len(top_level_args(deck, call)) for call in frame_calls(deck, frame, "points"))


@dataclass
class FigureRef:
    line: int
    file: str
    caption: str | None


def figures(deck: TypstDeck, frame: TypstFrame) -> list[FigureRef]:
    """``image(...)`` paths with the caption of the enclosing ``figure-box``."""
    boxes = frame_calls(deck, frame, "figure-box")
    found = []
    for call in frame_calls(deck, frame, "image"):
        literals = [lit for lit in deck.literals_in(call.open, call.close) if lit.kind == "str"]
        if not literals:
            continue
        caption = None
        owner = next((b for b in boxes if b.start <= call.start < b.end), None)
        if owner is not None:
            span = named_arg(deck, owner, "caption")
            if span is not None:
                caption = deck.plain(*span, sep=" ")
        found.append(FigureRef(deck.line_of(call.start), literals[0].value, caption))
    return found


def captions(deck: TypstDeck, frame: TypstFrame) -> list[tuple[int, str]]:
    """Text of the ``fig-caption(...)`` lines (grid figure and table captions)."""
    return [
        (deck.line_of(call.start), deck.plain(call.open, call.close, sep=" "))
        for call in frame_calls(deck, frame, "fig-caption")
    ]


def equations(deck: TypstDeck, frame: TypstFrame) -> list[tuple[int, str, bool]]:
    """Display equations: line, LaTeX source (the last raw text of the call), in a source region."""
    found = []
    for call in frame_calls(deck, frame, "mitex"):
        raws = [lit for lit in deck.literals_in(call.open, call.close) if lit.kind == "raw"]
        body = raws[-1].value if raws else ""
        found.append((deck.line_of(call.start), body, deck.in_region(call.start)))
    return found


def tables(deck: TypstDeck, frame: TypstFrame) -> list[tuple[int, list[str], bool]]:
    """``result-table`` calls: line, plain text of each cell in order, in a source region."""
    found = []
    for call in frame_calls(deck, frame, "result-table"):
        cells = []
        depth = 0
        first = 0
        for index in range(call.open, call.close):
            char = deck.code[index]
            if char == "[":
                depth += 1
                if depth == 1:
                    first = index
            elif char == "]":
                depth -= 1
                if depth == 0:
                    cells.append(deck.plain(first, index))
        found.append((deck.line_of(call.start), cells, deck.in_region(call.start)))
    return found


def outside_source(deck: TypstDeck, frame: TypstFrame) -> dict[str, list[int]]:
    """Lines of math and tables written outside the thesis source regions."""
    math: list[int] = []
    for match in re.finditer(r"\$", deck.code[frame.begin : frame.stop]):
        offset = frame.begin + match.start()
        if not deck.in_region(offset):
            math.append(deck.line_of(offset))
    for name in ("mitex", "mi", "mimath"):
        math += [
            deck.line_of(c.start)
            for c in frame_calls(deck, frame, name)
            if not deck.in_region(c.start)
        ]
    tab = [
        deck.line_of(c.start)
        for name in ("result-table", "table")
        for c in frame_calls(deck, frame, name)
        if not deck.in_region(c.start)
    ]
    return {"math": sorted(set(math)), "table": sorted(set(tab))}


def config_info(deck: TypstDeck) -> dict[str, tuple[int | None, str]]:
    """``config-info`` fields of the preamble: line and plain text of each value."""
    found: dict[str, tuple[int | None, str]] = dict.fromkeys(CONFIG_FIELDS, (None, ""))
    infos = calls(deck, 0, deck.preamble_end, "config-info")
    if not infos:
        return found
    call = infos[-1]
    for key in CONFIG_FIELDS:
        span = named_arg(deck, call, key)
        if span is not None:
            found[key] = (deck.line_of(span[0]), deck.plain(*span))
    return found


# ---------------------------------------------------------------------------
# Compiled output
# ---------------------------------------------------------------------------


def note_records(deck_path: Path) -> list[dict[str, Any]] | None:
    """``<ysu-note>`` records (frame, page, ...) of the compiled deck; None when unavailable.

    Uses ``typst eval`` (``typst query`` is deprecated in Typst 0.15) and runs only when
    every imported package is installed, so that typst downloads nothing.
    """
    executable = shutil.which("typst")
    if executable is None:
        return None
    text = deck_path.read_text(encoding="utf-8", errors="replace")
    # The theme imports touying; check it too, as build_deck.py --compile does.
    specs = list(re.findall(r'#import\s+"(@[^"]+)"', text)) + [typst_backend.TOUYING_PACKAGE]
    if typst_backend.missing_packages(specs):
        return None
    root = str(deck_path.parent)
    commands = [
        [
            executable,
            "eval",
            "query(<ysu-note>).map(it => it.value)",
            "--root",
            root,
            "--in",
            str(deck_path),
        ],
        [executable, "query", "--root", root, str(deck_path), "<ysu-note>", "--field", "value"],
    ]
    for command in commands:
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=600,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if result.returncode != 0:
            continue
        try:
            records = json.loads(result.stdout)
        except ValueError:
            continue
        if isinstance(records, list):
            return [r for r in records if isinstance(r, dict)]
    return None


def _pdf_string(token: str) -> str:
    if token.startswith("<"):
        data = bytes.fromhex(re.sub(r"\s", "", token[1:-1]))
        if data.startswith(b"\xfe\xff"):
            return data[2:].decode("utf-16-be", errors="replace")
        return data.decode("latin-1")
    body = token[1:-1]
    body = re.sub(r"\\([\\()])", r"\1", body)
    return body


def _roman(number: int) -> str:
    values = (
        (1000, "m"),
        (900, "cm"),
        (500, "d"),
        (400, "cd"),
        (100, "c"),
        (90, "xc"),
        (50, "l"),
        (40, "xl"),
        (10, "x"),
        (9, "ix"),
        (5, "v"),
        (4, "iv"),
        (1, "i"),
    )
    out = []
    for value, letters in values:
        while number >= value:
            out.append(letters)
            number -= value
    return "".join(out)


def _format(style: str | None, number: int) -> str:
    if style == "D":
        return str(number)
    if style in ("r", "R"):
        text = _roman(number)
        return text.upper() if style == "R" else text
    if style in ("a", "A"):
        letter = chr(ord("a") + (number - 1) % 26) * ((number - 1) // 26 + 1)
        return letter.upper() if style == "A" else letter
    return ""


def page_labels(document: Any) -> list[str]:
    """Page labels read from the catalog ``/PageLabels`` number tree (``/Nums`` and ``/Kids``).

    PyMuPDF 2.0 ``get_label()`` reads ``/Type /PageLabel`` in Typst output as a prefix.
    """
    count = document.page_count
    kind, value = document.xref_get_key(document.pdf_catalog(), "PageLabels")
    if kind == "null":
        return [""] * count
    rules: list[tuple[int, str]] = []

    def resolve(token: str) -> str:
        match = re.fullmatch(r"\s*(\d+)\s+0\s+R\s*", token)
        return document.xref_object(int(match.group(1))) if match else token

    def walk(source: str) -> None:
        nums = re.search(r"/Nums\s*\[(.*)\]", source, re.S)
        if nums:
            for match in NUMS_RE.finditer(nums.group(1)):
                start, ref, inline = match.groups()
                rules.append((int(start), document.xref_object(int(ref)) if ref else inline))
        kids = re.search(r"/Kids\s*\[([^\]]*)\]", source)
        if kids:
            for ref in re.findall(r"(\d+)\s+0\s+R", kids.group(1)):
                walk(document.xref_object(int(ref)))

    walk(resolve(value) if kind == "xref" else value)
    rules.sort()
    labels = []
    for page in range(count):
        index = bisect.bisect_right([start for start, _ in rules], page) - 1
        if index < 0:
            labels.append("")
            continue
        start, rule = rules[index]
        prefix = PDF_STRING_RE.search(rule)
        style = re.search(r"/S\s*/([A-Za-z])", rule)
        first = re.search(r"/St\s+(\d+)", rule)
        number = (int(first.group(1)) if first else 1) + page - start
        labels.append(
            (_pdf_string(prefix.group(1)) if prefix else "")
            + _format(style.group(1) if style else None, number)
        )
    return labels
