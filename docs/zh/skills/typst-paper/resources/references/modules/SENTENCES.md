# 模块：长难句分析
**触发词**: long sentence, 长句, simplify, decompose, 拆解

**脚本用法**:
```bash
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ --max-words 50 --max-clauses 3
uv run python $SKILL_DIR/scripts/analyze_sentences.py main.typ --section introduction
```

> 可用 flag：`--section`、`--max-words`（默认 50）、`--max-clauses`（默认 3）。
> 没有 `--threshold`。

**触发条件**:
- 句子词数 > `--max-words`（默认 50） 或 从句数 > `--max-clauses`（默认 3）
- 句切分与计数以英文为准（按 `.!?` 切句、按词计长）

**输出格式**:
```typst
// LONG SENTENCE (Line 45, 67 words, 5 clauses) [Severity: Minor] [Priority: P2]
// Original: ...
// Suggested: ...
// Rationale: Sentence exceeds complexity threshold, split for readability.
```

**拆分策略**:
1. 识别主干结构
2. 提取修饰成分
3. 拆分为多个短句
4. 保持逻辑连贯性

