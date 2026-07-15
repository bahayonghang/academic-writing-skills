# latex-thesis-zh 双语文档实施计划

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
rtk uv run python docs/scripts/check_resource_sync.py --skill latex-thesis-zh
rtk uv run pytest tests/contracts/test_docs_bilingual_resources.py -q
rtk npm --prefix docs run docs:build
rtk git diff --check
```

## Completion Gate

单技能 checker、构建和抽样复核全部通过后才可归档；不得以“父任务最终会修复”为由
遗留缺页、旧路径或未翻译原文。

## Verification Evidence

- `check_resource_sync.py --skill latex-thesis-zh`: passed，48 个源资源映射为 96 个双语页面。
- `pytest tests/contracts/test_docs_bilingual_resources.py -q`: 8 passed。
- `npm --prefix docs run docs:build`: VitePress build passed。
- `just ci`: 版本一致性、Ruff、Pyright 与完整 pytest 均通过。
- `git diff --check`: 通过；为同时满足源页逐字同步，已将源文件及双语页代码示例中的一处
  `% ` 尾随空格统一规范化为 `%`，并仅更新对应 manifest hash。
- 高风险抽样：燕山 58 项、清华 37 项、北大 35 项清单 ID 完整；GB/T 版本/日期、章节强约束、
  MUST/禁止语气、盲审 R1/R2 与 checker 代码均完成双语对照。
- Spec 判断：现有 `.trellis/spec/academic-writing-skills/docs-bilingual-resources.md` 已完整覆盖，
  本任务不新增共享契约。
