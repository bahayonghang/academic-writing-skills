# 示例：表达和翻译

用户请求：
润色`main.typ`中的摘要，收紧措辞，并帮助将一段中文段落翻译成学术英语。

推荐模块顺序：

1. `expression`
2. `translation`

命令：

```bash
# Polish the whole document (covers the abstract whether it is a heading,
# #abstract[..], or a template abstract: argument). Add --section <name>
# only when the target is a real heading section.
uv run python $SKILL_DIR/scripts/improve_expression.py main.typ
uv run python $SKILL_DIR/scripts/translate_academic.py input_zh.txt --domain deep-learning
```

预期输出：

- 打字员安全的措辞建议。
- 保持引文和 Typst 语法完整的翻译指南。
