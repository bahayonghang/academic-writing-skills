# 双语技能资源文档契约

## 1. Scope / Trigger

增删或修改任一技能的公开 `references`、`templates`、`examples`、Markdown
`agents`，或者修改 `docs/skills/*/resources`、`docs/zh/skills/*/resources`、
资源侧栏时，必须遵守本契约。

`SKILL.md` 是能力与路由事实来源；源资源正文是详细规则事实来源。文档站不能从
旧页面反向推断技能行为。

## 2. Signatures

```powershell
# 仅校验完整源清单、manifest 字段/散列和规范目标路径
uv run python docs/scripts/check_resource_sync.py --inventory-only

# 完整校验一个已迁移技能
uv run python docs/scripts/check_resource_sync.py --skill <skill-name>

# 父任务/CI 完整校验全部技能
uv run python docs/scripts/check_resource_sync.py

# 源资源增删后重建 manifest；随后必须审查 sourceLocale 和译文
uv run python docs/scripts/check_resource_sync.py --write-manifest --inventory-only
```

## 3. Contracts

每个公开源文件对应 `docs/resource-manifest.json` 的一行：

| Field | Type | Contract |
| --- | --- | --- |
| `skill` | string | 六个公开技能目录名之一 |
| `kind` | string | `references` / `templates` / `examples` / `agents` |
| `source` | repo-relative path | 真实源文件，保持文件名大小写 |
| `sourceLocale` | enum | `en` / `zh` / `neutral`，逐文件判定 |
| `sourceSha256` | hex string | 当前源文件 SHA-256 |
| `en` | repo-relative path | `docs/skills/<skill>/resources/<kind>/...` |
| `zh` | repo-relative path | `docs/zh/skills/<skill>/resources/<kind>/...` |

公开源范围：`references/**/*.{md,yaml,yml}`、`templates/**/*.md`、
`examples/**/*.md`、`agents/**/*.md`。脚本、evals、fixtures 和
`agents/openai.yaml` 不进入文档资源树。

`sourceLocale=en|zh` 的同语言页面必须与源文件完全一致；另一语言页面做完整翻译。
`neutral` 资源两份都与源文件字节一致。Markdown 译文必须保留标题层级、代码块、
inline code token、链接目标和表格形状。

## 4. Validation & Error Matrix

| Condition | Required failure |
| --- | --- |
| 新增公开源文件但 manifest 无记录 | `manifest missing source` |
| 删除/移动源文件但 manifest 仍有记录 | `manifest has stale source` |
| 源内容变化但未更新散列 | `sourceSha256 ... expected ...` |
| 两条记录写入同一目标 | `duplicate target path` |
| 单技能缺少任一语言页面 | `missing en/zh target` |
| 同语言页面擅自改写源规则 | `<locale> target must match source exactly` |
| 译文改动命令、代码、链接或表格结构 | 对应 Markdown shape error |
| 旧目录或额外文件残留 | `unexpected or legacy resource` |

`--inventory-only` 只用于核心契约建立阶段，不能作为技能翻译或最终 CI 的完成证明。

## 5. Good / Base / Bad Cases

- Good：新增 `references/workflow.md` 后重建 manifest，校正 `sourceLocale`，同时添加
  英文和中文规范路径，运行 `--skill` 与 docs build。
- Base：只改源文件内容时更新 source-faithful 页面、另一语言译文和 manifest 散列。
- Bad：手工复制到旧 `resources/modules`，只改一套语言，或通过 checker ignore
  掩盖缺页。

## 6. Tests Required

- `tests/contracts/test_docs_bilingual_resources.py` 必须断言 live inventory 与 manifest
  完全一致，并验证规范路径。
- router 变化必须从 `SKILL.md` 解析，断言英中文 `usage.md` 同时包含新模块/模式。
- 安装面变化必须断言两种语言列出全部公开技能。
- Markdown 结构保护至少覆盖一个通过样例和一个技术 token 漂移失败样例。
- 最终运行单技能/全量 checker、VitePress build、Ruff、Pyright 与 pytest。

## 7. Wrong vs Correct

### Wrong

```text
docs/skills/latex-thesis-zh/resources/modules/conclusion.md
docs/zh/skills/latex-thesis-zh/resources/modules/conclusion.md  # 直接复制中文冒充英文
```

### Correct

```text
docs/skills/latex-thesis-zh/resources/references/modules/conclusion.md
docs/zh/skills/latex-thesis-zh/resources/references/modules/conclusion.md
```

两条路径结构相同，英文页为完整英文译文，中文页与中文源文件一致；manifest 记录
源散列和两条规范路径，侧栏从文件系统自动发现页面。
