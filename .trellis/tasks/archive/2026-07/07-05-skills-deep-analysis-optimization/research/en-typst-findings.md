# Research: latex-paper-en + typst-paper deep audit (deai / tense / over-claim focus)

- **Query**: Deep-audit the newly added (post-2026-06-20, not-yet-independently-reviewed) deai structural-shell check, tense signal-word detection, and over-claim guard in `latex-paper-en` and `typst-paper`; find real bugs, en/typst drift, contract/doc drift, test gaps, red-line risk.
- **Scope**: internal (scripts + references + SKILL.md + tests)
- **Date**: 2026-07-05
- **Commits in focus**: `7311420` (deai structural-shell check), `3a8e3c2` (tense signal detection), `8cf4622` (over-claim guard, paper-audit side)

## Method

Read both `scripts/deai_check.py` (en 1097 lines, typst 1217 lines) and both `scripts/parsers.py` in full; read both YAML threshold files; verified referenced files exist; checked SKILL.md contracts, module docs, evals, and the two shared test files. Reproduced the two confirmed divergences with live runs of the actual skill scripts (repro scratch left at `research/_scratch/` — `rm` was permission-denied, safe to delete).

---

## Findings

### Confirmed bugs / divergences

#### XA-1 (medium) — Typst `low_information_density` misses citation evidence; the EN "E17" fix was never ported

- **Files**: `academic-writing-skills/typst-paper/scripts/deai_check.py:574-622` (`_check_low_information_density`) vs `academic-writing-skills/latex-paper-en/scripts/deai_check.py:456-514`.
- **Problem**: The EN version was explicitly fixed (comment at `latex-paper-en/scripts/deai_check.py:477-480`, "E17") to test evidence markers on the **raw source** because `extract_visible_text()` strips `\cite{}`/bracket refs — otherwise a citation-dense paragraph reads as evidence-free. The Typst copy still tests `self.EVIDENCE_MARKERS.search(text)` where `text` is the **visible** text (`typst-paper/scripts/deai_check.py:602`). Typst `extract_visible_text` blanks `@cite`/`#cite(...)` via `PRESERVE_PATTERNS` (`typst-paper/scripts/parsers.py:394-404`, blanked then excluded), so only bare inline numbers survive as evidence. A related-work paragraph carrying many `@refs` but no inline number is wrongly flagged as low information density.
- **Evidence (live repro)**: A 3-line `= Related Work` block with 6 `@cite` keys and 2 template phrases per line —
  - Typst result categories: `[empty_phrase, template_expr×4, low_information_density]` ← false positive
  - Same paragraph in LaTeX (`\cite{...}`): `[empty_phrase, template_expr×4]` ← correctly NOT flagged
  - `extract_visible_text("has been widely used across domains @smith2020 @jones2021.")` → `'has been widely used across domains    .'` (citations gone).
- **Fix direction**: Mirror the EN fix in Typst — build a `raw_text` from raw stripped lines and run `EVIDENCE_MARKERS.search(raw_text)` (the Typst `EVIDENCE_MARKERS` already includes `#cite\(` and `@\w+`, which only match on raw source). Keep boilerplate counting on visible text.

#### XA-2 (low) — Typst tense checker's figure/table false-positive guard almost never fires

- **Files**: `typst-paper/scripts/deai_check.py:810-814` (`_tense_false_positive`) + `_tense_fp_re` at `:390-394`.
- **Problem**: The guard suppresses a present-tense report verb when a figure/table/equation word precedes it (`Figure 2 shows ...`). The regex only matches the English words `figure/table/eq/...`. In Typst, cross-references are written `@fig-loss shows ...`, and `@fig-loss` is stripped by `extract_visible_text`, leaving `"shows ..."` with no keyword — so the guard misses it and the sentence is flagged. LaTeX authors write `Figure~\ref{...} shows`, where `\ref{}` is stripped but the literal word `Figure` survives, so the EN guard works.
- **Evidence (live repro)**: Typst `= Results` line `@fig-loss shows the training curve and the model outperforms the baseline.` → flagged `tense` on both `shows` and `outperforms` (should be exempt as a figure subject). `extract_visible_text(...)` → `'shows the training curve and the model outperforms the baseline.'`
- **Fix direction**: Either add Typst-ref forms to the FP guard (detect a stripped leading `@fig…`/`@tbl…` ref via raw text, or treat a line-leading blanked ref region as a figure subject), or document the limitation. Low severity — only affects method/experiment/result sentences whose subject is a bare `@`-ref.

