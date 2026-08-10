# Method Section Writing

## Objective

Make the method reproducible and motivated. A reader should be able to trace why each module
exists, how its input becomes its output, and how that output enters the next module without
reconstructing the intended pipeline.

## Pre-Writing Table

Before drafting, map each module:

| Module | Input -> Output | Why Needed | Why It Works | Evidence Later |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | table/ablation/analysis |

If a module has no motivation or no later evidence, mark it before writing prose.

Then map every adjacent edge:

| Upstream module | Upstream output | Connection type | Intermediate transform | Downstream use |
| --- | --- | --- | --- | --- |
| A | `z_A` | serial data | align/project | direct input to B |
| B | candidate set | calibration/selection | threshold and budget filter | supervision for C |

The map is complete when every adjacent module pair has one row and the output, transform, and
downstream-use cells are filled.

## Section Structure

1. **Overview**: task and data contract, shared input, module roles, execution order, train/inference
   differences, final output, and pipeline-figure pointer.
2. **Module subsections**: one subsection per technical module or design unit.
3. **Implementation details**: hyperparameters, normalization, training setup, practical choices,
   update/freeze states, stopping conditions, and fallback paths.

The overview is complete when its data flow agrees with the figure, equations, and pseudocode.

## Module Triad

Each method subsection should cover:

1. **Motivation**: what challenge or failure mode requires this module.
2. **Design**: concrete representation, network, data structure, algorithm, or forward process.
3. **Technical advantage**: why this design is better suited than alternatives, preferably tied to
   measurable behavior.

Also close the local contract: name the input, key transforms, output semantics, and downstream
consumer. One role may occupy a sentence or a paragraph; fixed announcement phrases are not required.

## Inter-Module Interface Contract

For every adjacent pair, state the upstream output, connection transform, and downstream use.

| Connection type | Criterion | What the prose must expose |
| --- | --- | --- |
| Serial data | A's output directly becomes B's input | name, shape, semantics, and any projection |
| Parallel representation | A and B share input and build separate representations | fusion point and fusion rule |
| Supervision/target | A produces labels, intervals, weights, losses, or constraints for B | entry point in B's objective |
| Calibration/selection | A produces candidates and B admits or ranks them | admission rule; candidates are not final samples |
| Feedback/control | downstream evaluation updates an upstream object | feedback quantity, update target, and stop condition |
| Remaining constraint | A resolves one limitation but exposes another | the unresolved constraint that requires B |

**M-NONDIRECT.** When two modules have no direct data dependency, exclude the likely misreading:

> B does not condition on A's predictions. They share the same input semantics and are linked by
> the supervision relation constructed in C.

An interface is closed only when the reader can identify the producer, transformation, and consumer.

## Equation Closure

Close each key equation as `purpose -> equation -> symbol gloss -> output semantics -> downstream use`.
Before the equation, name the required computation and input object. After it, define new symbols,
state what object the equation produces, and identify the next consumer.

Notation consistency and equation closure are separate checks: consistency detects conflicting names
or meanings; closure detects a missing purpose, gloss, output, or downstream link even when notation
is internally consistent. Equation order should follow computation order unless the derivation order
is explicitly justified.

## Heading Discipline

Run-in headings may navigate independent technical units; they should not replace their causal and
interface links. A dense sequence such as `\paragraph{Fusion.} This module is used to ...` becomes
announcement scaffolding when the body only restates responsibilities.

The heading itself is not the defect. Method subsections with real input/output contracts are valid,
as are evidence-led experiment-result lead-ins and the Related Work grouping pattern in
[`style-guide.md`](../style-guide.md#related-work). Review the first and last paragraph of each module;
the method chain is readable when those paragraphs alone expose the constraint, output, and next use.

## Evidence Tiers

Classify the claim before choosing its strength. The
[`claim-evidence-contract.md`](../../evidence/claim-evidence-contract.md) sets the evidence ceiling;
[`over-claim-guard.md`](../../evidence/over-claim-guard.md) supplies wording below that ceiling.

| Claim type | Minimum visible anchor | Strength ceiling in the method section |
| --- | --- | --- |
| Definition fact | equation or algorithm that directly defines it | `supported`, within the definition |
| Mechanism-level effect | structural, complexity, or logical derivation | `supported`; no empirical performance claim |
| Empirical performance | metric plus setting; comparison artifact for broader claims | `observed` locally, `supported/strong` only with matching evidence |
| Causal attribution | discriminating ablation, intervention, or proof | `strong` only within that design; otherwise do not make the causal claim |

Terms such as “improves,” “enhances,” and “effectively solves” do not create evidence. When only the
design is visible, state what it is used for or what it guarantees by definition.

## Writing Order

1. Lock equations, symbols, citations, values, data splits, and reported results; finish when every
   protected fact has an explicit source location.
2. Draw the module graph with input, transform, output, train/freeze state, and fallback path; finish
   when every core module has all applicable fields.
3. Fill the adjacent-edge table; finish when every graph edge has a connection type and downstream use.
4. Rewrite the overview and inter-module transitions first, module-internal sentences second, and
   headings last; finish when the prose and graph express the same edge order.
5. Check every key equation for purpose, gloss, output semantics, and downstream use; finish when no
   closure role is blank.
6. Map each benefit claim to the evidence tiers above; finish when no wording exceeds its visible anchor.
7. Read only each module's first and last paragraph; finish when that reduced view still reconstructs
   the complete method chain.

## Hard Boundaries

- Do not invent equations, hyperparameters, algorithm steps, complexity claims, evidence, or
  implementation details.
- If a detail is missing, write a reviewer-facing TODO rather than filling it in.
- Preserve math, macros, labels, citations, values, and figure references verbatim unless source edits
  are explicitly requested.

## Diagnostic

Run the candidate checker only on the method scope:

```bash
uv run python -B scripts/analyze_logic.py main.tex --section methods
```

Treat `M-HEADING`, `M-SEQWORD`, and `M-EQUATION` as `[Script]` candidates requiring LLM review. Fill
the emitted `M-EDGETABLE` before rewriting module transitions.

## Sources

- [MIT EECS Communication Lab, Paper: Methods (EE)](https://mitcommlab.mit.edu/eecs/commkit/journal-article-methods-ee/)
- [Gopen and Swan, The Science of Scientific Writing](https://www.americanscientist.org/blog/the-long-view/the-science-of-scientific-writing)
- [IEEE Author Center, Structure Your Article](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/)
- [Nature, Formatting Guide](https://www.nature.com/nature/for-authors/formatting-guide)
- [PLOS ONE, Submission Guidelines](https://journals.plos.org/plosone/s/submission-guidelines)
