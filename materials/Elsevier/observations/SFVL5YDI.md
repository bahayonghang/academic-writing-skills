---
key: SFVL5YDI
title: "Energy consumption prediction in cement calcination process: A method of deep belief network with sliding window"
venue: "Energy"
doi: "10.1016/j.energy.2020.118256"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-12"
date_observed: 2026-09-11
story_pattern: SP-ELS-001
---

## Structure

数字节：`1. Introduction` → `2. Relevant work` → `3. Cement calcination process and variable selection` → `4. Prediction scheme of cement multi-index energy consumption based on SW-DBN` → `5.` 实验（含 `5.3. Experimental setup`、`5.4. Experimental results`）→ `6. Conclusion`。前置 `abstract` 与 `Keywords`。独立 Related Work（`2. Relevant work`，时滞、非线性、DBN 电力预测）。Introduction 末有编号贡献 `(1)`/`(2)` + 节序路标。Method 标题为 `4. Prediction scheme ... based on SW-DBN`（sliding window、DBN）。Experiments 对比 DBN/SVM/SW-SVM，电耗与煤耗双指标。

## Openers

- abstract: `Electricity consumption and` — "Electricity consumption and coal consumption are two important indicators in the cement calcination process."
- introduction: `Cement industry is` — "Cement industry is dependent on electricity and fossil fuels which has the characteristic of high energy consumption [1]."
- method: `As mentioned in` — "As mentioned in Section 3, the data of energy consumption are highly correlated with the data of eight relevant variables."
- experiments: `In order to` — "In order to verify the superiority of SW-DBN model, we employ DBN, SVM and SW-SVM as contrastive methods."
- conclusion: `In this paper` — "In this paper, a novel prediction model for cement energy consumption was proposed."

## Gap transitions

- however (abstract): "However, due to the three characteristics of cement: time-varying delay, non-linearity and uncertainty, it is very difficult to establish accurate energy consumption prediction models."
- besides (introduction): "Besides, it takes about 50–60 minutes for the raw materials to be completely calcined into clinker, so there are delay times between raw materials feeding volume data and corresponding energy consumption data."
- thus (introduction): "Thus, this method cannot get the best result in the field of cement calcining."
- consequently (introduction): "Consequently, we proposed a multiple-index energy consumption forecasting model based on sliding window deep belief network."
- as far as (introduction): "As far as we know, most studies have only predicted one of them [8,9]."

## Hedge verbs

- proposed / causal / abstract, introduction, conclusion: "a multiple-index energy consumption prediction model based on sliding window deep belief network (SW-DBN) is proposed"; "we proposed a multiple-index energy consumption forecasting model"; "a novel prediction model for cement energy consumption was proposed"
- show / associative / abstract: "Experimental results show that the proposed model obtains improvement for multiple-index energy consumption prediction model in cement calcination process."
- employ / causal / experiments: "we employ DBN, SVM and SW-SVM as contrastive methods"
- outperforms / causal / experiments, conclusion: "SW-DBN outperforms all of the other compared methods"; "SW-DBN outperforms them in term of four evaluation errors"
- suggest / speculative / conclusion: "Therefore, we suggest that the idea of combination of sliding window and DBN can be used in not only cement calcination process but also other process industries"

## Cross-section linkers

- introduction → related work: "The rest of the paper is structured as follows. Relevant works are discussed in Section 2. The cement calcination process and variable selection are presented in Section 3. The algorithm and frame of the proposed model is introduced in Section 4. The experimental results compared with traditional model are reported and discussed in Section 5. The conclusions about this paper are summarized in Section 6."
- related work → method: process 节后 `4. Prediction scheme of cement multi-index energy consumption based on SW-DBN`
- method → experiments: DBN 算法后进入实验设置与 `5.4. Experimental results`
- experiments → conclusion: 双指标对比后 `6. Conclusion`

## Candidate rules

- R001 独立 Related Work：`2. Relevant work`。
- R003 节序路标：`The rest of the paper is structured as follows`
- R004 编号贡献：`The main advantages of this model are summarized as follows.`
- R009 自称：`In this paper` / `we proposed`

## Candidate phrases

- `a multiple-index energy consumption prediction model based on sliding window deep belief network (SW-DBN) is proposed in this paper` (abstract)
- `Consequently, we proposed a multiple-index energy consumption forecasting model` (introduction)
- `The rest of the paper is structured as follows` (introduction)
- `In this paper, a novel prediction model for cement energy consumption was proposed` (conclusion)
- `Therefore, we suggest that the idea of combination of sliding window and DBN can be used` (conclusion)

## House style

自称 `this paper` / `we proposed` / `In this paper` / `we suggest`。第一人称复数与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Electricity consumption and coal consumption are two important indicators in the cement calcination process.
- abstract: However, due to the three characteristics of cement: time-varying delay, non-linearity and uncertainty, it is very difficult to establish accurate energy consumption prediction models.
- abstract: To solve the above problems, a multiple-index energy consumption prediction model based on sliding window deep belief network (SW-DBN) is proposed in this paper.
- introduction: Cement industry is dependent on electricity and fossil fuels which has the characteristic of high energy consumption [1].
- introduction: Consequently, we proposed a multiple-index energy consumption forecasting model based on sliding window deep belief network.
- introduction: The rest of the paper is structured as follows. Relevant works are discussed in Section 2.
- related-work: As mentioned in section 1, there are three main characteristics in calcination process: time-varying delay, non-linearity and uncertainty.
- method: As mentioned in Section 3, the data of energy consumption are highly correlated with the data of eight relevant variables.
- experiments: In order to verify the superiority of SW-DBN model, we employ DBN, SVM and SW-SVM as contrastive methods.
- experiments: As shown in Table 2, SW-DBN outperforms all of the other compared methods in term of power consumption forecasting.
- conclusion: In this paper, a novel prediction model for cement energy consumption was proposed.
- conclusion: Compared with DBN, SVM and SW-SVM, SW-DBN outperforms them in term of four evaluation errors for electricity and coal consumption.
