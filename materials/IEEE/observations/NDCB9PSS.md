---
key: NDCB9PSS
title: "A Domain-Knowledge Embedded Framework for Soft Sensing in Complex Industrial Processes With Cascading Equipment"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3507937"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. SOFT-SENSOR MODELING BASED ON OSA-DCCLSTM` → `III. INDUSTRIAL APPLICATION: ALUMINA EVAPORATION PROCESS` → `IV. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 评 LSTM、STALSTM/VALSTM、自注意力、级联设备相关工作）。无 `The rest of this article is organized as follows`。Method 紧接引言。Experiments 标题为工业应用案例。

## Openers

- abstract: `Traditional industrial production` — "Traditional industrial production processes, such as nonferrous metallurgy, are mostly based on complex, cascading, large-scale equipment." (p.1)
- introduction: `AS ADVANCED control` — "AS ADVANCED control systems are developed and applied in modern industry, the overall level of automation in industrial processes has significantly increased." (p.1；栏首掉字)
- method: `In the industrial` — "In the industrial processes based on cascading equipment, the time delays for the influence of process variables on quality variable, it is necessary to first obtain the time-delay range of the process variables affecting the quality variables for each equipment." (p.2–3, II.A)
- experiments: `In this section,` — "In this section, the proposed soft-sensor framework is evaluated by an alumina evaporation process, and we conducted ablation tests and comparative tests to demonstrate the effectiveness of the proposed framework." (p.6, III)
- conclusion: `In this article,` — "In this article, we proposed an effective feature extraction and soft-sensor framework called OSA-DCCLSTM to solve the problems in the application of soft sensor in the industrial process with cascading equipment." (p.9)

## Gap transitions

- to alleviate (abstract): "To alleviate this problem, this article first proposes a time-delay analysis strategy to preliminarily reduce the input dimensions of the process variables." (p.1)
- however (introduction): "However, due to the complexity of the physical and chemical mechanisms in the vast majority of industrial processes, as well as the pronounced characteristics of high temperature and high pressure, the real-time monitoring of quality variables within the running duration is hindered [1], [2], [3]." (p.1)
- despite (introduction): "Despite their successes, most attention mechanisms currently applied to industrial soft sensors are static, failing to adapt to the complex data dynamics." (p.2)
- although (introduction): "Although the above methods attempted to model the cascading characteristics of complex processes, they struggle to describe the dynamic time-delay windows of variables in a more refined manner due to two reasons." (p.2)
- although (conclusion): "Although OSA-DCCLSTM achieves notable performance on soft sensor in industrial processes with cascading equipment, there are still some limitations." (p.9)

## Hedge verbs

- propose / causal / abstract, introduction, conclusion: "this article first proposes a time-delay analysis strategy"; "this article proposes a new soft-sensor framework"; "we proposed an effective feature extraction and soft-sensor framework"
- show / causal / abstract: "Extensive experiments on a real-world alumina evaporation process datasets show the effectiveness of the proposed framework."
- demonstrate / causal / experiments, conclusion: "we conducted ablation tests and comparative tests to demonstrate the effectiveness"; "demonstrating that OSA-DCCLSTM outperforms state-of-the-art models"

## Cross-section linkers

- introduction → method: 贡献列表后直接 `II. SOFT-SENSOR MODELING BASED ON OSA-DCCLSTM`，无节序路标 (p.2)
- method → experiments: DCCLSTM 结构段落后直接 `III. INDUSTRIAL APPLICATION: ALUMINA EVAPORATION PROCESS` (p.6)
- experiments → conclusion: 相对误差分析后直接 `IV. CONCLUSION` (p.9)

## Candidate rules

- R001 abstract 用 `this article first proposes` 分步交代模块，不用 `Here we`。
- R002 Introduction 无独立 Related Work；方法节标题直接点名框架缩写。
- R003 贡献用 `The main contributions are as follows.` + 编号列表。
- R004 Experiments 标题写成工业过程应用，不用独立 Discussion。
- R005 Conclusion 用 `In this article, we proposed`，再用 `Although` 承认局限，`in our future work, we will` 指向后续。

## Candidate phrases

- `To alleviate this problem, this article first proposes` (abstract)
- `The main contributions are as follows.` (introduction)
- `In this section, the proposed soft-sensor framework is evaluated by` (experiments)
- `In this article, we proposed an effective feature extraction and soft-sensor framework called` (conclusion)
- `in our future work, we will focus on` (conclusion)

## House style

自称是 `this article` / `we proposed` / `our proposed method` / `the proposed framework`。未见 `Here we`。未见 `In this paper`。`this article first proposes` 与 `In this article, we proposed` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Traditional industrial production processes, such as nonferrous metallurgy, are mostly based on complex, cascading, large-scale equipment.
- p.1 abstract: To alleviate this problem, this article first proposes a time-delay analysis strategy to preliminarily reduce the input dimensions of the process variables.
- p.1 abstract: Extensive experiments on a real-world alumina evaporation process datasets show the effectiveness of the proposed framework.
- p.1 introduction: AS ADVANCED control systems are developed and applied in modern industry, the overall level of automation in industrial processes has significantly increased.
- p.2 introduction: Despite their successes, most attention mechanisms currently applied to industrial soft sensors are static, failing to adapt to the complex data dynamics.
- p.2 introduction: Although the above methods attempted to model the cascading characteristics of complex processes, they struggle to describe the dynamic time-delay windows of variables in a more refined manner due to two reasons.
- p.2 introduction: The main contributions are as follows.
- p.2–3 method: In the industrial processes based on cascading equipment, the time delays for the influence of process variables on quality variable, it is necessary to first obtain the time-delay range of the process variables affecting the quality variables for each equipment.
- p.6 experiments: In this section, the proposed soft-sensor framework is evaluated by an alumina evaporation process, and we conducted ablation tests and comparative tests to demonstrate the effectiveness of the proposed framework.
- p.8 experiments: Compared with all above models, our proposed method obtained lower RMSE and MAE and higher R2, indicating that the proposed framework outperforms state-of-the-art methods in the field.
- p.9 conclusion: In this article, we proposed an effective feature extraction and soft-sensor framework called OSA-DCCLSTM to solve the problems in the application of soft sensor in the industrial process with cascading equipment.
- p.9 conclusion: Although OSA-DCCLSTM achieves notable performance on soft sensor in industrial processes with cascading equipment, there are still some limitations.
- p.9 conclusion: Taking this factor into account, in our future work, we will focus on enhancing the robustness of the model to mitigate the adverse effects of common sensor failures in industrial processes.