#### XA-3 (low) — `term_thresholds` drift: EN flags `remarkable/remarkably/obvious`, Typst does not

- **Files**: `latex-paper-en/scripts/deai_check.py:47-50` (+ `references/deai/tone-thresholds.yaml`) vs `typst-paper/scripts/deai_check.py:47-48` (+ `references/AI_TONE_THRESHOLDS.yaml`).
- **Problem**: EN `DEFAULT_THRESHOLDS.term_thresholds` includes `remarkable/remarkably/obvious/obviously/clearly`; Typst has only `obviously/clearly` (plus its Chinese terms). An English Typst paper over-using "remarkable" / "obvious" is not caught, though the EN skill catches it. Likely unintentional drift rather than a Typst-specific decision.
- **Fix direction**: Add `remarkable`, `remarkably`, `obvious` to the Typst English term set (and YAML) if parity is intended.

### Shared limitations (present in BOTH en and typst — not a divergence)

#### SH-1 (low-medium) — tense signal `\bpresents?\b` false-positives on the adjective "present"

- **Files**: `latex-paper-en/scripts/deai_check.py:104` and `typst-paper/scripts/deai_check.py:121` (`\bpresents?\b`).
- **Problem**: `\bpresents?\b` matches the adjective in the very common phrase "the present study / present work / present paper", producing a spurious `past_in_methods_results` flag in method/experiment/result sections.
- **Evidence (live repro)**: `The present study achieves lower error.` (Results) → flagged `tense` on `presents?` (false positive) and `achieves` (arguably legitimate).
- **Fix direction**: Exclude a preceding determiner/`the present` context, or drop `present` from the auto-flag set and leave it to judgment (consistent with how `is`/`are` were intentionally excluded per the tense-guide rationale).

#### SH-2 (low, informational) — contrast/over-claim evidence suppression can't see bare citations

- **Files**: `_is_false_positive` window built from visible text — `latex-paper-en/scripts/deai_check.py:361-371`, `typst-paper/scripts/deai_check.py:425-447`.
- **Problem**: The `binary_contrast_shell` suppression requires `EVIDENCE_MARKERS` in a visible-text window; citations are stripped from visible text, so a contrast backed only by a bare `\cite{}`/`@key` (no inline number) is not recognized as evidence-bearing and stays flagged. The existing test `tests/test_typst_paper_scripts.py:437 test_..._preserves_evidence_bearing_contrast_with_cite` actually passes on the inline `12.5%` number, not the citation — the name is slightly misleading. Consistent across en/typst, so not a drift; noting for completeness. Arguably acceptable (an unquantified contrast is still worth flagging).

#### SH-3 (very low) — tense checker double-reports a line

- A single line with two present-tense signal verbs (e.g. `shows ... outperforms ...`) yields two `tense` traces, inflating `trace_count` / density score. Both skills; matches the existing multi-pattern behavior elsewhere, likely acceptable.

### Test coverage gaps

#### TST-1 (medium) — Typst tense + over-claim checkers have zero tests

- **Files**: `tests/test_deai_tense.py:1-11` and `tests/test_deai_overclaim.py:1-10` both `import deai_check` resolved to the **EN** copy only (conftest puts `SCRIPT_DIR_EN` on `sys.path`); headers assert "the typst copy shares this logic … by design". That assumption is false for the surrounding code path (XA-1 low-info-density) and for the figure FP guard (XA-2), which is exactly why those divergences went uncaught.
- **Fix direction**: Add Typst-specific cases (load the typst copy via `spec_from_file_location`, like the cover-letter tests do) covering: tense on `@fig`-ref subjects, over-claim phrase detection, and low-info-density citation exemption.

#### TST-2 (low) — no regression test pins the low-info-density citation exemption

- Neither `latex-paper-en` nor `typst-paper` tests assert that a citation-dense (number-free) paragraph is exempt from `low_information_density`. The EN "E17" fix is therefore unguarded — a future refactor could silently regress it. `tests/test_typst_paper_scripts.py:399` only checks the positive (Chinese, no evidence) case.

### Documentation / eval drift

#### DOC-1 (low) — module docs omit the tense/over-claim checkers

