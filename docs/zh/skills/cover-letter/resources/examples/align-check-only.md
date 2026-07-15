# 示例：仅对齐检查

用户请求：
我已经写了一封投稿信；在发送之前检查是否有任何声明超出了我的论文稿件。

推荐模块顺序：

1. `align-check`

命令：

```bash
uv run python -B $SKILL_DIR/scripts/cover_letter.py --mode align-check --letter cover_letter.md --manuscript main.tex --json
```

预期输出：

- 对齐检查问题的 JSON 列表（或省略 `--json` 时的 LaTeX 注释块）。
- 对于每个不受支持的声明：准确的字母引用、稿件部分锚点（或 `none`）、`claim_strength` 标签、`missing_evidence` 数组以及保持在稿件范围内的 `allowed_wording` 重写。
- 退出代码 0（支持所有声明）、1（某些 `observed`/`unsupported`，但不是重大问题）或 2（至少一个重大严重性问题）。
