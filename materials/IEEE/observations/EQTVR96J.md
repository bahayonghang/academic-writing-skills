---
key: EQTVR96J
title: "Multisource Ensemble Network-Based Learning for Knowledge-Informed FeO Prediction in Sintering"
venue: "IEEE Transactions on Instrumentation and Measurement"
doi: "10.1109/TIM.2025.3579835"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. KIMEN SCHEME AND PROBLEM FORMULATION` → `III. KNOWLEDGE SOLIDIFICATION METHOD` → `IV.`（knowledge-informed image feature extraction，页眉未单列完整标题）→ `V. PROPOSED ENSEMBLE RECURRENT NETWORK` → `VI. EXPERIMENTS AND EVALUATION` → `VII. CONCLUSION AND FUTURE WORK`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 DBN、multisource images、small-sample generation、infrared fusion）。Introduction 末有 threefold 贡献与节序路标。Method 为 II–V。Experiments 为 Section VI。

## Openers

- abstract: `Lack of crucial` — "Lack of crucial state data is a common problem in processing industries, particularly in iron-making." (p.1)
- introduction: `INDUSTRIAL artificial intelligence` — "INDUSTRIAL artificial intelligence (IAI) systematically integrates academic research on artificial intelligence with industrial applications to provide reliable and sustainable solutions [1]." (p.1；栏首掉字)
- method: `Aiming to address` — "Aiming to address the challenges of small-sample training and multisource information fusion, the KIMEN model was proposed." (p.5, V)
- experiments: `Domain knowledge can` — "Domain knowledge can help in better understanding the physical significance of parameters and their relationship to system properties and can aid in prediction." (p.6, VI.A)
- conclusion: `In this article` — "In this article, to solidify and quantify the domain knowhow, an s-PCS strategy was proposed." (p.9)

## Gap transitions

- however (abstract): "In practice, technical experts rely on manual observations to make estimates; however, this knowledge is difficult to formalize and quantify." (p.1)
- nevertheless (introduction): "Nevertheless, solely relying on process parameters may miss important visual cues related to material properties." (p.1)
- however (introduction): "However, extracting image features using deep learning networks often demands large datasets, which poses challenges in industrial applications with limited labeled samples." (p.1)
- however (introduction): "However, the retirement of senior experts can significantly affect production stability, as their domain expertise is critical for maintaining consistent operations." (p.2)
- however (introduction): "However, the high cost of infrared equipment and the heterogeneity of data pose significant challenges for the fusion process." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction: "a novel knowledge-informed method ... (KIMEN) is proposed"; "we proposed a two-layer cascaded structure"
- introduce / causal / abstract: "a sParts-Pair comparing sorting (s-PCS) strategy was introduced"
- demonstrate / causal / abstract, conclusion: "the method demonstrates improved prediction performance"; "the method demonstrates practical effectiveness"
- show / causal / abstract: "Experimental results show that the proposed KIMEN outperforms"
- validate / causal / abstract: "Ablation studies, small-scale experiments, and transfer learning experiments further validate the advantages of our method."

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. Section II describes the KIMEN scheme and problem formulation. The proposed knowledge consolidation method is introduced in Section III. For a knowledge-informed image feature extraction method, it is presented in Section IV. Section V provides an introduction of the proposed ensemble recurrent network. In Section VI, the experiments settings and evaluation are presented. Section VII is the conclusion and future work." (p.2)
- method → experiments: GRU 公式段落后接 `VI. EXPERIMENTS AND EVALUATION` (p.6)
- experiments → conclusion: DEP 段落后接 `VII. CONCLUSION AND FUTURE WORK` (p.9)

## Candidate rules

- R001 abstract 用被动 `is proposed` + `we proposed` 混用。
- R002 Introduction 无独立 Related Work；贡献用 `The contributions of the proposed ... are threefold as follows`。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VII。
- R004 Conclusion 标题为 `CONCLUSION AND FUTURE WORK`，末句 `Future work will focus on`。
- R005 工业落地段写训练时间与 DEP 指标，属 experiments 而非 anti-AI。

## Candidate phrases

- `In this article, a novel knowledge-informed method ... is proposed` (abstract)
- `To address this, we proposed` (introduction)
- `The contributions of the proposed ... are threefold as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `Future work will focus on` (conclusion)

## House style

自称是 `In this article` / `we proposed` / `the proposed KIMEN` / `our method`。未见 `Here we`。`In this article` 与 `we proposed` 进 phrase_bank，不进 anti_ai_patterns。未见 `In this paper`。

## Quotes

- p.1 abstract: Lack of crucial state data is a common problem in processing industries, particularly in iron-making.
- p.1 abstract: In practice, technical experts rely on manual observations to make estimates; however, this knowledge is difficult to formalize and quantify.
- p.1 abstract: In this article, a novel knowledge-informed method that integrates a multisource fusion model with an ensemble network (KIMEN) is proposed to predict a key chemical indicator in the industry, the FeO content.
- p.1 abstract: Experimental results show that the proposed KIMEN outperforms some conventional methods and state-of-the-art approaches.
- p.1 introduction: INDUSTRIAL artificial intelligence (IAI) systematically integrates academic research on artificial intelligence with industrial applications to provide reliable and sustainable solutions [1].
- p.1 introduction: Nevertheless, solely relying on process parameters may miss important visual cues related to material properties.
- p.2 introduction: However, the high cost of infrared equipment and the heterogeneity of data pose significant challenges for the fusion process.
- p.2 introduction: To address this, we proposed a knowledge-informed image processing method using cost-effective visible light images.
- p.2 introduction: The contributions of the proposed knowledge-informed and multisource ensemble network (KIMEN) are threefold as follows.
- p.2 introduction: The rest of this article is organized as follows. Section II describes the KIMEN scheme and problem formulation.
- p.5 method: Aiming to address the challenges of small-sample training and multisource information fusion, the KIMEN model was proposed.
- p.6 experiments: Domain knowledge can help in better understanding the physical significance of parameters and their relationship to system properties and can aid in prediction.
- p.8 experiments: Even on a smaller database, the proposed method can still maintain a certain level of performance.
- p.9 conclusion: In this article, to solidify and quantify the domain knowhow, an s-PCS strategy was proposed.
- p.9 conclusion: When applied to Guangxi Liuzhou Iron & Steel (Group) Company, the method demonstrates practical effectiveness in real-world applications.
- p.9 conclusion: Future work will focus on further enhancing robustness in the rare cases involving anomalies, as the current design primarily addresses normal operating conditions.
