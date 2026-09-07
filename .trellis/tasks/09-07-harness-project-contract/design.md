# 设计

采用现有 AGENTS.md 为共享事实入口、CLAUDE.md 为薄入口；学术禁造假/只读审查/批准后实施等共同规则避免复制。PDF 依赖说明取实际 lazy import，不安装依赖。项目级规范不指向作者机器的 C:/Users 路径。

## 文件与边界

具体文件范围见本任务 prd.md；实现只读取本范围所需上下文。共享文件按前置顺序串行处理。相关根因见父任务 research/runtime-findings.md、test-baseline.md 及 harness-rules.md。

## 模型与工具

强模型做规则所有权、许可决策传达与最后审查；便宜模型可按批准表修改版本/依赖措辞，但不得改推荐模型行或重写法律文本。

## 回退

只回退本任务引入的 diff，保留原有 README 推荐模型改动。源资源、镜像与 manifest 同进同退；不回滚其他子任务。
