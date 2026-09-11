---
key: RVAHJZPN
title: "A Deep Regression Framework Toward Laboratory Accuracy in the Shop Floor of Microelectronics"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2022.3182343"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字：`I. INTRODUCTION` → `II. RELATED WORK` → `III. PROPOSED METHODOLOGY` → `IV. EXPERIMENTAL EVALUATION` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。独立 Related Work（缺陷检测 DL + 软测量与 AI）。Introduction 末有节序路标，指向 Section II–V。Experiments 标题为 `EXPERIMENTAL EVALUATION`（PCB 点胶体积）。

## Openers

- abstract: `Deep learning DL` — "Deep learning (DL) has certainly improved industrial inspection, while significant progress has also been achieved in metrology with impressive results reached through their combination." (p.2652)
- introduction: `INDUSTRY 4.0 aims` — "INDUSTRY 4.0 aims to automate manufacturing processes using smart technologies and has greatly benefited from recent advancements in deep learning (DL)." (p.2652)
- related_work: `In this section` — "In this section, we give an overview of the most recent work related to our method." (p.2653)
- method: `In this section` — "In this section, the proposed methodology is outlined." (p.2653)
- experiments: `In this section` — "In this section, our proposed methodology is evaluated." (p.2657)
- conclusion: `In this article` — "In this article, we propose a methodology to replace expensive laboratory sensors with in situ ones, and demonstrate its potential by applying it for the development of a PCB inspection system that only relies on the use of an industrial camera and a Jetson unit." (p.2659)

## Gap transitions

- however (abstract): "However, it is not easy to deploy metrology sensors in a factory, as they are expensive, and require special acquisition conditions." (p.2652)
- however (introduction): "However, the large amounts of accurately annotated data needed to train DL models necessitate the deployment of multiple high-accuracy sensors for industrial process monitoring." (p.2652)
- despite (introduction): "Despite the promising results obtained, this method relies on the use of a laser profilometer, which is expensive, slow, needs to be calibrated, and requires controlled illumination conditions during measurements." (p.2652)
- hence (introduction): "Hence it is necessary to rely on less accurate, yet low-cost sensors." (p.2652)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "we propose a methodology to replace a high-end sensor"; "we propose to replace the laser profilometer"; "we propose a methodology to replace expensive laboratory sensors"
- demonstrate / causal / introduction, conclusion: "We demonstrate the potential of this approach"; "demonstrate its potential by applying it"
- show / causal / experiments: "Testing set predictions for all the developed models are shown in Fig. 14."
- observe / causal / experiments: "We observe that the deepest model trained consisting of 34 layers performs the worst"

## Cross-section linkers

- introduction → related_work: "The rest of this article is organized as follows. Section II reviews the related work in soft sensors (SS) and metrology methods for defect detection for industrial applications. Section III outlines the examined defect detection use case as well as the proposed methodology. ... In Section IV, our methodology is evaluated and the experimental results are presented. Finally, Section V concludes this article." (p.2653)
- related_work → method: 软测量综述后 `III. PROPOSED METHODOLOGY` (p.2653)
- method → experiments: 纠错网络后 `IV. EXPERIMENTAL EVALUATION` (p.2657)
- experiments → conclusion: 测试预测后 `V. CONCLUSION` (p.2659)

## Candidate rules

- R006 独立 Related Work。
- R009 摘要用 `In this article, we propose` 点名软测量方法。
- R004 贡献列表：`The main novelties of our work are summarized as follows.`
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–V。
- R005 Conclusion 先收回方法与结果，再用 `a potential extension is` / `Another interesting extension` 指向后续。

## Candidate phrases

- `In this article, we propose a methodology to replace` (abstract, conclusion)
- `The main novelties of our work are summarized as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `To further benchmark and evaluate the limitations of the proposed methodology, a potential extension is` (conclusion)

## House style

自称 `In this article, we propose` / `our work` / `our method` / `We propose`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.2652 abstract: Deep learning (DL) has certainly improved industrial inspection, while significant progress has also been achieved in metrology with impressive results reached through their combination.
- p.2652 abstract: However, it is not easy to deploy metrology sensors in a factory, as they are expensive, and require special acquisition conditions.
- p.2652 abstract: In this article, we propose a methodology to replace a high-end sensor with a low-cost one introducing a data-driven soft sensor (SS) model.
- p.2652 abstract: Our methodology is evaluated under operational conditions achieving promising results, whereas PCB inspection takes a fraction of the time needed by other methods.
- p.2652 introduction: INDUSTRY 4.0 aims to automate manufacturing processes using smart technologies and has greatly benefited from recent advancements in deep learning (DL).
- p.2652 introduction: However, the large amounts of accurately annotated data needed to train DL models necessitate the deployment of multiple high-accuracy sensors for industrial process monitoring.
- p.2652 introduction: Hence it is necessary to rely on less accurate, yet low-cost sensors.
- p.2652 introduction: Despite the promising results obtained, this method relies on the use of a laser profilometer, which is expensive, slow, needs to be calibrated, and requires controlled illumination conditions during measurements.
- p.2652 introduction: The main novelties of our work are summarized as follows.
- p.2653 introduction: The rest of this article is organized as follows. Section II reviews the related work in soft sensors (SS) and metrology methods for defect detection for industrial applications. Section III outlines the examined defect detection use case as well as the proposed methodology. A detailed description of the available data is given and the various deep architectures used are introduced. In Section IV, our methodology is evaluated and the experimental results are presented. Finally, Section V concludes this article.
- p.2653 related_work: In this section, we give an overview of the most recent work related to our method.
- p.2653 method: In this section, the proposed methodology is outlined.
- p.2657 experiments: In this section, our proposed methodology is evaluated.
- p.2658 experiments: Contrary to the usual case, where deeper architectures yield improved results, we observe the opposite, even though ResNets are known to tackle the degradation problem associated with increased depth.
- p.2659 conclusion: In this article, we propose a methodology to replace expensive laboratory sensors with in situ ones, and demonstrate its potential by applying it for the development of a PCB inspection system that only relies on the use of an industrial camera and a Jetson unit.
- p.2659 conclusion: Despite the challenging nature of the problem addressed, we obtained satisfactory results.
- p.2659 conclusion: To further benchmark and evaluate the limitations of the proposed methodology, a potential extension is its deployment in other industrial use cases, where we can explore how well it can generalize in terms of domain adaptation and inferring values outside the nominal ones used during training.
