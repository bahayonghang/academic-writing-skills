# Routing, Workflow, and Safety Notes (typst-paper)

Extended guidance moved verbatim from `SKILL.md`. Read when routing is ambiguous, when combining modules, or when a boundary question arises.

## Routing Rules (full)

- Infer the module from the user request first. Ask for the module only if the request still maps equally well to multiple incompatible modules.
- If the user requests 2-3 compatible checks, run them in sequence rather than collapsing everything into one generic review.
- Use this execution order when multiple modules are needed: `compile` -> `bibliography` -> `format` -> `pseudocode` / `tables` -> `grammar` / `sentences` / `deai` -> `logic` / `literature` / `experiment` -> `title` / `expression` / `translation` / `adapt`.
- When applying multiple polish passes to the same prose, work coarse-to-fine — argument/logic -> sentence structure -> lexical/formatting — and do not reverse it; see `references/modules/WORKFLOW.md`.
- For bibliography requests, decide BibTeX vs Hayagriva before running the script; do not guess the format after the fact.
- Prefer `logic` for abstract-introduction-conclusion alignment, introduction funnel breaks, or contribution drift; prefer `literature` only when the user is specifically asking for Related Work synthesis, comparison, or gap derivation.
- For whole-paper motivation/red-thread questions ("does every introduction promise get tested and resolved?"), run `logic` with `--motivation-thread`; it appends a read-only Promise Map + Closure Map heuristic and leaves default `logic` output unchanged.
- For graded de-AI / AIGC-dimension analysis, run `deai` with `--tier light|medium|heavy`; it scales thresholds, adds a bilingual D1 sentence-length check, and labels findings by dimension (D1-D5). Omitting `--tier` keeps the default output.
- Keep `pseudocode` for `algorithm-figure`, `algorithmic`, `lovelace`, caption, wrapper, and IEEE-like style-hook issues even when the user phrases them as formatting problems.
- If a command fails, report the exact command and exit code before suggesting the next fallback; do not silently replace a failed script run with a generic prose review.

## Triggering scenarios (full list)

Use this skill when the user has an existing `.typ` paper project and wants help with:

- Typst compilation or export issues
- format or venue compliance
- bibliography validation for BibTeX or Hayagriva
- grammar, sentence, logic, or expression review
- literature review restructuring, related-work synthesis, or research-gap derivation
- translation or bilingual polishing
- title optimization
- pseudocode and algorithm-block review
- de-AI editing
- experiment-section review

## Safety rationale (full)

- Don't invent citations, labels, or experimental claims — fabricated evidence is harder to retract once the user trusts it than a clearly flagged gap.
- Leave `@cite`, `<label>`, math blocks, and Typst macros untouched by default — a stray edit there is far harder to spot in a diff than a prose edit, and Typst surfaces those errors only at compile time.
- Keep compile diagnostics separate from prose rewrites — bundling them encourages the user to apply both at once and lose track of which change broke what.
- Do not enable online bibliography checks unless the user explicitly asks for external verification or confirms that citation metadata may be sent to third-party APIs.

## Required inputs (detail)

- `main.typ` or the Typst entry file.
- Optional `--section SECTION` for targeted analysis.
- Optional bibliography path when the request targets references.
- Optional venue context when the user cares about IEEE, ACM, Springer, or similar expectations.

If arguments are missing, preserve the inferred module and ask only for the missing Typst entry file, section, bibliography path, or venue context.

## Auxiliary scripts

- `scripts/deai_batch.py`: batch the `deai` module over many sections/files.
- `scripts/online_bib_verify.py`: the online backend behind `verify_bib.py --online`.
