# bib-search-citation 双语文档实施计划

## Checklist

- [x] 读取当前 `SKILL.md`、Reference Map 和核心 manifest，确认动态资源数量。
- [x] 删除本技能旧的非规范 `resources` 路径并建立四类统一目录。
- [x] 将源资源放入其源语言页面，逐文件完成另一语言的完整翻译。
- [x] 保持 frontmatter、代码块、命令、路径、标识符、公式和引用键。
- [x] 修复所有相对链接并确认两种语言树结构一致。
- [x] 重写英文/中文技能概览并接入生成侧栏。
- [x] 更新本技能 manifest 的 source locale 与 source hash。
- [x] 运行单技能 checker，逐项处理差异，不添加 checker 例外。
- [x] 对指定高风险页面做并排人工复核。
- [x] 构建文档、检查 diff，仅提交本技能和任务工件。

## Validation

```powershell
rtk uv run python docs/scripts/check_resource_sync.py --skill bib-search-citation
rtk uv run pytest tests/contracts/test_docs_bilingual_resources.py -q
rtk npm --prefix docs run docs:build
rtk git diff --check
```

## Completion Gate

单技能 checker、构建和抽样复核全部通过后才可归档；不得以“父任务最终会修复”为由
遗留缺页、旧路径或未翻译原文。

## Verification Evidence

- `check_resource_sync.py --skill bib-search-citation`：通过，manifest 共 250 项。
- `tests/contracts/test_docs_bilingual_resources.py -q`：8 passed。
- `npm --prefix docs run docs:build`：VitePress 构建通过。
- `just ci`：Ruff、Pyright（0 errors）与 1157 项 pytest 测试通过。
- 六个英文资源逐文件与源文件一致；指定三份高风险中文译文已并排复核。
- 本任务路径的 `git diff --check`：通过；未修改无关 Trellis 运行时和 README 变更。
- Spec 判断：现有 `docs-bilingual-resources.md` 已覆盖本切片，没有新增契约需要同步。
