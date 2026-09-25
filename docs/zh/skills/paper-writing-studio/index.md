# `paper-writing-studio`

按投稿 venue 路由的学术写作润色技能，带中性基线。它按一个显式 profile 润色或翻译学术文本，并逐字保留承载证据的 token。

## 适用场景

- 按 Nature、IEEE 或 Elsevier 风格润色单节或整篇稿件。
- 把中文学术文本译为英文，并保留数字和引用。
- 没有目标 venue 时，用中性 `unspecified` profile 润色学术英文。
- 报告 venue 冲突和缺失证据，不猜测 profile。

## 不适用场景

- LaTeX 或 Typst 的格式、编译、模板或字体；请用 `latex-paper-en`、`latex-thesis-zh` 或 `typst-paper`。
- 参考文献格式检查或文献检索；请用 `bib-search-citation`。
- 审稿式批评或评分；请用 `paper-audit`。
- 投稿信；请用 `cover-letter`。
- Zotero 写入或未经授权的文件输出。

## Profile 路由

| Profile       | 适用场景                                                                | 证据状态                                                                          |
| ------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `nature`      | 显式 venue `nature`，或 Nature 类 domain 键                             | `ref/nature-writing-studio/skill` 存在时加载其中的行；不存在时输出标记 `degraded` |
| `ieee`        | 显式 venue `ieee`、IEEE allowlist 中的期刊或 IEEE domain 键             | 只有路由元数据；输出标记 `degraded`                                               |
| `elsevier`    | 显式 venue `elsevier`、Elsevier allowlist 中的期刊或 Elsevier domain 键 | 只有路由元数据；输出标记 `degraded`                                               |
| `unspecified` | 没有 venue 信号，或没有安全映射                                         | 中性基线；`missing_evidence` 写明缺失的信号                                       |

profile 选择优先级为显式 venue > 期刊 allowlist > 明确 domain > `unspecified`。

## 最小输入

- `input_text`：需要润色或翻译的文本。
- `target`：节名，例如 `abstract`、`introduction`、`methods`、`results` 或 `discussion`。
- 可选的 `venue`、`journal` 与 `domain`。

## 脚本入口

| 文件              | 用途                                                                                           |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| `scripts/core.py` | 内部模块，无 CLI：`select_profile`、`canonical_section`、`protected_tokens` 与 `render_result` |
| `profiles/*.json` | 各 profile 的加载计划、节路由、机制与证据门                                                    |

## 输出产物

- inline Markdown，包含 `text`、`text_compact` 与 `summary`。用户未要求时不写文件。
- `summary` 记录 venue、profile 版本、节名、已应用规则、证据行、受保护 token、冲突、缺失证据与 `degraded` 标记。

## 跨工具执行

frontmatter 中的 `allowed-tools` 为 Claude 兼容元数据，在其他平台上不构成强制权限列表。把读取与搜索需求映射到当前会话已有的能力。

## 公开资源

### 示例

- [按 IEEE Transactions 改写引言](./resources/examples/ieee-introduction-rewrite.md)
- [按 Nature 风格润色摘要](./resources/examples/nature-abstract-polish.md)
- [未指定 venue 的中性润色](./resources/examples/unspecified-neutral-polish.md)

## 常见请求

```text
按 Nature 风格润色这个 abstract，保留数字和引用。
```

```text
按 IEEE Transactions 的写法改写这段 introduction，保留证据 token。
```

```text
按 Elsevier 过程控制论文的 experiments 改写，不要套用 Nature 的 Here we。
```

```text
没有目标期刊，先用中性学术英文润色，并列出缺失的 venue 证据。
```
