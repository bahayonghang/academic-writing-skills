# Mode Guide

Per-mode workflow detail for the five cover-letter modes. The single command
surface is `scripts/cover_letter.py --mode <mode>`; the only flags it accepts
are `--mode`, `--manuscript`, `--letter`, `--journal` (alias `--venue`),
`--json`, and `--dedup-length` (journal-fit mode only; see Mode 2 and Mode 4).
`align-check` runs as a default capability inside `generate` and `optimize`.

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

Corresponding-author extraction trusts only an explicit `\corresponding{...}` or
`\correspondingauthor{...}` command. IEEE `\thanks{...}` and acmart
`\authornote{...}` prose intentionally fall back to the first parsed author: guessing from
free text can mistake an email local part for a person's name. Confirm the corresponding
author manually when those template-specific forms are used.

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
6. If a `journal-fit` pass is also run in this session (optional; see the Mode Integration Matrix), pass `--dedup-length` so the two checks do not both report the same template `word_limit` — `optimize`'s own `presubmission` pass already reports length via its finer-grained two-tier `L1` check.

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
6. Cross-check AI-disclosure consistency between the letter and the manuscript: if one document discloses generative-AI use (or non-use) and the other is silent, or the two contradict on polarity, emit a `moderate` `disclosure_consistency` finding. Both documents are read with `%`-comments stripped so a commented-out declaration does not count.

**Output**: claim-accuracy findings, each with the letter quote, the manuscript anchor (or `none`), and the recommended `allowed_wording`; plus at most one `disclosure_consistency` finding when the two documents disagree on AI disclosure.

## Mode 4: `journal-fit`

**Trigger**: user wants to know whether the letter is framed correctly for the target venue.

**Inputs**:

- `--letter <cover_letter.md|.tex>`
- `--venue <venue-name>` (alias of `--journal`)
- `--json` for structured output
- `--dedup-length` (optional; default off): skip this mode's own word-count sub-check when a `presubmission` pass in the same session already reports length via its finer-grained `L1` check (see Mode 2 step 6 and the Mode Integration Matrix).

**Workflow steps**:

1. Read the letter.
2. Read `templates/<venue>.md` for the tier and venue expectations.
3. Read `references/JOURNAL_TIERS.md` for tier strategy.
4. `journal_fit_check` scores four sub-axes:
   - `scope_fit`: does the letter name the venue's scope dimensions? (top-journal tier: one matched keyword is enough for HIGH, reflecting the tight ~350-word budget; other tiers need two.)
   - `novelty_framing`: is the novelty pitch calibrated for the tier?
   - `evidence_density`: does claim density match what the venue expects?
   - `format_compliance`: word count (skipped when `--dedup-length` is set), required declarations, banned phrases.
5. Overall verdict = worst sub-axis (LOW anywhere → LOW; else MEDIUM if any MEDIUM; HIGH only when all four HIGH).
6. A response with no `tier` in the active template's frontmatter is reported in `warnings` (defaults to mid-journal scoring).

**Heuristic limitations (disclose to the user)**: `journal-fit` is a `[Script]` heuristic, not editorial judgment. `scope_fit` matches a small fixed keyword set per venue, so a well-targeted letter that phrases scope differently can read LOW; `evidence_density` counts `LETTER_CLAIM_PATTERNS` claim-bearing sentences (the same extractor `align-check` uses — first-person "we report/show/...", "our work," direction+number, deployment, and similar claim styles), so a letter that avoids all of those styles can still undercount. Treat the verdict as a prompt to check framing, not a gate. Manuscript content is not read in this mode.

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
3. Scan: em dash (`G1`), AI-tone frequency (`AI*`, 2 = minor / 3+ = major), diverse AI-tone vocabulary (`AI-DIV`), parallel paragraph openings (`S1`), uniform sentence length (`S2`), opener clichés (`L2*`), banned phrases (`J1*`), generic-fit phrasings (`J4*`), required/optional declarations (`D-*`), length (`L1`), paragraph shape (`G2`/`G3`).
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

`generate` and `optimize`'s "Optional" `journal_fit_check` call always runs alongside a mandatory `presubmission_check` pass in the same session — pass `--dedup-length` to that `journal-fit` call so length is reported once (via `presubmission`'s `L1`), not twice.

## Routing Rules

- Default to `generate` only when no existing letter is provided.
- Default to `optimize` when both letter and manuscript are provided and the user does not name a mode.
- `align-check` and `journal-fit` are explicit-only — invoke them by name.
- If the user asks to "review my cover letter" without naming a mode, prefer `optimize` (which already runs align-check + presubmission).
