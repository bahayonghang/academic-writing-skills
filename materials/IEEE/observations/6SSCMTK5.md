---
key: 6SSCMTK5
title: "Dual Attention-Aided Cooperative Deep-Spatiotemporal-Feature-Extraction Network for Semi-Supervised Soft Sensing"
venue: "IEEE Robotics and Automation Letters"
doi: "10.1109/LRA.2024.3524901"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-7"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM STATEMENT` → `III. PROPOSED METHODOLOGY` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 semi-supervised soft sensors、RNN 动态建模与 spatiotemporal attention）。Introduction 末有节序路标，指向 Section II–V。Method 在正文中段。Experiments 标题为 `CASE STUDY`（debutanizer column process）。

## Openers

- abstract: `Soft sensing is` — "Soft sensing is a promising solution to predict key quality variables in various industries." (p.1)
- introduction: `IT IS essential` — "IT IS essential to perform real-time measurement of quality variables that are of key importance in industrial systems." (p.1；栏首掉字)
- method: `In this section` — "In this section, a dual attention-aided cooperative deep-spatiotemporal-feature-extraction network (DACDN) is presented in detail." (p.2, III)
- experiments: `In this section` — "In this section, our proposed DACDN is tested and evaluated via a real-life industrial process, i.e., a debutanizer column process (DCP)." (p.4, IV)
- conclusion: `In this work` — "In this work, we propose a deep learning-based soft sensing method, i.e., dual attention-aided cooperative deep-spatiotemporal-feature-extraction network (DACDN), to deal with unlabeled samples when performing the soft sensing of a dynamic industrial process." (p.6)

## Gap transitions

- however (introduction): "However, there exist two critical problems when developing a deep learning-based soft sensor." (p.1)
- however (introduction): "However, the traditional RNN is limited to mine long-distance dependencies, and ignores spatial dependence." (p.2)
- in this context (introduction): "In this context, spatial and temporal dependencies are considered as the interaction-influences among different variables at various time points." (p.2)
- in summary (method): "In summary, we propose DACDN, a deep neural network with efficient nonlinear and dynamic modeling abilities, devised specifically for soft sensing of industrial processes with unlabeled data." (p.4)
- therefore (experiments): "Therefore, in this work we set T = 25." (p.6)

## Hedge verbs

- propose / causal / abstract, introduction, method: "this work proposes a semi-supervised soft sensing method"; "We propose a dual attention-aided cooperative deep-spatiotemporal-feature-extraction network (DACDN)"; "we propose DACDN"
- demonstrate / causal / abstract: "The results demonstrate that our proposed model achieves state-of-the-art performance."
- show / causal / experiments: "Fig. 3 gives the epoch loss information, where DACDN can converge fast"; "This also verifies that DACDN is effective and accurate."
- indicate / causal / experiments: "The decreases of all indices indicate that the temporal self-attention mechanism can retain the temporal correlation"
- intend / speculative / conclusion: "Finally, we intend to introduce prior process knowledge into deep networks for facilitating the spatiotemporal learning."

## Cross-section linkers

- introduction → method: "The remaining sections are structured as follows. In Section II, a problem is stated. Then, DACDN-based soft sensor model is detailed in Section III. Our model is next evaluated via experiments described in Section IV. At last, conclusions are drawn in Section V." (p.2)
- method → experiments: "In summary, we propose DACDN..." 随后 `IV. CASE STUDY` (p.4)
- experiments → conclusion: 消融与 Wilcoxon 检验后直接 `V. CONCLUSION` (p.6)

## Candidate rules

- R001 abstract 贡献句用 `this work proposes` + 方法全称，不用 `Here we`。
- R002 Introduction 无独立 Related Work，半监督与 RNN 局限写在引言中段。
- R003 Introduction 末用 `The remaining sections are structured as follows` 指向 II–V。
- R004 贡献用 `This work aims to make the following two new contributions` + 编号列表。
- R005 Conclusion 先收回方法，再用 `three potential directions can be explored as our future work`。

## Candidate phrases

- `this work proposes a semi-supervised soft sensing method called` (abstract)
- `We propose a dual attention-aided cooperative deep-spatiotemporal-feature-extraction network (DACDN)` (introduction)
- `This work aims to make the following two new contributions:` (introduction)
- `The remaining sections are structured as follows.` (introduction)
- `In this work, we propose a deep learning-based soft sensing method` (conclusion)

## House style

自称是 `this work` / `We propose` / `our proposed model` / `our proposed DACDN`。未见 `Here we`。`this work proposes` 与 `In this work, we propose` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Soft sensing is a promising solution to predict key quality variables in various industries.
- p.1 abstract: To mitigate this issue, this work proposes a semi-supervised soft sensing method called dual attention-aided cooperative deep spatiotemporal-feature-extraction network.
- p.1 abstract: The results demonstrate that our proposed model achieves state-of-the-art performance.
- p.1 introduction: IT IS essential to perform real-time measurement of quality variables that are of key importance in industrial systems.
- p.1 introduction: We propose a dual attention-aided cooperative deep-spatiotemporal-feature-extraction network (DACDN) for soft sensing of dynamic processes with unlabeled data.
- p.1 introduction: However, there exist two critical problems when developing a deep learning-based soft sensor.
- p.2 introduction: However, the traditional RNN is limited to mine long-distance dependencies, and ignores spatial dependence.
- p.2 introduction: This work aims to make the following two new contributions:
- p.2 introduction: The remaining sections are structured as follows. In Section II, a problem is stated. Then, DACDN-based soft sensor model is detailed in Section III. Our model is next evaluated via experiments described in Section IV. At last, conclusions are drawn in Section V.
- p.2 method: In this section, a dual attention-aided cooperative deep-spatiotemporal-feature-extraction network (DACDN) is presented in detail.
- p.4 method: In summary, we propose DACDN, a deep neural network with efficient nonlinear and dynamic modeling abilities, devised specifically for soft sensing of industrial processes with unlabeled data.
- p.4 experiments: In this section, our proposed DACDN is tested and evaluated via a real-life industrial process, i.e., a debutanizer column process (DCP).
- p.5 experiments: These comparison results reveal a phenomenon, showing deep learning's stronger ability of mining sequential information for soft sensing than tradition machine learning.
- p.6 experiments: This also verifies that DACDN is effective and accurate.
- p.6 experiments: In summary, each component of DACDN is of great significance and contributes to the excellent soft sensing performance.
- p.6 conclusion: In this work, we propose a deep learning-based soft sensing method, i.e., dual attention-aided cooperative deep-spatiotemporal-feature-extraction network (DACDN), to deal with unlabeled samples when performing the soft sensing of a dynamic industrial process.
- p.7 conclusion: As compared to the state-of-the-art method, the proposed DACDN are more accurate and stable.
- p.7 conclusion: To further enhance the performance of DACDN, three potential directions can be explored as our future work.
