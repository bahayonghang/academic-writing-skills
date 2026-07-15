# Routing Rules — Full Detail

Extended routing guidance for `latex-paper-en`. The SKILL.md keeps only the core rules; this file preserves the full decision notes.

## Module inference

- Infer the module from the user request before asking follow-up questions. Ask for the module only when two or more modules are equally plausible after keyword routing.
- If the user asks for 2-3 compatible checks in one turn, run them sequentially instead of forcing a single-module reply.
- Execution order when multiple modules are needed: `compile` -> `bibliography` -> `format` -> `figures` / `tables` / `caption` / `pseudocode` -> `grammar` / `sentences` / `deai` -> `logic` / `literature` / `experiment` / `abstract` -> `section-writing` -> `title` / `expression` / `translation` / `adapt`.
- When applying multiple polish passes to the same prose, work coarse-to-fine — argument/logic -> sentence structure -> lexical/formatting — and do not reverse it; see `references/modules/workflow.md`.

## Choosing between adjacent modules

- Prefer `logic` for cross-section alignment requests (abstract vs introduction vs conclusion), introduction funnel issues, or contribution drift; prefer `literature` only when the problem is specifically about Related Work organization, comparison, or gap derivation.
- Prefer `section-writing` when the user asks to draft, rewrite, restructure, or reviewer-polish a specific section, or asks for paragraph roles, mini-outlines, reverse outlines, or claim-evidence maps. Prefer the diagnostic modules first when the user asks to check whether something is wrong.
- Keep `experiment` for results, discussion, baseline, ablation, significance, limitation, and conclusion-completeness concerns even if the user phrases them as "logic" problems.

## Special flags and loading rules

- For `section-writing`, load `references/modules/section-writing.md`, then exactly one active section guide from `references/writing/section-writing/` unless the user also asks for flow or self-review.
- For whole-paper motivation/red-thread questions ("does every introduction promise get tested and resolved?"), run `logic` with `--motivation-thread`; it appends a read-only Promise Map + Closure Map heuristic and leaves default `logic` output unchanged.
- For graded de-AI / AIGC-dimension analysis, run `deai` with `--tier light|medium|heavy`; it scales thresholds, adds a D1 sentence-length check, and labels findings by dimension (D1-D5). Omitting `--tier` keeps the default output.

## Failure handling

- When a script fails, stop the current module, report the exact command plus exit code, and recommend the next smallest useful fallback instead of silently switching modules.

## Output contract details

- For `literature`, default to diagnosis + rewrite blueprint first; only produce paragraph-level rewriting when the user explicitly asks for prose.
- For `section-writing`, return a section objective, compact outline, paragraph roles, rewrite blueprint or prose proposal, claim-evidence map, and self-review checklist. Mark missing evidence instead of filling it.

## Safety rationale (full text)

- Don't invent citations, metrics, baselines, or experimental results — fabricated evidence is harder to retract once the user trusts it than a clearly flagged gap.
- Leave `\cite{}`, `\ref{}`, `\label{}`, custom macros, and math environments untouched by default — a stray edit there is far harder to spot in a diff than a prose edit, and breaks compilation silently.
- Treat generated prose as proposals, not commits — keep source-preserving checks separate from rewriting so the user can validate each step.
- Do not enable online bibliography checks unless the user explicitly asks for external verification or confirms that citation metadata may be sent to third-party APIs.
- The `deai` module improves readability; it is not a detector-evasion tool and does not remove a disclosure obligation. If an LLM had a non-trivial role in the paper, remind the user to disclose it per the target venue's policy (`references/venues/ai-disclosure.md` has the per-venue matrix — some venues require disclosure in the cover letter, a dedicated section, or the checklist).
