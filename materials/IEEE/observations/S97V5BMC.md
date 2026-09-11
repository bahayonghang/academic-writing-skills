---
key: S97V5BMC
title: "Causal Disentangled Graph Neural Network for Fault Diagnosis of Complex Industrial Process"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3452246"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. PROBLEM FORMULATION AND PRELIMINARIES` → `III. PROPOSED FAULT DIAGNOSIS METHOD` → `IV. CASE STUDY` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 GNN 故障诊断与因果子图；II.C 再评图像因果方法 CAL/CCN）。Introduction 末有节序路标，指向 II–V。II 为问题形式化 + GNN/因果预备，不是综述节。Experiments 标题为 `CASE STUDY`。

## Openers

- abstract: `Graph neural networks` — "Graph neural networks (GNNs) are good at capturing the intricate topologies and dependencies among components and are outstanding in fault diagnosis tasks of complex industrial process." (p.386)
- introduction: `FAULT diagnosis is` — "FAULT diagnosis is one of the key techniques for prognostics and health management, serving a vital function in guaranteeing the secure and efficient operation of complex systems as well as reducing maintenance costs [1]." (p.386；栏首掉字)
- method: `In this section` — "In this section, we analyze causal relationships in the fault diagnosis according to causal theory and develop a structural causal model (SCM)." (p.388, III)
- experiments: `This section presents` — "This section presents an evaluation of the effectiveness of CDGNN in addressing fault diagnosis in complex industrial process." (p.391)
- conclusion: `In this study` — "In this study, we excavated the causal relationships inherent to GNN-based fault diagnosis according to the causal theory and introduced the novel CDGNN." (p.395)

Preliminaries 首句："In industrial systems, numerous sensors are used for system monitoring and process management, these sensor signals form n raw measured variables." (p.387, II.A)。不单列 `related_work` opener。

## Gap transitions

- however (abstract): "However, spurious correlations in the bias substructures will mislead predictions." (p.386)
- to address (abstract): "To address this issue, this study takes the disentanglement of causal and bias substructures as the key to improve model stability." (p.386)
- however (introduction): "However, it can only analyze the correlation of data and is susceptible to noise and irrelevant data." (p.386)
- however (introduction): "However, the bias substructure is independent of fault, which will result in large prediction biases." (p.387)
- based on (introduction): "Based on the above analysis, a causal disentangled GNN (CDGNN) framework for fault diagnosis in complex industrial process is proposed." (p.387)
- to address (preliminaries): "To address this challenge, Li et al. [15] proposed a causal consistency network (CCN) for mining constant causal data in individualized equipment." (p.388)

## Hedge verbs

- propose / causal / abstract, introduction, method: "A causal disentangled GNN (CDGNN) is proposed"; "a causal disentangled GNN (CDGNN) framework ... is proposed"; "CDGNN is proposed"
- indicate / associative / abstract, conclusion: "Experimental results on two complex industrial datasets indicate that CDGNN is an effective and stable method"; "Experimental results on the TFF and NPS datasets indicated that"
- demonstrate / causal / experiments: "CDGNN demonstrates commendable performance across various faults"

## Cross-section linkers

- introduction → preliminaries: "The rest of this article is organized as follows. Problem formulation and preliminaries are presented in Section II. Section III details the proposed CDGNN. In Section IV, we conducted case studies on two complex industrial datasets. Finally, Section V concludes this article." (p.387)
- method → experiments: 总损失与 Algorithm 1 后直接 `IV. CASE STUDY` (p.391)
- experiments → conclusion: 计算代价段落后直接 `V. CONCLUSION` (p.395)

## Candidate rules

- R001 摘要用 `A causal disentangled GNN (CDGNN) is proposed` / `this study takes`。
- R002 Related Work 并入 Introduction；II 是 PROBLEM FORMULATION AND PRELIMINARIES。
- R003 Introduction 末 `The rest of this article is organized as follows`。
- R004 贡献用 `The main contributions are as follows.` + 编号列表。
- R005 结论承认闭环假设，用 `Further research will focus on` 指向开集。

## Candidate phrases

- `To address this issue, this study takes` (abstract)
- `Based on the above analysis, a ... framework ... is proposed.` (introduction)
- `The main contributions are as follows.` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In this study, we excavated` (conclusion)
- `Further research will focus on` (conclusion)

## House style

自称 `this study` / `we` / `CDGNN is proposed` / `this investigation`。未见 `Here we`、`In this paper`。`this study` 与 `this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.386 abstract: Graph neural networks (GNNs) are good at capturing the intricate topologies and dependencies among components and are outstanding in fault diagnosis tasks of complex industrial process.
- p.386 abstract: However, spurious correlations in the bias substructures will mislead predictions.
- p.386 abstract: To address this issue, this study takes the disentanglement of causal and bias substructures as the key to improve model stability.
- p.386 abstract: Experimental results on two complex industrial datasets indicate that CDGNN is an effective and stable method for fault diagnosis.
- p.386 introduction: FAULT diagnosis is one of the key techniques for prognostics and health management, serving a vital function in guaranteeing the secure and efficient operation of complex systems as well as reducing maintenance costs [1].
- p.387 introduction: However, the bias substructure is independent of fault, which will result in large prediction biases.
- p.387 introduction: Based on the above analysis, a causal disentangled GNN (CDGNN) framework for fault diagnosis in complex industrial process is proposed.
- p.387 introduction: The main contributions are as follows.
- p.387 introduction: The rest of this article is organized as follows. Problem formulation and preliminaries are presented in Section II. Section III details the proposed CDGNN. In Section IV, we conducted case studies on two complex industrial datasets. Finally, Section V concludes this article.
- p.388 method: In this section, we analyze causal relationships in the fault diagnosis according to causal theory and develop a structural causal model (SCM).
- p.391 experiments: This section presents an evaluation of the effectiveness of CDGNN in addressing fault diagnosis in complex industrial process.
- p.395 conclusion: In this study, we excavated the causal relationships inherent to GNN-based fault diagnosis according to the causal theory and introduced the novel CDGNN.
- p.395 conclusion: This study was conducted in the closed-world assumption that all faults in testing data had already appeared in training data.
- p.395 conclusion: Further research will focus on applying CDGNN to open-set recognition, distinguishing, and identifying unknown faults based on causal features, and detecting hidden unknown faults in time.
