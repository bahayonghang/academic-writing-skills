# 核心双语文档契约设计

## Boundary

实现共享机制和核心页面，不声明任何技能资源已翻译完成。共享规则以父任务
`design.md` 为准。

## Components

1. `docs/resource-manifest.json`: 全量公开源文件的声明清单。
2. `docs/scripts/check_resource_sync.py`: inventory、单技能、全量检查入口。
3. `tests/contracts/test_docs_bilingual_resources.py`: 路径、结构和 checker 回归测试。
4. `docs/.vitepress/config.ts`: 从规范资源树递归生成资源侧栏。
5. 核心英文/中文页面：home、installation、quick-start、usage、skills index。

## Staged Check Contract

- `--inventory-only`: 校验 source inventory、manifest schema、source hash、目标路径；
  不要求翻译目标已经存在。仅核心子任务使用。
- `--skill <name>`: 对指定技能执行完整双语检查。技能子任务必须使用。
- 无范围参数: 对 manifest 全量执行完整检查。父任务最终验收使用。

不存在永久的 skip、ignore 或 pending 状态。分阶段豁免只来自显式 CLI 范围。

## Navigation

在 config 中保留人工编写的核心/技能顺序，资源项由 `resources` 文件树生成。
Markdown 成为页面；YAML 只作为可下载资产，不生成错误路由。生成结果按目录、标题
稳定排序，并在中文树读取中文 H1、英文树读取英文 H1。

## Failure Modes

- manifest 漏项：独立 inventory 推导失败。
- 路径大小写错误：Linux 构建或 checker 失败。
- 译文暂缺：inventory-only 允许，单技能/全量检查失败。
- 旧资源残留：单技能检查在该技能完成时失败。

## Rollback

核心契约一旦被技能子任务采用，不得单独回滚；需要连同所有依赖子任务回滚。
