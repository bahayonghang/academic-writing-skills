---
key: FJAEEZSN
title: "Attentive Continuous-Time Generative Adversarial Networks for Irregular Time Series Imputation"
venue: "IEEE Transactions on Knowledge and Data Engineering"
doi: "10.1109/TKDE.2025.3617659"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,12-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. RELATED WORK` → `III. BACKGROUND AND NOTATIONS` → `IV. METHOD` → `V. EXPRIMENTS` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work（II，含 A. GAN-Based Time Series Imputation Methods / B. Continuous-Time Flow in Time Series Modeling）。`related_work=independent`。Introduction 末有 `Outlines.` 路标，指向 Section II–VI。Method 在 IV。Experiments 标题 PDF 作 `V. EXPRIMENTS`（拼写）。III 为 Background and Notations。

## Openers

- abstract: `Time series are` — "Time series are widely used in many classification and regression tasks." (p.6973)
- introduction: `TIME series imputation` — "TIME series imputation is a fundamental task in time series analysis [1]." (p.6973；栏首掉字)
- related_work: `In this section` — "In this section, we present the related works regarding GAN-based time series imputation and continuous-time flow in time series modeling." (p.6974, II)
- method: `The overall structure` — "The overall structure of ACGANet, as illustrated in Fig. 2, can be divided into two parts including the joint-learning generator (J-generator) and the discriminator." (p.6976, IV.A)
- experiments: `In this section` — "In this section, we demonstrate the imputation effectiveness of the proposed ACGANet via comparisons with nine alternative methods." (p.6978, V)
- conclusion: `We propose an` — "We propose an end-to-end attentive continuous-time generative adversarial network, called ACGANet, for imputing incomplete time series." (p.6984)

## Gap transitions

- however (abstract): "However, numerous time series contain unavoidable missing data, making it challenging to model the temporal dynamics of sequential data." (p.6973)
- although (abstract): "Although sequences recorded at fixed time intervals are presented in discrete form, they possess an inherent temporal continuity, which is ignored in most existing approaches." (p.6973)
- although (introduction): "Although various deep learning-based methods have been proposed for time series imputation, most existing approaches assume that data are recorded at fixed intervals and ignore the inherent continuity of time." (p.6974)
- although (introduction): "Although NCDE and their variants have demonstrated strong performance on irregular time series, they focus primarily on temporal dynamics and often fail to capture the complex interdependencies among multiple variables." (p.6974)
- to tackle (introduction): "To tackle these issues, we propose an end-to-end Attentive Continuous-Time Generative Adversarial Network (ACGANet) to impute missing data in irregular time series." (p.6974)
- however (related work): "However, time series are typically recorded in a discrete form, and most GAN-based imputation methods overlook the inherent continuity between elements within the sequence" (p.6975)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "In this paper, we propose an end-to-end Attentive Continuous-Time Generative Adversarial Network (ACGANet)"; "We propose an end-to-end attentive continuous-time generative adversarial network, called ACGANet"
- demonstrate / causal / abstract, experiments: "Extensive experiments on three publicly available real-world datasets demonstrate that ACGANet achieves state-of-the-art performance"; "we demonstrate the imputation effectiveness"
- may / speculative / introduction, related work: "making it difficult to capture fine-grained evolution patterns"; "which may fail to capture finer-grained information"
- can (ability) / causal / related work: "NODE can be formulated as"; "the continuous nature of NCDE enables it to capture fine-grained temporal dynamics"
- will (future) / speculative / conclusion: "We will further investigate and address these problems in future work"

## Cross-section linkers

- introduction → related work / background / method / experiments / conclusion: "Outlines. The rest of this paper is organized as follows. Section II summarizes the related works. In Section III, we provide the background of time series imputation. Section IV gives an overview of the proposed ACGANet. Section V presents the experimental results and analysis, and we conclude with potential future extensions in Section VI." (p.6974)
- related work → background: NCDE 公式后直接 `III. BACKGROUND AND NOTATIONS` (p.6975)
- background → method: 符号表后直接 `IV. METHOD` (p.6976)
- method → experiments: Algorithm 1 / complexity 后直接 `V. EXPRIMENTS` (p.6978)
- experiments → conclusion: Memory and Computational Efficiency 后直接 `VI. CONCLUSION` (p.6984)

## Candidate rules

- R001 abstract 用 `Although ... which is ignored` 把离散采样与连续时间对立，再用 `In this paper, we propose`。
- R002 Introduction 贡献前加独立小标题 `Contributions:` 与 `Outlines.`，路标句以 `Outlines.` 起头。
- R003 Related Work 分 GAN 插补与连续时间流两支，每支末句用 `However` 收口。
- R004 Experiments 节标题 PDF 为 `EXPRIMENTS`（拼写），开篇用 `In this section, we demonstrate`。
- R005 Conclusion 先 `We propose` 收回方法，再用 `There are still many challenging issues to address in the future`。

## Candidate phrases

- `In this paper, we propose an end-to-end` (abstract)
- `To tackle these issues, we propose` (introduction)
- `Contributions: In sum, our contributions can be summarized as follows.` (introduction)
- `The rest of this paper is organized as follows.` (introduction)
- `We propose an end-to-end` (conclusion)
- `There are still many challenging issues to address in the future` (conclusion)

## House style

自称是 `In this paper, we propose` / `we propose` / `the proposed model` / `ACGANet`。未见 `Here we`。`In this paper, we propose` 进 phrase_bank，不进 anti_ai_patterns。结论开篇用 `We propose`。

## Quotes

- p.6973 abstract: Time series are widely used in many classification and regression tasks.
- p.6973 abstract: However, numerous time series contain unavoidable missing data, making it challenging to model the temporal dynamics of sequential data.
- p.6973 abstract: Although sequences recorded at fixed time intervals are presented in discrete form, they possess an inherent temporal continuity, which is ignored in most existing approaches.
- p.6973 abstract: In this paper, we propose an end-to-end Attentive Continuous-Time Generative Adversarial Network (ACGANet) to estimate unobserved values in irregular sequences.
- p.6973 abstract: Extensive experiments on three publicly available real-world datasets demonstrate that ACGANet achieves state-of-the-art performance in imputing incomplete time series.
- p.6973 introduction: TIME series imputation is a fundamental task in time series analysis [1].
- p.6974 introduction: Although various deep learning-based methods have been proposed for time series imputation, most existing approaches assume that data are recorded at fixed intervals and ignore the inherent continuity of time.
- p.6974 introduction: To tackle these issues, we propose an end-to-end Attentive Continuous-Time Generative Adversarial Network (ACGANet) to impute missing data in irregular time series.
- p.6974 introduction: Outlines. The rest of this paper is organized as follows. Section II summarizes the related works. In Section III, we provide the background of time series imputation. Section IV gives an overview of the proposed ACGANet. Section V presents the experimental results and analysis, and we conclude with potential future extensions in Section VI.
- p.6976 method: The overall structure of ACGANet, as illustrated in Fig. 2, can be divided into two parts including the joint-learning generator (J-generator) and the discriminator.
- p.6978 experiments: In this section, we demonstrate the imputation effectiveness of the proposed ACGANet via comparisons with nine alternative methods.
- p.6984 conclusion: We propose an end-to-end attentive continuous-time generative adversarial network, called ACGANet, for imputing incomplete time series.
- p.6984 conclusion: Experimental results on several publicly available real-world datasets demonstrate that the proposed model outperforms existing imputation methods in inferring missing data in incomplete time series.
- p.6984 conclusion: There are still many challenging issues to address in the future, such as the large number of hyper-parameters, relatively low computational efficiency and the need for robust error control when constructing continuous paths via interpolation.
- p.6984 conclusion: We will further investigate and address these problems in future work, as they are crucial for enhancing the performance of ACGANet.
