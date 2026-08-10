# Evidence-Aware De-AI Pattern Clusters

> Pattern lineage: Wikipedia's community-maintained “Signs of AI writing” guidance and
> general-purpose humanizer prior art, adapted here for academic evidence preservation.
> These patterns are review prompts, not AI-authorship detection rules.

## Purpose And Automation Boundary

Use this reference after the core de-AI guide when visible prose still contains low-information
rhetorical moves. All seven clusters are `[LLM]` / C-grade `llm-only`: a word, suffix,
punctuation mark, or item count cannot establish a finding. Do not add these clusters to
`deai_check.py`, threshold YAML, tone-term lists, or `--tier`.

Before classifying a span, extract:

1. `source_span` and its section role;
2. the `rhetorical_move` and the claim it adds or changes;
3. local `evidence_anchor` values such as metrics, comparisons, figures, experiments, or citations;
4. `scope_and_certainty`, including hedges and limitations;
5. `protected_units`: numbers, units, entities, terminology, citations, labels, math, macros, and layout.

Existing script trace/density scores remain heuristic readability signals. They are not AI
probabilities and are not acceptance scores for these clusters.

## H-ING: Unsupported Analytical Tail

**Flag when** a participial or accompanying tail adds significance, cause, consequence, or scope
that the preceding observation and visible evidence do not support.

**Keep when** the tail restates a reported metric or has a local figure, analysis, or citation
anchor. Do not flag text merely because it contains `highlighting`, `ensuring`, or an `-ing` form.

**Repair**: remove the unearned inference, bind it to visible evidence, or mark it as a testable
hypothesis. Do not invent the missing analysis.

## H-PROMO: Promotional Evaluation

**Flag when** praise such as “groundbreaking”, “transformative”, or “important” is not tied to an
observable property, comparator, condition, or citation.

**Keep when** the evaluation is immediately bounded by the property and evidence that earn it.

**Repair**: state the observable property and anchor. If neither exists, use `needs evidence`
instead of supplying a number, baseline, or source.

## H-ATTR: Vague Attribution

**Flag when** readers cannot identify who made a claim, which source supports it, or what scope the
attribution covers: for example, “experts argue” without a resolvable source.

**Keep when** the author or institution is named, the citation is resolvable, and the attributed
claim has a clear boundary. A truthful “evidence is limited” statement is also a valid limitation.

**Repair**: name and cite the source, or recast the sentence as the paper's own bounded claim. Never
fabricate an authority or citation.

## H-PRED: Indirect Predication

**Flag when** `serves as`, `represents`, `marks`, or a similar construction only lengthens a simple
predicate and contributes no technical relation. Example: “Table 2 serves as a presentation of the
results” can become “Table 2 presents the results.”

**Keep when** the predicate precisely denotes a mapping, proxy, state transition, mathematical
representation, or other domain relation.

**Repair**: simplify only when the relation and certainty remain unchanged.

## H-TERM: Synonym Cycling

**Flag when** one domain entity receives several undeclared names in a short span, creating doubt
about whether the text refers to the same object or different scopes.

**Keep when** a supertype/subtype change or alternate label is explicitly defined and needed for
precision.

**Repair**: select the author-approved canonical term and use it consistently. Preserve glossary
terms, abbreviations, model names, dataset names, genes, and chemical names.

## H-SCOPE: Manufactured Breadth

**Flag when** a `from X to Y` range, item count, or symmetric structure implies coverage beyond the
actual material or evidence.

**Keep when** the range is exact and every listed item is real, necessary, and supported. Three
genuine contributions remain three; do not add or delete content to break a rule of three.

**Repair**: narrow the scope to what the paper actually covers. Never manufacture a fourth item or
discard a supported result for rhythm.

## H-OUTLOOK: Empty Recovery Ending

**Flag when** a challenge or limitation is followed by a generic positive rebound with no result,
action, condition, or boundary.

**Keep when** the ending returns to a supported result, names a concrete future test, or states an
honest scope limitation.

**Repair**: delete the slogan or replace it with an evidence-supported conclusion. Preserve adverse
results, trade-offs, and legitimate hedging.

### Boundary With Defensive Speculative Explanations

H-OUTLOOK concerns an empty positive rebound. A defensive speculative explanation requires multiple
concrete mechanisms, missing per-mechanism evidence or discriminators, and a terminal caveat that
withdraws those mechanisms. An honest “mechanism remains undetermined” statement is not H-OUTLOOK.

If both appearances share one claim-evidence defect, emit one finding. When the defensive composite
criteria are met, make evidence calibration primary and record empty outlook only as a secondary
style facet. Split findings only when source spans, root causes, and repairs are independent; a
style-only H-OUTLOOK finding never enters the `paper-audit` claims lane.

## Audit, Rewrite, Fidelity Audit

Default to findings, a risk summary, or a rewrite blueprint. Provide replacement prose only after an
explicit prose request.

Before rewriting, inventory every claim, evidence anchor, number, citation, label, formula, entity,
canonical term, hedge, limitation, and scope boundary. Local syntax and rhetorical shells may change;
paragraph and section layout remain unchanged unless separately authorized. After rewriting, verify
that no item disappeared, appeared, became more certain, or expanded in scope without being flagged.

Use the existing `[LLM]` proposal contract:

```text
Changed: <local restructuring and rhetorical shells removed>
Protected: <claims, evidence, anchors, terminology, certainty, and scope retained>
Meaning-Check: PRESERVED | NEEDS-LLM
Risk-Flags: none | not-assessed | lexical-substitution | whitespace-normalized | overstatement | ambiguity | terminology-drift | invented-claim
```

`PRESERVED` remains a proposal for author review, not a tool guarantee.

## Optional Author-Sample Calibration

An author-confirmed sample may calibrate rhythm, syntax preferences, and tone. It cannot override the
current request, target venue and genre, terminology, protected syntax, evidence, claim strength, or
scope. Without a sample, use the skill's existing academic tone; do not invent personality, first
person, opinions, humor, or emotion.

## Evidence Status

Static references, fixtures, and contract tests prove the contract is present, not that a provider
implements it reliably. Without provider-backed evaluation, author blind review, or real-paper
precision measurement, performance remains `missing evidence / UNVERIFIED`.
