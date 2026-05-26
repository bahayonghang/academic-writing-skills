# Cover-Letter Pre-Submission Rules

Deterministic rules for `presubmission_check.py`. Adapted from `paper-audit/references/PRE_SUBMISSION_RULES.md` with cover-letter-specific additions and LaTeX-source-only rules removed.

## Banned AI-tone patterns (G4-AI\*)

Triggers at 3+ occurrences in the letter. Inherits from paper-audit canonical list.

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
    r"^\s*we are (?:pleased|excited|delighted|honored) to submit\b",
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

Triggers at 1+ occurrence. Severity: `minor` (`major` when 3+).

## Mechanical rules

| ID  | Severity      | Check                                                                                                              |
| --- | ------------- | ------------------------------------------------------------------------------------------------------------------ |
| G1  | `major`         | Em dash in reader-visible prose.                                                                                   |
| G2  | `minor`         | Paragraph longer than 120 words or 6 sentences (cover letters are shorter than papers — paragraph cap is tighter). |
| G3  | `minor`         | Paragraph starts with weak transition (however, moreover, in addition, furthermore, also).                         |
| G4  | `major`         | Any banned AI-tone term group appears ≥3 times across the letter.                                                  |
| L1  | `major` / `minor` | Letter exceeds template's `word_limit` by ≥20% (`major`) or up to 20% (`minor`).                                       |
| L2  | `minor`         | First content line matches a known opener cliché.                                                                  |
| J1  | `minor` / `major` | Cover-letter-specific banned phrase appears (`minor`) or appears 3+ times (`major`).                                   |

## Required declaration rules (D1-D6)

Driven by the active template's `required_declarations` frontmatter list. The check is:

1. Parse the template's `required_declarations` and `optional_declarations` arrays.
2. For each `required_declarations` item, scan the letter body for one of the canonical phrasings (see below).
3. If absent, emit a `major` finding with the declaration name.
4. For `optional_declarations`, emit a `minor` advisory if absent.

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
```

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
