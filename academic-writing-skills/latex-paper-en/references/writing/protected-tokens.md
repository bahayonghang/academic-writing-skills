# Protected Tokens in Prose

Single source of truth for what a polish pass must not rewrite. `SKILL.md` and the module docs point here; do not copy the table into them.

`\cite{}`, `\ref{}`, `\label{}`, macros, and math environments are already guarded by the syntax rules. This file covers the tokens that carry **no markup at all** — statistics, values with units, model and dataset names, gene and chemical names — which sit in running prose as ordinary words and therefore have no guard unless one is written.

## Three tiers

A rule engine cannot recognize every class. Each category is assigned to exactly one tier; do not promote a category without a detection method that actually works.

| Tier | Marker      | What the script does                                                                          |
| ---- | ----------- | --------------------------------------------------------------------------------------------- |
| A    | `auto`      | Detection is reliable — mask the token, never rewrite it, and list it under `Protected:`      |
| B    | `candidate` | Pattern is detectable but ambiguous — report it, never auto-apply, `Risk-Flags: not-assessed` |
| C    | `llm-only`  | No workable rule — the script does nothing; the `[LLM]` layer applies the judgement below     |

## Tier A — masked automatically

| Category                       | Examples                                           | Detection                                           |
| ------------------------------ | -------------------------------------------------- | --------------------------------------------------- |
| p-values                       | `p < 0.05`, `p<=0.01`                              | `p` followed by a comparison and a decimal          |
| Percentages                    | `92.1%`, `92.1\%`                                  | Number followed by an optional LaTeX escape and `%` |
| Value + unit                   | `3.2 GB`, `15 ms`, `2.4 GHz`, `5 kg`               | Number followed by a unit from the closed list      |
| Identifiers containing a digit | `ResNet-50`, `CIFAR-100`, `GPT-4`, `VGG16`, `TP53` | Word shape ending in digits, optionally hyphenated  |
| Capitalized hyphenated names   | `BERT-base`, `T5-small`                            | Capitalized head plus a hyphenated tail             |
| All-caps acronyms              | `SOTA`, `GPU`, `RMSE`                              | Two or more consecutive capitals                    |

Masking is deliberately generous: over-protecting an ordinary word costs one missed polish suggestion, while under-protecting a metric silently corrupts a result.

## Tier B — reported, never applied

| Category                                | Examples                          | Why not tier A                                       |
| --------------------------------------- | --------------------------------- | ---------------------------------------------------- |
| Ordinary-looking model or dataset names | `Transformer`, `ImageNet`, `Adam` | Indistinguishable from common nouns without a corpus |

These surface through the normal candidate blocks, so the author sees them without the script committing to an edit.

## Tier C — the `[LLM]` layer decides

| Category                               | Examples                          | Why no rule                                                           |
| -------------------------------------- | --------------------------------- | --------------------------------------------------------------------- |
| Gene and protein names not in all caps | `p53`, `Shh`, `mTOR`              | Shape overlaps with ordinary words and with variable names            |
| Chemical names                         | `sodium dodecyl sulfate`, `2,4-D` | Open vocabulary; a dictionary would be unmaintainable and still wrong |
| Statistic phrasing tied to a test      | "significant at the 5% level"     | Meaning lives in the sentence, not the token                          |

Guidance for the `[LLM]` layer: leave these strings byte-identical. If a rewrite would touch one, keep the original wording and note it — an author correcting a preserved term costs a second; an author discovering a silently renamed gene after submission costs a correction notice.

## Related

- Contract fields and the `Risk-Flags` closed set: [routing-rules.md](../modules/routing-rules.md)
- Claim strength: [over-claim-guard.md](../evidence/over-claim-guard.md)
