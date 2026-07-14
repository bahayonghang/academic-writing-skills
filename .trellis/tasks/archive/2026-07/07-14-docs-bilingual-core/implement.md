# 核心双语文档契约实施计划

## Checklist

- [x] 读取父任务设计与 `docs/.vitepress/config.ts`，确认无用户并发改动。
- [x] 实现公开 source inventory 与规范路径映射。
- [x] 生成 manifest，逐文件校正 `sourceLocale`，语言无关文件标记 `neutral`。
- [x] 实现 checker 三种范围及清晰错误输出。
- [x] 添加路径、散列、标题层级、代码块、inline token、链接和表格形状测试。
- [x] 抽取递归资源侧栏生成器，删除手工资源条目但保留技能顶层顺序。
- [x] 重写双语核心入口页，并只链接新的规范资源路径。
- [x] 运行 inventory-only、定向 pytest 和 VitePress build。
- [x] 检查 diff 不含技能资源批量翻译及任务前已有改动。

## Validation

```powershell
rtk uv run python docs/scripts/check_resource_sync.py --inventory-only
rtk uv run pytest tests/contracts/test_docs_bilingual_resources.py -q
rtk npm --prefix docs run docs:build
rtk git diff --check
```

## Review Gate

开始首个技能子任务前，确认 manifest 覆盖 250 个当前公开资源、路径生成无碰撞、
checker 无隐式跳过，并记录实际动态计数。

## Verification Evidence

- `check_resource_sync.py --inventory-only`: 250 entries, passed.
- Targeted contract tests: 8 passed.
- Full pytest: 1157 passed.
- Ruff format/check: passed.
- Pyright: 0 errors, 73 pre-existing warnings.
- VitePress production build: passed.
- `just ci`: passed.
- `git diff --check`: passed after normalizing Markdown EOF newlines.
