# `cover-letter`

面向已有 LaTeX 论文的投稿信助手。它负责生成、优化和核查写给编辑的投稿信，并把投稿信中的强 claim 绑定到论文可见证据上。

## 适用场景

- 根据 `main.tex` 生成投稿信初稿。
- 优化已有 `cover_letter.md` 或 `cover_letter.tex`，但不覆盖原文件。
- 检查 novelty、contribution、数字和范围 claim 是否超出论文证据。
- 判断投稿信是否适合内置期刊或会议模板。
- 做投稿前声明、长度、套话、AI-tone 和段落形态检查。

## 不适用场景

- 修改论文源码；请用 `latex-paper-en` 或 `latex-thesis-zh`。
- 做完整审稿式论文批评；请用 `paper-audit`。
- 检索文献库；请用 `bib-search-citation`。
- Typst 论文；当前版本只支持 LaTeX 论文。
- rebuttal 或 response-to-reviewer。

## 模式路由

| 模式 | 适用场景 | 主命令 |
| --- | --- | --- |
| `generate` | 有论文、没有投稿信草稿 | `uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode generate --manuscript main.tex --journal nature --json` |
| `optimize` | 已有草稿，需要更安全的表达 | `uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode optimize --letter cover_letter.md --manuscript main.tex --journal nature --json` |
| `align-check` | 需要核查投稿信 claim 是否被论文支撑 | `uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode align-check --letter cover_letter.md --manuscript main.tex --json` |
| `journal-fit` | 需要期刊/会议适配评分 | `uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode journal-fit --letter cover_letter.md --journal nature --json` |
| `presubmission` | 需要最终机械检查 | `uv run python academic-writing-skills/cover-letter/scripts/cover_letter.py --mode presubmission --letter cover_letter.md --journal nature --json` |

内置 venue：`nature`、`science`、`cell`、`ieee-trans`、`acm`、`springer-lncs`、`neurips`、`icml`、`cvpr`、`generic`。

## 最小输入

- `generate` 和 `align-check` 需要 `--manuscript main.tex`。
- `optimize`、`align-check`、`journal-fit`、`presubmission` 需要 `--letter cover_letter.md` 或 `--letter cover_letter.tex`。
- 期刊适配和投稿前规则建议提供 `--journal <venue>`。
- 需要机器可读结果时加 `--json`。

## 脚本入口

| 脚本 | 用途 |
| --- | --- |
| `cover_letter.py` | 五种模式的统一公开 CLI |
| `extract_manuscript_facts.py` | 从论文确定性抽取事实 |
| `build_letter_claim_map.py` | 提取投稿信 claim 清单 |
| `align_check.py` / `verify_letter_against_manuscript.py` | claim-evidence 核查 |
| `journal_fit_check.py` | venue-fit 评分 |
| `presubmission_check.py` | 声明、长度、套话和语气检查 |

## 输出产物

- `generate` 返回论文事实和确定性投稿信框架；缺失字段保留占位符。
- `optimize` 返回基于行号的建议和 claim-evidence 风险，不覆盖草稿。
- `align-check` 返回无支撑、范围过强或缺失证据的 claim findings。
- `journal-fit` 返回 HIGH / MEDIUM / LOW 维度评分和映射后的 findings。
- `presubmission` 返回声明、长度、套话、语气和段落形态的机械 findings。

findings 包含 `severity`、`priority`、`source_kind` 和 `comment_type`，脚本发现应可重复运行验证。

## 常见请求

```text
根据 main.tex 生成 Nature 投稿信，缺少的信息用占位符标出。
```

```text
帮我优化 cover_letter.md，目标是 IEEE Transactions，但不要直接改文件。
```

```text
检查这封投稿信里的每个强 claim 是否都被 main.tex 支撑。
```

```text
给这封 NeurIPS 投稿信用 journal-fit 打分，并指出最弱维度。
```

```text
投稿系统粘贴前，对 cover_letter.md 做最后的 presubmission 检查。
```
