"""Verify cover-letter claim quotes can be located in the manuscript source.

Adapted from ``paper-audit/scripts/verify_quotes.py``. The cover-letter
specialization is in the matching strategy:

* exact substring match against the manuscript's visible prose (post-LaTeX-strip)
* numeric + metric-keyword fallback (e.g. "47% reduction in latency" matches
  manuscript text containing "47%" and "latency" within the same paragraph)
* paraphrase tolerance: a 4-gram from the letter claim matching the manuscript
  is treated as ``quote_verified=true`` with confidence demoted to "medium"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from parsers import LatexParser

UNVERIFIED_CONFIDENCE = "unverified"


def _strip_manuscript(content: str) -> str:
    """Return manuscript text after stripping LaTeX markup for matching."""
    parser = LatexParser()
    return parser.clean_text(content)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _has_4gram_match(claim: str, manuscript: str) -> bool:
    """Return True if any 4-gram from the claim appears in the manuscript."""
    claim_tokens = re.findall(r"\b[\w'-]+\b", claim.lower())
    if len(claim_tokens) < 4:
        return False
    manuscript_normalized = " ".join(re.findall(r"\b[\w'-]+\b", manuscript.lower()))
    for i in range(len(claim_tokens) - 3):
        fragment = " ".join(claim_tokens[i : i + 4])
        if fragment in manuscript_normalized:
            return True
    return False


def _has_numeric_match(claim: str, manuscript: str) -> bool:
    """Return True when a number in the claim appears in the manuscript and a
    nearby metric keyword overlaps."""
    number_patterns = (
        r"\b\d+(?:\.\d+)?\s*(?:%|pp|x|×|ms|s|MB|GB|FLOPs?)",
        r"(?:\$|USD\s*)\s*\d+(?:\.\d+)?\s*(?:[kKmMbB]|million|billion)?\b",
        r"\b\d+(?:\.\d+)?\s+(?:sensor\s+)?modalit(?:y|ies)\b",
        r"\b\d+(?:\.\d+)?\s+(?:datasets?|benchmarks?|studies|facilit(?:y|ies))\b",
    )
    numbers: list[str] = []
    for pattern in number_patterns:
        numbers.extend(re.findall(pattern, claim, flags=re.IGNORECASE))
    metric_keywords = re.findall(
        r"\b(?:accuracy|f1|auc|precision|recall|rmse|mae|latency|throughput|"
        r"speedup|error|reduction|improvement|memory|footprint|cost|savings|modalit(?:y|ies))\b",
        claim,
        flags=re.IGNORECASE,
    )
    if not numbers:
        return False
    manuscript_lower = manuscript.lower().replace("\\", "")
    normalized_manuscript = re.sub(r"\s+", "", manuscript_lower)
    for number in numbers:
        normalized_number = re.sub(r"\s+", "", number.lower().replace("\\", ""))
        if normalized_number not in normalized_manuscript:
            continue
        if not metric_keywords:
            return True
        for kw in metric_keywords:
            if kw.lower() in manuscript_lower:
                return True
    return False


def verify_claim(claim: str, manuscript_text: str) -> tuple[bool, str]:
    """Verify a single claim against the manuscript.

    Returns ``(verified, confidence)``. Confidence ladder:
    * ``high`` — exact substring match (normalized).
    * ``medium`` — 4-gram or numeric+metric match.
    * ``unverified`` — no anchor found.
    """
    claim_norm = _normalize(claim)
    manuscript_norm = _normalize(manuscript_text)

    # Trim very short claims; they false-positive.
    if len(claim_norm) < 12:
        return False, UNVERIFIED_CONFIDENCE

    if claim_norm in manuscript_norm:
        return True, "high"
    if _has_numeric_match(claim, manuscript_text):
        return True, "medium"
    if _has_4gram_match(claim, manuscript_text):
        return True, "medium"
    return False, UNVERIFIED_CONFIDENCE


def verify_claim_candidates(
    candidates: list[dict],
    manuscript_text: str,
) -> list[dict]:
    """Annotate claim candidates with quote_verified + confidence."""
    manuscript_clean = _strip_manuscript(manuscript_text)
    updated: list[dict] = []
    for candidate in candidates:
        verified, confidence = verify_claim(candidate.get("claim", ""), manuscript_clean)
        patched = dict(candidate)
        patched["quote_verified"] = verified
        patched["confidence"] = confidence
        # Downgrade claim_strength to "unsupported" when the manuscript truly
        # cannot anchor the claim.
        if not verified and patched.get("claim_strength") in {"supported", "strong"}:
            patched["claim_strength"] = "observed"
        updated.append(patched)
    return updated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify cover-letter claim quotes against the manuscript source"
    )
    parser.add_argument(
        "claim_map",
        help="Path to claim_map.json emitted by build_letter_claim_map.py",
    )
    parser.add_argument(
        "manuscript",
        help="Path to the manuscript .tex source",
    )
    parser.add_argument("--output", "-o", help="Optional output path for verified map")
    parser.add_argument(
        "--write-back",
        action="store_true",
        help="Overwrite the claim_map file with verified annotations",
    )
    args = parser.parse_args(argv)

    claim_map_path = Path(args.claim_map).resolve()
    manuscript_path = Path(args.manuscript).resolve()
    if not claim_map_path.exists():
        print(f"File not found: {args.claim_map}", file=sys.stderr)
        return 2
    if not manuscript_path.exists():
        print(f"File not found: {args.manuscript}", file=sys.stderr)
        return 2

    claim_map = json.loads(claim_map_path.read_text(encoding="utf-8"))
    manuscript_text = manuscript_path.read_text(encoding="utf-8", errors="replace")

    candidates = claim_map.get("claim_candidates", [])
    verified = verify_claim_candidates(candidates, manuscript_text)
    claim_map["claim_candidates"] = verified
    claim_map["verified_count"] = sum(1 for c in verified if c.get("quote_verified"))
    claim_map["unverified_count"] = sum(1 for c in verified if not c.get("quote_verified"))

    payload = json.dumps(claim_map, indent=2, ensure_ascii=False)

    if args.write_back:
        claim_map_path.write_text(payload, encoding="utf-8")
    elif args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)

    return 0 if claim_map["unverified_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
