# 明确五套 Harness 的项目接入与上下文边界

优先级：P1。父需求：R1/R3/R5/R6。状态：planning。

## 目标与背景

.gitignore 忽略 .claude/.codex/.agents/.cursor，git ls-files 这些目录为空；.grok/.kimi-code/.omp 也未配置。工具存在不是团队交付证据。隔离 paper-audit 的 quick-audit 实际 RUN3/missing8，而完整布局 RUN11/missing0。

## 范围

- docs/installation.md
- docs/zh/installation.md
- docs/harnesses.md（新增）
- docs/zh/harnesses.md（新增）
- docs/.vitepress/config.ts
- tests/skills/paper_audit/test_installed_layout.py（新增）
- academic-writing-skills/paper-audit/SKILL.md（仅安装依赖/受限覆盖段；C5 后续顺序编辑）
- docs/skills/paper-audit/index.md、docs/zh/skills/paper-audit/index.md（上述安装契约镜像）

## 前置与授权

C1/C2/C3 完成；用户批准。

当前仅规划，禁止 task.py start/实现/正式规则回写。任务树归属不代替前置条件。不同工作者不得覆盖其他子任务或用户改动。

## 验收条件

以下需求编号继承父任务的同名要求，本子任务负责其中与自身范围有关的交付。

- R1：项目结构、关键入口和共同事实准确。
- R3：改造有已复现失败或工作流缺口证据，不混同历史与当前。
- R5：文件范围、前置与检查可实施、可逐项验收。
- R6：五套工具规则/使用说明无冲突，不混同原生与已验证能力。

- [x] AC1（R1/R6）：五工具都有项目维护和论文 skill 使用的清晰入口、加载方式、委派/权限差异、版本/日期和官方来源。
- [x] AC2（R1/R6）：新 clone 可通过 tracked AGENTS/CLAUDE 及指南显式读取共同规则；不依赖本机忽略目录、私有绝对路径或隐含全局 hook。
- [x] AC3（R3/R5）：paper-audit 完整检查所需 sibling 布局在安装页和自身 SKILL.md 均可见；隔离 smoke 验证推荐完整布局无意外 missing，单 skill 模式标为覆盖受限，入口中英镜像一致。
- [x] AC4（R5/R6）：贡献者测试命令使用 C2 的统一入口，不再漏掉包内42项测试；安装器/软链接/五工具未实测处明确 UNVERIFIED。

## 非目标

不新增依赖，不发布，不改全局工具配置，不扩大到整体框架重构。未运行的能力不得写成已验证。
