# 模块：长句分析

**触发**：长句、长句、简化、分解、>50 个单词

触发条件：句子>50字或>3个从句

```bash
uv run python -B scripts/analyze_sentences.py main.tex
uv run python -B scripts/analyze_sentences.py main.tex --section introduction --max-words 45 --max-clauses 3
```

输出格式：
```latex
% LONG SENTENCE (Line 45, 67 words) [Severity: Minor] [Priority: P2]
% Core: [subject + verb + object]
% Subordinates:
%   - [Relative] which...
%   - [Purpose] to...
% Suggested: [simplified version]
```

