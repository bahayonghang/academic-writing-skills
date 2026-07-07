#!/usr/bin/env python3
"""
De-AI Writing Trace Checker for English Academic Papers
Analyzes LaTeX/Typst source code for AI writing patterns.

Usage:
    uv run python -B deai_check.py main.tex --section introduction
    uv run python -B deai_check.py main.tex --analyze
    uv run python -B deai_check.py main.tex --fix-suggestions
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Import local parsers
try:
    from parsers import get_parser, resolve_section_keys
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from parsers import get_parser, resolve_section_keys


# --- AI tone thresholds (data-driven via references/deai/tone-thresholds.yaml) ---

THRESHOLDS_FILENAME = "tone-thresholds.yaml"

# Sections whose narration defaults to past tense; the tense checker only fires here.
TENSE_SECTIONS = frozenset({"method", "experiment", "result"})

DEFAULT_THRESHOLDS = {
    "term_thresholds": {
        "significant": 5,
        "comprehensive": 3,
        "effective": 5,
        "novel": 4,
        "robust": 4,
        "important": 5,
        "various": 5,
        "several": 5,
        "numerous": 3,
        "furthermore": 3,
        "moreover": 3,
        "notably": 3,
        "remarkable": 3,
        "remarkably": 3,
        "obvious": 3,
        "obviously": 3,
        "clearly": 4,
    },
    "burstiness": {
        "consecutive_paragraphs": 3,
        "opening_token_count": 2,
    },
    "throat_clearing": {
        "patterns": [
            r"^In order to better\b",
            r"^In this (?:section|chapter|paper|work),\s+we\b",
            r"^It is worth (?:noting|mentioning) that\b",
            r"^It should be noted that\b",
            r"^As (?:mentioned|stated|discussed) (?:earlier|before|above|previously)\b",
            r"^Notably,",
            r"^Furthermore,",
            r"^Moreover,",
            r"^In summary,",
            r"^To summarize,",
        ],
    },
    "punctuation": {
        "max_em_dashes_per_doc": 5,
        "ban_exclamation_in_body": True,
    },
    # Over-claim phrases: a focused set of unambiguous causal / firstness /
    # universality / application tells. Phrase-level only (term-count words like
    # novel/robust/comprehensive are handled by term_thresholds, not here).
    # See references/evidence/over-claim-guard.md for the full judgment tables.
    "overclaim": {
        "enabled": True,
        "patterns": {
            r"\bcaused by\b": "soften_causal",
            r"\bdetermines\b": "soften_causal",
            r"\bproves that\b": "soften_causal",
            r"\bfor the first time\b": "qualify_novelty",
            r"\bunprecedented\b": "qualify_novelty",
            r"\buniversally\b": "bound_universal",
            r"\bin all cases\b": "bound_universal",
            r"\bin every case\b": "bound_universal",
            r"\bwill revolutionize\b": "hedge_application",
        },
    },
    # Tense signal words: present-tense reporting verbs that usually signal a
    # past-tense violation when they narrate Methods / Experiments / Results.
    # "is" / "are" are intentionally excluded (too many valid uses); "presents"
    # matches the verb only, not the adjective in "the present study". See the
    # judgment-level checklist in references/modules/tense-guide.md.
    "tense": {
        "enabled": True,
        "present_signals": {
            r"\bshows?\b": "past_in_methods_results",
            r"\breveals?\b": "past_in_methods_results",
            r"\bdemonstrates?\b": "past_in_methods_results",
            r"\bindicates?\b": "past_in_methods_results",
            r"\bpresents\b": "past_in_methods_results",
            r"\bconfirms?\b": "past_in_methods_results",
            r"\bachieves?\b": "past_in_methods_results",
            r"\boutperforms?\b": "past_in_methods_results",
        },
    },
    # D1 (sentence-length uniformity): low coefficient of variation across
    # sentence lengths reads as machine-even. Only consulted when --tier is set.
    "sentence_length": {
        "min_sentences": 5,
        "cv_threshold": 0.30,
    },
}


def _load_thresholds(script_dir: Path) -> dict:
    """Load tone thresholds from references/deai/tone-thresholds.yaml.

    The YAML file is an optional user-overridable layer on top of
    DEFAULT_THRESHOLDS. When absent, the defaults are used as-is.
    Partial overrides are merged per-key so a user can tune one threshold
    without restating the others. PyYAML is optional: if it is not installed
    the defaults are used and a one-line notice is printed to stderr (E3).
    """
    merged = {
        k: (dict(v) if isinstance(v, dict) else list(v)) for k, v in DEFAULT_THRESHOLDS.items()
    }
    yaml_path = script_dir.parent / "references" / "deai" / THRESHOLDS_FILENAME
    if not yaml_path.exists():
        return merged

    try:
        import yaml  # PyYAML; optional override layer
    except ImportError:
        print(
            f"[deai] PyYAML not installed; using built-in default thresholds "
            f"(ignoring {THRESHOLDS_FILENAME})",
            file=sys.stderr,
        )
        return merged

    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{THRESHOLDS_FILENAME} must contain a top-level mapping")
    for k, v in data.items():
        if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
            merged[k].update(v)
        else:
            merged[k] = v
    return merged


# --- Tier scaling + AIGC detection-dimension labels (only used when --tier set) ---
#
# Dimensions follow the five generic AIGC stylistic axes (readability-oriented,
# NOT tuned to evade any specific detector):
#   D1 sentence-length variety / D2 paragraph structure /
#   D3 information density / D4 connector frequency / D5 term-context matching.

DIMENSION_MAP = {
    "sentence_length": "D1",
    "burstiness": "D2",
    "throat_clearing": "D2",
    "punctuation": "D2",
    "binary_contrast_shell": "D2",
    "lecture_colon": "D2",
    "low_information_density": "D3",
    "term_threshold": "D4",
    "empty_phrase": "D5",
    "vague_quantifier": "D5",
    "vague_referent": "D5",
    "template_expr": "D5",
    "fake_insight_marker": "D5",
    "over_confident": "D5",
    "overclaim": "D5",
}

TEACHING_NOTES = {
    "D1": "Uniform sentence lengths read as machine-even; vary short and long sentences.",
    "D2": "Repeated paragraph openings / boilerplate leads / heavy em-dashes signal templated prose.",
    "D3": "Long passages with little evidence look padded; add concrete methods, numbers, comparisons.",
    "D4": "Over-frequent connectors (furthermore/moreover/...) are a strong AI-tone tell.",
    "D5": "Generic praise words detached from specifics are the most common AI fingerprint.",
}

_TIER_FACTORS = {
    # term cap multiplier, cv-threshold multiplier, em-dash cap multiplier
    "light": (1.5, 0.7, 1.6),
    "medium": (1.0, 1.0, 1.0),
    "heavy": (0.6, 1.4, 0.6),
}


def _apply_tier(thresholds: dict, tier: str) -> dict:
    """Scale thresholds by aggressiveness. ``medium`` is a no-op (current
    behavior); ``light`` flags fewer items, ``heavy`` flags more."""
    if tier == "medium" or tier not in _TIER_FACTORS:
        return thresholds
    term_factor, cv_factor, em_factor = _TIER_FACTORS[tier]
    scaled = {
        k: (dict(v) if isinstance(v, dict) else list(v) if isinstance(v, list) else v)
        for k, v in thresholds.items()
    }
    for word, cap in scaled.get("term_thresholds", {}).items():
        scaled["term_thresholds"][word] = max(1, int(round(cap * term_factor)))
    sentence_cfg = scaled.get("sentence_length", {})
    if "cv_threshold" in sentence_cfg:
        sentence_cfg["cv_threshold"] = round(sentence_cfg["cv_threshold"] * cv_factor, 3)
    punctuation_cfg = scaled.get("punctuation", {})
    if "max_em_dashes_per_doc" in punctuation_cfg:
        punctuation_cfg["max_em_dashes_per_doc"] = max(
            1, int(round(punctuation_cfg["max_em_dashes_per_doc"] * em_factor))
        )
    return scaled


class AITraceChecker:
    """Detect AI writing traces."""

    # High-priority AI patterns (Category 1: Empty phrases)
    EMPTY_PHRASES = {
        r"\bsignificant\s+(?:improvement|performance|gain|enhancement|advancement)\b": "quantify",
        r"\bcomprehensive\s+(?:analysis|study|overview|survey|review)\b": "list_scope",
        r"\beffective\s+(?:solution|method|approach|technique)\b": "compare_baseline",
        r"\bimportant\s+(?:contribution|role|impact|implication)\b": "explain_why",
        r"\brobust\s+(?:performance|method|approach)\b": "specify_condition",
        r"\bnovel\s+(?:approach|method|technique|algorithm)\b": "explain_novelty",
        r"\bstate-of-the-art\s+(?:performance|results|accuracy)\b": "cite_sota",
    }

    # High-priority AI patterns (Category 2: Over-confident)
    OVER_CONFIDENT = {
        r"\bobviously\b": "hedge",
        r"\bclearly\b": "hedge",
        r"\bcertainly\b": "hedge",
        r"\bundoubtedly\b": "hedge",
        r"\bnecessarily\b": "condition",
        r"\bcompletely\b": "limit",
        r"\balways\b": "frequency",
        r"\bnever\b": "frequency",
    }

    # High-priority AI patterns (Category 4: Vague quantification)
    VAGUE_QUANTIFIERS = {
        r"\bmany\s+studies\b": "cite_specific",
        r"\bnumerous\s+experiments?\b": "quantify_exp",
        r"\bvarious\s+methods?\b": "list_methods",
        r"\bseveral\s+approaches?\b": "list_methods",
        r"\bmultiple\s+(?:datasets?|methods?|experiments?)\b": "quantify_items",
        r"\ba\s+(?:lot|large\s+number)\s+of\b": "quantify",
        r"\bthe\s+majority\s+of\b": "quantify_percent",
        r"\bsubstantial\s+(?:amount|number|gain|improvement)\b": "quantify",
    }

    # Medium-priority AI patterns (Category 3: Template expressions)
    TEMPLATE_EXPRESSIONS = {
        r"\bin\s+recent\s+years\b": "specific_time",
        r"\bmore\s+and\s+more\b": "increasingly",
        r"\bplays?\s+an?\s+important\s+role\b": "specific_impact",
        r"\bwith\s+the\s+(?:rapid\s+)?development\s+of\b": "context_direct",
        r"\bhas\s+(?:been\s+)?widely\s+used\b": "cite_examples",
        r"\bhas\s+attracted\s+(?:much\s+)?attention\b": "cite_examples",
    }

    BINARY_CONTRAST_SHELLS = {
        r"\bnot\s+(?:merely|only)\b.{1,80}?\bbut\b(?:\s+also\b)?": ("clarify_contrast_axis"),
        r"\brather\s+than\b.{1,80}?,": "clarify_contrast_axis",
        r"\binstead\s+of\b.{1,80}?,": "clarify_contrast_axis",
    }

    FAKE_INSIGHT_MARKERS = {
        r"\bessentially\b": "state_evidence_claim",
        r"\bin fact\b": "state_evidence_claim",
        r"\bthe key is\b": "state_evidence_claim",
        r"\bit is important to note\b": "state_evidence_claim",
        r"\bmore importantly\b": "state_evidence_claim",
    }

    LECTURE_COLON = {
        r"\b(?:The conclusion is|The reason is simple|The key point is):": (
            "rewrite_lecture_setup"
        ),
    }

    VAGUE_REFERENTS = {
        r"\bthings\b": "name_academic_referent",
        r"\baspects\b": "name_academic_referent",
        r"\bfactors\b": "name_academic_referent",
        r"\bThis\s+(?:shows|means|suggests|indicates|demonstrates)\b": ("name_academic_referent"),
    }

    EVIDENCE_MARKERS = re.compile(r"(\\cite\{|@\w+|\b\d+(?:\.\d+)?%?\b|\[[0-9,\s]+\])")
    ACADEMIC_CONTRAST_MARKERS = re.compile(
        r"(baseline|dataset|metric|experiment|table|figure|compared|comparison|"
        r"accuracy|MAE|RMSE|F1|p\s*[<>=])",
        re.IGNORECASE,
    )
    REPEATED_OPENING_RE = re.compile(r"^[A-Za-z]+(?:\s+[A-Za-z]+)?")

    def __init__(self, file_path: Path, tier: str | None = None):
        self.file_path = file_path
        self.content = file_path.read_text(encoding="utf-8", errors="ignore")
        self.lines = self.content.split("\n")
        self.parser = get_parser(file_path)
        self.section_ranges = self.parser.split_sections(self.content)
        self.comment_prefix = self.parser.get_comment_prefix()
        self.tier = tier
        self.thresholds = _load_thresholds(Path(__file__).parent)
        if tier:
            self.thresholds = _apply_tier(self.thresholds, tier)
        self._throat_clearing_re = [
            re.compile(p, re.IGNORECASE) for p in self.thresholds["throat_clearing"]["patterns"]
        ]
        overclaim_cfg = self.thresholds.get("overclaim", {})
        self._overclaim_enabled = bool(overclaim_cfg.get("enabled", True))
        self._overclaim_patterns = list(overclaim_cfg.get("patterns", {}).items())
        tense_cfg = self.thresholds.get("tense", {})
        self._tense_enabled = bool(tense_cfg.get("enabled", True))
        self._tense_signals = list(tense_cfg.get("present_signals", {}).items())
        # Present tense is fine when the subject is a figure/table/equation;
        # skip a match when such a reference sits just before the verb.
        self._tense_fp_re = re.compile(
            r"\b(?:figures?|fig|tables?|tab|equations?|eq|algorithms?|schemes?|listings?)\b"
            r"\.?\s*~?\s*\d*",
            re.IGNORECASE,
        )

    def _is_false_positive(self, match_obj, text: str, pattern: str) -> bool:
        """Check context to rule out false positives."""
        start, end = match_obj.span()

        # Look ahead context (next 50 chars)
        context_after = text[end : end + 50]
        # Look behind context (prev 50 chars)
        context_before = text[max(0, start - 50) : start]

        # 1. "significant" followed by p-value or statistical terms
        if "significant" in pattern:
            if re.search(r"statistically", context_before, re.IGNORECASE):
                return True
            if re.search(r"p\s*[<>=]\s*0\.\d+", context_after):
                return True
            if re.search(r"at\s+the\s+0\.\d+\s+level", context_after):
                return True

        # 2. "improvement" followed by percentage or number
        if "improvement" in pattern or "gain" in pattern:
            if re.search(r"by\s+\d+(?:\.\d+)?%", context_after):
                return True
            if re.search(r"of\s+\d+(?:\.\d+)?%", context_after):
                return True

        # 3. "comprehensive" followed by range
        if "comprehensive" in pattern and "from" in context_after and "to" in context_after:
            return True

        matched_text = text[start:end]
        window = context_before + matched_text + context_after
        return bool(
            re.search(
                r"\b(?:not\s+(?:merely|only)|rather\s+than|instead\s+of)\b",
                matched_text,
                re.IGNORECASE,
            )
            and self.EVIDENCE_MARKERS.search(window)
            and self.ACADEMIC_CONTRAST_MARKERS.search(window)
        )

    def _find_pattern_in_section(
        self, pattern: str, suggestion_type: str, section_name: str, category: str
    ) -> list[dict]:
        """Find pattern occurrences in a specific section."""
        if section_name not in self.section_ranges:
            return []

        start, end = self.section_ranges[section_name]
        matches = []

        for i in range(start - 1, min(end, len(self.lines))):
            line = self.lines[i]
            stripped = line.strip()

            # Skip comments
            if stripped.startswith(self.comment_prefix):
                continue

            visible_text = self.parser.extract_visible_text(stripped)

            for match in re.finditer(pattern, visible_text, re.IGNORECASE):
                # Context check
                if self._is_false_positive(match, visible_text, pattern):
                    continue

                matches.append(
                    {
                        "line": i + 1,
                        "text": visible_text,
                        "original": stripped,
                        "pattern": pattern,
                        "category": category,
                        "section": section_name,
                        "suggestion_type": suggestion_type,
                    }
                )

        return matches

    def check_section(self, section_name: str) -> dict:
        """Check a specific section for AI traces."""
        results = {
            "section": section_name,
            "total_lines": 0,
            "trace_count": 0,
            "traces": [],
        }

        if section_name not in self.section_ranges:
            start, end = 1, len(self.lines)
        else:
            start, end = self.section_ranges[section_name]

        results["total_lines"] = end - start + 1

        all_patterns = [
            ("empty_phrase", self.EMPTY_PHRASES),
            ("over_confident", self.OVER_CONFIDENT),
            ("vague_quantifier", self.VAGUE_QUANTIFIERS),
            ("template_expr", self.TEMPLATE_EXPRESSIONS),
            ("binary_contrast_shell", self.BINARY_CONTRAST_SHELLS),
            ("fake_insight_marker", self.FAKE_INSIGHT_MARKERS),
            ("lecture_colon", self.LECTURE_COLON),
            ("vague_referent", self.VAGUE_REFERENTS),
        ]

        for category, patterns_dict in all_patterns:
            for pattern, suggestion_type in patterns_dict.items():
                matches = self._find_pattern_in_section(
                    pattern, suggestion_type, section_name, category
                )
                results["traces"].extend(matches)

        results["traces"].extend(self._check_low_information_density(section_name))
        results["traces"].extend(self._check_burstiness(section_name))
        results["traces"].extend(self._check_throat_clearing(section_name))
        results["traces"].extend(self._check_overclaim(section_name))
        results["traces"].extend(self._check_tense(section_name))
        if self.tier:
            results["traces"].extend(self._check_sentence_length_variance(section_name))
        results["trace_count"] = len(results["traces"])
        return results

    def _check_low_information_density(self, section_name: str) -> list[dict]:
        """Detect long, content-light sections that rely on boilerplate without evidence."""
        if section_name not in self.section_ranges:
            return []

        start, end = self.section_ranges[section_name]
        visible_lines: list[tuple[int, str]] = []
        raw_lines: list[str] = []
        for i in range(start - 1, min(end, len(self.lines))):
            stripped = self.lines[i].strip()
            if not stripped or stripped.startswith(self.comment_prefix):
                continue
            raw_lines.append(stripped)
            visible = self.parser.extract_visible_text(stripped)
            if visible:
                visible_lines.append((i + 1, visible))

        if len(visible_lines) < 3:
            return []

        text = " ".join(text for _, text in visible_lines)
        # Evidence markers (\cite{}, @keys, numbers, [1,2]) must be matched on the
        # RAW source: extract_visible_text strips \cite{} and bracket refs, so a
        # citation-dense paragraph would otherwise read as evidence-free (E17).
        raw_text = " ".join(raw_lines)
        boilerplate_hits = 0
        for patterns_dict in (
            self.EMPTY_PHRASES,
            self.VAGUE_QUANTIFIERS,
            self.TEMPLATE_EXPRESSIONS,
        ):
            boilerplate_hits += sum(
                1 for pattern in patterns_dict if re.search(pattern, text, re.IGNORECASE)
            )

        if boilerplate_hits < 2 or self.EVIDENCE_MARKERS.search(raw_text):
            return []

        openings: list[str] = []
        for _, visible in visible_lines:
            match = self.REPEATED_OPENING_RE.search(visible)
            if match:
                openings.append(match.group(0).lower())
        repeated_opening = any(openings.count(opening) >= 2 for opening in set(openings))

        if not repeated_opening and len(text.split()) < 60:
            return []

        return [
            {
                "line": visible_lines[0][0],
                "text": text[:160],
                "original": "",
                "pattern": "low_information_density",
                "category": "low_information_density",
                "section": section_name,
                "suggestion_type": "increase_information_density",
            }
        ]

    # --- Checker: D1 sentence-length uniformity (tier-gated) ----------------

    def _check_sentence_length_variance(self, section_name: str) -> list[dict]:
        """Flag sections whose sentence lengths are suspiciously uniform.

        Human prose is bursty (a mix of short and long sentences); AI prose
        tends toward an even cadence. We measure the coefficient of variation
        (stddev / mean) of sentence word counts and flag when it falls below the
        configured threshold. Tier-gated so the default output is unchanged.
        """
        cfg = self.thresholds.get("sentence_length", {})
        min_sentences = int(cfg.get("min_sentences", 5))
        cv_threshold = float(cfg.get("cv_threshold", 0.30))

        paragraphs = self._iter_section_paragraphs(section_name)
        if not paragraphs:
            return []
        text = " ".join(visible for para in paragraphs for _, visible in para)
        sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
        lengths = [len(s.split()) for s in sentences if s.split()]
        if len(lengths) < min_sentences:
            return []

        mean = sum(lengths) / len(lengths)
        if mean <= 0:
            return []
        variance = sum((value - mean) ** 2 for value in lengths) / len(lengths)
        cv = (variance**0.5) / mean
        if cv >= cv_threshold:
            return []

        return [
            {
                "line": paragraphs[0][0][0],
                "text": (
                    f"sentence-length CV={cv:.2f} over {len(lengths)} sentences "
                    f"(threshold {cv_threshold})"
                ),
                "original": "",
                "pattern": "sentence_length_uniformity",
                "category": "sentence_length",
                "section": section_name,
                "suggestion_type": "vary_sentence_length",
            }
        ]

    # --- Paragraph helper for burstiness / throat_clearing -------------------

    def _iter_section_paragraphs(self, section_name: str) -> list[list[tuple[int, str]]]:
        """Group a section's visible lines into paragraphs.

        A paragraph is a run of non-blank, non-comment lines whose
        extract_visible_text() is non-empty. Blank or comment-only lines
        separate paragraphs.
        """
        if section_name not in self.section_ranges:
            return []
        start, end = self.section_ranges[section_name]

        paragraphs: list[list[tuple[int, str]]] = []
        current: list[tuple[int, str]] = []
        for i in range(start - 1, min(end, len(self.lines))):
            stripped = self.lines[i].strip()
            if not stripped or stripped.startswith(self.comment_prefix):
                if current:
                    paragraphs.append(current)
                    current = []
                continue
            visible = self.parser.extract_visible_text(stripped).strip()
            if not visible:
                continue
            current.append((i + 1, visible))
        if current:
            paragraphs.append(current)
        return paragraphs

    # --- Checker: burstiness (parallel paragraph openings) ------------------

    def _check_burstiness(self, section_name: str) -> list[dict]:
        cfg = self.thresholds["burstiness"]
        window = max(2, int(cfg.get("consecutive_paragraphs", 3)))
        k = max(1, int(cfg.get("opening_token_count", 2)))

        paragraphs = self._iter_section_paragraphs(section_name)
        if len(paragraphs) < window:
            return []

        def opening_key(para: list[tuple[int, str]]) -> str:
            first_text = para[0][1]
            tokens = re.findall(r"[A-Za-z][A-Za-z'-]*", first_text)
            return " ".join(t.lower() for t in tokens[:k])

        traces: list[dict] = []
        reported_starts: set[int] = set()
        for i in range(len(paragraphs) - window + 1):
            window_paras = paragraphs[i : i + window]
            keys = [opening_key(p) for p in window_paras]
            if not keys[0]:
                continue
            if len(set(keys)) == 1 and window_paras[0][0][0] not in reported_starts:
                reported_starts.add(window_paras[0][0][0])
                traces.append(
                    {
                        "line": window_paras[0][0][0],
                        "text": (f"{window} consecutive paragraphs open with '{keys[0]}'"),
                        "original": window_paras[0][0][1],
                        "pattern": "burstiness:parallel_opening",
                        "category": "burstiness",
                        "section": section_name,
                        "suggestion_type": "parallel_opening",
                    }
                )
        return traces

    # --- Checker: throat-clearing paragraph leads ---------------------------

    def _check_throat_clearing(self, section_name: str) -> list[dict]:
        if not self._throat_clearing_re:
            return []
        paragraphs = self._iter_section_paragraphs(section_name)
        traces: list[dict] = []
        for para in paragraphs:
            line_no, first_text = para[0]
            for compiled in self._throat_clearing_re:
                if compiled.search(first_text):
                    traces.append(
                        {
                            "line": line_no,
                            "text": first_text[:160],
                            "original": first_text,
                            "pattern": f"throat_clearing:{compiled.pattern}",
                            "category": "throat_clearing",
                            "section": section_name,
                            "suggestion_type": "throat_clearing",
                        }
                    )
                    break
        return traces

    # --- Checker: over-claim phrases (YAML-driven, [Script] LOW) -------------

    def _check_overclaim(self, section_name: str) -> list[dict]:
        """Flag unambiguous over-claim phrases (causal / firstness / universality /
        application). Phrase-level only; reuses the section pattern finder so the
        existing comment/visible-text/false-positive handling applies. Disabled
        when ``overclaim.enabled`` is false in the thresholds."""
        if not self._overclaim_enabled:
            return []
        traces: list[dict] = []
        for pattern, suggestion_type in self._overclaim_patterns:
            traces.extend(
                self._find_pattern_in_section(pattern, suggestion_type, section_name, "overclaim")
            )
        return traces

    # --- Checker: tense signal words (YAML-driven, [Script] LOW) -------------

    def _check_tense(self, section_name: str) -> list[dict]:
        """Flag present-tense reporting verbs in Methods / Experiments / Results,
        where past tense is the convention. Gated to those sections; ``is`` /
        ``are`` are intentionally not checked (see modules/tense-guide.md).
        Disabled when ``tense.enabled`` is false in the thresholds."""
        if not self._tense_enabled:
            return []
        if section_name.split("_", 1)[0] not in TENSE_SECTIONS:
            return []
        if section_name not in self.section_ranges:
            return []
        start, end = self.section_ranges[section_name]
        traces: list[dict] = []
        for i in range(start - 1, min(end, len(self.lines))):
            stripped = self.lines[i].strip()
            if not stripped or stripped.startswith(self.comment_prefix):
                continue
            visible_text = self.parser.extract_visible_text(stripped)
            for pattern, suggestion_type in self._tense_signals:
                for match in re.finditer(pattern, visible_text, re.IGNORECASE):
                    if self._tense_false_positive(visible_text, match.start()):
                        continue
                    traces.append(
                        {
                            "line": i + 1,
                            "text": visible_text,
                            "original": stripped,
                            "pattern": pattern,
                            "category": "tense",
                            "section": section_name,
                            "suggestion_type": suggestion_type,
                        }
                    )
        return traces

    def _tense_false_positive(self, text: str, match_start: int) -> bool:
        """Present tense is correct when the subject is a figure/table/equation
        (``Figure 2 shows ...``). Treat a nearby such reference as a false positive."""
        before = text[:match_start]
        return bool(self._tense_fp_re.search(before[-48:]))

    # --- Document-level visible-text helper ---------------------------------

    def _iter_visible_lines(self) -> list[tuple[int, str, str]]:
        """Yield (line_no, section_name, visible_text) for every non-blank,
        non-comment line in the document.
        """
        out: list[tuple[int, str, str]] = []
        section_lookup: dict[int, str] = {}
        for name, (start, end) in self.section_ranges.items():
            for ln in range(start, min(end, len(self.lines)) + 1):
                section_lookup.setdefault(ln, name)
        for i, line in enumerate(self.lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith(self.comment_prefix):
                continue
            visible = self.parser.extract_visible_text(stripped).strip()
            if not visible:
                continue
            out.append((i, section_lookup.get(i, "document"), visible))
        return out

    # --- Checker: term overuse (document-level word-count threshold) --------

    def _check_term_threshold(self) -> list[dict]:
        term_caps: dict[str, int] = {
            w.lower(): int(n) for w, n in self.thresholds["term_thresholds"].items()
        }
        if not term_caps:
            return []
        visible_lines = self._iter_visible_lines()
        word_re = re.compile(r"\b[A-Za-z][A-Za-z'-]*\b")
        # word -> (count, first_line_no, first_section)
        counts: dict[str, list] = {}
        for line_no, section, text in visible_lines:
            for m in word_re.finditer(text):
                w = m.group(0).lower()
                if w not in term_caps:
                    continue
                if w not in counts:
                    counts[w] = [0, line_no, section]
                counts[w][0] += 1
        traces: list[dict] = []
        for word, (count, first_line, section) in counts.items():
            cap = term_caps[word]
            if count <= cap:
                continue
            traces.append(
                {
                    "line": first_line,
                    "text": f"'{word}' used {count} times (cap {cap})",
                    "original": "",
                    "pattern": f"term_threshold:{word}",
                    "category": "term_threshold",
                    "section": section,
                    "suggestion_type": "term_overuse",
                }
            )
        traces.sort(key=lambda t: (t["section"], t["line"]))
        return traces

    # --- Checker: punctuation pattern (em-dash overuse, body-level "!") ----

    def _check_punctuation(self) -> list[dict]:
        cfg = self.thresholds["punctuation"]
        max_em = int(cfg.get("max_em_dashes_per_doc", 5))
        ban_excl = bool(cfg.get("ban_exclamation_in_body", True))
        visible_lines = self._iter_visible_lines()
        em_total = 0
        first_em: tuple[int, str] | None = None
        excl_hits: list[tuple[int, str, str]] = []
        for line_no, section, text in visible_lines:
            em_in_line = text.count("---") + text.count("—")
            if em_in_line:
                em_total += em_in_line
                if first_em is None:
                    first_em = (line_no, section)
            if ban_excl and "!" in text:
                excl_hits.append((line_no, section, text))
        traces: list[dict] = []
        if first_em is not None and em_total > max_em:
            line_no, section = first_em
            traces.append(
                {
                    "line": line_no,
                    "text": f"{em_total} em-dashes across document (cap {max_em})",
                    "original": "",
                    "pattern": "punctuation:em_dash_overuse",
                    "category": "punctuation",
                    "section": section,
                    "suggestion_type": "punctuation_pattern",
                }
            )
        for line_no, section, text in excl_hits:
            traces.append(
                {
                    "line": line_no,
                    "text": text[:160],
                    "original": text,
                    "pattern": "punctuation:exclamation_in_body",
                    "category": "punctuation",
                    "section": section,
                    "suggestion_type": "punctuation_pattern",
                }
            )
        return traces

    def analyze_document(self) -> dict:
        """Analyze entire document."""
        analysis = {
            "total_lines": len(self.lines),
            "sections": {},
            "document_traces": [],
        }

        for section_name in self.section_ranges:
            analysis["sections"][section_name] = self.check_section(section_name)

        analysis["document_traces"].extend(self._check_term_threshold())
        analysis["document_traces"].extend(self._check_punctuation())

        return analysis

    def calculate_density_score(self, result: dict) -> float:
        if result["total_lines"] == 0:
            return 0.0
        return (result["trace_count"] / result["total_lines"]) * 100

    def generate_suggestions_json(self, analysis: dict) -> list[dict]:
        """Generate structured suggestions for Agent."""
        suggestions = []
        for section_name, result in analysis["sections"].items():
            for trace in result["traces"]:
                suggestions.append(
                    {
                        "file": str(self.file_path),
                        "line": trace["line"],
                        "section": section_name,
                        "category": trace["category"],
                        "issue": trace["text"],
                        "pattern": trace["pattern"],
                        "suggestion_key": trace["suggestion_type"],
                        "instruction": self._get_instruction(trace["suggestion_type"]),
                    }
                )
        for trace in analysis.get("document_traces", []):
            suggestions.append(
                {
                    "file": str(self.file_path),
                    "line": trace["line"],
                    "section": trace.get("section", "document"),
                    "category": trace["category"],
                    "issue": trace["text"],
                    "pattern": trace["pattern"],
                    "suggestion_key": trace["suggestion_type"],
                    "instruction": self._get_instruction(trace["suggestion_type"]),
                }
            )
        if self.tier:
            for item in suggestions:
                dim = DIMENSION_MAP.get(item["category"])
                if dim:
                    item["dimension"] = dim
                    item["teaching_note"] = TEACHING_NOTES.get(dim, "")
        return suggestions

    def _get_instruction(self, key: str) -> str:
        """Get human-readable instruction for the suggestion key."""
        instructions = {
            "quantify": "Replace with specific numbers or metrics.",
            "list_scope": "Explicitly list what was covered (X, Y, Z).",
            "compare_baseline": 'State improvement over baseline (e.g., "reduces error by X%").',
            "explain_why": "Explain specific importance or impact.",
            "specify_condition": "Specify under what conditions this holds.",
            "explain_novelty": "Explain specific technical difference.",
            "cite_sota": "Cite specific SOTA papers and compare metrics.",
            "hedge": 'Use academic hedging (e.g., "results suggest").',
            "condition": 'Add condition (e.g., "under assumption X").',
            "limit": "Acknowledge limitations or boundaries.",
            "frequency": "Use frequency adverb or specific count.",
            "cite_specific": "Cite specific papers [1-3].",
            "quantify_exp": "State number of experiments/datasets.",
            "list_methods": "List specific methods compared.",
            "quantify_items": "State exact number.",
            "quantify_percent": "State percentage.",
            "specific_time": 'Use specific time period or "since 20XX".',
            "increasingly": 'Use "increasingly" or growth data.',
            "specific_impact": "Describe specific impact or function.",
            "context_direct": "Start directly with the problem/context.",
            "cite_examples": "Provide citation examples.",
            "increase_information_density": "Replace boilerplate with concrete methods, comparators, evidence, and results.",
            "term_overuse": "Reduce repeated use of this word; vary vocabulary or quantify the claim.",
            "parallel_opening": "Vary the opening syntax across consecutive paragraphs.",
            "throat_clearing": "Cut the leading boilerplate; start with the claim.",
            "punctuation_pattern": "Avoid em-dash overuse and exclamation marks in body sections.",
            "clarify_contrast_axis": (
                "Keep the contrast only if it names a real baseline, criterion, and evidence; "
                "otherwise remove the scaffold and state the claim directly."
            ),
            "state_evidence_claim": "Remove the insight marker and state the evidence-backed claim directly.",
            "rewrite_lecture_setup": "Replace the colon-led lecture setup with a normal academic sentence or a concrete inventory noun.",
            "name_academic_referent": "Replace the vague referent with the exact research object, method, result, factor, or limitation.",
            "vary_sentence_length": (
                "Mix short and long sentences to break the even, machine-like cadence."
            ),
            "soften_causal": (
                "Causal wording: use 'associated with / linked to' unless an intervention "
                "supports causation (see over-claim-guard)."
            ),
            "qualify_novelty": "Novelty claim: add 'to our knowledge' or name the specific first.",
            "bound_universal": "Bound the claim to the cases / datasets actually studied.",
            "hedge_application": "Hedge undemonstrated applications with 'may / could'.",
            "past_in_methods_results": (
                "Methods/Results narrate the study in past tense; change present-tense "
                "reporting verbs (e.g. 'shows' -> 'showed') unless the subject is a figure/table."
            ),
        }
        return instructions.get(key, "Rewrite to be more specific and objective.")

    def _dim_tag(self, category: str) -> str:
        """Return a ` [D#]` dimension tag for reports, only when --tier is active."""
        if not self.tier:
            return ""
        dim = DIMENSION_MAP.get(category)
        return f" [{dim}]" if dim else ""

    def generate_report(self, analysis: dict) -> str:
        # ... (Same as before, abbreviated for brevity) ...
        report = []
        report.append("=" * 70)
        report.append("DE-AI WRITING TRACE ANALYSIS REPORT (Enhanced)")
        report.append("=" * 70)
        report.append(f"File: {self.file_path}")
        report.append(f"Total lines: {analysis['total_lines']}")
        if self.tier:
            report.append(f"Tier: {self.tier} (dimension labels D1-D5 enabled)")
        report.append("")

        section_scores = []
        for section_name, result in analysis["sections"].items():
            score = self.calculate_density_score(result)
            section_scores.append((section_name, score, result))

        report.append("-" * 70)
        report.append("PRIORITY RANKING")
        report.append("-" * 70)
        section_scores.sort(key=lambda x: x[1], reverse=True)
        for i, (section_name, score, result) in enumerate(section_scores, 1):
            if score > 0:
                report.append(f"{i}. {section_name}: {score:.1f}% ({result['trace_count']} traces)")

        report.append("")
        report.append("-" * 70)
        report.append("DETAILED TRACE LISTING")
        report.append("-" * 70)

        for section_name, result in analysis["sections"].items():
            if result["traces"]:
                report.append(f"\n{section_name.upper()}:")
                for trace in result["traces"][:10]:
                    report.append(
                        f"  Line {trace['line']} [{trace['category']}]"
                        f"{self._dim_tag(trace['category'])}"
                    )
                    report.append(f"    {trace['text'][:80]}")
                    report.append(
                        f"    -> Suggestion: {self._get_instruction(trace['suggestion_type'])}"
                    )

        doc_traces = analysis.get("document_traces", [])
        if doc_traces:
            report.append("")
            report.append("-" * 70)
            report.append("DOCUMENT-LEVEL TRACES")
            report.append("-" * 70)
            for trace in doc_traces:
                report.append(
                    f"  Line {trace['line']} [{trace['category']}]"
                    f"{self._dim_tag(trace['category'])} "
                    f"({trace.get('section', 'document')})"
                )
                report.append(f"    {trace['text'][:80]}")
                report.append(
                    f"    -> Suggestion: {self._get_instruction(trace['suggestion_type'])}"
                )

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze LaTeX/Typst documents for AI writing traces"
    )
    parser.add_argument("file", type=Path, help="File to analyze")
    parser.add_argument("--section", type=str, help="Specific section to check")
    parser.add_argument("--analyze", action="store_true", help="Full document analysis")
    parser.add_argument("--score", action="store_true", help="Output section scores only")
    parser.add_argument(
        "--fix-suggestions", action="store_true", help="Generate JSON suggestions for fixing"
    )
    parser.add_argument("--output", type=Path, help="Save report/json to file")
    parser.add_argument(
        "--tier",
        choices=["light", "medium", "heavy"],
        default=None,
        help="Opt-in graded mode: scales thresholds, adds D1 sentence-length check "
        "and D1-D5 dimension labels. Omit for the default (unchanged) behavior.",
    )

    args = parser.parse_args()

    if not args.file.exists():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    checker = AITraceChecker(args.file, tier=args.tier)

    if args.fix_suggestions:
        analysis = checker.analyze_document()
        suggestions = checker.generate_suggestions_json(analysis)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(suggestions, f, indent=2)
            print(f"[SUCCESS] Suggestions saved to: {args.output}")
        else:
            print(json.dumps(suggestions, indent=2))
        sys.exit(0)

    if args.analyze:
        analysis = checker.analyze_document()
        report = checker.generate_report(analysis)

        if args.output:
            args.output.write_text(report, encoding="utf-8")
            print(f"[SUCCESS] Report saved to: {args.output}")
        else:
            print(report)

        worst_score = 0
        if analysis["sections"]:
            worst_score = max(
                checker.calculate_density_score(result) for result in analysis["sections"].values()
            )

        if worst_score > 10:
            sys.exit(2)
        elif worst_score > 5:
            sys.exit(1)
        else:
            sys.exit(0)

    # ... (other args handling same as before) ...
    elif args.section:
        # Resolve aliases (methods -> method) and fail loudly on an unknown
        # section name instead of silently scanning the whole document (E4/E5).
        matched, available = resolve_section_keys(args.section, checker.section_ranges)
        if not matched:
            print(
                f"[ERROR] Section not found: {args.section}\n"
                f"Available sections: {', '.join(available) if available else '(none detected)'}",
                file=sys.stderr,
            )
            sys.exit(2)
        for section_key in matched:
            result = checker.check_section(section_key)
            score = checker.calculate_density_score(result)
            print(f"\nSection: {section_key}")
            print(f"Density: {score:.1f}%")
            for trace in result["traces"]:
                print(f"Line {trace['line']}: {trace['text']}")
                print(f"-> {checker._get_instruction(trace['suggestion_type'])}\n")

    elif args.score:
        analysis = checker.analyze_document()
        print(f"\n{'Section':<15} {'Density':<10}")
        for section_name, result in analysis["sections"].items():
            score = checker.calculate_density_score(result)
            print(f"{section_name:<15} {score:>6.1f}%")

    else:
        print("[INFO] Use --analyze for full analysis")


if __name__ == "__main__":
    main()
