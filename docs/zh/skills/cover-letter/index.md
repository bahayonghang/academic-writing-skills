# cover-letter

`cover-letter` 用于为已有 LaTeX 论文准备投稿信。它可以生成、优化、校验投稿信，但不会修改论文源文件。

## 什么时候使用

- 从 `main.tex` 生成投稿信初稿。
- 优化已有的 `cover_letter.md` 或 `cover_letter.tex`。
- 检查投稿信中的 claim 是否超出论文证据。
- 判断投稿信是否适合某个内置期刊 / 会议模板。
- 运行投稿前的声明、字数、套话、语气和段落检查。

## 统一 CLI

```bash
uv run python -B academic-writing-skills/cover-letter/scripts/cover_letter.py \
  --mode align-check \
  --manuscript main.tex \
  --letter cover_letter.md \
  --journal nature \
  --json
```

支持的模式：

| 模式 | 必需输入 | 输出 |
|---|---|---|
| `generate` | `--manuscript main.tex` | 论文事实提取结果 + 确定性投稿信框架 |
| `optimize` | `--letter cover_letter.md`；建议同时给 `--manuscript` | 机械检查与 claim-evidence findings |
| `align-check` | `--letter cover_letter.md --manuscript main.tex` | 无支撑或范围过强的 claim findings |
| `journal-fit` | `--letter cover_letter.md --journal <venue>` | HIGH / MEDIUM / LOW 维度评分与 findings |
| `presubmission` | `--letter cover_letter.md --journal <venue>` | 声明、字数、套话、语气、段落 findings |

## 输出协议

JSON finding 使用：

- `severity`: `major`、`moderate` 或 `minor`
- `priority`: `P1`、`P2` 或 `P3`
- `source_kind`: 通常是 `script`
- `comment_type`: `claim_accuracy`、`journal_fit`、`declaration_missing`、`presentation` 或 `tone`

`journal-fit` 保留 HIGH / MEDIUM / LOW 评分，并把 LOW 映射为 `major` / `P1`，MEDIUM 映射为 `moderate` / `P2`，HIGH 不产生问题。

## 边界

- 仅支持 LaTeX 论文源文件。
- 不修改 `main.tex`。
- 不写 rebuttal 或 response-to-reviewer。
- 除非明确要求，否则不联网抓取期刊最新政策；内置模板是 bundled snapshot。
