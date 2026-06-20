# Workflow & Best Practices

Choose the smallest module sequence that fits the user request.

## Common Review Paths

1. Build/debug path:
   `compile` -> `bibliography`
2. Prose quality path:
   `grammar` -> `sentences` -> `logic`
3. Submission hygiene path:
   `format` -> `figures` -> `title`
4. Language cleanup path:
   `translation` or `deai`, then `expression` if tone polish is still needed
5. Experiment scrutiny path:
   `experiment` on its own unless the user also asks for logic or figure review

## Best Practices

1. Route to one concern at a time instead of invoking every module by default.
2. Preserve `\cite{}`, `\ref{}`, `\label{}`, math, and custom macros unless edits are explicitly requested.
3. Treat script output as raw analysis; convert it into concise LaTeX-friendly findings for the final response.
4. Use version control when the user asks for source edits after the review phase.

## Revision Order (logic → sentence → lexical, do not reverse)

When a request needs more than one polish pass, apply changes in this order and do
not invert it:

1. **Argument / logic** — paragraph order, missing or duplicated main messages, section transitions.
2. **Sentence structure** — split >40-word sentences, passive→active, front-load high-information content.
3. **Lexical / formatting** — AI-tone words, number/unit format, en-dash vs hyphen, acronym consistency.

Why the order is fixed: polishing a sentence's wording (step 3) before fixing
structure (step 1) wastes the effort when step 1 later deletes or merges that
paragraph. Coarse-to-fine is several times more efficient.
