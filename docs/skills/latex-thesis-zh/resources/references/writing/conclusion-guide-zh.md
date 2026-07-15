# Guide to writing the conclusion chapter (summary and outlook)

Writing and diagnosis of the **conclusion chapter** for Chinese doctoral/master's thesis. The conclusion chapter here specifically refers to the end of the text and before the references.
An independent chapter, usually titled "Conclusion", "Conclusion and Outlook", "Summary and Outlook". Diagnostic entry:

```bash
uv run python $SKILL_DIR/scripts/analyze_conclusion.py main.tex
uv run python $SKILL_DIR/scripts/analyze_conclusion.py main.tex --json
```

> All the rules in this article are based on 5 industrial background doctoral theses (solid waste incineration, cement burning, cement clinker, cement grinding, zinc smelting and leaching)
> The conclusion chapter is read through **discipline practices** caliber one by one, 3/5 of the samples are from Yanshan University, with a focus on process industries, and the rule copy is rated "Best"
>Practice/suggestion" expression, **subject to the latest regulations of the instructor and the graduate school of our school**. Only the rules ≥4/5 are used as default alarms, and the rules 2~3/5 are used as default alarms.
> Rules are only available at Info/suggestion level.

## Overall structure template of conclusion chapter

It is recommended to use the **flat three-paragraph format** for the conclusion chapter (5/5 do not need subsection numbers, just use the opening paragraph + numbered contribution list + outlook list):

```text
① 开篇承上式总述：复述研究问题，用"首先……其次……最后……"串起全文研究链
② "……如下："导语 + 编号贡献条 (1)(2)(3)[(4)]（3~4 条）
③ 局限/承接过渡句（"仍存在一定不足""仍然有很多问题悬而未决"）
④ 展望 2~3 条：具体技术研究方向
```

| Block | Function | Length Reference |
| --- | --- | --- |
| Summary of the opening paragraph | Restate the question + research chain, leading to subsections | 1 paragraph |
| Numbered contribution bars | Reorganized by technical contribution/chapter (not repeated chapter by chapter), 3~4 bars | Main body, largest proportion |
| Continuing transitional sentences | Acknowledging limitations and linking to prospects | 1~2 sentences |
| Outlook | 2~3 specific technical directions | Summary: Outlook is about 2:1~3:1 |

The whole chapter is **2~4 pages**, accounting for about 1.5%~3.3% of the text. The summary should be longer than the outlook (5/5, about 2:1~3:1).

## Overview of the opening chapter (CC-OPEN)

The opening paragraph first retells the research question and the full-text research chain, uses prefaces to string the work of each chapter into a line, and then introduces the sub-sections. Preface
(First/Secondly/Then/Again/Finally) **At least 2** can reflect the research chain, otherwise only an Info prompt will be made.

Positive example sentence pattern (rewrite an excerpt from the model essay, do not copy it):

```text
本文针对〈对象〉在〈场景〉下的〈瓶颈〉问题，开展了〈研究主题〉研究。首先，……；其次，
……；最后，……。取得的主要创新性工作如下：
```

## Contribution bar skeleton (CC-SKELETON / CC-ENUM)

The contribution body is presented as a serialized list (1)(2)(3)[(4)], and the number of entries falls between **3~4** (exceeding only prompts). There must be one sentence before the list
"...as follows:" Introduction, the words of the introduction can be "main innovative work/specific innovative work/main conclusions/achieved results", etc.

Each contribution follows the skeleton "**Aiming at...problems, proposed/established/designed...methods/models, experiments/applications (results)
Shows/verifies...**". There are many variations of the skeleton sentence pattern, and the script only performs rough screening and counting, and the semantic completeness is submitted to [LLM] for review.

| Writing | Judgment |
| --- | --- |
| "(1) Aiming at the problem of high-dimensional data imbalance, a data enhancement model of monotonic bounded adversarial learning was established, and its consistency was verified using production data." | Passed (target-method-verification three elements are complete) |
| "(1) This article studies data enhancement." | Defects (no problem orientation, no verification carrier, CC-SKELETON [LLM] prompt completion) |
| Contribution prose in paragraphs, no (1)(2) number | Info (CC-ENUM prompt changed to numbered list) |

Contributions are organized by **technical contribution/chapter** (each = a method/model/chapter of work) and are not separately split according to summary points.

## Outlook Writing (CC-OUTLOOK-*)

