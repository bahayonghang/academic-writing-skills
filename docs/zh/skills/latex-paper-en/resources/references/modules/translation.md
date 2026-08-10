# 模块：翻译（中文 -> 英文）

**触发**：翻译、汉译英、双语润色、术语对齐

**目的**：将中文技术散文翻译成学术英语，同时保持 LaTeX 命令和数学片段完整。

## 命令

```bash
uv run python -B scripts/translate_academic.py "本文提出了一种基于Transformer的方法" --domain deep-learning
uv run python -B scripts/translate_academic.py input_zh.txt --domain industrial-control --output translation_report.md
```

## 原始脚本输出

该脚本返回四个部分：
- 术语确认表
- 翻译草稿
- 不明确的注释可能需要手动确认
- 一个 `### Contract` 块，携带与注释流模块相同的四个字段

受保护的片段，例如 `\cite{...}`、`\ref{...}` 和 `$...$`，在翻译前被遮蔽、在草稿中逐字还原；数量报告在 `Protected` 里。

```markdown
### Contract
- Changed: rule-based draft translation (2 glossary term(s) applied)
- Protected: 3 LaTeX/math span(s) masked and restored verbatim
- Meaning-Check: NEEDS-LLM
- Risk-Flags: not-assessed
- Envelope: goal=grammar strength=minimal
```

规则草稿永远不是成品译文：`Meaning-Check` 恒为 `NEEDS-LLM`；翻译时升高措辞强度（例如把留有余地的中文动词译成 `demonstrates`）同样属于过度声称——见 [over-claim-guard.md](../evidence/over-claim-guard.md)。字段定义见 [routing-rules.md](routing-rules.md)。

## 技能层响应

- 报告翻译的散文以及任何歧义注释。
- 除非用户明确要求，否则不要编辑或标准化 LaTeX 片段。
- 如果术语仍然含糊不清，请将不确定性暴露出来，而不是默默猜测。
- 对于混合主张、证据、条件、比较、含义和限制的中文长句，使用 [translation-guide.md](../writing/translation-guide.md) 中的“5.1 Translate Intent Before Syntax”。
- 对于先泛谈重要性或先列方法、后写研究缺口的结构，使用 [translation-guide.md](../writing/translation-guide.md) 中的“5.2 Structural Repairs”。

参考：[terminology.md](../writing/terminology.md), [翻译指南.md](../writing/translation-guide.md)
