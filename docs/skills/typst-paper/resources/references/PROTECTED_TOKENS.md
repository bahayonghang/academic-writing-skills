# Protected Tokens in Prose

Single source of truth for the tokens a polish pass **must not rewrite**. `SKILL.md` and the module docs only point here; do not copy this table into them.

`@cite`, `<label>`, math blocks, and Typst macros are already guarded by the syntax rules. This file covers the class that carries **no markup at all** — statistics, values with units, model and dataset names, gene and chemical names. In running prose they are ordinary words, so they have no guard unless one is written.

## Three tiers

A rule engine cannot recognize every category. Each category belongs to exactly one tier; do not promote one without a detection method that actually works.

| Tier | Marker      | Script behaviour                                                                                |
| ---- | ----------- | ----------------------------------------------------------------------------------------------- |
| A    | `auto`      | Detection is reliable — mask the token, never rewrite it, and list it under `Protected:`        |
| B    | `candidate` | Pattern is detectable but ambiguous — report only, never auto-apply, `Risk-Flags: not-assessed` |
| C    | `llm-only`  | No workable rule — the script does nothing; the `[LLM]` layer judges per the guidance below     |

## Tier A — masked automatically

| Category                       | Examples                                           | Detection                                    |
| ------------------------------ | -------------------------------------------------- | -------------------------------------------- |
| p-values                       | `p < 0.05`, `p<=0.01`                              | `p` plus a comparison plus a decimal         |
| Percentages                    | `92.1%`                                            | Number plus an optional escape plus `%`      |
| Value + unit                   | `3.2 GB`, `15 ms`, `2.4 GHz`, `5 kg`               | Number plus a unit from the closed list      |
| Identifiers containing a digit | `ResNet-50`, `CIFAR-100`, `GPT-4`, `VGG16`, `TP53` | Word shape ending in digits, hyphens allowed |
| Capitalized hyphenated names   | `BERT-base`, `T5-small`                            | Capitalized head plus a hyphenated tail      |
| All-caps acronyms              | `SOTA`, `GPU`, `RMSE`                              | Two or more consecutive capitals             |

Masking is deliberately generous: over-protecting an ordinary word costs one missed polish suggestion, while under-protecting a metric silently corrupts a result.

## Tier B — reported, never applied

| Category                                       | Examples                          | Why not tier A                                       |
| ---------------------------------------------- | --------------------------------- | ---------------------------------------------------- |
| Model/dataset names shaped like ordinary nouns | `Transformer`, `ImageNet`, `Adam` | Indistinguishable from common nouns without a corpus |

They surface through the normal candidate blocks, so the author sees them without the script deciding for them.

## Tier C — the `[LLM]` layer decides

| Category                           | Examples                          | Why no rule                                                     |
| ---------------------------------- | --------------------------------- | --------------------------------------------------------------- |
| Gene/protein names not in all caps | `p53`, `Shh`, `mTOR`              | Shape overlaps with ordinary words and variable names           |
| Chemical names                     | `sodium dodecyl sulfate`, `2,4-D` | Open vocabulary; a dictionary is unmaintainable and still wrong |
| Statistic phrasing tied to a test  | "significant at the 5% level"     | The meaning lives in the sentence, not the token                |

Guidance for the `[LLM]` layer: keep these strings byte-identical. If a rewrite would touch one, preserve the original wording and say so — an author correcting a preserved term costs a second; discovering a silently renamed gene after submission costs a correction notice.

## Related

- Contract fields and the `Risk-Flags` closed set: [skill-routing-notes.md](skill-routing-notes.md)
- Claim strength: [OVER_CLAIM_GUARD.md](OVER_CLAIM_GUARD.md)
