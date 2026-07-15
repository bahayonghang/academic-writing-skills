# Tense Guide

How verb tense maps to paper sections, and which present-tense signal words usually
mark a mistake. The goal is not blanket past tense — each section has a convention,
and the most common error is narrating Methods/Results in the present tense.

The script (`deai_check.py`) flags a focused set of present-tense **reporting verbs**
inside Methods/Results as `[Script]` LOW traces. The tables below cover the judgment
calls the script deliberately leaves alone (notably `is` / `are`).

## Tense by section

| Section / part                                | Default tense          | Example                                             |
| --------------------------------------------- | ---------------------- | --------------------------------------------------- |
| Abstract — background                         | present                | "Long-context inference _is_ expensive for ..."     |
| Abstract — methods                            | past                   | "We _trained_ ... / Models _were evaluated_ on ..." |
| Abstract — results                            | past                   | "The model _achieved_ 92.3% / We _observed_ ..."    |
| Abstract — conclusion                         | present                | "These results _provide_ a basis for ..."           |
| Introduction — known background               | present                | "Quantization _reduces_ memory footprint."          |
| Introduction — a specific prior study         | past                   | "Vaswani et al. _introduced_ the Transformer."      |
| Introduction — prior conclusion still holding | present                | "Attention _is_ effective for long sequences."      |
| Introduction — aims of this work              | past (+ some present)  | "Here we _propose_ X and _present_ a study of ..."  |
| **Methods**                                   | **past (absolute)**    | "We _sampled_ ... / Inputs _were normalized_ ..."   |
| **Results**                                   | **past (absolute)**    | "Accuracy _ranged_ from ... / We _found_ ..."       |
| Results — describing a figure/table itself    | present                | "Figure 2 _shows_ ... / Table 1 _lists_ ..."        |
| Discussion — restating a finding              | past                   | "We _found_ that ..."                               |
| Discussion — interpreting                     | present                | "These results _suggest_ that ..."                  |
| Discussion — inference / speculation          | present + modal        | "_may_ indicate / _could_ explain"                  |
| Discussion — limitations                      | present                | "A limitation of this study _is_ ..."               |
| Figure / table caption                        | **present (absolute)** | "Figure 1 _shows_ the architecture of ..."          |

## Signal words (scan Methods / Results)

The most common slip is a present-tense reporting verb where past tense is expected:

- `shows / reveals / demonstrates / indicates / presents / confirms / achieves / outperforms`
  in Methods/Results narration → usually should be `showed / revealed / demonstrated / …`.
  The script flags these.

### `is` / `are` — check by hand (not flagged by the script)

Present-tense `is` / `are` in Methods/Results is _often_ a tense error, but it has too
many legitimate uses to flag automatically. Keep it when it is:

- a **definition**: "Let _G_ be ... / The loss _is defined as_ ...";
- a **standing general truth**: "Cross-entropy _is_ convex in the logits.";
- describing **a figure/table**: "Table 2 _is_ organized by ...";
- a **software capability**: "PyTorch _supports_ mixed precision.".

Otherwise prefer past tense: "The threshold _was set_ to 0.5" (not "_is_ set"),
"Samples _were drawn_" (not "_are drawn_").

## Exceptions the script skips (present tense is correct)

1. **Figures / tables / equations as subject**: "Figure 3 _shows_ ...", "as _shown_ in
   Fig. 4", "Table 1 _lists_ ...", "Equation 2 _gives_ ..." — describing the artifact
   itself takes present tense.
2. **Software / tool capability**: "The toolkit _provides_ ...", "PLINK _supports_ ...".
3. **General definitions and standing truths** that happen to sit inside a methods
   paragraph.

If a flagged line is one of these, it is a false positive — leave it.

## Boundary with other guides

- This guide is about **tense**. Wording strength (causal / firstness / universality)
  lives in [over-claim-guard.md](../evidence/over-claim-guard.md).
- Surface grammar beyond tense lives in [grammar.md](grammar.md).

## Script support

`deai_check.py` flags present-tense reporting verbs in Methods/Results as `[Script]`
LOW traces (config: `tense:` in `references/deai/tone-thresholds.yaml`, toggle with
`enabled`). It guards against figure/table/software false positives but cannot judge
`is` / `are` — use the checklist above for those.
