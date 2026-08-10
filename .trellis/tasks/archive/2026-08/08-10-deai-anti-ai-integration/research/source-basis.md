# `writing-anti-ai` 来源依据与风险评估

## 来源身份

本任务的直接参考是 `ref/claude-scholar/skills/writing-anti-ai/`，版本 `1.0.0`。该
skill 自述基于 Wikipedia WikiProject AI Cleanup 的 “Signs of AI writing”，并称合并了
`humanizer`、`humanizer-zh` 与 `stop-slop` 的内容。其本地来源说明只有一句“用作模式启发，
不要机械复制措辞”，没有给出固定快照、修订版本、抽样方法、学术论文语料或检测精确率。

因此，本任务将它定级为：**面向通用散文的社区模式清单，不是 AI 文本鉴定标准，也不是
学术写作规范。** 它可以提供候选审阅维度，不能支持“某段由 AI 生成”、AI 概率、查重通过率
或检测器规避承诺。

## 可用证据与局限

| 来源内容 | 可支持的结论 | 不能支持的结论 |
| --- | --- | --- |
| `references/patterns-english.md` / `patterns-chinese.md` 的 20 类模式 | 通用文本中存在可人工审阅的重复修辞形态 | 单词或标点命中即可判定 AI；这些模式在学术论文中必然错误 |
| `phrases-to-cut.md` | 部分填充语可在不损失信息时压缩 | 词表项可以无条件删除；所有语言和学科共享同一替换 |
| `wikipedia-source.md` | 模式来自社区维护页面的启发 | 来源完整、版本固定、已针对本仓库验证 |
| `examples/*.md` | 展示了参考 skill 期望的“前后对比”形式 | `After` 内容保持了原文事实，或可作为本仓库改写样例 |
| 50 分 Quick Scoring | 参考 skill 使用主观五维评分 | 分数可重复、可校准，或能表示真实性/AI 概率 |

## 示例完整性审计

参考示例不能直接移植。多处 `After` 为了“具体化”而加入 `Before` 中不存在的事实，包括：

- 学术摘要新增“调查 500 名青少年”“焦虑得分低 40%”；
- 软件更新新增 beta tester 反馈与完成速度；
- 公司简介新增 127 项专利和 6 项年度授权；
- 产品发布新增价格、12 个国家和预购增长 20%；
- 其他例子新增居民数量、市场、教堂、建筑师陈述等细节。

这些改写违反本仓库既有 Zero Fabrication 与 `Changed / Protected / Meaning-Check /
Risk-Flags` 契约。实施只能吸收**审阅模式**，不得复制参考改写文本或仿照其“用虚构数字替换
空泛表达”的做法。缺少支持时保留原边界并标记 `needs evidence` / `待补证`。

## 学术场景适配原则

1. 模式必须按“组合行为 + 上下文”判断，不以单词作为 AI 归因证据。
2. 学术合法结构优先：三项真实贡献、合法 hedge、技术术语 `represents`、带证据的
   `highlighting`、精确范围和范围局限都不得因表面形态被改坏。
3. “保留信息，不保留原修辞壳”只授权局部重组；引用、数值、术语、claim 强度、适用范围和
   用户未授权的章节结构仍受保护。
4. 新增模式按 `.trellis/spec/academic-writing-skills/polish-rewrite-contract.md` 归 C 档
   `llm-only`。没有真实论文标定前，不扩充默认正则、阈值或词表。
5. 未执行 provider-backed eval、作者盲评或真实论文精确率评估时，模型效果一律标为
   `missing evidence / UNVERIFIED`。

## 归属要求

实施后的 runtime reference 应注明该模式谱系来自 Wikipedia 社区指南及通用 humanizer
先例，已按学术证据保全要求重新设计。不得称其为官方规范、AI 检测规则或已验证的降 AI 率
方法。
