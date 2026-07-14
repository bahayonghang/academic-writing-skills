# 重构 latex-thesis-zh 双语文档

## Goal

将 `latex-thesis-zh` 的技能概览和全部公开资源迁移到统一路径并提供完整中英文版本，
严格对齐当前 `SKILL.md` 的路由、输入、命令、输出和安全边界。

## Scope

当前基线包含 39 个 references、4 个 templates、5 个 examples，共 48 个源资源、每种语言 48 个目标资源。
实现时以核心 manifest 动态盘点为准；若源文件变化，必须同步更新本任务记录和译文。

## Requirements

- 源文件以中文为主但夹有英文模块说明；逐文件确认 source locale，中文页完整中文化，英文页完整英文化。
- 资源路径统一为 `resources/{references,templates,examples,agents}/...`。
- 技能概览按共享七段结构重写，并链接全部四类中实际存在的资源。
- GB/T 编号、学校模板事实、LaTeX 命令、摘要/绪论/过程章/方法章/结论章的强制结构和 checker 代码必须保持准确；中文规范术语的英文译名要稳定。
- 修复迁移后的相对链接并删除本技能旧资源路径，不保留兼容副本。
- 不修改 `academic-writing-skills/latex-thesis-zh/` 下的技能源文件语义；允许为满足源页精确同步与
  `git diff --check` 同时通过而规范化 `caption-guide.md` 中一处无语义尾随空格。

## Acceptance Criteria

- [x] 当前 48 个源资源均有规范英文页和中文页；无漏项、多余项或旧路径残留。
- [x] 两种语言的概览模块/模式、命令、输入和输出逐项对应当前 `SKILL.md`。
- [x] `check_resource_sync.py --skill latex-thesis-zh` 通过。
- [x] 标题层级、代码块、inline 技术 token、表格结构和相对链接检查通过。
- [x] 对 `references/modules/routing-rules.md`、abstract/conclusion modules、四个 chapter guide、GB standard、thuthesis/yanshan templates 完成逐段双语抽样复核。
- [x] VitePress build 与 `git diff --check` 通过。

## Out of Scope

其他技能、共享 checker/导航机制、技能行为与旧 URL 重定向。

## Dependency

必须在 `07-14-docs-bilingual-core` 完成后启动。
