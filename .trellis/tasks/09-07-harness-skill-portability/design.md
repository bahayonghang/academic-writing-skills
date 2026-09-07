# 设计

跨工具说明作为现有技能契约的适配提示，不把工具名称写成必须存在的 API。原生委派可用时使用，否则顺序执行并标注证据来源。lane 仍由现有脚本/报告契约消费，不增加新的字段体系。

在既有 synthesis agent 与 editorial decision standards 增加执行方式解释，要求最终报告/overall_assessment 正文明确 native delegated 或 sequential single-agent。后一种模式保留 lane 来源和现有 CONSENSUS 标签，但只能解释为同一会话跨视角一致，不得写独立专家组共识。此处是正文事实声明，不新增 JSON字段、评分规则或硬编码模式引擎；deterministic fallback 没有真实 reviewer 执行时必须明确为脚本回退。人工语义验收用同一小段 fixture 的两类执行说明核对标签解释，不能用字符串存在测试代替。

## 文件与边界

具体文件范围见本任务 prd.md；实现只读取本范围所需上下文。共享文件按前置顺序串行处理。相关根因见父任务 research/runtime-findings.md、test-baseline.md 及 harness-rules.md。

## 模型与工具

Claude Code 或 Codex 强模型负责跨技能一致性、审稿证据与输出约束；低成本模型只处理批准的文档镜像，不能负责学术严重度、引用真实性或 reviewer 综合。

## 回退

只回退本任务引入的 diff，保留原有 README 推荐模型改动。源资源、镜像与 manifest 同进同退；不回滚其他子任务。
