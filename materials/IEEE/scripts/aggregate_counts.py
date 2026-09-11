"""Recount core-rule evidence from complete observations. Rewrites selected TSV rows."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

IEEE_ROOT = Path(__file__).resolve().parent.parent
OBS = IEEE_ROOT / "observations"
KNOW = IEEE_ROOT / "knowledge"

FRONT_PATTERN = re.compile(r"^story_pattern:\s*(\S+)", re.M)
FRONT_STATUS = re.compile(r"^status:\s*(\S+)", re.M)
FRONT_KEY = re.compile(r"^key:\s*(\S+)", re.M)


def load_complete() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for path in sorted(OBS.glob("*.md")):
        if path.name == "_schema.md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        status_m = FRONT_STATUS.search(text)
        if not status_m or status_m.group(1) != "complete":
            continue
        key_m = FRONT_KEY.search(text)
        rows.append((key_m.group(1) if key_m else path.stem, text))
    return rows


def keys_matching(
    papers: list[tuple[str, str]], needle: str, ignore_case: bool = True
) -> list[str]:
    flags = re.I if ignore_case else 0
    found: list[str] = []
    for key, text in papers:
        if re.search(needle, text, flags):
            found.append(key)
    return found


def top(keys: list[str], n: int = 5) -> str:
    return ",".join(keys[:n])


def rewrite_rules(papers: list[tuple[str, str]]) -> None:
    path = KNOW / "writing_rules.tsv"
    rows = list(csv.DictReader(path.open(encoding="utf-8"), delimiter="\t"))
    header = list(rows[0].keys()) if rows else []
    counts = {
        "R002": keys_matching(papers, r"story_pattern:\s*SP-IEEE-002"),
        "R003": keys_matching(papers, r"The rest of this article is organized as follows"),
        "R004": keys_matching(
            papers,
            r"(The main contributions|The primary contributions|Our contributions|key insights and contributions)",
        ),
        "R005": keys_matching(papers, r"future work|future research", ignore_case=True),
        "R006": keys_matching(papers, r"story_pattern:\s*SP-IEEE-001"),
        "R009": keys_matching(papers, r"this article proposes", ignore_case=True),
    }
    for row in rows:
        rid = row.get("rule_id") or ""
        if rid not in counts:
            continue
        keys = counts[rid]
        row["paper_count"] = str(len(keys))
        row["top_papers"] = top(keys)
        row["status"] = "core" if len(keys) >= 3 else "candidate"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print("writing_rules", {k: len(v) for k, v in counts.items()})


def rewrite_phrases(papers: list[tuple[str, str]]) -> None:
    path = KNOW / "phrase_bank.tsv"
    rows = list(csv.DictReader(path.open(encoding="utf-8"), delimiter="\t"))
    header = list(rows[0].keys())
    for row in rows:
        phrase = (row.get("phrase") or "").strip()
        if not phrase:
            continue
        keys = keys_matching(papers, re.escape(phrase), ignore_case=True)
        row["paper_count"] = str(len(keys))
        row["top_papers"] = top(keys)
        row["status"] = "core" if len(keys) >= 3 else "candidate"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    core = sum(1 for r in rows if r.get("status") == "core")
    print(f"phrase_bank core={core} rows={len(rows)}")


def rewrite_story(papers: list[tuple[str, str]]) -> None:
    path = KNOW / "paper_story_patterns.tsv"
    rows = list(csv.DictReader(path.open(encoding="utf-8"), delimiter="\t"))
    header = list(rows[0].keys())
    by_pat: dict[str, list[str]] = defaultdict(list)
    for key, text in papers:
        match = FRONT_PATTERN.search(text)
        if match:
            by_pat[match.group(1)].append(key)
    for row in rows:
        pid = row.get("pattern_id") or ""
        keys = by_pat.get(pid, [])
        row["paper_count"] = str(len(keys))
        if pid == "SP-IEEE-001":
            row["note"] = f"independent Related Work; n={len(keys)}"
        elif pid == "SP-IEEE-002":
            row["note"] = f"related work inlined; n={len(keys)}"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print("story", {k: len(v) for k, v in by_pat.items()})


def rewrite_domain() -> None:
    inv = IEEE_ROOT / "corpus" / "inventory.json"
    import json

    payload = json.loads(inv.read_text(encoding="utf-8"))
    counts: dict[str, int] = defaultdict(int)
    for item in payload["items"]:
        if item.get("status") != "complete":
            continue
        venue = item.get("venue") or "(no venue)"
        counts[venue] += 1
    path = KNOW / "domain_register.tsv"
    lines = ["domain\tpaper_count\tsecondary_paper_count\tevidence\n"]
    for venue, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        domain = venue.replace("IEEE ", "").replace("Transactions on ", "T-")
        lines.append(f"{domain}\t{n}\t\tcomplete observations\n")
    path.write_text("".join(lines), encoding="utf-8")
    print("domains", len(counts))


def main() -> None:
    papers = load_complete()
    print("complete_obs", len(papers))
    rewrite_rules(papers)
    rewrite_phrases(papers)
    rewrite_story(papers)
    rewrite_domain()


if __name__ == "__main__":
    main()
