# 深度研究 (deep-research)

面向自动化与 Industrial AI 的深度研究技能，具备强制 intake 问答、按 venue 分层的检索策略，以及稳定的结构化报告输出。

## 概述

`deep-research` 是一个偏研究前置的技能，适合做预测性维护、智能调度、工业异常检测、智能制造与 CPS 等方向的文献调研。

它和本仓库偏写作或审查的技能不同：先问清报告语言、输出形式、时间窗和研究侧重点，再按 arXiv 与 IEEE/自动化 venue 优先级进行检索和综合。

## 主要能力

- 在综合前先做 intake，确认报告语言、交付模式、时间范围与 Industrial AI 子方向
- 以 Industrial AI 为中心组织文献来源，robotics 相关 venue 作为交叉补充
- 区分 recent arXiv、IEEE automation venue 与相邻工业/控制 venue
- 提供固定的四种报告模式
- 在最终综合前执行一次反向质疑，暴露证据薄弱点和过度结论

## Intake 问题

技能会先问这四个问题：

1. 报告语言
2. 交付模式
3. 时间窗口
4. Industrial AI 研究侧重点

默认语言选项：
- `English`
- `Simplified Chinese`
- `Bilingual summary`

## 交付模式

| 模式 | 适用场景 |
|---|---|
| `research-brief` | 快速决策摘要 |
| `literature-map` | 主题化文献地图 |
| `venue-ranked survey` | 强调来源层级的文献调研 |
| `research-gap memo` | 研究空白与下一步机会分析 |

## 默认来源策略

Primary anchors:
- arXiv `eess.SY`
- arXiv `cs.AI`
- IEEE Transactions on Automation Science and Engineering
- IEEE CASE

Secondary crossover sources:
- arXiv `cs.RO`
- arXiv `cs.LG`
- ICRA
- IROS
- RA-L
- T-RO

## 示例请求

```text
Deep research recent predictive maintenance papers
```

```text
Compare latest scheduling RL papers from arXiv and IEEE
```

```text
Research industrial anomaly detection gaps and summarize them in Chinese
```
