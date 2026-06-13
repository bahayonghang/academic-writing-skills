"""Build a claim map for a cover letter, scored against manuscript evidence.

Adapted from ``paper-audit/scripts/build_claim_map.py``:
* claim patterns retuned for cover-letter style ("we report," "our work demonstrates," ...)
* accepts ``--manuscript-facts facts.json`` so claim_strength reflects evidence
  visible in the manuscript, not just in the letter itself.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LETTER_CLAIM_PATTERNS = (
    r"\bwe (?:report|present|show|demonstrate|find|propose|introduce|describe|provide)\b",
    r"\bour (?:work|study|method|approach|results?|findings?|manuscript|framework|system)\b",
    r"\bthis (?:work|study|paper|manuscript) (?:reports|presents|describes|introduces|demonstrates)\b",
    r"\bthe (?:main|key|central|primary) contribution\b",
    r"\bwe (?:argue|conclude|claim|establish)\b",
    r"\bthe (?:first|only|main) (?:framework|method|approach|tool|system)\b",
    # Sentences that name a concrete metric or improvement — claim-bearing even
    # when subject is not "we" / "our" (common in cover-letter prose):
    r"\b\d+(?:\.\d+)?\s*(?:%|pp|x|×|ms|MB|GB|FLOPs?)\s*.{0,80}\b(?:reduc\w*|improv\w*|speedup|gain|increas\w*|decreas\w*|faster|better|higher|lower)\b",
    r"\b(?:reduc\w*|improv\w*|speedup|gain|increas\w*|decreas\w*|faster|better|higher|lower)\b.{0,80}\b\d+(?:\.\d+)?\s*(?:%|pp|x|×|ms|MB|GB|FLOPs?)",
    # Domain-count and money claims do not always use an improvement verb but
    # still need manuscript support before appearing in a cover letter.
    r"\b\d+(?:\.\d+)?\s+(?:sensor\s+)?modalit(?:y|ies)\b",
    r"(?:\$|USD\s*)\s*\d+(?:\.\d+)?\s*(?:[kKmMbB]|million|billion)?\b",
    # Deployment / production claims that often appear in cover letters but are
    # easy to overshoot relative to manuscripts:
    r"\b(?:has been |was )?deployed (?:in|to|across)\b",
    r"\b(?:cost savings|adopted by|production use|industrial pilot|pilot studies)\b",
)

ANCHOR_PATTERNS = {
    "citation": (
        r"\\cite(?:[a-zA-Z*]+)?(?:\[[^\]]*\]){0,2}\{[^}]+\}",
        r"\[[A-Z][A-Za-z0-9_-]+(?:\d{4})?[^\]]*\]",
        r"\b[A-Z][A-Za-z-]+ et al\.\s*\(?\d{4}\)?",
    ),
    "figure_or_table": (r"\b(?:Fig\.|Figure|Table|Tab\.|Algorithm|Alg\.|Equation|Eq\.)\s*~?\d+",),
    "metric": (
        r"\b\d+(?:\.\d+)?\s*(?:%|pp|x|×|ms|s|MB|GB|FLOPs?)",
        r"\b\d+(?:\.\d+)?\s+(?:sensor\s+)?modalit(?:y|ies)\b",
        r"(?:\$|USD\s*)\s*\d+(?:\.\d+)?\s*(?:[kKmMbB]|million|billion)?\b",
        r"\b(?:accuracy|f1|auc|precision|recall|rmse|mae|latency|throughput|speedup|"
        r"error rate|memory|footprint|cost savings|p\s*[<=>]\s*0\.\d+)\b",
    ),
    "section": (r"\b(?:Section|Sec\.|Appendix)\s*~?\d+",),
}

STRONG_CLAIM_PATTERN = re.compile(
    r"\b("
    r"state-of-the-art|best|outperform|outperforms|superior|significant(?:ly)?|prove|"
    r"guarantee|always|never|all|novel|first|comprehensive|broadly|substantial(?:ly)?"
    r")\b",
    re.IGNORECASE,
)


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", text.replace("\n", " "))
    return [part.strip() for part in parts if part.strip()]


def extract_claims(text: str, max_items: int | None = None) -> list[str]:
    """Return likely claim-bearing sentences from the cover letter.

    ``max_items=None`` (default) returns every claim sentence so callers can
    report the true total; pass an int to cap the scan.
    """
    claims: list[str] = []
    for sentence in split_sentences(text):
        if any(re.search(p, sentence, re.IGNORECASE) for p in LETTER_CLAIM_PATTERNS):
            claims.append(sentence)
        if max_items is not None and len(claims) >= max_items:
            break
    return claims


def _detect_anchors(text: str) -> list[dict[str, str]]:
    anchors: list[dict[str, str]] = []
    for anchor_type, patterns in ANCHOR_PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                anchors.append({"type": anchor_type, "text": match.group(0)})
    return anchors


def _claim_strength_local(anchors: list[dict[str, str]]) -> str:
    """Claim strength based on local anchors visible inside the sentence."""
    anchor_types = {anchor["type"] for anchor in anchors}
    if {"metric", "figure_or_table"} <= anchor_types:
        return "strong"
    if "metric" in anchor_types:
        return "observed"
    if anchors:
        return "supported"
    return "unsupported"


def _manuscript_supports(
    sentence: str,
    manuscript_facts: dict | None,
) -> tuple[bool, list[dict[str, str]]]:
    """Check whether the manuscript facts blob supports the claim.

    Returns ``(supported, evidence_anchors)``. ``supported`` is True when at
    least one numeric token or contribution string from the manuscript appears
    in the claim sentence, indicating the letter's claim has a matching
    statement in the manuscript.
    """
    if not manuscript_facts:
        return False, []
    anchors: list[dict[str, str]] = []
    lowered = sentence.lower()
    sent_str = " ".join(re.findall(r"\b[\w'-]+\b", lowered))
    # Check headline numbers
    for number in manuscript_facts.get("headline_numbers", []):
        if number.lower() in lowered:
            anchors.append({"type": "metric", "text": number})
    # Check contribution overlap: any shared 4-gram counts as support.
    for contribution in manuscript_facts.get("contributions", []):
        contrib_tokens = re.findall(r"\b[\w'-]+\b", contribution.lower())
        if len(contrib_tokens) < 4:
            continue
        for i in range(len(contrib_tokens) - 3):
            fragment = " ".join(contrib_tokens[i : i + 4])
            if fragment in sent_str:
                anchors.append({"type": "section", "text": contribution[:80]})
                break
    return bool(anchors), anchors


def _missing_evidence(sentence: str, anchors: list[dict[str, str]], supported: bool) -> list[str]:
    if supported:
        return []
    if STRONG_CLAIM_PATTERN.search(sentence):
        return [
            "Strong wording in cover letter; manuscript does not visibly support this claim."
            " Soften, narrow scope, or add a matching statement to the manuscript."
        ]
    if not anchors:
        return ["Add a manuscript-anchored figure, table, metric, or section reference."]
    return []


def _allowed_wording(sentence: str, supported: bool) -> str:
    if supported:
        return sentence

    softened = sentence
    softened = re.sub(
        r"\b(?:with )?reported cost savings of (?:\$|USD\s*)\s*\d+(?:\.\d+)?\s*(?:[kKmMbB]|million|billion)?(?:\s+per\s+\w+)?",
        "with potential operational implications that should be described without a dollar amount unless the manuscript reports it",
        softened,
        flags=re.IGNORECASE,
    )
    softened = re.sub(
        r"\b(?:\$|USD\s*)\s*\d+(?:\.\d+)?\s*(?:[kKmMbB]|million|billion)?\b",
        "a manuscript-supported cost estimate",
        softened,
        flags=re.IGNORECASE,
    )
    softened = re.sub(
        r"\b(?:has been |was )?deployed (?:in|to|across) [^.;]+",
        "was evaluated in the manuscript's reported experimental setting",
        softened,
        flags=re.IGNORECASE,
    )
    softened = re.sub(
        r"\bachieves a \d+(?:\.\d+)?\s*(?:%|pp)\s+reduction in memory footprint\b",
        "shows lower memory use in the evaluated setting",
        softened,
        flags=re.IGNORECASE,
    )
    softened = re.sub(
        r"\b\d+(?:\.\d+)?\s*(?:%|pp)\s+reduction in memory footprint\b",
        "lower memory use in the evaluated setting",
        softened,
        flags=re.IGNORECASE,
    )
    softened = re.sub(
        r"\bsupports \d+(?:\.\d+)?\s+(?:sensor\s+)?modalit(?:y|ies)(?: including [^.;]+)?",
        "was evaluated on the manuscript-reported sensor streams",
        softened,
        flags=re.IGNORECASE,
    )
    softened = re.sub(
        r"\bstate-of-the-art\b",
        "improved in the reported setting",
        softened,
        flags=re.IGNORECASE,
    )
    softened = re.sub(
        r"\b(?:outperforms|surpasses) (?:all\s+)?prior(?: work)?\b",
        "improves over the evaluated baselines",
        softened,
        flags=re.IGNORECASE,
    )
    softened = re.sub(
        r"\b(?:significantly|substantially)\b",
        "measurably",
        softened,
        flags=re.IGNORECASE,
    )
    softened = re.sub(
        r"\bthe first\b",
        "to our knowledge the first",
        softened,
        flags=re.IGNORECASE,
    )
    return softened


def _forbidden_wording(sentence: str, supported: bool) -> list[str]:
    if supported:
        return []
    forbidden = []
    if STRONG_CLAIM_PATTERN.search(sentence):
        forbidden.append("unbounded superiority, novelty, or significance wording")
    return forbidden or ["unqualified conclusion without manuscript-visible evidence"]


def build_claim_candidate(
    sentence: str,
    index: int,
    manuscript_facts: dict | None,
) -> dict:
    """Build an additive claim candidate record."""
    local_anchors = _detect_anchors(sentence)
    supported, m_anchors = _manuscript_supports(sentence, manuscript_facts)
    all_anchors = local_anchors + m_anchors
    local_strength = _claim_strength_local(local_anchors)
    # If manuscript supports, upgrade strength when local was lower
    if supported and local_strength == "unsupported":
        strength = "supported"
    elif supported and local_strength == "supported":
        strength = "strong"
    else:
        strength = local_strength

    return {
        "id": f"letter:{index + 1}",
        "section_key": "letter",
        "claim": sentence,
        "evidence_anchor": all_anchors,
        "claim_strength": strength,
        "missing_evidence": _missing_evidence(sentence, all_anchors, supported),
        "allowed_wording": _allowed_wording(sentence, supported),
        "forbidden_wording": _forbidden_wording(sentence, supported),
        "manuscript_supported": supported,
    }


def build_claim_map(letter_text: str, manuscript_facts: dict | None, max_items: int = 12) -> dict:
    """Build the cover letter claim map.

    Detailed candidates are capped at ``max_items`` to bound work, but the full
    claim-sentence count is reported via ``total_claim_sentences`` and
    ``truncated`` so nothing is silently dropped (claims beyond the cap still
    surface as a count for the caller to act on).
    """
    all_claims = extract_claims(letter_text)
    total = len(all_claims)
    claims = all_claims[:max_items]
    candidates = [
        build_claim_candidate(claim, index=i, manuscript_facts=manuscript_facts)
        for i, claim in enumerate(claims)
    ]
    return {
        "letter_claims": claims,
        "claim_candidates": candidates,
        "total_claim_sentences": total,
        "truncated": total > max_items,
        "manuscript_supported_count": sum(1 for c in candidates if c.get("manuscript_supported")),
        "unsupported_count": sum(1 for c in candidates if c.get("claim_strength") == "unsupported"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a cover-letter claim map against manuscript evidence"
    )
    parser.add_argument("letter", help="Path to cover letter (.md or .tex)")
    parser.add_argument(
        "--manuscript-facts",
        help="Path to facts.json emitted by extract_manuscript_facts.py",
    )
    parser.add_argument("--output", "-o", help="Optional output path")
    args = parser.parse_args(argv)

    letter_path = Path(args.letter).resolve()
    if not letter_path.exists():
        print(f"File not found: {args.letter}", file=sys.stderr)
        return 2

    letter_text = letter_path.read_text(encoding="utf-8", errors="replace")

    manuscript_facts = None
    if args.manuscript_facts:
        facts_path = Path(args.manuscript_facts).resolve()
        if not facts_path.exists():
            print(f"Manuscript facts file not found: {args.manuscript_facts}", file=sys.stderr)
            return 2
        manuscript_facts = json.loads(facts_path.read_text(encoding="utf-8"))

    claim_map = build_claim_map(letter_text, manuscript_facts)
    payload = json.dumps(claim_map, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)

    return 1 if claim_map["unsupported_count"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
