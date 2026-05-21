"""Build a lightweight claim map for deep-review workflows."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CLAIM_PATTERNS = (
    r"\bwe (?:show|demonstrate|find|propose|introduce|present)\b",
    r"\bour results?\b",
    r"\bthis paper\b",
    r"\bthe main contribution\b",
    r"\bwe conclude\b",
    r"\bwe argue\b",
)

ANCHOR_PATTERNS = {
    "citation": (
        r"\\cite(?:[a-zA-Z*]+)?(?:\[[^\]]*\]){0,2}\{[^}]+\}",
        r"\[[A-Za-z][A-Za-z0-9_-]+(?:\d{4}|;\s*[A-Za-z])?[^\]]*\]",
        r"\b[A-Z][A-Za-z-]+ et al\.\s*\(?\d{4}\)?",
    ),
    "figure_or_table": (
        r"\b(?:Fig\.|Figure|Table|Tab\.|Algorithm|Alg\.|Equation|Eq\.)\s*~?"
        r"(?:\\(?:ref|autoref|cref)\{[^}]+\}|\d+)",
    ),
    "metric": (
        r"\b\d+(?:\.\d+)?\s*(?:%|pp|x|×|ms|s|msec|sec|MB|GB|FLOPs?)(?=\W|$)",
        r"\b(?:accuracy|acc\.|f1|auc|precision|recall|rmse|mae|latency|throughput|"
        r"speedup|error rate|p\s*[<=>]\s*0\.\d+)\b",
    ),
    "section": (r"\b(?:Section|Sec\.|Appendix)\s*~?(?:\\(?:ref|autoref|cref)\{[^}]+\}|\d+)",),
}

STRONG_CLAIM_PATTERN = re.compile(
    r"\b("
    r"state-of-the-art|best|outperform|superior|significant(?:ly)?|prove|guarantee|"
    r"always|never|all|novel|first|comprehensive|broadly|substantial(?:ly)?"
    r")\b",
    re.IGNORECASE,
)


def split_sentences(text: str) -> list[str]:
    """Split text into rough sentences without external dependencies."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text.replace("\n", " "))
    return [part.strip() for part in parts if part.strip()]


def extract_claims(text: str, max_items: int = 5) -> list[str]:
    """Return likely claim-bearing sentences."""
    claims: list[str] = []
    for sentence in split_sentences(text):
        if any(re.search(pattern, sentence, re.IGNORECASE) for pattern in CLAIM_PATTERNS):
            claims.append(sentence)
        if len(claims) >= max_items:
            break
    return claims


def _detect_evidence_anchors(sentence: str) -> list[dict[str, str]]:
    """Return lightweight evidence anchors visible in a claim sentence."""
    anchors: list[dict[str, str]] = []
    for anchor_type, patterns in ANCHOR_PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, sentence, re.IGNORECASE):
                anchors.append({"type": anchor_type, "text": match.group(0)})
    return anchors


def _claim_strength(sentence: str, anchors: list[dict[str, str]]) -> str:
    """Classify claim support from local, script-visible anchors only."""
    anchor_types = {anchor["type"] for anchor in anchors}
    if {"metric", "figure_or_table"} <= anchor_types:
        return "strong"
    if "metric" in anchor_types:
        return "observed"
    if anchors:
        return "supported"
    return "unsupported"


def _missing_evidence(sentence: str, anchors: list[dict[str, str]]) -> list[str]:
    """Describe missing support without pretending the script has read papers."""
    if anchors and "citation" in {anchor["type"] for anchor in anchors}:
        return ["verify that the cited source supports this manuscript sentence"]
    if anchors:
        return []
    if STRONG_CLAIM_PATTERN.search(sentence):
        return [
            "add a citation, figure/table, metric, or section anchor before using strong wording"
        ]
    return ["add an evidence anchor or soften the claim boundary"]


