#!/usr/bin/env python3
"""Calibrate paragraph-arc thresholds on a private LaTeX chapter.

The script prints JSON only. It never copies source prose into the repository:
paragraphs and adjacent pairs are identified by line numbers plus SHA-256
fingerprints. Use ``--show-text`` only for local human labeling.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
ZH_SCRIPTS = REPO_ROOT / "academic-writing-skills" / "latex-thesis-zh" / "scripts"
sys.path.insert(0, str(ZH_SCRIPTS))

import analyze_logic as product_logic  # noqa: E402
from analyze_logic import _thread_tokens  # noqa: E402
from parsers import LatexParser  # noqa: E402

SENTENCE_END_RE = re.compile(r"[。！？；]")
HEADING_RE = re.compile(r"^\\(?:chapter|section|subsection|subsubsection|paragraph)\*?")
BEGIN_ENV_RE = re.compile(r"\\begin\{([^}]+)\}")
END_ENV_RE = re.compile(r"\\end\{([^}]+)\}")
SKIPPED_ENVS = {
    "equation",
    "align",
    "gather",
    "multline",
    "eqnarray",
    "displaymath",
    "figure",
    "table",
    "tabular",
    "algorithm",
    "algorithmic",
    "itemize",
    "enumerate",
    "description",
    "lstlisting",
    "verbatim",
    "minted",
}

JUDGMENT_PREDICATES = ("是", "为", "作为", "属于", "意味着", "表明", "构成")
EMPTY_TRANSITIONS = ("此外", "进一步", "同时", "然而", "但是", "因此", "由此")
RETROSPECTIVE_MARKERS = ("因此", "从而", "由此", "可见", "综上", "说明", "表明", "意味着")
PROSPECTIVE_RE = re.compile(
    r"为(?:后续|下文|本文).{0,20}(?:提供|奠定|创造|打下)|成为|亟需|亟待|难以|无法|意义重大"
)
EXPLICIT_LINK_MARKERS = (
    "上述",
    "该",
    "这一",
    "此",
    "前述",
    "在此基础上",
    "针对上述",
    "基于此",
    "另一条路线",
    "另一组",
    "另一方面",
    "综合",
)


def _fingerprint(text: str) -> str:
    normalized = re.sub(r"\s+", "", text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[。！？；])", text) if part.strip()]


def _han_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def _as_int(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"expected int, got {type(value).__name__}")
    return value


def _as_float(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"expected number, got {type(value).__name__}")
    return float(value)


def _missing_lead(first: str) -> bool:
    han = _han_count(first)
    if han < 20 and not any(token in first for token in JUDGMENT_PREDICATES):
        return True
    for transition in EMPTY_TRANSITIONS:
        if first.startswith(transition):
            remainder = first[len(transition) :].lstrip("，,：:。；; ")
            if _han_count(remainder) < 15:
                return True
    if _han_count(re.sub(r"\\cite\{[^}]+\}", "", first)) < 10 and "\\cite{" in first:
        return True
    without_units = re.sub(r"[\d.%％℃°a-zA-Z\s,，.。:：;；/+-]", "", first)
    return not without_units


def _missing_close(last: str) -> bool:
    return not any(token in last for token in RETROSPECTIVE_MARKERS) and not PROSPECTIVE_RE.search(
        last
    )


def _jaccard(left: str, right: str) -> float:
    left_tokens = _thread_tokens(left)
    right_tokens = _thread_tokens(right)
    union = left_tokens | right_tokens
    return len(left_tokens & right_tokens) / len(union) if union else 0.0


def _split_paragraphs(content: str) -> list[dict[str, object]]:
    parser = LatexParser()
    paragraphs: list[dict[str, object]] = []
    buffer: list[tuple[int, str]] = []
    active_env: str | None = None
    heading_pending = False
    segment = 0

    def flush() -> None:
        nonlocal buffer, heading_pending
        if not buffer:
            return
        visible_lines = [parser.extract_visible_text(line).strip() for _no, line in buffer]
        visible = " ".join(part for part in visible_lines if part)
        sentences = _sentences(visible)
        if _han_count(visible) >= 40 and sentences:
            paragraphs.append(
                {
                    "start": buffer[0][0],
                    "end": buffer[-1][0],
                    "fingerprint": _fingerprint(visible),
                    "visible": visible,
                    "sentences": sentences,
                    "heading_lead": heading_pending,
                    "segment": segment,
                }
            )
        buffer = []
        heading_pending = False

    for line_no, raw in enumerate(content.splitlines(), 1):
        line = re.sub(r"(?<!\\)%.*$", "", raw).strip()
        if active_env is not None:
            end_match = END_ENV_RE.search(line)
            if end_match is not None and end_match.group(1).rstrip("*") == active_env:
                active_env = None
                heading_pending = False
            continue
        begin = BEGIN_ENV_RE.search(line)
        if begin and begin.group(1).rstrip("*") in SKIPPED_ENVS:
            flush()
            segment += 1
            active_env = begin.group(1).rstrip("*")
            if END_ENV_RE.search(line):
                active_env = None
            heading_pending = False
            continue
        if HEADING_RE.match(line):
            flush()
            segment += 1
            heading_pending = True
            continue
        if not line or line == r"\par":
            flush()
            continue
        buffer.append((line_no, line))
    flush()
    return paragraphs


def _double_missing_runs(paragraphs: list[dict[str, object]]) -> list[list[int]]:
    runs: list[list[int]] = []
    active: list[int] = []
    active_segment: int | None = None
    for paragraph in paragraphs:
        segment = _as_int(paragraph["segment"])
        if bool(paragraph["heading_lead"]) or segment != active_segment:
            if active:
                runs.append(active)
            active = []
            active_segment = segment
        if bool(paragraph["heading_lead"]):
            continue
        sentences = paragraph["sentences"]
        assert isinstance(sentences, list)
        first = str(sentences[0])
        last = str(sentences[-1])
        double_missing = _missing_lead(first) and _missing_close(last)
        if double_missing:
            active.append(_as_int(paragraph["start"]))
        elif active:
            runs.append(active)
            active = []
    if active:
        runs.append(active)
    return runs


def _parse_pair(value: str) -> tuple[int, int]:
    try:
        left, right = value.split("->", maxsplit=1)
        return int(left), int(right)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid pair identifier: {value!r}") from exc


def _pair_row(
    left: dict[str, object],
    right: dict[str, object],
    *,
    show_text: bool,
) -> dict[str, object] | None:
    left_sentences = left["sentences"]
    right_sentences = right["sentences"]
    assert isinstance(left_sentences, list) and isinstance(right_sentences, list)
    left_last = str(left_sentences[-1])
    right_first = str(right_sentences[0])
    if _han_count(left_last) < 15 or _han_count(right_first) < 15:
        return None
    row: dict[str, object] = {
        "pair": f"{left['start']}->{right['start']}",
        "left_hash": _fingerprint(left_last),
        "right_hash": _fingerprint(right_first),
        "explicit": any(marker in right_first for marker in EXPLICIT_LINK_MARKERS),
        "jaccard": round(_jaccard(left_last, right_first), 4),
    }
    if show_text:
        row["left_last"] = left_last
        row["right_first"] = right_first
    return row


def _load_labels(
    path: Path,
    *,
    source_sha256: str,
    paragraphs: list[dict[str, object]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    labels = json.loads(path.read_text(encoding="utf-8"))
    if labels.get("source_sha256") != source_sha256:
        raise ValueError("label source_sha256 does not match the input file")

    by_start = {_as_int(paragraph["start"]): paragraph for paragraph in paragraphs}
    labeled_rows: list[dict[str, object]] = []
    for expected in ("positive", "negative"):
        key = f"{expected}_pairs"
        values = labels.get(key)
        if not isinstance(values, list):
            raise ValueError(f"labels must contain a {key} list")
        for item in values:
            if not isinstance(item, dict) or not isinstance(item.get("pair"), str):
                raise ValueError(f"invalid entry in {key}")
            left_start, right_start = _parse_pair(item["pair"])
            try:
                left = by_start[left_start]
                right = by_start[right_start]
            except KeyError as exc:
                raise ValueError(
                    f"labeled pair references an unknown paragraph: {item['pair']}"
                ) from exc
            row = _pair_row(left, right, show_text=False)
            if row is None:
                raise ValueError(
                    f"labeled pair is shorter than the calibration minimum: {item['pair']}"
                )
            row["label"] = expected
            row["basis"] = item.get("basis", "manual-review")
            labeled_rows.append(row)

    budget = labels.get("false_positive_budget", 2)
    if not isinstance(budget, int) or budget < 0:
        raise ValueError("false_positive_budget must be a non-negative integer")
    candidates = sorted({0.0, *(_as_float(row["jaccard"]) for row in labeled_rows)})
    evaluations: list[dict[str, object]] = []
    for threshold in candidates:
        false_positives = sum(
            row["label"] == "positive"
            and not bool(row["explicit"])
            and _as_float(row["jaccard"]) < threshold
            for row in labeled_rows
        )
        negatives_detected = sum(
            row["label"] == "negative"
            and not bool(row["explicit"])
            and _as_float(row["jaccard"]) < threshold
            for row in labeled_rows
        )
        evaluations.append(
            {
                "threshold": round(threshold, 4),
                "positive_false_positives": false_positives,
                "negatives_detected": negatives_detected,
            }
        )
    feasible = [
        evaluation
        for evaluation in evaluations
        if _as_int(evaluation["positive_false_positives"]) <= budget
    ]
    chosen = max(
        feasible,
        key=lambda evaluation: (
            _as_float(evaluation["threshold"]),
            _as_int(evaluation["negatives_detected"]),
        ),
    )
    summary = {
        "method": "largest labeled score with positive false positives <= budget; interface is missing only when jaccard < threshold",
        "rounding": "Jaccard rounded to 4 decimal places before threshold selection and comparison",
        "empty_token_sets": "Jaccard = 0.0",
        "false_positive_budget": budget,
        "chosen_threshold": chosen["threshold"],
        "positive_false_positives": chosen["positive_false_positives"],
        "negatives_detected": chosen["negatives_detected"],
        "negative_total": sum(row["label"] == "negative" for row in labeled_rows),
        "evaluations": evaluations,
    }
    return summary, labeled_rows


def _implementation_g2(
    content: str,
    labels_path: Path,
    *,
    source_sha256: str,
) -> dict[str, object]:
    """Re-run confirmed positive interfaces through the shipped product implementation."""
    labels = json.loads(labels_path.read_text(encoding="utf-8"))
    if labels.get("source_sha256") != source_sha256:
        raise ValueError("label source_sha256 does not match the input file")

    parser = LatexParser()
    sections = parser.split_sections(content)
    paragraphs = product_logic._split_arc_paragraphs(content, parser, sections)
    by_start = {paragraph.start: paragraph for paragraph in paragraphs}
    positions = {paragraph.start: index for index, paragraph in enumerate(paragraphs)}
    terms = product_logic._load_paragraph_arc_terms(ZH_SCRIPTS)
    false_positives: list[dict[str, object]] = []
    evaluated = 0

    positive_pairs = labels.get("positive_pairs")
    if not isinstance(positive_pairs, list):
        raise ValueError("labels must contain a positive_pairs list")
    for item in positive_pairs:
        if not isinstance(item, dict) or not isinstance(item.get("pair"), str):
            raise ValueError("invalid entry in positive_pairs")
        pair = item["pair"]
        left_start, right_start = _parse_pair(pair)
        try:
            left = by_start[left_start]
            right = by_start[right_start]
        except KeyError as exc:
            raise ValueError(
                f"positive pair references an unknown product paragraph: {pair}"
            ) from exc
        if positions[right_start] != positions[left_start] + 1:
            raise ValueError(f"positive pair is not adjacent in the product splitter: {pair}")
        if left.segment_id != right.segment_id:
            raise ValueError(f"positive pair crosses a product prose segment: {pair}")
        if not product_logic._arc_is_eligible(left) or not product_logic._arc_is_eligible(right):
            raise ValueError(f"positive pair is not eligible in the product checker: {pair}")

        evaluated += 1
        missing, score = product_logic._arc_link_missing(left, right, terms)
        if missing:
            false_positives.append(
                {
                    "pair": pair,
                    "left_hash": _fingerprint(left.sentences[-1]),
                    "right_hash": _fingerprint(right.sentences[0]),
                    "jaccard": score,
                }
            )

    report = product_logic._check_paragraph_arc(
        content,
        parser,
        sections,
        [(1, len(content.splitlines()))],
    )
    total_link_findings = sum("[Script] P-ARC-LINK " in line for line in report)
    budget = labels.get("false_positive_budget")
    if not isinstance(budget, int) or budget < 0:
        raise ValueError("false_positive_budget must be a non-negative integer")
    return {
        "implementation": "latex-thesis-zh/scripts/analyze_logic.py product helpers",
        "threshold": product_logic.PARAGRAPH_ARC_LINK_THRESHOLD,
        "positive_pairs_evaluated": evaluated,
        "positive_false_positives": len(false_positives),
        "false_positive_budget": budget,
        "budget_pass": len(false_positives) <= budget,
        "false_positive_pairs": false_positives,
        "full_chapter_link_findings": total_link_findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tex", type=Path)
    parser.add_argument("--labels", type=Path)
    parser.add_argument("--show-text", action="store_true")
    args = parser.parse_args()

    content = args.tex.read_text(encoding="utf-8")
    paragraphs = _split_paragraphs(content)
    eligible = [p for p in paragraphs if not bool(p["heading_lead"])]
    close_hits = 0
    lead_missing = 0
    close_missing = 0
    for paragraph in eligible:
        sentences = paragraph["sentences"]
        assert isinstance(sentences, list)
        first = str(sentences[0])
        last = str(sentences[-1])
        lead_missing += int(_missing_lead(first))
        missing_close = _missing_close(last)
        close_missing += int(missing_close)
        close_hits += int(not missing_close)

    pair_rows: list[dict[str, object]] = []
    for left, right in zip(paragraphs, paragraphs[1:], strict=False):
        if (
            bool(left["heading_lead"])
            or bool(right["heading_lead"])
            or left["segment"] != right["segment"]
        ):
            continue
        row = _pair_row(left, right, show_text=args.show_text)
        if row is not None:
            pair_rows.append(row)

    runs = _double_missing_runs(paragraphs)
    source_sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
    result = {
        "source_name": args.tex.name,
        "source_sha256": source_sha256,
        "paragraphs": len(paragraphs),
        "eligible_paragraphs": len(eligible),
        "heading_leads_exempted": len(paragraphs) - len(eligible),
        "lead_missing": lead_missing,
        "close_marker_hits": close_hits,
        "close_marker_coverage": round(close_hits / len(eligible), 4) if eligible else 0.0,
        "close_missing": close_missing,
        "double_missing_runs": [{"length": len(run), "start_lines": run} for run in runs],
        "max_double_missing_run": max((len(run) for run in runs), default=0),
        "pair_candidates": pair_rows,
    }
    if args.labels is not None:
        threshold, labeled_rows = _load_labels(
            args.labels,
            source_sha256=source_sha256,
            paragraphs=paragraphs,
        )
        result["link_threshold_calibration"] = threshold
        result["labeled_pairs"] = labeled_rows
        result["implementation_g2"] = _implementation_g2(
            content,
            args.labels,
            source_sha256=source_sha256,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
