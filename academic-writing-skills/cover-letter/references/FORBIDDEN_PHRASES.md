# Forbidden Phrases

Phrases that should not appear in an academic submission cover letter. Used by `presubmission_check.py` and `optimize` mode.

## Tier 1: Low-effort openers (always flag)

These signal a low-effort letter to top-journal editors:

- "We are pleased to submit"
- "We are excited to share"
- "We are delighted to submit"
- "We are honored to submit"
- "It is our great pleasure to submit"
- "Enclosed please find"
- "Please find enclosed"
- "Please find attached"
- "We hereby submit"

## Tier 2: Marketing adjectives (flag at 3+ occurrences)

These inflate without adding evidence. Inherits from paper-audit `BANNED_TONE_PATTERNS`:

- innovative
- pioneering
- revolutionary
- transformative
- breakthrough
- unprecedented
- remarkable
- superior
- state-of-the-art
- "highlights the potential of"
- "paves the way"
- "profound challenges"
- "at its essence"

## Tier 3: Cover-letter-specific banned phrases (flag at 1+ occurrence)

These are template-style fillers that editors at top journals discount:

- "novel and innovative"
- "groundbreaking"
- "first-of-its-kind"
- "game-changing"
- "paradigm shift"
- "cutting-edge"
- "of great interest"
- "will be of broad interest"
- "the field is in need of"

## Tier 4: Generic-fit phrasings (flag with suggested replacement)

These indicate the author has not read the journal carefully:

- "your journal" / "your prestigious journal" — name the journal explicitly
- "fits well with the scope" — name the specific scope dimension
- "broad readership" — name the specific reader profile
- "important contribution to the field" — name the contribution category

## What is acceptable

- Confident factual statements: "Our method reduces inference latency by 47% on the ImageNet validation set."
- Bounded comparisons: "This extends the framework of Chen et al. (2024) by introducing X."
- Specific journal connections: "This work directly addresses the open question raised in [recent paper from the target journal]."

## Why these are forbidden

The pattern across these tiers: they substitute marketing for evidence. An editor reading 50 letters a week can spot template-language instantly and downgrades the letter's signal value. Cover letters that pass `presubmission_check.py` with zero Tier 1-3 hits read as written-with-attention.
