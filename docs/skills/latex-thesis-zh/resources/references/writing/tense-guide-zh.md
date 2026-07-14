# Tense Guide (English Abstract)

The **body of a Chinese degree thesis is written in Chinese, which has no tense**, so this guide and
its script check apply only to the **English abstract (Abstract)**. The English abstract should follow
English-paper tense conventions. The goal is not to use past tense everywhere; each part has its own
convention. The most common error is writing the method/results narrative in present tense.

The script (`deai_check.py`) runs **only in the English abstract region**: generic
`\begin{abstract}`, thuthesis `\begin{abstract*}`, and pkuthss `\begin{eabstract}`. It skips Chinese
abstract environments (explicit thuthesis `\begin{abstract}` and pkuthss `\begin{cabstract}`) and
emits a `[Script]` LOW trace for present-tense **reporting verbs** there. If it cannot locate an English
abstract, it performs no check.

## Tense in the English Abstract

| Part | Default Tense | Example |
|---|---|---|
| Background | Present | “Long-context inference *is* expensive ...” |
| Methods | Past | “We *trained* ... / Models *were evaluated* on ...” |
| Results | Past | “The model *achieved* 92.3% / We *observed* ...” |
| Conclusion | Present | “These results *provide* a basis for ...” |

> Body chapters (introduction/methods/experiments/conclusion) are written in Chinese and follow Chinese
> writing conventions, outside the tense script's scope. If the degree thesis requires English chapters,
> apply English-paper tense conventions: methods/results strictly in past tense, figure/table descriptions in present tense.

## Signal Words (Scan Method/Result Sentences in the English Abstract)

The most common error is using a present-tense reporting verb where past tense is required:

- `shows / reveals / demonstrates / indicates / presents / confirms / achieves / outperforms`
  in a method/result narrative -> normally change to `showed / revealed / demonstrated / …`. The script flags these forms.

### `is` / `are` - Manual Judgment (Not Flagged by the Script)

Present-tense `is` / `are` in English-abstract methods/results is **often** a tense error, but too many
legitimate uses exist for automatic flagging. Retain present tense in these cases:

- **Definition**: “Let *G* be ... / The loss *is defined as* ...”;
- **General fact**: “Cross-entropy *is* convex ...”;
- **Description of a figure/table**: “Table 2 *is* organized by ...”;
- **Software capability**: “The toolkit *supports* ...”.

Otherwise prefer past tense: “The threshold *was set* to 0.5” rather than *is* set.

## Exceptions Skipped by the Script (Present Tense Is Correct)

1. **Figure/table/equation as subject**: “Figure 3 *shows* ...”, “as *shown* in Fig. 4”, “Table 1 *lists* ...”.
2. **Software/tool capability**: “The library *provides* ...”.
3. A **definition or general fact** embedded in a methods paragraph.

Treat matches in these cases as false positives and retain the wording.

## Boundary with Other Guides

- This guide covers **tense**. For claim strength (causal/first/universal), see [over-claim-guard.md](over-claim-guard.md).
- For Chinese academic style, see [academic-style-zh.md](academic-style-zh.md).

## Script Support

`deai_check.py` (`ChineseAITraceChecker`) emits `[Script]` LOW traces for present-tense reporting verbs
only in the English abstract region (configured in `references/deai/tone-thresholds.yaml` under the
`tense:` section, controlled by `enabled`). The script filters figure/table and
software false positives but does not judge `is` / `are`; apply the checklist above manually.