def _allowed_wording(sentence: str, strength: str) -> str:
    """Offer a conservative wording boundary for unsupported or weak claims."""
    if strength in {"strong", "supported"}:
        return sentence

    softened = re.sub(
        r"\bstate-of-the-art performance\b",
        "improved performance in the reported setting",
        sentence,
        flags=re.IGNORECASE,
    )
    softened = re.sub(
        r"\b(?:state-of-the-art|best|superior)\b",
        "improved in the reported setting",
        softened,
        flags=re.IGNORECASE,
    )
    softened = re.sub(r"\bacross all\b", "in the evaluated", softened, flags=re.IGNORECASE)
    softened = re.sub(r"\bprove[s]?\b", "suggests", softened, flags=re.IGNORECASE)
    softened = re.sub(
        r"\bsignificant(?:ly)?\b",
        "reported",
        softened,
        flags=re.IGNORECASE,
    )
    return softened


def _forbidden_wording(sentence: str, strength: str) -> list[str]:
    """List wording families that need explicit evidence."""
    if strength in {"strong", "supported"}:
        return []
    forbidden = []
    if STRONG_CLAIM_PATTERN.search(sentence):
        forbidden.append("unbounded superiority, novelty, or significance wording")
    return forbidden or ["unqualified conclusion without visible evidence"]


def build_claim_candidate(sentence: str, section_key: str, index: int) -> dict:
    """Build an additive claim-candidate record for downstream reviewers."""
    anchors = _detect_evidence_anchors(sentence)
    strength = _claim_strength(sentence, anchors)
    return {
        "id": f"{section_key}:{index + 1}",
        "section_key": section_key,
        "claim": sentence,
        "evidence_anchor": anchors,
        "claim_strength": strength,
        "missing_evidence": _missing_evidence(sentence, anchors),
        "allowed_wording": _allowed_wording(sentence, strength),
        "forbidden_wording": _forbidden_wording(sentence, strength),
    }


def build_claim_map(
    content: str,
    section_index: list[dict],
    section_texts: dict[str, str] | None = None,
    max_items_per_section: int = 5,
) -> dict:
    """Build a minimal section-aware claim map from text and section index."""
    lines = content.splitlines()
    section_claims: dict[str, list[str]] = {}
    section_claim_candidates: dict[str, list[dict]] = {}
    claim_candidates: list[dict] = []
    headline_claims: list[str] = []
    closure_targets: list[str] = []

    for section in section_index:
        section_key = section["section_key"]
        if section_texts and section["section_key"] in section_texts:
            chunk = section_texts[section["section_key"]]
        else:
            start = int(section.get("start_line", 1))
            end = int(section.get("end_line", len(lines)))
            if section.get("line_base", 1) == 0:
                chunk = "\n".join(lines[start : end + 1])
            else:
                chunk = "\n".join(lines[max(0, start - 1) : end])

        claims = extract_claims(chunk, max_items=max_items_per_section)
        if claims:
            section_claims[section_key] = claims
            candidates = [
                build_claim_candidate(claim, section_key=section_key, index=index)
                for index, claim in enumerate(claims)
            ]
            section_claim_candidates[section_key] = candidates
            claim_candidates.extend(candidates)

        if section_key in {"abstract", "introduction"}:
            headline_claims.extend(claims[:max_items_per_section])
        if section_key in {"conclusion", "discussion"}:
            closure_targets.extend(claims[:max_items_per_section])

    return {
        "headline_claims": headline_claims[: max_items_per_section * 2],
        "closure_targets": closure_targets[: max_items_per_section * 2],
        "section_claims": section_claims,
        "claim_candidates": claim_candidates,
        "section_claim_candidates": section_claim_candidates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a claim map from a deep-review workspace")
    parser.add_argument("full_text", help="Path to full_text.md")
    parser.add_argument("section_index", help="Path to section_index.json")
    parser.add_argument("--output", "-o", help="Optional output path")
    args = parser.parse_args()

    full_text = Path(args.full_text).read_text(encoding="utf-8")
    section_index = json.loads(Path(args.section_index).read_text(encoding="utf-8"))
    claim_map = build_claim_map(full_text, section_index)
    payload = json.dumps(claim_map, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
