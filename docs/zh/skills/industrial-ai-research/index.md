# `industrial-ai-research`

面向 Industrial AI 文献调研的技能，包含 intake、按 venue 分层检索与结构化输出。

## 适用场景

- 预测性维护综述
- 智能调度文献扫描
- 工业异常检测进展追踪
- 智能制造与 CPS 趋势梳理
- Industrial AI 研究空白分析
- 文献综述质量标准参考（A1-A4 规则适用于综述写作）

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
| `survey-draft` | 先 taxonomy、后证据包、再逐节写作的综述草稿，并可选转交 `latex-paper-en` |

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

- 常规模式最终输出为一份稳定结构的报告；`survey-draft` 会额外产出 `outline.yml`、分节 evidence 文件、分节草稿、合并后的 `survey-draft.md` 和 `quality-report.md`。
- 当前强化方向是把 `survey-outline`、`survey-evidence`、`survey-write`、`survey-merge` 保持为严格分阶段模块：在大纲获批且证据包完成前，不生成正文 prose。
- survey prose 必须保留冲突证据，优先采用“共识 -> 分歧 -> 局限 -> 空白”的组织链条，而不是逐篇点名或强行写成统一意见。
