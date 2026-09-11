---
key: RCTK4PYP
title: "Real-time machine-learning-based optimization using Input Convex Long Short-Term Memory network"
venue: "Applied Energy"
doi: "10.1016/j.apenergy.2024.124472"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-6,10-14"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Nonlinear systems and optimization` → `3. Family of Recurrent Neural Networks and input convex neural networks` → `4. Input convex long short-term memory` → `5. IC-LSTM-based optimization` → `6` 光伏实时优化 → `7. Application to a chemical process` → `8. Conclusion`。前置 `ARTICLE INFO` / `Keywords` / `ABSTRACT`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 NN 优化、ICNN / ICFNN / ICRNN）。Introduction 末有节序路标，无编号贡献列表。Method 拆成系统类、RNN/ICNN 族与 IC-LSTM 证明。Experiments 为两案例（LHT 光伏 + CSTR）。

## Openers

- abstract: `Neural network-based optimization` — "Neural network-based optimization and control methods, often referred to as black-box approaches, are increasingly gaining attention in energy and manufacturing systems, particularly in situations where first-principles models are either unavailable or inaccurate."
- introduction: `Model-based optimization and` — "Model-based optimization and control have been widely applied in energy and chemical systems in decades [1–5]."
- method: `In this section,` — "In this section, we first propose a novel input convex network in the context of LSTM, and then theoretically prove the convex property of the IC-LSTM." (s.4)
- experiments: `Table 2 shows` — "Table 2 shows the average solving times (over 5 random runs) per step for LSTM and IC-LSTM." (s.6)
- conclusion: `In this study,` — "In this study, we developed a novel neural network architecture (i.e., IC-LSTM) that ensures convexity of the output with respect to the input, specifically tailored for convex neural network-based optimization and control."

## Gap transitions

- however (abstract): "However, their non-convex nature significantly slows down the optimization and control processes, limiting their application in real-time decision-making processes."
- to address (abstract): "To address this challenge, we propose a novel Input Convex Long Short-Term Memory (IC-LSTM) network to enhance the computational efficiency of neural network-based optimization."
- however (introduction): "However, traditional neural network-based optimization and control encounter challenges in computational efficiency for online implementation."
- therefore (introduction): "Therefore, in this study, by combining the strengths of the LSTM architecture with the benefits of convex optimization, we propose a novel Input Convex LSTM (IC-LSTM) network to enhance the computational efficiency of neural network-based optimization."
- however (experiments): "However, due to the modeling errors (i.e., especially for 𝑖𝑠 and 𝑑 as shown in Fig. 7), it is difficult for IC-LSTM to closely track the demand currents."

## Hedge verbs

- propose / causal / abstract, introduction, method: "we propose a novel Input Convex Long Short-Term Memory (IC-LSTM) network"; "we first propose a novel input convex network"
- demonstrate / causal / abstract, conclusion: "we demonstrate the superior performance of IC-LSTM-based optimization in terms of runtime"; "we demonstrated the efficacy and efficiency of our proposed framework"
- show / causal / experiments: "Table 2 shows the average solving times (over 5 random runs) per step for LSTM and IC-LSTM."
- highlight / causal / experiments: "We highlight that the findings in the results are consistent throughout the year"

## Cross-section linkers

- introduction → method: "The rest of this paper is organized as follows: Section 2 introduces nonlinear systems and model-based optimization. Section 3 provides a comprehensive overview of variants of RNNs and ICNNs, and proposes a novel IC-LSTM architecture, along with the underlying design principles. Section 4 delves into the proof of preservation of convexity for IC-LSTM, provides an implementation guide for the IC-LSTM cell, and evaluates its modeling performance on surface fitting for non-convex bivariate scalar functions. Section 5 proves the preservation of convexity in IC-LSTM-based optimization. Section 6 and Section 7 validate the performance and computational efficiency of our proposed framework against established baselines through case studies involving a solar PV energy system at LHT Holdings in Singapore and a continuous stirred tank reactor (CSTR), respectively."
- method → experiments: 凸优化证明后接光伏与 CSTR 案例
- experiments → conclusion: CSTR 讨论后 `8. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`The rest of this paper is organized as follows`
- R009 自称：`we propose` / `In this study, we developed`
- R010 摘要用 `To address this challenge, we propose`

## Candidate phrases

- `To address this challenge, we propose a novel` (abstract)
- `The rest of this paper is organized as follows:` (introduction)
- `we propose a novel Input Convex LSTM (IC-LSTM) network to enhance` (introduction)
- `In this study, we developed a novel neural network architecture` (conclusion)
- `we demonstrated the efficacy and efficiency of our proposed framework` (conclusion)

## House style

自称 `we propose` / `In this study` / `our proposed framework` / `this work`。未见 `Here we`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Neural network-based optimization and control methods, often referred to as black-box approaches, are increasingly gaining attention in energy and manufacturing systems, particularly in situations where first-principles models are either unavailable or inaccurate.
- abstract: However, their non-convex nature significantly slows down the optimization and control processes, limiting their application in real-time decision-making processes.
- abstract: To address this challenge, we propose a novel Input Convex Long Short-Term Memory (IC-LSTM) network to enhance the computational efficiency of neural network-based optimization.
- abstract: Specifically, in a real-time optimization problem of a real-world solar photovoltaic energy system at LHT Holdings in Singapore, IC-LSTM-based optimization achieved at least 4-fold speedup compared to conventional LSTM-based optimization.
- introduction: Model-based optimization and control have been widely applied in energy and chemical systems in decades [1–5].
- introduction: However, traditional neural network-based optimization and control encounter challenges in computational efficiency for online implementation.
- introduction: Therefore, in this study, by combining the strengths of the LSTM architecture with the benefits of convex optimization, we propose a novel Input Convex LSTM (IC-LSTM) network to enhance the computational efficiency of neural network-based optimization.
- introduction: The rest of this paper is organized as follows: Section 2 introduces nonlinear systems and model-based optimization.
- method: In this section, we first propose a novel input convex network in the context of LSTM, and then theoretically prove the convex property of the IC-LSTM.
- experiments: Table 2 shows the average solving times (over 5 random runs) per step for LSTM and IC-LSTM.
- experiments: In all cases, IC-LSTM enjoys a faster (at least 4×) solving time (for a scaled-up solar PV energy system or a longer prediction horizon, the time discrepancy could be even greater).
- experiments: Specifically, it achieves an average percentage decrease of 54.4%, 40.0%, and 41.3% compared to plain RNN, plain LSTM, and ICRNN, respectively.
- conclusion: In this study, we developed a novel neural network architecture (i.e., IC-LSTM) that ensures convexity of the output with respect to the input, specifically tailored for convex neural network-based optimization and control.
- conclusion: Through the real-time optimization of a real-world hybrid energy system at LHT Holdings and the simulation study of a dynamic CSTR system, we demonstrated the efficacy and efficiency of our proposed framework.
