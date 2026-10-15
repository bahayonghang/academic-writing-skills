# Response Writing

This file specifies how to write the concern, the reply, and the modification location in the 「博士生修改说明」 (revision statement), the plain-text-equivalent Markdown rules for pasting, how to write declined concerns and future work, the tone, and the page number convention. It also gives three synthetic examples. For the workflow and the ledger fields, see [Response Workflow](rebuttal-workflow.md). For the check codes, see [Response Quality Gate](rebuttal-gate.md).

Sources of the rules: the requirements of Chinese universities for revision statements on thesis review comments (write the specific change, not only 「已修改」 (revised); reply to the comments of each expert separately), and the practice of thesis amendment forms outside China (give the modification location and the page number; the page number refers to the revised version).

## Document structure

`rebuttal_build.py` generates `responses/response-all.md` from the ledger:

```text
博士生修改说明

总体说明：感谢各位评阅专家对本论文的审阅与指导。2位评阅专家共提出5条意见，拆分为8项逐项处理，其中修改已有内容3项、补充新内容2项、在回复中说明1项、列为后续工作1项、未采纳1项。下文页码均指修改后论文。

一、评阅人1意见的修改说明

意见1：<评阅原文>

回复：<回复正文>

修改位置：<位置>

意见3：<评阅原文>

（1）回复：<子项 a 的回复>

（1）修改位置：<子项 a 的位置>

（2）回复：<子项 b 的回复>

（2）修改位置：<子项 b 的位置>

二、评阅人2意见的修改说明

…
```

- The script generates the general statement: it thanks the reviewers once and gives the total concern count, the item count after the split, and the count of each handling action. The replies to the concerns do not thank again.
- Each reviewer has one self-contained section. `response-R<n>.md` contains only the section of that reviewer. Its title line is 「评阅人N意见的修改说明」, and it has no general statement.
- One reply for each concern. When different reviewers raise the same problem, each reply is written in full, and the script adds 「（与评阅人1意见3（1）一并修改）」 (changed together with reviewer 1 concern 3 (1)) at the end of the reply.
- For an item whose `status` is not `done`, the reply and the modification location render as 「〔待填写〕」 (to be filled in). When the thesis did not change, the modification location renders as 「无（论文未修改）」 (none, the thesis did not change).
- `review-result.md` has only one line, `总体评价 1（A）；总体评价 2（B）`, for the pre-review result field of the form.

## Concern

- After 「意见N：」 comes the review text. The script takes the full item from `workspace/reviews/R<n>.md` and does not rewrite it.
- When the original text has more than 160 characters, write an excerpt of the start and the end in `quote_short` of the ledger, joined by 「……」. Each part must be a verbatim substring of the original text.

## Reply

1. The first sentence gives the handling action and the specific content: what changed, what was added, or why there is no change. Do not write only 「已修改」 or 「已按意见修改」 (revised as suggested).
2. Write enough that a reader can decide whether the reply answers the concern without opening the thesis: which symbols were added, which parts of the figure changed, which analysis the section added. Do not paste a full new paragraph into the reply.
3. Numbers come only from the revised thesis or the review text. A number with a decimal point or a percent sign in a reply must occur in the visible text of the thesis. Otherwise check reports R-NUM-SRC.
4. Use the completion words (已修改, 已补充, 已增加, 已删除, 已调整, 已完善, 已重绘, 已修正, 已更正, 已统一) only for items where the thesis really changed. `clarify` and `decline` do not use completion words.
5. The thesis already has the content (`clarify`): give the location and the main point of the original text, for example 「第3.2节第2段给出了该假设的适用条件」 (paragraph 2 of section 3.2 gives the conditions of the assumption).
6. A reply usually has 1–3 sentences. When there are many sub-points, split them into sub-items. Do not write a long paragraph.

### Declined concerns and future work

- `decline`: give an academic reason, for example the problem scope, the research assumptions, the usual practice of existing literature, or the conditions in which a metric applies. Do not give time, funding, or workload as the reason (check reports R-TONE).
- `partial`: first write the changed part, then the part that is not accepted and its reason.
- `future_work`: give the reason why the work cannot be completed before the defense (data conditions, platform conditions, a new experiment that is necessary), and say that it is listed as future work. A discussion can be added to the 「局限与展望」 (limitations and outlook) section of the thesis, and that section becomes the modification location. Do not write a planned experiment as complete, and do not predict experimental results.
- When more than one reviewer raises the same problem, the handling actions must agree. When one item changes the thesis and the other does not, check reports R-SHARED.

### Tone

- State the facts and the handling. Do not disparage the reviewer (do not write 「专家误解了」 (the expert misunderstood), 「显然」 (obviously), or 「众所周知」 (as is well known)).
- Do not start every reply with the same sentence (for example 「感谢专家的宝贵意见」, thanks for the valuable comment). When the same opening occurs 3 times or more, check reports R-TONE.
- No AI tone in Chinese: no signpost phrases such as 「值得注意的是」 or 「需要指出的是」; no 「首先……其次……最后……」 (first, second, finally) series; no elevating summary sentences; no 「不是 A，而是 B」 (not A but B) construction that sets up a claim only to reject it; no 「从而」 or 「进而」 as paragraph transitions.

## Modification location

