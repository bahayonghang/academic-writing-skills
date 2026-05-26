# Cover-Letter Issue Schema

Simplified, field-compatible variant of `paper-audit/references/ISSUE_SCHEMA.md`. A cover-letter finding can be ingested by paper-audit's deep-review consolidation later by adding the dropped fields with default values.

## Canonical record

```json
{
  "title": "short issue title",
  "quote": "exact quote from the cover letter",
  "explanation": "why this matters and what remains problematic",
  "comment_type": "claim_accuracy|journal_fit|declaration_missing|presentation|tone",
  "severity": "major|moderate|minor",
  "source_kind": "script|llm",
  "confidence": "high|medium|low|unverified",
  "source_section": "header|opening|contributions|fit|declarations|closing",
  "manuscript_section_anchor": "abstract|introduction|results|conclusion|none",
  "evidence_anchor": [
    {
      "type": "citation|figure_or_table|metric|section|analysis_artifact|missing",
      "text": "visible anchor in manuscript"
    }
  ],
  "claim_strength": "unsupported|observed|supported|strong",
  "missing_evidence": ["specific support that is absent or unverified"],
  "allowed_wording": "bounded wording that stays within the evidence",
  "forbidden_wording": [
    "unbounded wording that would require stronger evidence"
  ],
  "quote_verified": true
}
```

## Required fields

- `title`
- `quote`
- `explanation`
- `comment_type`
- `severity`
- `source_kind`

## Optional fields

- `confidence` — high / medium / low / unverified; demote to `unverified` when the cover-letter quote cannot be located.
- `source_section` — which logical section of the letter the issue lives in.
- `manuscript_section_anchor` — which section of the manuscript the claim should be supported by; `none` when the issue is about the letter itself (e.g. tone) and not a claim-vs-manuscript alignment.
- `evidence_anchor` / `claim_strength` / `missing_evidence` / `allowed_wording` / `forbidden_wording` — added when the issue is about claim accuracy. Follows the `CLAIM_EVIDENCE_CONTRACT.md` contract.
- `quote_verified` — populated by `verify_letter_against_manuscript.py`.

## Dropped vs. paper-audit canonical

These fields are intentionally absent in v1; add them with default values when ingesting into paper-audit:

| Dropped field      | Default for ingestion                                    |
| ------------------ | -------------------------------------------------------- |
| `review_lane`      | `"presubmission_readiness"`                              |
| `root_cause_key`   | derive from `comment_type + source_section + quote hash` |
| `gate_blocker`     | `false` (cover-letter does not have a gate mode in v1)   |
| `related_sections` | use `manuscript_section_anchor` instead                  |

## Comment-type semantics

- `claim_accuracy` — letter claim is unsupported or overclaims relative to manuscript evidence.
- `journal_fit` — pitch is mismatched with the target venue's scope or tier.
- `declaration_missing` — required declaration absent (see template's `required_declarations`).
- `presentation` — length, paragraph shape, citation tilde, or other surface form.
- `tone` — AI-tone words, forbidden phrases, marketing language.

## Severity guidance

- `major` — declaration_missing for a template's `required` items; overt overclaim where claim_strength is `unsupported`; length exceeding the template's hard ceiling by ≥20%; journal_fit verdict of LOW.
- `moderate` — overclaim that is `observed` but pushed beyond observed scope; missing optional but recommended declaration when manuscript needs it; journal_fit verdict of MEDIUM on the most-loaded sub-axis.
- `minor` — paragraph length warnings; AI-tone term frequency; weak topic starters; non-required journal-specific phrasings.
