# Cover-Letter Pre-Submission Rules

Deterministic rules for `presubmission_check.py`. Adapted from `paper-audit/references/PRE_SUBMISSION_RULES.md` with cover-letter-specific additions and LaTeX-source-only rules removed.

## Banned AI-tone patterns (G4-AI\*)

Per-term ladder: the **same** term appearing 2 times is `minor`, 3+ times is
`major`. (Before, a term was silent below 3 occurrences, so a vocabulary-diverse
draft with each promo word used once slipped through entirely — see `AI-DIV`
below.) Inherits from paper-audit canonical list.

```python
BANNED_TONE_PATTERNS = (
    ("AI1", r"\binnovative\b"),
    ("AI2", r"\bpioneering\b"),
    ("AI3", r"\brevolutionary\b"),
    ("AI4", r"\btransformative\b"),
    ("AI5", r"\bbreakthrough\b"),
    ("AI6", r"\bunprecedented\b"),
    ("AI7", r"\bremarkable\b"),
    ("AI8", r"\bsuperior\b"),
    ("AI9", r"\bsurpass(?:es|ed|ing)?\b"),
    ("AI10", r"\bstate[- ]of[- ]the[- ]art\b"),
    ("AI11", r"\bhighlights? the potential of\b"),
    ("AI12", r"\bpaves? the way\b"),
    ("AI13", r"\bprofound challenges?\b"),
    ("AI14", r"\bat its essence\b"),
)
```

## Cover-letter-specific opener clichés (L2)

Triggers on first non-empty line of the letter body (post-salutation):

```python
LETTER_OPENER_CLICHES = (
    r"^\s*we are (?:pleased|excited|delighted|honored) to (?:submit|share)\b",
    r"^\s*we hereby submit\b",
    r"^\s*please find (?:enclosed|attached)\b",
    r"^\s*it is our (?:great )?pleasure to submit\b",
    r"^\s*enclosed please find\b",
)
```

Severity: `minor`. These openings flag the letter as low-effort to editors at top journals.

## Cover-letter-specific banned phrases (J1)

Marketing or AI-template language with zero editor signal:

- "novel and innovative"
- "groundbreaking"
- "first-of-its-kind"
- "game-changing"
- "paradigm shift"
- "cutting-edge"
- "of great interest"
- "will be of broad interest"
- "the field is in need of"

Triggers at 1+ occurrence. Severity: `minor` (`major` when 3+).

## Generic-fit phrasings (J4)

Tier 4 of `FORBIDDEN_PHRASES.md`: phrasings that signal the author did not read
the venue. Triggers at 1+ occurrence, `minor` / `P3`, each with a "name the
specific X" replacement hint:

- "your journal" / "your prestigious journal" → name the journal
- "fits (well) with/into the scope" → name the scope dimension
- "broad readership" → name the reader profile
- "important contribution to the field" → name the contribution category

## Mechanical rules

| ID  | Severity          | Check                                                                                                              |
| --- | ----------------- | ------------------------------------------------------------------------------------------------------------------ |
| G1  | `minor`           | Em dash in reader-visible prose (an AI-tone surface signal, aligned with the ISSUE_SCHEMA minor tier).             |
| G2  | `minor`           | Paragraph longer than 120 words or 6 sentences (cover letters are shorter than papers — paragraph cap is tighter). |
| G3  | `minor`           | Paragraph starts with weak transition (however, moreover, in addition, furthermore, also).                         |
| G4  | `minor` / `major` | Same banned AI-tone term appears 2 times (`minor`) or 3+ times (`major`).                                          |
| L1  | `major` / `minor` | Letter exceeds template's `word_limit` by ≥20% (`major`) or up to 20% (`minor`).                                   |
| L2  | `minor`           | First content line matches a known opener cliché.                                                                  |
| J1  | `minor` / `major` | Cover-letter-specific banned phrase appears (`minor`) or appears 3+ times (`major`).                               |
| J4  | `minor`           | Generic-fit phrasing (Tier 4) appears; emits a "name the specific X" replacement hint.                             |
| AI-DIV | `minor` / `major` | `minor` when 3 **distinct** banned AI-tone terms appear (each perhaps once), `major` at 4+. Catches diverse AI slop the per-term G4 ladder misses. |
| S1  | `minor`           | 3 consecutive body paragraphs open with the same first two word tokens (parallel/templated cadence).               |
| S2  | `minor`           | Sentence-length coefficient of variation < 0.25 over ≥8 sentences (suspiciously uniform cadence / low burstiness). |

## Structural AI-trace checks (AI-DIV, S1, S2)

These three checks port the structural AI-trace idea used by `latex-paper-en` /
`typst-paper` (deai) into the cover-letter genre. They are all `minor`/`P2`
except AI-DIV, which escalates to `major` at 4+ distinct terms, and they report
only — no rewriting.

Thresholds are fixed module constants in `presubmission_check.py`
(`AI_TONE_DIVERSITY_*`, `PARALLEL_OPENING_*`, `SENTENCE_UNIFORMITY_*`), not a
per-tier YAML: a cover letter is a single short genre, and the scans must run
even without a `--journal` (so no `word_limit` baseline exists). Length-adaptive
thresholds would add a "what baseline when no template?" dimension for no real
gain, so we chose deterministic constants that the zero-false-positive fixture
(`evals/fixtures/human_letter.md`) guards.

