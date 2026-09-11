---
key: IKFPMCK4
title: "Multiscale Dynamic Feature Learning for Quality Prediction Based on Hierarchical Sequential Generative Network"
venue: "IEEE Sensors Journal"
doi: "10.1109/JSEN.2023.3290163"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-5,6-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. OVERVIEW OF RNN AND DBN` → `III. HIERARCHICAL SEQUENTIAL GENERATIVE NETWORK` → `IV. CASE STUDIES` → `V. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PLS / ICA / PCA / SVR / ANN / ELM / DAE / GAN / RNN / LSTM）。Introduction 末有节序路标，指向 Section II–V。Method 在 III。Experiments 标题为 `CASE STUDIES`（加氢裂化，航空煤油 90% 沸腾点）。

## Openers

- abstract: `In industrial processes` — "In industrial processes, long short-term memory (LSTM) is usually used for temporal dynamic modeling of soft sensor." (p.1)
- introduction: `MODERN industrial processes` — "MODERN industrial processes are often equipped with a large number of hard sensors for real-time measurement of process data, which can provide timely information for process control and optimization." (p.1；栏首掉字)
- method: `In industrial plants` — "In industrial plants, process variables are usually sampled by hard sensors." (p.4, III)
- experiments: `The new HSGN` — "The new HSGN method is used for quality prediction in industrial process." (p.5, IV)
- conclusion: `This article mainly` — "This article mainly addresses the multiscale temporal correlations in process data." (p.8)

## Gap transitions

- however (abstract): "However, LSTM model can only extract the dynamic features at a specific time scale, which affects the feature learning capability and modeling accuracy." (p.1)
- even so (introduction): "Even so, there are still a number of key variables, such as gas composition and product concentration, that cannot be directly measured by online instruments due to severe production environment and immature technology [1], [2], [3], [4]." (p.1)
- to address (introduction): "To address these issues, soft sensor technology has been developed." (p.1)
- however (introduction): "However, the aforementioned methods are all static models." (p.2)
- to cope (introduction): "To cope with these problems, a new hierarchical sequential generative network (HSGN) is developed in this article." (p.2)

## Hedge verbs

- propose / causal / abstract: "a new hierarchical sequential generative network (HSGN) is proposed"
- develop / causal / introduction: "a new hierarchical sequential generative network (HSGN) is developed in this article"
- show / causal / abstract, introduction: "The application in a real industrial scene shows the effectiveness of the proposed method"; "A large number of experiments and applications show that"
- can / speculative / abstract, conclusion: "the HSGN method can take advantage of large number of unlabeled samples"; "an attention mechanism can be used"
- outperform / causal / experiments: "the proposed HSGN outperforms DBN and LSTM"

## Cross-section linkers

- introduction → method: "The remaining layout of this article is given as follows. Section II briefly states the structures and model formulations of LSTM and DBN, followed by Section III where a detailed introduction of the proposed HSGN method is given. Section IV provides a minute description of building the soft sensor model, and the proposed method-based soft sensor is assessed on an actual industrial scene. In Section V, conclusions are given for this article." (p.3)
- method → experiments: Algorithm 1 / Fig. 6 后 `IV. CASE STUDIES` (p.5)
- experiments → conclusion: "Comparatively speaking, the proposed HSGN outperforms DBN and LSTM with only a small error between the predicted and real values." 随后 `V. CONCLUSION` (p.8)

## Candidate rules

- R001 abstract 先 `However, LSTM model can only` 立 gap，再用 `In this article, a new X is proposed`。
- R002 Introduction 无独立 Related Work，静态/动态方法评述写在引言中段。
- R003 Introduction 末用 `The remaining layout of this article is given as follows` 指向 II–V。
- R004 Conclusion 开篇 `This article mainly addresses`，收束用 `in future research, an attention mechanism can be used`。
- R005 Experiments 标题为 `CASE STUDIES`，对比 DBN / LSTM / 所提方法。

## Candidate phrases

- `In this article, a new hierarchical sequential generative network (HSGN) is proposed for` (abstract)
- `To cope with these problems, a new ... is developed in this article.` (introduction)
- `The remaining layout of this article is given as follows.` (introduction)
- `This article mainly addresses` (conclusion)
- `in future research, an attention mechanism can be used to` (conclusion)

## House style

自称是 `In this article` / `This article` / `the proposed method`。未见 `Here we`。未见 `In this paper`。`In this article` 进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: In industrial processes, long short-term memory (LSTM) is usually used for temporal dynamic modeling of soft sensor.
- p.1 abstract: However, LSTM model can only extract the dynamic features at a specific time scale, which affects the feature learning capability and modeling accuracy.
- p.1 abstract: In this article, a new hierarchical sequential generative network (HSGN) is proposed for mining multiscale dynamic features using large amount of unlabeled process data for soft sensor.
- p.1 abstract: The application in a real industrial scene shows the effectiveness of the proposed method.
- p.1 introduction: MODERN industrial processes are often equipped with a large number of hard sensors for real-time measurement of process data, which can provide timely information for process control and optimization.
- p.1 introduction: To address these issues, soft sensor technology has been developed.
- p.2 introduction: However, the aforementioned methods are all static models.
- p.2 introduction: To cope with these problems, a new hierarchical sequential generative network (HSGN) is developed in this article.
- p.3 introduction: The remaining layout of this article is given as follows. Section II briefly states the structures and model formulations of LSTM and DBN, followed by Section III where a detailed introduction of the proposed HSGN method is given.
- p.4 method: In industrial plants, process variables are usually sampled by hard sensors.
- p.5 experiments: The new HSGN method is used for quality prediction in industrial process.
- p.8 experiments: Comparatively speaking, the proposed HSGN outperforms DBN and LSTM with only a small error between the predicted and real values.
- p.8 conclusion: This article mainly addresses the multiscale temporal correlations in process data.
- p.8 conclusion: To summarize, the newly proposed HSGN model, which combines a series of pretrained dynamic LSTM networks with a static DBN, can effectively utilize a large number of unlabeled samples and extract multiscale dynamic feature representations from dynamic process sequence data.
- p.8 conclusion: Therefore, in future research, an attention mechanism can be used to consider the impact of different time-scale dynamic features on the final output.
