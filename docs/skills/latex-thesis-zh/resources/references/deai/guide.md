# Guide to writing Chinese degree thesis without AI


## Directory

- [Purpose](#目的)
- [Core Principles](#核心原则)
  - [1. Syntax fidelity first](#1-语法保真优先)
  - [2. Zero fabrication principle](#2-零捏造原则)
  - [3. Increase information density](#3-提高信息密度)
  - [4. Restraint in wording](#4-克制措辞)
- [Academic voice contract: protect the paper before reducing AI traces](#学术人味契约先保论文再降-ai-味)
- [Common AI trace patterns and elimination methods](#常见-ai-痕迹模式及消除方法)
  - [Category 1: empty words and slogans](#类别-1空话与口号)
  - [Category 2: Overdetermined](#类别-2过度确定)
  - [Category 3: Mechanical ratio](#类别-3机械排比)
  - [Category 4: Fuzzy Quantization](#类别-4模糊量化)
  - [Category 5: Template Quote](#类别-5模板引言)
- [Structural-level AI traces (depending on judgment, marked `[LLM]`)](#结构级-ai-痕迹靠判断标-llm)
- [Chapter Guidelines](#分章节准则)
  - [Abstract](#摘要)
  - [Introduction](#引言)
  - [Related work](#相关工作)
  - [Method](#方法)
  - [Experiment](#实验)
  - [Result](#结果)
  - [Discussion](#讨论)
  - [Conclusion](#结论)
- [De-AI editing output format](#去ai化编辑输出格式)
- [Type of change](#改动类型)
- [Test list (used with `deai_check.py --analyze`)](#检测清单配合-deai_checkpy---analyze-使用)
  - [High priority AI traces (must be fixed)](#高优先级-ai-痕迹必须修复)
  - [Medium priority AI traces (should be fixed)](#中优先级-ai-痕迹应当修复)
  - [Low priority AI traces (consider fixing)](#低优先级-ai-痕迹考虑修复)
- [AI trace density score of each chapter](#各章节-ai-痕迹密度评分)
- [Quick Reference: Common Substitutions](#快速参考常见替换)
- [Use together with references](#参考文献配合使用)
- [Tiering mode (--tier) and D1-D5 dimensions](#分级模式--tier与-d1-d5-维度)
- [AIGC Testing Policy of Colleges and Universities and Positioning of this Module (2025-2026)](#高校-aigc-检测政策与本模块定位2025-2026)

---

## Purpose

This guide helps reduce the artifacts of AI-generated text while maintaining technical accuracy and LaTeX syntactic integrity.

**Target Mode**: Mode T - Chinese first draft of PhD thesis (more complete explanation)

---

## Core Principles

### 1. Grammar fidelity first
- **Never modify**: LaTeX commands, environments, formulas, quotes, tags
- **Modify only**: ordinary paragraph text, chapter title, chart title text
- **KEEP**: All structural integrity to ensure compilability

### 2. Zero fabrication principle
- **Never add new**: data, indicators, comparison conclusions, experimental settings
- **Never add new**: new assertions, new contribution points, new references
- **IMPROVED ONLY**: Clarity of expression and natural flow

### 3. Increase information density
- Every sentence must convey verifiable information
- Delete empty words without substance
- Replace general statements with specific claims (if data is available)
- Mark unverifiable assertions as [to be supplemented]

### 4. Use restraint in words
- Avoid over-certainty that is not supported by evidence
- Use appropriate qualifications on speculative assertions
- State contributions objectively and do not exaggerate their value

---

## Academic Humanity Contract: Protect the paper first, then reduce the AI flavor

Reducing the AI flavor is not about making the paper smoother, nor is it about bypassing detection. The order of processing must be:

1. First protect the syntax anchors: `\cite{}`, `\ref{}`, `\label{}`, formulas, environments, macros and chapter structures are not rewritten by default.
2. Extract the academic load: facts/evidence, author’s claims, chapter logic, applicable boundaries and areas to be supplemented with evidence.
3. Finally delete the structural shells: binary contrast shells, pseudo-insight prompt words, colon handout cavity, empty reference and non-criterion comparison.

The default output is diagnostics, risk summaries, or rewrite blueprints. Only when the user explicitly requests to rewrite the text, give a partial prose proposal; write [to be supplemented] where new evidence is needed, and do not make up data, quotes or conclusions.

### Structural shell priority check

| Categories | Common Triggers | Academic Fix |
|------|----------|----------|
| Binary contrast shell | Not A, but B; not A, but B | If there is a substantial comparison, fill in the comparison axis, baseline and evidence; otherwise, directly state the judgment |
| Pseudo-insight mark | Real, actual, essential, core, this explanation | Delete the prompt word and directly write the claim supported by the evidence or [to be supplemented] |
| Colon lecture accent | My conclusion is:; The reason is very simple:; The key point is: | Change it into a common academic sentence, or use specific nouns to introduce a list |
| Empty reference | These things, this thing, a category, several directions | Replaced with accurate nouns such as research objects, methods, factors, results, limitations, etc. |
| Criteria-free comparison | More suitable, more similar, more natural, more advanced | Write down the comparison objects, task scenarios and evaluation criteria |
| Starting with an imperative | Don’t rush, stop first, don’t reverse the order | Change to academic risks, research steps or observation conclusions |

---

## Common AI trace patterns and elimination methods

### Category 1: empty words and slogans

| ❌ AI Traces | ✅ Anthropomorphism | Description |
|-----------|----------|------|
| Significant improvement | Reduced MAE by X% | Use specific numbers |
| Comprehensive system | Analyzed three aspects: X, Y, and Z | List specific contents |
| Effective solution | X% improvement compared to baseline | State comparison indicators |
| Significance | Make X task possible | Explain practical value |
| Good robustness | Accurate in noisy environments | Description conditions |
| Novel approach | Introducing Y based on X | Explain the innovation |

**Detection method**: Look for adjectives that can be replaced by specific claims.

### Category 2: Overdetermination

| ❌ Absolute | ✅ Qualified |
|-----------|----------|
|Obvious |Experimental results show |
| Without a doubt | It can be considered / inferred from this |
| Inevitable | Under the setting of this article, tend to |
| Completely | In most cases |
| Without exception | Within the scope of experimental observation |
| Always | Consistent under the experimental conditions of this article |
| Never | Rarely observed |

**Detection Method**: An absolute assertion without qualifications or evidence.

> A table of conservative wording substitutions for grades (causal/first of its kind/universal/effect size/application) is available at [`../writing/over-claim-guard.md`](../writing/over-claim-guard.md).

### Category 3: Mechanical ratio

**Three-paragraph juxtaposition without substance**:
❌ "This method is **fast**, **accurate**, and **efficient**."
✅ "This method has a processing speed of 1000 samples/second and an accuracy of 95%."

**Template transition**:
❌ "Deep learning has developed rapidly in recent years."
✅ "Since 2020, deep learning has made breakthrough progress on X tasks [1-3]."

**Universal beginning**:
❌ "With the rapid development of technology..."
✅ Start directly with the context of the specific problem.

**Sentence Parallel Detection (C2)**:
Three or more consecutive sentences use the same starting pattern (the first 2-4 words are the same), suggesting template generation.

❌ "This article proposes method A. This article designs module B. This article implements the C framework."
✅ "Method A aims to solve problem

**Detection method**: A phrase that can be applied to any paper in any field; 3 consecutive lines with the same beginning pattern.

### Category 4: Fuzzy quantization

| ❌ Vague | ✅ Specific |
|--------|--------|
| Numerous studies | Three recent studies [1-3] |
| Multiple experiments | Experiments on three data sets: X, Y, Z |
| Significant improvement | 12% increase |
| The vast majority | 78% of cases |
| Significantly better | Better than baseline at p<0.01 |

**Detection Method**: No actual numbers or quoted quantifiers.

### Category 5: Template Introduction

❌ "Time series forecasting is a topic with important application value."
✅ "Time series forecasting plays a key role in grid optimization [1], energy management [2], and financial planning [3]."

❌ "Machine learning technology has been widely used in many fields."
✅ "Machine learning has achieved remarkable results in medical diagnosis [1], industrial quality inspection [2], and financial risk control [3]."

**Detection Method**: A broad summary that can be used in any textbook.

### Category 5b: AI filler connectives (C1)

AI-generated text often uses specific filler connectives to start paragraphs or sentences, and these words appear less often or are used differently in human writing.

| ❌ AI filler words | ✅ Replacement suggestions |
|-------------|-----------|
| In short | Delete and state the conclusion directly |
| In summary | Delete or replace with specific logical derivation |
| It is undeniable | Delete, directly state the facts |
| It is worth noting | Delete and use the "noteworthy" content directly as the main clause |
| It should be pointed out that | delete and directly state the main points |
| Easy to find | Delete and let readers draw their own conclusions from the data |
| Well known | Delete or cite specific literature support |
| Needless to say | Delete and state your point of view directly |

**Detection method**: These words usually appear at the beginning of sentences and are high-frequency feature words in AI text. The sentence should still be complete after deletion.

### Category 6: Stacked parallel references

In the introduction/introduction and related work/literature review, simply listing multiple documents without analyzing them one by one is a typical trace of AI writing.

| ❌ Stacked Quotes | ✅ Analytical Quotes |
|------------|-------------|
| Many scholars have studied this [1], [2], [3], [4], [5]. | Smith et al. [1] proposed the X method, which achieved the Y effect in the A scenario. Jones [2] introduced the Z mechanism on this basis, but it is limited by B. Wang et al. [3] started from the C perspective and solved the D problem. |
| Research in recent years has made a series of progress [6]-[12]. | In recent years, Transformer-based methods [6, 7] have shown advantages in long sequence modeling, while CNN-based methods [8, 9] are more competitive in terms of computational efficiency. Hybrid architectures [10] try to take care of both, but still have shortcomings in noisy environments [11]. |

**Scope of application**: Introduction/Introduction + Related work/Literature review

**Rules:**
- No more than 2 parallel quotes may be used in the same sentence (unless it is a background statement of generally accepted facts)
- Each cited article is accompanied by at least one sentence describing its core contribution, methods or limitations.
- Prefer narrative citations ("Smith et al. [1] proposed...") over parentheses
- In the literature review, groups are divided into methods/paradigms, and specific technical differences are discussed article by article within the group.

**Detection method**: Look for 3 or more occurrences of `\cite{}` or `[X]` in the same sentence.

---

## Structure-level AI traces (depending on judgment, marked `[LLM]`)

Such traces are not in words or sentences, but in the document structure. The script cannot detect them and must be judged by reading the entire article; hits will be marked `[LLM]`.

1. **Excessive symmetry of IMRAD**: Each section is filled in the same shape (always 4 paragraphs for the introduction, always "review + comparison + significance + limitations" for the discussion). Real papers are uneven—some sections are short, some are long. Signal: The number of segments is highly symmetrical.
2. **Declarative transition preparation**: "After establishing X, we next move to Y." "With this, we continue...". The transition to real writing is implicit: the next sentence goes directly to the new topic without warning.
3. **Positionless discussion**: List the pros and cons, but don’t choose a side. Real authors will make their position clear ("We think X is more credible than Y because...").
4. **Uniform paragraph length**: 80% of paragraphs are 5-7 sentences. Real rhythm has its ups and downs—a 3-sentence emphasis paragraph right next to a 10-sentence argument paragraph.

**How to fix**: Break symmetry – merge thin paragraphs, split overloaded paragraphs, remove declarative transitions, make discussions clear.

---

## Chapter Guidelines

### Summary

**Structure**: Purpose → Methods → Key Results (with numbers) → Conclusion

**Common AI pitfalls**:
- ❌ "This paper proposes a novel time series forecasting method."
- ✅ "This article proposes a time series prediction method based on attention mechanism."

- ❌ "Experimental results show that this method achieves significant performance improvements."
- ✅ "On the X dataset, this method reduces MAE by 12% compared to the baseline."

- ❌ "This research has important theoretical significance and application value."
- ✅ "This method enables real-time predictions with latency below 10ms."

**Constraints**:
- Generic assertions without specific content ("novel", "significant", "important") are prohibited
- Key results must contain specific numbers
- State specific contributions, do not talk about value in general terms

**Example**:
```latex
% ❌ AI 痕迹
本文提出了一种新颖的深度学习方法用于时间序列预测。该方法
相比现有方法取得了显著的性能提升。实验结果证明了该方法的
有效性。

% ✅ 拟人化
本文提出了一种基于注意力机制的多变量时间序列预测方法。
相比 Transformer 基线 [1]，该方法在 UCR 数据集上将 MAE
降低了 12%。实验结果表明，注意力机制有效提升了长程依赖
捕获能力。
```

---

### Introduction

**Structure**: Importance → Blank → Contribution → Organizational Structure

**Common AI pitfalls**:
- ❌ "Time series forecasting plays an important role in modern society."
- ✅ "Time series forecasting is a key technology for power grid optimization [1] and supply chain management [2]."

- ❌ "However, existing methods have certain limitations."
- ✅ "However, existing methods cannot effectively capture long-range dependencies in noisy environments [2, 3]."

- ❌ "The main contributions of this article are as follows:"
- ✅ "This article has three contributions:"

**Contribution Statement Rules**:
- Every contribution must be verifiable
- Avoid "first", "leading" and "most advanced" without evidence support
- State what was done rather than emphasize how important it is

**Example**:
```latex
% ❌ AI 痕迹
时间序列预测非常重要。很多学者研究这个问题。但是现有方法
有一些不足。本文提出了一种新方法，取得了很好的效果。

% ✅ 拟人化
时间序列预测使能源管理 [1] 和供应链优化 [2] 能够实现主动
决策。近期基于 Transformer 的方法 [3, 4] 展现出潜力，但在
噪声环境下表现不佳 [5]。本文提出了一种噪声鲁棒注意力机制，
相比标准 Transformer 将预测误差降低了 12%。
```

---

### Related work

**Structure**: Classification → Comparison → Positioning

**Common AI pitfalls**:
- ❌ "Smith et al. proposed a method that works well."
- ✅ "Smith et al. [1] proposed the X method to achieve Y accuracy on the Z dataset."

- ❌ "Existing methods can be divided into two categories: statistical methods and deep learning methods."
- ✅ "Existing methods follow two paradigms: statistical methods [1-3] and deep learning methods [4-6]."

- ❌ "Our approach is different from their approach."
- ✅ "Unlike [1, 2], this method introduces an attention mechanism to..."

**Guidelines**:
- Group by method/paradigm rather than chronologically
- Compare specific technical differences
- Explain how this article is different
- Avoid vague praise ("excellent", "outstanding")
- No more than 2 parallel citations may be used in the same sentence, and each document must be analyzed in detail (see Category 6)

**Example**:
```latex
% ❌ AI 痕迹
很多人研究时间序列预测。有的用统计方法，有的用深度学习。
Smith 提出了一个很好的方法。Jones 也提出了一个方法。
我们的方法比他们的方法都好。

% ✅ 拟人化
时间序列预测方法分为两类：统计模型 [1-3] 和深度学习方法
[4-6]。Smith 等人 [1] 提出了 ARIMA，假设线性关系。近期
基于 Transformer 的方法 [4, 5] 捕获非线性模式，但需要大量
训练数据。与 [4, 5] 不同，本文方法采用混合架构，在数据
有限时仍保持准确率。
```

---

### Method

**Structure**: Overview → Detailed Design → Algorithm → Complexity

**Common AI pitfalls**:
- ❌ "We used a neural network. It's very powerful."
- ✅ "We used a 3-layer LSTM with 256 hidden units."

- ❌ "The algorithm converges quickly."
- ✅ "The algorithm converges within 100 iterations."

- ❌ "Model performance is very good."
- ✅ "Model processing speed is 1000 samples/second."

**Guidelines**:
- Provide implementation details to ensure reproducibility
- Explain hyperparameter and architecture choices
- Include algorithm complexity analysis where relevant
- Focus on what was done, not the effect (the effect is in the results chapter)

**Example**:
```latex
% ❌ AI 痕迹
我们使用了一个深度学习��型。模型有很多层，可以自动学习
特征。我们用梯度下降训练模型。

% ✅ 拟人化
我们使用了一个 4 层 Transformer，包含 8 个注意力头
（第 3.1 节）。模型使用 Adam 优化器训练，学习率为 0.001，
批大小为 32（第 3.2 节）。在单张 NVIDIA V100 GPU 上，
训练在 50 轮后收敛。
```

---

### Experiment

**Structure**: Experimental settings → Dataset → Evaluation indicators → Baseline method

**Common AI pitfalls**:
- ❌ "We conducted a lot of experiments."
- ✅ "We performed evaluation on 5 datasets from the UCR archive."

- ❌ "We compared it with many methods."
- ✅ "We compare with 4 baselines: ARIMA [1], LSTM [2], Transformer [3], Informer [4]."

- ❌ "The experimental setup is reasonable."
- ✅ "We use a 70%/15%/15% training/validation/test set split."

**Guidelines**:
- state what was actually done
- List specific data sets and baselines
- Describe evaluation indicators
- Avoid subjective evaluation ("reasonable", "comprehensive")

---

### Results

**Structure**: Main results → Ablation experiments → Analysis

**Common AI pitfalls**:
- ❌ "Our method is much better than the baseline method."
- ✅ "Compared to the best baseline, our method reduces MAE by 12%."

- ❌ "The results demonstrate the effectiveness of our approach."
- ✅ "Table 1 shows that our method achieves the lowest MAE on 4/5 data sets."

- ❌ "It can be seen from Figure 2 that our method is better."
- ✅ "Figure 2 shows that our method still maintains accuracy under 50% training data."

**Guidelines**:
- Report facts and figures only
- No explanation of why (that is the task of the discussion chapter)
- Avoid explanatory language ("better", "better than" but no numbers)
- Let the table/chart speak for itself

**Example**:
```latex
% ❌ AI 痕迹
实验结果如表 1 所示。我们的方法表现最好。基线方法的性能
不如我们的方法。从结果可以看出我们的方法非常有效。

% ✅ 拟人化
表 1 报告了所有方法在 5 个数据集上的 MAE。本文方法在 4 个
数据集（Electricity、Traffic、Solar、Exchange）上取得最低
MAE。相比最佳基线（Transformer），本文方法平均将 MAE
降低了 12%。
```

---

### Discussion

**Structure**: Interpretation of results → Mechanism analysis → Limitations → Future work

**Common AI pitfalls**:
- ❌ "The good performance proves that our method is excellent."
- ✅ "The improvement in accuracy shows that the attention mechanism effectively captures long-range dependencies."

- ❌ "There are no limitations to our approach."
- ✅ "The training time of this method is longer (2.3 hours vs. 1.5 hours of baseline)."

- ❌ "Future work includes more experiments."
- ✅ "Future work will explore the interpretability of attention mechanisms."

**Guidelines**:
- Explain the mechanism rather than restate the results
- Acknowledge failure and boundary conditions
- Be honest about limitations
- Propose specific future work

---

### Conclusion

**Structure**: Summary → Answering research questions → Future work

**Common AI pitfalls**:
- ❌ "This paper proposes a novel approach that achieves significant improvements."
- ✅ "This paper proposes an attention mechanism-based method that reduces MAE by 12%."

- ❌ "This research has important theoretical and practical value."
- ✅ "This research makes real-time prediction possible when computing resources are limited."

- ❌ "We will continue to improve our approach in the future."
- ✅ "Future work will extend this method to multivariate time series with missing values."

**Guidelines**:
- Direct answers to research questions
- No new results or assertions are introduced
- No new experiments proposed
- Specific, actionable future work

---

## De-AI editing output format

```latex
% ============================================================
% 去AI化编辑（第X行 - [章节名称]）
% ============================================================
% 原文：[AI 痕迹文本]
% 修改后：[拟人化文本]
%
% 改动说明：
% 1. [改动类型]：[具体说明]
% 2. [改动类型]：[具体说明]
%
% ⚠️ 【待补证：需要证据支撑的断言】
% ============================================================

[修改后的完整源码]
```

## Change type

1. **Delete empty words**: Delete vague adjectives/adverbs
2. **Add specific content**: Replace general expressions with specific content
3. **Split long sentences**: Split sentences longer than 50 words
4. **Adjust structure**: Improve logic fluency
5. **Downgrade wording**: Add appropriate qualifications
6. **Remove Redundancy**: Remove duplicate content
7. **Supplementary Subject**: Insert missing grammatical subject
8. **Replace Template**: Replace general expressions with specific content

---

## Test list (used with `deai_check.py --analyze`)

### High priority AI traces (must be fixed)
- [ ] Adjectives without specific information: significant, comprehensive, effective, important
- [ ] Absolute assertion: obvious, inevitable, complete, no doubt
- [ ] Fuzzy quantifiers: a large number, numerous, large, vast majority
- [ ] Templated expression: in recent years, more and more, it plays an important role
- [ ] Stacked parallel citations: 3 or more citations in the same sentence without article-by-article analysis (introduction + literature review)

### Medium priority AI traces (should be fixed)
- [ ] A three-paragraph juxtaposition without substance.
- [ ] can be used as a general opening for any paper
- [ ] Overconfident predictions or assertions
- [ ] Three-point list without specific content

### Low priority AI traces (consider fixing)
- [ ] repetitive sentence structure
- [ ] Overuse of conjunctions
- [ ] Passive voice (when active is clearer)

---

## AI trace density score for each chapter

After running `deai_check.py --analyze`, process according to the following priority:

| Score | Action |
|------|------|
| >70% | Urgent: Rewrite now |
| 50-70% | High: Rewrite as soon as possible |
| 30-50% | Medium: Review and revise |
| <30% | Low: Just light touch up |

---

## Quick Reference: Common Substitutions

| ❌ Delete | ✅ Replace with |
|--------|----------|
| Significant improvement | [Specific indicators + numbers] |
| Comprehensive Research | Analyzed X, Y, Z |
| Effective solution | X% improvement compared to baseline |
| Novel approach | Introducing Y based on X |
| Robust | Accurate under [conditions] |
|Obviously/obviously |experimental results show/results show|
| Numerous studies | [number] studies [citations] |
| In recent years | Since [year] / During [specific period] |
| more and more | gradually / growing from X to Y |
| plays an important role | makes... possible / is the key to... |

---

## Used in conjunction with references

This guide should be used in conjunction with the following documentation:
- [academic-style-zh.md](../writing/academic-style-zh.md): Chinese academic writing standards
- [forbidden-terms.md](forbidden-terms.md): List of protected terms
- [structure-guide.md](../writing/structure-guide.md): Dissertation structure requirements
- [gb-standard.md](../citations/gb-standard.md): GB/T 7714 format specification

---

## Grading mode (`--tier`) and D1-D5 dimensions

`--tier {light|medium|heavy}` is an **optional switch**. When not passed, the output is exactly the same as the original; when passed in:

- **Scale Thresholds**: `light` reports less (loosens the cap), `heavy` reports more (tightens the cap), `medium` keeps existing thresholds;
- **Enable D1 sentence length check**: break sentences according to Chinese punctuation, and mark chapters where the coefficient of variation of sentence length is too low (mechanically uniform);
- **Annotate AIGC dimensions for each conclusion** D1-D5 and attach a teaching note (why the detector marked this pattern).

```powershell
uv run python scripts/deai_check.py main.tex --analyze --tier heavy
```

The five dimensions are oriented towards readability and are **not targeted at any specific testing platform such as CNKI/VIP**: D1 sentence length change, D2 paragraph structure, D3 information density, D4 connective frequency, and D5 term-context matching. Thresholds (including `sentence_length.cv_threshold`) can still be overridden by `references/deai/tone-thresholds.yaml`.

---

## AIGC testing policy for universities and positioning of this module (2025-2026)

>Fact check date: 2026-06. The policy is updated frequently, please refer to the notice of the Graduate School of our school that year.

### Detection pattern: thresholds are concentrated at 15%-40%

Starting from the class of 2025, the CNKI AIGC detection channel has been popularized in domestic universities, and most schools use "AI-generated suspicion"
As a prerequisite for thesis submission/defense. Public cases (excerpts):

| School | Red Line | Remarks |
|------|------|------|
| Sichuan University | Liberal Arts ≤20% / Science, Engineering and Medicine ≤15% | Double thresholds by subject |
| Civil Aviation University of China | ≤30% | Over-limit return and modification |
| Ocean University of China | ≤40% | Exceeding the limit requires explanation or re-inspection |
| East China Normal University | ≤20% and AI usage needs to be marked | Threshold + statement dual requirements |

### Detection misjudgment is normal, do not take the detection score as the true value

- **Formula-heavy passages, quotations from laws or standards, and interview transcripts may be misclassified wholesale as AI-generated text**; many public examples document this failure mode.
- The detection results of the same paper on different platforms can fluctuate between **7%-70%**;
- Nanjing University and other universities have clearly stated that "the test results are only for supplementary reference and not the sole basis."

Therefore, **treat this module's output as readability advice, not as a guarantee of evading detection**.
The D1-D5 dimensions of the deai check are oriented toward "writing more like what a serious person writes". Reducing the risk of misjudgment is a side effect.
Not a promise - no tool is guaranteed to pass detection on a specific platform.

### `--tier` Suggestions corresponding to school-level red lines (only wording of guidance, no scaling logic changed)

- School red line **≤20%** (such as Sichuan University, East China Normal University): It is recommended to read the full text of `--tier heavy`,
  And manual review and misjudgment of formula/reference-intensive chapters;
- Red line **20%-40%**: Default or `--tier medium` is enough, giving priority to high-density chapters;
- The school has not set the line yet: there is no need to rewrite for detection, and it is recommended to choose based on readability.

### Policy Boundaries (consistent with Safety Boundaries)

The common tone of the policies of the Ministry of Education and various schools is **"assistance is allowed, ghostwriting is prohibited"**: AI assistance can be used
Polish the language, check the formatting, and don’t let AI ghostwrite the core academic content. This module only deals with language style
Review and do not provide any functions or suggestions to avoid detection; the research content, data and conclusions of the paper must
It is the author's own work, and the use of AI is truthfully stated in accordance with the requirements of the school.
