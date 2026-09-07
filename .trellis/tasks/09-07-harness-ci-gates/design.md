# 设计

测试发现唯一入口是 pytest 配置，just 不再独立枚举目录。新增检查工作流与已有部署工作流分开，避免 PR 获得 Pages 写权限。最低支持/实际本机 Python 版形成明确验证范围，不扩大版本全排列。

## 文件与边界

具体文件范围见本任务 prd.md；实现只读取本范围所需上下文。共享文件按前置顺序串行处理。相关根因见父任务 research/runtime-findings.md、test-baseline.md 及 harness-rules.md。

## 模型与工具

Claude Code 或 Codex 上的强模型审查事件/权限/失败传播；便宜模型可执行已明确的 YAML、pytest 配置与命令修改，最终 hosted 证据由强模型核验。

## 回退

只回退本任务引入的 diff，保留原有 README 推荐模型改动。源资源、镜像与 manifest 同进同退；不回滚其他子任务。
