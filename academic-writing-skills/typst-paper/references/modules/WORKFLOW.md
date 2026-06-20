# Workflow & Best Practices

If user requests complete review, execute in order:

1. Format Check → fix critical issues
2. Grammar Analysis → fix errors
3. De-AI Editing → reduce AI writing traces
4. Long Sentence Analysis → simplify complex sentences
5. Expression Restructuring → improve academic tone

## Best Practices

1. **Start with Compilation**: Verify document compiles before other checks
2. **Iterative Refinement**: Apply one module at a time for better control
3. **Preserve Protected Elements**: Never modify `@cite`, `@ref`, `@label`, math environments
4. **Verify Before Commit**: Review all suggestions before accepting changes
5. Use with version control (git) to track changes

## Revision Order (logic → sentence → lexical, do not reverse)

When a request needs more than one polish pass, apply changes in this order and do
not invert it:

1. **Argument / logic** — paragraph order, missing or duplicated main messages, section transitions.
2. **Sentence structure** — split overly long sentences, passive→active, front-load high-information content.
3. **Lexical / formatting** — AI-tone words, number/unit format, dash usage, acronym consistency.

Why the order is fixed: polishing a sentence's wording (step 3) before fixing
structure (step 1) wastes the effort when step 1 later deletes or merges that
paragraph. Coarse-to-fine is several times more efficient.