- In `locations` of the ledger, prefer a LaTeX label or a bib key. The script uses the aux files of the revised thesis to render the current number and page.

| Location                                         | Rendered as                            |
| ------------------------------------------------ | -------------------------------------- |
| Label of a figure, table, equation, or algorithm | `图2-8（第28页）`, `式(2-1)（第14页）` |
| Number differs from the submitted version        | `原图2-1，现图2-2（第13页）`           |
| Chapter label                                    | `第6章`                                |
| Section label                                    | `第2.4节（第25页）`                    |
| Bib key                                          | `参考文献[24]`                         |
| File + section number (no label)                 | `第6.1节`                              |

- More than one location is separated by 「；」.
- Page number convention: the page numbers refer to the revised thesis. Run build after the last compile of the thesis, so that the page numbers agree with the version that goes to the university. When a tex file is newer than its aux file, check reports R-PAGE-STALE.
- When the reply text mentions a figure or table number, write the revised number. When the reply has only the original number, check reports R-RENUM.

## Plain-text-equivalent Markdown

For a file in responses, a copy of the raw file and a copy of the rendered Markdown view give the same text. Rules:

- Use only plain paragraphs, with one blank line between paragraphs.
- Do not start a line with `#`, `>`, `-`, `*`, `+`, `1.`, or `1)`. Write the numbers as 「意见1：」, 「（1）回复：」, and 「一、评阅人1意见的修改说明」.
- Do not use `**`, `__`, backticks, `[文字](链接)`, HTML tags, `|`, `$`, `\`, or `[^` inside a line.
- Do not leave two or more spaces at the end of a line.

The text in `response` of the ledger goes into responses unchanged, so `response` also obeys these rules. Write a formula as words or as its number in the thesis (「式(2-1)」), not as LaTeX source.

## Synthetic examples

The titles, numbers, pages, and content of these examples are invented.

### Example 1: change existing content (revise)

Ledger item:

```yaml
- id: R1-2
  reviewer: R1
  item: 2
  quote: 图3-4的坐标轴缺少单位，图例颜色与曲线不对应。
  category: figure
  severity: Minor
  priority: P2
  anchors:
    - text: 图3-4
      kind: figure
      label: fig:c3-error
      base_number: 3-4
      base_page: 46
  action: revise
  status: done
  owner: drawio
  plan: 重绘该图，补坐标轴单位，统一图例颜色。
  response: 已重绘该图，横轴标注时间单位分钟，纵轴标注流量单位辆每小时，图例颜色与对应曲线一致。
  locations:
    - label: fig:c3-error
  evidence:
    kind: git_diff
    files: [figures/chapter3/error.png]
    note: ""
```

Rendered result (the revised thesis has a new figure before this figure, so its number becomes 3-5):

```text
意见2：图3-4的坐标轴缺少单位，图例颜色与曲线不对应。

回复：已重绘该图，横轴标注时间单位分钟，纵轴标注流量单位辆每小时，图例颜色与对应曲线一致。

修改位置：原图3-4，现图3-5（第47页）
```

### Example 2: add new content (add)

Ledger item:

```yaml
- id: R2-1
  reviewer: R2
  item: 1
  quote: 第4章实验部分缺少与基线方法的显著性检验。
  category: experiment
  severity: Major
  priority: P1
  action: add
  status: done
  owner: latex-thesis-zh
  plan: 在第4.4节补充重复实验的配对检验，结果列表。
  response: 已在第4.4节补充5次重复实验的配对t检验，检验对象为本文方法与三种基线方法的误差，结果列于表4-6。
  locations:
    - label: sec:c4-4
    - label: tab:c4-ttest
  evidence:
    kind: git_diff
    files: [chapters/chapter4.tex]
    note: ""
```

Rendered result:

```text
意见1：第4章实验部分缺少与基线方法的显著性检验。

回复：已在第4.4节补充5次重复实验的配对t检验，检验对象为本文方法与三种基线方法的误差，结果列于表4-6。

修改位置：第4.4节（第68页）；表4-6（第69页）
```

### Example 3: list as future work (future_work)

Ledger item:

```yaml
- id: R2-3
  reviewer: R2
  item: 3
  quote: 建议在其他城市的数据集上验证方法的泛化能力。
  category: generalization
  severity: Major
  priority: P1
  action: future_work
  status: done
  owner: latex-thesis-zh
  plan: 在展望中补充跨城市验证的数据条件与实验设计，列为后续工作。
  response: 跨城市验证需要与本文数据相同采样间隔和检测器布设的数据，目前尚无满足该条件的公开数据集。本文在第6.2节展望中写出了跨城市验证所需的数据条件与实验设计，将其列为后续工作。
  locations:
    - label: sec:c6-2
  evidence:
    kind: git_diff
    files: [chapters/chapter6.tex]
    note: ""
```

Rendered result:

```text
意见3：建议在其他城市的数据集上验证方法的泛化能力。

回复：跨城市验证需要与本文数据相同采样间隔和检测器布设的数据，目前尚无满足该条件的公开数据集。本文在第6.2节展望中写出了跨城市验证所需的数据条件与实验设计，将其列为后续工作。

修改位置：第6.2节（第121页）
```

If the thesis did not add outlook text, `locations` is empty, `evidence.kind` is `none`, and the modification location renders as 「无（论文未修改）」.
