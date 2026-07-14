# 重构双语文档契约与核心页面

## Goal

建立统一资源路径、公开资源清单、双语一致性检查和可扩展侧栏，并重构两种语言的
核心入口页，为后续 6 个技能翻译子任务提供稳定契约。

## Requirements

- 从 6 个技能的 `references`、`templates`、`examples` 和公开 Markdown agents
  推导完整 source inventory，不用手写固定总数。
- 生成并校验 `docs/resource-manifest.json`；每行记录技能、种类、源路径、源语言、
  源散列及英/中文规范路径。
- 目标路径统一为 `resources/{references,templates,examples,agents}`；旧路径不兼容。
- 检查器支持 inventory-only、单技能和全量三种范围，以便子任务分阶段交付。
- VitePress 侧栏递归发现规范资源树，稳定排序并使用各语言页面 H1。
- 重构英文/中文首页、安装、quick-start、usage 和技能总览，按当前 6 个 `SKILL.md`
  统一路由与术语。
- 不在本子任务中批量翻译任一技能的资源正文。

## Acceptance Criteria

- [x] 完整 source inventory 与 manifest 一致，新增/删除公开源文件会使检查失败。
- [x] manifest 中每个目标路径符合统一路径契约且两种语言一一对应。
- [x] checker 的 inventory-only、单技能、全量模式有定向测试。
- [x] 侧栏生成器能处理四类资源、嵌套目录、大小写文件名和非 Markdown 资产。
- [x] 10 个核心入口页（5 英文 + 5 中文）与当前六技能路由一致。
- [x] 文档构建和定向测试通过；现有技能翻译缺口由后续子任务承担。

## Out of Scope

- 技能资源正文翻译。
- 修改技能包、主题视觉、部署工作流或旧 URL 重定向。

## Dependency

本子任务必须先完成。所有技能子任务依赖其 manifest、路径和检查契约。
