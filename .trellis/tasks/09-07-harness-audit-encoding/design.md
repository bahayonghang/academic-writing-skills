# 设计

只修改拥有 Python checker 进程边界的函数，使用 dict(os.environ, PYTHONIOENCODING='utf-8') 与 encoding='utf-8' 成对约定。无需防御链、配置选项或兼容 shim。

## 文件与边界

具体文件范围见本任务 prd.md；实现只读取本范围所需上下文。共享文件按前置顺序串行处理。相关根因见父任务 research/runtime-findings.md、test-baseline.md 及 harness-rules.md。

## 模型与工具

Codex 强模型负责复现/根因及复核；已固定边界后可由更便宜 coding 模型完成单函数与回归测试。出现解析/gate 语义变化立即升级主审。

## 回退

只回退本任务引入的 diff，保留原有 README 推荐模型改动。源资源、镜像与 manifest 同进同退；不回滚其他子任务。
