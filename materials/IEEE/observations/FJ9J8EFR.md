---
key: FJ9J8EFR
title: "Adaptive Data-Driven Soft Sensor for Monitoring and Prediction of Temperature Inside Zinc Rotary Kiln"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2025.3550793"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-19"
date_observed: 2026-09-11
story_pattern: SP-IEEE-001
---

## Structure

罗马数字标题：`I. Introduction` → `II. RELATED WORK` → `III. METHODOLOGY` → `IV. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。有独立 Related Work。`related_work=independent`。Introduction 路标写 `Section 2 reviews related work, Section 3 describes the temperature prediction method, and Section 4 concludes the paper`，未单列 Experiments 主节；案例、对比与 SHAP 写在 III 内。作者稿页码为 `VOL. XX`。

## Openers

- abstract: `Accurate temperature monitoring` — "Accurate temperature monitoring and prediction are crucial for maintaining product quality control in zinc rotary kilns." (p.1)
- introduction: `IN recent years,` — "IN recent years, with the continuous innovations in industrialization, temperature monitoring in critical areas has become essential in industries such as metallurgy and chemical engineering, particularly in high-temperature smelting processes, including zinc rotary kilns [1]." (p.1；栏首掉字)
- related_work: `With the development` — "With the development of industrial automation, traditional sensor methods based on physical modeling can no longer meet the requirements of modern complex industrial processes in terms of real-time performance, accuracy, and stability." (p.3, II)
- method: `In recent years,` — "In recent years, numerous adaptive soft-sensor methods have been proposed to address the dynamic monitoring demands in industrial processes, particularly in tasks such as temperature prediction and quality monitoring." (p.8, III)
- experiments: `To accurately predict` — "To accurately predict the tail-end temperature in the zinc rotary kiln, the following process was outlined in this study:" (p.8, III 内实验流程)
- conclusion: `In this study,` — "In this study, an adaptive data-driven soft-sensor is proposed for monitoring and predicting the internal temperature of a zinc rotary kiln." (p.17)

## Gap transitions

- however (abstract): "However, achieving precise temperature prediction and real-time monitoring under dynamic working conditions remains a pressing challenge." (p.1)
- however (introduction): "However, traditional temperature sensors are prone to unreliability in extreme environments, making it difficult to achieve the desired accuracy and stability and directly obtain internal temperature data." (p.1)
- thus (introduction): "Thus, it is now a well-recognized alternative to use soft-sensors to estimate difficult-to-measure key variables [4]." (p.1)
- therefore (introduction): "Therefore, it is of great importance for system operation and maintenance to extract informatic features and predict the internal temperature of zinc rotary kilns in a multidimensional, nonlinear, and time-varying environment." (p.1)
- however (related work): "However, the traditional PLS method is based on linear assumptions, which limits its effectiveness when dealing with highly nonlinear or complex dynamic processes." (p.3)
- although (related work): "Although NPLS has advantages in handling nonlinear problems, its training process is more cumbersome." (p.3)

## Hedge verbs

- proposes / causal / abstract: "This paper proposes a methodology to integrate the moving window (MW) technique and just-in-time (JIT) learning mechanism"
- is demonstrated / causal / abstract: "The feasibility of enhancing simple linear models with adaptive mechanisms for soft-sensors is demonstrated through validation using benchmark simulation data"
- reveal / causal / abstract: "Experimental findings reveal that the Moving Window Partial Least Squares (MW-PLS) mechanism reduces the root mean square error (RMSE)"
- demonstrates / causal / related work, conclusion: "the adaptive data-driven soft measurement method proposed in this paper demonstrates superior performance"
- is proposed / causal / conclusion: "an adaptive data-driven soft-sensor is proposed"

## Cross-section linkers

- introduction → related work: "The paper is structured as follows: Section 2 reviews related work, Section 3 describes the temperature prediction method, and Section 4 concludes the paper." (p.3)
- related work → method: PLS 改进评述后直接 `III. METHODOLOGY` (p.8)
- method → experiments: 实验流程嵌在 III.A 之后，无独立 Experiments 主节。(p.8)
- experiments → conclusion: Table VI 对比后直接 `IV. CONCLUSION` (p.17)

## Candidate rules

- R001 摘要缺口用 `However, achieving ... remains a pressing challenge.`，再用 `This paper proposes a methodology to integrate`。
- R002 Introduction 末用 `The main contributions of this paper are shown as follows:` + 编号列表。
- R003 路标把实验并入 Section 3，Conclusion 为 Section 4；与多数 IEEE 四节（含独立 Experiments）不同。
- R004 Related Work 用 DPLS/NPLS/APLSE 对比后收回 `the adaptive data-driven soft measurement method proposed in this paper`。

## Candidate phrases

- `This paper proposes a methodology to integrate` (abstract)
- `The main contributions of this paper are shown as follows:` (introduction)
- `The paper is structured as follows:` (introduction)
- `the adaptive data-driven soft measurement method proposed in this paper` (related work)
- `In this study, an adaptive data-driven soft-sensor is proposed` (conclusion)

## House style

自称是 `This paper` / `this paper` / `In this study` / `this study`。摘要用 `This paper proposes`。`This paper proposes` 进 phrase_bank，不进 anti_ai_patterns。未见 `Here we`。

## Quotes

- p.1 abstract: Accurate temperature monitoring and prediction are crucial for maintaining product quality control in zinc rotary kilns.
- p.1 abstract: However, achieving precise temperature prediction and real-time monitoring under dynamic working conditions remains a pressing challenge.
- p.1 abstract: This paper proposes a methodology to integrate the moving window (MW) technique and just-in-time (JIT) learning mechanism into the partial least squares (PLS) regression algorithm to construct two types of adaptive soft-sensors for quality variable predictions.
- p.1 abstract: Experimental findings reveal that the Moving Window Partial Least Squares (MW-PLS) mechanism reduces the root mean square error (RMSE) in temperature prediction by approximately 15.3% and the mean absolute error (MAE) by 12.5%.
- p.1 introduction: IN recent years, with the continuous innovations in industrialization, temperature monitoring in critical areas has become essential in industries such as metallurgy and chemical engineering, particularly in high-temperature smelting processes, including zinc rotary kilns [1].
- p.1 introduction: However, traditional temperature sensors are prone to unreliability in extreme environments, making it difficult to achieve the desired accuracy and stability and directly obtain internal temperature data.
- p.1 introduction: Therefore, it is of great importance for system operation and maintenance to extract informatic features and predict the internal temperature of zinc rotary kilns in a multidimensional, nonlinear, and time-varying environment.
- p.3 introduction: The main contributions of this paper are shown as follows:
- p.3 introduction: The paper is structured as follows: Section 2 reviews related work, Section 3 describes the temperature prediction method, and Section 4 concludes the paper.
- p.3 related_work: With the development of industrial automation, traditional sensor methods based on physical modeling can no longer meet the requirements of modern complex industrial processes in terms of real-time performance, accuracy, and stability.
- p.3 related_work: However, the traditional PLS method is based on linear assumptions, which limits its effectiveness when dealing with highly nonlinear or complex dynamic processes.
- p.3 related_work: Compared to existing soft measurement methods based on PLS, the adaptive data-driven soft measurement method proposed in this paper demonstrates superior performance in handling dynamic, nonlinear, and high-dimensional data.
- p.8 method: In recent years, numerous adaptive soft-sensor methods have been proposed to address the dynamic monitoring demands in industrial processes, particularly in tasks such as temperature prediction and quality monitoring.
- p.8 experiments: To accurately predict the tail-end temperature in the zinc rotary kiln, the following process was outlined in this study:
- p.17 experiments: These results indicate that the proposed adaptive soft-sensor method possesses high accuracy and real-time capability for dynamic temperature monitoring, effectively addressing the challenges of temperature prediction in industrial processes.
- p.17 conclusion: In this study, an adaptive data-driven soft-sensor is proposed for monitoring and predicting the internal temperature of a zinc rotary kiln.
