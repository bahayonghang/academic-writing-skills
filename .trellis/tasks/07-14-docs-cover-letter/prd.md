# 重构 cover-letter 双语文档

## Goal

将 `cover-letter` 的技能概览和全部公开资源迁移到统一路径并提供完整中英文版本，
严格对齐当前 `SKILL.md` 的路由、输入、命令、输出和安全边界。

## Scope

当前基线包含 8 个 references、10 个 templates、4 个 examples、2 个公开 agent 说明，共 24 个源资源、每种语言 24 个目标资源。
实现时以核心 manifest 动态盘点为准；若源文件变化，必须同步更新本任务记录和译文。

## Requirements

- 源文件以英文为主，英文页保持源内容，中文页完整翻译。
- 资源路径统一为 `resources/{references,templates,examples,agents}/...`。
- 技能概览按共享七段结构重写，并链接全部四类中实际存在的资源。
- template YAML frontmatter、期刊标识、声明要求、claim-evidence schema 和禁用措辞等级必须保持语义与机器字段。
- 修复迁移后的相对链接并删除本技能旧资源路径，不保留兼容副本。
- 不修改 `academic-writing-skills/cover-letter/` 下的技能源文件。

## Acceptance Criteria

- [ ] 当前 24 个源资源均有规范英文页和中文页；无漏项、多余项或旧路径残留。
- [ ] 两种语言的概览模块/模式、命令、输入和输出逐项对应当前 `SKILL.md`。
- [ ] `check_resource_sync.py --skill cover-letter` 通过。
- [ ] 标题层级、代码块、inline 技术 token、表格结构和相对链接检查通过。
- [ ] 对 `references/CLAIM_EVIDENCE_CONTRACT.md`、`references/ai-disclosure-policy.md`、Nature/IEEE template、两个 agent 说明 完成逐段双语抽样复核。
- [ ] VitePress build 与 `git diff --check` 通过。

## Out of Scope

其他技能、共享 checker/导航机制、技能行为与旧 URL 重定向。

## Dependency

必须在 `07-14-docs-bilingual-core` 完成后启动。