Parameters (letter-domain tuning vs. the paper-side defaults):

- **AI-DIV** — counts how many distinct `BANNED_TONE_PATTERNS` fire at least
  once. Distinct from G4 (repetition vs. diversity); both may fire on one letter.
- **S1 (parallel openings)** — window of 3 consecutive paragraphs, opening key =
  first 2 word tokens (same pins as the paper-side `_check_burstiness`). The
  `Dear …` salutation paragraph is skipped; declaration paragraphs ("We confirm
  …", "We declare …") differ under a 2-token key, so they do not false-positive.
- **S2 (sentence-length uniformity)** — whole-letter (cover letters have no
  sections), gated at ≥8 sentences with CV < 0.25. The paper-side default is
  min 5 / CV < 0.30 and tier-gated; the letter sample is short and CV-noisy, so
  the gate is raised and the threshold tightened to suppress false positives.

Not ported from the paper-side deai structural shell:

- **throat-clearing paragraph leads** — the letter genre already has equivalents
  (`L2` opener clichés + `G3` weak-transition paragraph starts); adding it would
  double-report.
- **low-information-density** — a cover letter's declaration paragraph is
  legitimately templated and evidence-marker-free, so this check would
  false-positive on well-formed letters at ≤400 words.

## Required declaration rules (D-\<kind\>)

Driven by the active template's `required_declarations` frontmatter list. The check is:

1. Parse the template's `required_declarations` and `optional_declarations` arrays.
2. For each `required_declarations` item with a known detector, scan the letter body for one of the canonical phrasings (see below).
3. If absent, emit a `major` finding (`D-<kind>`) with the declaration name.
4. For `optional_declarations` with a known detector, emit a `minor` advisory (`D-<kind>-opt`) if absent.
5. A required kind with **no** detector emits an informational `D-<kind>-unknown` (`minor`/`P3`, "verify manually") instead of a false "absent" major; an optional kind with no detector is skipped silently.

Canonical phrasings (regex, case-insensitive):

```text
originality:
  - not (?:been )?published elsewhere
  - not under (?:concurrent )?(?:consideration|review|submission)
  - original (?:research|work|manuscript)

dual_submission:
  - not (?:currently )?(?:under (?:concurrent )?(?:consideration|submission|review)|submitted)(?:\s+elsewhere)?
  - single submission policy
  - (?:dual|multiple) submission
  - not (?:been )?submitted (?:to|elsewhere)
  - concurrent consideration

competing_interests:
  - (?:no |declare(?:s)? (?:no |the following )?)?competing interests?
  - conflicts? of interest
  - declare(?:s)? no (?:competing|conflict)

data_availability:
  - data (?:will be |are |is )?(?:made )?available
  - code (?:will be |is )?(?:made )?available
  - materials (?:are|will be) available
  - data and code
  - data availability statement

ethics_irb:
  - institutional review board
  - \bIRB\b
  - \bIACUC\b
  - ethics? (?:committee|approval|board)
  - clinical trial (?:registration|number|identifier)
  - informed consent

authorship:
  - all authors (?:have )?approved
  - all authors (?:have )?read and approved
  - authorship agreement

ai_disclosure:
  - generative ai
  - \bgen[- ]?ai\b
  - (?:used|use of|using|employed|with|disclos\w+|assisted by) (?:a |an |the )?(?:large language model|llms?|generative ai|ai (?:tool|assistant|writing))
  - no (?:generative )?ai (?:tool|assistance|was|were|used)
  - ai[- ](?:assisted|generated) (?:writing|text|content|editing)
  - \b(?:chatgpt|gpt-\d|copilot|gemini)\b

prior_presentation:
  - (?:previously |earlier )?(?:presented|published|appeared) (?:as |in )?(?:a |an )?(?:poster|abstract|preprint|workshop|preliminary|short version)
  - \ba (?:preliminary|prior|earlier|conference) version\b
  - \bpresented at\b
  - \bextends? (?:our|a) (?:prior|earlier|previous) (?:conference |workshop )?(?:paper|version)
```

`ai_disclosure` is required by the Nature / Science / Cell templates (ICMJE Jan
2026 Section V; Science requires it in the cover letter explicitly). IEEE / ACM
place AI disclosure in the manuscript, so their templates do not list it.
Declaration kinds without a detector (`excluded_reviewers`,
`artifact_evaluation`, `reproducibility_statement`) are handled by rule 5 above.

## Length check (L1)

Reads `word_limit` from the template. Counts visible words (excludes salutation, address block, signature). Severity ladder:

- 0-100% of limit: OK.
- 100-120% of limit: `minor`.
- 120%+ of limit: `major`.

## Paragraph shape (G2, G3)

Stricter than paper-audit because cover letters are shorter:

- Long paragraph: >120 words OR >6 sentences (vs. 180/8 for papers).
- Weak topic starter: ≥60 words AND ≥2 sentences AND opens with a weak transition.

## Caption / equation / label / citation rules — NOT applicable

Cover letters do not contain LaTeX captions, numbered equations, or label/ref pairs. The corresponding rules from paper-audit are intentionally omitted.
