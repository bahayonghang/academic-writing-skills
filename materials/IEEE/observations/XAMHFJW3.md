---
key: XAMHFJW3
title: "A Novel Multiscale Gated Structure Model for Soft Sensing of Nonstationary Process With Randomly Missing Data"
venue: "IEEE Transactions on Industrial Informatics"
doi: "10.1109/TII.2024.3476522"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-10"
date_observed: 2026-09-11
story_pattern: SP-IEEE-002
---

## Structure

罗马数字标题：`I. INTRODUCTION` → `II. REVISIT OF RNN MODEL` → `III. MULTISCALE GATED STRUCTURE MODEL` → `IV. SOFT SENSING BASED ON THE MGSM` → `V. CASE STUDY` → `VI. CONCLUSION`。前置 `Abstract—` 与 `Index Terms—`。无独立 Related Work。`related_work=inlined`（Introduction 中段评 PCR/PLSR、LTSFA/SSA、RNN/LSTM/GRU、FIR-CNN、Transformer、SIA-LSTM）。Introduction 末无 `The rest of this article is organized as follows`，贡献列表后直接进入 II。II 为 RNN 回顾，不是综述节。Experiments 标题为 `CASE STUDY`。有 Appendix。

## Openers

- abstract: `Due to operating` — "Due to operating condition drift, environmental changes, and system oscillations, industrial processes often exhibit nonstationary characteristics that involve both stable long-term trend and fluctuant short-term dynamics." (p.1)
- introduction: `PRODUCT quality is` — "PRODUCT quality is of great significance for ensuring the safety and efficiency of industrial production processes." (p.1；栏首掉字)
- method: `In this section` — "In this section, a novel gated structure model is proposed to capture the characteristics of nonstationary processes with random data missing." (p.2, III)
- experiments: `In this section` — "In this section, the performance of the gated structure based soft sensing model is validated using the TE and thermal power plant process." (p.5, V)
- conclusion: `This article proposes` — "This article proposes an RM-MGSM model for extracting long-term trend and short-term dynamic components for soft sensing of nonstationary processes." (p.8)

Preliminaries 首句："In this section, a brief review of RNN is provided, which involves a hidden layer with cyclic structure and is capable of capturing autocorrelation information." (p.2, II)。不单列 `related_work` opener。

## Gap transitions

- however (introduction): "However, complex industrial processes often exhibit nonstationary characteristics, and the abovementioned methods only focus on stationary data." (p.1)
- despite (introduction): "Despite the research progress, it is still difficult to construct an accurate soft sensor for nonstationary industrial processes that exhibit complex characteristics like long-term trends, short-term dynamics, random missing. and nonlinearity [10]." (p.1)
- however (introduction): "However, due to complex internal mechanisms, process disturbances and random noise, nonstationary industrial processes often exhibit short-term dynamic characteristics, i.e., short-term abrupt fluctuations, which cannot be well captured by traditional methods [18]." (p.2)
- nevertheless (introduction): "Nevertheless, most of the abovementioned methods are designed for data missing at some certain mode, they are not suitable for practical industrial scenarios whose data may be missing at random." (p.2)
- based on (introduction): "Based on the abovementioned discussions, this article proposes a novel multiscale gated structure model (MGSM) to simultaneously extract long-term trends and short-term dynamic features based on enhanced gated units, and design a missing interval function for the application to soft sensing under random data missing." (p.2)

## Hedge verbs

- propose / causal / abstract, introduction, method: "a novel multiscale gated structure model (MGSM) is proposed"; "this article proposes a novel multiscale gated structure model"; "a novel gated structure model is proposed"
- show / causal / abstract, introduction: "application studies ... show that the proposed method has significant advantages"; "The experimental results show the superiority of the proposed method"
- indicate / associative / experiments: "which indicates the lack of long-term trend information in the extracted features"; "which indicates that it can accurately reflect the nonstationary characteristics"

## Cross-section linkers

- introduction → preliminaries: 贡献列表后无节序路标，直接 `II. REVISIT OF RNN MODEL` (p.2)
- method → experiments: "The whole procedures of soft sensing are shown in Table I." 随后 `V. CASE STUDY` (p.5)
- experiments → conclusion: 计算时间段落后直接 `VI. CONCLUSION` (p.8)

## Candidate rules

- R001 摘要贡献句用 `In this article, a novel ... is proposed`，不用 `Here we`。
- R002 Related Work 并入 Introduction；II 是 RNN 回顾而非 RELATED WORK。
- R004 贡献用 `The main contributions of this article are summarized as follows.` + 编号列表。
- 本篇无 `The rest of this article is organized as follows`，不计入 R003。
- R005 结论先收回方法与两案例，无 `Although`/`Nevertheless` 局限段。

## Candidate phrases

- `In this article, a novel ... is proposed` (abstract)
- `Based on the abovementioned discussions, this article proposes` (introduction)
- `The main contributions of this article are summarized as follows.` (introduction)
- `This article proposes an RM-MGSM model` (conclusion)

## House style

自称 `In this article` / `this article proposes` / `the proposed method` / `the proposed model`。未见 `Here we`、`In this paper`。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- p.1 abstract: Due to operating condition drift, environmental changes, and system oscillations, industrial processes often exhibit nonstationary characteristics that involve both stable long-term trend and fluctuant short-term dynamics.
- p.1 abstract: In this article, a novel multiscale gated structure model (MGSM) is proposed for nonstationary process soft sensing, which includes long-term memory chain (stable and low frequency) and short-term dynamic chain (respond to fluctuations).
- p.1 abstract: Finally, application studies to the Tennessee Eastman process and a thermal power generating process show that the proposed method has significant advantages in the quality prediction of nonstationary process.
- p.1 introduction: PRODUCT quality is of great significance for ensuring the safety and efficiency of industrial production processes.
- p.1 introduction: However, complex industrial processes often exhibit nonstationary characteristics, and the abovementioned methods only focus on stationary data.
- p.1 introduction: Despite the research progress, it is still difficult to construct an accurate soft sensor for nonstationary industrial processes that exhibit complex characteristics like long-term trends, short-term dynamics, random missing. and nonlinearity [10].
- p.2 introduction: Nevertheless, most of the abovementioned methods are designed for data missing at some certain mode, they are not suitable for practical industrial scenarios whose data may be missing at random.
- p.2 introduction: Based on the abovementioned discussions, this article proposes a novel multiscale gated structure model (MGSM) to simultaneously extract long-term trends and short-term dynamic features based on enhanced gated units, and design a missing interval function for the application to soft sensing under random data missing.
- p.2 introduction: The main contributions of this article are summarized as follows.
- p.2 preliminaries: In this section, a brief review of RNN is provided, which involves a hidden layer with cyclic structure and is capable of capturing autocorrelation information.
- p.2 method: In this section, a novel gated structure model is proposed to capture the characteristics of nonstationary processes with random data missing.
- p.5 experiments: In this section, the performance of the gated structure based soft sensing model is validated using the TE and thermal power plant process.
- p.8 conclusion: This article proposes an RM-MGSM model for extracting long-term trend and short-term dynamic components for soft sensing of nonstationary processes.
- p.8 conclusion: Finally, two industrial cases show that the proposed model is more suitable for nonstationary industrial processes and can maintain outstanding prediction accuracy.
