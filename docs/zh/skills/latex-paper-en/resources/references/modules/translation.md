# 模块：翻译（中文 -> 英文）

**触发**：翻译、汉译英、双语润色、术语对齐

**目的**：将中文技术散文翻译成学术英语，同时保持 LaTeX 命令和数学片段完整。

## 命令

```bash
uv run python -B scripts/translate_academic.py "本文提出了一种基于Transformer的方法" --domain deep-learning
uv run python -B scripts/translate_academic.py input_zh.txt --domain industrial-control --output translation_report.md
```

## 原始脚本输出

该脚本返回三个部分：
- 术语确认表
- 翻译草稿
- 不明确的注释可能需要手动确认

受保护的片段，例如`\cite{...}`, `\ref{...}`， 和`$...$`应在翻译草案中保留逐字保留。

## 技能层响应

- 报告翻译的散文以及任何歧义注释。
- 除非用户明确要求，否则不要编辑或标准化 LaTeX 片段。
- 如果术语仍然含糊不清，请将不确定性暴露出来，而不是默默猜测。

参考：[terminology.md](../writing/terminology.md), [翻译指南.md](../writing/translation-guide.md)
