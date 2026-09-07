# 设计

不新增自建 harness 配置框架；现有 tracked AGENTS 是共同入口，CLAUDE 只处理其原生加载。保持个人配置目录忽略，文档写出显式上下文读取路径。完整集合安装说明解决当前覆盖缺口，不改变缺失脚本时 exit/gate 行为。

## 文件与边界

具体文件范围见本任务 prd.md；实现只读取本范围所需上下文。共享文件按前置顺序串行处理。相关根因见父任务 research/runtime-findings.md、test-baseline.md 及 harness-rules.md。

## 模型与工具

agent-skill 强模型负责能力边界与安装契约；便宜模型可完成给定事实表的双语文档和隔离 fixture/测试，官方能力与语义最终由强模型审查。

## 回退

只回退本任务引入的 diff，保留原有 README 推荐模型改动。源资源、镜像与 manifest 同进同退；不回滚其他子任务。
