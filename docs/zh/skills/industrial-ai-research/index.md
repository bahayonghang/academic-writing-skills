# `industrial-ai-research`

面向 Industrial AI 文献调研的技能，包含 intake、按 venue 分层检索与结构化输出。

## 适用场景

- 预测性维护综述
- 智能调度文献扫描
- 工业异常检测进展追踪
- 智能制造与 CPS 趋势梳理
- Industrial AI 研究空白分析

## 工作流形态

1. intake
2. 检索规划
3. 来源收集
4. 验证与筛选
5. 综合分析
6. 报告组装

## 默认策略

如果用户没有明确说明，默认倾向于：

- 时间窗口为最近 3 年
- 研究重点由原始问题隐含决定

## 交付模式

| 模式 | 适用场景 |
| --- | --- |
| `research-brief` | 短而可决策的摘要 |
| `literature-map` | 按主题聚类的文献地图 |
| `venue-ranked survey` | 强调来源层级的综述 |
| `research-gap memo` | 研究空白与下一步机会 |

## 推荐提示词

```text
研究最近三年的 predictive maintenance 论文。
```

```text
比较 arXiv 和 IEEE automation venues 上的 scheduling RL 论文。
```

```text
写一份 industrial anomaly detection 的 research-gap memo。
```
