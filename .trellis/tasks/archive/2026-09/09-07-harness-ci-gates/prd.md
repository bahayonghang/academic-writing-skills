# 补齐合并前质量检查与发布构建门禁

优先级：P1。父需求：R2/R3/R5。状态：planning。

## 目标与背景

deploy.yml:3-6 仅 release published 触发，:25-62 只有文档安装/构建；默认 pytest 收集 1714 项，just test 收集 1756 项。历史 run 27467312342 的两处死链接已被 7913cbb 修复，不能算当前 bug。

## 范围

- .github/workflows/ci.yml（新增）
- justfile
- pyproject.toml（仅 tool.pytest.ini_options）

## 前置与授权

C1 完成（避免同时修改 pyproject.toml）；用户批准。

当前仅规划，禁止 task.py start/实现/正式规则回写。任务树归属不代替前置条件。不同工作者不得覆盖其他子任务或用户改动。

## 验收条件

以下需求编号继承父任务的同名要求，本子任务负责其中与自身范围有关的交付。

- R2：检查覆盖完整并记录真实通过/失败/未验证证据。
- R3：改造有已复现失败或工作流缺口证据，不混同历史与当前。
- R5：文件范围、前置与检查可实施、可逐项验收。

- [x] AC1（R2/R5）：同一 pytest 配置覆盖根 tests 和技能目录；默认 pytest 与 just test 的收集 node-id 集合一致，保留既有 1756 项（新增项只允许增加）。
- [x] AC2（R3/R5）：新增 PR/push workflow 显式提供 Python/uv/just 并执行项目完整门禁，Windows/Ubuntu 和 Python 3.10/3.13 均有覆盖；UV_PYTHON 与matrix一致，失败阻止该 job 成功。
- [x] AC3（R3/R5）：文档 job 用 Node20 与 docs/package-lock.json，检查资源同步及 VitePress 构建。
- [x] AC4（R3）：release-only 部署触发和生产权限不变；不把仅本地检查称为 hosted 同 SHA 通过。

## 非目标

不新增依赖，不发布，不改全局工具配置，不扩大到整体框架重构。未运行的能力不得写成已验证。
