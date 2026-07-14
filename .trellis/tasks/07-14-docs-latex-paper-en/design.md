# latex-paper-en 双语文档设计

## Shared Contract

继承父任务 `design.md` 和核心子任务的 manifest、规范路径、侧栏与 checker 契约。
本任务只拥有 `docs/skills/latex-paper-en/`、`docs/zh/skills/latex-paper-en/` 及对应 manifest 行。

## Mapping

- `references/<path>` -> `resources/references/<path>`
- `templates/<path>` -> `resources/templates/<path>`
- `examples/<path>` -> `resources/examples/<path>`
- 公开 `agents/<path>` -> `resources/agents/<path>`

文件名与大小写保持源路径。源文件以英文为主，英文页保持源内容，中文页完整翻译。

## Translation Risk Controls

LaTeX 命令、citation anchors、venue 名称、module router、section-writing 结构和 de-AI 约束不得发生技术漂移。

机器 frontmatter 的键、标识符与非展示值保持不变；可见说明文字按目标语言翻译。
内部链接在两种语言中指向同一相对资源位置。

## Review Sampling

至少复核 `references/modules/routing-rules.md`、section-writing 的 introduction/method/conclusion、`references/deai/guide.md`、IEEE template，覆盖规范性规则、操作流程和示例三类内容。检查 MUST/禁止、
severity、警告和限制条件没有在翻译中弱化。

## Rollback

回滚仅限本技能两套文档子树和 manifest 行，不修改核心契约或其他技能。
