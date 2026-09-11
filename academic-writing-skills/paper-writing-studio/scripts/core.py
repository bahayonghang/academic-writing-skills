"""Pure core contracts; venue profiles are deliberately supplied by callers."""

import re
from dataclasses import dataclass, field
from typing import Any

SCRIPT_INTERFACE = "internal-module"

VENUES = frozenset({"nature", "ieee", "elsevier", "unspecified"})
SECTION_ALIASES = {
    "method": "methods",
    "methods": "methods",
    "results": "results",
    "experiments": "results",
    "discussion": "discussion",
    "conclusion": "discussion",
    "related_work": "related_work",
    "related-work": "related_work",
}
IEEE_JOURNALS = frozenset(
    {
        "ieee transactions",
        "ieee transactions on industrial informatics",
        "ieee transactions on instrumentation and measurement",
        "ieee transactions on neural networks and learning systems",
    }
)
ELSEVIER_JOURNALS = frozenset(
    {
        "journal of process control",
        "computers & chemical engineering",
        "control engineering practice",
        "isa transactions",
        "chemical engineering science",
        "applied energy",
        "energy",
        "engineering applications of artificial intelligence",
        "expert systems with applications",
        "advanced engineering informatics",
    }
)


@dataclass(frozen=True)
class Selection:
    venue: str
    source: str
    conflicts: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class Section:
    requested: str
    canonical: str


@dataclass
class Result:
    text: str
    text_compact: str
    summary: dict[str, Any] = field(default_factory=dict)


def canonical_section(target: str) -> Section:
    value = target.strip().lower()
    return Section(value, SECTION_ALIASES.get(value, value))


def _journal_profile(journal: str) -> str | None:
    value = " ".join(journal.casefold().split())
    if value in IEEE_JOURNALS or value.startswith("ieee "):
        return "ieee"
    if value in ELSEVIER_JOURNALS:
        return "elsevier"
    return None


def _domain_profile(domain: str) -> str | None:
    value = domain.casefold().strip()
    if value.startswith("ieee:") or value in {"control_ieee", "industrial_informatics"}:
        return "ieee"
    if value.startswith("elsevier:") or value in {
        "process_control",
        "chemical_engineering",
        "industrial_ai",
    }:
        return "elsevier"
    if value in {"general_nature", "nature", "biology_neuro", "medicine_oncology"}:
        return "nature"
    return None


def select_profile(
    *, venue: str | None = None, journal: str | None = None, domain: str | None = None
) -> Selection:
    """Apply explicit venue > journal allowlist > unambiguous domain precedence."""
    explicit = venue.casefold().strip() if venue else None
    journal_profile = _journal_profile(journal or "") if journal else None
    domain_profile = _domain_profile(domain or "") if domain else None
    conflicts: list[str] = []
    if explicit:
        if explicit not in VENUES:
            raise ValueError(f"unsupported venue: {venue}")
        for label, candidate in (("journal", journal_profile), ("domain", domain_profile)):
            if candidate and candidate != explicit:
                conflicts.append(f"{label}={candidate} conflicts with venue={explicit}")
        return Selection(explicit, "explicit venue", tuple(conflicts))
    if journal_profile:
        if domain_profile and domain_profile != journal_profile:
            conflicts.append(f"domain={domain_profile} conflicts with journal={journal_profile}")
        return Selection(journal_profile, "journal allowlist", tuple(conflicts))
    if domain_profile:
        return Selection(domain_profile, "unambiguous domain")
    missing = (
        ("venue/journal/domain",) if not (venue or journal or domain) else ("safe venue mapping",)
    )
    return Selection("unspecified", "neutral baseline", missing_evidence=missing)


_TOKEN = re.compile(
    r"(?:\\cite\{[^}]+\}|\\ref\{[^}]+\}|\[[0-9][^]]*\]|\b\d+(?:\.\d+)?%?|\b[A-Z]{2,}[A-Za-z0-9_-]*\b)"
)


def protected_tokens(text: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(_TOKEN.findall(text)))


def render_result(
    text: str,
    *,
    input_text: str,
    selection: Selection,
    target: str,
    profile_version: str = "unresolved",
    rules_applied: list[str] | None = None,
    patterns_used: list[str] | None = None,
    ai_tells_avoided: list[str] | None = None,
    degraded: bool = False,
    untraceable_tokens: list[str] | None = None,
) -> Result:
    compact = " ".join(text.split())
    if len(compact) > 1:
        compact = compact[: max(1, int(len(compact) * 0.65))].rstrip()
    summary = {
        "venue": selection.venue,
        "profile_version": profile_version,
        "section": canonical_section(target).canonical,
        "domain": None,
        "rules_applied": rules_applied or [],
        "patterns_used": patterns_used or [],
        "evidence_rows": [],
        "ai_tells_avoided": ai_tells_avoided or [],
        "untraceable_tokens": untraceable_tokens or [],
        "degraded": degraded,
        "selection_source": selection.source,
        "conflicts": list(selection.conflicts),
        "missing_evidence": list(selection.missing_evidence),
        "protected_tokens": list(protected_tokens(input_text)),
    }
    return Result(text, compact, summary)
