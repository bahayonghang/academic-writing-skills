# Mode Guide

Per-mode workflow detail for the four cover-letter modes. `align-check` runs as a default capability across `generate` and `optimize`; this guide documents how that integration works.

## Mode 1: `generate`

**Trigger**: user has a `main.tex` manuscript and wants a cover letter from scratch.

**Required inputs**:

- `--manuscript <main.tex>` (positional or flag)
- `--journal <venue-name>` (one of the templates: nature, science, cell, ieee-trans, acm, springer-lncs, neurips, icml, cvpr, generic)
- Optional: `--out-format md|jourcl` (default `md`)
- Optional: `--output <path>` (default: stdout)

**Workflow steps**:

1. Run `extract_manuscript_facts.py` to produce `facts.json` (title, abstract, contributions, authors, corresponding author, section anchors).
2. Read `templates/<journal>.md` for tier strategy and required declarations.
3. Read `references/LETTER_STRUCTURE.md` for the five-segment scaffold.
4. Read `references/JOURNAL_TIERS.md` for the tier-specific framing rules.
5. Claude synthesizes the letter prose, filling each segment with facts from `facts.json` and following the tier's style guide.
6. **Default align-check integration**: immediately run `align_check.py` against the generated letter + manuscript. Any `claim_accuracy` issue with `claim_strength: unsupported` must be addressed before presenting the letter to the user.
7. Run `presubmission_check.py` on the final letter. Any Major finding is surfaced; Minor findings are surfaced if `--strict` is set.
8. Render the letter (Markdown by default; jourcl-compatible LaTeX if `--out-format jourcl`).

**Output**: cover letter text, plus a brief `% PRESUBMISSION` and `% ALIGNCHECK` comment block listing any unresolved findings.

## Mode 2: `optimize`

**Trigger**: user has an existing cover letter draft and wants it improved.

**Required inputs**:

- `--letter <cover_letter.md|.tex>` (the existing draft)
- `--manuscript <main.tex>` (for align-check; required for default integration)
- `--journal <venue-name>` (informs tier strategy)
- Optional: `--section <opening|contributions|fit|declarations|closing>` to scope optimization

**Workflow steps**:

1. Read the existing letter draft.
2. Run `presubmission_check.py` for mechanical findings.
3. Run `align_check.py` against the manuscript for claim-evidence findings.
4. Read `templates/<journal>.md` for tier strategy.
5. Claude proposes section-level rewrites as LaTeX-comment diff suggestions (not source edits). Each suggestion is anchored to a line in the original letter.
6. **Constraint**: any rewrite that introduces a new claim must pass align-check (i.e., the new claim must trace to manuscript evidence or be flagged as needing user verification).
7. Re-run `align_check.py` against the proposed rewrites to confirm no regression.

**Output**: LaTeX-comment review of the original letter with severity / priority / suggested rewrites.

## Mode 3: `align-check`

**Trigger**: user explicitly wants to verify the cover letter does not overclaim relative to the manuscript.

**Required inputs**:

- `--letter <cover_letter.md|.tex>`
- `--manuscript <main.tex>`
- Optional: `--json` for machine-readable output

**Workflow steps**:

1. Read both files.
2. Run `extract_manuscript_facts.py` to build the manuscript anchor set.
3. Run `build_letter_claim_map.py` to extract claim candidates from the letter.
4. Run `verify_letter_against_manuscript.py` to check each claim's quote against the manuscript.
5. Classify each claim with `claim_strength` and emit a list of findings using the simplified ISSUE_SCHEMA.

**Output**: list of claim-accuracy findings; each finding includes the letter quote, the manuscript anchor (or `none`), and the recommended `allowed_wording`.

## Mode 4: `journal-fit`

**Trigger**: user wants to know whether the letter is framed correctly for the target venue.

**Required inputs**:

- `--letter <cover_letter.md|.tex>`
- `--venue <venue-name>`
- Optional: `--manuscript <main.tex>` for richer scope-fit analysis

**Workflow steps**:

1. Read the letter.
2. Read `templates/<venue>.md` for the tier and venue-specific expectations.
3. Read `references/JOURNAL_TIERS.md` for tier strategy.
4. Run `journal_fit_check.py` which scores 4 sub-axes:
   - `scope_fit`: does the manuscript topic (read from letter or manuscript) match the venue's published scope?
   - `novelty_framing`: is the novelty pitch calibrated for the venue's tier?
   - `evidence_density`: does claim density match what this venue expects?
   - `format_compliance`: word count, required declarations present, banned phrases absent.
5. Overall verdict = worst sub-axis. LOW anywhere → LOW overall; else MEDIUM if any MEDIUM; HIGH only when all four HIGH.

**Output**: per-axis verdict (HIGH / MEDIUM / LOW) with specific quotes from the letter as evidence; overall verdict; per-axis suggestions.

## Mode Integration Matrix

| Mode          | Calls `extract_manuscript_facts` | Calls `align_check`              | Calls `presubmission_check`       | Calls `journal_fit_check` |
| ------------- | -------------------------------- | -------------------------------- | --------------------------------- | ------------------------- |
| `generate`    | Always                           | Always (after synthesis)         | Always (final pass)               | Optional                  |
| `optimize`    | If `--manuscript` provided       | Always (before + after rewrites) | Always                            | Optional                  |
| `align-check` | Always                           | Always                           | No                                | No                        |
| `journal-fit` | If `--manuscript` provided       | No                               | Implicit (format_compliance axis) | Always                    |

## Routing Rules

- Default to `generate` only when no existing letter is provided.
- Default to `optimize` when both letter and manuscript are provided and the user does not name a mode.
- `align-check` and `journal-fit` are explicit-only — invoke them by name.
- If the user asks for "review my cover letter" without naming a mode, prefer `optimize` (which already runs align-check + presubmission).
