# Method Section Writing

## Objective

Make the method reproducible and motivated: readers should understand what each module does, why it is needed, and why it should help.

## Pre-Writing Table

Before drafting, build this table:

| Module | Input -> Output | Why Needed | Why It Works | Evidence Later |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | table/ablation/analysis |

If a module has no motivation or no later evidence, mark it before writing prose.

## Section Structure

1. **Overview**: task setting, core contribution, pipeline figure pointer, and subsection map.
2. **Module subsections**: one subsection per technical module or design unit.
3. **Implementation details**: hyperparameters, normalization, training setup, practical choices.

## Module Triad

Each method subsection should cover:

1. **Motivation**: what challenge or failure mode requires this module.
2. **Design**: concrete representation, network, data structure, algorithm, or forward process.
3. **Technical advantage**: why this design is better suited than alternatives, preferably tied to measurable behavior.

## Writing Order

1. Draft the design backbone first: `Given input -> step 1 -> step 2 -> output`.
2. Add motivation before or around the design so the reader knows why each operation exists.
3. Add technical advantage after the design, keeping claims bounded to what experiments can test.
4. Check notation and term consistency across the pipeline figure, equations, captions, and subsection titles.

## Hard Boundaries

- Do not invent equations, hyperparameters, algorithm steps, complexity claims, or implementation details.
- If a detail is missing, write a reviewer-facing TODO rather than filling it in.
- Preserve math, macros, labels, and figure references verbatim unless source edits are explicitly requested.
