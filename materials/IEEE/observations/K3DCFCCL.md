---
key: K3DCFCCL
title: "A Survey on Deep Learning for Data-Driven Soft Sensors"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2021.3053128"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-14"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. SIGNIFICANCE OF DL FOR SOFT SENSOR` → `III. DL MODELS AND GENERAL TRICKS` → `IV. DL APPLICATIONS FOR SOFT SENSOR MODELING` → `V. DISCUSSIONS AND OUTLOOK` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。综述体：相关工作分布在 II–IV，Introduction 只给动机与问题清单。Introduction 末有 `The rest of this article is organized as follows`。无 Experiments 节；IV 为应用综述，V 为展望。

## Openers

- abstract: `Soft sensors are` — "Soft sensors are widely constructed in process industry to realize process monitoring, quality prediction, and many other important applications." (p.5853)
- introduction: `NOWADAYS, the process` — "NOWADAYS, the process industry is becoming more and more complicated, due to the development of information technologies and the increase of customer demands." (p.5853)
- method: `In this section` — "In this section, typical models and general tricks in DL field are reviewed and summarized, including autoencoder (AE), restricted Boltzmann machine (RBM), convolutional NN (CNN), and recurrent NN (RNN)." (p.5856, III)
- experiments: `A successful development` — "A successful development of DL algorithms is actually a highly iterative process, which can be summarized as Fig. 8." (p.5858, IV)
- conclusion: `DL techniques have` — "DL techniques have shown their great potential in many fields, as well as in soft sensor." (p.5862)

## Gap transitions

- however (introduction): "However, in order to monitor the operation status of systems, realize the smooth control of processes and improve the quality of products, those key variables or quality indices have to be obtained as fast and accurately as possible." (p.5853)
- however (introduction): "However, the increasing complexity of industrial process makes these preconditions difficult to meet." (p.5853)
- therefore (abstract/introduction): "Therefore, in this article, the necessity and significance of deep learning for soft sensor applications are demonstrated first by analyzing the merits of deep learning and the trends of industrial processes." (p.5853)
- although (section II): "Although those methods already have many applications, they may suffer from some drawbacks, such as heavy workload brought by handcrafted feature engineering or inefficiency when dealing with large amount of data, etc." (p.5854)
- although (outlook): "Although DL has made great progress in many fields, there is still a lot of work to do to better apply the advanced methods in the soft sensor domain, especially to meet the demands in practical industrial processes." (p.5862)

## Hedge verbs

- demonstrate / causal / abstract, introduction: "the necessity and significance of deep learning for soft sensor applications are demonstrated first"
- summarize / causal / abstract: "mainstream deep learning models, tricks, and frameworks/toolkits are summarized and discussed"
- show / causal / abstract, conclusion: "Deep learning, as a kind of data-driven approach, shows its great potential"; "DL techniques have shown their great potential"
- hope / speculative / conclusion: "It is our hope for this article to serve as a taxonomy and also a tutorial"

## Cross-section linkers

- introduction → method: "The rest of this article is organized as follows. Section II discusses the distinct merit of DL and demonstrates its necessity for soft sensor modeling. Section III provides an overview of several typical DL models and core training techniques. Then, the state of the art of soft sensor applications using DL approaches is investigated in Section IV. Discussions and outlook are given in Section V. Finally, Section VI concludes this article." (p.5853)
- method → applications: III 框架表后 `IV. DL APPLICATIONS FOR SOFT SENSOR MODELING` (p.5858)
- applications → conclusion: V 展望后 `VI. CONCLUSION` (p.5862)

## Candidate rules

- R002 综述无独立 Related Work，引言只列问题清单，综述正文在 II–IV。
- R003 Introduction 末用 `The rest of this article is organized as follows` 指向 II–VI。
- R004 结论用编号收回四条贡献。
- R005 Outlook 节独立于 Conclusion：`V. DISCUSSIONS AND OUTLOOK`。
- 综述结论可用 `It is our hope for this article to serve as`。

## Candidate phrases

- `Therefore, in this article, the necessity and significance` (abstract)
- `the motivation of this article is to answer these questions` (introduction)
- `The rest of this article is organized as follows.` (introduction)
- `In order to summarize the past, analyze the present, and look into the future, in this article, we made the following contributions` (conclusion)
- `It is our hope for this article to serve as a taxonomy` (conclusion)

## House style

自称是 `in this article` / `we made the following contributions` / `Here, we classify them`。未见 `In this paper`。`Here, we classify` 与 `in this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.5853 abstract: Soft sensors are widely constructed in process industry to realize process monitoring, quality prediction, and many other important applications.
- p.5853 abstract: With the development of hardware and software, industrial processes have embraced new characteristics, which lead to the poor performance of traditional soft sensor modeling methods.
- p.5853 abstract: Therefore, in this article, the necessity and significance of deep learning for soft sensor applications are demonstrated first by analyzing the merits of deep learning and the trends of industrial processes.
- p.5853 introduction: NOWADAYS, the process industry is becoming more and more complicated, due to the development of information technologies and the increase of customer demands.
- p.5853 introduction: However, the increasing complexity of industrial process makes these preconditions difficult to meet.
- p.5853 introduction: Therefore, the motivation of this article is to answer these questions as reasonably as possible.
- p.5853 introduction: The rest of this article is organized as follows. Section II discusses the distinct merit of DL and demonstrates its necessity for soft sensor modeling. Section III provides an overview of several typical DL models and core training techniques. Then, the state of the art of soft sensor applications using DL approaches is investigated in Section IV. Discussions and outlook are given in Section V. Finally, Section VI concludes this article.
- p.5854 method: Although those methods already have many applications, they may suffer from some drawbacks, such as heavy workload brought by handcrafted feature engineering or inefficiency when dealing with large amount of data, etc.
- p.5854 method: Here, we classify them into four categories at a greater granularity: rule-based system, classical machine learning, shallow representation learning, and deep learning.
- p.5856 method: In this section, typical models and general tricks in DL field are reviewed and summarized, including autoencoder (AE), restricted Boltzmann machine (RBM), convolutional NN (CNN), and recurrent NN (RNN).
- p.5858 applications: A successful development of DL algorithms is actually a highly iterative process, which can be summarized as Fig. 8.
- p.5862 outlook: Although DL has made great progress in many fields, there is still a lot of work to do to better apply the advanced methods in the soft sensor domain, especially to meet the demands in practical industrial processes.
- p.5862 conclusion: DL techniques have shown their great potential in many fields, as well as in soft sensor.
- p.5862 conclusion: In order to summarize the past, analyze the present, and look into the future, in this article, we made the following contributions to the application of DL theory in the field of soft sensor.
- p.5863 conclusion: It is our hope for this article to serve as a taxonomy and also a tutorial of advances elucidated from a multitude of works on DL-based soft sensors, and to provide the community with a picture of the roadmap and matters for future endeavors.