- `latex-paper-en/references/modules/deai.md` and `typst-paper/references/modules/DEAI.md` describe `--tier`/D1-D5 but never mention the `tense` or `overclaim` categories an agent will see in output. Dedicated guides exist and are referenced from code comments (`references/modules/tense-guide.md` / `references/evidence/over-claim-guard.md` for en; `references/TENSE_GUIDE.md` / `references/OVER_CLAIM_GUARD.md` for typst — all present), but the deai module doc doesn't link them. Minor completeness gap.

#### EVAL-1 (low) — no routing eval exercises tense/over-claim/structural-shell output

- `evals.json` (en + typst) has no entry that triggers the deai structural/tense/over-claim path; the only "overclaiming" mention is in the `experiment` routing eval (`latex-paper-en/evals/evals.json:130`). Trigger evals are routing-only, so this is low priority.

## Clean dimensions (no issues found)

- **Red-line safety (dimension #6): clean.** Neither `deai_check.py` writes to the source. `main()` only prints reports/JSON to stdout or an explicit `--output` report file; the checkers never mutate `\cite/\ref/\label`/math (LaTeX) or `@cite/<label>/$...$` (Typst). Line-by-line reads go through `extract_visible_text`, which preserves those spans out of scope but never edits the file.
- **SKILL.md contracts: consistent.** Both register the `deai` module → `scripts/deai_check.py` with `--section`, and document `--tier light|medium|heavy`; the referenced `references/modules/{deai.md,DEAI.md}` exist. All files named in code comments (`tense-guide.md`, `over-claim-guard.md`, `TENSE_GUIDE.md`, `OVER_CLAIM_GUARD.md`, both YAMLs) exist on disk.
- **Tense section gating: correct.** Both parsers' `SECTION_TITLE_RULES` emit canonical keys `method`/`experiment`/`result` (duplicates get `_2`/`_3`), and the gate `section_name.split("_",1)[0] in {"method","experiment","result"}` matches them; overclaim/tense YAML blocks match the code defaults exactly.
- **`parsers.py` copy divergence:** the en/typst split is the intentional, hash-locked `ALIGNMENTS` divergence (typst omits `LatexParser`) — not re-reported, per prior audits.
- **Other scripts** (`analyze_*`, `check_*`, `compile.py`, etc.) were untouched by the three in-focus commits and were covered by the 2026-06 audits; not re-reviewed here.

## Summary table (by severity)

| ID     | Sev       | File(s)                                        | Issue                                                                                                                               |
| ------ | --------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| XA-1   | medium    | typst `deai_check.py:602`                      | low_information_density tests evidence on visible text; strips `@cite`, so cited paragraphs falsely flagged (EN E17 fix not ported) |
| TST-1  | medium    | `test_deai_tense.py`, `test_deai_overclaim.py` | Typst tense/over-claim copies untested; let XA-1/XA-2 slip                                                                          |
| SH-1   | low-med   | en `:104` / typst `:121`                       | `\bpresents?\b` false-flags adjective "present study/work" in method/result                                                         |
| XA-2   | low       | typst `deai_check.py:810-814`                  | tense figure FP guard misses Typst `@fig`-ref subjects (`@fig:x shows` over-flagged)                                                |
| XA-3   | low       | typst `deai_check.py:47-48`                    | term list drift: `remarkable/remarkably/obvious` checked in EN, absent in Typst                                                     |
| TST-2  | low       | en+typst script tests                          | no regression pins citation exemption for low_information_density                                                                   |
| DOC-1  | low       | `modules/deai.md`, `modules/DEAI.md`           | tense/over-claim checkers undocumented in the deai module doc                                                                       |
| EVAL-1 | low       | `evals.json` (en+typst)                        | no routing eval for tense/over-claim/structural-shell output                                                                        |
| SH-2   | low(info) | en `:361-371` / typst `:425-447`               | contrast/over-claim evidence window can't see bare citations (shared, arguably intended)                                            |
| SH-3   | v.low     | both `deai_check.py`                           | tense checker double-reports a line with two signal verbs                                                                           |

**Highest-value fix:** XA-1 (port the EN raw-source evidence check to Typst `_check_low_information_density`) plus TST-1 (add Typst-specific deai tests), since the missing Typst tests are what allowed XA-1/XA-2 to drift.
