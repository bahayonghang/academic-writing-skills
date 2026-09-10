# Example: Joint Mainline Logic and Experiment Review

User request:
First check whether the thesis mainline closes from the introduction through the conclusion, then determine whether the experiment chapters read more like a project report than a thesis discussion.

Recommended module order:
1. `logic`
2. `experiment`

Commands:
```bash
uv run python $SKILL_DIR/scripts/analyze_logic.py main.tex
uv run python $SKILL_DIR/scripts/analyze_experiment.py main.tex
```

Note: full-document mode in `analyze_logic.py` includes the introduction funnel, chapter mainline,
and C3 introduction-conclusion closure by default. Add `--section 绪论` to focus on one chapter
(both Chinese chapter names and English keys are accepted).

Expected output:
- First identify any misalignment among the introduction, contribution origins, and conclusion.
- Then identify missing comparison, mechanism explanation, limitation discussion, and future work in experiment chapters.
- Report the two issue classes through their respective modules instead of merging them into generic “expression optimization.”

## Review Existing Paragraphs with a Reverse Outline

This synthetic material demonstrates a manual reading, not a new script output format. When the user
requests a review, provide located diagnoses and a disposition blueprint without changing prose or
moving paragraphs automatically.

Chapter goal: Chapter 2 compares the input assumptions of temporal reconstruction methods and derives
the thesis problem. The current subsection is `2.1.2`.

```text
chapters/review.tex:18 [prev.tail]
下节比较上述方法对输入完整性的要求。

chapters/review.tex:24 [current]
现有时序重建方法对输入完整性的假设不同。固定采样方法要求等间隔观测，掩码建模方法显式接收缺失位置\cite{regular,masked,survey}。两类输入条件划定了本章比较的范围。

chapters/review.tex:29 [current]
方法B在数据集D上的准确率为95%，证明其在所有缺失条件下都能重建真实动态。

chapters/review.tex:33 [current]
本文界面提供深色配色和菜单折叠选项，见\ref{fig:ui}。

chapters/review.tex:38 [next.head]
本节据此分析不规则观测下的输入定义。
```

Extract the topic from each paragraph and check “paragraph topic -> chapter goal”; then check
“evidence -> paragraph topic” before choosing a disposition:

| Source location | Paragraph topic and chapter goal | Visible evidence and limits | Disposition and reason |
| --- | --- | --- | --- |
| `chapters/review.tex:24` | Input-completeness assumptions directly serve the comparison goal | The two assumptions form a comparison; retain the grouped citations, while checking specific attribution against the papers | Keep (Info/P3 [LLM]): the paragraph's relationships already hold without explicit transition words; do not add “therefore” or split the synthesis into a paper-by-paper list |
| `chapters/review.tex:29` | The performance observation does not yet explain differences in input assumptions | The 95% on dataset D supports only this observation, not all missingness conditions or the reconstruction mechanism | Narrow (Major/P1 [LLM]): retain the number and dataset scope; identify missing comparison-protocol and mechanism evidence without adding a conclusion |
| `chapters/review.tex:33` | No connection is established between interface preferences and the chapter's input-assumption goal | Only an interface description and figure reference are supplied | Propose moving (Minor/P2 [LLM]): first check whether an engineering chapter needs it; do not move it now or invent a connection |

Use [paragraph-arc](../references/writing/paragraph-arc-zh.md) `P-ARC` observations and
[subsection-context](../references/writing/subsection-context-zh.md) `S-CTX` windows for location when
useful; surface observations cannot replace semantic review. Propose a rewrite for `current` only when
the user explicitly requests it. `prev.tail`, `next.head`, and `parent_lead` serve only as evidence.
Preserve citations, labels, formulas, terms, numbers, certainty, and scope without adding causality,
experiments, or author intent. Moving material outside `current` needs authorization for that scope.
