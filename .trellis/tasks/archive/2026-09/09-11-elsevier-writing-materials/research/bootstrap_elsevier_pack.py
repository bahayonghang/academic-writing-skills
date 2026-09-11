"""Create materials/Elsevier scaffold from research inventory. Run from repo root."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = Path(__file__).resolve().parent / "elsevier-inventory.json"
DST = ROOT / "materials" / "Elsevier"
SCHEMA_SRC = Path(__file__).resolve().parent / "observation-schema.md"

TSV_HEADERS = {
    "writing_rules.tsv": (
        "rule_id\tcategory\tdescription\tpaper_count\tseverity_votes\tseverity"
        "\texemplar_quote\tprimary_section\tevidence\tprior_row\ttop_papers\tstatus\n"
    ),
    "phrase_bank.tsv": (
        "phrase_id\tslot\tphrase\tpaper_count\tusage_note\tevidence"
        "\tprior_row\ttop_papers\tstatus\n"
    ),
    "opener_distribution.tsv": "section\topener_3gram\ttotal_occurrences\tpaper_count\ttop_papers\n",
    "gap_transitions.tsv": (
        "section\tpivot_word\ttemplate\toccurrences\tpaper_count\ttop_papers\texemplar_quotes\n"
    ),
    "hedge_verbs.tsv": "verb\ttier\ttotal_occurrences\tpaper_count\ttop_papers\texemplar_quotes\n",
    "cross_section_linkers.tsv": (
        "from_section\tto_section\tpattern\toccurrences\tpaper_count\ttop_papers\texemplar_quotes\n"
    ),
    "section_openers.tsv": "section\topener_template\ttotal_occurrences\tpaper_count\ttop_papers\n",
    "paper_story_patterns.tsv": (
        "pattern_id\tname\tsection_sequence\telsevier_variant\tpaper_count\tnote\n"
        "SP-ELS-001\tindependent_related\t"
        "abstract->introduction->related_work->method->experiments->conclusion\t"
        "independent Related Work\t0\tcandidate skeleton; not core\n"
        "SP-ELS-002\trelated_inlined\t"
        "abstract->introduction->method->experiments->conclusion\t"
        "related work inlined in introduction\t0\tcandidate skeleton; not core\n"
    ),
    "domain_register.tsv": "domain\tpaper_count\tsecondary_paper_count\tevidence\n",
    "anti_ai_patterns.tsv": (
        "pattern_id\tbanned_phrase\twhy\tsmell_severity\tpaper_count"
        "\tadversarial_count\tevidence\tpapers\n"
    ),
    "cross_section_rules.tsv": (
        "rule_id\tcategory\tdescription\tpaper_count\tseverity\tevidence"
        "\tprior_row\ttop_papers\tstatus\n"
    ),
}

PLACEHOLDER = """# {title}

## 节目标

{objective}

## 已晋升句式

待 core 行填充。
"""


def main() -> None:
    src = json.loads(SRC.read_text(encoding="utf-8"))
    items = []
    for item in src["items"]:
        row = dict(item)
        row["status"] = "pending"
        row["observation"] = None
        items.append(row)
    payload = {
        "count": src["count"],
        "pdf_count": src["pdf_count"],
        "by_venue": src["by_venue"],
        "items": items,
    }
    for sub in (
        DST / "corpus",
        DST / "knowledge",
        DST / "observations",
        DST / "references" / "writing",
        DST / "scripts",
    ):
        sub.mkdir(parents=True, exist_ok=True)
    (DST / "corpus" / "inventory.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    nopf = [i for i in items if not i.get("has_pdf")]
    (DST / "corpus" / "pending-nopf.json").write_text(
        json.dumps(nopf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    shutil.copyfile(SCHEMA_SRC, DST / "observations" / "_schema.md")
    for name, content in TSV_HEADERS.items():
        (DST / "knowledge" / name).write_text(content, encoding="utf-8")
    print(f"scaffold items={len(items)} nopf={len(nopf)} dest={DST}")


if __name__ == "__main__":
    main()
