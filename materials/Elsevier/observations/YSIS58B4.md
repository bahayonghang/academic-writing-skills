---
key: YSIS58B4
title: "Knowledge-data-driven process monitoring based on temporal knowledge graphs and supervised contrastive learning for complex industrial processes"
venue: "Journal of Process Control"
doi: "10.1016/j.jprocont.2024.103283"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-3,6-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Background` → `3. Proposed new monitoring strategy` → `4. Experiments and discussion` → `5. Conclusion`。前置 `ABSTRACT` 与 `ARTICLE INFO` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段解析模型、知识方法、PCA/CCA/ICA、GNN 与故障样本使用）。Section 2 为 Background（时序知识图谱、距离相关、GCN、对比预测编码）。Introduction 末有编号贡献。Experiments 标题为 `Experiments and discussion`。

## Openers

- abstract: `Process monitoring detects` — "Process monitoring detects faults and issues alerts when faults occur."
- introduction: `In recent years` — "In recent years, the industrial sector has seen rapid growth."
- method: `Having provided a` — "Having provided a description of the problem, using the process knowledge and procedural data, temporal knowledge graphs are constructed." (s.3)
- experiments: `Glass melting involves` — "Glass melting involves heating and melting qualified raw materials into a homogeneous, defect-free, and shape-conforming glass melt [36–38]." (s.4.1)
- conclusion: `In the present` — "In the present paper, a process-monitoring method based on temporal knowledge graphs and supervised contrastive learning is proposed."

## Gap transitions

- however (abstract): "However, data and knowledge exhibit complementary characteristics, and using them together can contribute to enhancing monitoring performance."
- however (introduction): "However, these data-driven methods tend to overly rely on process data."
- therefore (introduction): "Therefore, we provide a temporal knowledge graph perspective to construct a knowledge-data-driven process-monitoring model, integrating fault information into monitoring statistics to fully use the advantages of knowledge, data, and faults."
- in light of (abstract): "In light of these considerations, we propose a process-monitoring method based on temporal knowledge graphs and supervised contrastive learning"

## Hedge verbs

- propose / causal / abstract, method, conclusion: "we propose a process-monitoring method"; "This paper proposes a new joint knowledge-data-driven strategy"; "a process-monitoring method ... is proposed"
- indicate / associative / conclusion: "Experimental results indicate that, compared to baseline methods, the proposed approach effectively monitors fault occurrences"
- demonstrate / causal / conclusion: "The application of this method to real production data from a glass company in Hebei has demonstrated its effectiveness."

## Cross-section linkers

- introduction → background: 编号贡献后直接 `2. Background`
- background → method: CPC 段落后 `3. Proposed new monitoring strategy`
- method → experiments: 在线监测步骤后 `4. Experiments and discussion`
- experiments → conclusion: 对比学习结果后 `5. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction；随后独立 Background 而非 Related Work。
- R004 编号贡献：`The main contributions of this work are summarized as follows`
- R009 自称：`we propose` / `In the present paper, ... is proposed`

## Candidate phrases

- `In light of these considerations, we propose` (abstract)
- `Therefore, we provide a ... perspective` (introduction)
- `The main contributions of this work are summarized as follows` (introduction)
- `This paper proposes a new joint knowledge-data-driven strategy` (method)
- `In the present paper, a ... method ... is proposed` (conclusion)

## House style

自称 `we propose` / `this study attempts` / `This paper proposes` / `In the present paper`。第一人称复数与被动并存。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Process monitoring detects faults and issues alerts when faults occur.
- abstract: However, data and knowledge exhibit complementary characteristics, and using them together can contribute to enhancing monitoring performance.
- abstract: In light of these considerations, we propose a process-monitoring method based on temporal knowledge graphs and supervised contrastive learning,which can fully use knowledge, data, and fault information to improve the monitoring performance of the model.
- introduction: In recent years, the industrial sector has seen rapid growth.
- introduction: However, these data-driven methods tend to overly rely on process data.
- introduction: Therefore, we provide a temporal knowledge graph perspective to construct a knowledge-data-driven process-monitoring model, integrating fault information into monitoring statistics to fully use the advantages of knowledge, data, and faults.
- method: Having provided a description of the problem, using the process knowledge and procedural data, temporal knowledge graphs are constructed.
- method: This paper proposes a new joint knowledge-data-driven strategy by constructing temporal knowledge graphs, extracting multilevel spatiotemporal features from the graph using differential pooling, and using fault data for supervised contrastive learning to construct statistical measures for monitoring.
- experiments: Glass melting involves heating and melting qualified raw materials into a homogeneous, defect-free, and shape-conforming glass melt [36–38].
- conclusion: In the present paper, a process-monitoring method based on temporal knowledge graphs and supervised contrastive learning is proposed.
- conclusion: Experimental results indicate that, compared to baseline methods, the proposed approach effectively monitors fault occurrences, maintains a low false alarm rate, and achieves a monitoring rate of over 95%.
