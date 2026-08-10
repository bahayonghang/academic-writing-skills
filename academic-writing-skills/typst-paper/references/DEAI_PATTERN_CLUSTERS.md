# Evidence-Aware Bilingual De-AI Pattern Clusters

> Pattern lineage: Wikipedia's community-maintained “Signs of AI writing” guidance and
> general-purpose humanizer prior art, adapted for academic evidence preservation. These
> clusters are review prompts, not AI-authorship detection rules.

## Purpose And Automation Boundary

Load this reference after the core de-AI guide when visible English or Chinese prose still
contains low-information rhetorical moves. All seven clusters are `[LLM]` / C-grade
`llm-only`. Do not add them to `deai_check.py`, `AI_TONE_THRESHOLDS.yaml`,
`AI_TONE_TERMS.md`, or `--tier`; a word, suffix, punctuation mark, or item count cannot
establish a finding.

Before classifying a span, extract `source_span`, `rhetorical_move`, `claim`, local
`evidence_anchor`, `scope_and_certainty`, and `protected_units`. Protected units include
numbers, units, entities, terminology, `@cite`, `<label>`, math, code, macros, Typst functions,
and source layout. Existing trace/density scores remain heuristic readability signals, not AI
probabilities or acceptance scores for these clusters.

## H-ING: Unsupported Analytical Tail

**Flag when** an English participial tail or Chinese accompanying clause adds significance,
cause, consequence, or scope that the preceding observation and visible evidence do not support.

**Keep when** it restates a reported metric or has a local figure, analysis, or citation anchor.
Do not match only on `highlighting`, `ensuring`, “突出”, “确保”, or surface grammar.

**Repair**: remove the unearned inference, bind it to visible evidence, or mark a testable
hypothesis. Never invent the missing analysis.

## H-PROMO: Promotional Evaluation

**Flag when** praise such as “groundbreaking / transformative / 变革性 / 重要” lacks an
observable property, comparator, condition, or citation.

**Keep when** the property and evidence that earn the evaluation are local and scope-bounded.

**Repair**: state the property and anchor; otherwise mark `[PENDING VERIFICATION]` / `待补证`.
Do not supply a number, baseline, or source.

## H-ATTR: Vague Attribution

**Flag when** readers cannot resolve who made a claim, which source supports it, or what scope
it covers, such as “experts argue / 专家认为” without a source.

**Keep when** the author or institution is named, the citation resolves, and the attributed
claim is bounded. A truthful statement that evidence is limited is a valid limitation.

**Repair**: name and cite the source, or recast the paper's own bounded claim. Never fabricate
an authority or citation.

## H-PRED: Indirect Predication

**Flag when** `serves as / represents / marks / 作为 / 标志着` only lengthens a simple
predicate without specifying a technical relation. “Table 2 serves as a presentation of the
results” can become “Table 2 presents the results.”

**Keep when** the predicate denotes a mapping, proxy, state transition, mathematical
representation, or other precise domain relation.

**Repair**: simplify only when relation and certainty remain unchanged.

## H-TERM: Synonym Cycling

**Flag when** one domain entity receives several undeclared English or Chinese names in a short
span, making identity or scope ambiguous.

**Keep when** a supertype/subtype change or alternate label is explicitly defined and needed for
precision.

**Repair**: use the author-approved canonical term consistently. Preserve glossary terms,
abbreviations, model and dataset names, genes, and chemical names.

## H-SCOPE: Manufactured Breadth

**Flag when** `from X to Y / 从 X 到 Y`, item count, or symmetry implies coverage beyond the
actual material or evidence.

**Keep when** the range is exact and every item is real, necessary, and supported. Three genuine
contributions remain three; never add or delete content to break a rule of three.

**Repair**: narrow scope to actual coverage. Do not manufacture a fourth item or discard a
supported result for rhythm.

## H-OUTLOOK: Empty Recovery Ending

**Flag when** a challenge or limitation is followed by a generic positive rebound with no result,
action, condition, or boundary.

**Keep when** the ending returns to a supported result, names a concrete future test, or states an
honest scope limitation.

**Repair**: delete the slogan or state an evidence-supported conclusion. Preserve adverse results,
trade-offs, and legitimate hedging.

### Boundary With Defensive Speculative Explanations

H-OUTLOOK concerns an empty rebound. A defensive speculative explanation requires multiple
concrete mechanisms, missing per-mechanism evidence or discriminators, and a terminal caveat.
An honest “mechanism remains undetermined / 机制尚未确定” statement is not H-OUTLOOK.

When both appearances share one claim-evidence defect, emit one finding. Defensive evidence
calibration is primary when its composite criteria are met; empty outlook is a secondary style
facet. Split only independent spans, causes, and repairs. Style-only H-OUTLOOK never enters the
`paper-audit` claims lane.

## Audit, Rewrite, Fidelity Audit

Default to findings, a risk summary, or a rewrite blueprint. Provide replacement prose only after
an explicit request. Before rewriting, inventory claims, evidence, numbers, citations, labels,
math, entities, terminology, hedges, limitations, and scope. Preserve `@cite`, `<label>`, math,
code, `#set`, `#show`, `#let`, macros, and source layout.

Local syntax and rhetorical shells may change; paragraph and section layout require separate
authorization. After rewriting, verify that no protected item disappeared or appeared, certainty
did not rise, and scope did not expand.

Use the existing `[LLM]` proposal contract:

```text
Changed: <local restructuring and rhetorical shells removed>
Protected: <claims, evidence, Typst anchors, terminology, certainty, and scope retained>
Meaning-Check: PRESERVED | NEEDS-LLM
Risk-Flags: none | not-assessed | lexical-substitution | whitespace-normalized | overstatement | ambiguity | terminology-drift | invented-claim
```

`PRESERVED` remains a proposal for author review, not a tool guarantee.

## Optional Author-Sample Calibration

An author-confirmed sample may calibrate rhythm, syntax preferences, and tone. It cannot override
the current request, venue and genre, terminology, protected syntax, evidence, claim strength, or
scope. Without a sample, use the existing academic tone; do not invent personality, first person,
opinions, humor, or emotion.

## Evidence Status

Static references, fixtures, and contract tests prove contract presence, not provider reliability.
Without provider-backed evaluation, author blind review, or real-paper precision measurement,
performance remains `missing evidence / UNVERIFIED`.
