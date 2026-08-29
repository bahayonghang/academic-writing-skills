#!/usr/bin/env python3
"""Reproduce the writing-rhythm density calibration from extracted thesis text.

Run from the repository root. The script is read-only and uses only the Python
standard library so the evidence can be reproduced without the skill runtime.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from statistics import quantiles

ROOT = Path(__file__).resolve().parents[4]
THESIS_DIR = ROOT / "ref" / "thesis" / "decrypted"

TERM_THRESHOLDS = (
    "首先",
    "其次",
    "然后",
    "最后",
    "其一",
    "然而",
    "此外",
    "因此",
    "另外",
    "进而",
    "而且",
    "显然",
    "通常",
    "一般",
    "尤其",
    "显著",
    "全面",
    "深入",
    "大量",
    "众多",
    "重要",
    "关键",
    "核心",
    "基本",
    "主要",
    "最为",
    "极为",
    "尤为",
)
SEQUENCE_TERMS = ("首先", "其次", "然后", "最后")
HAN_RE = re.compile(r"[\u4e00-\u9fff]")
SIMPLE_HEADING_RE = re.compile(
    r"^(?P<num>[1-9]\d*\.\d+)\s+(?P<title>[^.·…]{2,80}?)\s*$"
)
ANY_HEADING_RE = re.compile(
    r"^(?P<num>[1-9]\d*\.\d+(?:\.\d+)*)\s+(?P<title>[^.·…]{2,80}?)\s*$"
)
THROAT_CLEARING_RE = re.compile(
    r"^(?:综上所述|总而言之|总的来说|由此可见|值得(?:指出|注意)的是|"
    r"需要(?:指出|说明)的是|不难(?:发现|看出)|众所周知|毋庸讳言|"
    r"首先[,，]|其次[,，]|然而[,，]|此外[,，]|一方面|另一方面)"
)


def percentile(values: list[float], percentile_value: float) -> float:
    """Linear-interpolated percentile, matching the planning calculation."""
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile requires at least one value")
    position = (len(ordered) - 1) * percentile_value
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def visible_pdf_lines(lines: list[str]) -> list[str]:
    """Normalize PDF-extracted text using the recorded calibration adapter."""
    reference_starts = [i for i, line in enumerate(lines) if line.strip() == "参考文献"]
    end = reference_starts[-1] if reference_starts else len(lines)
    visible: list[str] = []
    for raw in lines[:end]:
        stripped = raw.strip()
        if re.fullmatch(r"===== PDF第\d+页 =====", stripped):
            continue
        if "…" in raw or re.search(r"\.{6,}", raw):
            continue
        if re.fullmatch(r"\d+", stripped):
            continue
        if len(stripped) < 24 and re.search(
            r"大学.{0,6}(?:学位论文|博士|硕士)", stripped
        ):
            continue
        visible.append(stripped)
    return visible


def body_headings(
    lines: list[str], pattern: re.Pattern[str]
) -> list[tuple[int, str, str]]:
    candidates: list[tuple[int, str, str]] = []
    for index, raw in enumerate(lines):
        stripped = raw.strip()
        if "…" in raw or re.search(r"\.{6,}", raw):
            continue
        match = pattern.match(stripped)
        if match and re.search(r"[\u4e00-\u9fff]{2}", match.group("title")):
            candidates.append((index, match.group("num"), match.group("title").strip()))
    body_starts = [
        position
        for position, (_, number, title) in enumerate(candidates)
        if number == "1.1" and "背景" in title
    ]
    if not body_starts:
        raise ValueError("could not locate the body 1.1 background heading")
    return candidates[body_starts[-1] :]


def selected_text(
    lines: list[str],
    headings: list[tuple[int, str, str]],
    predicate: object,
) -> str:
    chunks: list[str] = []
    for position, (start, number, title) in enumerate(headings):
        if not predicate(number, title):  # type: ignore[operator]
            continue
        end = headings[position + 1][0] if position + 1 < len(headings) else len(lines)
        chunks.append("\n".join(lines[start + 1 : end]))
    return "\n".join(chunks)


def sequence_stats(text: str) -> dict[str, object]:
    corpus = len(HAN_RE.findall(text))
    counts = {term: text.count(term) for term in SEQUENCE_TERMS}
    densities = {
        term: round(count / corpus * 10000, 2) if corpus else 0.0
        for term, count in counts.items()
    }
    return {
        "corpus": corpus,
        "counts": counts,
        "densities": densities,
        "total_density": round(sum(counts.values()) / corpus * 10000, 2) if corpus else 0.0,
    }


def aggregate_sequence(rows: list[dict[str, object]]) -> dict[str, object]:
    corpus = sum(int(row["corpus"]) for row in rows)
    counts = {
        term: sum(int(row["counts"][term]) for row in rows)  # type: ignore[index]
        for term in SEQUENCE_TERMS
    }
    return {
        "corpus": corpus,
        "counts": counts,
        "densities": {
            term: round(count / corpus * 10000, 2) for term, count in counts.items()
        },
        "total_density": round(sum(counts.values()) / corpus * 10000, 2),
    }


def main() -> None:
    papers: list[dict[str, object]] = []
    section_rows: dict[str, list[dict[str, object]]] = {
        "background": [],
        "organization": [],
        "summary": [],
    }
    for path in sorted(THESIS_DIR.glob("*.txt")):
        lines = path.read_text(encoding="utf-8").splitlines()
        visible_lines = visible_pdf_lines(lines)
        visible_text = "\n".join(visible_lines)
        corpus = len(HAN_RE.findall(visible_text))
        counts = {term: visible_text.count(term) for term in TERM_THRESHOLDS}
        densities = {term: count / corpus * 10000 for term, count in counts.items()}
        throat_hits = sum(bool(THROAT_CLEARING_RE.search(line)) for line in visible_lines)
        papers.append(
            {
                "paper": path.stem,
                "corpus": corpus,
                "term_counts": counts,
                "term_densities": {term: round(value, 2) for term, value in densities.items()},
                "throat_hits": throat_hits,
                "throat_density": round(throat_hits / corpus * 10000, 2),
            }
        )

        simple = body_headings(lines, SIMPLE_HEADING_RE)
        all_headings = body_headings(lines, ANY_HEADING_RE)
        selectors = {
            "background": (
                simple,
                lambda number, title: number.startswith("1.") and "背景" in title,
            ),
            "organization": (
                simple,
                lambda number, title: number.startswith("1.")
                and bool(re.search(r"(?:组织结构|结构安排|论文结构)", title)),
            ),
            "summary": (all_headings, lambda _number, title: "本章小结" in title),
        }
        for kind, (headings, predicate) in selectors.items():
            section_rows[kind].append(sequence_stats(selected_text(lines, headings, predicate)))

    thresholds = {
        term: max(
            2.0,
            round(
                percentile(
                    [float(paper["term_densities"][term]) for paper in papers],  # type: ignore[index]
                    0.9,
                )
                * 1.3,
                1,
            ),
        )
        for term in TERM_THRESHOLDS
    }
    sections = {kind: aggregate_sequence(rows) for kind, rows in section_rows.items()}
    background_density = float(sections["background"]["total_density"])
    organization_factor = round(
        float(sections["organization"]["total_density"]) / background_density, 1
    )
    summary_factor = round(
        float(sections["summary"]["total_density"]) / background_density, 1
    )
    throat_density_values = [float(paper["throat_density"]) for paper in papers]
    throat_p75 = quantiles(throat_density_values, n=4, method="inclusive")[2]

    result = {
        "papers": papers,
        "term_thresholds": thresholds,
        "sections": sections,
        "section_factors": {
            "organization": organization_factor,
            "summary": summary_factor,
            "default": 1.0,
        },
        "throat_clearing": {
            "densities": throat_density_values,
            "p75": round(throat_p75, 2),
            "budget_per_10k": round(throat_p75, 1),
            "min_budget": 1,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
