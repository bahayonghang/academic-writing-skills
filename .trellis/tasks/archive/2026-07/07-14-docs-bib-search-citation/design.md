# bib-search-citation 双语文档设计

## Shared Contract

继承父任务 `design.md` 和核心子任务的 manifest、规范路径、侧栏与 checker 契约。
本任务只拥有 `docs/skills/bib-search-citation/`、`docs/zh/skills/bib-search-citation/` 及对应 manifest 行。

## Mapping

- `references/<path>` -> `resources/references/<path>`
- `templates/<path>` -> `resources/templates/<path>`
- `examples/<path>` -> `resources/examples/<path>`
- 公开 `agents/<path>` -> `resources/agents/<path>`

文件名与大小写保持源路径。源文件以英文为主，英文页保持源内容，中文页完整翻译。

## Translation Risk Controls

紧凑查询操作符、JSON 字段、BibTeX 字段、LaTeX/Typst 引用片段不得翻译或改写。

机器 frontmatter 的键、标识符与非展示值保持不变；可见说明文字按目标语言翻译。
内部链接在两种语言中指向同一相对资源位置。

## Review Sampling

至少复核 `references/query-syntax.md`、`references/limitations-and-errors.md`、`examples/raw-bib-export.md`，覆盖规范性规则、操作流程和示例三类内容。检查 MUST/禁止、
severity、警告和限制条件没有在翻译中弱化。

## Rollback

回滚仅限本技能两套文档子树和 manifest 行，不修改核心契约或其他技能。
