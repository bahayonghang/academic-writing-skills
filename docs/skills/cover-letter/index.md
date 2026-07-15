# `cover-letter`

Submission cover-letter assistant for existing LaTeX manuscripts. It generates, optimizes, and checks editor-facing letters while keeping every strong letter claim tied to manuscript evidence.

## Use It For

- Generate a cover letter draft from `main.tex`.
- Optimize an existing `cover_letter.md` or `cover_letter.tex` without overwriting it.
- Align-check novelty, contribution, numeric, and scope claims against the manuscript.
- Check whether the letter is framed for a bundled journal or conference template.
- Run final declaration, length, cliché, AI-tone, and paragraph-shape checks.

## Do Not Use It For

- Editing the manuscript source; use `latex-paper-en` or `latex-thesis-zh`.
- Full reviewer-style manuscript critique; use `paper-audit`.
- Searching bibliography files; use `bib-search-citation`.
- Typst manuscripts; this version supports LaTeX manuscripts only.
- Rebuttal or response-to-reviewer letters.

## Mode Router

| Mode | Use when | Primary command |
| --- | --- | --- |
| `generate` | You have a manuscript but no letter draft | `uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode generate --manuscript main.tex --journal nature --json` |
| `optimize` | You have a draft and want safer framing | `uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode optimize --letter cover_letter.md --manuscript main.tex --journal nature --json` |
| `align-check` | You need to verify claims against the paper | `uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode align-check --letter cover_letter.md --manuscript main.tex --json` |
| `journal-fit` | You need venue fit scoring | `uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode journal-fit --letter cover_letter.md --journal nature --json` |
| `presubmission` | You need final mechanical checks | `uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode presubmission --letter cover_letter.md --journal nature --json` |

Supported bundled venues: `nature`, `science`, `cell`, `ieee-trans`, `acm`, `springer-lncs`, `neurips`, `icml`, `cvpr`, and `generic`.

## Minimum Inputs

- `--manuscript main.tex` for `generate` and `align-check`.
- `--letter cover_letter.md` or `--letter cover_letter.tex` for `optimize`, `align-check`, `journal-fit`, and `presubmission`.
- `--journal <venue>` for journal-fit and venue-specific pre-submission rules.
- `--json` when you want a machine-readable issue bundle.

## Script Entry Points

| Script | Purpose |
| --- | --- |
| `cover_letter.py` | Unified public CLI for all five modes |
| `extract_manuscript_facts.py` | Deterministic facts extraction from the manuscript |
| `build_letter_claim_map.py` | Cover-letter claim inventory |
| `align_check.py` / `verify_letter_against_manuscript.py` | Claim-evidence verification |
| `journal_fit_check.py` | Venue-fit scoring |
| `presubmission_check.py` | Declaration, length, cliché, and tone checks |

## Output Artifacts

- `generate` returns manuscript facts plus a deterministic draft scaffold with placeholders for unknown editor or declaration fields.
- `optimize` returns line-anchored suggestions and claim-evidence warnings; it does not overwrite the draft.
- `align-check` returns unsupported, over-scoped, or missing-evidence claim findings.
- `journal-fit` returns HIGH / MEDIUM / LOW axis verdicts and mapped findings.
- `presubmission` returns mechanical findings for required declarations, length, cliché, tone, and paragraph shape.

Findings use `severity`, `priority`, `source_kind`, and `comment_type`; script-backed findings are intended to be rerunnable.

## Public Resources

### References

- [AI disclosure policy](./resources/references/ai-disclosure-policy.md)
- [Claim-evidence contract](./resources/references/CLAIM_EVIDENCE_CONTRACT.md)
- [Forbidden phrases](./resources/references/FORBIDDEN_PHRASES.md)
- [Issue schema](./resources/references/ISSUE_SCHEMA.md)
- [Journal tiers](./resources/references/JOURNAL_TIERS.md)
- [Letter structure](./resources/references/LETTER_STRUCTURE.md)
- [Mode guide](./resources/references/MODE_GUIDE.md)
- [Pre-submission rules](./resources/references/PRESUBMISSION_RULES.md)

### Templates

- [ACM](./resources/templates/acm.md)
- [Cell](./resources/templates/cell.md)
- [CVPR](./resources/templates/cvpr.md)
- [Generic](./resources/templates/generic.md)
- [ICML](./resources/templates/icml.md)
- [IEEE Transactions](./resources/templates/ieee-trans.md)
- [Nature](./resources/templates/nature.md)
- [NeurIPS](./resources/templates/neurips.md)
- [Science](./resources/templates/science.md)
- [Springer LNCS](./resources/templates/springer-lncs.md)

### Examples

- [Align check only](./resources/examples/align-check-only.md)
- [Generate a Nature letter](./resources/examples/generate-nature.md)
- [CVPR vs. TPAMI journal fit](./resources/examples/journal-fit-cvpr-vs-tpami.md)
- [Optimize and align](./resources/examples/optimize-and-align.md)

### Agent Contracts

- [Claims-evidence reviewer](./resources/agents/claims_evidence_reviewer_agent.md)
- [Committee editor](./resources/agents/committee_editor_agent.md)

## Common Requests

```text
Generate a Nature cover letter from main.tex and include placeholders where metadata is missing.
```

```text
Optimize cover_letter.md for an IEEE Transactions submission, but do not edit the file directly.
```

```text
Check whether every strong claim in this cover letter is supported by main.tex.
```

```text
Score this letter for NeurIPS journal-fit style framing and tell me the weakest axis.
```

```text
Run final pre-submission checks on cover_letter.md before I paste it into the submission system.
```
