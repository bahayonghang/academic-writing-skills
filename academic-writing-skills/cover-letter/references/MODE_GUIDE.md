# Mode Guide

Per-mode workflow detail for the five cover-letter modes. The single command
surface is `scripts/cover_letter.py --mode <mode>`; the only flags it accepts
are `--mode`, `--manuscript`, `--letter`, `--journal` (alias `--venue`), and
`--json`. `align-check` runs as a default capability inside `generate` and
`optimize`.

## Mode 1: `generate`

**Trigger**: user has a `main.tex` manuscript and wants a cover letter from scratch.

**Inputs**:

- `--manuscript <main.tex>` (required; `\input`/`\include` skeletons are assembled automatically)
- `--journal <venue-name>` (one of: nature, science, cell, ieee-trans, acm, springer-lncs, neurips, icml, cvpr, generic)
- `--json` for structured output (the facts blob + deterministic draft scaffold)

**Workflow steps**:

1. `cover_letter.py --mode generate` runs `extract_manuscript_facts` (title, abstract, contributions, authors, corresponding author, section anchors) and emits a deterministic draft scaffold.
2. Read `templates/<journal>.md` for tier strategy and required declarations.
3. Read `references/LETTER_STRUCTURE.md` for the five-segment scaffold.
4. Read `references/JOURNAL_TIERS.md` for the tier-specific framing rules.
5. Claude synthesizes the letter prose, filling each segment with facts and the tier's style guide.
6. **Default align-check integration**: if the synthesized letter is saved to a file, run `--mode align-check` against it; any `claim_accuracy` issue with `claim_strength: unsupported` must be resolved before presenting the letter.
7. Run `--mode presubmission` on the final letter and surface findings (declarations, length, clichés, tone).

**Output**: the cover letter text, plus `% PRESUBMISSION` and `% ALIGNCHECK` comment blocks listing any unresolved findings.

## Mode 2: `optimize`

**Trigger**: user has an existing cover letter draft and wants it improved.

**Inputs**:

- `--letter <cover_letter.md|.tex>` (the existing draft)
- `--manuscript <main.tex>` (recommended; enables the align-check pass)
- `--journal <venue-name>` (informs tier strategy)
- `--json` for structured output

**Workflow steps**:

1. `cover_letter.py --mode optimize` runs `presubmission_check` and (when `--manuscript` is given) `align_check`.
2. Read `templates/<journal>.md` for tier strategy.
3. Claude proposes section-level rewrites as LaTeX-comment diff suggestions (never source edits), each anchored to a line in the original letter.
4. Any rewrite that introduces a new claim must pass align-check (trace to manuscript evidence or be flagged for user verification).
5. Re-run `--mode align-check` on proposed rewrites saved to a file to confirm no regression.

**Output**: a LaTeX-comment review of the original letter with severity / priority / suggested rewrites.

## Mode 3: `align-check`

**Trigger**: user explicitly wants to verify the cover letter does not overclaim relative to the manuscript.

**Inputs**:

- `--letter <cover_letter.md|.tex>`
- `--manuscript <main.tex>`
- `--json` for machine-readable output

**Workflow steps**:

1. Read both files (the manuscript is assembled across `\input`/`\include`).
2. Build the manuscript anchor set (`extract_manuscript_facts`).
3. Extract claim candidates from the letter (`build_letter_claim_map`); the claim map reports `total_claim_sentences` and `truncated` when there are more candidates than the detail cap.
4. Verify each claim's quote against the manuscript (`verify_letter_against_manuscript`): exact match, paragraph-local number+metric co-occurrence, or 4-gram.
5. Classify each claim with `claim_strength` and emit findings using the simplified ISSUE_SCHEMA.

**Output**: claim-accuracy findings, each with the letter quote, the manuscript anchor (or `none`), and the recommended `allowed_wording`.

## Mode 4: `journal-fit`

**Trigger**: user wants to know whether the letter is framed correctly for the target venue.

**Inputs**:

- `--letter <cover_letter.md|.tex>`
- `--venue <venue-name>` (alias of `--journal`)
- `--json` for structured output

**Workflow steps**:

1. Read the letter.
2. Read `templates/<venue>.md` for the tier and venue expectations.
3. Read `references/JOURNAL_TIERS.md` for tier strategy.
4. `journal_fit_check` scores four sub-axes:
   - `scope_fit`: does the letter name the venue's scope dimensions?
   - `novelty_framing`: is the novelty pitch calibrated for the tier?
   - `evidence_density`: does claim density match what the venue expects?
   - `format_compliance`: word count, required declarations, banned phrases.
5. Overall verdict = worst sub-axis (LOW anywhere → LOW; else MEDIUM if any MEDIUM; HIGH only when all four HIGH).

**Heuristic limitations (disclose to the user)**: `journal-fit` is a `[Script]` heuristic, not editorial judgment. `scope_fit` matches a small fixed keyword set per venue, so a well-targeted letter that phrases scope differently can read LOW; `evidence_density` counts only first-person claim sentences ("we report/show/..."), so passive or third-person framing undercounts. Treat the verdict as a prompt to check framing, not a gate. Manuscript content is not read in this mode.

**Output**: per-axis verdict (HIGH / MEDIUM / LOW) with quotes as evidence; overall verdict; per-axis suggestions.

## Mode 5: `presubmission`

**Trigger**: user wants declaration, length, cliché, and tone checks only.

**Inputs**:

- `--letter <cover_letter.md|.tex>`
- `--journal <venue-name>` (enables the template-driven declaration and length checks)
- `--json` for structured output

**Workflow steps**:

1. Read the letter (`errors="replace"`, so non-UTF-8 letters do not crash).
2. Load the active template's frontmatter (no PyYAML dependency).
3. Scan: em dash (`G1`), AI-tone frequency (`AI*`), opener clichés (`L2*`), banned phrases (`J1*`), generic-fit phrasings (`J4*`), required/optional declarations (`D-*`), length (`L1`), paragraph shape (`G2`/`G3`).
4. Declarations without a detector emit an informational `D-<kind>-unknown` (required) or are skipped (optional) rather than a false "absent".

**Output**: a list of presentation / declaration / tone findings.

## Mode Integration Matrix

| Mode            | Calls `extract_manuscript_facts` | Calls `align_check`        | Calls `presubmission_check` | Calls `journal_fit_check` |
| --------------- | -------------------------------- | -------------------------- | --------------------------- | ------------------------- |
| `generate`      | Always                           | Always (after synthesis)   | Always (final pass)         | Optional                  |
| `optimize`      | If `--manuscript` provided       | If `--manuscript` provided | Always                      | Optional                  |
| `align-check`   | Always                           | Always                     | No                          | No                        |
| `journal-fit`   | No                               | No                         | No                          | Always                    |
| `presubmission` | No                               | No                         | Always                      | No                        |

## Routing Rules

- Default to `generate` only when no existing letter is provided.
- Default to `optimize` when both letter and manuscript are provided and the user does not name a mode.
- `align-check` and `journal-fit` are explicit-only — invoke them by name.
- If the user asks to "review my cover letter" without naming a mode, prefer `optimize` (which already runs align-check + presubmission).
