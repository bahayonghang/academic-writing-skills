# Pre-Submission Mechanical Rules

Source attribution: adapted from
`ref/Supervisor-Skills/plugins/phd-research/skills/pre-submission-reviewer`
(license: CC-BY-4.0). This reference keeps the rule structure and severity
calibration while fitting `paper-audit`'s deep-review-first architecture.

This file lists the deterministic rules and the AI-tone term list. For how
those rules plug into each mode (gate behavior, deep-review promotion, PDF
skip rules, regression in re-audit), see `references/PRESUBMISSION_GUIDE.md`.

## Purpose

`paper-audit` uses this layer as a deterministic final-week check, not as a
competing mode. The `PRESUBMISSION` script feeds:

- `quick-audit`: fast mechanical readiness signals.
- `gate`: advisory findings plus any true Critical blockers.
- `re-audit`: regression comparison for mechanical findings.
- `deep-review` Phase 0: context for reviewer lanes.

For full/editor deep-review, high-signal `PRESUBMISSION` findings can become
`pre_submission_readiness` lane issues. Focused theory, literature,
methodology, and logic reviews keep these findings in Phase 0 context only.

## Severity Mapping

| Source taxonomy | paper-audit script severity | deep-review bundle severity |
|---|---|---|
| CRITICAL | Critical / P0 | major, `gate_blocker=true` |
| MAJOR | Major / P1 | moderate |
| MINOR | Minor / P2 | minor or Phase 0 only |

`gate` fails only on Critical script findings or failed checklist items. Major
and Minor `PRESUBMISSION` findings stay advisory.

## Deterministic Script Rules

These rules are safe for `pre_submission_check.py` because they are directly
visible in source or extracted PDF text.

### Grammar and style IDs

- G1: em dash found in reader-visible prose. Default severity: Major.
- G2: paragraph longer than 180 words or more than 8 sentences. Default:
  Minor.
- G3: paragraph starts with a weak transition instead of a claim-like topic
  sentence. Default: Minor.
- G4: banned AI-tone term group appears three or more times. Default: Major.
- G5: abstract lacks the five submission elements: background, objective,
  method, results, conclusion. Missing results or missing quantitative result
  evidence is Major; other missing elements are Minor.
- G6: repeated promotional claim language without local evidence should be
  escalated to reviewer judgment, not auto-failed.
- G7: article, tense, agreement, which/that, and Chinglish findings require
  exact quoted evidence when reported by an LLM reviewer.
- G8: passive voice or sentence-length findings are Minor unless they hide a
  method or result claim.

### LaTeX/source hygiene IDs

- L1: citation lacks a non-breaking tie before `\cite...`, for example
  `Method \cite{key}` instead of `Method~\cite{key}`. Default: Minor.
- L2: label contains spaces. Default: Major.
- L3: label uses hyphens where underscores are safer. Default: Minor.
- L4: numbered equation environment has no label. Default: Minor.
- L5: numbered equation label is never referenced in text. Default: Minor.
- L6: figure/table source has a caption but no concrete finding. Default:
  Minor.
- L7: figure/table source has a label but no preceding in-text reference.
  Covered by `references`; do not duplicate unless source context matters.
- L8: bibliography, citation key existence, and malformed references stay in
  `bib`, `citations`, and `references` modules.
- L9: page-limit checks stay venue/checklist specific.
- L10: compile errors are outside `paper-audit`; route to the LaTeX/Typst
  writing skill when the user asks to fix source.
- L11: source comments should be ignored by mechanical scans.
- L12: PDF input must skip source-only checks instead of guessing LaTeX state.
- L13: source-only findings should include line numbers whenever available.

### Figure quality IDs

The script can only check source captions. The following remain manual or LLM
reviewer prompts:

- F1: caption lacks a concrete finding or comparison cue. Script-checkable from
  source captions.
- F2: raster instead of vector final figure.
- F3: post-scaling font size too small.
- F4: non-color-blind-safe palette without dual encoding.
- F5: chartjunk or decorative elements that obscure comparison.
- F6: overview figure labels do not match section titles.

F2-F6 require the PDF/figure artifacts or reviewer inspection. Do not report
them as deterministic script findings unless a visual checker proves them.

## Forbidden AI-Tone Terms

The script treats these as a frequency threshold, not a single-word ban. Three
or more matches in reader-visible text becomes Major/P1:

- innovative
- pioneering
- revolutionary
- transformative
- breakthrough
- unprecedented
- remarkable
- superior
- surpass
- state-of-the-art
- highlights the potential of
- pave the way
- profound challenge
- at its essence

Single uses may be legitimate technical wording. Keep them in Phase 0 context
unless they become a pattern.

## Abstract Five-Element Rule

A submission-ready abstract should show:

1. Background or problem pressure.
2. Objective or research question.
3. Method or approach.
4. Concrete result, preferably quantitative.
5. Conclusion, implication, or bounded takeaway.

Missing quantitative result evidence is a Major readiness finding because it
prevents a final-week gate from seeing what the paper actually achieved.

## PDF vs Source Behavior

PDF mode runs only text-verifiable checks:

- em dash scan
- banned AI-tone frequency
- abstract five-element check
- long paragraph/topic-sentence weak signals

PDF mode explicitly skips:

- LaTeX citation tie hygiene
- label space/hyphen rules
- numbered equation reference rules
- source-caption rules

The skip must be visible in script output as an ignored comment or metadata,
not as an issue.

## Integrity Gate

Before using these findings in reviewer-facing output:

1. Every finding must be tied to source text, a line number, or a section.
2. Severity must follow the mapping above; taste-only concerns are not Critical.
3. Script findings must keep `[Script]` provenance.
4. `PRESUBMISSION` findings should not replace deep reviewer judgment about
   methodology, theory, literature, or claim validity.
5. The skill audits only; it does not rewrite paper source.