The outlook must be **specific technical research directions**, and counterexamples are empty talk. The following is a blacklist of empty words (vocabulary is documented to maintain rhythm alignment
deai vocabulary convention, see script `OUTLOOK_EMPTY_PHRASES`):

- "Broad prospects" "Deserves further research" "Needs further study" "Further improve this method" "Continue in-depth research"

Judgment rules: Warning (CC-OUTLOOK-EMPTY) will be reported only if the blacklist is hit and **there is no specific technical term in the same sentence**; if empty words appear
At the end of the specific direction sentence (such as "The optimal scheduling of the amount of roasted sand added in... deserves further study"), since the same sentence contains technical terms, there is no false alarm.

Other outlook specifications (all Info level):

- **CC-OUTLOOK-TRANS**: There is a limitation/continuation transition sentence before the outlook ("There are still certain deficiencies", "There are still problems worth it"
  Delving further" "There are still many unanswered questions"). The most elegant one explicitly lists the scope of this article and then corresponds to the outlook one by one.
- **CC-OUTLOOK-COUNT**: The number of outlooks falls within **2~3** (only prompts if exceeded; segmented unnumbered outlooks are not mandatory).
- Outlook sentences are worded in the future direction ("Next step..." "The future can..." "Will be the next issue to consider").

Positive example (adapted from the sample article):

```text
然而，所提方法在更复杂工况下的泛化能力、工业现场可部署性仍存在一定不足。因此，未来
研究可从以下两方面深入：（1）物理与数据混合驱动的建模方法……；（2）面向 PLC/DCS 的
工程部署与在线适配……。
```

## Length ratio and structural style (CC-RATIO / CC-SUBSEC)

- **CC-RATIO** (Info): Summary: Prompt only if the outlook character ratio falls outside 1.5:1~4:1; the summary should be significantly longer than the outlook.
- **CC-SUBSEC** (Info): Whether to set the subsection number (X.1 Summary / X.2 Outlook) and whether the number is "Chapter X" are both
  **Style Selection** - Only 1/5 of the 5 articles have subsection numbers, and 3/5 have numbered chapters. Checker** only gives "with full text style" when detected
  "Be consistent" prompt, no right or wrong**, no requirement that the conclusion chapter must have subsections.

## Numerical consistency (CC-QUANT)

The conclusion is **not mandatory** (only 1/5 of the 5 articles restated the percentage intensively in the conclusion, and 4/5 kept the qualitative closing). But ** once
Restate the value and must be consistent with the main text/abstract**: The script extracts the percentage/decimal indicator tokens in the conclusion and places them one by one in the visible text of the main text.
Check the existence; if it cannot be found, a NEEDS-LLM soft prompt (not a hard report) will appear for manual review to see if it is a clerical error or caliber drift.

## Conclusion ≠ Abstract (CC-VERBATIM)

The opening summary and subsections should be a **paraphrase** of the abstract (sentence structure reorganization, supplementary connectives), and **the abstract must not be copied word for word**. script
Use difflib to compare the conclusion and the Chinese abstract sentence by sentence. If ratio ≥ 0.85, it will be reported as a hit; if the hit sentence accounts for ≥30% of the conclusion sentences, it will be reported as Warning.
Single sentence hit column Info details. Semantic-level synonym rewriting for [LLM] review.

## Three-stage complete (CC-TRIAD)

The conclusion must contain all three elements: **substantive summary + contribution statements + outlook**. The script uses keyword sets to locate the three blocks:

- Missing outlook or summary body → **Error** (structural lack);
- Lack of innovation/result statement introduction → **Warning**.

## Taboo list

| Taboo | Checkcode | Level | Description |
| --- | --- | --- | --- |
| Introducing a new chart environment (figure/table) | CC-NO-FIG | Error | The conclusion only restates the existing chart data in text, and does not create a new illustration table (5/5) |
| Introduce new concepts/new method names not seen in the main text | CC-NEW-CONCEPT | Warning ([LLM]) | The subdivision method names must be terms defined in each chapter of the main text |
| Introducing new documents (`\cite`) | Responsible for spec-check | — | The prohibition of citations in the conclusion is a hard format rule, and this script will not report it repeatedly |
| Copy summary verbatim | CC-VERBATIM | Warning | See previous section |
| Over-claim ("first time/complete solution/comprehensive transcendence") | See over-claim-guard.md | — | Contribution statements should be restrained and hedged; do not repeat the implementation in this script |

## Boundaries with other modules

The following checks in the conclusion chapter are **outside the scope** of this script and will be directed in the endnotes of the report:

- `\cite`, word limit (≤2000), vague wording (probably/maybe) → Go to `spec-check` module
  (`check_spec.py`, see [../modules/spec-check.md](../modules/spec-check.md));
- Overclaim → Follow the [over-claim-guard.md](over-claim-guard.md) process;
- English Abstract Tense/AI Accent → Go to `deai` module.

## Grading description

- Whether the conclusion is numbered as "Chapter X" (3/5), uses numbered subsections (1/5), or repeats numerical results (1/5) produces only an **Info-level reminder to stay consistent with the rest of the thesis; none is a hard rule** (Constraint 1: patterns found in only 2~3 of 5 references can support Info or recommendation level only).
- "This article/this paper" is a legal subject and is not included in the first-person forbidden words; only "I/we/the author" are spoken person issues.

## checker mapping table

Each specification ↔ corresponds to a check code (`[Script]` is script judgment, `[LLM]` is semantic-level manual review), and the last column points to research
The serial number traceability of `conclusion-patterns.md`:

| Checkcode | Lane | Trigger | Severity | Traceability |
| --- | --- | --- | --- | --- |
| CC-TRIAD | Script | Missing any element of summary/innovative expression/outlook | Error (lack of outlook/summary)/Warning (lack of innovative expression) | web C1/C5·HIT; C-LABEL |
| CC-OPEN | Script | First paragraph < 2 words | Info | C-OPENING 5/5 |
| CC-ENUM | Script | The contribution is not numbered or the number is not between 3~4 | Info | C-ENUM 5/5 |
| CC-SKELETON | LLM | Contribution bar lacks the element of "propose... to indicate that..." | Warning | C-SKELETON 5/5 |
| CC-OUTLOOK-EMPTY | Script | Outlook empty talk blacklist hit and no technical terms in the same sentence | Warning | C-OUTLOOK-SPEC 5/5; web C6 |
| CC-OUTLOOK-TRANS | Script | Looking ahead without limitations/taking over transitional sentences | Info | C-OUTLOOK-TRANS 5/5 |
| CC-OUTLOOK-COUNT | Script | The number of outlooks is not 2~3 | Info | C-OUTLOOK-COUNT 5/5 |
| CC-VERBATIM | Script + LLM | Verbatim copy summary of conclusion (ratio≥0.85, hit ratio≥30%) | Warning | C-NO-VERBATIM-ABS; web C4·HIT |
| CC-QUANT | Script | The conclusion value cannot be found in the text (NEEDS-LLM soft prompt) | Warning (inconsistent) | C-QUANT-CONSIST |
| CC-NO-FIG | Script | figure/table environment appears in the conclusion chapter | Error | C-NO-FIG 5/5 |
| CC-NEW-CONCEPT | LLM | A method name/concept not seen in the text appears in the conclusion | Warning | C-NO-NEW-CONCEPT 5/5 |
| CC-RATIO | Script | Summary: The expected character ratio is outside 1.5:1~4:1 | Info | C-RATIO 5/5 |
| CC-SUBSEC | Script | Subsection number or numbered chapter style detected | Info (not true or false) | C-SUBSEC 4/5 flat; C-NUM 3/5 |

## Output suggested format

```latex
% 结论章（chapters/conclusion.tex:42）[Severity: Warning] [Priority: P1]: [Script] CC-OUTLOOK-EMPTY 展望第 2 条"具有广阔的应用前景，值得进一步研究"为空话套话且无具体技术名词
% 建议：改为具体技术方向，如"下一步将研究多尺度不平衡数据增强与预测方法"。
```

---

## Further reading

- [thesis-writing-guide.md](thesis-writing-guide.md): The main line of the full text, abstract/innovation points/conclusion are closed in three directions.
- [abstract-structure.md](abstract-structure.md): Dissertation abstract skeleton (thesis model) - conclusion and abstract
  contribution correspondence.
- [method-chapter-guide-zh.md](method-chapter-guide-zh.md): Division of work between the summary of this chapter and the conclusion of the full text
  (Conclusion ≠ Simply repeat the summary of each chapter).
- [../modules/conclusion.md](../modules/conclusion.md): Detailed explanation of CC-\* check items and commands.
