---
key: C45RFS8R
title: "A Novel Accuracy-Constrained Scheme for Efficient Trend Extraction of Industrial Time-Series Data"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3554295"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PRELIMINARIES` → `III. TREND EXTRACTION AND SEGMENTATION WITH ACCURACY-CONSTRAINED POLYNOMIAL FIT` → `IV. CASE STUDIES ON INDUSTRIAL TIME-SERIES DATA` → `V. APPLICATION IN IDLE INDEX COMPUTATION` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 statistical methods / DP / AIC / SC / OP / low-pass filters）。Introduction 末有节序路标，指向 Section II–V 与 concluding remarks。Method 为 Section III。Experiments 为 IV–V（工业时序 + idle index）。

## Openers

- abstract: `Data trend extraction` — "Data trend extraction provides a useful means to qualitatively capture the underlying variations of time-series data." (p.1)
- introduction: `DUE to the` — "DUE to the rapid development of measurement and information technologies, industrial data mining has attracted immense interest from both academia and industries [1]." (p.1；栏首掉字)
- method: `To flexibly regulate` — "To flexibly regulate the complexity of piecewise polynomial fitting, we propose to use the fewest segments to fit the entire trajectory while attaining a prescribed approximation accuracy." (p.3, III.A)
- experiments: `In this study` — "In this study, we investigate the performance of the proposed trend extraction method on real-world data." (p.7, IV)
- conclusion: `In this work` — "In this work, we developed a novel accuracy-constrained formulation for data trend extraction and segmentation." (p.11)

## Gap transitions

- however (abstract): "However, it is not trivial to specify when tackling datasets of different sizes, and expensive computations are required in current global optimization algorithms." (p.1)
- to-address (abstract): "To address these issues, we propose a novel data trend extraction and segmentation method based on accuracy-constrained polynomial fitting." (p.1)
- unfortunately (introduction): "Unfortunately, these methods bear no tuning freedom in adjusting the tradeoff between fitting accuracy and model complexity." (p.1)
- to-overcome (introduction): "To overcome these limitations, we propose a novel global optimization-based trend extraction strategy based on accuracy-constrained polynomial fitting, which features both the ease of fine-tuning the accuracy-complexity tradeoff and lower computational costs." (p.2)
- however (experiments): "However, the performance of OP is much worse, and its best performance is attained by setting λ = 0.005." (p.8)

## Hedge verbs

- propose / causal / abstract, method: "we propose a novel data trend extraction"; "we propose to use the fewest segments"
- prove / causal / abstract, introduction: "we prove that the proposed solution algorithm has a desirable O(n^2) complexity"
- show / causal / abstract, conclusion: "Comprehensive case studies show"; "we showed that the trend extraction algorithm"
- develop / causal / conclusion: "we developed a novel accuracy-constrained formulation"
- illustrate / causal / introduction: "The outperformance, easy tuning of parameters, and low computational cost of our trend extraction method are empirically illustrated"

## Cross-section linkers

- introduction → method: "The remainder of this article is organized as follows. In Section II, the basics of data segmentation and polynomial fitting are revisited. In Section III, we introduce the efficient segmentation and trend extraction method. Sections IV and V are devoted to the presentation of case studies, followed by final concluding remarks." (p.2)
- method → experiments: "This completes the proof." 随后 `IV. CASE STUDIES ON INDUSTRIAL TIME-SERIES DATA` (p.7)
- experiments → conclusion: idle-index 段落后直接 `VI. CONCLUSION` (p.11)

## Candidate rules

- R001 abstract 缺口用 `However` + `To address these issues, we propose`。
- R002 Introduction 无独立 Related Work，方法评述写在引言中段。
- R003 Introduction 末用 `The remainder of this article is organized as follows` 指向 II–V。
- R004 Conclusion 用 `In this work, we developed` 收回方法，再对比 DP 复杂度。
- R005 复杂度主张用 `we prove that` + big-O，不把证明句写成 anti-AI。

## Candidate phrases

- `To address these issues, we propose` (abstract)
- `To overcome these limitations, we propose` (introduction)
- `The remainder of this article is organized as follows.` (introduction)
- `In this study, we investigate the performance of` (experiments)
- `In this work, we developed` (conclusion)

## House style

自称是 `we propose` / `we developed` / `our approach` / `this article` / `In this work` / `In this study`。未见 `Here we`。`we propose` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Data trend extraction provides a useful means to qualitatively capture the underlying variations of time-series data.
- p.1 abstract: However, it is not trivial to specify when tackling datasets of different sizes, and expensive computations are required in current global optimization algorithms.
- p.1 abstract: To address these issues, we propose a novel data trend extraction and segmentation method based on accuracy-constrained polynomial fitting.
- p.1 abstract: In particular, we prove that the proposed solution algorithm has a desirable O(n^2) complexity that does not grow with the number of segments and is much lower than that of generic global optimization algorithms.
- p.1 abstract: Comprehensive case studies show that compared with conventional methods, our approach enjoys better empirical performance, easier tuning of parameters, and lower computational cost.
- p.1 introduction: DUE to the rapid development of measurement and information technologies, industrial data mining has attracted immense interest from both academia and industries [1].
- p.1 introduction: Unfortunately, these methods bear no tuning freedom in adjusting the tradeoff between fitting accuracy and model complexity.
- p.2 introduction: To overcome these limitations, we propose a novel global optimization-based trend extraction strategy based on accuracy-constrained polynomial fitting, which features both the ease of fine-tuning the accuracy-complexity tradeoff and lower computational costs.
- p.2 introduction: The remainder of this article is organized as follows. In Section II, the basics of data segmentation and polynomial fitting are revisited. In Section III, we introduce the efficient segmentation and trend extraction method. Sections IV and V are devoted to the presentation of case studies, followed by final concluding remarks.
- p.3 method: To flexibly regulate the complexity of piecewise polynomial fitting, we propose to use the fewest segments to fit the entire trajectory while attaining a prescribed approximation accuracy.
- p.7 experiments: In this study, we investigate the performance of the proposed trend extraction method on real-world data.
- p.8 experiments: However, the performance of OP is much worse, and its best performance is attained by setting λ = 0.005.
- p.11 conclusion: In this work, we developed a novel accuracy-constrained formulation for data trend extraction and segmentation.
- p.11 conclusion: Importantly, we proved that the worst case computational complexity of our solution algorithm is only O(n^2), which is much lower than the O(M_max n^2) complexity of classic DP procedure.
- p.11 conclusion: Through case studies, we showed that the trend extraction algorithm not only well captures the underlying variations of data, but also features an easier parameter tuning and reduced computational burden as compared to known algorithms.
